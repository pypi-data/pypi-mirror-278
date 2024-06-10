import os

from .svc import svc
from .target_base import TargetBase


# --------------------
class TargetCpp(TargetBase):
    # --------------------
    @classmethod
    def create(cls, targets, target_name):
        impl = TargetCpp(target_name)
        targets.append(impl)
        return impl

    # --------------------
    def __init__(self, target_name):
        super().__init__(target_name)

        self._objs = ''
        self._cxx = 'c++'
        self._cpp_flags = '-std=c++20'

        self._build_dirs = {}

        self._ld_flags = ''

    # --------------------
    @property
    def target_type(self):
        return 'cpp'

    # --------------------
    def check(self):
        svc.log.highlight(f'{self.target}: check target...')
        self._common_check()

    # --------------------
    def gen_target(self):
        svc.log.highlight(f'{self.target}: gen target, type:{self.target_type}')

        self._gen_args()
        self._gen_init()
        self._gen_app()
        self._gen_link()
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
        self._writeln(f'\t{self._cxx} {self._objs} {self._ld_flags} -o {exe}')
        self._writeln('')
        self.add_clean(self.target)

        self._writeln(f'## {self.target}: link')
        self._writeln(f'{rule}: {exe} {self.target}-build')
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
