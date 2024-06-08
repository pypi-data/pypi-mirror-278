import numpy as np
import logging
from nwae.math.fit.utils.FitUtils import FitUtils
from sklearn.cluster import KMeans, MeanShift, DBSCAN
import matplotlib.pyplot as mplt


#
# The idea is this:
#   Case 1: All clusters (think towns) are almost-equally spaced apart
#      - in this case, suppose optimal cluster centers=n (think salesmen)
#      - if number of clusters k<n, then each salesman need to cover a larger area, and their average distances from each other is smaller
#      - if number of clusters k>n, then things become a bit crowded, with more than 1 salesman covering a single town
#      Thus at transition from n --> n+1 clusters, the average distance between cluster centers will decrease
#   Case 2: Some clusters are spaced much larger apart from other clusters
#      In this case, there will be multiple turning points, and we may take an earlier turning point or later turning points
#
# Нет кластеров - как узнать
#    1.
#
class Cluster:

    def __init__(
            self,
            logger = None,
    ):
        self.logger = logger if logger is not None else logging.getLogger()
        self.fit_utils = FitUtils(logger=self.logger)
        return

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

    def derive_additional_cluster_info(
            self,
            x: np.ndarray,
            n_centers: int,
            cluster_centers: np.ndarray,
            cluster_labels: np.ndarray,
            metric,
    ):
        assert len(cluster_centers) > 0
        assert type(cluster_centers) is np.ndarray
        # get distances between all center pairs
        distances_cluster_centers = self.fit_utils.get_point_distances(
            np_tensors = cluster_centers,
            np_center = None if len(cluster_centers) > 1 else cluster_centers[0],
        )
        # This is the key metric for us to define optimal number of centers, by looking at the +/- change
        # when cluster centers increase/decrease
        centers_distance_median = np.median(distances_cluster_centers)
        self.logger.debug('At n=' + str(n_centers) + ' centers median distance ' + str(centers_distance_median))

        # median radius of each cluster center to cluster points
        inner_radiuses = []
        # number of points inside each cluster
        inner_sizes = []
        for i in range(len(cluster_centers)):
            points_in_cluster = x[cluster_labels == i]
            # get distances of points with respect to center reference point
            inner_distances = self.fit_utils.get_point_distances(
                np_tensors = points_in_cluster,
                np_center = cluster_centers[i],
                metric = metric,
            )
            inner_rad = np.median(inner_distances)
            # self.logger.debug('Cluster #' + str(i) + ', radius = ' + str(radius))
            inner_radiuses.append(inner_rad)
            inner_sizes.append(len(points_in_cluster))

        inner_radiuses = np.array(inner_radiuses)
        inner_sizes = np.array(inner_sizes)
        return {
            'centers_median': centers_distance_median,
            'inner_radiuses': inner_radiuses,
            'cluster_sizes': inner_sizes,
        }

    def kmeans(
            self,
            x: np.ndarray,
            n_centers: int,
            km_iters = 100,
    ):
        assert x.ndim == 2

        kmeans = KMeans(
            n_clusters = n_centers,
            init = 'k-means++',
            max_iter = km_iters,
            n_init = 10,
            random_state = 0
        )
        kmeans.fit(x)
        self.logger.debug(kmeans.labels_)

        additional_info = self.derive_additional_cluster_info(
            x = x,
            n_centers = n_centers,
            cluster_centers = kmeans.cluster_centers_,
            cluster_labels = kmeans.labels_,
            metric = 'euclid',
        )

        return {
            'n_centers': n_centers,
            'kmeans': kmeans,
            'cluster_centers': kmeans.cluster_centers_,
            'cluster_labels': kmeans.labels_,
            'centers_median': additional_info['centers_median'],
            'inner_radiuses': additional_info['inner_radiuses'],
            'cluster_sizes': additional_info['cluster_sizes'],
            'points_inertia': kmeans.inertia_,
        }

    def kmeans_optimal(
            self,
            x: np.ndarray,
            km_iters = 100,
            max_clusters = 100,
            min_clusters = 2,
            plot = False,
            # by default if 25% of the clusters are single point clusters, we quit
            thr_single_clusters = 0.25,
            estimate_min_max = False,
    ):
        assert x.ndim == 2

        if estimate_min_max:
            min_clusters, max_clusters = self.estimate_min_max_clusters(n=len(x))

        # do a Monte-carlo
        # distances = self.fit_utils.get_point_distances_mc(np_tensors=self.text_encoded, iters=10000)
        # median_point_dist = np.median( distances )

        cluster_sets = {}
        max_n = min_clusters
        for n_centers in range(min_clusters, min(max_clusters+1, len(x)+1), 1):
            cluster_res = self.kmeans(
                x = x,
                n_centers = n_centers,
                km_iters = km_iters,
            )
            cluster_sets[n_centers] = cluster_res
            max_n = n_centers
            inner_sizes = cluster_res['cluster_sizes']

            # Check if clusters are becoming too sparse (1-member clusters too many)
            count_1_point_clusters = len(inner_sizes[inner_sizes==1])
            if count_1_point_clusters / len(inner_sizes) > thr_single_clusters:
                self.logger.info(
                    'Break at n centers = ' + str(n_centers) + ' with more than ' + str(100*thr_single_clusters)
                    + '% single point clusters, total single point clusters = '
                    + str(count_1_point_clusters)
                )
                break

        cs = cluster_sets
        val_cm = np.array([cs[i]['centers_median'] for i in range(max_n+1) if i>=min_clusters])
        #
        # Heuristic method using "pigeonhole principle". If n is the optimal number of clusters, then adding
        # one more will need to "crowd" the new center among the existing n centers. Thus center median should
        # reduce, or gradient calculated below is positive
        #
        grad_cm = [
            cs[i]['centers_median']-cs[i+1]['centers_median'] for i in range(max_n+1)
            if ((i >= min_clusters) and (i < max_n))
        ]
        grad_cm.append(0.)
        is_local_max_cm = [1*(x>0.00001) for x in grad_cm]
        if plot:
            self.logger.debug('Value CM: ' + str(val_cm))
            self.logger.debug('Gradient CM: ' + str(grad_cm))
            self.logger.debug('Is local max: ' + str(is_local_max_cm))
            mplt.plot(val_cm, linestyle='dotted')
            mplt.plot(is_local_max_cm)
            mplt.show()

        count_turning_point = 0
        for n_ctr, cluster_info in cluster_sets.items():
            is_turning_point = is_local_max_cm[n_ctr-min_clusters]
            count_turning_point += 1*is_turning_point

            cluster_info['count_turning_point'] = count_turning_point
            cluster_info['is_local_max_centers_median'] = is_turning_point
            cluster_info['gradient'] = grad_cm[n_ctr-min_clusters]

            if cluster_info['is_local_max_centers_median']:
                self.logger.info(
                    'Decrease of median distance of cluster centers at n_centers=' + str(n_ctr)
                    + ', from median distance ' + str(val_cm[n_ctr-min_clusters])
                    + ' to ' + str(val_cm[n_ctr+1-min_clusters])
                )

        final_clusters = [
            x for n,x in cluster_sets.items() if cluster_sets[n]['is_local_max_centers_median']
        ]
        if len(final_clusters) == 0:
            # There was no turning point, thus take the last one
            final_clusters = [x for n,x in cluster_sets.items() if (n==max_n)]
        return final_clusters


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    clstr = Cluster()
    x = np.array([
        [5, 1, 1], [8, 2, 1], [6, 0, 2],
        [1, 5, 1], [2, 7, 1], [0, 6, 2],
        [1, 1, 5], [2, 1, 8], [0, 2, 6],
    ])
    res = clstr.kmeans_optimal(x=x, estimate_min_max=True)
    for cluster_info in res:
        print('  Cluster ' + str(cluster_info['n_centers']))
        [print('    ' + str(k) + ': ' + str(v)) for k,v in cluster_info.items()]
    exit(0)
