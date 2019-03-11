import webbrowser
import sys
import inspect
from types import TracebackType


def handle(func):
    def err_handle_inner(*args, **kwrgs):
        try:
            return func(*args, **kwrgs)
        except Exception as e:
            err = Error(e)
            err.printmsg()
            err.search()
    return err_handle_inner


class Error:
    def __init__(self, error):
        self.error = error
        self.search_url = 'https://stackoverflow.com/search?q={} python'.format(str(self))

    def __str__(self):
        if self.error.__class__.__module__ == 'builtins':
            fmt = '{}{}: {}'.format
            module = ''
        else:
            fmt = '{}.{}: {}'.format
            module = self.error.__class__.__module__

        return fmt(module, self.error.__class__.__name__, str(self.error))

    def msg(self):
        tb = self.error.__traceback__
        if tb is None:
            return ''
        msg = 'Traceback (most recent call last):\n{stacktrace}{errmsg}'
        return msg.format(
            stacktrace=self._stacktrace_msg(tb),
            errmsg=str(self),
        )

    def search(self):
        webbrowser.open_new_tab(self.search_url)

    def printmsg(self, out=sys.stdout):
        out.write(self.msg())

    @staticmethod
    def _stacktrace_msg(tb):
        if not isinstance(tb, (TracebackType, type(None))):
            raise TypeError('did not give a traceback object')
        info = '  File "{file}", line {line}, in {func}\n    {code}\n'.format
        c = tb.tb_frame.f_code

        err_info = info(
            file=c.co_filename,
            line=tb.tb_lineno,
            func=c.co_name,
            code=getsource_at(c, tb.tb_lineno),
        )

        if tb.tb_next is None:
            ending = ''
        else:
            ending = Error._stacktrace_msg(tb.tb_next)

        return '{}{}'.format(err_info, ending)


def getsource_at(obj, lineindex):
    lines = inspect.findsource(obj)[0]
    return lines[lineindex - 1].strip()


if __name__ == '__main__':
    @handle
    def raises_overflow():
        return raises_overflow()

    @handle
    def raises_err():
        raise Exception('test error')

    class CustumError(Exception):
        pass

    try:
        raise CustumError('test')
    except CustumError as e:
        err = Error(e)
        # print(err.msg())

    raises_overflow()
