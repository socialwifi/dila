import cmd2

from dila.frontend import wsgi


class Dila(cmd2.Cmd):
    """Dila Commandline."""
    def do_run_dev_server(self, arg):
        print('Running dev server')
        wsgi.create_app().run(host='0.0.0.0', port=80)


def run():
    import sys
    if len(sys.argv) > 1:
        Dila().onecmd(' '.join(sys.argv[1:]))
    else:
        Dila().cmdloop()


if __name__ == '__main__':
    run()
