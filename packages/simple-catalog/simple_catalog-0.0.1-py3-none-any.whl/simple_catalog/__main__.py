import sys
import argparse

from . import Client


def main():
    parser = argparse.ArgumentParser(description="simple_catalog")
    parser.add_argument("--host", help="database host", required=True)
    parser.add_argument("--user", help="database user", required=True)
    parser.add_argument("--password", help="database password", required=True)
    parser.add_argument("--database", help="database", required=True)
    parser.add_argument("--file", help="file to register", required=True)
    parser.add_argument("--salt", help="seed value used for hashing", required=True)
    parser.add_argument("--product", help="product name")
    parser.add_argument("--revision", help="revision number")
    parser.add_argument("--hash", help="repository hash")
    parser.add_argument("--add", action="store_true", help="add file to catalog")
    parser.add_argument(
        "--delete", action="store_true", help="delete file from catalog"
    )
    parser.add_argument(
        "--check", action="store_true", help="check if file exists in catalog"
    )

    try:
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        print(f"Argument parsing error: {e}")
        parser.print_help()
        sys.exit(-1)

    if not args.add and not args.delete and not args.check:
        parser.print_help()
        sys.exit(-1)

    client = Client(
        args.host,
        args.user,
        args.password,
        args.database,
        args.salt,
        args.product,
        args.revision,
        args.hash,
    )

    if args.add:
        client.add(args.file)
    elif args.delete:
        result = client.delete(args.file)
        if result is None:
            print("Entry not found")
        else:
            print(result)
    elif args.check:
        result = client.check(args.file)
        if result is None:
            print("No matching hash found")
        else:
            for entry in result:
                print(entry)


if __name__ == "__main__":
    main()
