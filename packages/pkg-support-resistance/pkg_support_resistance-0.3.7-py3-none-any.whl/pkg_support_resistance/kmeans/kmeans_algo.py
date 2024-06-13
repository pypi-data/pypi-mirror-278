"""KMeans ML algorithms module"""

from typing import Any, Dict, List, Union

import pandas as pd
from sklearn.cluster import KMeans


class KMeansSupportResistance:
    """KMeans Clustering Support Resistance (unsupervised algorithms) class"""

    @classmethod
    def __preprocess_data(
        cls, input_data: Dict[str, List[Union[float, int]]]
    ) -> pd.DataFrame:
        """
        Preprocess data.
        Return: pd.DataFrame.
        I.e.:
            open        close      high       low     volume    avg_price
        0    42780.00  42834.94  42901.10  42730.03  173.63661  42811.5175
        1    42834.94  42961.84  42986.06  42795.41  169.47648  42894.5625
        2    42961.83  43069.98  43160.86  42914.13  298.77136  43026.7000
        3    43070.30  43139.40  43159.74  42988.00  221.97150  43089.3600
        4    43139.40  43303.82  43333.00  43115.00  398.10382  43222.8050
        ...
        """

        df: pd.DataFrame = pd.DataFrame(data=input_data)
        df["avg_price"] = df[["open", "close", "high", "low"]].mean(axis=1)
        return df

    @classmethod
    def __apply_kmeans(
        cls, df: pd.DataFrame, n_clusters: int | None = 5
    ) -> pd.DataFrame:
        """
        Apply kmeans.
        Return: pd.DataFrame.
        I.e.:
            open         close      high       low     volume   avg_price   cluster
        0    42780.00  42834.94  42901.10  42730.03  173.63661  42811.5175        4
        1    42834.94  42961.84  42986.06  42795.41  169.47648  42894.5625        4
        2    42961.83  43069.98  43160.86  42914.13  298.77136  43026.7000        4
        3    43070.30  43139.40  43159.74  42988.00  221.97150  43089.3600        4
        4    43139.40  43303.82  43333.00  43115.00  398.10382  43222.8050        4
        ...
        """

        kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(df[["avg_price"]])
        df["cluster"] = kmeans.labels_
        return df

    @classmethod
    def __calculate_cluster(
        cls, df: pd.DataFrame, n_clusters: int
    ) -> List[Dict[str, Any]]:
        """
        Calculate cluster.
        Return: List[Dict[str, Any]].
        I.e.: [
            {'pivotPrice': 41247.07, 'limitsDown': 40965.2125, 'limitsUp': 41334.82750000001, 'accumulatedVolume': 11484.42265, 'score': 25},
            {'pivotPrice': 41541.4925, 'limitsDown': 41350.675, 'limitsUp': 41683.4625, 'accumulatedVolume': 16764.66682, 'score': 44},
            {'pivotPrice': 41740.695, 'limitsDown': 41685.535, 'limitsUp': 42090.5675, 'accumulatedVolume': 25677.978769999998, 'score': 54},
            {'pivotPrice': 42616.125, 'limitsDown': 42105.2425, 'limitsUp': 42692.68749999999, 'accumulatedVolume': 28562.038430000004, 'score': 68},
            {'pivotPrice': 42939.847499999996, 'limitsDown': 42811.5175, 'limitsUp': 43384.869999999995, 'accumulatedVolume': 29510.197329999995, 'score': 65},
            {'pivotPrice': 43669.6875, 'limitsDown': 43419.9975, 'limitsUp': 44002.247500000005, 'accumulatedVolume': 25561.89504, 'score': 64},
            {'pivotPrice': 45788.325, 'limitsDown': 44330.0825, 'limitsUp': 45788.325, 'accumulatedVolume': 12449.31098, 'score': 13},
            {'pivotPrice': 46947.585, 'limitsDown': 46947.585, 'limitsUp': 47633.6625, 'accumulatedVolume': 40150.74441, 'score': 55},
            {'pivotPrice': 47886.935000000005, 'limitsDown': 47651.009999999995, 'limitsUp': 48355.61749999999, 'accumulatedVolume': 39565.819639999994, 'score': 111}
        ]
        """

        cluster_info = []
        for i in range(n_clusters):
            cluster_data = df[df["cluster"] == i]
            limitsDown = cluster_data["avg_price"].min()
            limitsUp = cluster_data["avg_price"].max()
            accumulatedVolume = cluster_data["volume"].sum()

            max_volume_idx = cluster_data["volume"].idxmax()
            pivotPrice = cluster_data.loc[max_volume_idx, "avg_price"]
            score = len(cluster_data)

            cluster_info.append(
                {
                    "cluster": i,
                    "pivotPrice": pivotPrice,
                    "limitsDown": limitsDown,
                    "limitsUp": limitsUp,
                    "score": score,
                    "accumulatedVolume": accumulatedVolume,
                }
            )

        cluster_sorted: list[dict] = sorted(cluster_info, key=lambda x: x["pivotPrice"])
        cluster_result: list[dict] = [
            {k: v for k, v in d.items() if k != "cluster"} for d in cluster_sorted
        ]
        return cluster_result

    @classmethod
    def exec_pipeline(
        cls, input_data: Dict[str, List[Union[float, int]]], n_clusters: int | None = 5
    ) -> List[Dict[str, Any]]:
        """
        Calculate support/resistance process pipeline.
        Return: list[dict[str, Union[int, float]]]. Support/Resistance calculated data. I.e.: [
            {'pivotPrice': 41247.07, 'limitsDown': 40965.2125, 'limitsUp': 41334.82750000001, 'accumulatedVolume': 11484.42265},
            {'pivotPrice': 41541.4925, 'limitsDown': 41350.675, 'limitsUp': 41683.4625, 'accumulatedVolume': 16764.66682},
            {'pivotPrice': 41740.695, 'limitsDown': 41685.535, 'limitsUp': 42090.5675, 'accumulatedVolume': 25677.978769999998},
            {'pivotPrice': 42616.125, 'limitsDown': 42105.2425, 'limitsUp': 42692.68749999999, 'accumulatedVolume': 28562.038430000004},
            {'pivotPrice': 42939.847499999996, 'limitsDown': 42811.5175, 'limitsUp': 43384.869999999995, 'accumulatedVolume': 29510.197329999995},
            {'pivotPrice': 43669.6875, 'limitsDown': 43419.9975, 'limitsUp': 44002.247500000005, 'accumulatedVolume': 25561.89504},
            {'pivotPrice': 45788.325, 'limitsDown': 44330.0825, 'limitsUp': 45788.325, 'accumulatedVolume': 12449.31098},
            {'pivotPrice': 46947.585, 'limitsDown': 46947.585, 'limitsUp': 47633.6625, 'accumulatedVolume': 40150.74441},
            {'pivotPrice': 47886.935000000005, 'limitsDown': 47651.009999999995, 'limitsUp': 48355.61749999999, 'accumulatedVolume': 39565.819639999994}
        ]
        """

        df: pd.DataFrame = cls.__preprocess_data(input_data=input_data)
        df: pd.DataFrame = cls.__apply_kmeans(df=df, n_clusters=n_clusters)
        cluster_model: list[dict] = cls.__calculate_cluster(
            df=df, n_clusters=n_clusters
        )
        return cluster_model
