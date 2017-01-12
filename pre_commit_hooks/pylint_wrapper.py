import argparse
import re
import sys

from pylint import epylint as lint


def get_score(stdout):
    rate_regexp = re.compile(r'^Your code has been rated at (\-?[0-9\.]+)/10', re.MULTILINE)
    rate = rate_regexp.findall(stdout)

    return float(rate[0]) if rate else 0


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--rcfile')
    parser.add_argument('--reports')
    parser.add_argument('--report-file', default='pylint-report.txt')
    parser.add_argument('--score', type=float, default=9.5)
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.'
    )
    args = parser.parse_args(argv)
    files = " ".join(args.filenames)
    stdout, stderr = lint.py_run("{} --rcfile {} --reports {}".format(files, args.rcfile, args.reports),
                                 return_std=True)
    return_value = 0
    with open(args.report_file, 'w') as pylint_report:
        if stderr:
            print 'test'
            print stderr.read()
            pylint_report.write(stderr.read())
            return_value = 1
        else:
            pylint_report.write(stdout.read())
            score = get_score(stdout.read())
            if score < args.score:
                print "=== PYLINT score: {:.2}/10.00".format(float(score))
                return_value = 1
    return return_value


if __name__ == '__main__':
    exit(main())
