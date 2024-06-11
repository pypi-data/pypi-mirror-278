import glob
import os

from .svc import svc


# --------------------
## perform the do_clean operation
class DoClean:
    # --------------------
    ## do_clean mainline.
    #
    # @param verbose  amount of logging: min
    # @param depth    how much to clean: lite, full, '' defaults to lite
    # @return None
    def run(self, verbose='min', depth=''):
        if depth == '':
            depth = 'lite'

        svc.log.highlight(f'{svc.gbl.tag}: starting verbose:{verbose} '
                          f'tech:{svc.cfg.mod_tech} module:{svc.cfg.is_module}...')

        svc.utils_fs.safe_delete_tree(svc.gbl.outdir, verbose=verbose)
        svc.utils_fs.safe_delete_file('Doxyfile', verbose=verbose)
        svc.utils_fs.safe_delete_file('.coverage', verbose=verbose)
        svc.utils_fs.safe_delete_tree('dist', verbose=verbose)
        svc.utils_fs.safe_delete_tree('.pytest_cache', verbose=verbose)

        if svc.cfg.is_module:
            svc.utils_fs.safe_delete_tree(os.path.join(f'{svc.cfg.mod_dir_name}.egg-info'), verbose=verbose)
            svc.utils_fs.safe_delete_file(os.path.join('setup.py'), verbose=verbose)
            svc.utils_fs.safe_delete_file(os.path.join('MANIFEST.in'), verbose=verbose)
            svc.utils_fs.safe_delete_file(os.path.join(svc.cfg.mod_dir_name, 'lib', 'build_info.py'), verbose=verbose)
            svc.utils_fs.safe_delete_file(os.path.join(svc.cfg.mod_dir_name, 'lib', 'version.json'), verbose=verbose)
        else:  # an app
            svc.utils_fs.safe_delete_file(os.path.join('lib', 'build_info.py'), verbose=verbose)
            svc.utils_fs.safe_delete_file(os.path.join('lib', 'version.json'), verbose=verbose)

        if svc.cfg.mod_tech in ['cpp', 'arduino']:
            svc.utils_fs.safe_delete_tree('cmake-build-debug', verbose=verbose)
            svc.utils_fs.safe_delete_tree('cmake-build-release', verbose=verbose)

        if depth == 'full':
            svc.utils_fs.safe_delete_tree('venv', verbose=verbose)

            # must be after venv
            self._delete_cache(verbose)

        # note: no return code

    # --------------------
    ## recursively deletes __pycache__ subdirectories in the root_dir.
    #
    # @param verbose  logging verbosity: 'full' or ''
    # @return None
    def _delete_cache(self, verbose):
        folders = glob.glob('**/__pycache__', recursive=True)
        # uncomment to debug
        # svc.log.dbg(f'{folders}')

        if not folders:
            if verbose in ['full']:
                svc.log.ok(f'{"rm: dirs do not exist": <25}: __pycache__')
            return

        # at least one cache folder exists
        for folder in folders:
            # uncomment to debug
            # svc.log.dbg(f'rmtree {folder}')
            svc.utils_fs.safe_delete_tree(folder, verbose=verbose)
