import requests
import wap
import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "url",
        help="Url to request"
    )

    parser.add_argument(
        "--file",
        help="File with apps regexps",
        default="apps.json"
    )

    parser.add_argument(
        "--confidence", "-c",
        help="Show confidence (between 0 and 100)",
        action="store_true",
    )

    parser.add_argument(
        "--version", "-b",
        help="Show version",
        action="store_true",
    )

    parser.add_argument(
        "--category", "-k",
        help="Show categories",
        action="store_true",
    )

    parser.add_argument(
        "--delimiter", "-d",
        help="Set fields delimiter",
        default=" "
    )

    return parser.parse_args()


def main():
    args = parse_args()
    technologies, _ = wap.load_file(args.file)

    resp = requests.get(args.url)

    techno_matches = wap.discover_requests_technologies(technologies, resp)

    for t in techno_matches:
        fields = [t.technology.name]

        if args.version:
            fields.append(t.version)

        if args.confidence:
            fields.append(str(t.confidence))

        if args.category:
            fields.append(",".join(
                [c.name for c in t.technology.categories]
            ))

        print(args.delimiter.join(fields))


if __name__ == '__main__':
    main()
