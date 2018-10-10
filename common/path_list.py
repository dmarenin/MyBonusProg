from common import api_func

def get():

    reg_path_list = []

    reg_path_list.append({'method':'GET', 'func':'/info', 'handler':api_func.info})
    
    reg_path_list.append({'method':'GET', 'func':'/purchase', 'handler':api_func.purchase})
    
    reg_path_list.append({'method':'GET', 'func':'/revert', 'handler':api_func.revert})
    
    reg_path_list.append({'method':'GET', 'func':'/accrue_bonuses', 'handler':api_func.accrue_bonuses})
    
    return reg_path_list

