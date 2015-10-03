# coding=utf-8

import sys
import wa.utils
from wa.env import Environment


def main():
    if len(sys.argv) == 1:
        print('wa: workflow automation tool')
        sys.exit()

    env = Environment()
    manifest = wa.utils.find_manifest()
    env.set_project_root(manifest)
    wa.utils.parse_args(env, sys.argv[1:])
