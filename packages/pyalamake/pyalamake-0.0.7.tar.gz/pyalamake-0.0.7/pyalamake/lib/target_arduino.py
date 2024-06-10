import os

from .svc import svc
from .target_base import TargetBase


# --------------------
class TargetArduino(TargetBase):
    # --------------------
    @classmethod
    def create(cls, targets, target_name, shared=None):
        impl = TargetArduino(target_name, shared)
        targets.append(impl)
        return impl

    # --------------------
    def __init__(self, target_name, shared):
        super().__init__(target_name)

        if shared is None:
            svc.abort('Arduino Targets must have a shared Arduino component passed in')

        self._shared = shared

        self._build_dirs = {}

        # these need to be set below
        self.tgt_build_dir = None
        self._elffile = None
        self._eepfile = None
        self._hexfile = None
        self._app_deps = None

    # --------------------
    @property
    def target_type(self):
        return 'arduino'

    # --------------------
    def _update_inc_dirs(self):
        super()._update_inc_dirs()
        for incdir in self._shared.core_includes:
            self._inc_dirs += f' "-I{incdir}" '

    # --------------------
    def check(self):
        svc.log.highlight(f'{self.target}: check target...')
        self._common_check()

        errs = 0
        self._shared.check()
        if errs > 0:
            svc.abort(f'{self.target} target_arduino: resolve errors')

    # --------------------
    def gen_target(self):
        self.tgt_build_dir = f'{svc.gbl.build_dir}/{self.target}-dir'

        svc.log.highlight(f'{self.target}: gen target, type:{self.target_type}')
        svc.log.line(f'   boardid  : {self._shared.boardid}')
        svc.log.line(f'   port     : {self._shared.avrdude_port}')
        svc.log.line(f'   baud_rate: {self._shared.avrdude_baudrate}')
        svc.log.line(f'   mcu      : {self._shared.mcu}')
        svc.log.line(f'   tgt dir  : {self.tgt_build_dir}')
        svc.log.line(f'   corelib  : {self._shared.corelib}')
        svc.log.line(f'   coredir  : {self._shared.coredir}')

        self._elffile = f'{svc.gbl.build_dir}/{self.target}.elf'
        self.add_clean(f'{self.target}.elf')

        self._eepfile = f'{svc.gbl.build_dir}/{self.target}.eep'
        self.add_clean(f'{self.target}.eep')

        self._hexfile = f'{svc.gbl.build_dir}/{self.target}.hex'
        self.add_clean(f'{self.target}.hex')

        self._gen_args()
        self._gen_init()
        self._gen_app()
        self._gen_link()
        self._gen_upload()

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
        obj = f'{self.tgt_build_dir}/{file}.o'
        dst_dir = os.path.dirname(obj)
        return obj, dst_dir

    # --------------------
    def _gen_app(self):
        rule = f'{self.target}-build'
        self.add_rule(rule)

        self._app_deps = ''
        build_deps = ''
        for file in self.sources:
            obj, dst_dir = self._get_obj_path(file)

            # gen clean paths
            clean_path = dst_dir.replace(f'{svc.gbl.build_dir}/', '')
            self.add_clean(f'{clean_path}/*.o')
            self.add_clean(f'{clean_path}/*.d')

            self._writeln(f'{obj}: {file}')
            self._writeln(f'\t{self._shared.cpp} {self._shared.cpp_flags} {self._inc_dirs} {file} -o {obj}')
            self._app_deps += f'{obj} '
            build_deps += f'{file} '

        self._writeln('')
        self._writeln(f'## {self.target}: build sketch')
        self._writeln(f'{rule}: {build_deps}')
        self._writeln('')

    # --------------------
    def _gen_link(self):
        rule = f'{self.target}-link'
        self.add_rule(rule)

        self._writeln(f'## {self.target}: link sketch and core')
        self._writeln(f'{rule}: {self._shared.core_tgt} {self._hexfile}')
        self._writeln('')

        # creates the ELF
        self._writeln(f'{self._elffile}: {self._app_deps} {self._shared.corelib}')
        self._writeln(f'\t{self._shared.cc} -Os -Wl,--gc-sections -mmcu={self._shared.mcu} '
                      f'-o {self._elffile} {self._app_deps} {self._shared.corelib} -lm')
        self._writeln('')

        # creates the EEP
        self._writeln(f'{self._eepfile}: {self._elffile}')
        self._writeln(f'\t{self._shared.obj_copy} -O ihex -j .eeprom --set-section-flags=.eeprom=alloc,load '
                      f'--no-change-warnings --change-section-lma .eeprom=0 {self._elffile} {self._eepfile}')
        self._writeln('')

        # creates the HEX
        self._writeln(f'{self._hexfile}: {self._elffile} {self._eepfile}')
        self._writeln(f'\t{self._shared.obj_copy} -O ihex -R .eeprom {self._elffile} {self._hexfile}')
        self._writeln('')

    # --------------------
    def _gen_upload(self):
        rule = f'{self.target}-upload'
        # don't add rule

        avrdude_conf = f'{self._shared.avrdude_dir}/avrdude.conf'
        avrdude_protocol = self._shared.avrdude_protocol
        avrdude_args = f'-C{avrdude_conf} -p{self._shared.mcu} -c{avrdude_protocol} ' \
                       f'-P{self._shared.avrdude_port} -b{self._shared.avrdude_baudrate}'

        self._writeln(f'## {self.target}: upload to arduino')
        self._writeln(f'{rule}: {self.target}-link')
        self._writeln(f'\t{self._shared.avrdude} -v {avrdude_args} -D -Uflash:w:{self._hexfile}:i -Ueeprom:w:{self._eepfile}:i')
        self._writeln('')
