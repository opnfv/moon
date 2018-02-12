import sys
import python_moonclient

from cliff.app import App
from cliff.commandmanager import CommandManager


class Moon(App):
  
    def __init__(self):
        super(Moon, self).__init__(
          description='Moon client',
          version=python_moonclient.__version__,
          command_manager=CommandManager('moon'),
          deferred_help=True,
          )


def main(argv=sys.argv[1:]):
    myapp = Moon()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(Moon(sys.argv[1:]))



