import numpy as np
from scipy.integrate._ivp.common import norm, EPS, warn_extraneous
from scipy.integrate._ivp.base import DenseOutput
from .dae import DaeSolver


S6 = 6 ** 0.5

# Butcher tableau. A is not used directly, see below.
C = np.array([(4 - S6) / 10, (4 + S6) / 10, 1])
E = np.array([-13 - 7 * S6, -13 + 7 * S6, -1]) / 3

# Eigendecomposition of A is done: A = T L T**-1. There is 1 real eigenvalue
# and a complex conjugate pair. They are written below.
MU_REAL = 3 + 3 ** (2 / 3) - 3 ** (1 / 3)
MU_COMPLEX = (3 + 0.5 * (3 ** (1 / 3) - 3 ** (2 / 3))
              - 0.5j * (3 ** (5 / 6) + 3 ** (7 / 6)))

# These are transformation matrices.
T = np.array([
    [0.09443876248897524, -0.14125529502095421, 0.03002919410514742],
    [0.25021312296533332, 0.20412935229379994, -0.38294211275726192],
    [1, 1, 0]])
TI = np.array([
    [4.17871859155190428, 0.32768282076106237, 0.52337644549944951],
    [-4.17871859155190428, -0.32768282076106237, 0.47662355450055044],
    [0.50287263494578682, -2.57192694985560522, 0.59603920482822492]])

# These linear combinations are used in the algorithm.
TI_REAL = TI[0]
TI_COMPLEX = TI[1] + 1j * TI[2]

# gamma = MU_REAL
# alpha = MU_COMPLEX.real
# beta = -MU_COMPLEX.imag
gamma = 3 + 3 ** (2 / 3) - 3 ** (1 / 3)
alpha = 3 + 0.5 * (3 ** (1 / 3) - 3 ** (2 / 3))
beta = 0.5 * (3 ** (5 / 6) + 3 ** (7 / 6))
Lambda = np.array([
    [gamma, 0, 0],
    [0, alpha, beta],
    [0, -beta, alpha],
])
denom = alpha**2 + beta**2
Lambda_inv = np.array([
    [denom / gamma, 0, 0],
    [0, alpha, -beta],
    [0, beta, alpha],
]) / denom

TLA = T @ Lambda
A_inv = T @ Lambda @ TI
A = T @ Lambda_inv @ TI
b = A[-1, :]
b_hat = b + (E * gamma) @ A

# Interpolator coefficients.
P = np.array([
    [13/3 + 7*S6/3, -23/3 - 22*S6/3, 10/3 + 5 * S6],
    [13/3 - 7*S6/3, -23/3 + 22*S6/3, 10/3 - 5 * S6],
    [1/3, -8/3, 10/3]])

NEWTON_MAXITER = 6  # Maximum number of Newton iterations.
MIN_FACTOR = 0.2  # Minimum allowed decrease in a step size.
MAX_FACTOR = 10  # Maximum allowed increase in a step size.


def solve_collocation_system(fun, t, y, h, Z0, scale, tol,
                             LU_real, LU_complex, solve_lu):
    """Solve the collocation system.

    Parameters
    ----------
    fun : callable
        Right-hand side of the system.
    t : float
        Current time.
    y : ndarray, shape (n,)
        Current state.
    h : float
        Step to try.
    Z0 : ndarray, shape (3, n)
        Initial guess for the solution. It determines new values of `y` at
        ``t + h * C`` as ``y + Z0``, where ``C`` is the Radau method constants.
    scale : ndarray, shape (n)
        Problem tolerance scale, i.e. ``rtol * abs(y) + atol``.
    tol : float
        Tolerance to which solve the system. This value is compared with
        the normalized by `scale` error.
    LU_real, LU_complex
        LU decompositions of the system Jacobians.
    solve_lu : callable
        Callable which solves a linear system given a LU decomposition. The
        signature is ``solve_lu(LU, b)``.

    Returns
    -------
    converged : bool
        Whether iterations converged.
    n_iter : int
        Number of completed iterations.
    Z : ndarray, shape (3, n)
        Found solution.
    rate : float
        The rate of convergence.
    """
    n = y.shape[0]

    # W = V of Fabien
    # A_inv = W of Fabien
    Z = Z0
    W = TI.dot(Z0)
    Yp = A_inv @ Z / h

    F = np.empty((3, n))
    tau = t + h * C

    dW_norm_old = None
    dW = np.empty_like(W)
    converged = False
    rate = None
    for k in range(NEWTON_MAXITER):
        Z = T.dot(W)
        Yp = (A_inv / h) @ Z
        Y = y + Z
        for i in range(3):
            F[i] = fun(tau[i], Y[i], Yp[i])

        if not np.all(np.isfinite(F)):
            break

        U = TI @ F
        f_real = -U[0]
        f_complex = -(U[1] + 1j * U[2])

        dW_real = solve_lu(LU_real, f_real)
        dW_complex = solve_lu(LU_complex, f_complex)

        dW[0] = dW_real
        dW[1] = dW_complex.real
        dW[2] = dW_complex.imag

        dW_norm = norm(dW / scale)
        if dW_norm_old is not None:
            rate = dW_norm / dW_norm_old

        if (rate is not None and (rate >= 1 or rate ** (NEWTON_MAXITER - k) / (1 - rate) * dW_norm > tol)):
            break

        W += dW
        Z = T.dot(W)
        Yp = A_inv @ Z / h
        Y = y + Z

        if (dW_norm == 0 or rate is not None and rate / (1 - rate) * dW_norm < tol):
            converged = True
            break

        dW_norm_old = dW_norm

    return converged, k + 1, Y, Yp, Z, rate


def predict_factor(h_abs, h_abs_old, error_norm, error_norm_old):
    """Predict by which factor to increase/decrease the step size.

    The algorithm is described in [1]_.

    Parameters
    ----------
    h_abs, h_abs_old : float
        Current and previous values of the step size, `h_abs_old` can be None
        (see Notes).
    error_norm, error_norm_old : float
        Current and previous values of the error norm, `error_norm_old` can
        be None (see Notes).

    Returns
    -------
    factor : float
        Predicted factor.

    Notes
    -----
    If `h_abs_old` and `error_norm_old` are both not None then a two-step
    algorithm is used, otherwise a one-step algorithm is used.

    References
    ----------
    .. [1] E. Hairer, S. P. Norsett G. Wanner, "Solving Ordinary Differential
           Equations II: Stiff and Differential-Algebraic Problems", Sec. IV.8.
    """
    if error_norm_old is None or h_abs_old is None or error_norm == 0:
        multiplier = 1
    else:
        multiplier = h_abs / h_abs_old * (error_norm_old / error_norm) ** 0.25

    with np.errstate(divide='ignore'):
        factor = min(1, multiplier) * error_norm ** -0.25

    return factor


# TODO:
# - adapt documentation
# - fix error estimate
class RadauDAE(DaeSolver):
    """Implicit Runge-Kutta method of Radau IIA family of order 5.

    The implementation follows [4]_, where most of the ideas come from [2]_. 
    The embedded formula of [3]_ is applied to implicit differential equations.
    The error is controlled with a third-order accurate embedded formula as 
    introduced in [2]_ and refined in [3]_. The procedure is slightly adapted 
    by [4]_ to cope with implicit differential equations. A cubic polynomial 
    which satisfies the collocation conditions is used for the dense output.

    Parameters
    ----------
    fun : callable
        Right-hand side of the system. The calling signature is ``fun(t, y)``.
        Here ``t`` is a scalar, and there are two options for the ndarray ``y``:
        It can either have shape (n,); then ``fun`` must return array_like with
        shape (n,). Alternatively it can have shape (n, k); then ``fun``
        must return an array_like with shape (n, k), i.e., each column
        corresponds to a single column in ``y``. The choice between the two
        options is determined by `vectorized` argument (see below). The
        vectorized implementation allows a faster approximation of the Jacobian
        by finite differences (required for this solver).
    t0 : float
        Initial time.
    y0 : array_like, shape (n,)
        Initial state.
    t_bound : float
        Boundary time - the integration won't continue beyond it. It also
        determines the direction of the integration.
    first_step : float or None, optional
        Initial step size. Default is ``None`` which means that the algorithm
        should choose.
    max_step : float, optional
        Maximum allowed step size. Default is np.inf, i.e., the step size is not
        bounded and determined solely by the solver.
    rtol, atol : float and array_like, optional
        Relative and absolute tolerances. The solver keeps the local error
        estimates less than ``atol + rtol * abs(y)``. HHere `rtol` controls a
        relative accuracy (number of correct digits), while `atol` controls
        absolute accuracy (number of correct decimal places). To achieve the
        desired `rtol`, set `atol` to be smaller than the smallest value that
        can be expected from ``rtol * abs(y)`` so that `rtol` dominates the
        allowable error. If `atol` is larger than ``rtol * abs(y)`` the
        number of correct digits is not guaranteed. Conversely, to achieve the
        desired `atol` set `rtol` such that ``rtol * abs(y)`` is always smaller
        than `atol`. If components of y have different scales, it might be
        beneficial to set different `atol` values for different components by
        passing array_like with shape (n,) for `atol`. Default values are
        1e-3 for `rtol` and 1e-6 for `atol`.
    jac : {None, array_like, sparse_matrix, callable}, optional
        Jacobian matrix of the right-hand side of the system with respect to
        y, required by this method. The Jacobian matrix has shape (n, n) and
        its element (i, j) is equal to ``d f_i / d y_j``.
        There are three ways to define the Jacobian:

            * If array_like or sparse_matrix, the Jacobian is assumed to
              be constant.
            * If callable, the Jacobian is assumed to depend on both
              t and y; it will be called as ``jac(t, y)`` as necessary.
              For the 'Radau' and 'BDF' methods, the return value might be a
              sparse matrix.
            * If None (default), the Jacobian will be approximated by
              finite differences.

        It is generally recommended to provide the Jacobian rather than
        relying on a finite-difference approximation.
    jac_sparsity : {None, array_like, sparse matrix}, optional
        Defines a sparsity structure of the Jacobian matrix for a
        finite-difference approximation. Its shape must be (n, n). This argument
        is ignored if `jac` is not `None`. If the Jacobian has only few non-zero
        elements in *each* row, providing the sparsity structure will greatly
        speed up the computations [2]_. A zero entry means that a corresponding
        element in the Jacobian is always zero. If None (default), the Jacobian
        is assumed to be dense.
    vectorized : bool, optional
        Whether `fun` is implemented in a vectorized fashion. Default is False.
    mass_matrix : {None, array_like, sparse_matrix}, optional
        Defined the constant mass matrix of the system, with shape (n,n).
        It may be singular, thus defining a problem of the differential-
        algebraic type (DAE), see [1]. The default value is None.

    Attributes
    ----------
    n : int
        Number of equations.
    status : string
        Current status of the solver: 'running', 'finished' or 'failed'.
    t_bound : float
        Boundary time.
    direction : float
        Integration direction: +1 or -1.
    t : float
        Current time.
    y : ndarray
        Current state.
    t_old : float
        Previous time. None if no steps were made yet.
    step_size : float
        Size of the last successful step. None if no steps were made yet.
    nfev : int
        Number of evaluations of the right-hand side.
    njev : int
        Number of evaluations of the Jacobian.
    nlu : int
        Number of LU decompositions.

    References
    ----------
    .. [1] E. Hairer, G. Wanner, "Solving Ordinary Differential Equations II:
           Stiff and Differential-Algebraic Problems", Sec. IV.8.
    .. [2] A. Curtis, M. J. D. Powell, and J. Reid, "On the estimation of
           sparse Jacobian matrices", Journal of the Institute of Mathematics
           and its Applications, 13, pp. 117-120, 1974.
    .. [3] J. de Swart, G. Söderlind, "On the construction of error estimators for 
           implicit Runge-Kutta methods", Journal of Computational and Applied 
           Mathematics, 86, pp. 347-358, 1997.
    .. [4] B. Fabien, "Analytical System Dynamics: Modeling and Simulation", 
           Sec. 5.3.5.
    """
    def __init__(self, fun, t0, y0, yp0, t_bound, max_step=np.inf,
                 rtol=1e-3, atol=1e-6, jac=None, jac_sparsity=None,
                 vectorized=False, first_step=None, **extraneous):
        warn_extraneous(extraneous)
        super().__init__(fun, t0, y0, yp0, t_bound, rtol, atol, first_step, max_step, vectorized, jac, jac_sparsity)
        self.y_old = None

        self.h_abs_old = None
        self.error_norm_old = None

        self.newton_tol = max(10 * EPS / rtol, min(0.03, rtol ** 0.5))
        self.sol = None

        self.current_jac = True
        self.LU_real = None
        self.LU_complex = None
        self.Z = None

    def _step_impl(self):
        t = self.t
        y = self.y
        yp = self.yp
        f = self.f

        max_step = self.max_step
        atol = self.atol
        rtol = self.rtol

        min_step = 10 * np.abs(np.nextafter(t, self.direction * np.inf) - t)
        if self.h_abs > max_step:
            h_abs = max_step
            h_abs_old = None
            error_norm_old = None
        elif self.h_abs < min_step:
            h_abs = min_step
            h_abs_old = None
            error_norm_old = None
        else:
            h_abs = self.h_abs
            h_abs_old = self.h_abs_old
            error_norm_old = self.error_norm_old

        Jy = self.Jy
        Jyp = self.Jyp
        LU_real = self.LU_real
        LU_complex = self.LU_complex

        current_jac = self.current_jac
        jac = self.jac

        step_accepted = False
        message = None
        while not step_accepted:
            if h_abs < min_step:
                return False, self.TOO_SMALL_STEP

            h = h_abs * self.direction
            t_new = t + h

            if self.direction * (t_new - self.t_bound) > 0:
                t_new = self.t_bound

            h = t_new - t
            h_abs = np.abs(h)

            if self.sol is None:
                Z0 = np.zeros((3, y.shape[0]))
            else:
                Z0 = self.sol(t + h * C).T - y

            scale = atol + np.abs(y) * rtol

            converged = False
            while not converged:
                if LU_real is None or LU_complex is None:
                    # Fabien (5.59) and (5.60)
                    LU_real = self.lu(MU_REAL / h * Jyp + Jy)
                    LU_complex = self.lu(MU_COMPLEX / h * Jyp + Jy)

                converged, n_iter, Y, Yp, Z, rate = solve_collocation_system(
                    self.fun, t, y, h, Z0, scale, self.newton_tol,
                    LU_real, LU_complex, self.solve_lu)

                if not converged:
                    if current_jac:
                        break

                    Jy, Jyp = self.jac(t, y, yp, f)
                    current_jac = True
                    LU_real = None
                    LU_complex = None

            if not converged:
                h_abs *= 0.5
                LU_real = None
                LU_complex = None
                continue

            # Hairer1996 (8.2b)
            # y_new = y + Z[-1]
            y_new = Y[-1]
            yp_new = Yp[-1]

            scale = atol + np.maximum(np.abs(y), np.abs(y_new)) * rtol

            if True:
                # # ######################################################
                # # # error estimate by difference w.r.t. embedded formula
                # # ######################################################
                # # # compute embedded formula
                # # gamma0 = MU_REAL
                # # y_new_hat = y + h * gamma0 * yp + h * b_hat @ Yp

                # # # # # embedded trapezoidal step
                # # # # y_new_hat = y + 0.5 * h * (yp + Yp[-1])

                # # # y_new = y + h * (b @ Yp)
                # # error = y_new_hat - y_new
                # # # # error = Yp.T.dot(E) + h * gamma0 * yp
                # # # error = gamma0 * Yp.T.dot(E) + h * yp

                # # # # ZE = Z.T.dot(E) #/ h
                # # # # error = (yp + Jyp.dot(ZE)) * h
                # # # # error = (yp + Z.T @ E / h)
                # # # # error = (yp + Z.T @ E) * h
                # # # # error = Jyp @ (yp + Z.T @ E) * h
                # # # # error = (f + Jyp.dot(ZE)) #* (h / MU_REAL)
                # # # # error = (h * yp + Yp.T @ (b_hat - b)) / h
                # # # error = (yp + Yp.T @ (b_hat - b) / h)
                # # # error = self.solve_lu(LU_real, error)
                # # # # error = self.solve_lu(LU_real, f + self.mass_matrix.dot(ZE))

                # # ###########################
                # # # decomposed error estimate
                # # ###########################
                # # gamma0h = MU_REAL * h

                # # # scale E by MU_real since this is already done by Hairer's 
                # # # E that is used here
                # # e = E * MU_REAL

                # # # embedded thirs order method
                # # err = gamma0h * yp + Z.T.dot(e)

                # # # use bad error estimate
                # # error = err

                # ###########################
                # # decomposed error estimate
                # ###########################
                # # gamma0 = 1 / MU_REAL
                # gamma0 = MU_REAL

                # # scale E by MU_real since this is already done by Hairer's 
                # # E that is used here
                # e = E * gamma0

                # # embedded third order method
                # err = h * gamma0 * yp + Z.T.dot(e)
                # # err = h * MU_REAL * yp + Jyp @ Z.T.dot(E * MU_REAL)
                # # err = h * gamma0 * (yp - f) + Z.T.dot(e)

                # # embedded third order method, see Fabien2009 (5.65)
                # b0_hat = 0.02
                # # gamma_hat = 1 / MU_REAL
                # # yp_hat_new = (MU_REAL / h) * (y_new - (y + h * Z.T.dot(E * MU_REAL)))
                # # yp_hat_new = MU_REAL * (Z.T.dot(E * MU_REAL) / h - b0_hat * yp_new)
                # yp_hat_new = MU_REAL * (Yp.T.dot(E * MU_REAL) - b0_hat * yp)
                # # yp_hat_new = -(Z.T.dot(E * MU_REAL) / h - b0_hat * yp) / MU_REAL
                # err = -self.solve_lu(LU_real, self.fun(t_new, y_new, yp_hat_new))
                # # err = -self.solve_lu(LU_real, self.fun(t_new, y_new, yp_new))

                # # LU_real = self.lu(MU_REAL / h * Jyp + Jy)

                # # use bad error estimate
                # error = err




                # ####################
                # # ODE error estimate
                # ####################
                # err_ODE = h * MU_REAL * (yp - f) + Z.T.dot(E * MU_REAL)
                # LU_real_ODE = self.lu(MU_REAL / h * self.I - Jy)
                # error_ODE = self.solve_lu(LU_real_ODE, err_ODE) / (MU_REAL * h)
                # # error = error_ODE

                #####################################
                # ODE with mass matrix error estimate
                #####################################
                # LU_real_ODE_mass = self.lu(MU_REAL / h * Jyp - Jy)
                # # Fabien (5.59) and (5.60)
                # LU_real = self.lu(MU_REAL / h * Jyp + Jy)
                LU_real_ODE_mass = LU_real
                # err_ODE_mass = h * MU_REAL * Jyp @ ((yp - f) + Z.T.dot(E * MU_REAL))
                # error_ODE_mass = self.solve_lu(LU_real_ODE_mass, err_ODE_mass) / (MU_REAL * h)
                error_ODE_mass = self.solve_lu(
                    LU_real_ODE_mass, 
                    Jyp @ ((yp - f) + Z.T.dot(E) / h),
                )
                error = error_ODE_mass
                
                # ###############
                # # Fabien (5.65)
                # ###############
                # b0_hat = 0.02
                # # b0_hat = 1 / MU_REAL # TODO: I prefer this...
                # gamma_hat = 1 / MU_REAL
                # yp_hat_new = (y_new - (y + h * b_hat @ Yp + h * b0_hat * yp)) / (h * gamma_hat)
                # yp_hat_new = MU_REAL * (b - b_hat) @ Yp - b0_hat * yp
                # # yp_hat_new = MU_REAL * ((b - b_hat) @ Yp - b0_hat * yp)
                # # # for b0_hat = 1 / MU_REAL this reduces to
                # # yp_hat_new = MU_REAL * (b - b_hat) @ Yp - yp
                # # yp_hat_new *= h
                # # print(f"yp_new:     {yp_new}")
                # # print(f"yp_hat_new: {yp_hat_new}")
                # # y_hat_new = y + h * b_hat @ Yp + h * b0_hat * yp + h * gamma_hat * yp_hat_new
                # # y_hat_new = y + h * b_hat @ Yp + h * b0_hat * yp + h * gamma_hat * yp_hat_new
                # # error = y_hat_new - y_new

                # error = np.zeros_like(y_new)

                # # F = self.fun(t_new, y_new, yp_hat_new)
                # F = self.fun(t_new, y_new, MU_REAL * (b - b_hat) @ Yp - b0_hat * yp)
                # # error = np.linalg.solve(Jy + Jyp / (h * gamma_hat), -F)
                # error = self.solve_lu(LU_real, -F)

                # yp_hat_new = MU_REAL * (b - b_hat) @ Yp - b0_hat * yp
                # F = self.fun(t_new, y_new, yp_hat_new)
                # error = self.solve_lu(LU_real, -F) #* (h * gamma_hat)
                # # y1 = Y((ride_data.s-1)*ride_data.n+1:ride_data.s*ride_data.n,1);
                # # t1 = t0+h;
                # # yp1 = ride_data.mu(1)*(kron(ride_data.v',eye(ride_data.n))*Yp - ride_data.b0*yp0);
                # # g = feval(IDEFUN,y1,yp1,t1);
                # # ride_data.nfun = ride_data.nfun + 1;
                # # r = -(ride_data.U\(ride_data.L\(ride_data.P*g)));

                # LU_real = self.lu(MU_REAL / h * Jyp + Jy)

                # error = -self.solve_lu(LU_real, self.fun(t_new, y_new, yp_hat_new))
                # print(f"error: {error}")
                # # error = -self.solve_lu(LU_real, self.fun(t_new, y_hat_new, yp_hat_new))

                
                error_norm = norm(error / scale)

                safety = 0.9 * (2 * NEWTON_MAXITER + 1) / (2 * NEWTON_MAXITER + n_iter)

                if error_norm > 1:
                    factor = predict_factor(h_abs, h_abs_old, error_norm, error_norm_old)
                    h_abs *= max(MIN_FACTOR, safety * factor)

                    LU_real = None
                    LU_complex = None
                else:
                    step_accepted = True
            else:
                step_accepted = True

        if True:
            # Step is converged and accepted
            # TODO: Make this rate a user defined argument
            recompute_jac = jac is not None and n_iter > 2 and rate > 1e-3

            factor = predict_factor(h_abs, h_abs_old, error_norm, error_norm_old)
            factor = min(MAX_FACTOR, safety * factor)

            if not recompute_jac and factor < 1.2:
                factor = 1
            else:
                LU_real = None
                LU_complex = None

            f_new = self.fun(t_new, y_new, yp_new)
            if recompute_jac:
                Jy, Jyp = self.jac(t_new, y_new, yp_new, f_new)
                current_jac = True
            elif jac is not None:
                current_jac = False

            self.h_abs_old = self.h_abs
            self.error_norm_old = error_norm

            self.h_abs = h_abs * factor

        f_new = self.fun(t_new, y_new, yp_new)

        self.y_old = y
        self.yp_old = yp

        self.t = t_new
        self.y = y_new
        self.yp = yp_new
        self.f = f_new

        self.Z = Z

        self.LU_real = LU_real
        self.LU_complex = LU_complex
        self.current_jac = current_jac
        self.Jy = Jy
        self.Jyp = Jyp

        self.t_old = t
        self.sol = self._compute_dense_output()

        return step_accepted, message

    def _compute_dense_output(self):
        Q = np.dot(self.Z.T, P)
        return RadauDenseOutput(self.t_old, self.t, self.y_old, Q)

    def _dense_output_impl(self):
        return self.sol

class RadauDenseOutput(DenseOutput):
    def __init__(self, t_old, t, y_old, Q):
        super().__init__(t_old, t)
        self.h = t - t_old
        self.Q = Q
        self.order = Q.shape[1] - 1
        self.y_old = y_old

    def _call_impl(self, t):
        x = (t - self.t_old) / self.h
        if t.ndim == 0:
            p = np.tile(x, self.order + 1)
            p = np.cumprod(p)
        else:
            p = np.tile(x, (self.order + 1, 1))
            p = np.cumprod(p, axis=0)
        # Here we don't multiply by h, not a mistake.
        y = np.dot(self.Q, p)
        if y.ndim == 2:
            y += self.y_old[:, None]
        else:
            y += self.y_old

        return y
