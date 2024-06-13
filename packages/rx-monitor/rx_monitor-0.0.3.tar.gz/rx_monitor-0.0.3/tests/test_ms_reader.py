from monitor.ms_reader import ms_reader

#----------------------------------
def test_simple():
    for scale in ['mu_g', 'sg_g', 'mu', 'sg', 'br']:
        rdr=ms_reader(version='v7')
        df =rdr.get_scales(scale)
        print(df)
#----------------------------------
if __name__ == '__main__':
    test_simple()

