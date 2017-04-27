import uuid

import sqlalchemy
import sqlalchemy.dialects.postgresql as postgres_dialect

from dila.data import engine


class Resource(engine.Base):
    __tablename__ = 'resource'
    id = sqlalchemy.Column(postgres_dialect.UUID(as_uuid=True), default=uuid.uuid4,
                           server_default=sqlalchemy.text("uuid_generate_v4()"), primary_key=True,
                           nullable=False)
    name = sqlalchemy.Column(sqlalchemy.Text(), nullable=False)


def add_resource(name):
    resource = Resource(name=name)
    engine.session.add(resource)
    engine.session.flush()
    return resource.id
