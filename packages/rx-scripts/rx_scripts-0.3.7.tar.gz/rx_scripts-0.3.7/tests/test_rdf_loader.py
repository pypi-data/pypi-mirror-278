from rdf_loader import rdf_loader

#----------------------------------
def test_simple():
    d_cut = {
            'bdt_cmb' : 'BDT_cmb > 0.3',
            'bdt_prc' : 'BDT_prc > 0.8',
            }

    obj              = rdf_loader(sample='bdt_fit', proc='ctrl', asl_vers=None, ntp_vers='v10.21p2', year='2011', trig='ETOS')
    obj.selection    = d_cut
    rdf, df_cf, d_md = obj.get_rdf()
#----------------------------------
def test_dset(dset):
    d_cut = {
            'bdt_cmb' : 'BDT_cmb > 0.3',
            'bdt_prc' : 'BDT_prc > 0.8',
            }

    obj              = rdf_loader(sample='bdt_fit', proc='ctrl', asl_vers=None, ntp_vers='v10.21p2', year=dset, trig='ETOS')
    obj.selection    = d_cut
    rdf, df_cf, d_md = obj.get_rdf()
#----------------------------------
def main():
    test_dset('r1')
    test_dset('r2p1')
    test_dset('all')
    test_simple()
#----------------------------------
if __name__ == '__main__':
    main()

