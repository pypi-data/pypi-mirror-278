from .svc import svc


# --------------------
## perform the do_makefile operations
class DoMakefile:
    # --------------------
    ## do_build mainline.
    #
    # @param tech        technology: cpp, arduino
    # @param build_type  build type: debug or release
    # @param target      cmake target to build e.g. ut
    # @return None
    def run(self, target):
        svc.log.highlight(f'{svc.gbl.tag}: starting target:{target}...')

        # TODO
        # # generate CPIP files as needed
        # cpip = DoCpip()
        # cpip.gen(tech, build_type)

        self._run_make(target)

        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: target {target} rc={svc.gbl.rc}')

    # --------------------
    ## run a makefile target
    #
    # @param target      the make target to run e.g. ut
    # @return None
    def _run_make(self, target):
        cmd = f'make {target}'
        rc, out = svc.utils_ps.run_cmd(cmd)
        svc.gbl.rc += rc
        svc.log.num_output(out.split('\n'))
