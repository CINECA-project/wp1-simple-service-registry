#!/usr/bin/env python3
"""
Driver program for service
"""
import sys
import argparse
import logging
import pkg_resources
import connexion
from tornado.options import define
import service_registry.orm


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser('Run service registry')
    parser.add_argument('--database', default="./data/services.sqlite")
    parser.add_argument('--host', default="0.0.0.0")
    parser.add_argument('--port', default=3000)
    parser.add_argument('--logfile', default="./log/services.log")
    parser.add_argument('--loglevel', default='INFO',
                        choices=['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL'])
    args = parser.parse_args(args)

    # set up the application
    app = connexion.FlaskApp(__name__, server='tornado')
    define("dbfile", default=args.database)
    define("host", args.host)
    define("port", args.port)
    service_registry.orm.init_db()
    db_session = service_registry.orm.get_session()

    @app.app.teardown_appcontext
    def shutdown_session(exception=None):  # pylint:disable=unused-variable,unused-argument
        """
        Tear down the DB session
        """
        db_session.remove()

    # configure logging
    log_handler = logging.FileHandler(args.logfile)
    numeric_loglevel = getattr(logging, args.loglevel.upper())
    log_handler.setLevel(numeric_loglevel)

    app.app.logger.addHandler(log_handler)
    app.app.logger.setLevel(numeric_loglevel)

    # add the swagger APIs
    api_def = pkg_resources.resource_filename('service_registry',
                                              'api/swagger.yaml')
    app.add_api(api_def, strict_validation=True, validate_responses=True)

    app.run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
