import numpy as np
import pandas as pd
import sys
from sklearn.base import BaseEstimator, RegressorMixin, ClusterMixin
from sklearn.cluster import KMeans, MiniBatchKMeans
from FastKmedoids.models import FastKmedoidsGG, KFoldFastKmedoidsGG
from PyDistances.quantitative import Euclidean_dist

#####################################################################################################################

class FastKmedoidsEstimator(BaseEstimator, RegressorMixin) :
    """
    Implements the Fast-K-medoids-Estimator based on Fast-K-medoids and Sklearn estimators.
    """

    def __init__(self, estimators, n_clusters, method='pam', init='heuristic', max_iter=100, random_state=123,
                    frac_sample_size=0.1, p1=None, p2=None, p3=None, d1='robust_mahalanobis', d2='jaccard', d3='matching', 
                    robust_maha_method='trimmed', alpha=0.05, epsilon=0.05, n_iters=20, q=1,
                    fast_VG=False, VG_sample_size=1000, VG_n_samples=5, y_type=None) :
        """
        Constructor method.
        
        Parameters:
            estimators: a dictionary with the sklearn estimators (single models or pipelines) to be used in each clusters (keys: cluster indexes, values: estimators initialized).
            n_clusters: the number of clusters.
            method: the k-medoids clustering method. Must be in ['pam', 'alternate']. PAM is the classic one, more accurate but slower.
            init: the k-medoids initialization method. Must be in ['heuristic', 'random']. Heuristic is the classic one, smarter burt slower.
            max_iter: the maximum number of iterations run by k-medodis.
            frac_sample_size: the sample size in proportional terms.
            p1, p2, p3: number of quantitative, binary and multi-class variables in the considered data matrix, respectively. Must be a non negative integer.
            d1: name of the distance to be computed for quantitative variables. Must be an string in ['euclidean', 'minkowski', 'canberra', 'mahalanobis', 'robust_mahalanobis']. 
            d2: name of the distance to be computed for binary variables. Must be an string in ['sokal', 'jaccard'].
            d3: name of the distance to be computed for multi-class variables. Must be an string in ['matching'].
            q: the parameter that defines the Minkowski distance. Must be a positive integer.
            robust_maha_method: the method to be used for computing the robust covariance matrix. Only needed when d1 = 'robust_mahalanobis'.
            alpha : a real number in [0,1] that is used if `method` is 'trimmed' or 'winsorized'. Only needed when d1 = 'robust_mahalanobis'.
            epsilon: parameter used by the Delvin algorithm that is used when computing the robust covariance matrix. Only needed when d1 = 'robust_mahalanobis'.
            n_iters: maximum number of iterations used by the Delvin algorithm. Only needed when d1 = 'robust_mahalanobis'.
            fast_VG: whether the geometric variability estimation will be full (False) or fast (True).
            VG_sample_size: sample size to be used to make the estimation of the geometric variability.
            VG_n_samples: number of samples to be used to make the estimation of the geometric variability.
            random_state: the random seed used for the (random) sample elements.
            y_type: the type of response variable. Must be in ['quantitative', 'binary', 'multiclass'].
        """                   
        self.estimators = estimators; self.n_clusters = n_clusters; self.method = method; self.init = init; self.max_iter = max_iter; self.random_state = random_state
        self.frac_sample_size = frac_sample_size; self.p1 = p1; self.p2 = p2; self.p3 = p3; self.d1 = d1; self.d2 = d2; self.d3 = d3; self.robust_maha_method = robust_maha_method
        self.alpha = alpha; self.epsilon = epsilon; self.n_iters = n_iters; self.fast_VG = fast_VG; self.VG_sample_size = VG_sample_size; self.VG_n_samples = VG_n_samples; self.q = q;
        self.y_type = y_type
    
    def set_params(self, **params):
        """
        Set params method: for setting params properly.
        
        Parameters:
            params: a dictionary with params as values and params keys as names, following the sklearn conventions.
        """      
        for key, param_value in params.items():               
            parts = key.split('__')           
            # Setting values for the params of the estimators defined in FastKmedoidsEstimator
            if 'estimators' in parts:
                if parts[0] == 'estimators': # When FastKmedoidsEstimator is NOT part of a pipeline
                    estimator_key = int(parts[1])
                    param_key = '__'.join(parts[2:])
                    self.estimators[estimator_key].set_params(**{param_key: param_value})                
                elif parts[1] == 'estimators': # When FastKmedoidsEstimator is part of a pipeline
                    estimator_key = int(parts[2])
                    param_key = '__'.join(parts[3:])
                    self.estimators[estimator_key].set_params(**{param_key: param_value})
            
            else: # Setting values for the other parameters (different to 'estimators') of FastKmedoidsEstimator
                setattr(self, key, param_value)
                

    def fit(self, X, y, weights=None):
        """
        Fit method: fitting the fast k-medoids algorithm to `X` (and `y` if needed).
        
        Parameters:
            X: a pandas/polars data-frame or a numpy array. Represents a predictors matrix. Is required.
            y: a pandas/polars series or a numpy array. Represents a response variable. Is required.
            weights: the sample weights, if exists.
        """  
            
        pandas_required = False
        if isinstance(X, pd.DataFrame):
            pandas_required = True # If the input X is Pandas, we assume that the estimators are pipelines with ColumnTransform, which needs Pandas.
            X_pd = X.copy()
            X = X.to_numpy()
        if isinstance(y, pd.Series):
            y = y.to_numpy()

        self.fast_kmedoids = FastKmedoidsGG(n_clusters=self.n_clusters, method=self.method, init=self.init, max_iter=self.max_iter, random_state=self.random_state,
                                            frac_sample_size=self.frac_sample_size, p1=self.p1, p2=self.p2, p3=self.p3, 
                                            d1=self.d1, d2=self.d2, d3=self.d3, 
                                            robust_maha_method=self.robust_maha_method, alpha=self.alpha, epsilon=self.epsilon, n_iters=self.n_iters,
                                            fast_VG=self.fast_VG, VG_sample_size=self.VG_sample_size, VG_n_samples=self.VG_n_samples,
                                            y_type=self.y_type)
        self.fast_kmedoids.fit(X=X, y=y, weights=weights) 
        cluster_labels = self.fast_kmedoids.labels
        _ , counts = np.unique(cluster_labels, return_counts=True)
        print(f'Num.Clusters: {self.n_clusters}. Clusters proportions: {counts/len(X)}')

        X_cluster, Y_cluster = {}, {}
        if pandas_required == False:
            for j in range(self.n_clusters):
                X_cluster[j] = X[cluster_labels == j, :]
                Y_cluster[j] = y[cluster_labels == j]
                self.estimators[j].fit(X=X_cluster[j], y=Y_cluster[j])
        else: # pandas required
            for j in range(self.n_clusters):
                X_cluster[j] = X_pd.loc[cluster_labels == j, :]
                Y_cluster[j] = y[cluster_labels == j]
                self.estimators[j].fit(X=X_cluster[j], y=Y_cluster[j])   

    def predict(self, X):
        """
        Predict method: predicting the response variable for `X`.

        Parameters:
            X: a pandas/polars data-frame or a numpy array. Represents a predictors matrix. Is required.
        """
                
        pandas_required = False
        if isinstance(X, pd.DataFrame):
            pandas_required = True # If the input X is Pandas, we assume that the estimators are pipelines with ColumnTransform, which needs Pandas.
            X_pd = X.copy()
            X = X.to_numpy()

        predicted_clusters = self.fast_kmedoids.predict(X=X)

        Y_test_hat = []
        if pandas_required == True:
            for i in range(0, len(X)):
                Y_test_hat.append(self.estimators[predicted_clusters[i]].predict(X_pd.iloc[[i]])[0])
        else: # pandas not required
            for i in range(0, len(X)):
                Y_test_hat.append(self.estimators[predicted_clusters[i]].predict(X[i,:].reshape(1, -1))[0])

        return  np.array(Y_test_hat)    
    
#####################################################################################################################

class KFoldFastKmedoidsEstimator(BaseEstimator, RegressorMixin) :
    """
    Implements the KFold-Fast-K-medoids-Estimator based on KFold-Fast-K-medoids and Sklearn estiamators.
    """

    def __init__(self, estimators, n_clusters, method='pam', init='heuristic', max_iter=100, random_state=123,
                        frac_sample_size=0.1, p1=None, p2=None, p3=None, d1='robust_mahalanobis', d2='jaccard', d3='matching', 
                        robust_maha_method='trimmed', alpha=0.05, epsilon=0.05, n_iters=20, q=1,
                        fast_VG=False, VG_sample_size=1000, VG_n_samples=5, 
                        n_splits=5, shuffle=True, kfold_random_state=123, y_type=None, verbose=True) :
            """
            Constructor method.
            
            Parameters:
                estimators: a dictionary with the sklearn estimators (single models or pipelines) to be used in each clusters (keys: cluster indexes, values: estimators initialized).
                n_clusters: the number of clusters.
                method: the k-medoids clustering method. Must be in ['pam', 'alternate']. PAM is the classic one, more accurate but slower.
                init: the k-medoids initialization method. Must be in ['heuristic', 'random']. Heuristic is the classic one, smarter burt slower.
                max_iter: the maximum number of iterations run by k-medodis.
                frac_sample_size: the sample size in proportional terms.
                p1, p2, p3: number of quantitative, binary and multi-class variables in the considered data matrix, respectively. Must be a non negative integer.
                d1: name of the distance to be computed for quantitative variables. Must be an string in ['euclidean', 'minkowski', 'canberra', 'mahalanobis', 'robust_mahalanobis']. 
                d2: name of the distance to be computed for binary variables. Must be an string in ['sokal', 'jaccard'].
                d3: name of the distance to be computed for multi-class variables. Must be an string in ['matching'].
                q: the parameter that defines the Minkowski distance. Must be a positive integer.
                robust_maha_method: the method to be used for computing the robust covariance matrix. Only needed when d1 = 'robust_mahalanobis'.
                alpha : a real number in [0,1] that is used if `method` is 'trimmed' or 'winsorized'. Only needed when d1 = 'robust_mahalanobis'.
                epsilon: parameter used by the Delvin algorithm that is used when computing the robust covariance matrix. Only needed when d1 = 'robust_mahalanobis'.
                n_iters: maximum number of iterations used by the Delvin algorithm. Only needed when d1 = 'robust_mahalanobis'.
                fast_VG: whether the geometric variability estimation will be full (False) or fast (True).
                VG_sample_size: sample size to be used to make the estimation of the geometric variability.
                VG_n_samples: number of samples to be used to make the estimation of the geometric variability.
                random_state: the random seed used for the (random) sample elements.
                y_type: the type of response variable. Must be in ['quantitative', 'binary', 'multiclass'].
                n_splits: number of folds to be used.
                shuffle: whether data is shuffled before applying KFold or not, must be in [True, False]. 
                kfold_random_state: the random seed for KFold if shuffle = True.
            """  
            self.estimators = estimators; self.n_clusters = n_clusters; self.method = method; self.init = init; self.max_iter = max_iter; self.random_state = random_state
            self.frac_sample_size = frac_sample_size; self.p1 = p1; self.p2 = p2; self.p3 = p3; self.d1 = d1; self.d2 = d2; self.d3 = d3; self.robust_maha_method = robust_maha_method
            self.alpha = alpha; self.epsilon = epsilon; self.n_iters = n_iters; self.fast_VG = fast_VG; self.VG_sample_size = VG_sample_size; self.VG_n_samples = VG_n_samples; self.q = q;
            self.n_splits = n_splits; self.shuffle = shuffle; self.kfold_random_state = kfold_random_state; self.y_type = y_type; self.verbose= verbose


    def set_params(self, **params):
        """
        Set params method: for setting params properly.
        
        Parameters:
            params: a dictionary with params as values and params keys as names, following the sklearn conventions.
        """
        for key, param_value in params.items():               
            parts = key.split('__')           
            # Setting values for the params of the estimators defined in FastKmedoidsEstimator
            if 'estimators' in parts:
                if parts[0] == 'estimators': # When FastKmedoidsEstimator is NOT part of a pipeline
                    estimator_key = int(parts[1])
                    param_key = '__'.join(parts[2:])
                    self.estimators[estimator_key].set_params(**{param_key: param_value})                
                elif parts[1] == 'estimators': # When FastKmedoidsEstimator is part of a pipeline
                    estimator_key = int(parts[2])
                    param_key = '__'.join(parts[3:])
                    self.estimators[estimator_key].set_params(**{param_key: param_value})
            # Setting values for the other parameters (different to 'estimators') of FastKmedoidsEstimator
            else:                 
                setattr(self, key, param_value)

    def fit(self, X, y, weights=None):
        """
        Fit method: fitting the fast k-medoids algorithm to `X` (and `y` if needed).
        
        Parameters:
            X: a pandas/polars data-frame or a numpy array. Represents a predictors matrix. Is required.
            y: a pandas/polars series or a numpy array. Represents a response variable. Is required.
            weights: the sample weights, if exists.
        """  

        pandas_required = False
        if isinstance(X, pd.DataFrame):
            pandas_required = True # If the input X is Pandas, we assume that the estimators are pipelines with ColumnTransform, which needs Pandas.
            X_pd = X.copy()
            X = X.to_numpy()
        if isinstance(y, pd.Series):
            y = y.to_numpy()

        self.kfold_fast_kmedoids = KFoldFastKmedoidsGG(n_clusters=self.n_clusters, method=self.method, init=self.init, max_iter=self.max_iter, random_state=self.random_state,
                                                        frac_sample_size=self.frac_sample_size, p1=self.p1, p2=self.p2, p3=self.p3, 
                                                        d1=self.d1, d2=self.d2, d3=self.d3, 
                                                        robust_maha_method=self.robust_maha_method, alpha=self.alpha, epsilon=self.epsilon, n_iters=self.n_iters,
                                                        fast_VG=self.fast_VG, VG_sample_size=self.VG_sample_size, VG_n_samples=self.VG_n_samples, 
                                                        n_splits=self.n_splits, shuffle=self.shuffle, kfold_random_state=self.kfold_random_state,
                                                        y_type=self.y_type, verbose=self.verbose)
        self.kfold_fast_kmedoids.fit(X=X, y=y, weights=weights) 
        cluster_labels = self.kfold_fast_kmedoids.labels
        _ , counts = np.unique(cluster_labels, return_counts=True)
        print(f'Num.Clusters: {self.n_clusters}. Clusters proportions: {counts/len(X)}')

        X_cluster, Y_cluster = {}, {}
        if pandas_required == False:
            for j in range(self.n_clusters):
                X_cluster[j] = X[cluster_labels == j, :]
                Y_cluster[j] = y[cluster_labels == j]
                self.estimators[j].fit(X=X_cluster[j], y=Y_cluster[j])
        else: # pandas required
            for j in range(self.n_clusters):
                X_cluster[j] = X_pd.loc[cluster_labels == j, :]
                Y_cluster[j] = y[cluster_labels == j]
                self.estimators[j].fit(X=X_cluster[j], y=Y_cluster[j])              

    def predict(self, X):
        """
        Predict method: predicting the response variable for `X`.

        Parameters:
            X: a pandas/polars data-frame or a numpy array. Represents a predictors matrix. Is required.
        """

        pandas_required = False
        if isinstance(X, pd.DataFrame):
            pandas_required = True # If the input X is Pandas, we assume that the estimators are pipelines with ColumnTransform, which needs Pandas.
            X_pd = X.copy()
            X = X.to_numpy()

        predicted_clusters = self.kfold_fast_kmedoids.predict(X=X)

        Y_test_hat = []
        if pandas_required == True:
            for i in range(0, len(X)):
                Y_test_hat.append(self.estimators[predicted_clusters[i]].predict(X_pd.iloc[[i]])[0])
        else: # pandas not required
            for i in range(0, len(X)):
                Y_test_hat.append(self.estimators[predicted_clusters[i]].predict(X[i,:].reshape(1, -1))[0])

        return  np.array(Y_test_hat)    

#####################################################################################################################
        
def euclidean_predict_rule(X, y=None, centers=None, y_idx=None):
    """
    Rule used for predicting clusters based on euclidean distance by assigning to the nearest centroid.

    Parameters:
        X: a pandas/polars data-frame or a numpy array. Represents a predictors matrix. Is required.
        y: a pandas/polars series or a numpy array. Represents a response variable. Is not required.
        centers: clusters centers.
        y_idx: the column index in which `y` is located in `X`.

    """
    n_clusters = len(centers)

    # removing y from the centers, since in predict method X doesn't contain y.
    for j in range(n_clusters):
        centers[j] = np.delete(centers[j], y_idx)

    predicted_clusters = []
    for i in range(0, len(X)):
            dist_xi_centers = [Euclidean_dist(xi=X[i,:], xr=centers[j]) for j in range(n_clusters)]
            predicted_clusters.append(np.argmin(dist_xi_centers))

    return predicted_clusters

#####################################################################################################################

class KmeansEstimator(BaseEstimator, RegressorMixin, ClusterMixin):
    """
    Implements the K-means-Estimator based on K-means and Sklearn estimators.
    """

    def __init__(self, estimators, n_clusters, random_state=123):
        """
        Constructor method.
        
        Parameters:
            estimators: a dictionary with the sklearn estimators (single models or pipelines) to be used in each clusters (keys: cluster indexes, values: estimators initialized).
            n_clusters: the number of clusters.
            random_state: the random seed used for the (random) sample elements.
        """         
        self.estimators = estimators 
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=self.random_state)

    def set_params(self, **params):
        """
        Set params method: for setting params properly.
        
        Parameters:
            params: a dictionary with params as values and params keys as names, following the sklearn conventions.
        """     
        for key, param_value in params.items():               
            parts = key.split('__')           
            # Setting values for the params of the estimators defined in FastKmedoidsEstimator
            if 'estimators' in parts:
                if parts[0] == 'estimators': # When FastKmedoidsEstimator is NOT part of a pipeline
                    estimator_key = int(parts[1])
                    param_key = '__'.join(parts[2:])
                    self.estimators[estimator_key].set_params(**{param_key: param_value})                
                elif parts[1] == 'estimators': # When FastKmedoidsEstimator is part of a pipeline
                    estimator_key = int(parts[2])
                    param_key = '__'.join(parts[3:])
                    self.estimators[estimator_key].set_params(**{param_key: param_value})
            
            else: # Setting values for the other parameters (different to 'estimators') of KmeansEstimator
                setattr(self, key, param_value)

    def fit(self, X, y=None):
        """
        Fit method: fitting the fast k-medoids algorithm to `X` (and `y` if needed).
        
        Parameters:
            X: a pandas/polars data-frame or a numpy array. Represents a predictors matrix. Is required.
            y: a pandas/polars series or a numpy array. Represents a response variable. Is required.
            weights: the sample weights, if exists.
        """  

        pandas_required = False
        if isinstance(X, pd.DataFrame):
            pandas_required = True # If the input X is Pandas, we assume that the estimators are pipelines with ColumnTransform, which needs Pandas.
            X_pd = X.copy()
            X = X.to_numpy()
        if isinstance(y, pd.Series):
            y = y.to_numpy()

        X_y = np.column_stack((y,X))
        self.y_idx = 0

        self.kmeans.fit(X=X_y) 
        
        self.centers = {j: self.kmeans.cluster_centers_[j] for j in range(self.n_clusters)}
        cluster_labels = self.kmeans.labels_
        _ , counts = np.unique(cluster_labels, return_counts=True)
        print(f'Clusters proportions: {counts/len(X)}')

        X_cluster, Y_cluster = {}, {}
        if pandas_required == False:
            for j in range(self.n_clusters):
                X_cluster[j] = X[cluster_labels == j, :]
                Y_cluster[j] = y[cluster_labels == j] 
                self.estimators[j].fit(X=X_cluster[j], y=Y_cluster[j])
        else: # pandas required
            for j in range(self.n_clusters):
                X_cluster[j] = X_pd.loc[cluster_labels == j, :]
                Y_cluster[j] = y[cluster_labels == j]
                self.estimators[j].fit(X=X_cluster[j], y=Y_cluster[j]) 

        self.y = y

    def predict(self, X):
        """
        Predict method: predicting the response variable for `X`.

        Parameters:
            X: a pandas/polars data-frame or a numpy array. Represents a predictors matrix. Is required.
        """

        pandas_required = False
        if isinstance(X, pd.DataFrame):
            pandas_required = True # If the input X is Pandas, we assume that the estimators are pipelines with ColumnTransform, which needs Pandas.
            X_pd = X.copy()
            X = X.to_numpy()

        predicted_clusters = euclidean_predict_rule(X=X, y=self.y, centers=self.centers, y_idx=self.y_idx)

        Y_test_hat = []
        if pandas_required == True:
            for i in range(0, len(X)):
                Y_test_hat.append(self.estimators[predicted_clusters[i]].predict(X_pd.iloc[[i]])[0])
        else: # pandas not required
            for i in range(0, len(X)):
                Y_test_hat.append(self.estimators[predicted_clusters[i]].predict(X[i,:].reshape(1, -1))[0])
                       
        return np.array(Y_test_hat) 
    
#####################################################################################################################

class MiniBatchKmeansEstimator(BaseEstimator, RegressorMixin):

    def __init__(self, estimators, n_clusters, random_state=123):
        
        self.estimators = estimators 
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.minibatchkmeans = MiniBatchKMeans(n_clusters=self.n_clusters, random_state=self.random_state)

        # estimators: a dictionary with the estimators (single models or pipelines) to be used in each clusters (keys: cluster indexes, values: estimators initialized)                

    def set_params(self, **params):
        """
        Set params method: for setting params properly.
        
        Parameters:
            params: a dictionary with params as values and params keys as names, following the sklearn conventions.
        """   
        for key, param_value in params.items():               
            parts = key.split('__')           
            # Setting values for the params of the estimators defined in FastKmedoidsEstimator
            if 'estimators' in parts:
                if parts[0] == 'estimators': # When FastKmedoidsEstimator is NOT part of a pipeline
                    estimator_key = int(parts[1])
                    param_key = '__'.join(parts[2:])
                    self.estimators[estimator_key].set_params(**{param_key: param_value})                
                elif parts[1] == 'estimators': # When FastKmedoidsEstimator is part of a pipeline
                    estimator_key = int(parts[2])
                    param_key = '__'.join(parts[3:])
                    self.estimators[estimator_key].set_params(**{param_key: param_value})
            
            else: # Setting values for the other parameters (different to 'estimators') of MiniBatchKmeansEstimator                
                setattr(self, key, param_value)
    
    def fit(self, X, y=None):
        """
        Fit method: fitting the fast k-medoids algorithm to `X` (and `y` if needed).
        
        Parameters:
            X: a pandas/polars data-frame or a numpy array. Represents a predictors matrix. Is required.
            y: a pandas/polars series or a numpy array. Represents a response variable. Is required.
            weights: the sample weights, if exists.
        """  

        pandas_required = False
        if isinstance(X, pd.DataFrame):
            pandas_required = True # If the input X is Pandas, we assume that the estimators are pipelines with ColumnTransform, which needs Pandas.
            X_pd = X.copy()
            X = X.to_numpy()
        if isinstance(y, pd.Series):
            y = y.to_numpy()

        X_y = np.column_stack((y,X))
        self.y_idx = 0
        self.minibatchkmeans.fit(X=X_y) 
        self.centers = {j: self.minibatchkmeans.cluster_centers_[j] for j in range(self.n_clusters)}
        cluster_labels = self.minibatchkmeans.labels_
        _ , counts = np.unique(cluster_labels, return_counts=True)
        print(f'Clusters weights (proportions): {counts/len(X)}')

        X_cluster, Y_cluster = {}, {}
        if pandas_required == False:
            for j in range(self.n_clusters):
                X_cluster[j] = X[cluster_labels == j, :]
                Y_cluster[j] = y[cluster_labels == j] 
                self.estimators[j].fit(X=X_cluster[j], y=Y_cluster[j])
        else: # pandas required
            for j in range(self.n_clusters):
                X_cluster[j] = X_pd.loc[cluster_labels == j, :]
                Y_cluster[j] = y[cluster_labels == j]
                self.estimators[j].fit(X=X_cluster[j], y=Y_cluster[j]) 

        self.y = y

    def predict(self, X):
        """
        Predict method: predicting the response variable for `X`.

        Parameters:
            X: a pandas/polars data-frame or a numpy array. Represents a predictors matrix. Is required.
        """

        pandas_required = False
        if isinstance(X, pd.DataFrame):
            pandas_required = True # If the input X is Pandas, we assume that the estimators are pipelines with ColumnTransform, which needs Pandas.
            X_pd = X.copy()
            X = X.to_numpy()

        predicted_clusters = euclidean_predict_rule(X=X, y=self.y, centers=self.centers, y_idx=self.y_idx)

        Y_test_hat = []
        if pandas_required == True:
            for i in range(0, len(X)):
                Y_test_hat.append(self.estimators[predicted_clusters[i]].predict(X_pd.iloc[[i]])[0])
        else: # pandas not required
            for i in range(0, len(X)):
                Y_test_hat.append(self.estimators[predicted_clusters[i]].predict(X[i,:].reshape(1, -1))[0])

        return  np.array(Y_test_hat) 
    
#####################################################################################################################
