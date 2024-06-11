import os

from .svc import svc


# --------------------
## perform the do_upload operation
class DoUpload:
    # --------------------
    ## do_upload mainline.
    #
    # @param tech        technology: arduino
    # @param build_type  build type: debug or release
    # @param target      cmake target to build e.g. ut
    # @return None
    def run(self, tech, build_type, target):
        if not build_type:
            build_type = 'debug'

        if build_type not in ['debug', 'release']:
            svc.gbl.rc += 1
            svc.log.err(f'{svc.gbl.tag}: unknown build_type:{build_type}, use one of: debug, release')

        if not tech:
            # default to xplat.cfg value
            tech = svc.cfg.mod_tech
        if not tech:
            # not set, the default to arduino
            tech = 'arduino'

        if not target:
            target = svc.cfg.mod_name

        svc.log.highlight(f'{svc.gbl.tag}: starting build_type:{build_type} target:{target}...')
        if tech in ['arduino']:
            self._run_upload(build_type, target)

        else:
            svc.gbl.rc += 1
            svc.log.err(f'{svc.gbl.tag}: unknown tech:{tech}, must be: arduino')

        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: build {build_type} rc={svc.gbl.rc}')

    # --------------------
    ## upload using the cmake target to upload
    #
    # @param build_type  build type: debug or release
    # @param target      cmake target to build, usually the app name
    # @return None
    def _run_upload(self, build_type, target):
        build_dir = f'cmake-build-{build_type}'
        if not os.path.isdir(build_dir):
            svc.gbl.rc += 1
            svc.log.err(f'{svc.gbl.tag}: build_dir not found: {build_dir}')
            return
        svc.log.highlight(f'{svc.gbl.tag}: load project for {build_type}')

        cmd = f'cmake --build "{build_dir}" --target "{target}-upload"'
        svc.utils_ps.run_process(cmd, use_raw_log=False)
        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: cmake upload {build_type} rc={svc.gbl.rc}')
