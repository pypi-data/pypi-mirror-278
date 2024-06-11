###
# #%L
# aiSSEMBLE::Test::MDA::Data Delivery Pyspark
# %%
# Copyright (C) 2021 Booz Allen
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from abc import ABC


class TypeWithPoliciesBase(ABC):
    """
    Base implementation of the typeWithPolicies dictionary type from PysparkDataDeliveryDictionary.

    GENERATED CODE - DO NOT MODIFY (add your customizations in TypeWithPolicies).

    Generated from: templates/data-delivery-data-records/dictionary.type.base.py.vm
    """

    DRIFT_POLICY: str = 'dictionaryTypeDriftPolicy'
    ETHICS_POLICY: str = 'dictionaryTypeEthicsPolicy'
    PROTECTION_POLICY: str = 'dictionaryTypeProtectionPolicy'


    def __init__(self, value: str):
        if value is not None:
            self._value = str(value)
        else:
            self._value = None


    @property
    def value(self) -> str:
        return self._value


    @value.setter
    def value(self, value: str) -> None:
        if value is not None:
            value = str(value)
            self._value = value
        else:
            self._value = None


    def validate(self) -> None:
        """
        Performs the validation for this dictionary type.
        """
        pass
