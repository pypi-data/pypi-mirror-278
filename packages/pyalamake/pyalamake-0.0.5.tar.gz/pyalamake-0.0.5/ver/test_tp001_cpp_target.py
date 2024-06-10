import unittest

from medver_pytest import pth

from pyalamake.lib.svc import svc as pamsvc
from ver.helpers import svc
from ver.helpers.helper import Helper


# -------------------
class TestTp001CppTarget(unittest.TestCase):
    # --------------------
    @classmethod
    def setUpClass(cls):
        pth.init()
        svc.helper = Helper()
        svc.helper.init()

    # -------------------
    def setUp(self):
        svc.helper.init_each_test(self)

    # -------------------
    def tearDown(self):
        svc.helper.term_each_test()

    # --------------------
    @classmethod
    def tearDownClass(cls):
        svc.helper.term()
        pth.term()

    # --------------------
    # @pytest.mark.skip(reason='skip')
    def test_tp001_cpp_target(self):
        pth.proto.protocol('tp-001', 'gen for cpp targets')
        pth.proto.add_objective('check the generation of a C++ target')
        pth.proto.add_precondition('do_install has been run')

        pth.proto.step('check current version')
        pth.ver.verify_equal('0.0.3', svc.mut.version, reqids=['srs-004'])

        # clean up from previous run
        svc.helper.del_build_dir()
        svc.helper.del_makefile()

        pth.proto.step('create cpp target')
        tgt = svc.mut.create('cpp_name', 'cpp')
        pth.ver.verify_equal('cpp_name', tgt.target)
        pth.ver.verify_equal('cpp', tgt.target_type, reqids=['srs-050'])  # cpp exists
        pth.ver.verify_equal([], tgt.sources)  # initially empty
        pth.ver.verify_equal([], tgt.include_directories)  # initially empty

        # related globals
        pth.ver.verify_equal('debug', pamsvc.gbl.build_dir, reqids=['srs-001'])  # default is debug

        # --- sources
        tgt.add_sources('src1')  # add a string
        pth.ver.verify_equal(['src1'], tgt.sources, reqids=['srs-002'])  # has added source
        tgt.add_sources(['src2', 'src3'])  # add a list
        pth.ver.verify_equal(['src1', 'src2', 'src3'], tgt.sources, reqids=['srs-002'])  # has added source
        # TODO set_sources()

        # --- include dirs
        tgt.add_include_directories('inc1')  # add a string
        pth.ver.verify_equal(['inc1'], tgt.include_directories, reqids=['srs-003'])  # has added include dirs
        tgt.add_include_directories(['inc2', 'inc3'])  # add a list
        pth.ver.verify_equal(['inc1', 'inc2', 'inc3'], tgt.include_directories, reqids=['srs-003'])  # has added include dirs
        # TODO set_include_directories()

        # --- values set during gen_target()
        svc.mut.makefile(svc.helper.makefile_path)

        pth.ver.verify_equal(['cpp_name-init', 'cpp_name-build', 'cpp_name-link'], tgt.rules)
        # targets to clean
        pth.ver.verify_equal({'cpp_name-dir/*.o': 1,  # obj files
                              'cpp_name-dir/*.d': 1,  # dependecy files
                              'cpp_name': 1},  # main executable
                             tgt.clean)

        # TODO base - lines?

        # --- make help
        pth.proto.step('check make help output')
        rc, out = svc.helper.run_make('help')
        pth.ver.verify_equal(0, rc)

        for line in out.split('\n'):
            svc.log.info(line)
        pth.ver.verify_equal(10, len(svc.log.lines))
        pth.ver.verify_equal('Available targets:', svc.log.lines[0])
        pth.ver.verify_equal('  \x1b[32;01mall                                \x1b[0m build all', svc.log.lines[1])
        pth.ver.verify_equal('  \x1b[32;01mclean                              \x1b[0m clean files', svc.log.lines[2])
        pth.ver.verify_equal('  \x1b[32;01mcpp_name                           \x1b[0m build cpp_name', svc.log.lines[3])
        pth.ver.verify_equal('  \x1b[32;01mcpp_name-build                     \x1b[0m cpp_name: build source files', svc.log.lines[4])
        pth.ver.verify_equal('  \x1b[32;01mcpp_name-clean                     \x1b[0m cpp_name: clean files in this target',
                             svc.log.lines[5])
        pth.ver.verify_equal('  \x1b[32;01mcpp_name-init                      \x1b[0m cpp_name: initialize for debug build',
                             svc.log.lines[6])
        pth.ver.verify_equal('  \x1b[32;01mcpp_name-link                      \x1b[0m cpp_name: link', svc.log.lines[7])
        pth.ver.verify_equal(
            '  \x1b[32;01mcpp_name-run                       \x1b[0m cpp_name: run executable, use s="args_here" to pass in args',
            svc.log.lines[8])
        pth.ver.verify_equal('  \x1b[32;01mhelp                               \x1b[0m this help info', svc.log.lines[9])
