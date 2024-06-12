###
# #%L
# aiSSEMBLE::Test::MDA::Data Delivery Pyspark
# %%
# Copyright (C) 2021 Booz Allen
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from ...generated.step.abstract_pipeline_step import AbstractPipelineStep
from krausening.logging import LogManager
from abc import abstractmethod
from time import time_ns
from ..pipeline.pipeline_base import PipelineBase
from pyspark.sql.dataframe import DataFrame
from aiops_core_metadata.hive_metadata_api_service import HiveMetadataAPIService
from pathlib import Path
from policy_manager.configuration import PolicyConfiguration
from aiops_encrypt_policy import DataEncryptionPolicy, DataEncryptionPolicyManager
from typing import List
import os
from uuid import uuid4
from datetime import datetime



class DeltaLakePersistenceAsyncBase(AbstractPipelineStep):
    """
    Performs scaffolding asynchronous processing for DeltaLakePersistenceAsync. Business logic is delegated to the subclass.

    GENERATED CODE - DO NOT MODIFY (add your customizations in DeltaLakePersistenceAsync).

    Generated from: templates/data-delivery-pyspark/asynchronous.processor.base.py.vm
    """

    logger = LogManager.get_instance().get_logger('DeltaLakePersistenceAsyncBase')
    step_phase = 'DeltaLakePersistenceAsync'
    bomIdentifier = "Unspecified DeltaLakePersistenceAsync BOM identifier"



    def __init__(self, data_action_type, descriptive_label):
        super().__init__(data_action_type, descriptive_label)

        self.delta_output_directory = '/tmp/output/deltalake/'
        self.set_metadata_api_service(HiveMetadataAPIService())


    async def execute_step(self) -> None:
        """
        Executes this step.
        """
        start = time_ns()
        DeltaLakePersistenceAsyncBase.logger.info('START: step execution...')


        run_id = uuid4()
        parent_run_facet = PipelineBase().get_pipeline_run_as_parent_run_facet()
        job_name = self.get_job_name()
        default_namespace = self.get_default_namespace()
        event_data = self.create_base_lineage_event_data()
        start_time = datetime.utcnow()
        self.record_lineage(self.create_lineage_start_event(run_id=run_id,job_name=job_name,default_namespace=default_namespace,parent_run_facet=parent_run_facet,event_data=event_data,start_time=start_time))
        try:
            await self.execute_step_impl()
            end_time = datetime.utcnow()
            self.record_lineage(self.create_lineage_complete_event(run_id=run_id,job_name=job_name,default_namespace=default_namespace,parent_run_facet=parent_run_facet,event_data=event_data,start_time=start_time,end_time=end_time))
        except Exception as error:
            self.logger.exception(
                "An exception occurred while executing "
                + self.get_data_action_descriptive_label()
            )
            self.logger.exception(error)
            self.record_lineage(self.create_lineage_fail_event(run_id=run_id,job_name=job_name,default_namespace=default_namespace,parent_run_facet=parent_run_facet,event_data=event_data,start_time=start_time,end_time=datetime.utcnow(),error=error))
            PipelineBase().record_pipeline_lineage_fail_event()
            raise Exception(error)

        self.record_provenance()


        stop = time_ns()
        DeltaLakePersistenceAsyncBase.logger.info('COMPLETE: step execution completed in %sms' % ((stop - start) / 1000000))
        


    @abstractmethod
    async def execute_step_impl(self) -> None:
        """
        This method performs the business logic of this step,
        and should be implemented in DeltaLakePersistenceAsync.
        """
        pass


  


    def save_dataset(self, dataset: DataFrame, table_name: str) -> None:
        """
        Saves a dataset.
        """
        DeltaLakePersistenceAsyncBase.logger.info('Saving %s To Delta Lake...' % self.descriptive_label)

        path = self.delta_output_directory + table_name
        dataset.write.format('delta').mode('append').save(path)
        # PySpark 3.0 does not have a tableExists method
        if table_name not in [t.name for t in self.spark.catalog.listTables()]:
            self.spark.catalog.createTable(table_name, path, "delta")

        DeltaLakePersistenceAsyncBase.logger.info('Saved %s to Delta Lake' % self.descriptive_label)




