import os

from .svc import svc


# --------------------
class TargetBase:
    # --------------------
    def __init__(self, target_name):
        self._target = target_name

        # === source files
        self._src_files = []

        # === include directories
        self._includes = []
        self._inc_dirs = ''

        # === link libaries
        self._link_libs = []  # holds shortened library names
        self._link_files = []  # holds full path and library name
        self._libs = ''

        # === clean rules for this target
        self._clean = {}
        self._clean_cov = {}

        self._rules = []
        self._lines = []

    # --------------------
    @property
    def target(self):
        return self._target

    # === target rules

    # --------------------
    def add_rule(self, rule):
        self._rules.append(rule)

    # --------------------
    @property
    def rules(self):
        return self._rules

    # === clean rules

    # --------------------
    def add_clean(self, pattern):
        if pattern not in self._clean:
            self._clean[pattern] = 1

    # --------------------
    @property
    def clean(self):
        return self._clean

    # === source files

    # --------------------
    @property
    def sources(self):
        return self._src_files

    # --------------------
    def add_sources(self, srcs):
        if isinstance(srcs, list):
            for src in srcs:
                self._src_files.append(src)
        elif isinstance(srcs, str):
            self._src_files.append(srcs)
        else:
            svc.abort(f'add_sources: can only add strings: {srcs}')

    # === include directories

    # --------------------
    @property
    def include_directories(self):
        return self._includes

    # --------------------
    def add_include_directories(self, inc_list):
        if isinstance(inc_list, list):
            pass
        elif isinstance(inc_list, str):
            # convert to a list
            inc_list = [inc_list]
        else:
            svc.abort('add_include_directories(): accepts only str or list of str')

        for inc_dir in inc_list:
            if not isinstance(inc_dir, str):
                svc.abort(f'add_include_directories(): accepts only str or list of str, {inc_dir} is {type(inc_dir)}')
            self._includes.append(inc_dir)

        self._update_inc_dirs()

    # --------------------
    def _update_inc_dirs(self):
        self._inc_dirs = ''
        for incdir in self._includes:
            self._inc_dirs += f'"-I{incdir}" '

    # === link libraries

    # --------------------
    @property
    def link_libraries(self):
        return self._link_libs

    # --------------------
    def add_link_libraries(self, lib_list):
        if isinstance(lib_list, list):
            pass
        elif isinstance(lib_list, str):
            # convert to a list
            lib_list = [lib_list]
        else:
            svc.abort('add_link_libraries(): accepts only str or list of str')

        for lib in lib_list:
            if not isinstance(lib, str):
                svc.abort(f'add_link_libraries(): accepts only str or list of str, {lib} is {type(lib)}')
            self._link_libs.append(lib)

        self._update_link_libs()

    # --------------------
    @property
    def link_files(self):
        return self._link_files

    # --------------------
    def add_link_files(self, file_list):
        if isinstance(file_list, list):
            pass
        elif isinstance(file_list, str):
            # convert to a list
            file_list = [file_list]
        else:
            svc.abort('add_link_files(): accepts only str or list of str')

        for path in file_list:
            if not isinstance(path, str):
                svc.abort(f'add_link_files(): accepts only str or list of str, {path} is {type(path)}')
            self._link_files.append(path)

        self._update_link_libs()

    # --------------------
    def _update_link_libs(self):
        self._libs = ''
        for lib in self._link_libs:
            self._libs += f'-l{lib} '

        for file in self._link_files:
            self._libs += f'"{file}" '

    # === gen functions

    # --------------------
    def _gen_reset_coverage(self, reset_rule):
        self._writeln(f'## {self.target}: reset coverage info')
        self._writeln(f'{reset_rule}:')

        for pattern in self._clean_cov:
            self._writeln(f'\trm -f {svc.gbl.build_dir}/{pattern}')
        self._writeln('')

    # --------------------
    def gen_clean(self):
        clean_cov_rule = ''
        if self._clean_cov != {}:
            reset_rule = f'{self.target}-cov-reset'
            self._gen_reset_coverage(reset_rule)
            clean_cov_rule = f' {reset_rule}'

        self._writeln(f'## {self.target}: clean files in this target')
        self._writeln(f'{self.target}-clean:{clean_cov_rule}')

        patterns = {}
        for pattern in self.clean:
            patterns[pattern] = 1
        for pattern in patterns:
            self._writeln(f'\trm -f {svc.gbl.build_dir}/{pattern}')
        self._writeln('')

    # --------------------
    def _common_check(self):
        for file in self._src_files:
            if not os.path.isfile(file):
                svc.log.warn(f'{self.target}: source file {file} not found')

        for incdir in self._includes:
            if not os.path.isdir(incdir):
                svc.log.warn(f'{self.target}: include directory {incdir} not found')

        # _link_libs # can't do, these may be generated
        # _link_files # can't do, these may be generated

    # === for writing to Makefile

    # --------------------
    @property
    def lines(self):
        return self._lines

    # --------------------
    def _writeln(self, line):
        self._lines.append(line)
