import cmd2


class Dila(cmd2.Cmd):
    """Dila Commandline."""
    def do_run_dev_server(self, arg):
        print('Running dev server')


def run():
    import sys
    if len(sys.argv) > 1:
        Dila().onecmd(' '.join(sys.argv[1:]))
    else:
        Dila().cmdloop()


if __name__ == '__main__':
    run()
