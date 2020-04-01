import datetime
from functools import partial

import factory
from faker import Factory as FakerFactory

from app import models
from app.tests.utils.session import TestSession

faker = FakerFactory.create()


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta(object):
        model = models.User
        sqlalchemy_session = TestSession
        sqlalchemy_session_persistence = 'commit'

    email = factory.Faker("safe_email")
    username = factory.LazyAttribute(lambda x: faker.name())
    first_name = factory.LazyAttribute(lambda x: faker.name())
    last_name = factory.LazyAttribute(lambda x: faker.name())
    full_name = factory.LazyAttribute(lambda obj: f'{obj.first_name} {obj.last_name}')
    is_active = True
    is_staff = True
    is_eeci = True
    is_superuser = False
    date_joined = factory.LazyFunction(partial(datetime.datetime.now, datetime.timezone.utc))
    hashed_password = 'stub_hash'
