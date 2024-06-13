from rk.dbase_paths import dbase_paths as dbpath

#---------------------------------
def test_bdt():
    db  = dbpath()
    cmb = db('bdt_cmb')
    prc = db('bdt_prc')
#---------------------------------
def main():
    test_bdt()
#---------------------------------
if __name__ == '__main__':
    main()

