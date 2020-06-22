# pylint: disable=invalid-name
# pylint: disable=C0301
"""
Implement endpoints of model service
"""
import sys
from urllib.parse import urljoin
import requests
from service_registry import orm
from service_registry.orm import models
from service_registry.api.logging import apilog
from service_registry.api.models import Error, ServiceType
from service_registry.api.models import Service, ExternalService
from service_registry.orm.models import URL

SERVICE_NAME = "CINECA Service Registry"
THIS_SERVICE_TYPE = ServiceType(group='org.ga4gh', artifact='service-registry', version='1.0.0')
THIS_SERVICE = Service(id='this.service',
                       name='CINECA service registry',
                       type=THIS_SERVICE_TYPE,
                       description='CINECA service registry',
                       organization={'name': "CINECA", 'url': 'www.cineca-project.eu'},
                       version='1.0.0')

def get_service_info(url):
    """
    Fetch service info from url
    """
    service_info_url = urljoin(f"{url}/", "service-info")
    print(f"[{SERVICE_NAME}] Contacting {service_info_url}", flush=True)
    try:
        r = requests.get(service_info_url, timeout=1)
        if r.status_code != 200:
            print(f"[{SERVICE_NAME}] Non-200 status code on {service_info_url}: {r.status_code}", file=sys.stderr,
                  flush=True)
            return None
    except requests.exceptions.Timeout:
        print(f"[{SERVICE_NAME}] Encountered timeout with {service_info_url}", file=sys.stderr, flush=True)
        return None

    service_data = r.json()
    if "cohorts" not in service_data:
        cohort_url = urljoin(f"{url}/", "cohorts")
        cr = requests.get(cohort_url, timeout=1)
        if cr.status_code != 200:
            print(f"[{SERVICE_NAME}] No cohort data available at f{url}", file=sys.stderr, flush=True)
        else:
            service_data.update["cohorts"] = cr.json()

    return Service(**service_data)


@apilog
def list_services():
    """
    Return all known and active services
    """
    db_session = orm.get_session()
    try:
        urls = URL().query.all()
    except orm.ORMException as e:
        return Error(status=500, title='Error connecting to database', detail=str(e)), 500

    external_services = []
    for url in urls:
        service = get_service_info(url.url)
        if not service:
            continue
        # overwrite ID and name with local values
        service.id = url.id
        service.name = url.name
        service_as_dict = orm.dump(service)
        service_as_dict['url'] = url.url

        external_services.append(ExternalService(**service_as_dict))

    return [orm.dump(ext_svc) for ext_svc in external_services], 200, {'Access-Control-Allow-Origin':'*'}


@apilog
def get_one_service(serviceId):
    """
    Return info for one service
    """
    db_session = orm.get_session()
    try:
        q = db_session.query(models.URL).get(serviceId)
    except orm.ORMException as e:
        return Error(status=500, title='Error connecting to database', detail=str(e)), 500

    if not q:
        return Error(title="No such service found", detail="No result for service "+str(serviceId), status=404), 404

    service = get_service_info(q.url)

    if not service:
        return Error(title="Service not available", detail="Could not connect to service "+str(serviceId), status=404), 404

    # overwrite ID and name with local values
    service.id = q.id
    service.name = q.name
    service_as_dict = orm.dump(service)
    service_as_dict['url'] = q.url
    external_service = ExternalService(**service_as_dict)
    return orm.dump(external_service), 200, {'Access-Control-Allow-Origin':'*'}


@apilog
def get_this_service():
    """
    Return info for this service
    """
    return orm.dump(THIS_SERVICE), 200, {'Access-Control-Allow-Origin':'*'}


@apilog
def list_service_types():
    """
    Return all known and active services
    """
    db_session = orm.get_session()
    try:
        urls = URL().query.all()
    except orm.ORMException as e:
        return Error(status=500, title='Error connecting to database', detail=str(e)), 500

    service_types = []
    for url in urls:
        service = get_service_info(url.url)
        if not service:
            continue
        service_type = ServiceType(**service.type)
        if not service_type in service_types:
            service_types.append(service_type)

    return [orm.dump(svc_type) for svc_type in service_types], 200, {'Access-Control-Allow-Origin':'*'}
