#!/usr/bin/env python3


import argparse
import sys
import logging
from Core import nextDiscFunctions


def main():
    parser = argparse.ArgumentParser(description='nextdisc v1.0\nBy m0noid')
    parser.add_argument('url', nargs='*', help='URL(s) for processing')
    parser.add_argument('-o', '--output', help='output')
    parser.add_argument('-u', '--user-agent', default='nextdisc/1.0', help='User-Agent')
    parser.add_argument('-t', '--timeout', type=float, default=10, help='Timeout in seconds')
    parser.add_argument('-v', '--verbose', action='store_true', help='Logging')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    if not args.url:
        if sys.stdin.isatty():
            parser.error("[!] no urls found at stdin")
        else:
            args.url = [line.strip() for line in sys.stdin if line.strip()]

    all_paths = set()
    for target in args.url:
        target = target.rstrip('/')
        logging.info(f"[!] Processing URL: {target}")
        page_content = nextDiscFunctions.get_page_content(target, args.user_agent, args.timeout)
        if not page_content:
            continue

        next_data = nextDiscFunctions.extract_next_data(page_content)
        if next_data:
            paths = nextDiscFunctions.parse_next_data(next_data)
            all_paths.update(paths)

        for manifest_name in ['_buildManifest', '_ssgManifest', '_middlewareManifest']:
            paths = nextDiscFunctions.process_additional_manifest(target, manifest_name, page_content, args.user_agent, args.timeout)
            all_paths.update(paths)

        routes_manifest = nextDiscFunctions.get_routes_manifest(target, args.user_agent, args.timeout)
        if routes_manifest:
            paths = nextDiscFunctions.parse_routes_manifest(routes_manifest)
            all_paths.update(paths)

    if all_paths:
        output = '\n'.join(sorted(all_paths))
        if args.output:
            try:
                with open(args.output, 'w') as f:
                    f.write(output)
                logging.info(f"[!] file saved at: {args.output}")
            except IOError as e:
                logging.error(f"[!] erro while saving {args.output}: {e}")
        else:
            print(output)
    else:
        logging.info("Paths not found")

if __name__ == '__main__':
    main()
