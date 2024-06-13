import os
import zfit
import math
import numpy
import pprint
import matplotlib.pyplot as plt

from zutils.plot    import plot     as zfp
from fitter         import zfitter
from log_store      import log_store

log=log_store.add_logger('phsp_cmb:phsp')
#-------------------------------------
class phsp:
    '''
    This class is meant to find the phase space boundaries and the q2 distribution from a suitable combinatorial proxy.
    '''
    #-------------------------------------
    def __init__(self, rdf):
        self._rdf      = rdf
        self._plot_dir = None
        self._bdt_cut  = 0.977000
        self._l_bdt    = [(0.0, 0.1), (0.1, 0.3), (0.3, 0.5), (0.5, 0.8), (0.8, 1.2)]
        self._obs      = zfit.Space('$q^2$[GeV${}^2$]', limits=(16, 22))
        self._lam      = zfit.Parameter('lam', -0.01, -1, 0)
        self._pdf_exp  = zfit.pdf.Exponential(self._lam, self._obs)
        self._nbins    = 20


        self._initialized = False
    #-------------------------------------
    def _initialize(self):
        if self._initialized:
            return

        self._check_rdf()

        self._rdf = self._rdf.Define('qsq', 'Jpsi_M * Jpsi_M * 0.000001')

        d_data        = self._rdf.AsNumpy(['BDT_cmb', 'qsq', 'B_M', 'H_PE'])
        self._arr_bdt = d_data['BDT_cmb']
        self._arr_mas = d_data['B_M'    ]
        self._arr_qsq = d_data['qsq'    ]
        self._arr_ken = d_data['H_PE'   ]

        self._initialized = True 
    #-------------------------------------
    def _check_rdf(self):
        nent = self._rdf.Count().GetValue()
        if nent <= 0:
            log.error(f'No entries found in dataframe')
            raise
        else:
            log.info(f'Using {nent} entries')
    #-------------------------------------
    @property
    def plot_dir(self):
        return self._plot_dir

    @plot_dir.setter
    def plot_dir(self, value):
        try:
            os.makedirs(value, exist_ok=True)
        except:
            log.error(f'Cannot make: {value}')

        self._plot_dir = value
    #-------------------------------------
    def get_bounds(self):
        self._initialize()

        self._plot_var(self._arr_ken, 'kaon_energy', rng=[0, 5000])
        ken = 497
        ken = 600

        l_low= [4500                 , (4500 - ken) ** 2 / 1e6]
        l_hig= [math.sqrt(22e6) + ken,                      22]

        self._plot_warp_data(l_low, l_hig)

        return l_low, l_hig
    #-------------------------------
    def _plot_warp_data(self, l_low, l_hig, name=None):
        if self._plot_dir is None:
            return

        c, x, y = numpy.histogram2d(self._arr_mas, self._arr_qsq, bins=self._nbins)

        cb=plt.pcolor(x, y, c.T)
        plt.colorbar(cb)

        log.info(f'Saving to: {self._plot_dir}/bdt_qsq.png')
        plt.xlabel('Mass (B) [MeV]')
        plt.ylabel('$q^2$ [GeV${}^2$]')
        plt.savefig(f'{self._plot_dir}/mas_qsq_woln.png')
        plt.plot([l_low[0], l_hig[0] ], [l_low[1], l_hig[1]], color='r', linestyle='-')
        plt.savefig(f'{self._plot_dir}/mas_qsq_whln.png')
        plt.close('all')
    #-------------------------------------
    def _fit(self, arr_val, name):
        obj=zfitter(self._pdf_exp, arr_val)
        res=obj.fit()
        res.hesse(method='minuit_hesse')

        val=res.params['lam']['value']
        err=res.params['lam']['hesse']['error']

        obj=zfp(model=self._pdf_exp, data=arr_val, result=res)
        obj.plot()

        obj.axs[0].set_title(f'$\lambda={val:.3f}\pm{err:.3f}$')
        obj.axs[1].set_xlabel('$q^2$ [GeV${}^2$]')

        return [val, err]
    #-------------------------------------
    def _plot_var(self, arr_val, name, yscale='linear', rng=None, normalized=False, fit=None):
        slope = None
        if fit is not None:
            slope = self._fit(arr_val, name)

        if self._plot_dir is None:
            return slope

        plt.hist(arr_val, range=rng, bins=50, histtype='step', density=normalized)
        plot_path = f'{self._plot_dir}/{name}.png'
        plt.yscale(yscale)
        if 'BDT' in name:
            plt.axvline(x=self._bdt_cut, color='r')
        plt.savefig(plot_path)
        plt.close('all')

        return slope
    #-------------------------------------
    def _study_qsq(self):
        self._plot_var(self._arr_bdt, 'BDT_cmb', yscale='log', rng=[0,1])
        self._plot_var(self._arr_qsq, 'qsq'    , yscale='log', rng= None)

        arr_tot = numpy.array([self._arr_bdt, self._arr_qsq]).T
        slope   = None
        for min_bdt, max_bdt in self._l_bdt:
            arr_slc = arr_tot[arr_tot[:, 0] > min_bdt]
            arr_slc = arr_slc[arr_slc[:, 0] < max_bdt]
            arr_bdt = arr_slc.T[0]
            arr_qsq = arr_slc.T[1]

            self._plot_var(arr_bdt, f'BDT_cmb_{min_bdt}_{max_bdt}', yscale='log'   , rng=[0,1], normalized=False)
            slope=self._plot_var(arr_qsq, f'qsq_{min_bdt}_{max_bdt}'    , yscale='linear', rng=None , normalized=True, fit='expo')

        return slope
    #-------------------------------------
    def get_slope(self):
        self._initialize()
        slope, error = self._study_qsq()

        return slope, error
#-------------------------------------

