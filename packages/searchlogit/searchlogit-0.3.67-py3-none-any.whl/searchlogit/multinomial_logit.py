"""Implements multinomial and conditional logit models."""

import logging

import numpy as np
from scipy.optimize import minimize

from ._choice_model import ChoiceModel
from .boxcox_functions import boxcox_param_deriv, boxcox_transformation

# define the computation boundary values not to be exceeded
max_exp_val = 700

max_comp_val = 1e+300
min_comp_val = 1e-300

logger = logging.getLogger(__name__)


class MultinomialLogit(ChoiceModel):
    """Class for estimation of Multinomial and Conditional Logit Models"""

    def fit(self, X, y, varnames=None, alts=None, isvars=None, transvars=None,
            transformation="boxcox", ids=None, weights=None, avail=None,
            base_alt=None, fit_intercept=False, init_coeff=None, maxiter=2000,
            random_state=None, ftol=1e-7, gtol=1e-5, return_grad=True,
            return_hess=True, verbose=1, method="bfgs",
            scipy_optimisation=True):
        """Fit multinomial and/or conditional logit models.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_variables)
            Input data for explanatory variables in long format

        y : array-like, shape (n_samples,)
            Choices in long format

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

        base_alt : int, float or str, default=None
            Base alternative

        fit_intercept : bool, default=False
            Whether to include an intercept in the model.

        init_coeff : numpy array, shape (n_variables,), default=None
            Initial coefficients for estimation.

        maxiter : int, default=2000
            Maximum number of iterations

        random_state : int, default=None
            Random seed for numpy random generator

        ftol : int, float, default=1e-5
            Sets the tol parameter in scipy.optimize.minimize - Tolerance for
            termination.

        gtol: int, float, default=1e-5
            Sets the gtol parameter in scipy.optimize.minimize(method="bfgs) -
            Gradient norm must be less than gtol before successful termination.

        return_grad : bool, default=True
            Calculate and return the gradient in _loglik_and_gradient

        return_hess : bool, default=True
            Calculate and return the gradient in _loglik_and_gradient

        verbose : int, default=1
            Verbosity of messages to show during estimation. 0: No messages,
            1: Some messages, 2: All messages

        method : string, default="bfgs"
            specify optimisation method passed into scipy.optimize.minimize

        scipy_optimisation : bool, default=False
            Use scipy_optimisation for minimisation. When false uses own
            bfgs method.

        Returns
        -------
        None.
        """
        X, y, varnames, alts, isvars, transvars, ids, weights, panels, avail \
            = self._as_array(X, y, varnames, alts, isvars, transvars, ids,
                             weights, None, avail)
        self._validate_inputs(X, y, alts, varnames, isvars, ids, weights, None,
                              base_alt, fit_intercept, maxiter)

        self._pre_fit(alts, varnames, isvars, transvars, base_alt,
                      fit_intercept, transformation, maxiter, panels)
        self.fxidx, self.fxtransidx = [], []
        for var in self.varnames:
            if isvars is not None:
                if var in isvars:
                    continue
            if var in transvars:
                self.fxidx.append(False)
                self.fxtransidx.append(True)
            else:
                self.fxtransidx.append(False)
                self.fxidx.append(True)

        self.return_grad = return_grad
        self.return_hess = return_hess
        self.gtol = gtol
        self.ftol = ftol
        self.method = method

        jac = True if self.return_grad else False

        if random_state is not None:
            np.random.seed(random_state)

        if transformation == "boxcox":
            self.trans_func = boxcox_transformation
            self.transform_deriv = boxcox_param_deriv

        self.fixedtransvars = transvars
        X, Xnames = self._setup_design_matrix(X)
        self.Xnames = Xnames  # saved due to use in LCM

        if init_coeff is None:
            betas = np.repeat(.1, self.Kf + self.Kftrans*2)
        else:
            betas = init_coeff
            if len(init_coeff) != (self.Kf + self.Kftrans*2):
                if hasattr(self, 'is_latent_class') and self.is_latent_class:
                    pass
                else:
                    raise ValueError("The size of initial_coeff must be: "
                                     + str(int(X.shape[1])))

        if weights is not None:
            weights = weights.reshape(X.shape[0], X.shape[1])

        if avail is not None:
            avail = avail.reshape(X.shape[0], X.shape[1])

        y = y.reshape(-1, self.J)

        self.y = y

        self.obs_prob = np.mean(y, axis=0)

        # Call optimization routine
        if scipy_optimisation:
            optimizat_res = self._scipy_bfgs_optimization(betas, X, y, weights,
                                                          avail, maxiter, ftol,
                                                          gtol, jac)

        else:
            optimizat_res = self._bfgs_optimization(betas, X, y, weights,
                                                    avail, maxiter)

        # save predicted and observed probabilities to display in summary
        try:
            # don't save (here) for latent class models
            if 'is_latent_class' in optimizat_res.keys():
                pass
            else:
                p = self._compute_probabilities(optimizat_res['x'], X, avail)

                self.ind_pred_prob = p
                self.choice_pred_prob = p
                self.pred_prob = np.mean(p, axis=0)
        except Exception:
            pass

        sample_size = X.shape[0]
        self._post_fit(optimizat_res, Xnames, sample_size,
                       verbose=verbose)

    def _compute_probabilities(self, betas, X, avail):
        """Compute choice probabilities for each alternative."""
        Xf = X[:, :, self.fxidx]
        X_trans = X[:, :, self.fxtransidx]
        XB = 0
        if self.Kf > 0:
            B = betas[0:self.Kf]
            XB = Xf.dot(B)
        Xtrans_lmda = None
        if sum(self.fxtransidx):
            B_transvars = betas[self.Kf:(self.Kf+self.Kftrans)]
            lambdas = betas[(self.Kf + self.Kftrans):]
            # applying transformations
            Xtrans_lmda = self.trans_func(X_trans, lambdas)
            XB_trans = Xtrans_lmda.dot(B_transvars)
            XB += XB_trans

        XB[XB > max_exp_val] = max_exp_val  # avoiding infs
        XB[XB < -max_exp_val] = -max_exp_val  # avoiding infs

        XB = XB.reshape(self.N, self.J)

        eXB = np.exp(XB)
        if avail is not None:
            eXB = eXB*avail

        p = eXB / np.sum(eXB, axis=1, keepdims=True)

        return p

    def _loglik_and_gradient(self, betas, X, y, weights, avail):
        """Compute log-likelihood, gradient, and hessian."""
        logger.debug("Betas: {}".format(betas))
        logger.debug("Total func. evaluations: {}".format(self.total_fun_eval))

        self.total_fun_eval += 1

        p = self._compute_probabilities(betas, X, avail)
        # Log likelihood
        lik = np.sum(y*p, axis=1)
        lik[lik == 0] = min_comp_val
        loglik = np.log(lik)

        if weights is not None:
            loglik = loglik * weights[:, 0]  # doesn't matter which column
        loglik = np.sum(loglik)

        # Individual contribution to the gradient
        # Position of trans vars
        transpos = [self.varnames.tolist().index(i) for i in self.transvars]
        B_trans = betas[self.Kf:self.Kf+self.Kftrans]
        lambdas = betas[self.Kf+self.Kftrans:]
        X_trans = X[:, :, transpos]
        X_trans = X_trans.reshape(self.N, len(self.alternatives),
                                  len(transpos))
        ymp = y - p
        if self.Kf > 0:
            Xf = X[:, :, self.fxidx]
            grad = np.einsum('nj,njk -> nk', ymp, Xf)
        else:
            grad = np.array([])
        if self.Kftrans > 0:
            # Individual contribution of trans to the gradient
            lambdas = betas[(self.Kf + self.Kftrans):]
            Xtrans_lmda = self.trans_func(X_trans, lambdas)
            gtrans = np.einsum('nj,njk -> nk', ymp, Xtrans_lmda)
            der_Xtrans_lmda = self.transform_deriv(X_trans, lambdas)
            der_XBtrans = np.einsum('njk,k -> njk', der_Xtrans_lmda, B_trans)
            gtrans_lmda = np.einsum('nj,njk -> nk', ymp, der_XBtrans)
            grad = np.concatenate((grad, gtrans, gtrans_lmda), axis=1) \
                if grad.size \
                else np.concatenate((gtrans, gtrans_lmda), axis=1)  # (N, K)
        if weights is not None:
            #  all columns of weights same so only first used
            grad = np.transpose(np.transpose(grad)*weights[:, 0])

        if self.return_hess:
            H = np.dot(grad.T, grad)
            H[H == 0] = min_comp_val
            H[np.isnan(H)] = min_comp_val
            H[H > 1e+30] = 1e+30
            H[H < -1e+30] = -1e+30
            try:
                Hinv = np.linalg.inv(H)
            except Exception:  # use pseduo if normal inv fails
                Hinv = np.linalg.pinv(H)
            self.Hinv = Hinv

        grad = np.sum(grad, axis=0)
        self.gtol_res = np.linalg.norm(grad, ord=np.inf)

        result = (loglik)
        logger.debug('Norm: {}'.format(np.linalg.norm(grad, ord=np.inf)))
        # print('grad: ', grad)  # useful debugging
        # print('norm', np.linalg.norm(grad, ord=np.inf)) #  useful debugging

        if self.return_grad:
            result = (-loglik, -grad)
            if self.return_hess:
                result = (-loglik, -grad, Hinv)

        return result

    def _compute_null_loglik(self):
        """Computes the log-likelihood of the null model."""
        null_p = (1/self.J)*np.ones_like(self.y)
        lik = np.sum(self.y*null_p, axis=1)
        null_loglik = np.log(lik)
        null_loglik = np.sum(null_loglik)
        null_loglik = -2 * null_loglik
        return null_loglik

    def validation_loglik(self, validation_X, validation_Y, avail=None,
                          weights=None, betas=None):
        """Computes the log-likelihood on the validation set using
        the betas fitted using the training set.

        """
        validation_X, Xnames = self._setup_design_matrix(validation_X)
        validation_Y = validation_Y.reshape(self.N, self.J)

        betas = betas if betas is not None else self.coeff_
        res = self._loglik_and_gradient(betas, validation_X, validation_Y,
                                        avail=avail, weights=weights)
        loglik = res[0]
        logger.info('Validation loglik: ', loglik)
        return loglik

    def _scipy_bfgs_optimization(self, betas, X, y, weights, avail, maxiter,
                                 ftol, gtol, jac):
        optimizat_res = minimize(self._loglik_and_gradient,
                                 betas,
                                 args=(X, y, weights, avail),
                                 jac=jac,
                                 method=self.method,
                                 tol=ftol,
                                 options={
                                    'gtol': gtol,
                                    'maxiter': maxiter,
                                    }
                                 )
        return optimizat_res

    def _bfgs_optimization(self, betas, X, y, weights, avail, maxiter):
        res, g, Hinv = self._loglik_and_gradient(betas, X, y, weights, avail)
        current_iteration = 0
        convergence = False
        while True:
            old_g = g
            d = -Hinv.dot(g)
            step = 2
            while True:
                step = step/2
                s = step*d
                betas = betas + s
                resnew, gnew, _ = self._loglik_and_gradient(betas, X, y,
                                                            weights, avail)
                if resnew <= res or step < 1e-10:
                    break

            old_res = res
            res = resnew
            g = gnew
            delta_g = g - old_g

            Hinv = Hinv + (((s.dot(delta_g) + (delta_g[None, :].dot(Hinv)).dot(
                delta_g))*np.outer(s, s)) / (s.dot(delta_g))**2) - ((np.outer(
                    Hinv.dot(delta_g), s) + (np.outer(s, delta_g)).dot(Hinv)) /
                    (s.dot(delta_g)))
            current_iteration = current_iteration + 1
            if np.abs(res - old_res) < 0.00001:
                convergence = True
                break
            if current_iteration > maxiter:
                convergence = False
                break

        return {'success': convergence, 'x': betas, 'fun': res,
                'hess_inv': Hinv, 'nit': current_iteration}
