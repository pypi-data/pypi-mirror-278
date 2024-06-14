import ROOT
import utils_noroot as utnr


from atr_mgr import mgr as amgr
from atr_mgr import ldr as aldr

#--------------------------------
def test_simple():
    df = ROOT.RDataFrame(20)

    df.name    = 'dataframe_simple'
    df.entries = 20
    df.l_data  = [1, 2, 3]

    obj = amgr(df)
#--------------------------------
def test_dump():
    df = ROOT.RDataFrame(20)

    df.name    = 'dataframe_simple'
    df.entries = 20
    df.l_data  = [1, 2, 3]

    obj = amgr(df)
    obj.to_json('tests/atr_mgr/dump/data.json')
#--------------------------------
def test_load():
    json_path = 'tests/atr_mgr/load/data.json'
    d_dat     = {'x' : 1, 'y' : [1, 2, 3], 'z' : 'something here'}
    utnr.dump_json(d_dat, json_path)

    rdf = ROOT.RDataFrame(20)

    obj = aldr(rdf)
    rdf = obj.from_json('tests/atr_mgr/load/data.json')
#--------------------------------
def main():
    test_load()
    return
    test_dump()
    test_simple()
#--------------------------------
if __name__ == '__main__':
    main()

