import pdg_utils as pu

#-------------------------------------------
def test_bf():
    bpjpkp = 'B+ --> J/psi(1S) K+'
    bdjpks = 'B0 --> J/psi(1S) K0'
    bsjpph = 'B_s()0 --> J/psi(1S) phi'

    pu.get_bf(bpjpkp)
    pu.get_bf(bdjpks)
    pu.get_bf(bsjpph)
#-------------------------------------------
def main():
    test_bf()
#-------------------------------------------
if __name__ == '__main__':
    main()

