from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import re
import yaml


def generate_directory_pattern(dirs):
    """generate the regex pattern for match a list of directories
    :arg dirs the list of directories
    :type dirs list
    """
    pattern_dirs = []
    for d in dirs:
        if '.' in d:
            d = d.replace('.', r'\.').replace('*', '.*')
            d += '$'
        else:
            d = d.replace('*', '.*')
            d += '.*'
        pattern_dirs.append(d)
    pattern = r'^(?:%s)' % '|'.join(pattern_dirs)
    return pattern


def project_mapping_check(config, changed_files):
    """
    Checks if none mapped files changed based on project mapping file
    """
    map_file = open(config, 'r')
    mappings = yaml.safe_load(map_file)['mappings']
    none_mapped = []
    for f in changed_files:
        all_dirs = [d for p in mappings.values() for d in p]
        all_dirs = list(set(all_dirs))
        pattern = generate_directory_pattern(all_dirs)
        regex = re.compile(pattern)
        if not regex.match(f):
            none_mapped.append(f)
    return none_mapped


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--config')
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)
    none_mapped_files = project_mapping_check(args.config, args.filenames)
    if none_mapped_files:
        print("=== There are files changed which didn't matched to any projects ===")
        for f in none_mapped_files:
            print(f)
        print("=== Please add those files to the mapping file of 'projmap.yaml' in the root of codebase ===")
        return 1
    return 0


if __name__ == '__main__':
    exit(main())
