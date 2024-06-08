import json
import os

from .arduino_shared import ArduinoShared
from .gbl import Gbl
from .logger import Logger
from .svc import svc


# --------------------
class AlaMake:
    # --------------------
    def __init__(self):
        svc.log = Logger  # not an instance, it is the class
        svc.gbl = Gbl()

        self._targets = []

        self._fp = None
        self._tgt = None
        self._rules = {}
        svc.log.highlight('creating targets...')

    # --------------------
    @property
    def version(self):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'version.json')
        with open(path, 'r', encoding='utf-8') as fp:
            vers = json.load(fp)
        return vers['version']

    # --------------------
    @property
    def gbl(self):
        return svc.gbl

    # --------------------
    @property
    def ut_svc(self):
        return svc

    # --------------------
    def create_arduino_shared(self):
        return ArduinoShared()

    # --------------------
    def create(self, target_name, target_type, shared=None):
        valid_types = [
            # do not put arduino_core here
            'arduino',
            'cpp',
            'gtest',
        ]

        for tgt in self._targets:
            if target_name == tgt.target:
                svc.abort(f'target name is already in use: {target_name}')
                return None  # pragma: no cover

        if target_type == 'cpp':
            from .target_cpp import TargetCpp
            svc.log.line(f'create: {target_name}')
            impl = TargetCpp.create(self._targets, target_name)
        elif target_type == 'gtest':
            from .target_gtest import TargetGtest
            svc.log.line(f'create: {target_name}')
            impl = TargetGtest.create(self._targets, target_name)
        elif target_type == 'arduino':
            svc.log.line(f'create: {target_name}')
            from .target_arduino import TargetArduino
            impl = TargetArduino.create(self._targets, target_name, shared=shared)
        elif target_type == 'arduino-core':
            svc.log.line(f'create: {target_name}')
            from .target_arduino_core import TargetArduinoCore
            impl = TargetArduinoCore.create(self._targets, target_name, shared=shared)
        else:
            svc.log.err(f'unknown target type: {target_type}')
            svc.abort(f'valid target types: {" ".join(valid_types)} ')
            return None  # pragma: no cover

        return impl

    # --------------------
    def makefile(self, path='Makefile'):
        with open(path, 'w', encoding='utf-8') as self._fp:
            svc.log.highlight('generating targets...')
            self._gather_targets()
            svc.log.highlight('generating makefile...')
            self._gen_rules()
            self._gen_targets()
            self._gen_clean()
            self._gen_help()
        svc.log.line('done')

    # --------------------
    def _gather_targets(self):
        self._rules = {}
        for tgt in self._targets:
            # uncomment to debug
            # svc.log.dbg(f'   source   : {tgt.sources}')

            tgt.check()
            tgt.gen_target()
            tgt.gen_clean()
            self._rules[tgt.target] = tgt.rules

    # --------------------
    def _gen_rules(self):
        # gen rule for all
        rules_str = ''
        for tgt, rules in self._rules.items():
            rules_str += f' {tgt} '
            rules_str += ' '.join(rules)
        self._writeln(f'.PHONY : all clean help {rules_str}')

        # has to be first target found otherwise clion can't parse it
        self._writeln('## build all')
        self._writeln(f'all: {rules_str}')

        # generate a single rule to build each target in total
        for tgt, rules in self._rules.items():
            self._writeln(f'## build {tgt}')
            rules_str = ' '.join(rules)
            self._writeln(f'{tgt}: {rules_str}')

        self._writeln('')

    # --------------------
    def _gen_targets(self):
        for tgt in self._targets:
            self._writeln(f'# ==== {tgt.target}')
            for line in tgt.lines:
                self._writeln(line)

    # --------------------
    def _gen_help(self):
        # TODO gather this during gen
        bslash = '\\'
        fslash = '/'
        openb = '{'
        closeb = '}'
        self._writeln('## this help info')
        self._writeln('help:')
        self._writeln(f'\t@printf "Available targets:{bslash}n"')
        self._writeln(f'\t@awk \'{fslash}^[a-zA-Z{bslash}-{bslash}0-9%:{bslash}{bslash}]+/ {openb} {bslash}')
        self._writeln(f'          helpMessage = match(lastLine, {fslash}^## (.*){fslash}); {bslash}')
        self._writeln(f'          if (helpMessage) {openb} {bslash}')
        self._writeln(f'            helpCommand = $$1; {bslash}')
        self._writeln(f'            helpMessage = substr(lastLine, RSTART + 3, RLENGTH); {bslash}')
        self._writeln(f'            gsub("{bslash}{bslash}{bslash}{bslash}", "", helpCommand); {bslash}')
        self._writeln(f'            gsub(":+$$", "", helpCommand); {bslash}')
        self._writeln(f'            printf "  {bslash}x1b[32;01m%-35s{bslash}x1b[0m %s{bslash}n", helpCommand, helpMessage; {bslash}')
        self._writeln(f'          {closeb} {bslash}')
        self._writeln(f'       {closeb} {bslash}')
        self._writeln(f'       {openb} lastLine = $$0 {closeb}\' $(MAKEFILE_LIST) | sort -u')
        self._writeln(f'\t@printf "{bslash}n"')

    # --------------------
    def _gen_clean(self):
        # TODO add quiet to add "@" on commands
        self._writeln('## clean files')
        clean_tgts = ''
        for tgt in self._targets:
            clean_tgts += f'{tgt.target}-clean '
        self._writeln(f'clean: {clean_tgts}')

        self._writeln('')

    # --------------------
    def _writeln(self, line):
        self._fp.write(line + '\n')
