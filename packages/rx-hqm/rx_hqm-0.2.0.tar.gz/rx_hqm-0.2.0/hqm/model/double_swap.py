import os
import zfit
import glob
import ROOT
import pprint
import read_selection    as rs
import utils_noroot      as utnr
import matplotlib.pyplot as plt

from misid_check         import misid_check
from zutils.plot         import plot   as zfp
from fitter              import zfitter
from importlib.resources import files
from log_store           import log_store

log=log_store.add_logger('rk_extractor:double_swap')
#---------------------------------
class dswp_bmass:
    def __init__(self, obs_bb, obs_mm, proc=None, name=None):
        self._obs_bb  = obs_bb
        self._obs_mm  = obs_mm
        self._proc    = proc
        self._name    = name

        self._out_dir  = None
        self._d_par_bb = None
        self._d_par_mm = None
        self._res      = None
        self._scl      = None

        self._init_fail  =False
        self._initialized=False
    #---------------------------------
    def _initialize(self):
        if self._initialized:
            return

        self._check_not_none('obs_bb', self._obs_bb)
        self._check_not_none('obs_mm', self._obs_mm)
        self._check_not_none('name'  , self._name)
        self._check_not_none('proc'  , self._proc)

        if self._init_fail:
            raise

        self._d_par_mm = self._load_pars('mass_mm')
        self._d_par_bb = self._load_pars('mass_bb')

        if (self._d_par_mm is not None) and (self._d_par_mm is not None):
            log.info(f'Parameters found not recalculating them')
            return

        rdf = self._get_rdf()
        rdf = self._filter_rdf(rdf)
        rdf = self._add_vars(rdf)

        self._cache_pars(rdf, 'mass_mm')
        self._cache_pars(rdf, 'mass_bb')

        self._d_par_bb = self._load_pars('mass_bb')
        self._d_par_mm = self._load_pars('mass_mm')

        self._initialized = True
    #---------------------------------
    def _check_not_none(self, name, val):
        if val is None:
            log.error(f'Argument {name} is None')
            self._init_fail=True
    #---------------------------------
    def _load_pars(self, variable):
        pars_path = files('hqm_data').joinpath(f'double_swap/{self._proc}_{variable}.json')
        if not os.path.isfile(pars_path):
            return

        log.debug(f'Fitting parameters found, loading: {pars_path}')
        d_par_val = utnr.load_json(pars_path)
        d_par     = self._pars_from_vals(d_par_val, variable)
        d_par     = { name : self._fix_par(par) for name, par in d_par.items() } 

        return d_par 
    #---------------------------------
    def _fix_par(self, par):
        if not isinstance(par, zfit.param.Parameter):
            return par

        if '_mu_'    in par.name:
            return par

        if '_sigma_' in par.name:
            return par

        if self._proc == 'cmb':
            return par

        par.floating = False

        return par
    #---------------------------------
    def _cache_pars(self, rdf, variable):
        arr_mass = rdf.AsNumpy([variable])[variable]
        pdf      = self._get_pdf(variable)

        obj      = zfitter(pdf, arr_mass)
        #obj.out_dir = self._out_dir 
        res      = obj.fit(ntries=10, pval_threshold=0.05)
        print(res)

        pars_path = files('hqm_data').joinpath(f'double_swap/{self._proc}_{variable}.json')
        d_par     = self._pars_from_res(res)
        utnr.dump_json(d_par, pars_path)

        self._plot_fit(pdf, arr_mass, variable)
    #---------------------------------
    def _pars_from_vals(self, d_par_val, variable):
        d_par = dict()
        for par_name, [val, minv, maxv] in d_par_val.items():
            if  variable == 'mass_bb' and par_name in ['mu_mc', 'sigma_mc']:
                d_par = self._add_peak_pars(d_par, par_name, val, minv, maxv, variable)
            else:
                d_par[par_name] = zfit.param.Parameter(f'{self._name}_{par_name}_{variable}', val, minv, maxv)

        return d_par
    #---------------------------------
    def _pars_from_res(self, res):
        d_par = dict()
        for par in res.params:
            val = float(par.value().numpy())
            low = float(par.lower)
            hig = float(par.upper)

            d_par[par.name] = [val, low, hig]

        return d_par
    #---------------------------------
    def _add_peak_pars(self, d_par, par_name, val, minv, maxv, variable):
        par_name = par_name.replace('_mc', '')
        if self._scl is None and self._res is None:
            d_par[par_name] = zfit.param.Parameter(f'{self._name}_{par_name}_{variable}', val, minv, maxv)

            return d_par

        if   par_name == 'mu':
            mu_mc = zfit.param.Parameter(f'{self._name}_mu_mc_{variable}', val, minv, maxv)
            mu_mc.floating = False
            par   = zfit.ComposedParameter('mu'   , func=lambda d_par : d_par['p1'] + d_par['p2'], params={'p1' : mu_mc, 'p2' : self._scl} )
        elif par_name == 'sigma':
            sg_mc = zfit.param.Parameter(f'{self._name}_sigma_mc_{variable}', val, minv, maxv)
            sg_mc.floating = False
            par   = zfit.ComposedParameter('sigma', func=lambda d_par : d_par['p1'] * d_par['p2'], params={'p1' : sg_mc, 'p2' : self._res} )
        else:
            log.error(f'Wrong parameter name: {par_name}')
            raise

        d_par[par_name] = par 

        return d_par 
    #---------------------------------
    def _get_rdf(self):
        cas_dir = os.environ['CASDIR']
        root_wc = f'{cas_dir}/tools/apply_selection/double_swap/{self._proc}/v10.21p2/*_MTOS/*.root'
        l_file  = glob.glob(root_wc)
        if len(l_file) == 0:
            log.error(f'No file found in: {root_wc}')
            raise

        log.info(f'Using {len(l_file)} files')
        rdf = ROOT.RDataFrame('MTOS', l_file)

        return rdf
    #---------------------------------
    def _filter_rdf(self, rdf):
        #Both double swapped and non-double swapped will contribute to fit in data
        truth_swap = 'TMath::Abs(H_TRUEID)==13 && (TMath::Abs(L1_TRUEID) == 321 ||  TMath::Abs(L2_TRUEID) == 321)'
        truth_sign = 'TMath::Abs(H_TRUEID)==321 && TMath::Abs(L1_TRUEID) == 13 && TMath::Abs(L2_TRUEID) == 13 && TMath::Abs(B_TRUEID)==521'
        truth      = f'({truth_swap}) == 1 || ({truth_sign}) == 1'

        if   self._proc == 'sign':
            pid_cut    = rs.get('pid', 'MTOS', 'central', '2016')
        elif self._proc in ['ctrl', 'cmb']:
            #Will drop isMuon, because otherwise no entries pass, 
            #assume mass shape does not depend on isMuon
            pid_cut    = 'H_ProbNNk > 0.200 && L1_PIDmu> -3. && L2_PIDmu > -3'
            log.warning(f'Dropping isMuon requirements: {pid_cut}')
        else:
            log.error(f'Invalid process: {self._proc}')
            raise

        if self._proc != 'cmb':
            rdf = rdf.Filter(truth, 'truth')

        rdf = rdf.Filter(pid_cut,   'PID')
        #Fit seems to break sometimes
        #60 K does not break it
        #this is enough statistics
        rdf = rdf.Range(60000)

        rep = rdf.Report()
        rep.Print()

        return rdf
    #---------------------------------
    def _good_column(self, col):
        if 'L1_P' in col:
            return True

        if 'L2_P' in col:
            return True

        if 'H_P'  in col:
            return True

        if col in ['B_M', 'mass']:
            return True
    #---------------------------------
    def _get_columns(self, rdf):
        v_col = rdf.GetColumnNames()
        l_col = [ col.c_str() for col in v_col ]

        icols = len(l_col)
        l_col = [ col         for col in l_col if self._good_column(col)]
        fcols = len(l_col)

        log.info(f'Dropping columns: {icols} -> {fcols}')

        return l_col
    #---------------------------------
    def _add_vars(self, rdf):
        df  = misid_check.rdf_to_df(rdf, '(L1|L2|H)_(P\w|ID)$')
        obj = misid_check(df, d_lep={'L1' : 13, 'L2' : 13}, d_had={'H' : 13})
        df  = obj.get_df(nan_val = -1, multiple_candidates=False)

        l_col             = self._get_columns(rdf)
        d_data            = rdf.AsNumpy(l_col)
        d_data['mass_mm'] = df.H_swp.to_numpy().astype(float)

        rdf = ROOT.RDF.FromNumpy(d_data)
        rdf = rdf.Define('mass_bb', 'B_M')

        return rdf
    #---------------------------------
    def _get_peak_pars(self):
        mu_mc = zfit.Parameter('mu_mc'    , 5200, 5000, 5600)
        sg_mc = zfit.Parameter('sigma_mc' ,   10,  0.1,  500)

        if self._scl is None and self._res is None:
            return mu_mc, sg_mc

        mu = zfit.ComposedParameter('mu', func=lambda d_par : d_par['p1'] + d_par['p2'], params={'p1' : mu_mc, 'p2' : self._scl} )
        sg = zfit.ComposedParameter('sg', func=lambda d_par : d_par['p1'] * d_par['p2'], params={'p1' : sg_mc, 'p2' : self._res} )

        return mu, sg
    #---------------------------------
    def _get_double_cb(self, variable):
        if   variable == 'mass_bb':
            mu, sg = self._get_peak_pars()
            obs    = self._obs_bb
        elif variable == 'mass_mm':
            mu = zfit.Parameter('mu'    , 3000, 2900, 3100)
            sg = zfit.Parameter('sigma' ,   10,  0.1,  500)
            obs= self._obs_mm
        else:
            log.error(f'Invalid variable: {variable}')
            raise

        al = zfit.Parameter('alphal', 1, 0,  20)
        nl = zfit.Parameter('nl'    , 1, 0, 150)

        ar = zfit.Parameter('alphar', 1, 0,  20)
        nr = zfit.Parameter('nr'    , 1, 0, 120)

        dscb = zfit.pdf.DoubleCB(
            mu    = mu,
            sigma = sg,
            alphal= al,
            nl    = nl,
            alphar= ar,
            nr    = nr,
            obs   = obs,
        )

        return dscb
    #---------------------------------
    def _get_exponential(self, variable):
        if   variable == 'mass_bb':
            obs= self._obs_bb
        elif variable == 'mass_mm':
            obs= self._obs_mm
        else:
            log.error(f'Invalid variable: {variable}')
            raise

        lam  = zfit.param.Parameter('lam' ,   -1/1000.,  -10/1000.,  0)
        expo = zfit.pdf.Exponential(
            lam   = lam,
            obs   = obs,
        )

        return expo 
    #---------------------------------
    def _get_polynomial(self, variable):
        if   variable == 'mass_bb':
            obs= self._obs_bb
        elif variable == 'mass_mm':
            obs= self._obs_mm
        else:
            log.error(f'Invalid variable: {variable}')
            raise

        c0 = zfit.param.Parameter('c0' , 0, -5, +1)
        c1 = zfit.param.Parameter('c1' , 0, -1, +1)
        c2 = zfit.param.Parameter('c2' , 0, -1, +1)

        pdf = zfit.pdf.Chebyshev(
            coeffs = [c0, c1, c2],
            obs    = obs,
        )

        return pdf 
    #---------------------------------
    def _get_pdf(self, variable):
        if   self._proc == 'ctrl':
            pdf = self._get_double_cb(variable)
        elif self._proc == 'cmb':
            pdf = self._get_exponential(variable)
        elif self._proc == 'sign' and variable == 'mass_mm':
            pdf = self._get_polynomial(variable)
        elif self._proc == 'sign' and variable == 'mass_bb':
            pdf = self._get_double_cb(variable)
        else:
            log.error(f'Invalid process/variable: {self._proc}/{variable}')
            raise

        return pdf
    #---------------------------------
    @property
    def out_dir(self):
        return self._out_dir

    @out_dir.setter
    def out_dir(self, value):
        try:
            os.makedirs(value, exist_ok=True)
        except:
            log.error(f'Cannot make directory: {value}')
            raise

        self._out_dir = value
    #---------------------------------
    @property
    def mass_scale(self):
        return self._scl

    @mass_scale.setter
    def mass_scale(self, value):
        self._scl = value
    #---------------------------------
    @property
    def mass_resolution(self):
        return self._res

    @mass_resolution.setter
    def mass_resolution(self, value):
        self._res = value
    #---------------------------------
    def _plot_fit(self, pdf, arr_mass, variable):
        obj  = zfp(data=arr_mass, model=pdf)
        obj.plot(nbins=50, ext_text='')

        obj.axs[1].set_ylim(-5, 5)
        obj.axs[1].plot(linestyle='--', color='black')

        if   variable == 'mass_bb':
            obj.axs[0].axvline(x=5280, color='r', linestyle=':', label='$B^+$')
        elif variable == 'mass_mm':
            obj.axs[0].axvline(x=3097, color='r', linestyle=':', label='$J/\psi$')
        else:
            log.error(f'Invalid variable: {variable}')
            raise
                            
        plt_dir = f'{self._out_dir}/fit_plots'
        os.makedirs(plt_dir, exist_ok=True)
        obj.axs[0].legend()
        plt.savefig(f'{plt_dir}/fit_{variable}.png', bbox_inches='tight')
    #---------------------------------
    def _extend_pdf(self, pdf_bb, pdf_mm, ncnd):
        name = pdf_bb.name
        if ncnd is None:
            ncnd   = zfit.Parameter(f'ncnd_{name}', 100, 0.0, 200000)

        pdf_bb.set_yield(ncnd)
        pdf_mm.set_yield(ncnd)

        return pdf_bb, pdf_mm
    #---------------------------------
    def get_pdf(self, extended=False, ncnd=None):
        '''
        Parameters:
        ---------------
        extended (bool)       : Will extend PDF if True, by default False.
        ncnd (zfit.parameter) : If extended=True, ncnd will be used to extend the PDF, if given

        Returns
        ---------------
        tuple : Tuple of PDFs with PDF for the B mass first and then the one for the dimuon mass, after swapping mass hypotheses.
        '''
        self._initialize()

        if   self._proc == 'ctrl':
            pdf_bb = zfit.pdf.DoubleCB(obs=self._obs_bb, name=self._name, **self._d_par_bb)
            pdf_mm = zfit.pdf.DoubleCB(obs=self._obs_mm, name=self._name, **self._d_par_mm)
        elif self._proc == 'cmb':
            pdf_bb = zfit.pdf.Exponential(obs=self._obs_bb, name=self._name, **self._d_par_bb)
            pdf_mm = zfit.pdf.Exponential(obs=self._obs_mm, name=self._name, **self._d_par_mm)
        elif self._proc == 'sign':
            pdf_bb = zfit.pdf.DoubleCB(obs=self._obs_bb, name=self._name, **self._d_par_bb)

            l_coef = [ par for par in self._d_par_mm.values() ]
            pdf_mm = zfit.pdf.Chebyshev(obs=self._obs_mm, name=self._name, coeffs=l_coef)
        else:
            log.error(f'Invalid process: {self._proc}')
            raise

        if extended:
            pdf_bb, pdf_mm = self._extend_pdf(pdf_bb, pdf_mm, ncnd)

        return pdf_bb, pdf_mm
#---------------------------------

