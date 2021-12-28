from argparse import ArgumentParser


def get_cmdline_params():
    parser = ArgumentParser(description="Synctify")
    parser.add_argument(
        "-e", "--environment",
        required=True,
        choices=["devl", "test", "prod"],
        help="Environment - devl, test or prod"
    )
    parser.add_argument(
        "-c", "--cfgfile",
        required=False,
        default="synctify.cfg",
        help="Name of the configuration file to use"
    )
    args = parser.parse_args()
    return vars(args)
