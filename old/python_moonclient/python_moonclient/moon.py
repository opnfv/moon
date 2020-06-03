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
    # import python_moonclient.python_moonclient.core.import_json
    # import python_moonclient.python_moonclient.core.models
    # import python_moonclient.core.policies.init as init_policy
    # import python_moonclient.core.pdp.init as init_pdp
    # consul_host = "consul"
    # consul_port = "8005"

    # init_model(consul_host, consul_port)
    # init_policy.init(consul_host, consul_port)
    # init_pdp.init(consul_host, consul_port)
    # import_json('/home/fcellier/moon/tests/functional/scenario_available/rbac.json')

    sys.exit(Moon(sys.argv[1:]))
