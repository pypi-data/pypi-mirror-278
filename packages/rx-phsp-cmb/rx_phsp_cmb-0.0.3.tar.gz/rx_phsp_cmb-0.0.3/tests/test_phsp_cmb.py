from phsp_cmb.phsp_cmb import cmb_fun
from phsp_cmb.phsp_cmb import cmb_pdf

from zutils.plot       import plot   as zfp
from fitter            import zfitter

import os
import math
import zfit
import numpy
import tensorflow        as tf
import matplotlib.pyplot as plt

from log_store import log_store

log=log_store.add_logger('rx_phsp_cmb')
#------------------------------------
class data:
    qmin = math.sqrt(15.5)
#------------------------------------
def delete_pars():
    d_par = zfit.Parameter._existing_params
    l_key = list(d_par.keys())

    for key in l_key:
        del(d_par[key])
#------------------------------------
def test_fun():
    lm = tf.constant(   2., dtype=tf.float64)
    ms = tf.constant(5500., dtype=tf.float64)

    obj=cmb_fun(lm=lm, qmin=data.qmin)
    val=obj(ms)
    print(val)
#------------------------------------
def test_simple():
    obs=zfit.Space('x', limits=[4500, 6000])
    lam=zfit.param.Parameter('lam', 2, 0.1, 3)
    qmi=zfit.param.ConstantParameter('qmi', data.qmin)

    log.info('Making PDF')
    pdf=cmb_pdf(lam, qmi, obs)

    log.info('Making data')
    sam=pdf.create_sampler(n=100000)

    log.info('Fitting')
    obj=zfitter(pdf, sam)
    res=obj.fit()

    log.info('Getting errors')
    res.hesse(method='minuit_hesse')

    log.info('Plotting')
    obj = zfp(data=sam, model=pdf, result=res)
    obj.plot(nbins=50) 

    plt.show()
#------------------------------------
def plot_pdf(pdf, qsq):
    arr_mas = numpy.linspace(4300, 7000, 200)
    arr_val = pdf.pdf(arr_mas)

    plt.plot(arr_mas, arr_val, label=str(qsq))
#------------------------------------
def test_overlay():
    for qsq in [10, 12, 14.3, 16, 19, 21]:
        data.qmin = math.sqrt(qsq)
        obs=zfit.Space('x', limits=[4300, 7000])
        lam=zfit.param.Parameter('lam', 2, 1, 3)
        qmi=zfit.param.ConstantParameter('qmi', data.qmin)

        pdf=cmb_pdf(lam, qmi, obs)
        plot_pdf(pdf, qsq)

        delete_pars()

    plt.xlabel('B mass[MeV]')
    plt.ylabel('Normalized')
    plt.legend()
    plt.grid()
    out_dir = 'tests/test_phsp_cmb/overlay'
    os.makedirs(out_dir, exist_ok=True)
    plt.savefig(f'{out_dir}/overlay_crosscheck.png')
    plt.close('all')
#------------------------------------
def main():
    test_simple()
    test_overlay()
#------------------------------------
if __name__ == '__main__':
    main()

