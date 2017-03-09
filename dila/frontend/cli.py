import cmd2

from dila import application
from dila.frontend import flask
from dila.frontend import initialize


class Dila(cmd2.Cmd):
    """Dila Commandline."""
    def do_run_dev_server(self, arg):
        print('Running dev server')
        flask.main().run(host='0.0.0.0', port=80)


def run():
    import sys
    register_termination_signals()
    initialize.initialize_config()
    application.setup()
    if len(sys.argv) > 1:
        Dila().onecmd(' '.join(sys.argv[1:]))
    else:
        Dila().cmdloop()


if __name__ == '__main__':
    run()
