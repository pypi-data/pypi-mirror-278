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
from aiops_core_metadata.hive_metadata_api_service import HiveMetadataAPIService
from kafka import KafkaConsumer
from aiops_core_config import MessagingConfig
from pathlib import Path
from policy_manager.configuration import PolicyConfiguration
from aiops_encrypt_policy import DataEncryptionPolicy, DataEncryptionPolicyManager
import os
from typing import List
from pyspark.sql.functions import udf, col, lit, when, collect_list
from pyspark.sql.types import StringType
from aiops_encrypt.vault_key_util import VaultKeyUtil
from aiops_encrypt.aes_cbc_encryption_strategy import AesCbcEncryptionStrategy
from aiops_encrypt.aes_gcm_96_encryption_strategy import AesGcm96EncryptionStrategy
from aiops_encrypt.vault_remote_encryption_strategy import VaultRemoteEncryptionStrategy
from aiops_encrypt.vault_local_encryption_strategy import VaultLocalEncryptionStrategy
from uuid import uuid4
from datetime import datetime



class MessagingInboundAndVoidOutboundBase(AbstractPipelineStep):
    """
    Performs scaffolding synchronous processing for MessagingInboundAndVoidOutbound. Business logic is delegated to the subclass.

    GENERATED CODE - DO NOT MODIFY (add your customizations in MessagingInboundAndVoidOutbound).

    Generated from: templates/data-delivery-pyspark/synchronous.processor.base.py.vm
    """

    logger = LogManager.get_instance().get_logger('MessagingInboundAndVoidOutboundBase')
    step_phase = 'MessagingInboundAndVoidOutbound'
    bomIdentifier = "Unspecified MessagingInboundAndVoidOutbound BOM identifier"

    def __init__(self, data_action_type, descriptive_label):
        super().__init__(data_action_type, descriptive_label)

        self.set_metadata_api_service(HiveMetadataAPIService())
        self.messaging_config = MessagingConfig()
        self.consumer = KafkaConsumer("inboundChannel", **self.get_consumer_configs())


    def get_consumer_configs(self) -> dict:
        """
        Returns the configurations for the kafka consumer. Override this method to specify your own configurations.
        """
        return {
            'api_version': (2, 0, 2),
            'bootstrap_servers': [self.messaging_config.server()],
            'group_id': 'MessagingInboundAndVoidOutbound',
            'auto_offset_reset': 'earliest'
        }


    def execute_step(self) -> None:
        """
        Executes this step.
        """
        self.consume_from_kafka()


    def consume_from_kafka(self) -> None:
        for message in self.consumer:
            start = time_ns()
            MessagingInboundAndVoidOutboundBase.logger.info('START: step execution...')

            message_value = message.value.decode('utf-8')
            inbound = self.check_and_apply_encryption_policy(message_value)

            run_id = uuid4()
            job_name = self.get_job_name()
            default_namespace = self.get_default_namespace()
            parent_run_facet = PipelineBase().get_pipeline_run_as_parent_run_facet()
            event_data = self.create_base_lineage_event_data()
            start_time = datetime.utcnow()
            self.record_lineage(self.create_lineage_start_event(run_id=run_id,job_name=job_name,default_namespace=default_namespace,parent_run_facet=parent_run_facet, event_data=event_data, start_time=start_time))
            try:
                self.execute_step_impl(inbound)
                end_time = datetime.utcnow()
                self.record_lineage(self.create_lineage_complete_event(run_id=run_id,job_name=job_name,default_namespace=default_namespace,parent_run_facet=parent_run_facet, event_data=event_data, start_time=start_time, end_time=end_tine))
            except Exception as error:
                self.logger.exception(
                    "An exception occurred while executing "
                    + self.get_data_action_descriptive_label()
                )
                self.record_lineage(self.create_lineage_fail_event(run_id=run_id,job_name=job_name,default_namespace=default_namespace,parent_run_facet=parent_run_facet, event_data=event_data, start_time=start_time, end_time=datetime.utcnow(), error=error))
                PipelineBase().record_pipeline_lineage_fail_event()
                raise Exception(error)

            self.record_provenance()


            self.consumer.commit()

            stop = time_ns()
            MessagingInboundAndVoidOutboundBase.logger.info('COMPLETE: step execution completed in %sms' % ((stop - start) / 1000000))

        self.consumer.close()


    @abstractmethod
    def execute_step_impl(self, inbound: str) -> None:
        """
        This method performs the business logic of this step, 
        and should be implemented in MessagingInboundAndVoidOutbound.
        """
        pass





    def check_and_apply_encryption_policy(self, inbound: str) -> None:
        """
        Checks for encryption policies and applies encryption to the designated fields.
        If no policies are found then the original data is returned.
        """

        MessagingInboundAndVoidOutboundBase.logger.warn('Encryption is not yet supported for messaging without specifying an inbound record type!')
        MessagingInboundAndVoidOutboundBase.logger.warn('If desired, please add encryption manually by overriding check_and_apply_encryption_policy()!')
        return inbound


    def aiops_encrypt_aes_udf(self):
        return udf(lambda text: aiops_encrypt_simple_aes(text))


    def aiops_encrypt_vault_udf(self, key):
        return udf(lambda text: aiops_encrypt_with_vault_key(key, text))


    def apply_encryption_to_dataset(self, inbound: str, fields_to_update: List[str], algorithm: str) -> str:
        '''
            This method applies encryption to the given fields
        '''
        MessagingInboundAndVoidOutboundBase.logger.info('applying encryption')


        # some other text
        return_payload = []
        for encrypt_field in fields_to_update:
            if(algorithm == 'VAULT_ENCRYPT'):
                # Because of the restrictive nature of PySpark UDF's we have to retrieve the Vault key outside of
                # the udf call to avoid threading errors
                vault_key_util = VaultKeyUtil.get_instance()
                vault_key = vault_key_util.get_vault_key_encoded()
                return_payload = inbound.withColumn(encrypt_field, self.aiops_encrypt_vault_udf(vault_key)(col(encrypt_field)))
            else:
                return_payload = inbound.withColumn(encrypt_field, self.aiops_encrypt_aes_udf()(col(encrypt_field)))

            return_payload.show()

        return return_payload


    def get_fields_list(self, inbound: str) -> List[str]:
        '''
            This method gets the field names from the given data type
        '''
        # Get the column names
        return inbound.columns
