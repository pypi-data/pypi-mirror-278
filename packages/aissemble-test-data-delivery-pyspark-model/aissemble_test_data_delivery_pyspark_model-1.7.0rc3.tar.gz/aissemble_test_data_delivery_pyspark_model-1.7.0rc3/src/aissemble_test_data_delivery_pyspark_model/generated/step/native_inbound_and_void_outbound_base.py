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

def aiops_encrypt_simple_aes(plain_text):
    '''
    Pyspark User Defined Function for running encryption on columns.
    Note: must be registered with the spark session.
    return The cipher text
    '''
    # TODO: Due to issues with defining the udf inside the class we are defining them outside.  It would be good to revisit this issue in future releases.
    if (plain_text is not None):
        if not os.environ.get('KRAUSENING_BASE'):
            NativeInboundAndVoidOutboundBase.logger.warn('KRAUSENING_BASE environment variable was not set.  Using default path -> ./config')
            os.environ['KRAUSENING_BASE'] = 'krausening/base/'

        encryption_strategy = AesCbcEncryptionStrategy()

        encrypted_column_value = encryption_strategy.encrypt(plain_text)
        encrypted_column_value = encrypted_column_value.decode('utf-8')

        return encrypted_column_value
    else:
        return ''


def aiops_encrypt_with_vault_key(key, plain_text):
    '''
    Pyspark User Defined Function for running encryption on columns.
    Vault supplies an AES GCM 96 encryption key which will be used here.
    Note: must be registered with the spark session.
    return The cipher text
    '''
    if (plain_text is not None):
        if not os.environ.get('KRAUSENING_BASE'):
            NativeInboundAndVoidOutboundBase.logger.warn('KRAUSENING_BASE environment variable was not set.  Using default path -> ./config')
            os.environ['KRAUSENING_BASE'] = 'krausening/base/'

        encryption_strategy = AesGcm96EncryptionStrategy(key)

        encrypted_column_value = encryption_strategy.encrypt(plain_text)
        encrypted_column_value = encrypted_column_value.decode('utf-8')

        return encrypted_column_value
    else:
        return ''


class NativeInboundAndVoidOutboundBase(AbstractPipelineStep):
    """
    Performs scaffolding synchronous processing for NativeInboundAndVoidOutbound. Business logic is delegated to the subclass.

    GENERATED CODE - DO NOT MODIFY (add your customizations in NativeInboundAndVoidOutbound).

    Generated from: templates/data-delivery-pyspark/synchronous.processor.base.py.vm
    """

    logger = LogManager.get_instance().get_logger('NativeInboundAndVoidOutboundBase')
    step_phase = 'NativeInboundAndVoidOutbound'
    bomIdentifier = "Unspecified NativeInboundAndVoidOutbound BOM identifier"

    def __init__(self, data_action_type, descriptive_label):
        super().__init__(data_action_type, descriptive_label)

        self.set_metadata_api_service(HiveMetadataAPIService())


    def execute_step(self, inbound: DataFrame) -> None:
        """
        Executes this step.
        """
        start = time_ns()
        NativeInboundAndVoidOutboundBase.logger.info('START: step execution...')

        inbound = self.check_and_apply_encryption_policy(inbound)

        run_id = uuid4()
        parent_run_facet = PipelineBase().get_pipeline_run_as_parent_run_facet()
        job_name = self.get_job_name()
        default_namespace = self.get_default_namespace()
        event_data = self.create_base_lineage_event_data()
        start_time = datetime.utcnow()
        self.record_lineage(self.create_lineage_start_event(run_id=run_id,job_name=job_name,default_namespace=default_namespace,parent_run_facet=parent_run_facet, event_data=event_data, start_time=start_time))
        try:
            self.execute_step_impl(inbound)
            end_time = datetime.utcnow()
            self.record_lineage(self.create_lineage_complete_event(run_id=run_id,job_name=job_name,default_namespace=default_namespace,parent_run_facet=parent_run_facet, event_data=event_data, start_time=start_time, end_time=end_time))
        except Exception as error:
            self.logger.exception(
                "An exception occurred while executing "
                + self.get_data_action_descriptive_label()
            )
            self.record_lineage(self.create_lineage_fail_event(run_id=run_id,job_name=job_name,default_namespace=default_namespace,parent_run_facet=parent_run_facet, event_data=event_data, start_time=start_time, end_time=datetime.utcnow(), error=error))
            PipelineBase().record_pipeline_lineage_fail_event()
            raise Exception(error)

        self.record_provenance()


        stop = time_ns()
        NativeInboundAndVoidOutboundBase.logger.info('COMPLETE: step execution completed in %sms' % ((stop - start) / 1000000))



    @abstractmethod
    def execute_step_impl(self, inbound: DataFrame) -> None:
        """
        This method performs the business logic of this step, 
        and should be implemented in NativeInboundAndVoidOutbound.
        """
        pass





    def check_and_apply_encryption_policy(self, inbound: DataFrame) -> None:
        """
        Checks for encryption policies and applies encryption to the designated fields.
        If no policies are found then the original data is returned.
        """

        return_payload = inbound
        NativeInboundAndVoidOutboundBase.logger.info('Checking encryption policies')

        # Check if the KRAUSENING_BASE is set in the environment and use a default if it isn't
        if not os.environ.get('KRAUSENING_BASE'):
            NativeInboundAndVoidOutboundBase.logger.warn('KRAUSENING_BASE environment variable was not set.  Using default path -> ./config')
            os.environ['KRAUSENING_BASE'] = 'resources/krausening/base/'

        directory = PolicyConfiguration().policiesLocation()

        policy_manager = DataEncryptionPolicyManager.getInstance()
        retrieved_policies = policy_manager.policies

        for key, encrypt_policy in retrieved_policies.items():
            # Encryption policies have a property called encryptPhase.
            # If that property is missing then we should ignore the policy.
            if encrypt_policy.encryptPhase:
                if self.step_phase.lower() == encrypt_policy.encryptPhase.lower():

                    encrypt_fields = encrypt_policy.encryptFields
                    input_fields = self.get_fields_list(inbound)
                    field_intersection = list(set(encrypt_fields) & set(input_fields))

                    return_payload = self.apply_encryption_to_dataset(inbound, field_intersection, encrypt_policy.encryptAlgorithm)
                else:
                    NativeInboundAndVoidOutboundBase.logger.info('Encryption policy does not apply to this phase: ' + self.step_phase)

        return return_payload


    def aiops_encrypt_aes_udf(self):
        return udf(lambda text: aiops_encrypt_simple_aes(text))


    def aiops_encrypt_vault_udf(self, key):
        return udf(lambda text: aiops_encrypt_with_vault_key(key, text))


    def apply_encryption_to_dataset(self, inbound: DataFrame, fields_to_update: List[str], algorithm: str) -> DataFrame:
        '''
            This method applies encryption to the given fields
        '''
        NativeInboundAndVoidOutboundBase.logger.info('applying encryption')


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


    def get_fields_list(self, inbound: DataFrame) -> List[str]:
        '''
            This method gets the field names from the given data type
        '''
        # Get the column names
        return inbound.columns
