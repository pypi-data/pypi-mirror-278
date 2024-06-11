import re
import sys
import json
import datetime
import argparse

from send_s3.db import Database
from send_s3.common import LINESEP, Console

DATE_REGEX = r'^\d{4}-\d{2}-\d{2}$'
TIME_REGEX = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'


def human_readable_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    size /= 1024
    if size < 1024:
        return f"{size:.2f} KB"
    size /= 1024
    if size < 1024:
        return f"{size:.2f} MB"
    size /= 1024
    return f"{size:.2f} GB"


def main(args: argparse.Namespace) -> int:
    db = Database()
    time_from, time_to = None, None
    if args.time_from:
        if re.match(DATE_REGEX, args.time_from):
            args.time_from += 'T00:00:00'
        if not re.match(TIME_REGEX, args.time_from):
            Console() >> f"ERROR: Invalid time format in '--from': {args.time_from}" >> sys.stderr
            return 1
        time_from = datetime.datetime.strptime(args.time_from, '%Y-%m-%dT%H:%M:%S')
    if args.time_to:
        if re.match(DATE_REGEX, args.time_to):
            args.time_to += 'T23:59:59'
        if not re.match(TIME_REGEX, args.time_to):
            Console() >> f"ERROR: Invalid time format in '--to': {args.time_to}" >> sys.stderr
            return 1
        time_to = datetime.datetime.strptime(args.time_to, '%Y-%m-%dT%H:%M:%S')
    logs = db.select(args.limit, time_from, time_to, args.name)
    logs = list(logs)
    if args.json:
        Console() >> json.dumps(logs, indent=2, ensure_ascii=False) >> sys.stdout
        return 0
    for log in logs:
        date = datetime.datetime.fromtimestamp(log['timestamp']).strftime('%Y-%m-%d %H:%M:%S %Z')
        Console() >> "\033[1;32m" >> log['checksum'] >> "\033[0m" >> LINESEP >> sys.stdout
        Console() >> "\033[1;33m" >> f"Date: \033[0m{date}" >> LINESEP >> sys.stdout
        Console() >> "\033[1;33m" >> f"File: \033[0m{log['filepath']}" >> LINESEP >> sys.stdout
        Console() >> "\033[1;33m" >> f"Key:  \033[0m{log['key']}" >> LINESEP >> sys.stdout
        Console() >> "\033[1;33m" >> f"Size: \033[0m{human_readable_size(log['size'])}" >> LINESEP >> sys.stdout
        Console() >> "\033[1;33m" >> f"URL:  \033[0m{log['url']}" >> LINESEP >> sys.stdout
        Console() >> LINESEP >> sys.stdout
        download_links = log['data'].get('download_links', {})
        max_len = max(map(len, download_links.keys()))
        for domain, url in download_links.items():
            Console() >> '    ' >> f"download_url/{domain:<{max_len}}: {url}" >> LINESEP >> sys.stdout
        Console() >> LINESEP >> ("-" * 60) >> LINESEP >> sys.stdout
    return 0


def register_arguments(parser: argparse.ArgumentParser):
    parser.add_argument('-f', '--from', dest='time_from',
                        help='Time from, format: "Y-m-d" or "Y-m-dTH:M:S"', required=False, default=None)
    parser.add_argument('-t', '--to', dest='time_to',
                        help='Time to, format: "Y-m-d" or "Y-m-dTH:M:S"', required=False, default=None)
    parser.add_argument('-n', '--name', dest='name',
                        help='Keyword of name (or path) of original file to search', required=False, default=None)
    parser.add_argument('-l', '--limit', dest='limit',
                        help='Limit the number of logs to show', required=False, default=100, type=int)
    parser.add_argument('--json', dest='json', action='store_true', help='Output in JSON format')


__all__ = ['main', 'register_arguments']
