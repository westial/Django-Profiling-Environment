import uuid
from django.utils import timezone
from cqlengine import columns, connection
from cqlengine.models import Model


class Product(Model):

    id = columns.UUID(partition_key=True, primary_key=True,
                      default=uuid.uuid4())
    date = columns.Date(primary_key=True, clustering_order='DESC')
    title = columns.Text(required=True, max_length=90)
    description = columns.Text()
    image = columns.Text(max_length=255)
    inventory = columns.BigInt()
    created = columns.DateTime()
    modified = columns.DateTime()


class User(Model):

    email = columns.Text(partition_key=True, primary_key=True, required=True,
                         max_length=90)
    created = columns.DateTime()


class Sale(Model):

    product_id = columns.UUID(partition_key=True, primary_key=True,
                              required=True)
    user_email = columns.Text(partition_key=True, primary_key=True,
                              required=True, max_length=90)
    quantity = columns.Integer(required=True)
    created = columns.DateTime(primary_key=True, clustering_order='DESC')


# Cassandra Database Router Class
# Using cassandra database configuration for cassandra app
# see https://docs.djangoproject.com/en/1.7/topics/db/multi-db/

class CassandraRouter(object):
    """
    A router to control all database operations on models in the
    cassandra application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read cassandra models go to cassandra db.
        """
        if model._meta.app_label == 'app_cassandra':

            return 'cassandra'

        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write cassandra models go to cassandra db.
        """
        if model._meta.app_label == 'app_cassandra':

            return 'cassandra'

        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the cassandra app is involved.
        """
        if obj1._meta.app_label == 'app_cassandra' or \
           obj2._meta.app_label == 'app_cassandra':

           return True

        return None

    def allow_migrate(self, db, model):
        """
        Make sure the cassandra app only appears in the 'cassandra'
        database.
        """
        if db == 'cassandra':

            return model._meta.app_label == 'app_cassandra'

        elif model._meta.app_label == 'app_cassandra':

            return False

        return None