import unittest

import pytest
from medver_pytest import pth

from ver.helpers import svc
from ver.helpers.helper import Helper


# -------------------
class TestTp004GtestTarget(unittest.TestCase):
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
    def test_tp004_gtest_target(self):
        pth.proto.protocol('tp-004', 'gen for gtest targets')
        pth.proto.add_objective('check the generation of a C++ gtest target')
        pth.proto.add_precondition('do_install has been run')

        # clean up from previous run
        svc.helper.del_build_dir()
        svc.helper.del_makefile()

        pth.proto.step('create gtest target')
        tgt = svc.mut.create('gtest_name', 'gtest')
        pth.ver.verify_equal('gtest_name', tgt.target)
        pth.ver.verify_equal('gtest', tgt.target_type, reqids=['srs-130'])  # gtest exists
        pth.ver.verify_equal([], tgt.sources)  # initially empty
        pth.ver.verify_equal([], tgt.include_directories)  # initially empty

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

        # --- coverage dirs
        tgt.add_coverage('src1')  # add a single directory
        pth.ver.verify_equal(['src1'], tgt._cov_dirs)
        tgt.add_coverage(['src2', 'src3'])  # add a list of directories
        pth.ver.verify_equal(['src1', 'src2', 'src3'], tgt._cov_dirs, reqids=['srs-131'])  # has added coverage dirs

        # --- values set during gen_target()
        svc.mut.makefile(svc.helper.makefile_path)

        pth.ver.verify_equal(['gtest_name-init', 'gtest_name-build', 'gtest_name-link'], tgt.rules)
        # targets to clean
        pth.ver.verify_equal({'gtest_name-dir/*.o': 1,  # obj files
                              'gtest_name-dir/*.d': 1,  # dependency files
                              'gtest_name-dir/*.gcno': 1,  # coverage
                              'gtest_name-dir/*.gcda': 1,  # coverage
                              'gtest_name': 1,  # main executable
                              'gtest_name.html': 1,  # coverage report
                              'gtest_name.css': 1,  # coverage report
                              'gtest_name.**.html': 1,  # coverage report
                              },
                             tgt.clean)

        # --- invalide coverage dirs
        with pytest.raises(SystemExit) as excp:
            tgt.add_coverage(1)  # invalid
        pth.ver.verify_equal(SystemExit, excp.type, reqids=['srs-131'])  # sys.exit abort

        tgt = svc.mut.create('gtest2', 'gtest')  # use a unique target name
        with pytest.raises(SystemExit) as excp:
            tgt.add_coverage([1, 'src4'])  # invalid
        pth.ver.verify_equal(SystemExit, excp.type, reqids=['srs-131'])  # sys.exit abort
