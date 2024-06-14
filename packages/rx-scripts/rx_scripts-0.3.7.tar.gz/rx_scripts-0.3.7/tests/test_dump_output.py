import pprint

from dump_output import dump_output as dout 

from log_store   import log_store

log=log_store.add_logger('rx_scripts:dump_output')
#------------------------------------------------
def test_simple():
    obj = dout()

    text_in = ''
    for i_iter in range(10):
        line = f'Iteration {i_iter}'
        print(line)
        text_in += f'{line}\n'

    text_ot = obj.retrieve()
    text_ot = obj.retrieve()

    try:
        log.info(f'simple: passed')
        assert text_in == text_ot 
    except:
        log.info(f'simple: failed')
        log.error(text_in)
        log.error(text_ot)
        raise
#------------------------------------------------
def main():
    test_simple()
#------------------------------------------------
if __name__ == '__main__':
    main()

