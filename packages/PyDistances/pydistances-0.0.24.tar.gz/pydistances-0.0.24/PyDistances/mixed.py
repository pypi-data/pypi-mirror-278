import polars as pl
import numpy as np
import pandas as pd
from PyDistances.quantitative import Euclidean_dist_matrix, Euclidean_dist, Minkowski_dist_matrix, Minkowski_dist, Canberra_dist_matrix, Canberra_dist, Pearson_dist_matrix, Mahalanobis_dist_matrix, Mahalanobis_dist, Robust_Maha_dist_matrix, Robust_Maha_dist, S_robust
from PyDistances.binary import  Sokal_dist_matrix, Sokal_dist, Jaccard_dist_matrix, Jaccard_dist
from PyDistances.multiclass import Matching_dist_matrix, Matching_dist

################################################################################

dist_functions = dict()
dist_functions['euclidean'] = Euclidean_dist_matrix
dist_functions['minkowski'] = Minkowski_dist_matrix
dist_functions['canberra'] = Canberra_dist_matrix
dist_functions['pearson'] = Pearson_dist_matrix
dist_functions['mahalanobis'] = Mahalanobis_dist_matrix
dist_functions['robust_mahalanobis'] = Robust_Maha_dist_matrix
dist_functions['sokal'] = Sokal_dist_matrix
dist_functions['jaccard'] = Jaccard_dist_matrix
dist_functions['matching'] = Matching_dist_matrix

################################################################################

dist_funtions_obs = dict()
dist_funtions_obs['euclidean'] = Euclidean_dist
dist_funtions_obs['minkowski'] = Minkowski_dist
dist_funtions_obs['canberra'] = Canberra_dist
dist_funtions_obs['mahalanobis'] = Mahalanobis_dist
dist_funtions_obs['robust_mahalanobis'] = Robust_Maha_dist
dist_funtions_obs['sokal'] = Sokal_dist
dist_funtions_obs['jaccard'] = Jaccard_dist
dist_funtions_obs['matching'] = Matching_dist

################################################################################

def VG(D_2):
    """
    Calculates the geometric variability of the squared distance matrix `D_2` passed as input.

    Parameters (inputs)
    ----------
    D_2: a numpy array. It should represent an squared distance matrix.

    Returns (outputs)
    -------
    VG: the geometric variability of the squared distance matrix `D_2`.
    """
    n = len(D_2)
    VG = (1/(2*(n**2)))*np.sum(D_2)
    return VG

################################################################################

class get_dist_matrices:
    """
    Calculates the distance matrices that are involved in the Generalized Gower distance.
    """

    def __init__(self, p1, p2, p3, d1='euclidean', d2='sokal', d3='matching', q=1, method='trimmed', epsilon=0.05, alpha=0.05, n_iters=20, weights=None):
        """
        Constructor method.
        
        Parameters:
            p1, p2, p3: number of quantitative, binary and multi-class variables in the considered data matrix, respectively. Must be a non negative integer.
            d1: name of the distance to be computed for quantitative variables. Must be an string in ['euclidean', 'minkowski', 'canberra', 'mahalanobis', 'robust_mahalanobis']. 
            d2: name of the distance to be computed for binary variables. Must be an string in ['sokal', 'jaccard'].
            d3: name of the distance to be computed for multi-class variables. Must be an string in ['matching'].
            q: the parameter that defines the Minkowski distance. Must be a positive integer.
            method: the method to be used for computing the robust covariance matrix. Only needed when d1 = 'robust_mahalanobis'.
            epsilon: parameter used by the Delvin algorithm that is used when computing the robust covariance matrix. Only needed when d1 = 'robust_mahalanobis'.
            n_iter: maximum number of iterations used by the Delvin algorithm. Only needed when d1 = 'robust_mahalanobis'.
            weights: the sample weights.
        """        
        self.p1 = p1 ; self.p2 = p2 ; self.p3 = p3
        self.d1 = d1 ; self.d2 = d2 ; self.d3 = d3
        self.q = q ; self.method = method ; self.alpha = alpha ; 
        self.epsilon = epsilon ; self.n_iters = n_iters ; self.weights = weights

    def compute(self, X):
        """
        Compute method.
        
        Parameters:
            X: a pandas/polars data-frame or a numpy array. Represents a data matrix.
            
        Returns:
            D1, D2, D3: the distances matrices associated to the quantitative, binary and multi-class variables, respectively.
        """
        d1 = self.d1 ; d2 = self.d2 ; d3 = self.d3
        p1 = self.p1 ; p2 = self.p2 ; p3 = self.p3

        if isinstance(X, pl.DataFrame):
            X = X.to_numpy()
        elif isinstance(X, pd.DataFrame):
            X = X.to_numpy() 

        n = len(X)
        X_quant = X[:, 0:p1] 
        X_bin = X[:, (p1):(p1+p2)]
        X_multi = X[:, (p1+p2):(p1+p2+p3)]

        # Define D1 based on d1 and p1
        if p1 > 0:
            if d1 == 'minkowski':
                D1 = dist_functions[d1](X_quant, self.q)
            elif d1 == 'robust_mahalanobis':
                S_robust_ = S_robust(X=X_quant, method=self.method, alpha=self.alpha,
                                     epsilon=self.epsilon, n_iters=self.n_iters, weights=self.weights)
                D1 = dist_functions[d1](X_quant, S_robust=S_robust_)
            else:
                D1 = dist_functions[d1](X_quant)
        elif p1 == 0:
            D1 = np.zeros((n, n))
        # Define D2 based on p2
        D2 = dist_functions[d2](X_bin) if p2 > 0 else np.zeros((n, n)) 
        # Define D3 based on p3
        D3 = dist_functions[d3](X_multi) if p3 > 0 else np.zeros((n, n))

        return D1, D2, D3
    
class get_dist_obs:
    """
    Calculates the distance between observations that are involved in the Generalized Gower distance.
    """

    def __init__(self, p1, p2, p3, d1='euclidean', d2='sokal', d3='matching', q=1, S=None, S_robust=None):
        """
        Constructor method.
        
        Parameters:
            p1, p2, p3: number of quantitative, binary and multi-class variables in the considered data matrix, respectively. Must be a non negative integer.
            d1: name of the distance to be computed for quantitative variables. Must be an string in ['euclidean', 'minkowski', 'canberra', 'mahalanobis', 'robust_mahalanobis']. 
            d2: name of the distance to be computed for binary variables. Must be an string in ['sokal', 'jaccard'].
            d3: name of the distance to be computed for multi-class variables. Must be an string in ['matching'].
            q: the parameter that defines the Minkowski distance. Must be a positive integer.
            S: the covariance matrix of the considered data matrix.
            S_robust: the robust covariance matrix of the considered data matrix.
        """  
        self.p1 = p1 ; self.p2 = p2 ; self.p3 = p3
        self.d1 = d1 ; self.d2 = d2 ; self.d3 = d3
        self.q = q ; self.S = S ; self.S_robust = S_robust 

    def compute(self, xi, xr):    
        """
        Compute method.
        
        Parameters:
            xi, xr: a pair of quantitative vectors. They represent a couple of statistical observations.
            
        Returns:
            dist1, dist2, dist3: the distances values associated to the quantitative, binary and multi-class observations, respectively.
        """

        if isinstance(xi, (pl.DataFrame, pd.DataFrame)) :
            xi = xi.to_numpy().flatten()
        elif isinstance(xi, (pd.Series, pl.Series)) :
            xi = xi.to_numpy() 
        if isinstance(xr, (pl.DataFrame, pd.DataFrame)) :
            xr = xr.to_numpy().flatten()
        elif isinstance(xr, (pd.Series, pl.Series)) :
            xr = xr.to_numpy() 
        
        d1 = self.d1 ; d2 = self.d2 ; d3 = self.d3
        p1 = self.p1 ; p2 = self.p2 ; p3 = self.p3   
           
        xi_quant = xi[0:p1] ; xr_quant = xr[0:p1] ; 
        xi_bin = xi[(p1):(p1+p2)] ; xr_bin = xr[(p1):(p1+p2)]
        xi_multi = xi[(p1+p2):(p1+p2+p3)] ; xr_multi = xr[(p1+p2):(p1+p2+p3)]

        if p1 > 0:
            if d1 == 'minkowski':
                dist1 = dist_funtions_obs[d1](xi_quant, xr_quant, q=self.q)
            elif d1 == 'robust_mahalanobis':
                dist1 = dist_funtions_obs[d1](xi_quant, xr_quant, S_robust=self.S_robust)
            elif d1 == 'mahalanobis':
                dist1 = dist_funtions_obs[d1](xi_quant, xr_quant, S=self.S)
            else:
                dist1 = dist_funtions_obs[d1](xi_quant, xr_quant)
        elif p1 == 0:
            dist1 = 0

        dist2 = dist_funtions_obs[d2](xi_bin, xr_bin) if p2 > 0 else 0
        dist3 = dist_funtions_obs[d3](xi_multi, xr_multi) if p3 > 0 else 0

        return dist1, dist2, dist3
    
################################################################################
class VG_GG_Estimation: 
    """
    Calculates the geometric variability of an Generalized Gower distance matrix.
    """

    def __init__(self, p1, p2, p3, d1='euclidean', d2='sokal', d3='matching', q=1, method='trimmed', 
                 epsilon=0.05, alpha=0.05, n_iters=20, weights=None):
        """
        Constructor method.
        
        Parameters:
            p1, p2, p3: number of quantitative, binary and multi-class variables in the considered data matrix, respectively. Must be a non negative integer.
            d1: name of the distance to be computed for quantitative variables. Must be an string in ['euclidean', 'minkowski', 'canberra', 'mahalanobis', 'robust_mahalanobis']. 
            d2: name of the distance to be computed for binary variables. Must be an string in ['sokal', 'jaccard'].
            d3: name of the distance to be computed for multi-class variables. Must be an string in ['matching'].
            q: the parameter that defines the Minkowski distance. Must be a positive integer.
            method: the method to be used for computing the robust covariance matrix. Only needed when d1 = 'robust_mahalanobis'.
            epsilon: parameter used by the Delvin algorithm that is used when computing the robust covariance matrix. Only needed when d1 = 'robust_mahalanobis'.
            n_iter: maximum number of iterations used by the Delvin algorithm. Only needed when d1 = 'robust_mahalanobis'.
            weights: the sample weights.
        """
        self.p1 = p1 ; self.p2 = p2 ; self.p3 = p3
        self.d1 = d1 ; self.d2 = d2 ; self.d3 = d3
        self.q = q ; self.method = method ; self.alpha = alpha ; 
        self.epsilon = epsilon ; self.n_iters = n_iters ; self.weights = weights

    def compute(self, X):
        """
        Compute method.
        
        Parameters:
            X: a pandas/polars data-frame or a numpy array. Represents a data matrix.
            
        Returns:
            VG1, VG2, VG3: the geometric variabilities of the distances matrices associated to the quantitative, binary and multi-class variables, respectively.
        """

        get_dist_matrices_ = get_dist_matrices(p1=self.p1, p2=self.p2, p3=self.p3, 
                                               d1=self.d1, d2=self.d2, d3=self.d3, 
                                               q=self.q, method=self.method, epsilon=self.epsilon, 
                                               alpha=self.alpha, n_iters=self.n_iters, weights=self.weights)
       
        D1, D2, D3 = get_dist_matrices_.compute(X=X)
        D1_2, D2_2, D3_2 = D1**2, D2**2, D3**2
        VG1, VG2, VG3 = VG(D1_2), VG(D2_2), VG(D3_2)

        return VG1, VG2, VG3

################################################################################

class VG_GG_Fast_Estimation :
    """
    Calculates a fast estimation of the geometric variability of an squared Generalized Gower distance matrix.
    """

    def __init__(self, p1, p2, p3, d1='euclidean', d2='sokal', d3='matching', method='trimmed', epsilon=0.05, alpha=0.05, n_iters=20, q=1,
                 VG_sample_size=300, VG_n_samples=5, random_state=123, weights=None):
        """
        Constructor method.
        
        Parameters:
            p1, p2, p3: number of quantitative, binary and multi-class variables in the considered data matrix, respectively. Must be a non negative integer.
            d1: name of the distance to be computed for quantitative variables. Must be an string in ['euclidean', 'minkowski', 'canberra', 'mahalanobis', 'robust_mahalanobis']. 
            d2: name of the distance to be computed for binary variables. Must be an string in ['sokal', 'jaccard'].
            d3: name of the distance to be computed for multi-class variables. Must be an string in ['matching'].
            q: the parameter that defines the Minkowski distance. Must be a positive integer.
            method: the method to be used for computing the robust covariance matrix. Only needed when d1 = 'robust_mahalanobis'.
            epsilon: parameter used by the Delvin algorithm that is used when computing the robust covariance matrix. Only needed when d1 = 'robust_mahalanobis'.
            n_iter: maximum number of iterations used by the Delvin algorithm. Only needed when d1 = 'robust_mahalanobis'.
            weights: the sample weights.
            VG_sample_size: sample size to be used to make the estimation of the geometric variability.
            VG_n_samples: number of samples to be used to make the estimation of the geometric variability.
            random_state: the random seed used for the (random) sample elements.
        """
        self.p1 = p1 ; self.p2 = p2 ; self.p3 = p3
        self.d1 = d1 ; self.d2 = d2 ; self.d3 = d3
        self.q = q ; self.method = method ; self.alpha = alpha ; 
        self.epsilon = epsilon ; self.n_iters = n_iters
        self.VG_sample_size = VG_sample_size; self.VG_n_samples = VG_n_samples
        self.random_state = random_state; self.weights = weights

    def compute(self, X):
        """
        Compute method.
        
        Parameters:
            X: a pandas/polars data-frame or a numpy array. Represents a data matrix.
            
        Returns:
            VG1, VG2, VG3: the geometric variabilities of the distances matrices associated to the quantitative, binary and multi-class variables, respectively.
        """

        if isinstance(X, (pl.DataFrame, pd.DataFrame)) :
            X = X.to_numpy()  
        
        n = len(X)
        VG1_list, VG2_list, VG3_list = [], [], []

        for i in range(0, self.VG_n_samples) :

            np.random.seed(self.random_state + i)
            index = np.arange(0,n)
            sample_index = np.random.choice(index, size=self.VG_sample_size)
            X_sample = X[sample_index,:].copy()
            
            if self.weights is not None:
                sample_weights = self.weights[sample_index].copy() 
            else:
                sample_weights = None
            
            VG_GG_fast = VG_GG_Estimation(p1=self.p1, p2=self.p2, p3=self.p3, 
                                          d1=self.d1, d2=self.d2, d3=self.d3, q=self.q,
                                          method=self.method, epsilon=self.epsilon, alpha=self.alpha, 
                                          n_iters=self.n_iters, weights=sample_weights)
            
            VG1, VG2, VG3 = VG_GG_fast.compute(X=X_sample)
            VG1_list.append(VG1) ; VG2_list.append(VG2) ; VG3_list.append(VG3) 

        VG1 = np.mean(VG1_list) ; VG2 = np.mean(VG2_list) ; VG3 = np.mean(VG3_list)

        return VG1, VG2, VG3

################################################################################
    
class GG_dist_matrix: 
    """
    Calculates the Generalized Gower matrix for a data matrix.
    """

    def __init__(self, p1, p2, p3, d1='euclidean', d2='sokal', d3='matching', q=1, method='trimmed', epsilon=0.05, alpha=0.05, n_iters=20,
                 fast_VG=False, VG_sample_size=300, VG_n_samples=5, random_state=123, weights=None):
        """
        Constructor method.
        
        Parameters:
            p1, p2, p3: number of quantitative, binary and multi-class variables in the considered data matrix, respectively. Must be a non negative integer.
            d1: name of the distance to be computed for quantitative variables. Must be an string in ['euclidean', 'minkowski', 'canberra', 'mahalanobis', 'robust_mahalanobis']. 
            d2: name of the distance to be computed for binary variables. Must be an string in ['sokal', 'jaccard'].
            d3: name of the distance to be computed for multi-class variables. Must be an string in ['matching'].
            q: the parameter that defines the Minkowski distance. Must be a positive integer.
            method: the method to be used for computing the robust covariance matrix. Only needed when d1 = 'robust_mahalanobis'.
            alpha : a real number in [0,1] that is used if `method` is 'trimmed' or 'winsorized'. Only needed when d1 = 'robust_mahalanobis'.
            epsilon : parameter used by the Delvin transformation. epsilon=0.05 is recommended. Only needed when d1 = 'robust_mahalanobis'.
            n_iter : maximum number of iterations run by the Delvin algorithm. Only needed when d1 = 'robust_mahalanobis'.
            weights: the sample weights.
            fast_VG: whether the geometric variability estimation will be full (False) or fast (True).
            VG_sample_size: sample size to be used to make the estimation of the geometric variability.
            VG_n_samples: number of samples to be used to make the estimation of the geometric variability.
            random_state: the random seed used for the (random) sample elements.
        """
        self.p1 = p1 ; self.p2 = p2 ; self.p3 = p3
        self.d1 = d1 ; self.d2 = d2 ; self.d3 = d3
        self.q = q ; self.method = method ; self.alpha = alpha ; 
        self.epsilon = epsilon ; self.n_iters = n_iters
        self.VG_sample_size = VG_sample_size; self.VG_n_samples = VG_n_samples
        self.random_state = random_state ; self.fast_VG = fast_VG; self.weights = weights

    def compute(self, X):
        """
        Compute method.
        
        Parameters:
            X: a pandas/polars data-frame or a numpy array. Represents a data matrix.
            
        Returns:
            D: the Generalized Gower matrix for the data matrix `X`.
        """

        get_dist_matrices_ = get_dist_matrices(p1=self.p1, p2=self.p2, p3=self.p3, 
                                               d1=self.d1, d2=self.d2, d3=self.d3, 
                                               q=self.q, method=self.method, epsilon=self.epsilon, 
                                               alpha=self.alpha, n_iters=self.n_iters, weights=self.weights)
     
        D1, D2, D3 = get_dist_matrices_.compute(X=X)        
        D1_2 = D1**2  ; D2_2 = D2**2 ; D3_2 = D3**2

        if self.fast_VG == True:   
            VG_GG_fast = VG_GG_Fast_Estimation(p1=self.p1, p2=self.p2, p3=self.p3, 
                                               d1=self.d1, d2=self.d2, d3=self.d3, 
                                               method=self.method, alpha=self.alpha,
                                               VG_sample_size=self.VG_sample_size, VG_n_samples=self.VG_n_samples, 
                                               random_state=self.random_state, weights=self.weights)
            VG1, VG2, VG3 = VG_GG_fast.compute(X=X)
        else:
            VG1, VG2, VG3 = VG(D1_2), VG(D2_2), VG(D3_2)

        D1_std = D1_2/VG1 if VG1 > 0 else D1_2 
        D2_std = D2_2/VG2 if VG2 > 0 else D2_2 
        D3_std = D3_2/VG3 if VG3 > 0 else D3_2
        D_2 = D1_std + D2_std + D3_std
        D = np.sqrt(D_2)

        return D 

################################################################################
    
class GG_dist: 
    """
    Calculates the Generalized Gower distance for a pair of data observations.
    """

    def __init__(self, p1, p2, p3, d1='euclidean', d2='sokal', d3='matching', q=1, method='trimmed', alpha=0.05, epsilon=0.05, n_iters=20,
                 VG_sample_size=300, VG_n_samples=5, random_state=123, weights=None):
        """
        Constructor method.
        
        Parameters:
            p1, p2, p3: number of quantitative, binary and multi-class variables in the considered data matrix, respectively. Must be a non negative integer.
            d1: name of the distance to be computed for quantitative variables. Must be an string in ['euclidean', 'minkowski', 'canberra', 'mahalanobis', 'robust_mahalanobis']. 
            d2: name of the distance to be computed for binary variables. Must be an string in ['sokal', 'jaccard'].
            d3: name of the distance to be computed for multi-class variables. Must be an string in ['matching'].
            q: the parameter that defines the Minkowski distance. Must be a positive integer.
            method: the method to be used for computing the robust covariance matrix. Only needed when d1 = 'robust_mahalanobis'.
            epsilon: parameter used by the Delvin algorithm that is used when computing the robust covariance matrix. Only needed when d1 = 'robust_mahalanobis'.
            n_iter: maximum number of iterations used by the Delvin algorithm. Only needed when d1 = 'robust_mahalanobis'.
            weights: the sample weights.
            VG_sample_size: sample size to be used to make the estimation of the geometric variability.
            VG_n_samples: number of samples to be used to make the estimation of the geometric variability.
            random_state: the random seed used for the (random) sample elements.
        """
        self.p1 = p1 ; self.p2 = p2 ; self.p3 = p3
        self.d1 = d1 ; self.d2 = d2 ; self.d3 = d3
        self.q = q ; self.method = method ; self.alpha = alpha ; 
        self.epsilon = epsilon ; self.n_iters = n_iters
        self.VG_sample_size = VG_sample_size; self.VG_n_samples = VG_n_samples
        self.random_state = random_state; self.weights = weights

    def fit(self, X) :
        """
        Fit method that computes the geometric variability and (robust) covariance matrix to be used in the Compute method if needed.
        
        Parameters:
            X: a pandas/polars data-frame or a numpy array. Represents a data matrix.
            
        Returns:
            D: the Generalized Gower matrix for the data matrix `X`.
        """
        p1 = self.p1 ; p2 = self.p2 ; p3 = self.p3
        d1 = self.d1 ; d2 = self.d2 ; d3 = self.d3
        self.S, self.S_robust = None, None

        if d1 in ['robust_mahalanobis', 'mahalanobis']:

            if X is None: 
                raise ValueError('X is required if  d1=\'robust_mahalanobis\' or d1=\'mahalanobis\'') 
            else:
                if isinstance(X, (pl.DataFrame, pd.DataFrame)) :
                   X = X.to_numpy()
                X_quant = X[:, 0:p1] 

                if d1 == 'robust_mahalanobis':
                    self.S_robust = S_robust(X=X_quant, method=self.method, alpha=self.alpha, 
                                              epsilon=self.epsilon, n_iters=self.n_iters, weights=self.weights)
                elif d1 == 'mahalanobis':
                    self.S = np.cov(X_quant, rowvar=False)

        VG_GG_fast = VG_GG_Fast_Estimation(p1=p1, p2=p2, p3=p3, d1=d1, d2=d2, d3=d3, method=self.method, 
                                           alpha=self.alpha, epsilon=self.epsilon, n_iters=self.n_iters,
                                           VG_sample_size=self.VG_sample_size, VG_n_samples=self.VG_n_samples, 
                                           random_state=self.random_state, weights=self.weights)
        
        self.VG1, self.VG2, self.VG3 = VG_GG_fast.compute(X=X)

    def compute(self, xi, xr):
        """
        Compute method.
        
        Parameters:
            xi, xr: a pair of quantitative vectors. They represent a couple of statistical observations.
            
        Returns:
            dist: the Generalized Gower distance between the observations `xi` and `xr`.
        """
        get_dist_obs_ = get_dist_obs(p1=self.p1, p2=self.p2, p3=self.p3, 
                                     d1=self.d1, d2=self.d2, d3=self.d3, 
                                     q=self.q, S=self.S, S_robust=self.S_robust)
        
        dist1, dist2, dist3 = get_dist_obs_.compute(xi=xi, xr=xr)
        dist1_2 = dist1**2 ; dist2_2 = dist2**2 ; dist3_2 = dist3**2
        dist1_2_std = dist1_2/self.VG1 if self.VG1 > 0 else dist1_2 
        dist2_2_std = dist2_2/self.VG2 if self.VG2 > 0 else dist2_2 
        dist3_2_std = dist3_2/self.VG3 if self.VG3 > 0 else dist3_2 
        dist_2 = dist1_2_std + dist2_2_std + dist3_2_std
        dist = np.sqrt(dist_2)

        return dist
    
################################################################################
    
def Simple_Gower_dist(xi, xr, X, p1, p2, p3) :
    """
    Compute method.
    
    Parameters:
        xi, xr: a pair of quantitative vectors. They represent a couple of statistical observations.
        X: a pandas/polars data-frame or a numpy array. It represents a data matrix.
        p1, p2, p3: number of quantitative, binary and multi-class variables in the considered data matrix, respectively. Must be a non negative integer.

    Returns:
        dist: the Simple Gower distance between the observations `xi` and `xr`.
    """    

    if isinstance(X, (pl.DataFrame, pd.DataFrame)) :
        X = X.to_numpy()  
    if isinstance(xi, (pl.DataFrame, pd.DataFrame)) :
        xi = xi.to_numpy().flatten()
    elif isinstance(xi, (pd.Series, pl.Series)) :
        xi = xi.to_numpy() 
    if isinstance(xr, (pl.DataFrame, pd.DataFrame)) :
        xr = xr.to_numpy().flatten()
    elif isinstance(xi, (pd.Series, pl.Series)) :
        xr = xr.to_numpy() 
    
    X_quant = X[:,0:p1]  
    xi_quant = xi[0:p1] ; xr_quant = xr[0:p1] ; 
    xi_bin = xi[(p1):(p1+p2)] ; xr_bin = xr[(p1):(p1+p2)]
    xi_multi = xi[(p1+p2):(p1+p2+p3)] ; xr_multi = xr[(p1+p2):(p1+p2+p3)]
    R = np.max(X_quant, axis=0) - np.min(X_quant, axis=0)

    dist1 = np.sum(np.abs(xi_quant - xr_quant)/R) if p1 > 0 else 0
    dist2 = Jaccard_dist(xi_bin, xr_bin) if p2 > 0 else 0
    dist3 = Matching_dist(xi_multi, xr_multi) if p3 > 0 else 0
    dist = dist1 + dist2 + dist3

    return dist
    
################################################################################
    
class RelMS_dist_matrix: 
    """
    Calculates the Related Metric Scaling matrix for a data matrix.
    """

    def __init__(self, p1,p2,p3,d1='euclidean',d2='sokal',d3='matching',q=1, method='trimmed', 
                 epsilon=0.05, alpha=0.05, n_iters=20, weights=None, fast_VG=False):
        """
        Constructor method.
        
        Parameters:
            p1, p2, p3: number of quantitative, binary and multi-class variables in the considered data matrix, respectively. Must be a non negative integer.
            d1: name of the distance to be computed for quantitative variables. Must be an string in ['euclidean', 'minkowski', 'canberra', 'mahalanobis', 'robust_mahalanobis']. 
            d2: name of the distance to be computed for binary variables. Must be an string in ['sokal', 'jaccard'].
            d3: name of the distance to be computed for multi-class variables. Must be an string in ['matching'].
            q: the parameter that defines the Minkowski distance. Must be a positive integer.
            method: the method to be used for computing the robust covariance matrix. Only needed when d1 = 'robust_mahalanobis'.
            epsilon: parameter used by the Delvin algorithm that is used when computing the robust covariance matrix. Only needed when d1 = 'robust_mahalanobis'.
            n_iter: maximum number of iterations used by the Delvin algorithm. Only needed when d1 = 'robust_mahalanobis'.
            weights: the sample weights.
        """
        self.p1 = p1 ; self.p2 = p2 ; self.p3 = p3
        self.d1 = d1 ; self.d2 = d2 ; self.d3 = d3
        self.q = q ; self.method = method ; self.alpha = alpha ; self.fast_VG = fast_VG;
        self.epsilon = epsilon ; self.n_iters = n_iters ; self.weights = weights


    def compute(self, X, tol=0.009, d=2, Gs_PSD_trans=True):
        """
        Compute method.
        
        Parameters:
            X: a pandas/polars data-frame or a numpy array. Represents a data matrix.
            tol: a tolerance value to round the close-to-zero eigenvalues of the Gramm matrices.
            Gs_PSD_trans: controls if a transformation is applied to enforce positive semi-definite Gramm matrices.
            d: a parameter that controls the omega definition involved in the transformation mentioned above.
            
        Returns:
            D: the Related Metric Scaling matrix for the data matrix `X`.
        """
        get_dist_matrices_ = get_dist_matrices(p1=self.p1, p2=self.p2, p3=self.p3, 
                                               d1=self.d1, d2=self.d2, d3=self.d3, 
                                               q=self.q, method=self.method, epsilon=self.epsilon, 
                                               alpha=self.alpha, n_iters=self.n_iters, weights=self.weights)
       
        D1, D2, D3 = get_dist_matrices_.compute(X=X)        
        D1_2 = D1**2  ; D2_2 = D2**2 ; D3_2 = D3**2

        if self.fast_VG == True:   
            VG_GG_fast = VG_GG_Fast_Estimation(p1=self.p1, p2=self.p2, p3=self.p3, 
                                               d1=self.d1, d2=self.d2, d3=self.d3, 
                                               method=self.method, alpha=self.alpha,
                                               VG_sample_size=self.VG_sample_size, VG_n_samples=self.VG_n_samples, 
                                               random_state=self.random_state, weights=self.weights)
            VG1, VG2, VG3 = VG_GG_fast.compute(X=X)
        else:
            VG1, VG2, VG3 = VG(D1_2), VG(D2_2), VG(D3_2)

        D1_std = D1_2/VG1 if VG1 > 0 else D1_2 
        D2_std = D2_2/VG2 if VG2 > 0 else D2_2 
        D3_std = D3_2/VG3 if VG3 > 0 else D3_2
 
        n = len(D1)
        ones = np.ones((n, 1)) 
        ones_T = np.ones((1, n))
        ones_M = np.ones((n, n))
        I = np.identity(n)
        H = I - (1/n)*(ones @ ones_T)
        G_1 = -(1/2)*(H @ D1_std @ H)
        G_2 = -(1/2)*(H @ D2_std @ H) 
        G_3 = -(1/2)*(H @ D3_std @ H)

        if Gs_PSD_trans == True :

            v1 = np.real(np.linalg.eigvals(G_1))
            v2 = np.real(np.linalg.eigvals(G_2))
            v3 = np.real(np.linalg.eigvals(G_3))
            v1[np.isclose(v1, 0, atol=tol)] = 0 
            v2[np.isclose(v2, 0, atol=tol)] = 0 
            v3[np.isclose(v3, 0, atol=tol)] = 0
            G1_SDP = np.all(v1 >= 0)
            G2_SDP = np.all(v2 >= 0) 
            G3_SDP = np.all(v3 >= 0)

            if not G1_SDP :

                omega = d*np.abs(np.min(v1))  
                D1_std  = D1_std + omega*ones_M - omega*I
                G_1 = -(1/2)*(H @ D1_std @ H)

            elif not G2_SDP :

                omega = d*np.abs(np.min(v2)) 
                D2_std = D2_std + omega*ones_M - omega*I
                G_2 = -(1/2)*(H @ D2_std @ H)

            elif not G3_SDP :

                omega = d*np.abs(np.min(v3))  
                D3_std = D3_std + omega*ones_M - omega*I
                G_3 = -(1/2)*(H @ D3_std @ H) 
        
        U1, S1, V1 = np.linalg.svd(G_1) 
        U2, S2, V2 = np.linalg.svd(G_2)   
        U3, S3, V3 = np.linalg.svd(G_3)
        sqrtG1 = U1 @ np.diag(np.sqrt(S1)) @ V1 
        sqrtG2 = U2 @ np.diag(np.sqrt(S2)) @ V2 
        sqrtG3 = U3 @ np.diag(np.sqrt(S3)) @ V3

        G = G_1 + G_2 + G_3 - (1/3)*(sqrtG1@sqrtG2 + sqrtG1@sqrtG3 + sqrtG2@sqrtG1 + sqrtG2@sqrtG3 + sqrtG3@sqrtG1 + sqrtG3@sqrtG2)
        g = np.diag(G) 
        g =  np.reshape(g, (len(g), 1))  
        g_T = np.reshape(g, (1, len(g)))   
        D_2_ = g @ ones_T + ones @ g_T - 2*G
        D_2_[np.isclose(D_2_, 0, atol=0.001)] = 0
        D = np.sqrt(D_2_)
 
        return D    

################################################################################