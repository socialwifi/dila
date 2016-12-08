import cmd2

from dila import config
from dila.frontend import flask


class Dila(cmd2.Cmd):
    """Dila Commandline."""
    def do_run_dev_server(self, arg):
        print('Running dev server')
        config.setup(DEBUG=True)
        flask.create_app().run(host='0.0.0.0', port=80)


def run():
    import sys
    if len(sys.argv) > 1:
        Dila().onecmd(' '.join(sys.argv[1:]))
    else:
        Dila().cmdloop()


if __name__ == '__main__':
    run()
