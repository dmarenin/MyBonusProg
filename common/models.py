from peewee import *

DB = SqliteDatabase('D:\\repos\\MyBonusProg\\common\\db.db')

class BaseModel(Model):

    class Meta:
        database = DB

class Purchases(BaseModel):
    id_card = TextField()
    id_oper = TextField()
    date_time = DateTimeField()
    summ = DecimalField()
    summ_dics = DecimalField()
    type_oper = IntegerField()

    class Meta:
        table_name = 'purchases'

class BonusOperations(BaseModel):
    id_card = TextField()
    date_time = DateTimeField()
    summ = DecimalField()

    class Meta:
        table_name = 'bonus_operations'

