import sys


# -------------------
## Holds all info for logging debug lines
class UtilsLogger:
    ## flag to log to stdout or not
    verbose = True
    ## for UT only
    ut_mode = False
    ## for UT only
    ut_lines = []

    # --------------------
    ## log a message. Use ok() or err() as appropriate.
    #
    # @param ok      the check state
    # @param msg     the message to print
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def check(ok, msg, prefix=None):
        if ok:
            UtilsLogger.ok(msg, prefix)
        else:
            UtilsLogger.err(msg, prefix)

    # --------------------
    ## log a series of messages. Use ok() or err() as appropriate.
    #
    # @param ok      the check state
    # @param title   the line indicating what the check is about
    # @param msgs    individual list of lines to print
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def check_all(ok, title, msgs, prefix=None):
        UtilsLogger.check(ok, f'{title}: {ok}', prefix)
        for msg in msgs:
            UtilsLogger.check(ok, f'   - {msg}', prefix)

    # -------------------
    ## write a "====" line with the given message
    #
    # @param msg     the message to write
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def start(msg, prefix=None):
        UtilsLogger._write_line('====', msg, prefix)

    # -------------------
    ## write a "line" line with the given message
    #
    # @param msg     the message to write
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def line(msg, prefix=None):
        UtilsLogger._write_line(' ', msg, prefix)

    # -------------------
    ## write a "highlight" line with the given message
    #
    # @param msg     the message to write
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def highlight(msg, prefix=None):
        UtilsLogger._write_line('  ->', msg, prefix)

    # -------------------
    ## write a "ok" line with the given message
    #
    # @param msg     the message to write
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def ok(msg, prefix=None):
        UtilsLogger._write_line('OK', msg, prefix)

    # -------------------
    ## write a "err" line with the given message
    #
    # @param msg     the message to write
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def err(msg, prefix=None):
        UtilsLogger._write_line('ERR', msg, prefix)

    # -------------------
    ## write a "bug" line with the given message
    #
    # @param msg     the message to write
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def bug(msg, prefix=None):
        UtilsLogger._write_line('BUG', msg, prefix)

    # -------------------
    ## write an output line with the given message
    #
    # @param msg     the message to write
    # @param prefix  (optional) prefix for each line printed
    # @param lineno  (optional) the current line number for each line printed
    # @return None
    @staticmethod
    def output(msg, prefix=None, lineno=None):
        if lineno is None:
            tag = ' --    '
        else:
            tag = f' --{lineno: >3}] '
        UtilsLogger._write_line(tag, msg, prefix)

    # -------------------
    ## write a "warn" line with the given message
    #
    # @param msg     the message to write
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def warn(msg, prefix=None):
        UtilsLogger._write_line('WARN', msg, prefix)

    # -------------------
    ## write a "err" line with the given message
    #
    # @param msg     the message to write
    # @param prefix  (optional) prefix for each line printed
    # @return None
    @staticmethod
    def dbg(msg, prefix=None):
        UtilsLogger._write_line('DBG', msg, prefix)

    # -------------------
    ## write a raw line (no tag) with the given message
    #
    # @param msg     the message to write
    # @return None
    @staticmethod
    def raw(msg):
        UtilsLogger._write_line(None, msg)

    # -------------------
    ## write the given line to stdout
    #
    # @param tag     the prefix tag
    # @param msg     the message to write
    # @param prefix  (optional) prefix for line
    # @return None
    @staticmethod
    def _write_line(tag, msg, prefix=None):
        if not UtilsLogger.verbose:
            return

        # TODO add ability to optionally save to file

        if tag is None:
            line = msg
        elif prefix:
            line = f'{prefix} {tag: <4} {msg}'
        else:
            line = f'{tag: <4} {msg}'

        if UtilsLogger.ut_mode:
            UtilsLogger.ut_lines.append(line)
        else:
            print(line)  # print okay
        sys.stdout.flush()
