import argparse

from .constants import URL_ENDPOINT
import requests


def parse_args():
    """
    Parses arguments using argparse and returns parse_args()
    :return:
    :rtype:
    """
    parser = argparse.ArgumentParser(
        'Zap AppImage Package Manager',
        description=''
    )
    parser.add_argument(
        'appname',
        default=''
    )
    return parser.parse_args()


class Zap:
    def __init__(self, appname):
        self.app = appname.lower()
        pass

    def install(self):
        r = requests.get(URL_ENDPOINT.format(self.app))
        if not r.status_code == 200:
            # the app does not exist or the name provided is incorrect
            print("Sorry. The app does not exist on our database.")
            return
        result_core_api = r.json()
        print("{} - {}".format(self.app, result_core_api['latest_release']))
        input("Ok?")


if __name__ == "__main__":
    args = parse_args()
    zap = Zap(args.appname)
