from tmva_log_reader import reader

#------------------------------------
def test_simple():
    rdr = reader('tests/tmva_log_reader/output.log')
    dfi = rdr.get_table(kind='importance')
    dfs = rdr.get_table(kind='separation')

    print(dfi)
    print(dfs)
#------------------------------------
def main():
    test_simple()
#------------------------------------
if __name__ == '__main__':
    main()

