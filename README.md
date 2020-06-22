# Simple Service Registry Demo

This repo stands up a simple service registry, extended with cohorts
information.

Services are added to the registry by giving them a name and a URL;
the service registry queries their `service-info` endpoint.  If no
cohort information is provided there, it queries a `cohorts` endpoint.
Querying the service-

## Running

The stack can be run with:

```
docker-compose up --build
```

The UI will then be available at `http://localhost:2000`; the service
registry can be queried directly at `http://localhost:2001`. 

Services can be added to the service registry as follows:

```
cd backend
./add_service.py --database=data/services.sqlite [name] [base-url]
```
