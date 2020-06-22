"""
API Data Model definitions
"""

import dataclasses
from dataclasses import dataclass, field


@dataclass
class Error():
    status: int
    title: str
    detail: str


@dataclass
class ServiceType():
    group: str
    artifact: str
    version: str

    def __init__(self, **kwargs):
        names = set([f.name for f in dataclasses.fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)


@dataclass
class Organization():
    name: str
    url: str

    def __init__(self, **kwargs):
        names = set([f.name for f in dataclasses.fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)


@dataclass
class Service():
    id: str
    name: str
    type: ServiceType
    organization: Organization
    version: str
    cohorts: list = field(default_factory=list)
    contactUrl: str = ''
    documentationUrl: str = ''
    description: str = ''
    createdAt: str = ''
    updatedAt: str = ''
    environment: str = ''

    def __init__(self, **kwargs):
        names = set([f.name for f in dataclasses.fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)


@dataclass
class ExternalService():
    id: str
    name: str
    type: ServiceType
    organization: Organization
    version: str
    url: str
    cohorts: list = field(default_factory=list)
    contactUrl: str = ''
    documentationUrl: str = ''
    description: str = ''
    createdAt: str = ''
    updatedAt: str = ''
    environment: str = ''

    def __init__(self, **kwargs):
        names = set([f.name for f in dataclasses.fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)

