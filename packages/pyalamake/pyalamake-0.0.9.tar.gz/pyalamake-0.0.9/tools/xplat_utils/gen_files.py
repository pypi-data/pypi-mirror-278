import json
import os

from .gen_build_info import GenBuildInfo
from .svc import svc


# --------------------
## perform gen files operations
class GenFiles:
    # --------------------
    ## generate all files
    #
    # @param verbose  the logging verbosity
    # @return None
    def all(self, verbose):
        if svc.cfg.mod_tech == 'python':
            self.version_json()
            self.build_info_file(verbose)
        elif svc.cfg.mod_tech in ['cpp', 'arduino']:
            self.version_h(verbose)
            self.build_info_txt(verbose)

    # --------------------
    ## generate the version.json file in the module/app directory
    #
    # @return None
    def version_json(self):
        filedir = os.path.join('lib', 'version.json')
        if svc.cfg.is_module:
            mod_dir = os.path.join(svc.utils_fs.root_dir, svc.cfg.mod_dir_name)
            if not os.path.isdir(mod_dir):
                svc.log.warn(f'version_json: dir does not exist: {mod_dir}')
                svc.gbl.rc = 1
                return

            path = os.path.join(str(mod_dir), filedir)
        else:
            path = os.path.join(svc.utils_fs.root_dir, filedir)

        # generate version.json
        version = {'version': svc.cfg.version}
        with open(path, 'w', encoding='utf-8', newline='\n') as fp:
            json.dump(version, fp, indent=4)

        if os.path.isfile(path):
            svc.gbl.rc = 0
        else:
            svc.gbl.rc = 1

        msg = f'gen: version_json rc={svc.gbl.rc}'
        if not svc.gbl.verbose:
            svc.log.line(msg)
        elif svc.gbl.rc == 0:
            svc.log.ok(msg)
        else:
            svc.log.warn(msg)
        svc.gbl.overallrc += svc.gbl.rc

    # --------------------
    ## generate the build_info.py file in the module/app source directory
    #
    # @param verbose  whether to generate the log line prefix
    # @return None
    def build_info_file(self, verbose):
        # Note: do not use svc.glb.verbose
        filedir = os.path.join('lib', 'build_info.py')
        if svc.cfg.is_module:
            mod_dir = os.path.join(svc.utils_fs.root_dir, svc.cfg.mod_dir_name)
            if not os.path.isdir(mod_dir):
                svc.log.warn(f'build_info_file: dir does not exist: {mod_dir}')
                svc.gbl.rc = 1
                return

            path = os.path.join(str(mod_dir), filedir)
        else:
            path = os.path.join(svc.utils_fs.root_dir, filedir)

        binfo = GenBuildInfo()
        binfo.init(path, verbose)
        svc.gbl.rc = binfo.gen(svc.cfg.version)
        binfo.term()

        msg = f'gen: build_info_file rc={svc.gbl.rc}'
        if not verbose:
            svc.log.line(msg)
        elif svc.gbl.rc == 0:
            svc.log.ok(msg)
        else:
            svc.log.warn(msg)
        svc.gbl.overallrc += svc.gbl.rc

    # ---------------------
    ## generate version.h for cpp/arduino
    #
    # @param verbose  the logging verbosity
    # @return None
    def version_h(self, verbose):  # pylint: disable=unused-argument
        if svc.cfg.is_module:
            path = os.path.join('lib', 'version.h')
        else:
            path = os.path.join('src', 'version.h')

        with open(path, 'w', encoding='utf-8', newline='\n') as fp:
            fp.write('#ifndef VERSION_H\n')
            fp.write('#define VERSION_H\n')
            fp.write(f'static const char version[] = "{svc.cfg.version}";\n')
            fp.write('#endif //VERSION_H\n')

        if os.path.isfile(path):
            svc.gbl.rc = 0
        else:
            svc.gbl.rc = 1

        msg = f'gen: version.h rc={svc.gbl.rc}'
        if not svc.gbl.verbose:
            svc.log.line(msg)
        elif svc.gbl.rc == 0:
            svc.log.ok(msg)
        else:
            svc.log.warn(msg)
        svc.gbl.overallrc += svc.gbl.rc

    # ---------------------
    ## generate build_info.txt file
    #
    # @param verbose  the logging verbosity
    # @return None
    def build_info_txt(self, verbose):
        if svc.cfg.is_module:
            path = os.path.join('lib', 'build_info.txt')
        else:
            path = os.path.join('src', 'build_info.txt')

        binfo = GenBuildInfo()
        binfo.init(path, verbose)
        svc.gbl.rc = binfo.gen(svc.cfg.version)
        binfo.term()
