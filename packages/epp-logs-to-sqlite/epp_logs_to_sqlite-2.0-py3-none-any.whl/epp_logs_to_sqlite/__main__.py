import argparse
from .logs_to_db import logs_to_db


def parse_arguments():
    parser = argparse.ArgumentParser(description='Save Eggplant test logs to a SQLite database')

    parser.add_argument('resultsPath', help='The path to the base directory of the test')
    args, _ = parser.parse_known_args()
    return args


if __name__ == '__main__':
    args = parse_arguments()
    logs_to_db(args.resultsPath)
