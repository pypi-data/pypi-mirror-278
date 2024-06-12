###
# #%L
# aiSSEMBLE::Test::MDA::Data Delivery Pyspark
# %%
# Copyright (C) 2021 Booz Allen
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from __future__ import annotations
from enum import Enum
from typing import List
from ...dictionary.type_with_policies import TypeWithPolicies

class RecordWithPoliciesField(Enum):
    """
    Enum to represent the fields of a RecordWithPolicies record.

    GENERATED CODE - DO NOT MODIFY

    Originally generated from: templates/data-delivery-data-records/record.field.enum.py.vm
    """

    FIELD_WITH_POLICIES = 0, 'fieldDriftPolicy', 'fieldEthicsPolicy', 'fieldProtectionPolicy'
    FIELD_WITH_DICTIONARY_TYPE_POLICIES = 1, TypeWithPolicies.DRIFT_POLICY, TypeWithPolicies.ETHICS_POLICY, TypeWithPolicies.PROTECTION_POLICY
    FIELD_WITH_DICTIONARY_TYPE_POLICIES_OVERRIDDEN = 2, 'overriddenDriftPolicy', 'overriddenEthicsPolicy', 'overriddenProtectionPolicy'


    def __new__(cls, index: int, drift_policy: str, ethics_policy: str, protection_policy: str):
        field = object.__new__(cls)
        field.index = index
        field._drift_policy = drift_policy
        field._ethics_policy = ethics_policy
        field._protection_policy = protection_policy
        return field


    @property
    def drift_policy(self) -> str:
        return self._drift_policy


    def has_drift_policy(self) -> bool:
        return True if self._drift_policy and self._drift_policy.strip() else False


    @property
    def ethics_policy(self) -> str:
        return self._ethics_policy


    def has_ethics_policy(self) -> bool:
        return True if self._ethics_policy and self._ethics_policy.strip() else False


    @property
    def protection_policy(self) -> str:
        return self._protection_policy


    def has_protection_policy(self) -> bool:
        return True if self._protection_policy and self._protection_policy.strip() else False


    @classmethod
    def get_fields_with_drift_policy(cls) -> List[RecordWithPoliciesField]:
        """
        Returns the list of fields that have a drift policy.
        """
        fields_with_drift_policy = []
        for field in RecordWithPoliciesField:
            if field.has_drift_policy():
                fields_with_drift_policy.append(field)

        return fields_with_drift_policy

    @classmethod
    def get_fields_with_ethics_policy(cls) -> List[RecordWithPoliciesField]:
        """
        Returns the list of fields that have an ethics policy.
        """
        fields_with_ethics_policy = []
        for field in RecordWithPoliciesField:
            if field.has_ethics_policy():
                fields_with_ethics_policy.append(field)

        return fields_with_ethics_policy

    @classmethod
    def get_fields_with_protection_policy(cls) -> List[RecordWithPoliciesField]:
        """
        Returns the list of fields that have a protection policy.
        """
        fields_with_protection_policy = []
        for field in RecordWithPoliciesField:
            if field.has_protection_policy():
                fields_with_protection_policy.append(field)

        return fields_with_protection_policy
