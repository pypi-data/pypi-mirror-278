"""Vanilla algorithms module"""

from typing import Any, Dict, List, Union

import numpy as np


class VanillaSupportResistance:
    """Vanilla Support Resistance class"""

    @classmethod
    def __calc_points(cls, data: np.ndarray, extreme: str) -> np.ndarray[np.ndarray]:
        """
        Calculate points (max o min).
        Return: numpy.ndarray. Dtype = [('idx', 'i4'), ('open', 'f8'), ('close', 'f8'), ('high', 'f8'), ('low', 'f8'), ('volume', 'f8')]
        I.e.: [[4.93000000e+02 4.77248100e+04 4.75912400e+04 4.77299900e+04 4.75580000e+04 1.92358790e+02], ...]
        """

        points = []
        extreme_value = data[:, 2] if extreme == "max" else data[:, 3]

        center = extreme_value[1:-1]
        left = extreme_value[:-2]
        right = extreme_value[2:]

        max_condition = (center > left) & (center > right)
        min_condition = (center < left) & (center < right)

        np.where(max_condition)[0] + 1  # Index adjustment
        np.where(min_condition)[0] + 1  # Index adjustment

        idx = None
        if extreme == "max":
            idx = np.where(max_condition)[0] + 1
        elif extreme == "min":
            idx = np.where(min_condition)[0] + 1

        points = np.empty((len(idx), 6))
        for i, idx in enumerate(idx):
            points[i] = [
                idx,
                data[idx, 0],
                data[idx, 1],
                data[idx, 2],
                data[idx, 3],
                data[idx, 4],
            ]

        return points

    @classmethod
    def __clustering(  # pylint: disable=too-many-locals, too-many-branches
        cls, data: np.ndarray, threshold: float, direction: str
    ) -> List[np.ndarray[np.ndarray]]:
        """
        Clustering.
        Return: numpy.ndarray[numpy.ndarray[numpy.ndarray]].
        dtype: [('idx', 'i4'), ('open', 'f8'), ('close', 'f8'), ('high', 'f8'), ('low', 'f8'), ('volume', 'f8')]
        I.e.: [[[493., 47724.81, 47591.24, 47729.99, 47558., 192.35879], ...], ...]
        """

        clusters = []
        high_index = 3  # Index of the 'high' column in the data array
        low_index = 4  # Index of the 'low' column in the data array

        for curr_first in data:  # pylint: disable=too-many-nested-blocks
            cluster = []
            if direction == "resistance":
                h0_first = curr_first[high_index]
            elif direction == "support":
                h0_first = curr_first[low_index]
            else:
                h0_first = None

            cluster.append(curr_first)
            for curr_second in data:
                if direction == "resistance":
                    h0_second = curr_second[high_index]
                elif direction == "support":
                    h0_second = curr_second[low_index]
                else:
                    h0_second = None

                dif = abs(((h0_first - h0_second) / h0_first) * 100)

                if dif <= threshold:
                    cluster.append(curr_second)

            if cluster:
                if not clusters:
                    clusters.append(np.array(cluster))
                else:
                    push = True
                    clust = (
                        cluster[0][high_index]
                        if direction == "resistance"
                        else cluster[0][low_index]
                    )

                    for curr in clusters:
                        curr_clust = (
                            curr[0][high_index]
                            if direction == "resistance"
                            else curr[0][low_index]
                        )

                        dif = abs(((clust - curr_clust) / clust) * 100)

                        if dif <= threshold:
                            push = False
                            if len(curr) > len(cluster):
                                cluster = curr

                    if push:
                        clusters.append(np.array(cluster))

        return clusters

    @classmethod
    def __recovery_line(  # pylint: disable=too-many-locals
        cls, clusters: List[np.ndarray[np.ndarray]], direction: str
    ) -> np.ndarray:
        """
        Recovery line.
        Return: numpy.ndarray. dtype: [
            ('idx', 'i4'), ('open', 'f8'), ('close', 'f8'), ('high', 'f8'), ('low', 'f8'), ('volume', 'f8')
        ]
        I.e.: [
            (47729.99, 48495.  , 47716.9 , 32, 16145.34576)
            (45000.  , 45000.  , 44990.  ,  4,  3689.66919)
            (43996.5 , 44141.37, 43307.85, 25, 12609.72691)
            (43473.45, 43777.  , 43127.97, 20, 10403.64128)
            (42259.58, 42787.38, 42077.62, 21,  9709.83536)
            (41465.  , 42593.69, 41450.  , 28, 13145.51234)
        ]
        """

        dtype = np.dtype(
            [
                ("pivotPrice", "f8"),
                ("limitsUp", "f8"),
                ("limitsDown", "f8"),
                ("score", "i4"),
                ("accumulatedVolume", "f8"),
            ]
        )

        lines = []
        for curr_cluster in clusters:
            pivot_price = None
            approach = 0
            limits_up = 0
            limits_down = np.inf
            accumulated_volume = 0
            curr_data_price_line = None
            data_line = None

            for idx in range(len(curr_cluster)):
                if direction == "resistance":
                    curr_data_price_line = curr_cluster[idx, 3]
                    data_line = (
                        curr_cluster[idx + 1, 3]
                        if idx + 1 < len(curr_cluster)
                        else None
                    )
                elif direction == "support":
                    curr_data_price_line = curr_cluster[idx, 4]
                    data_line = (
                        curr_cluster[idx + 1, 4]
                        if idx + 1 < len(curr_cluster)
                        else None
                    )

                limits_up = max(limits_up, curr_data_price_line)
                limits_down = min(limits_down, curr_data_price_line)

                if curr_data_price_line >= (data_line if data_line is not None else 0):
                    pivot_price = curr_data_price_line
                else:
                    pivot_price = data_line

                approach += 1
                accumulated_volume += curr_cluster[idx, 5]

            line = (
                pivot_price,
                max(limits_up, pivot_price),
                min(limits_down, pivot_price),
                approach,
                accumulated_volume,
            )

            if len(lines) > 0:
                lines_np = np.array(lines, dtype=dtype)
                existing_line_idx = np.where(lines_np["pivotPrice"] == pivot_price)[0]
            else:
                existing_line_idx = np.array([])

            if len(existing_line_idx) == 0:
                lines.append(line)
            else:
                idx_update = existing_line_idx[0]
                if lines[idx_update][3] < approach:
                    lines[idx_update] = line

        lines_np = np.array(lines, dtype=dtype)
        return np.sort(lines_np, order="pivotPrice")[::-1]

    @classmethod
    def __unify(
        cls,
        src_r: np.ndarray,
        src_s: np.ndarray,
        threshold: float,
        total_lines: np.ndarray | None = np.ndarray,
    ) -> List[Dict[str, Any]]:
        """
        Unify.
        Return: numpy.ndarray. dtype: [
            ('idx', 'i4'), ('open', 'f8'), ('close', 'f8'), ('high', 'f8'), ('low', 'f8'), ('volume', 'f8')
        ]
        I.e.: [
            (47729.99, 48495.  , 47716.9 , 32, 16145.34576)
            (45000.  , 45000.  , 44990.  ,  4,  3689.66919)
            (43996.5 , 44141.37, 43307.85, 25, 12609.72691)
            (43473.45, 43777.  , 43127.97, 20, 10403.64128)
            (42259.58, 42787.38, 42077.62, 21,  9709.83536)
            (41465.  , 42593.69, 41450.  , 28, 13145.51234)
        ]
        """

        # Combine and sort the sources
        src = np.concatenate((src_r, src_s))
        src = src[np.argsort(src["pivotPrice"])[::-1]]

        for curr_src in src:
            push = True
            idx_update = None

            if total_lines.size == 0:
                new_line = np.array(
                    [
                        (
                            curr_src["pivotPrice"],
                            curr_src["limitsUp"],
                            curr_src["limitsDown"],
                            curr_src["score"],
                            curr_src["accumulatedVolume"],
                        )
                    ],
                    dtype=total_lines.dtype,
                )
                total_lines = np.append(total_lines, new_line)
            else:
                for idx, curr_total_line in enumerate(total_lines):
                    dif = abs(
                        (
                            (curr_src["pivotPrice"] - curr_total_line["pivotPrice"])
                            / curr_src["pivotPrice"]  # noqa: W503
                        )
                        * 100  # noqa: W503
                    )

                    if dif <= threshold:  # update
                        push = False
                        idx_update = idx
                        break

                if push:  # push
                    new_line = np.array(
                        [
                            (
                                curr_src["pivotPrice"],
                                curr_src["limitsUp"],
                                curr_src["limitsDown"],
                                curr_src["score"],
                                curr_src["accumulatedVolume"],
                            )
                        ],
                        dtype=total_lines.dtype,
                    )
                    total_lines = np.append(total_lines, new_line)
                else:  # update
                    total_lines[idx_update]["pivotPrice"] = max(
                        curr_src["pivotPrice"], total_lines[idx_update]["pivotPrice"]
                    )
                    total_lines[idx_update]["limitsUp"] = max(
                        curr_src["limitsUp"], total_lines[idx_update]["limitsUp"]
                    )
                    total_lines[idx_update]["limitsDown"] = min(
                        curr_src["limitsDown"], total_lines[idx_update]["limitsDown"]
                    )
                    total_lines[idx_update]["score"] += curr_src["score"]
                    total_lines[idx_update]["accumulatedVolume"] += curr_src[
                        "accumulatedVolume"
                    ]

        return total_lines

    @classmethod
    def exec_pipeline(  # pylint: disable=dangerous-default-value
        cls,
        input_data: Dict[str, List[Union[float, int]]],
        cluster_threshold: float | None = 1.0,
        previous_sr: list | None = [],
    ) -> List[Dict[str, Union[int, float]]]:
        """
        Calculate support/resistance process pipeline.
        Return: list[dict[str, Union[int, float]]]. Support/Resistance calculated data. I.e.: [
            {'pivotPrice': 48184.0, 'limitsUp': 48495.0, 'limitsDown': 47347.53, 'score': 67, 'accumulatedVolume': 44687.15635},
            {'pivotPrice': 47534.34, 'limitsUp': 47874.98, 'limitsDown': 46763.68, 'score': 41, 'accumulatedVolume': 23864.294279999995},
            {'pivotPrice': 45000.0, 'limitsUp': 45000.0, 'limitsDown': 44700.0, 'score': 8, 'accumulatedVolume': 6010.54166},
            {'pivotPrice': 43996.5, 'limitsUp': 44141.37, 'limitsDown': 43100.0, 'score': 40, 'accumulatedVolume': 17909.42211},
            {'pivotPrice': 43473.45, 'limitsUp': 43580.0, 'limitsDown': 42697.01, 'score': 37, 'accumulatedVolume': 18501.36496},
            {'pivotPrice': 42819.86, 'limitsUp': 42850.0, 'limitsDown': 42041.7, 'score': 15, 'accumulatedVolume': 6355.429050000001},
            {'pivotPrice': 42259.58, 'limitsUp': 42787.38, 'limitsDown': 42017.33, 'score': 24, 'accumulatedVolume': 12506.830009999998},
            {'pivotPrice': 41619.99, 'limitsUp': 42365.48, 'limitsDown': 41115.0, 'score': 91, 'accumulatedVolume': 42944.990900000004},
            {'pivotPrice': 41071.29, 'limitsUp': 41157.26, 'limitsDown': 40753.88, 'score': 8, 'accumulatedVolume': 4474.11918}
        ]
        """

        # Convert to numpy array
        data_np = np.array(list(input_data.values())).T

        # Previous lines (empty)
        dtype = [
            ("pivotPrice", "f8"),
            ("limitsUp", "f8"),
            ("limitsDown", "f8"),
            ("score", "i4"),
            ("accumulatedVolume", "f8"),
        ]
        previous_sr = np.array(previous_sr, dtype=dtype)

        max_point: np.ndarray[np.ndarray] = cls.__calc_points(
            data=data_np, extreme="max"
        )
        min_point: np.ndarray[np.ndarray] = cls.__calc_points(
            data=data_np, extreme="min"
        )
        clusters_r: np.ndarray[np.ndarray[np.ndarray]] = cls.__clustering(
            data=max_point, threshold=cluster_threshold, direction="resistance"
        )
        clusters_s: np.ndarray[np.ndarray[np.ndarray]] = cls.__clustering(
            data=min_point, threshold=cluster_threshold, direction="support"
        )
        recovery_line_r: np.ndarray = cls.__recovery_line(
            clusters=clusters_r, direction="resistance"
        )
        recovery_line_s: np.ndarray = cls.__recovery_line(
            clusters=clusters_s, direction="support"
        )
        s_r_calculated = cls.__unify(
            src_r=recovery_line_r,
            src_s=recovery_line_s,
            threshold=cluster_threshold,
            total_lines=previous_sr,
        )

        s_r_calculated_dict = [
            {
                "pivotPrice": row["pivotPrice"],
                "limitsUp": row["limitsUp"],
                "limitsDown": row["limitsDown"],
                "score": row["score"],
                "accumulatedVolume": row["accumulatedVolume"],
            }
            for row in s_r_calculated
        ]
        return s_r_calculated_dict
