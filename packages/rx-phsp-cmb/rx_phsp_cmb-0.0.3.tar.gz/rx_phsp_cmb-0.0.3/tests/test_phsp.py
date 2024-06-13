from phsp_cmb.phsp import phsp

import os
import glob
import ROOT

#-----------------------------------
def get_rdf(kind, trig):
    asl_dir = os.environ['ASLDIR']
    root_wc = f'{asl_dir}/phsp_cmb/{kind}/v10.21p2/*_{trig}/*.root'
    l_root  = glob.glob(root_wc)
    rdf     = ROOT.RDataFrame(trig, l_root)

    return rdf
#-----------------------------------
def test_simple():
    rdf          = get_rdf('cmb', 'ETOS')
    obj          = phsp(rdf)
    obj.plot_dir = 'tests/test_phsp/simple'
    p1, p2       = obj.get_bounds()
    slope, error = obj.get_slope()
#-----------------------------------
def main():
    test_simple()
#-----------------------------------
if __name__ == '__main__':
    main()

