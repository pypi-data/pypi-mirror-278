import filecmp
import json
import os
import shutil

import requests

from .os_specific import OsSpecific
from .svc import svc


# --------------------
## perform the do_publish using cpip operation.
class DoCpip:
    # --------------------
    ## constructor
    def __init__(self):
        OsSpecific.init()

        ## location of the staging local directory
        self._staging_dir = 'staging'
        ## the location of the cpip directory (may have ~ in it)
        self._cpip_root_dir = os.path.expanduser(svc.cfg.cpip.root_dir)
        # make sure root dir exists
        self._check_dir_exists(self._cpip_root_dir)

    # --------------------
    ## do_cpip mainline
    #
    # @param action  the action to take: pull or publish
    # @return None
    def run(self, action):
        svc.log.highlight(f'{svc.gbl.tag}: starting cpip: {action} ...')
        if action == 'publish':
            self._do_staging()
            self._push_local()
        elif action == 'pull':
            self._pull_remote_to_local()
        else:
            svc.abort(f'{svc.gbl.tag}: action is invalid: {action}, expected publish or pull')

    # === publish functions

    # --------------------
    ## stage all content ready for a push
    #
    # @return None
    def _do_staging(self):
        svc.log.highlight(f'{svc.gbl.tag}: staging content for push...')

        cpip_json = self._get_cpip_json()

        # content for staging/cpip.json
        packages_json = self._get_packages_json()
        self._update_cpip_json(cpip_json, packages_json)

        # uncomment to debug
        # svc.log.dbg(f'{svc.gbl.tag}: cpip_json: {json.dumps(cpip_json, indent=4)}')

        # for each item in updated cpip_json: copy to ./staging
        for _, pkgdata in cpip_json.items():
            stg_pkg_dir = os.path.join(self._staging_dir, pkgdata['dst'])
            # svc.log.dbg(f'  stg_pkg_dir: {stg_pkg_dir}')
            self._check_dir_exists(stg_pkg_dir)
            self._copy_pkg_files(stg_pkg_dir, pkgdata)

        # uncomment to debug
        # svc.log.dbg(f'{svc.gbl.tag}: cpip_json: {json.dumps(cpip_json, indent=4)}')

        # save the updated cpip.json file
        path = os.path.join(self._staging_dir, 'cpip.json')
        with open(path, 'w', encoding='utf-8') as fp:
            json.dump(cpip_json, fp, indent=4)

    # --------------------
    ## copy pkg files to the staging directory.
    #
    # @param pkg_dir   the pkg directory for the source
    # @param pkgdata   the rest of the package data
    # @return None
    def _copy_pkg_files(self, pkg_dir, pkgdata):
        lib_cfged = False
        if 'lib.src' in pkgdata:
            lib_cfged = True
            src_files = pkgdata['lib.src']
        else:
            src_files = pkgdata['src']

        # svc.log.dbg(f'  src files: {src_files} cfged:{lib_cfged}')

        for _, file in enumerate(src_files):
            # the files lib_src_files are relative to lib directory
            src = os.path.join('lib', file)
            if lib_cfged:
                staging_dst = os.path.join(pkg_dir, pkgdata['src'][0])
            else:
                staging_dst = os.path.join(pkg_dir, file)
            # svc.log.dbg(f'    [{idx: >3}] src: {src: <25} stg dst: {staging_dst}')

            self._check_path_dir_exists(staging_dst)

            # at this point the dst directory exists, the file may or may not exist
            if os.path.isfile(staging_dst):
                # the file exists, check if it is the same content
                if filecmp.cmp(src, staging_dst, shallow=False):
                    # same content, skip the copy
                    # svc.log.dbg(f'    same content, skipping {src}')
                    continue

            # either the file didn't exist or it has changed, so copy it
            svc.log.line(f'    cp : {src: <25} to {staging_dst}')
            shutil.copy(src, str(staging_dst))

        if 'lib.src' in pkgdata:
            del pkgdata['lib.src']

    # --------------------
    ## update cpip_json with new packages info.
    # if it's a new package add a new item
    # otherwise replace the existing package info
    #
    # @param cpip_json       the json holding cpip data
    # @param packages_json   the json holding the creator proj's data
    # @return None
    def _update_cpip_json(self, cpip_json, packages_json):
        for pkg, pkgdata in packages_json.items():
            cpip_json[pkg] = pkgdata
            cpip_json[pkg]['src-proj'] = svc.cfg.mod_name

    # --------------------
    ## push staging dir content to local CPIP directory
    #
    # @return None
    def _push_local(self):
        svc.log.highlight(f'{svc.gbl.tag}: pushing to local {svc.cfg.cpip.root_dir} ...')

        # at this point, staging exists, cpip_root_dir exists

        src = self._staging_dir
        dst = self._cpip_root_dir

        # use rsync to transfer
        # -r recursive
        # -c use a different checksum to trigger a push (not mod-time or size change)
        # -h use human-readable numbers
        # -i output a change-summary instead of continuous output
        cmd = f'rsync -rchi  {src}/ {dst}/'
        svc.log.line(f'push_local: {cmd}')
        svc.utils_ps.run_process(cmd, use_raw_log=False)

    # === clone/pull functions: copy from remote server

    # --------------------
    ## copy all files from remote to local cpip directory
    #
    # @return None
    def _pull_remote_to_local(self):
        svc.log.highlight(f'{svc.gbl.tag}: pulling from server to local {svc.cfg.cpip.root_dir} ...')

        requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member

        svc.log.line(f'{svc.gbl.tag}: pulling from: {svc.cfg.cpip.server_root} to '
                     f'{self._cpip_root_dir} for platform: {OsSpecific.os_name}')

        # download cpip.json here
        self._download_file('cpip.json')
        cpip_json = self._get_cpip_json()

        # go through all entries in cpip
        for pkg, pkgdata in cpip_json.items():
            # svc.log.dbg(f'pkg:{pkg} {pkgdata}')

            if OsSpecific.os_name not in pkgdata['platforms'] and pkgdata['platforms'] != ['all']:
                svc.log.line(f'{svc.gbl.tag}: pkg: {pkg} skipping, only for {pkgdata["platforms"]}')
                continue

            svc.log.line(f'{svc.gbl.tag}: pkg: {pkg} pulling...')
            for src in pkgdata['src']:
                file = os.path.join(pkgdata['dst'], src)
                svc.log.line(f'   > {file}')

                self._download_file(file)

    # --------------------
    ## download file from the server
    #
    # @param file   the file to download
    # @return None
    def _download_file(self, file):
        url = f'{svc.cfg.cpip.server_root}/{file}'
        local_path = os.path.join(self._cpip_root_dir, file)

        try:
            with requests.get(url, stream=True, verify=False, timeout=5) as rsp:
                rsp.raise_for_status()
                with open(local_path, 'wb') as fp:
                    shutil.copyfileobj(rsp.raw, fp)
        except requests.exceptions.HTTPError as excp:
            svc.log.err(excp)

    # === gen functions: used in ut and build (via cmake)

    # --------------------
    ## gen Findcpip.cmake file
    #
    # @param tech         technology: cpp, arduino (note: currently not used)
    # @param build_type   build type: debug or release (note: currently not used)
    # @return None
    def gen(self, tech, build_type):  # pylint: disable=unused-argument
        # TODO get rid of tech and build_type?
        svc.gbl.rc = 0

        if getattr(svc.cfg.cpip, 'packages', None) is None:
            svc.abort(f'{svc.gbl.tag}: packages is not defined in [cpip] section')

        path = os.path.join('Findcpip.cmake')
        with open(path, 'w', encoding='utf-8', newline='\n') as fp:
            # gen cmake variables for directories
            fp.write(f'set(CPIP_ROOT_DIR {self._cpip_root_dir})\n')
            fp.write(f'set(CPIP_INCLUDE_DIR {self._cpip_root_dir})\n')
            # add additional directories here...
            fp.write('\n')

            # have cmake print them out
            fp.write('message(STATUS "home dir        : ${HOME_DIR}")\n')
            fp.write('message(STATUS "cpip root dir   : ${CPIP_ROOT_DIR}")\n')
            fp.write('message(STATUS "cpip include dir: ${CPIP_INCLUDE_DIR}")\n')
            fp.write('\n')

            self._gen_package_info(fp)

        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: rc={svc.gbl.rc}')
        svc.gbl.overallrc += svc.gbl.rc

    # --------------------
    ## generate package info in cmake format.
    #
    # @param fp  the file pointer for the output file
    # @return None
    def _gen_package_info(self, fp):
        # check each package in xplat.cfg against the cpip content
        cpip = self._get_cpip_json()

        self._check_packages(cpip)
        if svc.gbl.rc != 0:
            return

        # generate the source list for all packages
        for pkg in svc.cfg.cpip.packages:
            fp.write('set(CPIP_SRC\n')
            for file in cpip[pkg]['src']:
                dst_dir = cpip[pkg]['dst']
                if cpip[pkg]['dst'] == '.':
                    fp.write(f'        ${{CPIP_INCLUDE_DIR}}/{file}\n')
                else:
                    fp.write(f'        ${{CPIP_INCLUDE_DIR}}/{dst_dir}/{file}\n')
            fp.write(')\n')

    # === common functions

    # --------------------
    ## check that all packages named in xplat packages section are valid
    #
    # @param cpip  the content of the cpip directory
    # @return None
    def _check_packages(self, cpip):
        for pkg in svc.cfg.cpip.packages:
            if pkg not in cpip:
                svc.log.err(f'{svc.gbl.tag}: unknown pkg: {pkg}')
                svc.gbl.rc += 1
                continue

    # --------------------
    ## load the local directory cpip.json file
    #
    # @return the cpip json content
    def _get_cpip_json(self):
        path = os.path.join(self._cpip_root_dir, 'cpip.json')
        if not os.path.isfile(path):
            svc.abort(f'{svc.gbl.tag}: cpip.json does not exist: {path}')

        with open(path, 'r', encoding='utf-8') as fp:
            cpip = json.load(fp)
            return cpip

    # --------------------
    ## load the local directory packages.json file (for creator projects)
    #
    # @return the packages json content
    def _get_packages_json(self):
        path = os.path.join('lib', 'packages.json')
        if not os.path.isfile(path):
            svc.abort(f'{svc.gbl.tag}: packages.json does not exist: {path}')

        with open(path, 'r', encoding='utf-8') as fp:
            cpip = json.load(fp)
            return cpip

    # --------------------
    ## check that the path to the file exists.
    # if the dir doesn't exist, create all directories needed.
    #
    # @param dst  a path with a dir + file
    # @return True
    def _check_path_dir_exists(self, dst):
        dst_dir = os.path.dirname(dst)
        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir, exist_ok=True)

    # --------------------
    ## check the given directory exists
    # if the dir doesn't exist, create all directories needed.
    #
    # @param dst_dir  a path with only dirs
    # @return True
    def _check_dir_exists(self, dst_dir):
        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir, exist_ok=True)
