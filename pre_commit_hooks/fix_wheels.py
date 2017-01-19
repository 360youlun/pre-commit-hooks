from __future__ import absolute_import

import argparse
import imp

from pre_commit_hooks.util import execute


def check_wheels(wheel_tool_path, wheel_house, wheel_files):
    """
    Checks new added packages if there they are
    """
    wheel_tool = imp.load_source('wheels', wheel_tool_path)
    built_or_not = False
    for filename in wheel_files:
        wheels = wheel_tool.Wheels(requirements_file=filename, wheelhouse_path=wheel_house)
        if wheels.has_changes:
            build_wheel_cmd = 'yl wheels:requirements=%s' % filename
            execute(build_wheel_cmd)
            built_or_not = True
    return built_or_not


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--wheel-tool')
    parser.add_argument('--wheel-house')
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.'
    )
    args = parser.parse_args(argv)
    status = check_wheels(args.wheel_tool, args.wheel_house, args.filenames)
    if status:
        print("=== Added new .whl files. Please, commit them as well.\n")
        return 1
    return 0


if __name__ == '__main__':
    exit(main())
