import argparse

from orcan.core.config import Config
from orcan.core.runner import Runner

def arguments():
    parser = argparse.ArgumentParser(
        prog="reco", description="not the best reconnaissance tool, but it is a reconnaissance tool"
    )
    parser.add_argument(
        "--url",
        help="the addy", # todo: implement lookup so we can use ip and crt.sh works
    )
    parser.add_argument(
        "--domain",
        help="get subdomains",
        default="false",
        action="store_true",
    )
    parser.add_argument(
        "--who",
        help="get whois data",
        default="false",
        action="store_true",
    )
    args = parser.parse_args()
    return Config(args)


def main():
    config = arguments()
    Runner(config).run()
