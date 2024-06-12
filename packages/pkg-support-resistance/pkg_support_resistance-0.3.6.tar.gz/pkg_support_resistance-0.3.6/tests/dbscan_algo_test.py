"""DBSCAN ML algorithms test module"""

from src.pkg_support_resistance import DBSCANSupportResistance
from src.pkg_support_resistance.data_set import sr_input_example
from .expected_output_test import dbscan_sr_exec_pipeline_expected_output_test


def test_dbscan_algorithms_exec_pipeline():
    """
    Test dbscan algorithms the calculation of support/resistance process.
    This test verifies that the function exec_pipeline,
    """

    result: list[dict] = DBSCANSupportResistance.exec_pipeline(
        input_data=sr_input_example, eps=1000, min_samples=1
    )
    assert result == dbscan_sr_exec_pipeline_expected_output_test
