import signal

import cmd2
import sys

import os

import pathlib

from dila.frontend import flask
from dila.frontend import initialize

TERMINATION_SIGNALS = [signal.SIGTERM, signal.SIGQUIT, signal.SIGINT]


def register_termination_signals():
    def terminate(signum, frame):
        sys.exit(0)

    for signum in TERMINATION_SIGNALS:
        signal.signal(signum, terminate)


class Dila(cmd2.Cmd):
    """Dila Commandline."""
    def do_run_dev_server(self, arg):
        initialize.initialize()
        print('Running dev server')
        flask.main(initialized=True).run(host='0.0.0.0', port=80)

    def do_migrate(self, arg):
        initialize.initialize()
        print('migrating')
        os.execv('/usr/local/bin/alembic', [
            'alembic', '-c', str(pathlib.Path(__file__).parent.parent / 'alembic.ini'),
            'upgrade', 'head'])

    def do_tar_static(self, arg):
        print('migrating')
        os.execv('/bin/tar', [
            'tar', '-c', '-C', str(pathlib.Path(__file__).parent / 'flask/static'), '.'])


def run():
    import sys
    register_termination_signals()
    if len(sys.argv) > 1:
        Dila().onecmd(' '.join(sys.argv[1:]))
    else:
        Dila().cmdloop()


if __name__ == '__main__':
    run()
