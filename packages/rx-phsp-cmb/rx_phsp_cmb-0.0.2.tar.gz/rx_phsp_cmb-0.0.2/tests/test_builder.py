import logzero
import ROOT



from phsp_cmb.phsp    import phsp 
from phsp_cmb.builder import builder
from zutils.plot      import plot       as zfp
from log_store        import log_store

log_store.set_level('phsp_cmb:builder', logzero.DEBUG)

import os
import zfit
import glob
import numpy
import zutils.utils      as zut
import matplotlib.pyplot as plt

#------------------------------
class data:
    obs = zfit.Space('B mass [MeV]', limits=(4500, 6000))
#------------------------------
def delete_pars():
    d_par = zfit.Parameter._existing_params
    l_key = list(d_par.keys())

    for key in l_key:
        del(d_par[key])
#------------------------------
def overlay_pdf(l_pdf, name=None):
    plt.close('all')
    arr_x = numpy.linspace(4500, 6000, 200)

    l_lab = ['$-\sigma$', 'Nominal', '$+\sigma$']
    for lab, pdf in zip(l_lab, l_pdf):
        arr_y = pdf.pdf(arr_x) 

        plt.plot(arr_x, arr_y, label=lab)

    plt.xlabel('Mass (B)[MeV]')
    plt.ylabel('Normalized')
    plt.grid()
    plt.legend()
#------------------------------
def plot_pdf(pdf, name=None):
    sam=pdf.create_sampler(n=10000)
    obj=zfp(data=sam, model=pdf)
    obj.plot(nbins=50)
    plt.savefig(f'tests/test_builder/{name}/pdf.png')

    zut.print_pdf(pdf, txt_path=f'tests/test_builder/{name}/pdf.txt')
#------------------------------
def get_rdf(kind, trig):
    asl_dir = os.environ['ASLDIR']
    root_wc = f'{asl_dir}/phsp_cmb/{kind}/v10.21p2/*_{trig}/*.root'
    l_root  = glob.glob(root_wc)
    rdf     = ROOT.RDataFrame(trig, l_root)
    return rdf 
#------------------------------
def test_real():
    rdf          = get_rdf('cmb', 'ETOS')
    obj          = phsp(rdf)
    obj.plot_dir = 'tests/test_builder/real'
    p1, p2       = obj.get_bounds()
    slope, error = obj.get_slope()

    obj=builder(obs=data.obs, p1=p1, p2=p2)
    obj.out_dir   = 'tests/test_builder/real'
    obj.slope     = slope, error 
    pdf=obj.get_pdf()

    plot_pdf(pdf, name='real')
    delete_pars()
#------------------------------
def test_syst():
    rdf          = get_rdf('cmb', 'ETOS')
    obj          = phsp(rdf)
    slope, error = obj.get_slope()
    p1, p2       = obj.get_bounds()

    obj_0=builder(obs=data.obs, p1=p1, p2=p2)
    obj_0.slope  = slope - error , 0 

    obj_1=builder(obs=data.obs, p1=p1, p2=p2)
    obj_1.slope  = slope, 0

    obj_2=builder(obs=data.obs, p1=p1, p2=p2)
    obj_2.slope  = slope + error , 0

    pdf_0=obj_0.get_pdf('z')
    pdf_1=obj_1.get_pdf('o')
    pdf_2=obj_2.get_pdf('t')

    overlay_pdf([pdf_0, pdf_1, pdf_2], name='real')
    dir_path = 'tests/test_builder/syst'
    os.makedirs(dir_path, exist_ok=True)
    plt.savefig(f'{dir_path}/syst.png')

    delete_pars()
#------------------------------
def test_simple():
    obj=builder(obs=data.obs, p1=(4500, 15), p2=(5250, 22))
    obj.out_dir   = 'tests/test_builder/simple'
    obj.slope     = -0.10, 0.01
    pdf=obj.get_pdf()

    plot_pdf(pdf, name='simple')

    delete_pars()
#------------------------------
def main():
    #test_simple()
    #test_real()
    #test_syst()
#------------------------------
if __name__ == '__main__':
    main()

