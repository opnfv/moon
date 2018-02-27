
class Parser:

    @staticmethod
    def add_common_options(parser):
        parser.add_argument('--consul-host', help='Set the name of the consul server (default: 127.0.0.1)', default="127.0.0.1")
        parser.add_argument('--consul-port', help='Set the port of the consult server (default: 30005)',default="30005")
        parser.add_argument("--verbose", "-v", action='store_true', help="verbose mode")
        parser.add_argument("--debug", "-d", action='store_true', help="debug mode")

    @staticmethod
    def add_filename_argument(parser):
        parser.add_argument('filename', help='configuration filename in json format')

    @staticmethod
    def add_name_argument(parser):
        Parser._add_name_argument(parser)

    @staticmethod
    def add_policy_argument(parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--policy-name', help='name of the policy')
        group.add_argument('--policy-id', help='id of the policy')

    @staticmethod
    def add_category_argument(parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--category-name', help='name of the category')
        group.add_argument('--category-id', help='id of the category')

    @staticmethod
    def add_id_or_name_argument(parser):
        group = parser.add_mutually_exclusive_group(required=True) 
        Parser._add_id_argument(group)
        Parser._add_name_argument(group)

    @staticmethod
    def _add_id_argument(parser):
        parser.add_argument('--id', help='id of the element')

    @staticmethod
    def _add_name_argument(parser):
        parser.add_argument('--name', help='name of the element')

    @staticmethod
    def add_id_or_name_pdp_argument(parser):
        group = parser.add_mutually_exclusive_group(required=True) 
        Parser._add_id_pdp_argument(group)
        Parser._add_name_pdp_argument(group)

    @staticmethod
    def _add_id_pdp_argument(parser):
        parser.add_argument('--id-pdp', help='id of the pdp')

    @staticmethod
    def _add_name_pdp_argument(parser):
        parser.add_argument('--name-pdp', help='name of the pdp')
    
    @staticmethod
    def add_id_or_name_project_argument(parser):
        group = parser.add_mutually_exclusive_group(required=True) 
        Parser._add_id_project_argument(group)
        Parser._add_name_project_argument(group)

    @staticmethod
    def _add_id_project_argument(parser):
        parser.add_argument('--id-project', help='id of the project')

    @staticmethod
    def _add_name_project_argument(parser):
        parser.add_argument('--name-project', help='name of the project')

    @staticmethod
    def add_authz_arguments(parser):
        parser.add_argument("--dry-run", "-n", action='store_true',
                            help="Dry run", dest="dry_run")
        parser.add_argument("--destination",
                            help="Set the type of output needed "
                                 "(default: wrapper, other possible type: "
                                 "interface).",
                            default="wrapper")
        parser.add_argument("--authz-host",
                            help="Set the name of the authz server to test"
                                 "(default: 127.0.0.1).",
                            default="127.0.0.1")
        parser.add_argument("--authz-port",
                            help="Set the port of the authz server to test"
                                 "(default: 31002).",
                            default="31002")
        parser.add_argument("--stress-test", "-s", action='store_true',
                            dest='stress_test',
                            help="Execute stressing tests (warning delta measures "
                                 "will be false, implies -t)")
        parser.add_argument("--write", "-w", help="Write test data to a JSON file",
                                default="/tmp/data.json")
