import subprocess

from .svc import svc


# --------------------
## holds all OS process related utility functions
class UtilsPs:
    # --------------------
    ## run a process in a bash shell
    #
    # @param cmd            the bash command to run
    # @param use_raw_log    generates logging lines without a prefix; Pycharm does allow clicking on dirs
    # @param working_dir    the working directory in which to execute the cmd
    # @param log_file       where to save the output
    # @return None
    def run_process(self, cmd, use_raw_log=False, working_dir=None, log_file=None):
        svc.gbl.rc = 0
        if working_dir is None:
            working_dir = svc.utils_fs.root_dir

        proc = subprocess.Popen(cmd,  # pylint: disable=consider-using-with
                                cwd=working_dir,
                                shell=True,
                                bufsize=0,
                                universal_newlines=True,
                                stdin=None,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        fp = None
        if log_file is not None:
            fp = open(log_file, 'w', encoding='utf-8', newline='\n')  # pylint: disable=consider-using-with

        lastline = ''
        lineno = 0
        while True:
            if lastline:
                if fp:
                    if use_raw_log:
                        fp.write(f'{lastline}')
                    else:
                        fp.write(f'{lineno: >3}] {lastline}')
                elif use_raw_log:
                    svc.log.raw(lastline.strip())
                else:
                    svc.log.output(lastline.strip(), lineno=lineno)
            retcode = proc.poll()
            if retcode is not None:
                break
            lastline = proc.stdout.readline()
            lineno += 1

        svc.gbl.rc = proc.returncode
        svc.gbl.overallrc += svc.gbl.rc

    # --------------------
    ## run a cmd and returns the rc and output
    #
    # @param cmd            the bash command to run
    # @param msys2          call the command from msys2 bash shell otherwise from windows shell
    # @return tuple: (return code, a string delimited by newlines)
    def run_cmd(self, cmd, msys2=False):
        shell = True
        if msys2:
            cmd = ['c:/msys64/usr/bin/bash', '-i', '-c', cmd]
            shell = False
            # TODO move location of bash to xplat.cfg

        result = subprocess.run(cmd,
                                check=False,
                                shell=shell,
                                bufsize=0,
                                universal_newlines=True,
                                stdin=None,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        return result.returncode, result.stdout.strip()
