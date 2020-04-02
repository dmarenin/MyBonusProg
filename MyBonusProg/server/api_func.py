from orm.models import *
from datetime import datetime, date, timedelta
from server.conf import *


def info(param):
    id_card = kwargs_get(param, 'id_card')

    bonus_info = get_bonus_info(id_card)
    
    summ = bonus_info['summ']
    summ_availible = bonus_info['summ_availible'] 
    bonus_opperations = bonus_info['bonus_opperations']

    purchases = get_purchases(id_card)  

    summ_purchases = 0
    for x in purchases:
        if (datetime.now()-x['date_time']).days>MAX_DAYS:
            break
        
        summ_purchases += x['summ']

    level = get_level(purchases)

    info = {'max_summ_percent':SETTING_MAX_SUMM_PERCENT, 'summ':summ, 'summ_availible':summ_availible, 'summ_purchases':summ_purchases, 'level':level, 'max_days':MAX_DAYS, 'min_days':MIN_DAYS}

    d = {'purchases':purchases, 'bonus_opperations':bonus_opperations, 'info':info}

    return d  

def purchase(param):
    id_card = kwargs_get(param, 'id_card')
    id_oper = kwargs_get(param, 'id_oper')
    summ = float(kwargs_get(param, 'summ'))
    summ_dics = float(kwargs_get(param, 'summ_dics'))
    comment = kwargs_get(param, 'comment')

    type_oper = 1
    date_time = int(datetime.now().timestamp()*1000000)

    if summ<0:
        type_oper = 2

    elif summ_dics>summ*SETTING_MAX_SUMM_PERCENT/100:
        raise Exception('summ_dics is not correct')

    new_op = Purchases.create(id_card=id_card, id_oper=id_oper, summ=summ, summ_dics=summ_dics, comment=comment, type_oper=type_oper, date_time=date_time)
   
    new_op_id = new_op.id

    if new_op_id is None:
        raise Exception('new_op_id is none')
    
    bonus_info = get_bonus_info(id_card)
    
    summ_availible = bonus_info['summ_availible'] 

    if summ_dics>summ_availible:
        raise Exception('summ_dics>summ_availible')

    new_bonus_op_del_id = None
    if summ_dics>0:
        com = 'Списание бонусов '+comment
        new_bonus_op = Bonus_Operations.create(id_card=id_card, date_time=date_time, summ=-(summ_dics), comment=com, id_purchases=new_op_id)
        
        new_bonus_op_del_id = new_bonus_op.id

    elif summ_dics<0:
        com = 'Возврат бонусов '+comment
        new_bonus_op = Bonus_Operations.create(id_card=id_card, date_time=date_time, summ=-(summ_dics), comment=com, id_purchases=new_op_id)
        
        new_bonus_op_del_id = new_bonus_op.id

    purchases = get_purchases(id_card)  

    level = get_level(purchases)

    com = 'Начисление бонусов '+comment

    new_bonus_op = Bonus_Operations.create(id_card=id_card, date_time=date_time, summ=(summ-summ_dics)*level['perc']/100, comment=com, id_purchases=new_op_id)

    new_bonus_op_add_id = new_bonus_op.id

    return {'new_op_id':new_op_id, 'new_bonus_op_add_id':new_bonus_op_add_id, 'new_bonus_op_del_id':new_bonus_op_del_id}

def revert(param):
    new_bonus_op_id = kwargs_get(param, 'new_bonus_op_id')

    res = Bonus_Operations.select(Bonus_Operations.id_card, Bonus_Operations.date_time, Bonus_Operations.summ).where(Bonus_Operations.rowid==new_bonus_op_id)
    
    purchases = list(res.dicts())
    
    comment = 'Отмена начисления бонусов '+purchases[0]['id_purchases']

    new_bonus_op = Bonus_Operations.create(id_card=purchases[0]['id_card'], date_time=purchases[0]['date_time'], summ=-(purchases[0]['summ']), comment=comment, id_purchases=purchases[0]['id_purchases'])

    return {'new_bonus_op_id':new_bonus_op.id}

def accrue_bonuses(param):
    id_card = kwargs_get(param, 'id_card')
    comment = kwargs_get(param, 'comment')
    summ = float(kwargs_get(param, 'summ'))   
    
    date_time = int(datetime.now().timestamp()*1000000)
    
    new_bonus_op = Bonus_Operations.create(id_card=id_card, date_time=date_time, summ=summ, comment=comment)

    return {'new_bonus_op_id':new_bonus_op.id}

def get_bonus_info(id_card):
    res = Bonus_Operations.select(Bonus_Operations.id_card, Bonus_Operations.date_time, Bonus_Operations.summ, Bonus_Operations.comment, Bonus_Operations.id_purchases).where(Bonus_Operations.id_card==id_card).order_by(Bonus_Operations.date_time.desc())
    
    bonus_opperations = list(res.dicts()) 
    
    summ = 0
    summ_availible = 0 
    for x in bonus_opperations:
        x['date_time'] = datetime.fromtimestamp(x['date_time']/1000000) 
        if (datetime.now()-x['date_time']).days<MAX_DAYS:
            summ += x['summ']
            if (datetime.now()-x['date_time']).days<MIN_DAYS:
                continue
            summ_availible += x['summ']

    return {'summ':summ, 'summ_availible':summ_availible, 'bonus_opperations':bonus_opperations}

def get_purchases(id_card, days=MAX_DAYS):
    d_t = datetime.now() + timedelta(days=-days)
    d_t_int = int(d_t.timestamp()*1000000)

    res = Purchases.select(Purchases.id_card, Purchases.id_oper, Purchases.date_time, Purchases.summ, Purchases.summ_dics, Purchases.type_oper, Purchases.comment).where((Purchases.id_card==id_card) & (Purchases.date_time>=d_t_int) ).order_by(Purchases.date_time.desc())
    
    purchases = list(res.dicts())   
    for x in purchases:
        x['date_time'] = datetime.fromtimestamp(x['date_time']/1000000) 

    return purchases

def get_level(purchases):
    if len(purchases)==0:
        return LEVELS[DELAULT_LEVEL]
    
    summ_lasts_purchase = 0

    for x in purchases: 
        if (datetime.now()-x['date_time']).days>MAX_DAYS:
            break
        
        summ_lasts_purchase += x['summ']

    for x in LEVELS:
        if LEVELS[x]['min_summ']<=summ_lasts_purchase and summ_lasts_purchase<=LEVELS[x]['max_summ']:
            return LEVELS[x]
    else:
        return LEVELS[DELAULT_LEVEL]

def kwargs_get(qs, key, default=None):
    res = qs.get(key, (default))
    if default is None and res is default:
        raise KeyError(key)
    return res

