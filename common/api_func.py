from common.models import *
from datetime import datetime, date, timedelta
#from common.conf import *

def info(param):
    id_card = kwargs_get(param, 'id_card')

    purchases = get_purchases(id_card)  

    res = BonusOperations.select(BonusOperations.id_card, BonusOperations.date_time, BonusOperations.summ, BonusOperations.comment).where(BonusOperations.id_card==id_card).order_by(BonusOperations.date_time.desc())
    
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

    summ_purchases = 0
    for x in purchases:
        #if (datetime.now()-x['date_time']).days<MIN_DAYS:
        #    continue

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

    if summ_dics>summ*SETTING_MAX_SUMM_PERCENT/100:
        raise Exception('summ_dics is not correct')

    new_op = Purchases.create(id_card=id_card, id_oper=id_oper, summ=summ, summ_dics=summ_dics, comment=comment, type_oper=type_oper, date_time=date_time)
   
    new_op_id = new_op.id

    if new_op_id is None:
        raise Exception('new_op_id is none')
    
    if summ_dics>0:
        comment = 'Списание бонусов'
        new_bonus_op = BonusOperations.create(id_card=id_card, date_time=date_time, summ=-(summ_dics), comment=comment)
        
        new_bonus_op_del_id = new_bonus_op.id

    purchases = get_purchases(id_card)  

    level = get_level(purchases)

    comment = 'Начисление бонусов'

    new_bonus_op = BonusOperations.create(id_card=id_card, date_time=date_time, summ=(summ-summ_dics)*level['perc']/100, comment=comment)

    new_bonus_op_add_id = new_bonus_op.id

    return {'new_op_id':new_op_id, 'new_bonus_op_add_id':new_bonus_op_add_id, 'new_bonus_op_del_id':new_bonus_op_del_id}

def revert(param):
    new_bonus_op_id = kwargs_get(param, 'new_bonus_op_id')

    res = BonusOperations.select(BonusOperations.id_card, BonusOperations.date_time, BonusOperations.summ).where(BonusOperations.rowid==new_bonus_op_id)
    
    purchases = list(res.dicts())
    
    comment = 'Отмена начисления бонусов'

    new_bonus_op = BonusOperations.create(id_card=purchases[0]['id_card'], date_time=purchases[0]['date_time'], summ=-(purchases[0]['summ']), comment=comment)

    return {'new_bonus_op_id':new_bonus_op.id}

def accrue_bonuses(param):
    id_card = kwargs_get(param, 'id_card')
    comment = kwargs_get(param, 'comment')
    summ = float(kwargs_get(param, 'summ'))   
    
    date_time = int(datetime.now().timestamp()*1000000)
    
    new_bonus_op = BonusOperations.create(id_card=id_card, date_time=date_time, summ=summ, comment=comment)

    return {'new_bonus_op_id':new_bonus_op.id}


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
        #if (datetime.now()-x['date_time']).days<MIN_DAYS:
        #    continue

        if (datetime.now()-x['date_time']).days>MAX_DAYS:
            break
        
        summ_lasts_purchase += x['summ']

    for x in LEVELS:
        if LEVELS[x]['min_summ']<=summ_lasts_purchase and summ_lasts_purchase<=LEVELS[x]['max_summ']:
            return LEVELS[x]
    else:
        return LEVELS[DELAULT_LEVEL]

def kwargs_get(qs, key, default = None):
    res, *junk = qs.get(key, (default,))
    if default is None and res is default:
        raise KeyError(key)
    return res

