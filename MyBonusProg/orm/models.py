from peewee import *
from server.conf import DB_PATH

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

class Bonus_Operations(BaseModel):
    rowid = IntegerField()
    
    id_card = TextField()
    date_time = DateTimeField()
    summ = DecimalField()
    comment = TextField()
    id_purchases = IntegerField()

    class Meta:
        table_name = 'bonus_operations'

