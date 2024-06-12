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
from ...record.custom_record import CustomRecord
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



class NativeInboundWithCustomRecordTypeBase(AbstractPipelineStep):
    """
    Performs scaffolding synchronous processing for NativeInboundWithCustomRecordType. Business logic is delegated to the subclass.

    GENERATED CODE - DO NOT MODIFY (add your customizations in NativeInboundWithCustomRecordType).

    Generated from: templates/data-delivery-pyspark/synchronous.processor.base.py.vm
    """

    logger = LogManager.get_instance().get_logger('NativeInboundWithCustomRecordTypeBase')
    step_phase = 'NativeInboundWithCustomRecordType'
    bomIdentifier = "Unspecified NativeInboundWithCustomRecordType BOM identifier"

    def __init__(self, data_action_type, descriptive_label):
        super().__init__(data_action_type, descriptive_label)

        self.set_metadata_api_service(HiveMetadataAPIService())


    def execute_step(self, inbound: CustomRecord) -> None:
        """
        Executes this step.
        """
        start = time_ns()
        NativeInboundWithCustomRecordTypeBase.logger.info('START: step execution...')

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
        NativeInboundWithCustomRecordTypeBase.logger.info('COMPLETE: step execution completed in %sms' % ((stop - start) / 1000000))



    @abstractmethod
    def execute_step_impl(self, inbound: CustomRecord) -> None:
        """
        This method performs the business logic of this step, 
        and should be implemented in NativeInboundWithCustomRecordType.
        """
        pass





    def check_and_apply_encryption_policy(self, inbound: CustomRecord) -> None:
        """
        Checks for encryption policies and applies encryption to the designated fields.
        If no policies are found then the original data is returned.
        """

        return_payload = inbound
        NativeInboundWithCustomRecordTypeBase.logger.info('Checking encryption policies')

        # Check if the KRAUSENING_BASE is set in the environment and use a default if it isn't
        if not os.environ.get('KRAUSENING_BASE'):
            NativeInboundWithCustomRecordTypeBase.logger.warn('KRAUSENING_BASE environment variable was not set.  Using default path -> ./config')
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
                    NativeInboundWithCustomRecordTypeBase.logger.info('Encryption policy does not apply to this phase: ' + self.step_phase)

        return return_payload




    def apply_encryption_to_dataset(self, inbound: CustomRecord, fields_to_update: List[str], algorithm: str) -> CustomRecord:
        '''
            This method applies encryption to the given fields
        '''
        NativeInboundWithCustomRecordTypeBase.logger.info('applying encryption')


        # return type is a single custom data type
        aiops_encrypt = AesCbcEncryptionStrategy()
        if(algorithm == 'VAULT_ENCRYPT'):
            aiops_encrypt = VaultRemoteEncryptionStrategy()

        for column in fields_to_update:
            encrypted_column_value = aiops_encrypt.encrypt(getattr(record, column))
            # Depending on the encryption algorithm the return value may be bytes or bytesarray which requires decoding
            try:
                encrypted_column_value = encrypted_column_value.decode('utf-8')
            except (UnicodeDecodeError, AttributeError):
                pass

            setattr(record, column, encrypted_column_value)

        return_payload = inbound

        return return_payload


    def get_fields_list(self, inbound: CustomRecord) -> List[str]:
        '''
            This method gets the field names from the given data type
        '''
        return [p for p in dir(CustomRecord) if isinstance(getattr(CustomRecord,p),property)]
