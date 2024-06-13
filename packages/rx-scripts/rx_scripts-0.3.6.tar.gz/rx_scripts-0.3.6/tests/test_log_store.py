from log_store import log_store

import logzero 

#--------------------------------
def test_show():
    log_store.set_level('sho_1', logzero.WARNING)
    
    log_1 = log_store.add_logger('sho_1')
    log_2 = log_store.add_logger('sho_2')
    
    log_store.show_loggers()
#--------------------------------
def test_level():
    log_store.log_level = logzero.DEBUG
    
    log_1 = log_store.add_logger('lvl_1')
    log_2 = log_store.add_logger('lvl_2')

    log_store.log_level = logzero.INFO
    
    log_3 = log_store.add_logger('lvl_3')
    log_4 = log_store.add_logger('lvl_4')

    log_store.show_loggers()
#--------------------------------
def main():
    test_level()
    test_show()
#--------------------------------
if __name__ == '__main__':
    main()

