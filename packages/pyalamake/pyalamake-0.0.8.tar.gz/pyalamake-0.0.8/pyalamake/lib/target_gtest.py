import os

from .svc import svc
from .target_base import TargetBase


# --------------------
class TargetGtest(TargetBase):
    # --------------------
    @classmethod
    def create(cls, targets, target_name):
        impl = TargetGtest(target_name)
        targets.append(impl)
        return impl

    # --------------------
    def __init__(self, target_name):
        super().__init__(target_name)

        self._objs = ''
        self._cxx = 'g++'
        self._cpp_flags = '-g -fdiagnostics-color=always -fprofile-arcs -ftest-coverage -DGTEST_HAS_PTHREAD=1 -std=gnu++20'

        self._build_dirs = {}

        self._includes = []
        self._update_inc_dirs()

        self._link_libs = ['gtest', 'pthread', 'gcov']
        self._update_link_libs()

        self._ld_flags = ''

        self._cov_dirs = []

    # --------------------
    @property
    def target_type(self):
        return 'gtest'

    # --------------------
    def add_coverage(self, cov_list):
        if isinstance(cov_list, list):
            pass
        elif isinstance(cov_list, str):
            # convert to a list
            cov_list = [cov_list]
        else:
            svc.abort('add_coverage(): accepts only str or list of str')

        for cov_dir in cov_list:
            if not isinstance(cov_dir, str):
                svc.abort(f'add_coverage(): accepts only str or list of str, {cov_dir} is {type(cov_dir)}')
            self._cov_dirs.append(cov_dir)

    # --------------------
    def check(self):
        svc.log.highlight(f'{self.target}: check target...')
        self._common_check()

        for covdir in self._cov_dirs:
            if not os.path.isdir(covdir):
                svc.log.warn(f'{self.target}: coverage directory {covdir} not found')

    # --------------------
    def gen_target(self):
        svc.log.highlight(f'{self.target}: gen target, type:{self.target_type}')

        self._gen_args()
        self._gen_init()
        self._gen_app()
        self._gen_link()
        self._gen_coverage()
        self._gen_run()

    # --------------------
    def _gen_args(self):
        # create output build directory
        self._build_dirs[svc.gbl.build_dir] = 1

        for file in self.sources:
            obj, dst_dir = self._get_obj_path(file)
            self._build_dirs[dst_dir] = 1

        self._writeln('')

    # --------------------
    def _gen_init(self):
        rule = f'{self.target}-init'
        self.add_rule(rule)

        self._writeln(f'## {self.target}: initialize for {svc.gbl.build_dir} build')
        self._writeln(f'{rule}:')
        for blddir in self._build_dirs:
            self._writeln(f'\tmkdir -p {blddir}')
        self._writeln('')

    # --------------------
    def _get_obj_path(self, file):
        obj = f'{svc.gbl.build_dir}/{self.target}-dir/{file}.o'
        dst_dir = os.path.dirname(obj)
        return obj, dst_dir

    # --------------------
    def _add_clean_cov(self, pattern):
        if pattern not in self._clean_cov:
            self._clean_cov[pattern] = 1

    # --------------------
    def _gen_app(self):
        rule = f'{self.target}-build'
        self.add_rule(rule)

        build_deps = ''
        for file in self.sources:
            obj, dst_dir = self._get_obj_path(file)

            # gen clean paths
            clean_path = dst_dir.replace(f'{svc.gbl.build_dir}/', '')
            self.add_clean(f'{clean_path}/*.o')
            self.add_clean(f'{clean_path}/*.d')
            # coverage related cleans
            self.add_clean(f'{clean_path}/*.gcno')
            self._add_clean_cov(f'{clean_path}/*.gcda')

            self._writeln(f'{obj}: {file}')
            self._writeln(f'\t{self._cxx} -c {self._cpp_flags} {self._inc_dirs} {file} -o {obj}')
            self._objs += f'{obj} '
            build_deps += f'{file} '

        self._writeln('')
        self._writeln(f'## {self.target}: build source files')
        self._writeln(f'{rule}: {self._objs}')
        self._writeln('')

    # --------------------
    def _gen_link(self):
        rule = f'{self.target}-link'
        self.add_rule(rule)

        exe = f'{svc.gbl.build_dir}/{self.target}'
        self._writeln(f'{exe}: {self._objs}')
        self._writeln(f'\t{self._cxx} {self._objs} {self._ld_flags} {self._libs} -o {exe}')
        self._writeln('')
        self.add_clean(self.target)

        self._writeln(f'## {self.target}: link')
        self._writeln(f'{rule}: {exe} {self.target}-build')
        self._writeln('')

    # --------------------
    def _gen_coverage(self):
        rule = f'{self.target}-cov'
        # don't add to rules

        utdir = f'{svc.gbl.build_dir}/{self.target}-dir'
        report_page = f'{svc.gbl.build_dir}/{self.target}.html'
        cmd = ('gcovr --html-details '  # show individual source files
               f'-r {utdir} '  # default to debug for unit test coverage
               '--no-color '  # no color for text output
               '--sort=uncovered-percent '  # sort source files based on percentage uncovered lines
               '--print-summary '  # print summary to stdout
               f'-o {report_page} ')  # location of report main page

        if not self._cov_dirs:
            svc.log.warn(f'gen_covrage: cov_dirs is empty, use add_coverage()')

        for cov_dir in self._cov_dirs:
            cmd += f'--filter {cov_dir} '

        self.add_clean(f'{self.target}.html')
        self.add_clean(f'{self.target}.css')
        self.add_clean(f'{self.target}.**.html')

        self._writeln(f'## {self.target}: show coverage')
        self._writeln(f'{rule}: ')
        self._writeln(f'\t{cmd}')
        self._writeln(f'\t@echo "see {report_page}" for HTML report')
        self._writeln('')

    # --------------------
    def _gen_run(self):
        rule = f'{self.target}-run'
        # don't add rule

        exe = f'{svc.gbl.build_dir}/{self.target}'

        self._writeln(f'## {self.target}: run executable, use s="args_here" to pass in args')
        self._writeln(f'{rule}: {self.target}-link')
        self._writeln(f'\t{exe} $(if $s, $s, )')
        self._writeln('')
