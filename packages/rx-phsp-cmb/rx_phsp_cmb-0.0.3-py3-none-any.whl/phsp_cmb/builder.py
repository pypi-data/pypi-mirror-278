import os
import numpy
import zfit
import matplotlib.pyplot as plt

from log_store   import log_store 
from zutils.plot import plot   as zfp

log=log_store.add_logger('phsp_cmb:builder')
#-------------------------------
class builder:
    def __init__(self, obs=None, p1=None, p2=None):
        self._obs = obs
        self._p1  = p1
        self._p2  = p2

        self._nsam_warp = 100000
        self._nbins     = 20
        self._out_dir   = None
        self._l_slope   = None

        self._initialized = False
    #-------------------------------
    def _initialize(self):
        if self._initialized:
            return

        try:
            [val, err] = self._l_slope
        except:
            log.error(f'Cannot extract slope parameters from: {self._l_slope}')
            raise

        self._initialized = True 
    #-------------------------------
    @property
    def out_dir(self):
        return self._out_dir

    @out_dir.setter
    def out_dir(self, value):
        try:
            os.makedirs(value, exist_ok=True)
        except:
            log.error(f'Cannot make: {value}')
            raise

        self._out_dir = value
    #-------------------------------
    @property
    def slope(self):
        return self._l_slope

    @slope.setter
    def slope(self, value):
        self._l_slope = value
    #-------------------------------
    def _plot_warp_data(self, arr_data, name=None):
        if self._out_dir is None:
            return

        [arr_x, arr_y] = arr_data.T

        _, y1 = self._p1
        _, y2 = self._p2
        [[x1]], [[x2]] = self._obs.limits

        x_rng  = [x1, x2]
        y_rng  = [y1, y2]

        c, x, y = numpy.histogram2d(arr_x, arr_y, range=[x_rng, y_rng], bins=self._nbins)

        cb=plt.pcolor(x, y, c.T)
        plt.colorbar(cb)

        log.info(f'Saving to: {self._out_dir}/warp_data_{name}.png')
        plt.xlabel('B mass [MeV]')
        plt.ylabel('$q^2$ [GeV${}^2$]')
        plt.savefig(f'{self._out_dir}/warp_data_{name}.png')
        plt.close('all')
    #-------------------------------
    def _remove_phsp(self, arr_data):
        x1, y1   = self._p1
        x2, y2   = self._p2

        m = (y2 - y1) / (x2  - x1)
        b = y1 - m * x1

        l_point = [ [x, y] for [x, y] in arr_data if  y < m * x + b] 

        return numpy.array(l_point)
    #-------------------------------
    def _plot_kde(self, pdf, arr_dat, name=None):
        if self._out_dir is None:
            return

        obj = zfp(data=arr_dat, model=pdf)
        obj.plot(nbins=50)
        obj.axs[1].set_xlabel('Mass (B)[MeV]')

        log.info(f'Saving to: {self._out_dir}/kde_{name}.png')
        plt.savefig(f'{self._out_dir}/kde_{name}.png')
        plt.close('all')
    #-------------------------------
    def _get_warping_data(self, suffix):
        log.debug(f'Getting warped data')
        x1, y1   = self._p1
        x2, y2   = self._p2

        log.debug(f'Getting warped data')
        qsq_obs  = zfit.Space('$q^2$[GeV${}^2$]', limits=(y1, y2))
        lam      = zfit.param.Parameter(f'lam_q2_{suffix}', self._l_slope[0], -1, 0)
        pdf_q2   = zfit.pdf.Exponential(lam=lam, obs=qsq_obs)

        [[low]], [[hig]] = self._obs.limits
        pdf_ms   = zfit.pdf.Uniform(low, hig, obs=self._obs)

        log.debug(f'Getting BDT-Q2 distribution with {self._nsam_warp} entries')
        pdf      = zfit.pdf.ProductPDF([pdf_ms, pdf_q2]) 
        sam      = pdf.create_sampler(n=self._nsam_warp)
        arr_data = sam.numpy()

        log.debug(f'Plotting 2D unwarped data')
        self._plot_warp_data(arr_data, name='all')
        arr_data = self._remove_phsp(arr_data)

        log.debug(f'Plotting 2D warped data')
        self._plot_warp_data(arr_data, name='warped')

        return arr_data.T[0]
    #-------------------------------
    def _get_warping_pdf(self, suffix):
        arr_mas = self._get_warping_data(suffix)

        log.debug(f'Building KDE from warped mass')
        pdf_wrp = zfit.pdf.KDE1DimFFT(arr_mas, obs=self._obs, bandwidth=80, name='Warping function', padding={'uppermirror' : 1})

        self._plot_kde(pdf_wrp, arr_mas, name='warp')

        return pdf_wrp
    #-------------------------------
    def _get_expo(self, suffix):
        lb  = zfit.param.Parameter(f'lb_{suffix}', -0.001, -0.01, 0)
        pdf = zfit.pdf.Exponential(lam=lb, obs=self._obs)

        return pdf
    #-------------------------------
    def get_pdf(self, suffix=None):
        self._initialize()

        pdf_wp = self._get_warping_pdf(suffix)
        pdf_ex = self._get_expo(suffix) 

        pdf = zfit.pdf.ProductPDF([pdf_wp, pdf_ex], obs=self._obs, name='PHSP PDF')

        return pdf
#-------------------------------

