import base_svc
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
from sklearn.base import BaseEstimator

multi_method = {
    "ovo": OneVsOneClassifier,
    "ovr": OneVsRestClassifier,
}


class MultiLinearSVC(BaseEstimator):
    def __init__(self,
                 C=1,
                 max_iter=1000,
                 tol=1e-3,
                 verbose=False,
                 n_jobs=None,
                 method="ovo") -> None:
        super().__init__()
        self.max_iter = max_iter
        self.C = C
        self.tol = tol
        self.verbose = verbose
        self.n_jobs = n_jobs
        self.method = method

        self.base_model = base_svc.LinearSVC(C, max_iter, tol, verbose)

    def fit(self, X, y):
        self.multi_model = multi_method[self.method](
            estimator=self.base_model,
            n_jobs=self.n_jobs,
        )
        self.multi_model.fit(X, y)
        return self

    def predict(self, X):
        return self.multi_model.predict(X)

    def score(self, X, y):
        pred = self.predict(X)
        return (pred == y).mean(0)


class MultiKernelSVC(BaseEstimator):
    def __init__(self,
                 C=1,
                 max_iter=1000,
                 kernel='rbf',
                 degree=3,
                 gamma='scale',
                 coef0=0,
                 tol=1e-3,
                 verbose=False,
                 n_jobs=None,
                 method="ovo") -> None:
        super().__init__()
        self.C = C
        self.max_iter = 1000
        self.kernel = kernel
        self.gamma = gamma
        self.degree = degree
        self.coef0 = coef0
        self.tol = tol
        self.max_iter = max_iter
        self.verbose = verbose
        self.n_jobs = n_jobs
        self.method = method

        self.base_model = base_svc.KernelSVC(
            C,
            max_iter,
            kernel,
            degree,
            gamma,
            coef0,
            tol,
            verbose,
        )

    def fit(self, X, y):
        self.multi_model = multi_method[self.method](
            estimator=self.base_model,
            n_jobs=self.n_jobs,
        )
        self.multi_model.fit(X, y)
        return self

    def predict(self, X):
        return self.multi_model.predict(X)

    def score(self, X, y):
        pred = self.predict(X)
        return (pred == y).mean(0)


class MultiNuSVC(BaseEstimator):
    def __init__(
        self,
        nu=0.5,
        max_iter=1000,
        kernel='rbf',
        degree=3,
        gamma='scale',
        coef0=0,
        tol=1e-3,
        verbose=False,
        n_jobs=None,
        method="ovo",
    ) -> None:
        super().__init__()
        self.max_iter = max_iter
        self.nu = nu
        self.kernel = kernel
        self.gamma = gamma
        self.degree = degree
        self.coef0 = coef0
        self.tol = tol
        self.verbose = verbose
        self.n_jobs = n_jobs
        self.method = method
        self.base_model = base_svc.NuSVC(
            nu,
            max_iter,
            kernel,
            degree,
            gamma,
            coef0,
            tol,
            verbose,
        )

    def fit(self, X, y):
        self.multi_model = multi_method[self.method](
            estimator=self.base_model,
            n_jobs=self.n_jobs,
        )
        self.multi_model.fit(X, y)
        return self

    def predict(self, X):
        return self.multi_model.predict(X)

    def score(self, X, y):
        pred = self.predict(X)
        return (pred == y).mean(0)


LinearSVC = MultiLinearSVC
KernelSVC = MultiKernelSVC
NuSVC = MultiKernelSVC
