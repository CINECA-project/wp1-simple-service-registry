"""
Pre- and post- hooks for the dredd tests to ensure that
the tests are made in the correct order, and that IDs
returned previously are used in proceeding API calls
"""
import sys
import dredd_hooks as hooks

ORDER = ["/services > List services in the registry > 200 > application/json",
         "/services/{serviceId} > Find service in the registry by ID > 200 > application/json",
         "/services/{serviceId} > Find service in the registry by ID > 404 > application/json",
         "/services/types > List types of services exposed by the registry > 200 > application/json"]
        
# Dredd incorrectly thinks all fields in Service are required so fails service-ifo
#         "/service-info > Show information about the registry > 200 > application/json"]

@hooks.before_all
def reorder_actions(transactions):
    """
    Order the endpoint calls in the order given by ORDER,
    skipping calls that aren't present.

    Optionally output all the endpoints in an easy-to-use format
    """
    def sort_key(transaction):
        if not transaction['name'] in ORDER:
            return 10000
        else:
            return ORDER.index(transaction['name'])

    transactions.sort(key=sort_key)
    for transaction in transactions:
        transaction['skip'] = (transaction['name'] not in ORDER)

    for transaction in transactions:
        print(transaction, file=sys.stderr, flush=True)

UUID_EXAMPLE = "3c4b179d-1857-489b-b1eb-0a2fa2c5c21f"
GOOD_UUID_EXAMPLE = "1b037a70-06b2-40e0-9e94-18865ce86d73"
BAD_UUID_EXAMPLE = "bf3ba75b-8dfe-4619-b832-31c4a087a589"


@hooks.before("/services/{serviceId} > Find service in the registry by ID > 200 > application/json")
def insert_good_id(transaction):
    "Put the saved individual ID into the URL"
    transaction['fullPath'] = transaction['fullPath'].replace(UUID_EXAMPLE, GOOD_UUID_EXAMPLE)

@hooks.before("/services/{serviceId} > Find service in the registry by ID > 404 > application/json")
def insert_bad_id(transaction):
    "Put the saved individual ID into the URL"
    transaction['fullPath'] = transaction['fullPath'].replace(UUID_EXAMPLE, BAD_UUID_EXAMPLE)
