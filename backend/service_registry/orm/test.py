# pylint: disable=redefined-outer-name
"""
create empty db
"""
import os
import uuid

from service_registry.orm import dump, init_db, get_session
from service_registry.orm.models import URL


def empty_db(db_filename="services.db"):  # pylint: disable=too-many-locals
    """
    Create an empty db
    """
    # delete db if already exists
    try:
        os.remove(db_filename)
    except OSError:
        pass

    init_db('sqlite:///'+db_filename)
    session = get_session(expire_on_commit=False)

    session.commit()