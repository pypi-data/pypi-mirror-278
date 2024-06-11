import json
import os

from .svc import svc


# --------------------
class ArduinoShared:
    # set by user
    boardid = None
    avrdude_port = None

    # these are from /usr/share/arduino/hardware/arduino/avr/boards.txt
    f_cpu = None
    mcu = None
    avrdude = None
    avrdude_baudrate = None
    avrdude_protocol = None
    # these are derived from the above
    common_flags = None
    cpp_flags = None
    cc_flags = None

    arduino_dir = '/usr/share/arduino'
    cpp = 'avr-g++'
    cc = 'avr-gcc'
    ar = 'avr-ar'
    obj_copy = 'avr-objcopy'
    avrdude_dir = '/usr/share/arduino/hardware/tools'

    # core related
    core_tgt = None  # name of core target
    corelib = None  # path to core lib
    corelib_name = None  # name of the lib
    coredir = None  # the build dir
    core_includes = [
        f'{arduino_dir}/hardware/arduino/avr/cores/arduino',
        f'{arduino_dir}/hardware/arduino/avr/variants/standard',
    ]

    # --------------------
    def set_avrdude_port(self, val):
        self.avrdude_port = val

    # --------------------
    def print_board_list(self):
        boards = self._get_board_json()
        svc.log.line('Available boards:')
        for name, info in boards.items():
            svc.log.line(f'   {name: <20}: {info["fullname"]}')

    # --------------------
    def check(self):
        errs = 0
        errs = self._check_arg(errs, 'boardid')
        errs = self._check_arg(errs, 'avrdude_port')
        errs = self._check_arg(errs, 'f_cpu')
        errs = self._check_arg(errs, 'mcu')
        errs = self._check_arg(errs, 'avrdude')
        errs = self._check_arg(errs, 'avrdude_baudrate')
        errs = self._check_arg(errs, 'avrdude_protocol')
        errs = self._check_arg(errs, 'common_flags')
        errs = self._check_arg(errs, 'cpp_flags')
        errs = self._check_arg(errs, 'cc_flags')

        errs = self._check_arg(errs, 'core_tgt')
        errs = self._check_arg(errs, 'coredir')
        errs = self._check_arg(errs, 'corelib')
        errs = self._check_arg(errs, 'corelib_name')

        if errs > 0:
            svc.abort('arduino: resolve errors')

    # --------------------
    def _check_arg(self, errs, arg):
        selfarg = getattr(self, arg, None)
        if selfarg is None:
            errs += 1
            svc.log.err(f'arduino: {arg} is not set')
        return errs

    # --------------------
    def set_boardid(self, boardid):
        info = self._get_board_info(boardid)
        self.boardid = boardid

        # set values based on board id
        self.f_cpu = info['build.f_cpu']
        self.mcu = info['build.mcu']
        self.avrdude = info['upload.tool']
        self.avrdude_baudrate = info['upload.speed']
        self.avrdude_protocol = info['upload.protocol']

        self.common_flags = f'-c -g -Os -Wall -ffunction-sections -fdata-sections ' \
                            f'-mmcu={self.mcu} -DF_CPU={self.f_cpu}L ' \
                            '-MMD -DUSB_VID=null -DUSB_PID=null -DARDUINO=106'
        self.cpp_flags = f'{self.common_flags} -fno-exceptions -std=c++11'
        self.cc_flags = self.common_flags

    # --------------------
    def _get_board_info(self, boardid):
        boards = self._get_board_json()
        if boardid not in boards:
            svc.abort(f'ardunio: invalid boardid: {boardid}')

        info = boards[boardid]
        return info

    # --------------------
    def _get_board_json(self):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'boards.json')
        with open(path, 'r', encoding='utf-8') as fp:
            boards = json.load(fp)
            return boards
