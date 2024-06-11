import glob

from pyalamake.lib.svc import svc
from pyalamake.lib.target_base import TargetBase


# --------------------
class TargetArduinoCore(TargetBase):
    # --------------------
    @classmethod
    def create(cls, targets, target_name, shared=None):
        impl = TargetArduinoCore(target_name, shared)
        targets.append(impl)
        return impl

    # --------------------
    def __init__(self, target_name, shared):
        super().__init__(target_name)

        self._shared = shared
        self._shared.core_tgt = target_name
        self._shared.coredir = f'{svc.gbl.build_dir}/{self._shared.core_tgt}-dir'
        self._shared.corelib_name = f'{self._shared.core_tgt}.a'
        self._shared.corelib = f'{svc.gbl.build_dir}/{self._shared.corelib_name}'

        self._build_dirs = {}

        self._libdir = None
        self._objs = []
        self._inc_dirs = []

    # --------------------
    @property
    def target_type(self):
        return 'arduino_core'

    # --------------------
    def check(self):
        svc.log.highlight(f'{self.target}: check target...')
        self._common_check()

        errs = 0
        self._shared.check()
        if errs > 0:
            svc.abort(f'{self.target} target_arduino_core: resolve errors')

    # --------------------
    def gen_target(self):
        svc.log.highlight(f'gen target {self.target}, type:{self.target_type}')

        self._gen_args()
        self._gen_init()

        self.add_clean(self._shared.corelib_name)

        self._libdir = f'{self._shared.arduino_dir}/hardware/arduino/avr/cores/arduino'

        self._inc_dirs = ''
        for incdir in self._shared.core_includes:
            self._inc_dirs += f' "-I{incdir}" '

        self._gen_core_compile()
        self._gen_core_link()
        self._writeln('')

    # --------------------
    def _gen_args(self):
        # create output build directory
        self._build_dirs[svc.gbl.build_dir] = 1
        self._build_dirs[self._shared.coredir] = 1

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
    def _gen_core_compile(self):
        rule = f'{self.target}-build'
        self.add_rule(rule)

        cpp_files = self._gen_core_cpp_compile()
        c_files = self._gen_core_c_compile()

        # add clean rules; the clean function automatically adds the build_dir
        self.add_clean(f'{self._shared.core_tgt}-dir/*.o')
        self.add_clean(f'{self._shared.core_tgt}-dir/*.d')

        src_deps = ''
        for (src, _) in cpp_files + c_files:
            src_deps += f' {src}'

        self._writeln(f'## {self.target}: compile arduino core source files')
        self._writeln(f'{rule}: {src_deps}')
        self._writeln('')

    # --------------------
    def _gen_core_cpp_compile(self):
        src_files = []
        for src in glob.glob(f'{self._libdir}/*.cpp', recursive=True):
            obj = src.replace(self._libdir, self._shared.coredir) + '.o'
            src_files.append((src, obj))

        for src, obj in src_files:
            # TODO how to do these without conflict across targets?
            self._writeln(f'{obj}: {src}')
            self._writeln(f'\t{self._shared.cpp} {self._shared.cpp_flags} {self._inc_dirs} {src} -o {obj}')
            self._objs.append(obj)

        self._writeln('')

        return src_files

    # --------------------
    def _gen_core_c_compile(self):
        src_files = []
        for src in glob.glob(f'{self._libdir}/*.c', recursive=True):
            obj = src.replace(self._libdir, self._shared.coredir) + '.o'
            src_files.append((src, obj))

        for src, obj in src_files:
            # TODO how to do these without conflict across targets
            self._writeln(f'{obj}: {src}')
            self._writeln(f'\t{self._shared.cc} {self._shared.cc_flags} {self._inc_dirs} {src} -o {obj}')
            self._objs.append(obj)

        self._writeln('')

        return src_files

    # --------------------
    def _gen_core_link(self):
        rule = f'{self.target}-link'
        self.add_rule(rule)

        self._writeln(f'## {self.target}: create arduino core library')
        self._writeln(f'{rule}: {self._shared.corelib}')
        self._writeln('')

        obj_deps = ' '.join(self._objs)
        self._writeln(f'{self._shared.corelib}: {obj_deps}')
        self._writeln(f'\trm -f {self._shared.corelib}')
        for obj in self._objs:
            self._writeln(f'\t{self._shared.ar} rcs {self._shared.corelib} {obj}')
