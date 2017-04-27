import uuid

import sqlalchemy
import sqlalchemy.dialects.postgresql as postgres_dialect

from dila.application import structures
from dila.data import engine


class Resource(engine.Base):
    __tablename__ = 'resource'
    id = sqlalchemy.Column(postgres_dialect.UUID(as_uuid=True), default=uuid.uuid4,
                           server_default=sqlalchemy.text("uuid_generate_v4()"), primary_key=True,
                           nullable=False)
    name = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)

    def as_data(self):
        return structures.Resource(pk=self.id, name=self.name)


def add_resource(name):
    resource = Resource(name=name)
    engine.session.add(resource)
    engine.session.flush()
    return resource.as_data()


def get_resource(pk):
    return Resource.query.get(pk).as_data()


def get_resources():
    for resource in Resource.query.all():
        yield resource.as_data()
