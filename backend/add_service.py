#!/usr/bin/env python3
import sys
import uuid
import argparse
from service_registry.orm.models import URL
from service_registry.orm import init_db, get_session


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser('Run service registry')
    parser.add_argument('--database', default="./data/services.sqlite")
    parser.add_argument('name', type=str)
    parser.add_argument('url', type=str)
    args = parser.parse_args(args)

    init_db(uri="sqlite:///"+args.database)
    db_session = get_session()

    new_url = URL(url=args.url, name=args.name, id=uuid.uuid4())
    db_session.add(new_url)
    db_session.commit()


if __name__ == "__main__":
    main()
