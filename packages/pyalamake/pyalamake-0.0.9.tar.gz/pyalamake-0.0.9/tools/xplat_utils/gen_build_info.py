import os
import re
import sys

from .os_specific import OsSpecific
from .svc import svc


# --------------------
## generates the build_info information
class GenBuildInfo:
    # --------------------
    ## constructor
    def __init__(self):
        ## the file pointer for the build_info file
        self._fp = None
        ## the path to the build_info file
        self._path = None
        ## the overall exit return code
        self._exitrc = 0
        ## holds the original logger verbosity
        self._orig_verbose = True

    # --------------------
    ## initialize
    #
    # @param path     the path to the build_info file
    # @param verbose  whether to log to stdout or not
    # @return None
    def init(self, path, verbose):
        self._path = path
        self._orig_verbose = svc.log.verbose
        svc.log.verbose = verbose

        self._fp = open(self._path, 'w', encoding='utf-8', newline='\n')  # pylint: disable=consider-using-with

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        if self._fp is not None:
            self._fp.close()
        svc.log.verbose = self._orig_verbose

    # --------------------
    ## generate all build info
    #
    # @param version   the module/app version
    # @return error return code
    def gen(self, version):
        self._gen_init(version)
        self._gen_git_sha()
        self._gen_git_branch()
        self._gen_uncommitted_changes()
        self._gen_unpushed_commits()
        if svc.cfg.mod_tech != 'python':
            self._writeln('    === */')

        return self._exitrc

    # --------------------
    ## generate common build values
    #
    # @param version   the module/app version
    # @return None
    def _gen_init(self, version):
        if svc.cfg.mod_tech == 'python':
            self._writeln('class BuildInfo:  # pylint: disable=too-few-public-methods')
        else:
            self._writeln('/* === Build Info:')

        m = re.search(r'^(\d+\.\d+\.\d+) ', sys.version)
        self._set('python version', 'python_version', m.group(1))
        self._set('OS name', 'os_name', f'{os.name}:{OsSpecific.os_name}')

        # ensure file is created & flushed here so the import works cleanly
        self._fp.flush()

        self._set('version', 'version', version)

    # --------------------
    ## set the value in BuildInfo object
    #
    # @param tag    tag for logging
    # @param name   the name of the variable
    # @param val    the value of the variable
    # @return None
    def _set(self, tag, name, val):
        svc.log.ok(f'{tag: <25}: {val}')
        self._writeln(f'    {name} = \'{val}\'')

    # --------------------
    ## set a list of value in BuildInfo object
    #
    # @param name   the name of the list variable
    # @param items  the values of the list variable
    # @return None
    def _setlist(self, name, items):
        self._writeln(f'    {name} = [')
        for item in items:
            self._writeln(f'        \'{item}\',')
        self._writeln('    ]')

    # --------------------
    ## write a line to the build_info file
    # ensures it is terminated with a linefeed
    #
    # @param line  the line to write
    # @return None
    def _writeln(self, line):
        self._fp.write(f'{line}\n')

    # --------------------
    ## gen the current git SHA for the latest commit
    #
    # @return None
    def _gen_git_sha(self):
        tag = 'git SHA'
        rc, out = svc.utils_ps.run_cmd('git rev-parse --verify HEAD')
        self._exitrc += rc

        if rc != 0:
            svc.log.err(f'{tag: <25}: cmd failed: rc={rc}')
            return

        self._set(tag, 'git_sha', out)

    # --------------------
    ## gen the current branch name
    #
    # @return None
    def _gen_git_branch(self):
        tag = 'git branch'

        rc, out = svc.utils_ps.run_cmd('git rev-parse --abbrev-ref HEAD')
        self._exitrc += rc

        if rc != 0:
            svc.log.err(f'{tag: <25}: cmd failed: rc={rc}')
            return

        self._set(tag, 'git_branch', out)

    # --------------------
    ## show any uncommitted changes
    #
    # @return None
    def _gen_uncommitted_changes(self):
        tag = 'git uncommitted changes'
        rc, out = svc.utils_ps.run_cmd('git status -s')
        self._exitrc += rc

        if rc != 0:
            svc.log.err(f'{tag: <25}: cmd failed: rc={rc}')
            return

        uncommitted = []
        count = self._get_failed_lines(tag, out, uncommitted, 'has uncommitted changes')
        self._exitrc += count

        self._setlist('git_uncommitted', uncommitted)

    # --------------------
    ## show any unpushed commits
    #
    # @return None
    def _gen_unpushed_commits(self):
        tag = 'git unpushed commits'
        rc, out = svc.utils_ps.run_cmd('git cherry -v')
        self._exitrc += rc

        if rc != 0:
            svc.log.err(f'{tag: <25}: cmd failed: rc={rc}')
            return

        unpushed = []
        count = self._get_failed_lines(tag, out, unpushed, 'has unpushed changes')
        self._exitrc += count

        self._setlist('git_unpushed', unpushed)

    # --------------------
    ## gather and report failed lines in the given result lines
    #
    # @param tag           the logging tag
    # @param out           the output lines
    # @param failed_lines  the list to append any failed lines
    # @param suffix        the logging suffix if a warning occurs
    # @return the number of failed lines
    def _get_failed_lines(self, tag, out, failed_lines, suffix):
        header = False
        count = 0
        for line in out.split('\n'):
            if line != '':
                count += 1
                if not header:
                    svc.log.warn(f'{tag: <25}:')
                    header = True
                failed_lines.append(line)
                svc.log.warn(f'    {line}')

        if count == 0:
            svc.log.ok(f'{tag: <25}: none')
        else:
            svc.log.warn(f'{tag: <25}: {suffix}')
        return count
