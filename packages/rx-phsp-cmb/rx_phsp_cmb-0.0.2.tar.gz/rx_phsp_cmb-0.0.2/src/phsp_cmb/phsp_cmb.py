
import zfit
import tensorflow             as tf
import tensorflow_probability as tfp
import numpy
from zfit            import z
from scipy.integrate import trapz

#-----------------------
class cmb_fun:
    def __init__(self, lm=None, qmin=None):
        self._qmin = qmin
        self._lm   = lm 
        self._mk   = 0.497
    #-----------------------
    def _gamma(self, x, q):
        fac = 1./ (4 * x * q)
        exp = z.exp(-self._lm * x)

        v1  = self._get_sqrt_arg(x, q, +1)
        v2  = self._get_sqrt_arg(x, q, -1)

        sq_1= z.sqrt(v1) / x 
        sq_2= z.sqrt(v2) / x 
    
        res = fac * exp * sq_1  * sq_2

        res = tf.where(tf.math.is_nan(res), tf.zeros_like(res), res)
    
        return res 
    #-----------------------
    def _get_sqrt_arg(self, x, q, fac):
        val = x**2 - (self._mk + fac * q) ** 2

        return val
    #-----------------------
    def __call__(self, x):
        x       = x / 1000.
        qmax    = x - self._mk
        arr_qsq = tf.linspace(self._qmin, qmax, 50)
        arr_gam = self._gamma(x, arr_qsq)
        integral= tfp.math.trapz(arr_gam, arr_qsq, axis=0)
        #integral= tf.where(tf.math.is_nan(integral), tf.zeros_like(integral), integral)

        return integral 
#-----------------------
class cmb_pdf(zfit.pdf.BasePDF):
    def __init__(self, lam, qmin, obs, extended=None, norm=None, name=None):
        params = {'lam': lam, 'qmin' : qmin}

        super().__init__(obs=obs, params=params, extended=extended, norm=norm, name=name)
    #-----------------------
    def _unnormalized_pdf(self, x):
        x = z.unstack_x(x)
        l = self.params['lam' ]
        q = self.params['qmin']

        obj = cmb_fun(lm=l, qmin=q)

        return obj(x) 
#-----------------------

