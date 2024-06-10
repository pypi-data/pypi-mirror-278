"""Implements all the logic for mixed logit models."""
import itertools
import logging

import numpy as np
import scipy.stats as ss
from scipy.optimize import minimize

from ._choice_model import ChoiceModel
from ._device import device as dev
from .boxcox_functions import (boxcox_param_deriv_mixed,
                               boxcox_transformation_mixed)
from .multinomial_logit import MultinomialLogit

"""
Notations
---------
    N : Number of choice situations
    P : Number of observations per panel
    J : Number of alternatives
    K : Number of variables (Kf: fixed (non-trans), Kr: random,
                             Kftrans: fixed trans, Krtrans: random trans)
"""

# define the computation boundary values not to be exceeded
max_exp_val = 700

max_comp_val = 1e+300
min_comp_val = 1e-300

logger = logging.getLogger(__name__)


class MixedLogit(ChoiceModel):
    """Class for estimation of Mixed Logit Models

    Attributes
    ----------
        coeff_ : numpy array, shape (n_variables + n_randvars, )
            Estimated coefficients

        coeff_names : numpy array, shape (n_variables + n_randvars, )
            Names of the estimated coefficients

        stderr : numpy array, shape (n_variables + n_randvars, )
            Standard errors of the estimated coefficients

        zvalues : numpy array, shape (n_variables + n_randvars, )
            Z-values for t-distribution of the estimated coefficients

        pvalues : numpy array, shape (n_variables + n_randvars, )
            P-values of the estimated coefficients

        loglikelihood : float
            Log-likelihood at the end of the estimation

        convergence : bool
            Whether convergence was reached during estimation

        total_iter : int
            Total number of iterations executed during estimation

        estim_time_sec : float
            Estimation time in seconds

        sample_size : int
            Number of samples used for estimation

        aic : float
            Akaike information criteria of the estimated model

        bic : float
            Bayesian information criteria of the estimated model
    """

    def __init__(self):
        """Init Function"""
        super(MixedLogit, self).__init__()
        self.rvidx = None  # Boolean index of random vars in X. True = rand var
        self.rvdist = None
        self.reg_penalty  = 5 # value to change the penalty amount for lasso 
        #TODO penalty as a paramater

    # X: (N, J, K)
    def fit(self, X, y, varnames=None, alts=None, isvars=None, transvars=None,
            transformation="boxcox", ids=None, weights=None, avail=None,
            randvars=None, panels=None, base_alt=None, fit_intercept=False,
            init_coeff=None, maxiter=2000, random_state=None, correlation=None,
            n_draws=1000, halton=True, minimise_func=None, verbose=1,
            batch_size=None, halton_opts=None, ftol=1e-7, 
            gtol=1e-5, return_hess=True, return_grad=True, method="bfgs",
            save_fitted_params=True, mnl_init=True, reg_penalty = 5):
        """Fit Mixed Logit models.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_variables)
            Input data for explanatory variables in long format

        y : array-like, shape (n_samples,)
            Choices (outcome) in long format

        varnames : list, shape (n_variables,)
            Names of explanatory variables that must match the number and
            order of columns in ``X``

        alts : array-like, shape (n_samples,)
            Alternative indexes in long format or list of alternative names

        isvars : list
            Names of individual-specific variables in ``varnames``

        transvars: list, default=None
            Names of variables to apply transformation on

        transformation: string, default="boxcox"
            Name of transformation to apply on transvars

        ids : array-like, shape (n_samples,)
            Identifiers for choice situations in long format.

        weights : array-like, shape (n_variables,), default=None
            Weights for the choice situations in long format.

        avail: array-like, shape (n_samples,)
            Availability of alternatives for the choice situations. One when
            available or zero otherwise.

        randvars : dict
            Names (keys) and mixing distributions (values) of variables that
            have random parameters as coefficients. Possible mixing
            distributions are: ``'n'``: normal, ``'ln'``: lognormal,
            ``'u'``: uniform, ``'t'``: triangular, ``'tn'``: truncated normal

        panels : array-like, shape (n_samples,), default=None
            Identifiers in long format to create panels in combination with
            ``ids``

        base_alt : int, float or str, default=None
            Base alternative

        fit_intercept : bool, default=False
            Whether to include an intercept in the model.

        init_coeff : numpy array, shape (n_variables,), default=None
            Initial coefficients for estimation.

        maxiter : int, default=200
            Maximum number of iterations

        random_state : int, default=None
            Random seed for numpy random generator

        correlation: boolean or list, default=None
            If boolean finds correlation for all random (non trans) vars
            If list finds correlation between variables specified

        n_draws : int, default=1000
            Number of random draws to approximate the mixing distributions of
            the random coefficients

        halton : bool, default=True
            Whether the estimation uses halton draws.

        minimise_func : func, default=None
            Sets minimise function used.

        verbose : int, default=1
            Verbosity of messages to show during estimation. 0: No messages,
            1: Some messages, 2: All messages

        batch_size : int, default=None
            Size of batches of random draws used to avoid overflowing memory during computations.

        halton_opts : dict, default=None
            Options for generation of halton draws. The dictionary accepts the following options (keys):

                shuffle : bool, default=False
                    Whether the Halton draws should be shuffled

                drop : int, default=100
                    Number of initial Halton draws to discard to minimize correlations between Halton sequences

                primes : list
                    List of primes to be used as base for generation of Halton sequences.

        ftol : int, float, default=1e-7
            Sets the tol parameter in scipy.optimize.minimize - Tolerance for
            termination.

        gtol: int, float, default=1e-5
            Sets the gtol parameter in scipy.optimize.minimize(method="bfgs) -
            Gradient norm must be less than gtol before successful termination.

        return_hess : bool, default=True
            Calculate and return the gradient in _loglik_and_gradient

        return_grad : bool, default=True
            Calculate and return the gradient in _loglik_and_gradient

        method: string, default="bfgs"
            specify optimisation method

        mnl_init: bool, default=True
            Initialise coefficients with multinomial logit estimates.

        Returns
        -------
        None.
        """

        X, y, varnames, alts, isvars, transvars, ids, weights, \
            panels, avail = self._as_array(X, y, varnames, alts, isvars,
                                           transvars, ids, weights, panels,
                                           avail)
        # Handle array-like inputs by converting everything to numpy arrays
        self._validate_inputs(X, y, alts, varnames, isvars, ids, weights,
                              panels, base_alt, fit_intercept, maxiter)

        self._pre_fit(alts, varnames, isvars, transvars, base_alt,
                      fit_intercept, transformation, maxiter, panels,
                      correlation, randvars)

        X_original = X  # tmp fix... store to use in mnl_init later
        y_original = y

        batch_size = n_draws if batch_size is None else min(n_draws, batch_size)
        self.batch_size = batch_size

        self.randvarsdict = randvars  # random variables not transformed
        self.randvars = [x for x in self.randvars if x not in transvars]
        #  random variables that are transformed
        self.randtransvars = [x for x in transvars if (x in randvars) and
                              (x not in self.randvars)]
        self.fixedtransvars = [x for x in transvars if x not in
                               self.randtransvars]
        self.n_draws = n_draws
        self.gtol = gtol
        # divide the variables in varnames into fixed, fixed transformed,
        # random, random transformed by getting 4 index arrays
        # also for random and random transformed save the distributions
        # in a separate array
        self.reg_penalty = reg_penalty
        self.fxidx, self.fxtransidx = [], []
        self.rvidx, self.rvdist = [], []
        self.rvtransidx, self.rvtransdist = [], []
        for var in self.varnames:
            if isvars is not None:
                if var in isvars:
                    continue
            if hasattr(randvars, 'keys') and var in randvars.keys():  # bug fix
                self.fxidx.append(False)
                self.fxtransidx.append(False)
                if var in self.randvars:
                    self.rvidx.append(True)
                    self.rvdist.append(randvars[var])
                    self.rvtransidx.append(False)
                else:
                    self.rvidx.append(False)
                    self.rvtransidx.append(True)
                    self.rvtransdist.append(randvars[var])
            else:
                self.rvidx.append(False)
                self.rvtransidx.append(False)
                self.rvdist.append(False)
                self.rvtransdist.append(False)
                if var in transvars:
                    self.fxtransidx.append(True)
                    self.fxidx.append(False)
                else:
                    self.fxtransidx.append(False)
                    self.fxidx.append(True)

        self.rvidx = np.array(self.rvidx)
        self.rvtransidx = np.array(self.rvtransidx)
        self.fxidx = np.array(self.fxidx)
        self.fxtransidx = np.array(self.fxtransidx)
        if random_state is not None:
            np.random.seed(random_state)
        X, y, panels = self._arrange_long_format(X, y, ids, alts, panels)
        X, Xnames = self._setup_design_matrix(X)
        self._model_specific_validations(randvars, Xnames)
        self.Xnames = Xnames  # saved here to use in LatentMixed...
        J, K, R = X.shape[1], X.shape[2], n_draws

        if self.transformation == "boxcox":
            self.trans_func = boxcox_transformation_mixed
            self.transform_deriv = boxcox_param_deriv_mixed

        R = n_draws
        if panels is not None:
            X, y, avail, panel_info = self._balance_panels(X, y, avail, panels)
            N, P = panel_info.shape
        else:
            N, P = X.shape[0], 1
            panel_info = np.ones((N, 1))

        X = X.reshape(N, P, J, K)
        y = y.reshape(N, P, J, 1)
        self.y = y
        self.panel_info = panel_info

        self.obs_prob = np.mean(np.mean(np.mean(y, axis=3), axis=1), axis=0)

        self.verbose = verbose

        self.return_grad = return_grad
        self.return_hess = return_hess
        if hasattr(method, 'lower'):
            self.method = method.lower()

        jac = True if self.return_grad else False

        self.total_fun_eval = 0

        #  reshape weights (using panel data if necessary)
        if weights is not None:
            weights = self._reshape_weights(weights, panels)

        if avail is not None:
            avail = self._reshape_avail(avail, panels)

        # Generate draws
        draws, drawstrans = self._generate_draws(self.N, R, halton)  # (N,Kr,R)

        # save draws for use in summary
        self.draws = draws
        self.drawstrans = drawstrans
        self.save_fitted_params = save_fitted_params
        # 2x Kftrans - mean and lambda, 3x Krtrans - mean, s.d., lambda
        # Kchol, Kbw - relate to random variables, non-transformed
        # Kchol - cholesky matrix, Kbw the s.d. for random vars
        n_coeff = self.Kf + self.Kr + self.Kchol + self.Kbw + 2*self.Kftrans +\
            3*self.Krtrans

        if mnl_init and init_coeff is None:
            # Initalise coefficients using a multinomial logit model
            mnl = MultinomialLogit()
            # varnames_mnl = [varname for varname in Xnames if 'sd' not in varname
            #                                               and 'chol' not in varname
            #                                               and 'lambda' not in varname]
            varnames_mnl = varnames
            mnl.fit(X_original,
                    y_original.flatten(),
                    varnames_mnl,
                    alts,
                    isvars,
                    transvars=transvars,
                    ids=ids,
                    weights=weights,
                    avail=avail,
                    base_alt=base_alt,
                    fit_intercept=fit_intercept,
                    verbose=0)

            init_coeff = mnl.coeff_
            # mnl estimates -> mxl needs to add stdev to random variables
            init_coeff = np.concatenate((init_coeff[:self.Kf+2*self.Kftrans+self.Kr],
                                         np.repeat(.1, self.Kchol + self.Kbw),
                                         init_coeff[self.Kf+2*self.Kftrans+self.Kr:self.Kf+2*self.Kftrans+self.Kr+self.Krtrans],
                                         ))
            if self.Krtrans:
                init_coeff = np.concatenate((init_coeff,
                                             np.repeat(.1, self.Krtrans),
                                             init_coeff[-self.Krtrans:]))
        if init_coeff is None:
            betas = np.repeat(.1, n_coeff)
        else:
            betas = init_coeff
            if len(init_coeff) != n_coeff and not hasattr(self, 'class_params_spec'):
                raise ValueError("The size of init_coeff must be: " + str(n_coeff))
        if dev.using_gpu:
            X, y = dev.to_gpu(X), dev.to_gpu(y)
            panel_info = dev.to_gpu(panel_info)
            draws = dev.to_gpu(draws)
            drawstrans = dev.to_gpu(drawstrans)
            if weights is not None:
                weights = dev.to_gpu(weights)
            if avail is not None:
                avail = dev.to_gpu(avail)
            if verbose > 0:
                print("Estimation with GPU processing enabled.")
        positive_bound = (0, 1e+30)
        any_bound = (-1e+30, 1e+30)
        # corr_bound = (-1, 1)
        lmda_bound = (-5, 1)

        # to be used with L-BFGS-B method, automatically generate bounds
        bound_dict = {
            "bf": (any_bound, self.Kf),
            "br_b": (any_bound, self.Kr),
            "chol": (any_bound, self.Kchol),
            "br_w": (positive_bound, self.Kr - self.correlationLength),
            "bf_trans": (any_bound, self.Kftrans),
            "flmbda": (lmda_bound, self.Kftrans),
            "br_trans_b": (any_bound, self.Krtrans),
            "br_trans_w": (any_bound, self.Krtrans),
            "rlmbda": (lmda_bound, self.Krtrans)
        }

        # list comrephension to add number of bounds for each variable type
        # bound[1][0] - the bound range
        # bound[1][1] - how many bounds to add
        bnds = [(bound[1][0],) * int(bound[1][1])
                for bound in bound_dict.items() if bound[1][1] > 0]
        # convert into appropriate format for L-BFGS-B
        bnds = [tuple(itertools.chain.from_iterable(bnds))][0]

        minimise_func = minimize if minimise_func is None else minimise_func

        optimizat_res = \
            minimise_func(
                self._loglik_gradient,
                betas,
                jac=jac,
                method=method,
                args=(X, y, panel_info, draws, drawstrans, weights,
                      avail, batch_size),
                tol=ftol,
                bounds=bnds if method == "L-BFGS-B" else None,
                options={
                    'gtol': gtol,
                    'maxiter': maxiter,
                    'disp': verbose > 0,
                }
            )
        if hasattr(self, 'method') and self.method == "L-BFGS-B":
            # calculate hessian by finite differences at minimisation point
            def _hessian(x, func, eps=1e-8):
                N = x.size
                h = np.zeros((N, N))
                df_0 = func(x)[1]
                for i in np.arange(N):
                    xx0 = 1 * x[i]
                    x[i] = xx0 + eps
                    df_1 = func(x)[1]
                    h[i, :] = (df_1 - df_0)/eps
                    x[i] = xx0
                return h

            def _get_loglik_gradient(betas):
                res = self._loglik_gradient(betas, X, y, panel_info, draws,
                                            drawstrans, weights, avail)
                return res

            H = _hessian(optimizat_res['x'], _get_loglik_gradient)
            H = np.linalg.inv(H)
            optimizat_res['hess_inv'] = H

        if self.save_fitted_params:
            self._save_fitted_params(self.y, self.p, panel_info, self.Br)

        # save predicted and observed probabilities to display in summary
        try:
            if 'is_latent_class' in optimizat_res.keys():
                pass
            else:
                p = self._compute_probabilities(optimizat_res['x'],
                                                X,
                                                panel_info,
                                                draws,
                                                drawstrans,
                                                avail,
                                                self.var_list,
                                                self.chol_mat)

                self.choice_pred_prob = np.mean(p, axis=3)
                self.ind_pred_prob = np.mean(self.choice_pred_prob, axis=1)
                self.pred_prob = np.mean(self.ind_pred_prob, axis=0)
                self.prob_full = p
        except Exception:
            pass
        self._post_fit(optimizat_res, Xnames, N, verbose=verbose)

    def _reshape_weights(self, weights, panels):
        """Logic to reshape weights according to panels."""
        N, P, J = self.N, self.P, self.J
        weights = weights*(N/np.sum(weights))  # Normalize weights
        if panels is not None:
            # copied logic from _balance_panels function
            _, p_obs = np.unique(panels, return_counts=True)
            p_obs = (p_obs/J).astype(int)
            weights_temp = np.zeros((N, P, J))
            cum_p = 0
            for n, p in enumerate(p_obs):
                weights_temp[n, 0:p, :] = weights[cum_p:cum_p+(p*J)].reshape((1, p, J))
                cum_p += p
            weights = weights_temp.reshape(N, P, J)
        else:
            weights = weights.reshape(N, J)
        return weights

    def _reshape_avail(self, avail, panels):
        """Logic to reshape avail according to panels."""
        N, P, J = self.N, self.P, self.J
        if panels is not None:
            # copied logic from _balance_panels function
            _, p_obs = np.unique(panels, return_counts=True)
            p_obs = (p_obs/J).astype(int)
            avail_temp = np.zeros((N, P, J))
            cum_p = 0
            for n, p in enumerate(p_obs):
                avail_temp[n, 0:p, :] = avail[cum_p:cum_p+(p*J)].reshape((1, p, J))
                cum_p += p
            avail = avail_temp.reshape(N, P, J)
        else:
            avail = avail.reshape(N, J)
        return avail

    def _save_fitted_params(self, y, p, panel_info, Br):
        # TODO: could improve ... look at xlogit
        # calculate fitted parameter values
        if dev.using_gpu:
            y, p = dev.to_gpu(y), dev.to_gpu(p)
        pch = np.sum(y*p, axis=2)  # (N, P, R)
        pch = self._prob_product_across_panels(pch, panel_info)
        # Thresholds to avoid divide by zero warnings
        pch[pch == 0] = min_comp_val

        pch2 = np.divide(pch, np.sum(pch, axis=1)[:, None])  # pch/rowsum(pch)

        pch2 = pch2.flatten()
        temp_br = np.zeros((self.N*self.batch_size, self.Kr))
        if dev.using_gpu:
            temp_br = dev.to_gpu(temp_br)
        for i in range(self.N):
            for k in range(self.Kr):
                temp_br[(i*self.batch_size):((i+1)*self.batch_size), k] = Br[i, k, :]

        Br = temp_br

        pch2 = np.multiply(pch2[:, None], Br)
        # if not dev.using_gpu:
        pch2_res = np.zeros((self.N, self.Kr))
        pch2_sd_test = np.zeros((self.N, self.Kr))
        if dev.using_gpu:
            pch = dev.to_gpu(pch)
            pch2_res = dev.to_gpu(pch2_res)
            pch2_sd_test = dev.to_gpu(pch2_sd_test)
        for i in range(self.N):
            # print('pch2[i*self.n_draws:(i+1)*self.n_draws, :]', pch2[i*self.n_draws:(i+1)*self.n_draws, :])
            pch2_res[i, :] = np.sum(pch2[i*self.batch_size:(i+1)*self.batch_size, :], axis=0)
            pch2_sd_test[i, :] = np.std(pch2[i*self.batch_size:(i+1)*self.batch_size, :],
                                        axis=0)

        self.pch2_res = pch2_res
        self.pch2_sd_test = pch2_sd_test

    def _construct_chol_mat(self, chol, Br_w, Brtrans_w):
        # creating cholesky matrix for the variance-covariance matrix
        # all random variables not included in correlation will only
        # have their standard deviation computed
        # NOTE: fairly poorly written function, made to patch bugs
        chol_mat = np.zeros((self.correlationLength, self.correlationLength))
        indices = np.tril_indices(self.correlationLength)
        if dev.using_gpu:
            chol = dev.to_cpu(chol)
            chol_mat[indices] = chol  # TODO? Better
        else:
            chol_mat[indices] = chol
        Kr_all = self.Kr + self.Krtrans
        chol_mat_temp = np.zeros((Kr_all, Kr_all))

        # TODO: Structure ... Kr first, Krtrans last, fill in for correlations
        # TODO: could do better
        rv_count = 0
        rv_count_all = 0
        rv_trans_count = 0
        rv_trans_count_all = 0
        chol_count = 0
        corr_indices = []

        # TODO: another bugfix
        # Know beforehand to order rvtrans correctly
        num_corr_rvtrans = 0
        for ii, var in enumerate(self.varnames):
            if self.rvtransidx[ii]:
                if hasattr(self, 'correlation') and self.correlation:
                    if hasattr(self.correlation, 'append'):
                        if var in self.correlation:
                            num_corr_rvtrans += 1
                    # else:
                    #     num_corr_rvtrans += 1

        num_rvtrans_total = self.Krtrans + num_corr_rvtrans

        offset_varnames = []
        if hasattr(self, 'Xnames'):
            offset_varnames = self.Xnames
        else:
            offset_varnames = self.varnames
        inter_offset = 0
        if not hasattr(self, 'class_params_spec'):
            inter_offset = len([x for x in offset_varnames if 'inter' in x]) - 1
        if inter_offset < 0:
            inter_offset = 0
        for ii, var in enumerate(self.varnames):  # TODO: BUGFIX
            ii_offset = ii + inter_offset
            is_correlated = False
            if hasattr(self, 'correlation') and self.correlation:
                if hasattr(self.correlation, 'append'):
                    if var in self.correlation:
                        is_correlated = True
                else:
                    is_correlated = True
            if self.rvidx[ii_offset]:
                rv_val = chol[chol_count] if is_correlated else Br_w[rv_count]
                chol_mat_temp[rv_count_all, rv_count_all] = rv_val
                rv_count_all += 1
                if is_correlated:
                    chol_count += 1
                else:
                    rv_count += 1
            if self.rvtransidx[ii_offset]:
                if hasattr(self, 'correlation') and isinstance(self.correlation, bool):  # BUG FIX
                    is_correlated = False
                rv_val = chol[chol_count] if is_correlated else Brtrans_w[rv_trans_count]
                chol_mat_temp[-num_rvtrans_total + rv_trans_count_all, -num_rvtrans_total + rv_trans_count_all] = rv_val
                rv_trans_count_all += 1
                if is_correlated:
                    chol_count += 1
                else:
                    rv_trans_count += 1
            if hasattr(self, 'correlation') and self.correlation:
                if hasattr(self.correlation, 'append'):
                    if var in self.correlation:
                        if self.rvidx[ii_offset]:
                            corr_indices.append(rv_count_all - 1)
                        else:
                            corr_indices.append(Kr_all - num_rvtrans_total + rv_trans_count_all - 1)   # TODO i think

        if hasattr(self, 'correlation') and isinstance(self.correlation, bool) and self.correlation:
            corr_pairs = list(itertools.combinations(np.arange(self.Kr), 2)) + [(i, i) for i in range(self.Kr)]
        else:
            corr_pairs = list(itertools.combinations(corr_indices, 2)) + [(idx, idx) for ii, idx in enumerate(corr_indices)]

        reversed_corr_pairs = [tuple(reversed(pair)) for ii, pair in enumerate(corr_pairs)]
        reversed_corr_pairs.sort(key=lambda x: x[0])

        chol_count = 0
        for _, corr_pair in enumerate(reversed_corr_pairs):
            # lower cholesky matrix
            chol_mat_temp[corr_pair] = chol[chol_count]
            chol_count += 1
        # # add non-correlated random variables to cholesky matrix
        # num_rand_noncorr = sel f.Kr - self.correlationLength
        # for i in range(num_rand_noncorr):
        #     chol_mat_temp[i, i] = Br_w[i]
        # # add non-correlated transformed random variables to cholesky matrix
        # for i in range(self.Krtrans):
        #     chol_mat_temp[i + num_rand_noncorr, i + num_rand_noncorr] = Brtrans_w[i]

        # if self.correlationLength > 0:
        #     chol_mat_temp[-self.correlationLength:, -self.correlationLength:] = \
        #         chol_mat

        chol_mat = chol_mat_temp

        return chol_mat

    def _compute_probabilities(self, betas, X, panel_info, draws, drawstrans,
                               avail, var_list, chol_mat):
        """Compute choice probabilities for each alternative."""
        # Creating random coeffs using Br_b, cholesky matrix and random draws
        # Estimating the linear utility specification (U = sum of Xb)

        Bf, Br_b, chol, Br_w, Bftrans, flmbda, Brtrans_b, Brtrans_w, rlmda = \
            var_list.values()
        if dev.using_gpu:
            Bf, Br_b, chol, Br_w, Bftrans, flmbda, Brtrans_b, \
                Brtrans_w, rlmda = \
                dev.to_gpu(Bf), dev.to_gpu(Br_b), dev.to_gpu(chol), \
                dev.to_gpu(Br_w), dev.to_gpu(Bftrans), dev.to_gpu(flmbda), \
                dev.to_gpu(Brtrans_b), dev.to_gpu(Brtrans_w), dev.to_gpu(rlmda)

        Xf = X[:, :, :, self.fxidx]
        Xftrans = X[:, :, :, self.fxtransidx]
        Xr = X[:, :, :, self.rvidx]
        Xrtrans = X[:, :, :, self.rvtransidx]

        XBf = np.zeros((self.N, self.P, self.J))
        XBr = np.zeros((self.N, self.P, self.J, self.batch_size))
        V = np.zeros((self.N, self.P, self.J, self.batch_size))
        Br = None
        if dev.using_gpu:
            XBf = dev.to_gpu(XBf)
            XBr = dev.to_gpu(XBr)
            V = dev.to_gpu(V)
        if self.Kf != 0:
            XBf = dev.cust_einsum('npjk,k -> npj', Xf, Bf)

        if self.Kr != 0:
            Br = Br_b[None, :, None] + dev.np.matmul(chol_mat[:self.Kr, :self.Kr], draws)
            Br = self._apply_distribution(Br, self.rvdist)

            self.Br = Br  # save Br to use later
            XBr = dev.cust_einsum('npjk,nkr -> npjr', Xr, Br)  # (N, P, J, R)
            V = XBf[:, :, :, None] + XBr

        #  transformations for variables with fixed coeffs
        if self.Kftrans != 0:
            Xftrans_lmda = self.trans_func(Xftrans, flmbda)
            Xftrans_lmda[np.where(Xftrans_lmda < -max_comp_val)] = -max_comp_val
            Xftrans_lmda[np.where(Xftrans_lmda > max_comp_val)] = max_comp_val
            # Estimating the linear utility specificiation (U = sum XB)
            Xbf_trans = dev.cust_einsum('npjk,k -> npj', Xftrans_lmda, Bftrans)
            # combining utilities
            V += Xbf_trans[:, :, :, None]

        # transformations for variables with random coeffs
        if self.Krtrans != 0:
            # creating the random coeffs
            Brtrans = Brtrans_b[None, :, None] + \
                    drawstrans[:, 0:self.Krtrans, :] * Brtrans_w[None, :, None]
            Brtrans = self._apply_distribution(Brtrans, self.rvtransdist)
            self.Brtrans = Brtrans  # saving for later use
            # applying transformation
            Xrtrans_lmda = self.trans_func(Xrtrans, rlmda)
            Xrtrans_lmda[np.where(Xrtrans_lmda > max_comp_val)] = max_comp_val
            Xrtrans_lmda[np.where(Xrtrans_lmda < -max_comp_val)] = -max_comp_val

            Xbr_trans = dev.cust_einsum('npjk,nkr -> npjr', Xrtrans_lmda, Brtrans)  # (N, P, J, R)
            # combining utilities
            V += Xbr_trans  # (N, P, J, R)

        # Thresholds to avoid overflow warnings
        V[np.where(V > max_exp_val)] = max_exp_val
        V[np.where(V < -max_exp_val)] = -max_exp_val
        eV = dev.np.exp(V)

        # Exponent of the utility function for the logit formula
        if avail is not None:
            if self.panels is not None:
                eV = eV*avail[:, :, :, None]  # Acommodate availablity of alts with panels
            else:
                eV = eV*avail[:, None, :, None]  # Acommodate availablity of alts.

        sum_eV = dev.np.sum(eV, axis=2, keepdims=True)
        sum_eV[np.where(sum_eV < min_comp_val)] = min_comp_val
        p = np.divide(eV, sum_eV, out=np.zeros_like(eV))
        if self.save_fitted_params:
            self.p = p  # save

        return p

    def regularize_loglik(self, betas, backwards = False):
        
        """_summary_ 
            Use lasso reugularisation L2 to penalise in the function_

        Returns:
            float_: returns penalty term for lasso regression (regularizaiton)
            
        """
        if backwards:
            return -self.reg_penalty*sum(np.square(betas))
        else:
            return self.reg_penalty*sum(np.square(betas))
        
    
    
    def _loglik_gradient(self, betas, X, y, panel_info, draws, drawstrans,
                         weights, avail, batch_size):
        """Compute the log-likelihood and gradient.

        Fixed and random parameters are handled separately to
        speed up the estimation and the results are concatenated.
        """
        # Segregating initial values to fixed betas (Bf),
        # random beta means (Br_b)
        # for both non-transformed and transformed variables
        # and random beta cholesky factors (chol)
        self.betas = betas  # save to display later

        if dev.using_gpu:
            betas = dev.to_gpu(betas)

        beta_segment_names = ["Bf", "Br_b", "chol", "Br_w", "Bftrans",
                              "flmbda", "Brtrans_b", "Brtrans_w", "rlmda"]
        var_list = dict()
        # number of parameters for each corresponding segment
        iterations = [self.Kf, self.Kr, self.Kchol, self.Kbw, self.Kftrans,
                      self.Kftrans, self.Krtrans, self.Krtrans, self.Krtrans]

        i = 0
        for count, iteration in enumerate(iterations):
            prev_index = i
            i = int(i + iteration)
            var_list[beta_segment_names[count]] = betas[prev_index:i]

        Bf, Br_b, chol, Br_w, Bftrans, flmbda, Brtrans_b, Brtrans_w, rlmda = \
            var_list.values()
        if dev.using_gpu:
            Bf, Br_b, chol, Br_w, Bftrans, flmbda, Brtrans_b, \
                Brtrans_w, rlmda = \
                dev.to_gpu(Bf), dev.to_gpu(Br_b), dev.to_gpu(chol), \
                dev.to_gpu(Br_w), dev.to_gpu(Bftrans), dev.to_gpu(flmbda), \
                dev.to_gpu(Brtrans_b), dev.to_gpu(Brtrans_w), dev.to_gpu(rlmda)

        chol_mat = self._construct_chol_mat(chol, Br_w, Brtrans_w)

        if dev.using_gpu:
            chol_mat = dev.to_gpu(chol_mat)

        omega = dev.np.matmul(chol_mat, np.transpose(chol_mat))
        corr_mat = np.zeros_like(chol_mat)

        standard_devs = np.sqrt(np.abs(np.diag(omega)))
        K = len(standard_devs)
        for i in range(K):
            for j in range(K):
                corr_mat[i, j] = omega[i, j] / (standard_devs[i] * standard_devs[j])
        self.omega = omega
        self.stdevs = standard_devs
        self.corr_mat = corr_mat

        R = self.n_draws
        n_batches = R//batch_size + (1 if R % batch_size != 0 else 0)
        N = self.N
        _, gr_b, gr_w, pch = np.zeros((N, self.Kf)), np.zeros((N, self.Kr)), np.zeros((N, self.Kr)), []  # Batch data

        g_all = np.zeros((N, len(betas)))

        for batch in range(n_batches):
            draws_batch = draws[:, :, batch*batch_size: batch*batch_size + batch_size]
            drawstrans_batch = drawstrans[:, :, batch*batch_size: batch*batch_size + batch_size]
            if dev.using_gpu:
                draws_batch = dev.to_gpu(draws_batch)

            self.chol_mat = chol_mat
            self.var_list = var_list

            p = self._compute_probabilities(betas, X, panel_info, draws_batch, drawstrans_batch,
                                            avail, var_list, chol_mat)

            # Joint probability estimation for panels data
            pch_batch = np.sum(y*p, axis=2)  # (N, P, R)
            pch_batch = self._prob_product_across_panels(pch_batch, panel_info)
            # Thresholds to avoid divide by zero warnings
            pch_batch[pch_batch == 0] = min_comp_val

            # Observed probability minus predicted probability
            ymp = y - p  # (N, P, J, R)

            Xf = X[:, :, :, self.fxidx]
            Xftrans = X[:, :, :, self.fxtransidx]
            Xr = X[:, :, :, self.rvidx]
            Xrtrans = X[:, :, :, self.rvtransidx]

            # For fixed params
            # gradient = (Obs prob. minus predicted probability) * obs. var
            g = np.array([])
            if self.Kf != 0:
                g = dev.cust_einsum('npjr,npjk -> nkr', ymp, Xf)
                g = (g*pch_batch[:, None, :]).mean(axis=2)

            # For random params w/ untransformed vars, two gradients will be
            # estimated: one for the mean and one for the s.d.
            # for mean: gr_b = (Obs. prob. minus pred. prob.)  * obs. var
            # for s.d.: gr_b = (Obs. prob. minus pred. prob.)  * obs. var * rand draw
            # if random coef. is lognormally dist:
            # gr_b = (obs. prob minus pred. prob.) * obs. var. * rand draw * der(R.V.)

            if self.Kr != 0:
                der = self._compute_derivatives(betas, draws_batch, chol_mat=chol_mat, betas_random=self.Br)
                gr_b = dev.cust_einsum('npjr,npjk -> nkr', ymp, Xr)*der  # (N, Kr, R)
                # For correlation parameters
                # for s.d.: gr_w = (Obs prob. minus predicted probability) * obs. var * random draw
                draws_tril_idx = np.array([j
                                           for i in range(self.correlationLength)
                                           for j in range(i+1)])  # varnames pos.
                X_tril_idx = np.array([i
                                       for i in range(self.correlationLength)
                                       for j in range(i+1)])
                # Find the s.d. for random variables that are not correlated
                range_var = [x for x in
                             range(self.correlationLength, self.Kr)]
                range_var = sorted(range_var)
                draws_tril_idx = np.array(np.concatenate((draws_tril_idx,
                                                          range_var)))
                X_tril_idx = np.array(np.concatenate((X_tril_idx, range_var)))
                draws_tril_idx = draws_tril_idx.astype(int)
                X_tril_idx = X_tril_idx.astype(int)
                gr_w = gr_b[:, X_tril_idx, :]*draws_batch[:, draws_tril_idx, :]  # (N,P,Kr,R)
                gr_b = (gr_b*pch_batch[:, None, :]).mean(axis=2)  # (N,Kr)
                gr_w = (gr_w*pch_batch[:, None, :]).mean(axis=2)  # (N,Kr)

                # Gradient for fixed and random params
                g = np.concatenate((g, gr_b, gr_w), axis=1) if g.size \
                    else np.concatenate((gr_b, gr_w), axis=1)

            # For Box-Cox vars
            if len(self.transvars) > 0:
                if self.Kftrans:  # with fixed params
                    Xftrans_lmda = self.trans_func(Xftrans, flmbda)
                    Xftrans_lmda[np.where(Xftrans_lmda < -max_comp_val)] = -max_comp_val
                    Xftrans_lmda[np.where(Xftrans_lmda > max_comp_val)] = max_comp_val

                    gftrans = dev.cust_einsum('npjr,npjk -> nkr', ymp,
                                              Xftrans_lmda)  # (N, Kf, R)
                    # for the lambda param
                    der_Xftrans_lmda = self.transform_deriv(Xftrans, flmbda)
                    der_Xftrans_lmda[np.where(der_Xftrans_lmda > max_comp_val)] = max_comp_val
                    der_Xftrans_lmda[np.where(der_Xftrans_lmda < -max_comp_val)] = -max_comp_val
                    der_Xftrans_lmda[np.isnan(der_Xftrans_lmda)] = min_comp_val
                    der_Xbftrans = dev.np.einsum('npjk,k -> njk', der_Xftrans_lmda,
                                             Bftrans)

                    gftrans_lmda = dev.np.einsum('npjr,njk -> nkr', ymp,
                                             der_Xbftrans)
                    gftrans = (gftrans*pch_batch[:, None, :]).mean(axis=2)
                    gftrans_lmda = (gftrans_lmda*pch_batch[:, None, :]).mean(axis=2)
                    g = np.concatenate((g, gftrans, gftrans_lmda), axis=1) if g.size \
                        else np.concatenate((gftrans, gftrans_lmda), axis=1)

                if self.Krtrans:
                    # for rand parameters
                    # for mean: (obs prob. min pred. prob)*obs var * deriv rand coef
                    # if rand coef is lognormally distributed:
                    # gr_b = (obs prob minus pred. prob) * obs. var * rand draw * der(RV)
                    temp_chol = chol_mat if chol_mat.size != 0 else np.diag(Brtrans_w)
                    dertrans = self._compute_derivatives(betas,
                                                         draws=drawstrans_batch,
                                                         dist=self.rvtransdist,
                                                         chol_mat=temp_chol,
                                                         K=self.Krtrans,
                                                         trans=True,
                                                         betas_random=self.Brtrans
                                                         )
                    Xrtrans_lmda = self.trans_func(Xrtrans, rlmda)

                    Brtrans = Brtrans_b[None, :, None] + \
                        drawstrans[:, 0:self.Krtrans, :] * \
                        Brtrans_w[None, :, None]
                    Brtrans = self._apply_distribution(Brtrans,
                                                       self.rvtransdist)

                    grtrans_b = dev.cust_einsum('npjr,npjk -> nkr', ymp,
                                                Xrtrans_lmda)*dertrans
                    # for s.d. (obs - pred) * obs var * der rand coef * rd draw
                    grtrans_w = dev.cust_einsum('npjr,npjk -> nkr', ymp,
                                                Xrtrans_lmda) * dertrans * \
                        drawstrans_batch
                    # for the lambda param
                    # gradient = (obs - pred) * deriv x_lambda * beta
                    der_Xrtrans_lmda = self.transform_deriv(Xrtrans, rlmda)
                    der_Xrtrans_lmda[np.where(der_Xrtrans_lmda > max_comp_val)] = max_comp_val
                    der_Xrtrans_lmda[np.where(der_Xrtrans_lmda < -max_comp_val)] = max_comp_val
                    # TODO? KEEP an eye out ... 4, 3, 5 ...  no cust_einsum
                    der_Xbrtrans = dev.np.einsum('npjk, nkr -> npjkr', der_Xrtrans_lmda,
                                             Brtrans)  # (N, P, J, K, R)
                    grtrans_lmda = dev.np.einsum('npjr, npjkr -> nkr', ymp, der_Xbrtrans)  # (N, Krtrans, R)
                    grtrans_b = (grtrans_b*pch_batch[:, None, :]).mean(axis=2)  # (N,Kr)
                    grtrans_w = (grtrans_w*pch_batch[:, None, :]).mean(axis=2)  # (N,Kr)
                    grtrans_lmda = (grtrans_lmda*pch_batch[:, None, :]).mean(axis=2)  # (N,Kr)
                    g = np.concatenate((g, grtrans_b, grtrans_w, grtrans_lmda), axis=1) if g.size \
                        else np.concatenate((grtrans_b, grtrans_w, grtrans_lmda), axis=1)

            if dev.using_gpu:
                g = dev.to_cpu(g)
                pch_batch = dev.to_cpu(pch_batch)

            pch.append(pch_batch)

            g_all += g

        pch = np.concatenate(pch, axis=-1)
        lik = pch.mean(axis=1)  # (N,)
        loglik = np.log(lik)
        if weights is not None:
            loglik = loglik*weights
        loglik = loglik.sum()

        self.total_fun_eval += 1
        g = g_all

        g = g/lik[:, None]
        # updated gradient
        if weights is not None:
            if weights.ndim == 1:
                g = np.transpose(np.transpose(g) * weights)
            if weights.ndim == 2:
                g = np.transpose(np.transpose(g)*weights[:, 0])
            if weights.ndim == 3:  # (3 dim for panel data)
                g = np.transpose(np.transpose(g)*weights[:, 0, 0])
        g = np.sum(g, axis=0)/n_batches  # (K, )
        # log-lik
        self.gtol_res = np.linalg.norm(g, ord=np.inf)

        # print('g: ', g)
        # print('norm: ', np.linalg.norm(g, ord=np.inf))

        penalty = self.regularize_loglik(betas)
        
        result = (-loglik +penalty)

        if self.return_grad:
            result = (-loglik +penalty, -g)

        return result

    def validation_loglik(self, validation_X, validation_Y, betas=None,
                          avail=None, weights=None, panels=None):
        """Computes the log-likelihood on the validation set.

        Using estimated parameters, computes the log-likelihood on the
        validation set.
        """
        if panels is not None:
            N = len(np.unique(panels))
        else:
            N = self.N
        validation_X, Xnames = self._setup_design_matrix(validation_X)
        self.N = N

        betas = betas if betas is not None else self.coeff_
        if panels is not None:
            validation_X, validation_Y, avail, panel_info =   \
                self._balance_panels(validation_X, validation_Y, avail, panels)
        else:
            panel_info = np.ones((self.N, 1))

        if avail is not None:
            avail = self._reshape_avail(avail, panels)

        if weights is not None:
            weights = self._reshape_weights(weights, panels)

        validation_X = validation_X.reshape((N, self.P, self.J, -1))
        validation_Y = validation_Y.reshape((N, self.P, self.J, -1))
        draws, drawstrans = self._generate_draws(N, self.n_draws)  # (N,Kr,R)

        if dev.using_gpu:
            validation_X, validation_Y = dev.to_gpu(validation_X), dev.to_gpu(validation_Y)
            panel_info = dev.to_gpu(panel_info)
            draws = dev.to_gpu(draws)
            drawstrans = dev.to_gpu(drawstrans)
            if weights is not None:
                weights = dev.to_gpu(weights)
            if avail is not None:
                avail = dev.to_gpu(avail)

        self.y = validation_Y

        res = self._loglik_gradient(betas, validation_X, validation_Y,
                                    avail=avail, weights=weights,
                                    panel_info=panel_info,
                                    draws=draws, drawstrans=drawstrans,
                                    batch_size=self.batch_size
                                    )
        loglik = -res[0]
        return loglik

    def _prob_product_across_panels(self, pch, panel_info):
        if not np.all(panel_info):  # If panels unbalanced. Not all ones
            idx = panel_info == 0
            for i in range(pch.shape[2]):
                pch[:, :, i][idx] = 1  # Multiply by one when unbalanced
        pch = pch.prod(axis=1)  # (N,R)
        pch[pch == 0] = min_comp_val
        return pch  # (N,R)

    def _apply_distribution(self, betas_random, index=None, draws=None):
        """Apply the mixing distribution to the random betas."""
        index = index if (index is not None) else self.rvdist
        for k, dist in enumerate(index):
            if dist == 'ln':
                betas_random[:, k, :] = dev.np.exp(betas_random[:, k, :])
            elif dist == 'tn':
                betas_random[:, k, :] = betas_random[:, k, :] *\
                    (betas_random[:, k, :] > 0)
        return betas_random

    def _balance_panels(self, X, y, avail, panels):
        """Balance panels if necessary and produce a new version of X and y.

        If panels are already balanced, the same X and y are returned. This
        also returns panel_info, which keeps track of the panels that needed
        balancing.
        """
        _, J, K = X.shape
        _, p_obs = np.unique(panels, return_counts=True)
        p_obs = (p_obs/J).astype(int)
        N = len(p_obs)  # This is the new N after accounting for panels
        P = np.max(p_obs)  # panels length for all records
        if not np.all(p_obs[0] == p_obs):  # Balancing needed
            y = y.reshape(X.shape[0], J, 1) if y is not None else None
            avail = avail.reshape(X.shape[0], J, 1) if avail is not None else None
            Xbal, ybal, availbal = np.zeros((N*P, J, K)), np.zeros((N*P, J, 1)), np.zeros((N*P, J, 1))
            panel_info = np.zeros((N, P))
            cum_p = 0  # Cumulative sum of n_obs at every iteration
            for n, p in enumerate(p_obs):
                # Copy data from original to balanced version
                Xbal[n*P:n*P + p, :, :] = X[cum_p:cum_p + p, :, :]
                ybal[n*P:n*P + p, :, :] = y[cum_p:cum_p + p, :, :] if y is not None else None  # TODO? predict mode in xlogit?
                availbal[n*P:n*P + p, :, :] = avail[cum_p:cum_p + p, :, :] if avail is not None else None
                panel_info[n, :p] = np.ones(p)
                cum_p += p
        else:  # No balancing needed
            Xbal, ybal, availbal = X, y, avail
            panel_info = np.ones((N, P))
        ybal = ybal if y is not None else None
        availbal = availbal if avail is not None else None
        return Xbal, ybal, availbal, panel_info

    def _compute_derivatives(self, betas, draws, dist=None, K=None,
                             chol_mat=None, trans=False, betas_random=None):
        """Compute the derivatives based on the mixing distributions."""
        N, R = draws.shape[0], draws.shape[2]
        Kr = K if K else self.Kr

        der = dev.np.ones((N, Kr, R))
        dist = dist if dist else self.rvdist
        if any(set(dist).intersection(['ln', 'tn'])):  # If any ln or tn
            for k, dist_k in enumerate(dist):
                if dist_k == 'ln':
                    der[:, k, :] = betas_random[:, k, :]
                elif dist_k == 'tn':
                    der[:, k, :] = 1*(betas_random[:, k, :] > 0)
        return der

    def _transform_betas(self, betas, draws, index=None, trans=False, chol_mat=None):
        """Compute the products between the betas and the random coefficients.

        This method also applies the associated mixing distributions.
        """
        if trans:
            br_mean = betas[-3*self.Krtrans:-2*self.Krtrans]  # get pos from end array
            br_sd = betas[-2*self.Krtrans:-self.Krtrans]
            betas_random = br_mean[None, :, None] + draws*br_sd[None, :, None]
            betas_fixed = []
            betas_random = self._apply_distribution(betas_random, index,
                                                    draws=draws)
        else:
            # Extract coeffiecients from betas array
            betas_fixed = betas[0:self.Kf]  # First Kf positions
            br_mean = betas[self.Kf:self.Kf+self.Kr]

            betas_random = br_mean[None, :, None] + dev.np.matmul(chol_mat, draws)
            betas_random = self._apply_distribution(betas_random, index,
                                                    draws=draws)
        return betas_fixed, betas_random

    def _generate_draws(self, sample_size, n_draws, halton=True, chol_mat=None):
        """Generate draws based on the given mixing distributions."""
        draws = drawstrans = []
        if halton:
            if self.randvars:
                draws = self._generate_halton_draws(sample_size, n_draws,
                                                    np.sum(self.rvidx))
            if self.randtransvars:
                drawstrans = \
                    self._generate_halton_draws(sample_size,
                                                n_draws,
                                                np.sum(self.rvtransidx))
        else:
            if self.randvars:
                draws = self._get_random_draws(sample_size, n_draws,
                                               np.sum(self.rvidx))
            if self.randtransvars:
                drawstrans = self._get_random_draws(sample_size, n_draws,
                                                    np.sum(self.rvtransidx))
        # remove False to allow better enumeration
        self.rvdist = [x for x in self.rvdist if x is not False]
        for k, dist in enumerate(self.rvdist):
            if dist in ['n', 'ln', 'tn']:  # Normal based
                draws[:, k, :] = ss.norm.ppf(draws[:, k, :])
            elif dist == 't':  # Triangular
                draws_k = draws[:, k, :]
                draws[:, k, :] = (np.sqrt(2*draws_k) - 1)*(draws_k <= .5) +\
                    (1 - np.sqrt(2*(1 - draws_k)))*(draws_k > .5)
            elif dist == 'u':  # Uniform
                draws[:, k, :] = 2*draws[:, k, :] - 1

        # remove False to allow better enumeration
        self.rvtransdist = [x for x in self.rvtransdist if x is not False]
        for k, dist in enumerate(self.rvtransdist):
            if dist in ['n', 'ln', 'tn']:  # Normal based
                drawstrans[:, k, :] = ss.norm.ppf(drawstrans[:, k, :])
            elif dist == 't':  # Triangular
                draws_k = drawstrans[:, k, :]
                drawstrans[:, k, :] = (np.sqrt(2*draws_k) - 1)*(draws_k <= .5) +\
                    (1 - np.sqrt(2*(1 - draws_k)))*(draws_k > .5)
            elif dist == 'u':  # Uniform
                drawstrans[:, k, :] = 2*drawstrans[:, k, :] - 1
        draws = np.atleast_3d(draws)
        drawstrans = np.atleast_3d(drawstrans)
        return draws, drawstrans  # (N,Kr,R)

    def _get_random_draws(self, sample_size, n_draws, n_vars):
        """Generate random uniform draws between 0 and 1."""
        return np.random.uniform(size=(sample_size, n_vars, n_draws))

    def _generate_halton_draws(self, sample_size, n_draws, n_vars, shuffled=False, drop=100, primes=None):
        """Generate Halton draws for multiple random variables using different primes as base."""
        if primes is None:
            primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                      53, 59, 61, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109,
                      113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
                      179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
                      239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293,
                      307, 311]

        def halton_seq(length, prime=3, shuffled=False, drop=100):
            """Generates a halton sequence while handling memory efficiently.

            Memory is efficiently handled by creating a single array ``seq`` that is iteratively filled without using
            intermidiate arrays.
            """
            req_length = length + drop
            seq = np.empty(req_length)
            seq[0] = 0
            seq_idx = 1
            t = 1
            while seq_idx < req_length:
                d = 1/prime**t
                seq_size = seq_idx
                i = 1
                while i < prime and seq_idx < req_length:
                    max_seq = min(req_length - seq_idx, seq_size)
                    seq[seq_idx: seq_idx+max_seq] = seq[:max_seq] + d*i
                    seq_idx += max_seq
                    i += 1
                t += 1
            seq = seq[drop:length+drop]
            if shuffled:
                np.random.shuffle(seq)
            return seq

        draws = [halton_seq(sample_size*n_draws, prime=primes[i % len(primes)],
                            shuffled=shuffled, drop=drop).reshape(sample_size, n_draws) for i in range(n_vars)]
        draws = np.stack(draws, axis=1)
        return draws  # (N,Kr,R)

    def _model_specific_validations(self, randvars, Xnames):
        """Conduct validations specific for mixed logit models."""
        if randvars is None:
            raise ValueError("The randvars parameter is required for Mixed "
                             "Logit estimation")
        if not set(randvars.keys()).issubset(Xnames):
            raise ValueError("Some variable names in randvars were not found "
                             "in the list of variable names")
        if not set(randvars.values()).issubset(["n", "ln", "t", "tn", "u"]):
            raise ValueError("Wrong mixing distribution found in randvars. "
                             "Accepted distrubtions are n, ln, t, u, tn")

    def summary(self):
        """Show estimation results in console."""
        super(MixedLogit, self).summary()

    def _compute_null_loglik(self):
        null_p = (1/self.J)*np.ones_like(self.y)
        p = np.sum(self.y*null_p, axis=2)
        null_loglik = np.log(self._prob_product_across_panels(p,
                                                              self.panel_info))
        null_loglik = np.sum(null_loglik)
        null_loglik = -2 * null_loglik
        return null_loglik

    @staticmethod
    def check_if_gpu_available():
        """Check if GPU processing is available by running a quick estimation.

        Returns
        -------
        bool
            True if GPU processing is available, False otherwise.

        """
        n_gpus = dev.get_device_count()
        if n_gpus > 0:
            # Test a very simple example to see if CuPy is working
            X = np.array([[2, 1], [1, 3], [3, 1], [2, 4]])
            y = np.array([0, 1, 0, 1])
            model = MixedLogit()
            model.fit(X, y, varnames=["a", "b"], alts=["1", "2"], n_draws=500,
                      randvars={'a': 'n', 'b': 'n'}, maxiter=0, verbose=0)
            print("{} GPU device(s) available. xlogit will use "
                  "GPU processing".format(n_gpus))
            return True
        else:
            print("*** No GPU device found. Verify CuPy is properly installed")
            return False
