from django.db import models


class Product(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=90)
    date = models.DateField()
    description = models.TextField()
    image = models.CharField(max_length=255)
    inventory = models.BigIntegerField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True, auto_now=True)


class User(models.Model):

    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=90)
    created = models.DateTimeField(auto_now_add=True)


class Sale(models.Model):

    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)


# MySQL Database Router Class
# Using mysql database configuration for mysql app
# see https://docs.djangoproject.com/en/1.7/topics/db/multi-db/

class MySQLRouter(object):
    """
    A router to control all database operations on models in the
    mysql application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to mysql db.
        """
        if model._meta.app_label == 'app_rdbms':

            return 'mysql'

        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write mysql models go to mysql db.
        """
        if model._meta.app_label == 'app_rdbms':

            return 'mysql'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the mysql app is involved.
        """
        if obj1._meta.app_label == 'app_rdbms' or \
           obj2._meta.app_label == 'app_rdbms':

           return True

        return None

    def allow_migrate(self, db, model):
        """
        Make sure the auth app only appears in the 'mysql'
        database.
        """
        if db == 'mysql':

            return model._meta.app_label == 'app_rdbms'

        elif model._meta.app_label == 'app_rdbms':

            return False

        return None