from .svc import svc


# --------------------
## holds all functions for getting or composing values
# Note: all functions in this class should have a return value
class UtilsVal:
    # --------------------
    ## return the module name for this given arg
    #  if var is invalid, AttributeError is thrown
    #
    # @param var   the variable to retrieve
    # @return the module name or an error message
    def get_cfg(self, var):
        return getattr(svc.cfg, var)

    # --------------------
    ## return the Coverage options needed for the module/app.
    #
    # @return coverage options needed for pytest
    def get_cov_opts(self):
        opts = ''
        # the directory to cover
        if svc.cfg.is_module:
            opts += f'--cov={svc.cfg.mod_dir_name}/lib '
        else:  # an app
            opts += '--cov=lib '

        opts += '--cov-report= '  # the type of report; default is HTML
        opts += '--cov-branch '  # branch coverage
        opts += '--cov-config=setup.cfg '  # other cfg is in setup.cfg
        opts += '--cov-append'  # append to coverage content; up to caller to clear it
        return opts
