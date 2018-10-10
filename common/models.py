from peewee import *
from common.conf import *

DB = SqliteDatabase(DB_PATH)

class BaseModel(Model):

    class Meta:
        database = DB

class Purchases(BaseModel):
    rowid = IntegerField()

    id_card = TextField()
    id_oper = TextField()
    date_time = DateTimeField()
    summ = DecimalField()
    summ_dics = DecimalField()
    type_oper = IntegerField()
    comment = TextField()

    class Meta:
        table_name = 'purchases'

class BonusOperations(BaseModel):
    rowid = IntegerField()
    
    id_card = TextField()
    date_time = DateTimeField()
    summ = DecimalField()
    comment = TextField()

    class Meta:
        table_name = 'bonus_operations'

