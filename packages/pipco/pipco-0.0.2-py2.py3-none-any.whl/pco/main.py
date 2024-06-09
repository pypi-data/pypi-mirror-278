import argparse
import sys


def show_current_source():
    # Implement logic to show current pip source
    print("Current pip source is pypi.")


def change_source(source_name):
    # Implement logic to change pip source
    print(f"Source changed to {source_name}.")


def list_sources():
    # Implement logic to list all available sources
    sources = {
        "pypi": "https://pypi.python.org/simple/",
        "douban": "http://pypi.douban.com/simple/",
        "aliyun": "http://mirrors.aliyun.com/pypi/simple/",
        "qinghua": "https://mirrors.tuna.tsing. hua.edu.cn/pypi/web/simple/"
    }
    for key, value in sources.items():
        print(f"{key}: {value}")


def main():
    parser = argparse.ArgumentParser(description="Manage pip sources easily")
    parser.add_argument('-n', '--name', action='store_true', help='Show current pip source')
    parser.add_argument('-c', '--change', metavar='SOURCE', help='Change the pip source')
    parser.add_argument('-list', action='store_true', help='List available pip sources')

    args = parser.parse_args()

    if args.name:
        show_current_source()
    elif args.change:
        change_source(args.change)
    elif args.list:
        list_sources()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
