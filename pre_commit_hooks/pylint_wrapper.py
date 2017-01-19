from __future__ import with_statement
import argparse
import collections
import re
import subprocess

ExecutionResult = collections.namedtuple(
    'ExecutionResult',
    'status, stdout, stderr'
)


def get_score(stdout):
    rate_regexp = re.compile(r'^Your code has been rated at (\-?[0-9\.]+)/10', re.MULTILINE)
    rate = rate_regexp.findall(stdout)
    return float(rate[0]) if rate else 0


def execute(cmd, **kwargs):
    splitted_cmd = cmd.split()
    kwargs.setdefault('stdout', subprocess.PIPE)
    kwargs.setdefault('stderr', subprocess.PIPE)
    try:
        process = subprocess.Popen(splitted_cmd, **kwargs)
        stdout, stderr = process.communicate()
        return ExecutionResult(0, stdout, stderr)
    except OSError as e:
        print "Command exec error: '%s' %s" % (cmd, e)
        return ExecutionResult(1, '', '')


def pylint_check(pylint_conf, reports, pylint_report, files):
    files_string = " ".join(files)
    result = execute('pylint --rcfile=%s -r %s %s' % (pylint_conf, reports, files_string))
    with open(pylint_report, 'w') as f:
        f.write(result.stderr)
        f.write(result.stdout)
    if result.status:
        return 0
    return get_score(result.stdout)


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
    score = pylint_check(args.rcfile, args.reports, args.report_file, args.filenames)
    if score < args.score:
        print "=== PYLINT score: {:.2}/10.00".format(float(score))
        return 1
    return 0


if __name__ == '__main__':
    exit(main())
