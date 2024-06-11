import os
import sys

from .cfg import Cfg
from .do_build import DoBuild
from .do_check import DoCheck
from .do_clean import DoClean
from .do_coverage import DoCoverage
from .do_cpip import DoCpip
from .do_doc import DoDoc
from .do_lint import DoLint
from .do_makefile import DoMakefile
from .do_makefile_coverage import DoMakefileCoverage
from .do_post_ver import DoPostVer
from .do_publish import DoPublish
from .do_upload import DoUpload
from .do_ver_info import DoVerInfo
from .gen_files import GenFiles
from .svc import svc
from .utils_fs import UtilsFs
from .utils_logger import UtilsLogger
from .utils_ps import UtilsPs
from .utils_val import UtilsVal


# --------------------
## holds mainline for all utilities
class Utils:
    # --------------------
    ## create the output directory
    #
    # @return None
    def create_outdir(self):
        self._init('create_out_dir')
        svc.utils_fs.create_outdir()
        # Note: no _term()

    # --------------------
    ## recreate subdirectory in output directory
    #
    # @param dst the subdirectory to create
    # @return None
    def recreate_outsubdir(self, dst):
        self._init('recreate_outsubdir')
        svc.utils_fs.clean_out_dir(dst)
        # Note: no _term()

    # --------------------
    ## gen bash set_cfg.sh file for use in bash scripts
    #
    # @param verbose     True for additional verbosity
    # @return None
    def gen_bash_cfg(self, verbose):
        self._set_params(verbose)
        self._init('gen_bash_cfg')

        path = os.path.join('tools', 'set_cfg.sh')
        with open(path, 'w', encoding='utf-8', newline='\n') as fp:
            fp.write('#! /usr/bin/env bash\n')

            val = svc.utils_val.get_cfg('mod_name')
            fp.write(f'export cmn_mod_name="{val}"\n')

            val = svc.utils_val.get_cfg('mod_dir_name')
            fp.write(f'export cmn_mod_dir_name="{val}"\n')

            val = str(svc.utils_fs.convert_relative_to_abs(svc.gbl.outdir))
            fp.write(f'export OUT_DIR="{val}"\n')

            val = svc.utils_val.get_cov_opts()
            fp.write(f'export COV_OPTS="{val}"\n')

    # --------------------
    ## takes the given path and converts it a path relative to home, e.g,
    # * ~/out    => ~/out
    # * ./out    => ~/projects/proj1/out
    # * out      => ~/projects/proj1/out
    #
    # @param path the path to convert
    # @return the converted path
    def convert_relative_to_home(self, path):
        path1 = os.path.expanduser(path)
        path2 = os.path.abspath(path1)
        homedir = os.path.expanduser('~')
        path3 = path2.replace(homedir, '~')
        return path3

    # --------------------
    ## initialze cfg values and generate version.json
    #
    # @param verbose True for additional verbosity
    # @return None
    def gen_files(self, verbose):
        self._set_params(verbose)
        self._init('gen_files')
        svc.gen_files.all(verbose)
        # Note: no _term()

    # --------------------
    ## mainline for the do_clean operation.
    # removes all generated files and subdirectories.
    # The root directory should be equivalent to a clean git clone
    #
    # @param verbose True for additional verbosity
    # @param depth   cleaning action depth: full, lite
    # @return None
    def do_clean(self, verbose, depth=''):
        self._set_params(verbose)
        self._init('do_clean')
        impl = DoClean()
        impl.run(verbose=verbose, depth=depth)
        self._term(verbose)

    # --------------------
    ## mainline for the do_check operation.
    # checks all versions
    #
    # @param verbose True for additional verbosity
    # @return None
    def do_check(self, verbose):
        self._set_params(verbose)
        self._init('do_check')
        impl = DoCheck()
        impl.run()
        self._term(verbose)

    # --------------------
    ## mainline for the do_doc operation.
    # runs doxygen on all files specified in Doxyfile
    #
    # @param verbose   True for additional verbosity
    # @param make_pdf  generate the PDF (default) or not (False)
    # @return None
    def do_doc(self, verbose, make_pdf=True):
        self._set_params(verbose)
        self._init('do_doc')
        impl = DoDoc()
        impl.run(make_pdf)
        self._term(verbose)

    # --------------------
    ## mainline for the do_lint operation.
    # runs pylint on all given source files
    #
    # @param verbose True for additional verbosity
    # @param tech  the technology: python, cpp/arduino
    # @param tool  for cpp/arduino use clang-tidy or cppcheck
    # @return None
    def do_lint(self, verbose, tech=None, tool=None):
        self._set_params(verbose)
        self._init('do_lint')
        impl = DoLint()
        impl.run(tech, tool)
        self._term(verbose)

    # --------------------
    ## mainline for the do_build operation.
    # runs cmake on source files
    #
    # @param verbose     True for additional verbosity
    # @param build_type  build type: debug or release
    # @param tech        technology: cpp or arduino
    # @param target      the cmake target to build e.g. ut
    # @return None
    def do_build(self, verbose, build_type='debug', tech=None, target=None):
        self._set_params(verbose)
        self._init('do_build')
        impl = DoBuild()
        impl.run(tech, build_type, target)
        self._term(verbose)

    # --------------------
    ## mainline for the do_upload operation.
    # uploads a binary image to a microcontroller board
    #
    # @param verbose     True for additional verbosity
    # @param build_type  build type: debug or release
    # @param tech        technology: arduino
    # @param target      the cmake target to upload, usually the arduino app name
    # @return None
    def do_upload(self, verbose, build_type='debug', tech='arduino', target=None):
        self._set_params(verbose)
        self._init('do_upload')
        impl = DoUpload()
        impl.run(tech, build_type, target)
        self._term(verbose)

    # --------------------
    ## mainline for the do_ut operation.
    # runs cmake on source files
    #
    # @param verbose     True for additional verbosity
    # @param build_type  build type: debug or release
    # @param tech        technology: python, cpp or arduino
    # @return None
    def do_ut(self, verbose, build_type='debug', tech=None):
        self._set_params(verbose)
        self._init('do_ut')
        impl = DoBuild()
        impl.run(tech, build_type, target='ut')
        self._term(verbose)

    # --------------------
    ## mainline for the do_makefile_ut operation.
    #
    # @param verbose     True for additional verbosity
    # @return None
    def do_makefile(self, verbose, target):
        self._set_params(verbose)
        self._init('do_makefile')
        impl = DoMakefile()
        impl.run(target)
        self._term(verbose)

    # --------------------
    ## mainline for the do_publish operation.
    # generate the setup.py file
    #
    # @param verbose     True for additional verbosity
    # @return None
    def do_publish(self, verbose):
        self._set_params(verbose)
        self._init('do_publish')
        impl = DoPublish()
        impl.run()
        # script also reports overallrc; set verbose to False to prevent
        self._term(False)

    # --------------------
    ## mainline for the do_publish operation.
    # post the verification data
    #
    # @param verbose     True for additional verbosity
    # @return None
    def do_post_ver(self, verbose):
        self._set_params(verbose)
        self._init('do_post_ver')
        impl = DoPostVer()
        impl.run()
        self._term(verbose)

    # --------------------
    ## mainline for the do_ver_info operation.
    # generate version info files
    #
    # @param verbose     True for additional verbosity
    # @return None
    def do_ver_info(self, verbose):
        self._set_params(verbose)
        self._init('do_post_ver')
        impl = DoVerInfo()
        impl.run()
        self._term(verbose)

    # --------------------
    ## mainline for the do_cpip operation.
    #
    # @param verbose     True for additional verbosity
    # @param action      publish or pull
    # @return None
    def do_cpip(self, verbose, action):
        self._set_params(verbose)
        self._init('do_cpip')
        impl = DoCpip()
        impl.run(action)
        self._term(verbose)

    # --------------------
    ## mainline for the do_coverage operation.
    #
    # @param verbose     True for additional verbosity
    # @param action      reset or gen
    # @return None
    def do_coverage(self, verbose, action=None):
        self._set_params(verbose)
        self._init('do_coverage')
        impl = DoCoverage()
        impl.run(action)
        self._term(False)

    # --------------------
    ## mainline for the do_makefile_coverage operations.
    #
    # @param verbose     True for additional verbosity
    # @param action      reset or gen
    # @return None
    def do_makefile_coverage(self, verbose, action, target):
        self._set_params(verbose)
        self._init('do_makefile_coverage')
        impl = DoMakefileCoverage()
        impl.run(action, target)
        self._term(False)

    # --------------------
    ## check if any python pip modules are out of date
    #
    # @param verbose     True for additional verbosity
    # @return None
    def pip_outofdate(self, verbose):
        self._set_params(verbose)
        self._init('pip_outofdate')
        svc.log.line('out of date modules in tools/requirements.txt')
        # Note: old 'pip3 install --upgrade -r tools/requirements.txt --dry-run --quiet'
        cmd = 'pip3 list --outdated'
        svc.utils_ps.run_process(cmd)
        svc.log.check(svc.gbl.rc == 0, f'out of date rc={svc.gbl.rc}')

    # == support functions related

    # --------------------
    ## set the class parameters used to run mainline functions
    #
    # @param verbose       whether the function should run with verbose logging or not
    # @return None
    def _set_params(self, verbose):
        svc.gbl.verbose = verbose

    # --------------------
    ## initialization.
    # sets logging tag and overallrc to 0
    #
    # @param tag  the logging tag to use
    # @return None
    def _init(self, tag):
        svc.gbl.tag = tag
        svc.gbl.rc = 0
        svc.gbl.overallrc = 0

        # must be before Cfg, etc.
        svc.log = UtilsLogger

        svc.cfg = Cfg
        svc.utils_fs = UtilsFs()
        svc.utils_ps = UtilsPs()
        svc.gen_files = GenFiles()
        svc.utils_val = UtilsVal()

        # load cfg if necessary
        svc.cfg.load(svc.utils_fs.root_dir)

    # --------------------
    ## terminate.
    # reports overall rc
    #
    # @param verbose  flag for log verbosity
    # @return None
    def _term(self, verbose=True):
        # hack; some functions are not setting overallrc correctly
        if svc.gbl.overallrc == 0 and svc.gbl.rc != 0:
            svc.gbl.overallrc = svc.gbl.rc

        if verbose:
            svc.log.check(svc.gbl.overallrc == 0, f'{svc.gbl.tag}: overall rc={svc.gbl.overallrc}')
        sys.exit(svc.gbl.overallrc)
