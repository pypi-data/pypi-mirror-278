###
# #%L
# aiSSEMBLE::Test::MDA::Data Delivery Pyspark
# %%
# Copyright (C) 2021 Booz Allen
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from krausening.logging import LogManager
from data_delivery_spark_py.test_utils.spark_session_manager import create_standalone_spark_session

"""
Behave test environment setup to configure Spark for unit tests.

GENERATED CODE - DO NOT MODIFY (add your customizations in environment.py).

Originally generated from: templates/data-delivery-pyspark/behave.environment.base.py.vm
"""
logger = LogManager.get_instance().get_logger("Environment")


"""
Generated or model-dependent setup to be executed prior to unit tests.
"""
def initialize(sparkapplication_path = "target/apps/pyspark-data-delivery-patterns-test-chart.yaml"):
    create_standalone_spark_session(sparkapplication_path)


"""
Generated or model-dependent setup to be executed after completion of unit tests.
"""
def cleanup():
    pass
