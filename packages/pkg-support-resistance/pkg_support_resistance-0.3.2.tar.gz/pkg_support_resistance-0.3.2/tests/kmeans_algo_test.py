"""KMeans ML algorithms test module"""

from src.pkg_support_resistance import KMeansSupportResistance
from src.pkg_support_resistance.data_set import sr_input_example
from .expected_output_test import kmeans_sr_exec_pipeline_expected_output_test


def test_kmeans_algorithms_exec_pipeline():
    """
    Test kmeans algorithms the calculation of support/resistance process.
    This test verifies that the function exec_pipeline,
    """

    result: list[dict] = KMeansSupportResistance.exec_pipeline(
        input_data=sr_input_example, n_clusters=9
    )
    assert result == kmeans_sr_exec_pipeline_expected_output_test
