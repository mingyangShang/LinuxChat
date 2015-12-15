#coding:utf-8

from django.db import models
from datetime import datetime
from time import strftime

#
# Custom field types in here.
#
class TimestampField(models.DateTimeField):
    """TimestampField: creates a DateTimeField that is represented on the
    database as a TIMESTAMP field rather than the usual DATETIME field.
    """
    op_params=''
    def __init__(self, null=False, blank=False, op_params='', **kwargs):
        super(TimestampField, self).__init__(**kwargs)
        # default for TIMESTAMP is NOT NULL unlike most fields, so we have to
        # cheat a little:
        self.blank, self.isnull = blank, null
        self.null = True # To prevent the framework from shoving in "not null".

    def db_type(self, connection):
        typ=['TIMESTAMP']
        # See above!
        if self.isnull:
            typ += ['NULL']
        if self.op_params != '':
            typ += [self.op_params]
        return ' '.join(typ)

    def to_python(self, value):
        return datetime.from_timestamp(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value==None:
            return None
        return strftime('%Y%m%d%H%M%S',value.timetuple())

    def to_python(self, value):
        return value