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
        self._help = {}
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
        rule = 'all'
        rules_str = ''
        for tgt, rules in self._rules.items():
            rules_str += f' {tgt} '
            rules_str += ' '.join(rules)
        self._writeln(f'.PHONY : all clean help {rules_str}')

        # has to be first target found otherwise clion can't parse it
        self._gen_rule(rule, rules_str, f'build {rule}')

        # generate a single rule to build each target in total
        for rule, rules_deps in self._rules.items():
            rules_str = ' '.join(rules_deps)
            self._gen_rule(rule, rules_str, f'build {rule}')

        self._writeln('')

    # --------------------
    def _gen_targets(self):
        for tgt in self._targets:
            self._writeln(f'# ==== {tgt.target}')
            for line in tgt.lines:
                self._writeln(line)

    # --------------------
    def _gen_help(self):
        bslash = '\\'
        self._add_help('help', 'this help info')

        # gather all the help
        all_help = {}
        all_help.update(self._help)
        for tgt in self._targets:
            all_help.update(tgt.help)

        self._writeln('help:')
        self._writeln(f'\t@printf "Available targets:{bslash}n"')
        lastrule = 'help'
        for rule, desc in sorted(all_help.items()):
            if rule.startswith(f'{lastrule}-'):
                rulepfx = '  '
            else:
                lastrule = rule
                rulepfx = ''
            desc2 = desc.replace('"', f'{bslash}"')
            self._writeln(f'\t@printf "  {rulepfx}\x1b[32;01m{rule: <35}\x1b[0m {desc2}{bslash}n"')
        self._writeln(f'\t@printf "{bslash}n"')

    # --------------------
    def _gen_clean(self):
        # TODO add quiet to add "@" on commands
        rule = 'clean'
        clean_tgts = ''
        for tgt in self._targets:
            clean_tgts += f'{tgt.target}-clean '

        self._gen_rule(rule, clean_tgts, f'clean files')
        self._writeln('')

    # --------------------
    def _writeln(self, line):
        self._fp.write(line + '\n')

    # --------------------
    def _add_help(self, target, desc):
        if target in self._help:
            svc.log.warn(f'add_help: target "{target}" already has description')
            svc.log.warn(f'   prev: {self._help[target]}')
            svc.log.warn(f'   curr: {desc}')
            svc.log.warn(f'   replacing...')
        self._help[target] = desc

    # --------------------
    def _gen_rule(self, rule, deps, desc):
        self._writeln(f'#-- {desc}')
        self._add_help(rule, desc)
        if deps:
            self._writeln(f'{rule}: {deps}')
        else:
            self._writeln(f'{rule}:')
