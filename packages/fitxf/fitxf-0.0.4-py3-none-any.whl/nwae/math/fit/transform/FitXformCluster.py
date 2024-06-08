import logging
import os
import numpy as np
from nwae.math.fit.transform.FitXformInterface import FitXformInterface
from nwae.math.fit.utils.FitUtils import FitUtils
from nwae.math.fit.cluster.Cluster import Cluster
from nwae.math.utils.Lock import Lock
from nwae.math.utils.EnvironRepo import EnvRepo
from nwae.math.utils.Logging import Logging


class FitXformCluster(FitXformInterface):

    def __init__(
            self,
            logger = None,
    ):
        super().__init__(
            logger = logger,
        )

        self.__mutex_model = 'model'
        self.__lock = Lock(
            mutex_names = [self.__mutex_model],
            logger = self.logger,
        )
        self.fit_utils = FitUtils(logger=self.logger)
        self.cluster = Cluster(logger=self.logger)

        # Model parameters
        self.model_params_ready = False
        self.n_cluster = None
        self.cluster_centers = None
        self.cluster_labels = None
        self.cluster_inertia = None
        self.cluster_inertia_per_point = None
        self.centers_median_distance = None
        # Data/labels
        self.X = None
        self.X_labels = None
        self.X_full_records = None
        self.X_transform = None
        self.X_transform_check = None
        # Inverse PCA transform
        self.X_inverse_transform = None
        # Create an artificial grid
        self.X_grid_vectors = None
        self.X_grid_numbers = None
        # Measures for us to optimize the number of optimal number of pca components
        self.grid_density = None
        self.grid_density_mean = None
        self.distance_error = None
        self.distance_error_mean = None
        return

    def is_model_ready(self):
        return self.model_params_ready

    def estimate_min_max_clusters(
            self,
            n,
    ):
        max_clusters = 3*int(np.log(n))
        min_clusters = max(2, int(np.log(n)))
        self.logger.info(
            'Min/max clusters estimated as ' + str(min_clusters) + ' and ' + str(max_clusters) + ', n=' + str(n)
        )
        return min_clusters, max_clusters

    def fit_optimal(
            self,
            X: np.ndarray,
            X_labels = None,
            X_full_records = None,
            target_grid_density = 2,
            # allowed values 'median', 'mean', 'min'
            measure = 'median',
            # Model dependent interpretation, or ignore if not relevant for specific model
            min_components = 2,
            max_components = 100,
    ):
        try:
            self.__lock.acquire_mutexes(
                id = 'fit_optimal',
                mutexes = [self.__mutex_model],
            )

            # Interpret as min/max clusters
            min_clusters, max_clusters = min_components, max_components

            return self.__fit_optimal(
                X = X,
                X_labels = X_labels,
                X_full_records = X_full_records,
                target_grid_density = target_grid_density,
                min_clusters = min_clusters,
                max_clusters = max_clusters,
            )
        finally:
            self.__lock.release_mutexes(mutexes=[self.__mutex_model])

    def fit(
            self,
            X: np.ndarray,
            X_labels = None,
            X_full_records = None,
            # Model dependent interpretation, or ignore if not relevant for specific model
            # For example, can mean how many clusters, or how many PCA components, or how many to sample
            # in a discrete Fourier transform, etc.
            n_components = 2,
            return_details = False,
    ):
        n_centers = n_components
        self.logger.info(
            'Start kmeans optimal with X shape ' + str(X.shape) + ', n clusters ' + str(n_centers)
        )
        desired_cluster = self.cluster.kmeans(
            x = X,
            n_centers = n_centers,
            km_iters = 100,
        )
        self.logger.info('Desired cluster of requested n=' + str(n_centers) + ': ' + str(desired_cluster))
        return self.__record_cluster(
            desired_cluster = desired_cluster,
            X = X,
            X_labels = X_labels,
            X_full_records = X_full_records,
        )

    # Will dynamically look for optimal number of pca components, on the condition of the target grid density
    def __fit_optimal(
            self,
            X: np.ndarray,
            X_labels = None,
            X_full_records = None,
            target_grid_density = 2,
            # Model dependent interpretation, or ignore if not relevant for specific model
            min_clusters = 2,
            max_clusters = 100,
            km_iters = 100,
            # by default if 25% of the clusters are single point clusters, we quit
            thr_single_clusters = 0.25,
            plot = False,
    ):
        assert target_grid_density > 0, 'Target grid density not valid ' + str(target_grid_density)
        self.logger.info(
            'Start kmeans optimal with X shape ' + str(X.shape) + ', min clusters ' + str(min_clusters)
            + ', max clusters ' + str(max_clusters)
        )
        res = self.cluster.kmeans_optimal(
            x = X,
            km_iters = km_iters,
            min_clusters = min_clusters,
            max_clusters = max_clusters,
            thr_single_clusters = thr_single_clusters,
            plot = plot,
        )
        desired_cluster = res[0]
        self.logger.info('Desired optimal cluster: ' + str(desired_cluster))
        return self.__record_cluster(
            desired_cluster = desired_cluster,
            X = X,
            X_labels = X_labels,
            X_full_records = X_full_records,
        )

    def __record_cluster(
            self,
            desired_cluster: dict,
            X: np.ndarray,
            X_labels,
            X_full_records,
    ):
        # Copy over original data
        self.X = np.array(X)
        self.X_labels = np.array(X_labels)
        self.X_full_records = np.array(X_full_records)
        self.cluster_centers = desired_cluster['cluster_centers']
        self.cluster_labels = np.array(desired_cluster['cluster_labels'])
        self.n_cluster = desired_cluster['n_centers']
        self.cluster_inertia = desired_cluster['points_inertia']
        self.cluster_inertia_per_point = self.cluster_inertia / len(self.X)
        self.centers_median_distance = desired_cluster['centers_median']
        self.logger.info(
            'Inertia ' + str(self.cluster_inertia) + ', inertia per point ' + str(self.cluster_inertia_per_point)
            + ', centers median distance ' + str(self.centers_median_distance)
        )

        self.X_transform = self.__calc_transform(
            X = self.X,
        )
        self.logger.info('X transform: ' + str(self.X_transform))
        self.X_inverse_transform = self.__inverse_transform(
            x_transform = self.X_transform,
        )

        # Form grid using 1st dimension in increasing order
        x0 = self.cluster_centers[:,0]
        grid_order = np.argsort(x0)
        self.logger.info('Grid order: ' + str(grid_order))
        grid_lines = x0[grid_order]
        l = len(grid_lines)
        for i in range(l-1):
            grid_lines[i] = ( grid_lines[i] + grid_lines[i+1] ) / 2
        grid_lines[l-1] = 2 * grid_lines[l-1]
        self.logger.info('Grid lines: ' + str(grid_lines))

        return self.X_transform

    # Recover estimate of original point from PCA compression
    def inverse_transform(
            self,
            x_transform: np.ndarray,
    ):
        try:
            self.__lock.acquire_mutexes(
                id = 'inverse_transform',
                mutexes = [self.__mutex_model],
            )
            return self.__inverse_transform(
                x_transform = x_transform,
            )
        finally:
            self.__lock.release_mutexes(mutexes=[self.__mutex_model])

    def __inverse_transform(
            self,
            x_transform: np.ndarray,
    ):
        # Transform is just the cluster label (or cluster center index)
        x_estimated = self.cluster_centers[x_transform]
        return x_estimated

    # Get PCA values of arbitrary points
    def calc_transform(
            self,
            X: np.ndarray,
    ):
        try:
            self.__lock.acquire_mutexes(
                id = 'calc_transform',
                mutexes = [self.__mutex_model],
            )
            return self.__calc_transform(X=X)
        finally:
            self.__lock.release_mutexes(mutexes=[self.__mutex_model])

    def __calc_transform(
            self,
            X: np.ndarray,
    ):
        pred_labels, pred_probs = self.predict_standard(
            X = X,
            ref_X = self.cluster_centers,
            ref_labels = np.array(range(len(self.cluster_centers))),
            top_k = 3,
        )
        # Cluster transform is just the cluster label
        return np.array([r[0] for r in pred_labels])

    # def __predict_grid_pca(
    #         self,
    #         X: np.ndarray,
    # ):
    #     # TODO First, determine the grid segments of the texts/embeddings
    #     x_pca = self.calc_transform(
    #         X = X,
    #     )
    #     grid, grid_numbers = self.__calc_pca_grid(
    #         x_pca = x_pca,
    #     )
    #     return grid, grid_numbers

    def __calc_grid(
            self,
            X: np.ndarray,
    ):
        raise Exception('TODO')

    def predict(
            self,
            X: np.ndarray,
            top_k = 5,
            return_full_record = False,
            use_grid = False,
    ):
        try:
            self.__lock.acquire_mutexes(
                id = 'predict',
                mutexes = [self.__mutex_model],
            )

            pred_labels, pred_probs = self.predict_standard(
                X = X,
                ref_X = self.cluster_centers,
                ref_labels = np.array(range(len(self.cluster_centers))),
                top_k = 3,
            )
            # Cluster transform is just the cluster label
            return np.array([r[0] for r in pred_labels])
        finally:
            self.__lock.release_mutexes(mutexes=[self.__mutex_model])


if __name__ == '__main__':
    from nwae.math.lang.encode.LangModelPt import LangModelPt as LmPt
    texts = [
        "Let's have coffee", "Free for a drink?", "How about Starbucks?",
        "I am busy", "Go away", "Don't disturb me",
        "Monetary policies", "Interest rates", "Deposit rates",
    ]
    lmo = LmPt(lang='en', cache_folder=EnvRepo(repo_dir=os.environ["REPO_DIR"]).MODELS_PRETRAINED_DIR)

    embeddings = lmo.encode(text_list=texts, return_tensors='np')

    # use the function create_pca_plot to
    fitter = FitXformCluster(logger=Logging.get_default_logger(log_level=logging.INFO, propagate=False))
    x_compressed = fitter.fit_optimal(X=embeddings)

    fitter.create_scatter_plot2d(
        x_transform = fitter.X_inverse_transform,
        labels_list = texts,
        show = True,
        # add some noise to separate the points a little more
        add_noise = True,
    )

    x = np.array([[1,2,3], [3,2,1], [-1,-2,-2], [-3,-4,-2]])
    x_ = fitter.fit(X=x, X_labels=['+', '+', '-', '-'], n_components=2)
    print('Clusters:', x_)
    print('Fit arbitrary:', fitter.predict(X=np.array([[9,9,8], [-55,-33,-55]]), use_grid=False))
    print('Fit arbitrary:', fitter.predict(X=np.array([[9,9,8], [-55,-33,-55]]), use_grid=True))

    exit(0)
