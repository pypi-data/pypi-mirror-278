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
from ...dictionary.decimal_with_validation import DecimalWithValidation
from ...dictionary.float_with_validation import FloatWithValidation
from ...dictionary.integer_with_validation import IntegerWithValidation
from ...dictionary.string_with_validation import StringWithValidation
from decimal import Decimal
from .record_with_validation_field import RecordWithValidationField
from typing import Any, Dict
import jsonpickle

class RecordWithValidationBase(ABC):
    """
    Base implementation of the Record for RecordWithValidation.

    GENERATED CODE - DO NOT MODIFY (add your customizations in RecordWithValidation).

    Generated from: templates/data-delivery-data-records/record.base.py.vm
    """

    def __init__(self):
        """
        Default constructor for this record.
        """
        self._string_validation: StringWithValidation = None
        self._integer_validation: IntegerWithValidation = None
        self._decimal_validation: DecimalWithValidation = None
        self._float_validation: FloatWithValidation = None
        self._required_simple_type: str = None
        self._required_complex_type: StringWithValidation = None


    @classmethod
    def from_dict(cls, dict_obj: Dict[str, Any]):
        """
        Creates a record with the given dictionary's data.
        """
        record = cls()
        if dict_obj is not None:
            if dict_obj.get('stringValidation') is not None:
                record.string_validation = StringWithValidation(dict_obj.get('stringValidation'))
            else:
                record.string_validation = None

            if dict_obj.get('integerValidation') is not None:
                record.integer_validation = IntegerWithValidation(dict_obj.get('integerValidation'))
            else:
                record.integer_validation = None

            if dict_obj.get('decimalValidation') is not None:
                record.decimal_validation = DecimalWithValidation(dict_obj.get('decimalValidation'))
            else:
                record.decimal_validation = None

            if dict_obj.get('floatValidation') is not None:
                record.float_validation = FloatWithValidation(dict_obj.get('floatValidation'))
            else:
                record.float_validation = None

            record.required_simple_type = dict_obj.get('requiredSimpleType')

            if dict_obj.get('requiredComplexType') is not None:
                record.required_complex_type = StringWithValidation(dict_obj.get('requiredComplexType'))
            else:
                record.required_complex_type = None

        return record


    def as_dict(self) -> Dict[str, Any]:
        """
        Returns this record as a dictionary.
        """
        dict_obj = dict()

        if self.string_validation is not None:
            dict_obj['stringValidation'] = self.string_validation.value
        else:
            dict_obj['stringValidation'] = None
        if self.integer_validation is not None:
            dict_obj['integerValidation'] = self.integer_validation.value
        else:
            dict_obj['integerValidation'] = None
        if self.decimal_validation is not None:
            dict_obj['decimalValidation'] = self.decimal_validation.value
        else:
            dict_obj['decimalValidation'] = None
        if self.float_validation is not None:
            dict_obj['floatValidation'] = self.float_validation.value
        else:
            dict_obj['floatValidation'] = None
        dict_obj['requiredSimpleType'] = self.required_simple_type
        if self.required_complex_type is not None:
            dict_obj['requiredComplexType'] = self.required_complex_type.value
        else:
            dict_obj['requiredComplexType'] = None

        return dict_obj


    @classmethod
    def from_json(cls, json_str: str):
        """
        Creates a record with the given json string's data.
        """
        dict_obj = jsonpickle.decode(json_str)
        return cls.from_dict(dict_obj)


    def as_json(self) -> str:
        """
        Returns this record as a json string.
        """
        return jsonpickle.encode(self.as_dict())


    @property
    def string_validation(self) -> StringWithValidation:
        return self._string_validation


    @string_validation.setter
    def string_validation(self, string_validation: StringWithValidation) -> None:
        self._string_validation = string_validation


    @property
    def integer_validation(self) -> IntegerWithValidation:
        return self._integer_validation


    @integer_validation.setter
    def integer_validation(self, integer_validation: IntegerWithValidation) -> None:
        self._integer_validation = integer_validation


    @property
    def decimal_validation(self) -> DecimalWithValidation:
        return self._decimal_validation


    @decimal_validation.setter
    def decimal_validation(self, decimal_validation: DecimalWithValidation) -> None:
        self._decimal_validation = decimal_validation


    @property
    def float_validation(self) -> FloatWithValidation:
        return self._float_validation


    @float_validation.setter
    def float_validation(self, float_validation: FloatWithValidation) -> None:
        self._float_validation = float_validation


    @property
    def required_simple_type(self) -> str:
        return self._required_simple_type


    @required_simple_type.setter
    def required_simple_type(self, required_simple_type: str) -> None:
        self._required_simple_type = required_simple_type


    @property
    def required_complex_type(self) -> StringWithValidation:
        return self._required_complex_type


    @required_complex_type.setter
    def required_complex_type(self, required_complex_type: StringWithValidation) -> None:
        self._required_complex_type = required_complex_type


    def validate(self) -> None:
        """
        Performs the validation for this record.
        """
        self.validate_fields()


    def validate_fields(self) -> None:
        if self.string_validation is not None:
            self.string_validation.validate()

        if self.integer_validation is not None:
            self.integer_validation.validate()

        if self.decimal_validation is not None:
            self.decimal_validation.validate()

        if self.float_validation is not None:
            self.float_validation.validate()

        if self.required_simple_type is None:
            raise ValueError('Field \'requiredSimpleType\' is required')

        if self.required_complex_type is None:
            raise ValueError('Field \'requiredComplexType\' is required')
        else:
            self.required_complex_type.validate()



    def get_value_by_field(self, field: RecordWithValidationField) -> any:
        """
        Returns the value of the given field for this record.
        """
        value = None
        if field == RecordWithValidationField.STRING_VALIDATION:
            value = self.string_validation.value if self.string_validation is not None else None
        if field == RecordWithValidationField.INTEGER_VALIDATION:
            value = self.integer_validation.value if self.integer_validation is not None else None
        if field == RecordWithValidationField.DECIMAL_VALIDATION:
            value = self.decimal_validation.value if self.decimal_validation is not None else None
        if field == RecordWithValidationField.FLOAT_VALIDATION:
            value = self.float_validation.value if self.float_validation is not None else None
        if field == RecordWithValidationField.REQUIRED_SIMPLE_TYPE:
            value = self.required_simple_type
        if field == RecordWithValidationField.REQUIRED_COMPLEX_TYPE:
            value = self.required_complex_type.value if self.required_complex_type is not None else None

        return value
