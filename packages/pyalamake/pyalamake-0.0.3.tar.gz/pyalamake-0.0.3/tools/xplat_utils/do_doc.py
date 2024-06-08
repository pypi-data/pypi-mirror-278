import os
import re
import shutil

from .svc import svc


# --------------------
## perform the do_doc operation
class DoDoc:
    # --------------------
    ## do_doc mainline.
    #
    # @param make_pdf  gen the pdf (True) or not (False)
    # @return None
    def run(self, make_pdf=True):
        svc.log.start(f'{svc.gbl.tag}: starting (make_pdf={make_pdf})...')

        # ensure outdir is created
        svc.utils_fs.create_outdir()
        # ensure out/doc is created
        svc.utils_fs.clean_out_dir('doc')

        self._gen_doxyfile()
        self._gen_html()
        self._sort_warnings()
        if make_pdf:
            self._gen_pdf()

    # --------------------
    ## generate the Doxyfile cfg from tools/doxyfile_template
    #
    # @return None
    def _gen_doxyfile(self):
        svc.utils_fs.safe_delete_file('Doxyfile')

        # generate the setup.py file from setup_template.py
        src = os.path.join(svc.utils_fs.root_dir, 'tools', 'doxyfile_template')
        dst = os.path.join(svc.utils_fs.root_dir, 'Doxyfile')
        with open(dst, 'w', encoding='utf-8', newline='\n') as fp_dst:
            with open(src, 'r', encoding='utf-8') as fp_src:
                for line in fp_src:
                    while True:
                        m = re.search(r'\$\$([^$]+)\$\$', line)
                        if not m:
                            # uncomment to debug
                            # log.dbg(f'line: {line.strip()}')
                            fp_dst.write(line)
                            break

                        vrbl = m.group(1)
                        if vrbl == 'root_dir':
                            val = str(svc.utils_fs.root_dir)
                        elif vrbl == 'outdir':
                            val = str(svc.gbl.outdir)
                        elif vrbl in ['doxy_type', 'doxy_desc', 'doxy_exclude', 'doxy_include']:
                            val = getattr(svc.cfg.do_doc, vrbl)
                        else:
                            val = getattr(svc.cfg, vrbl)
                        # uncomment to debug
                        # log.dbg(f'grp:{m.group(1)} line:{line.strip()}')
                        line = line.replace(f'$${vrbl}$$', val)

                for dirname in svc.cfg.do_doc.doxy_exclude:
                    line = f'EXCLUDE += {dirname}\n'
                    fp_dst.write(line)

                for dirname in svc.cfg.do_doc.doxy_include:
                    line = f'INPUT += {dirname}\n'
                    fp_dst.write(line)

        svc.gbl.overallrc += svc.gbl.rc

    # --------------------
    ## generate the doxygen HTML and latex content
    #
    # @return None
    def _gen_html(self):
        svc.log.start(f'{svc.gbl.tag}: running doxygen')
        svc.utils_ps.run_process('doxygen', use_raw_log=False)
        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: doxygen rc={svc.gbl.rc}')

        svc.gbl.overallrc += svc.gbl.rc

    # --------------------
    ## generate the doxygen PDF file from latex content
    #
    # @return None
    def _gen_pdf(self):
        svc.log.start(f'{svc.gbl.tag}: generate PDF')
        path = os.path.join(svc.gbl.outdir, 'doc', 'latex')
        log_file = os.path.join(svc.gbl.outdir, 'doxygen_latex.txt')
        svc.utils_ps.run_process('make', use_raw_log=False, working_dir=path, log_file=log_file)
        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: generate PDF rc={svc.gbl.rc}')
        if svc.gbl.rc != 0:
            svc.log.err(f'check the contents of {log_file}')
            svc.gbl.overallrc += svc.gbl.rc
            return

        pdf_path = os.path.join(svc.gbl.outdir, 'doc', 'latex', 'refman.pdf')
        pdf_path = pdf_path.replace('\\', '/')
        if os.path.isfile(pdf_path):
            svc.log.ok(f'{svc.gbl.tag}: see full output in: {log_file}')
        else:
            svc.log.err(f'{svc.gbl.tag}: PDF does not exist: {pdf_path}')
            svc.log.err(f'{svc.gbl.tag}: see full output in: {log_file}')

        dst = os.path.join(svc.gbl.outdir, f'{svc.cfg.mod_name}.pdf')
        shutil.copyfile(pdf_path, dst)

        svc.gbl.overallrc += svc.gbl.rc

    # --------------------
    ## sort the doxygen warnings in order of path to the file,
    # and the line number within in the file
    #
    # @return None
    def _sort_warnings(self):
        path = os.path.join(svc.gbl.outdir, 'doxygen.txt')
        warnings = 0
        lines = []
        with open(path, 'r', encoding='UTF-8') as fp:
            for line in fp:
                srch = f'{os.getcwd()}/(.*\n)'
                srch = srch.replace('\\', '/')
                m = re.search(srch, line)
                if m:
                    lines.append(m.group(1))
                else:
                    lines.append(line)

        lines = sorted(lines, key=self._get_warning_fields)

        with open(path, 'w', encoding='UTF-8', newline='\n') as fp:
            fp.writelines(lines)

        for line in lines:
            if line != '':
                warnings += 1
                svc.log.raw(line.strip())
        if warnings != 0:
            svc.gbl.rc += warnings

        svc.log.check(svc.gbl.rc == 0, f'{svc.gbl.tag}: found {warnings} warnings')
        svc.gbl.overallrc += svc.gbl.rc

    # --------------------
    ## get fields from a doxygen warning line.
    # used to sort them
    #
    # @param line  the current line
    # @return tuple with file path and line number within the file
    def _get_warning_fields(self, line):
        m = re.search(r'([^:]+):(\d+):', line)
        if m:
            return m.group(1), int(m.group(2))

        return line, ''
