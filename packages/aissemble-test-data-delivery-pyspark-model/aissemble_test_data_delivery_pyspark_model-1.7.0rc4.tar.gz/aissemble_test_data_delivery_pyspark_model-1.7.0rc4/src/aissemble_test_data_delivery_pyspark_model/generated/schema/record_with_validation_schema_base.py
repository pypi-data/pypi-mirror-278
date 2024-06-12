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
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.column import Column
from pyspark.sql.types import StructType
from pyspark.sql.types import DataType
from pyspark.sql.functions import col
from typing import List
import types
from pyspark.sql.types import DecimalType
from pyspark.sql.types import FloatType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import StringType


class RecordWithValidationSchemaBase(ABC):
    """
    Base implementation of the PySpark schema for RecordWithValidation.

    GENERATED CODE - DO NOT MODIFY (add your customizations in RecordWithValidation).

    Generated from: templates/data-delivery-data-records/pyspark.schema.base.py.vm
    """

    STRING_VALIDATION_COLUMN: str = 'stringValidation'
    INTEGER_VALIDATION_COLUMN: str = 'integerValidation'
    DECIMAL_VALIDATION_COLUMN: str = 'decimalValidation'
    FLOAT_VALIDATION_COLUMN: str = 'floatValidation'
    REQUIRED_SIMPLE_TYPE_COLUMN: str = 'requiredSimpleType'
    REQUIRED_COMPLEX_TYPE_COLUMN: str = 'requiredComplexType'


    def __init__(self):
        self._schema = StructType()

        self.add(RecordWithValidationSchemaBase.STRING_VALIDATION_COLUMN, StringType(), True)
        self.add(RecordWithValidationSchemaBase.INTEGER_VALIDATION_COLUMN, IntegerType(), True)
        self.add(RecordWithValidationSchemaBase.DECIMAL_VALIDATION_COLUMN, DecimalType(10, 3), True)
        self.add(RecordWithValidationSchemaBase.FLOAT_VALIDATION_COLUMN, FloatType(), True)
        self.add(RecordWithValidationSchemaBase.REQUIRED_SIMPLE_TYPE_COLUMN, StringType(), False)
        self.add(RecordWithValidationSchemaBase.REQUIRED_COMPLEX_TYPE_COLUMN, StringType(), False)


    def cast(self, dataset: DataFrame) -> DataFrame:
        """
        Returns the given dataset cast to this schema.
        """
        string_validation_type = self.get_data_type(RecordWithValidationSchemaBase.STRING_VALIDATION_COLUMN)
        integer_validation_type = self.get_data_type(RecordWithValidationSchemaBase.INTEGER_VALIDATION_COLUMN)
        decimal_validation_type = self.get_data_type(RecordWithValidationSchemaBase.DECIMAL_VALIDATION_COLUMN)
        float_validation_type = self.get_data_type(RecordWithValidationSchemaBase.FLOAT_VALIDATION_COLUMN)
        required_simple_type_type = self.get_data_type(RecordWithValidationSchemaBase.REQUIRED_SIMPLE_TYPE_COLUMN)
        required_complex_type_type = self.get_data_type(RecordWithValidationSchemaBase.REQUIRED_COMPLEX_TYPE_COLUMN)

        return dataset \
            .withColumn(RecordWithValidationSchemaBase.STRING_VALIDATION_COLUMN, dataset[RecordWithValidationSchemaBase.STRING_VALIDATION_COLUMN].cast(string_validation_type)) \
            .withColumn(RecordWithValidationSchemaBase.INTEGER_VALIDATION_COLUMN, dataset[RecordWithValidationSchemaBase.INTEGER_VALIDATION_COLUMN].cast(integer_validation_type)) \
            .withColumn(RecordWithValidationSchemaBase.DECIMAL_VALIDATION_COLUMN, dataset[RecordWithValidationSchemaBase.DECIMAL_VALIDATION_COLUMN].cast(decimal_validation_type)) \
            .withColumn(RecordWithValidationSchemaBase.FLOAT_VALIDATION_COLUMN, dataset[RecordWithValidationSchemaBase.FLOAT_VALIDATION_COLUMN].cast(float_validation_type)) \
            .withColumn(RecordWithValidationSchemaBase.REQUIRED_SIMPLE_TYPE_COLUMN, dataset[RecordWithValidationSchemaBase.REQUIRED_SIMPLE_TYPE_COLUMN].cast(required_simple_type_type)) \
            .withColumn(RecordWithValidationSchemaBase.REQUIRED_COMPLEX_TYPE_COLUMN, dataset[RecordWithValidationSchemaBase.REQUIRED_COMPLEX_TYPE_COLUMN].cast(required_complex_type_type))


    @property
    def struct_type(self) -> StructType:
        """
        Returns the structure type for this schema.
        """
        return self._schema


    @struct_type.setter
    def struct_type(self, struct_type: StructType) -> None:
        raise Exception('Schema structure type should not be set manually!')


    def get_data_type(self, name: str) -> str:
        """
        Returns the data type for a field in this schema.
        """
        data_type = None
        if name in self._schema.fieldNames():
            data_type = self._schema[name].dataType

        return data_type


    def add(self, name: str, data_type: DataType, nullable: bool) -> None:
        """
        Adds a field to this schema.
        """
        self._schema.add(name, data_type, nullable)


    def update(self, name: str, data_type: DataType) -> None:
        """
        Updates the data type of a field in this schema.
        """
        fields = self._schema.fields
        if fields and len(fields) > 0:
            update = StructType()
            for field in fields:
                if field.name == name:
                    update.add(name, data_type, field.nullable)
                else:
                    update.add(field)

            self._schema = update

    def validate_dataset(ingest_dataset: DataFrame) -> DataFrame:
        """
        Validates the given dataset and returns the lists of validated records.
        """
        data_with_validations = ingest_dataset
        data_with_validations = data_with_validations.withColumn("STRING_VALIDATION_GREATER_THAN_MAX_LENGTH", col("STRING_VALIDATION").rlike("^.{5,}"))
        data_with_validations = data_with_validations.withColumn("STRING_VALIDATION_LESS_THAN_MAX_LENGTH", col("STRING_VALIDATION").rlike("^.{50,}").eqNullSafe(False))
        data_with_validations = data_with_validations.withColumn("STRING_VALIDATION_MATCHES_FORMAT", col("STRING_VALIDATION").rlike("example-regex")
            | col("STRING_VALIDATION").rlike("[A-Z]*[1-5]+")
            | col("STRING_VALIDATION").rlike("\\D*"))
        data_with_validations = data_with_validations.withColumn("INTEGER_VALIDATION_GREATER_THAN_MIN", col("INTEGER_VALIDATION").cast('double') >= 100)
        data_with_validations = data_with_validations.withColumn("INTEGER_VALIDATION_LESS_THAN_MAX", col("INTEGER_VALIDATION").cast('double') <= 999)
        data_with_validations = data_with_validations.withColumn("DECIMAL_VALIDATION_GREATER_THAN_MIN", col("DECIMAL_VALIDATION").cast('double') >= 12.345)
        data_with_validations = data_with_validations.withColumn("DECIMAL_VALIDATION_LESS_THAN_MAX", col("DECIMAL_VALIDATION").cast('double') <= 100.0)
        data_with_validations = data_with_validations.withColumn("DECIMAL_VALIDATION_MATCHES_SCALE", col("DECIMAL_VALIDATION").cast(StringType()).rlike(r"^[0-9]*(?:\.[0-9]{0,3})?$"))
        data_with_validations = data_with_validations.withColumn("FLOAT_VALIDATION_GREATER_THAN_MIN", col("FLOAT_VALIDATION").cast('double') >= 12.345)
        data_with_validations = data_with_validations.withColumn("FLOAT_VALIDATION_LESS_THAN_MAX", col("FLOAT_VALIDATION").cast('double') <= 100.0)
        data_with_validations = data_with_validations.withColumn("FLOAT_VALIDATION_MATCHES_SCALE", col("FLOAT_VALIDATION").cast(StringType()).rlike(r"^[0-9]*(?:\.[0-9]{0,3})?$"))
        data_with_validations = data_with_validations.withColumn("REQUIRED_SIMPLE_TYPE_IS_NOT_NULL", col("REQUIRED_SIMPLE_TYPE").isNotNull())
        data_with_validations = data_with_validations.withColumn("REQUIRED_COMPLEX_TYPE_IS_NOT_NULL", col("REQUIRED_COMPLEX_TYPE").isNotNull())
        data_with_validations = data_with_validations.withColumn("REQUIRED_COMPLEX_TYPE_GREATER_THAN_MAX_LENGTH", col("REQUIRED_COMPLEX_TYPE").rlike("^.{5,}"))
        data_with_validations = data_with_validations.withColumn("REQUIRED_COMPLEX_TYPE_LESS_THAN_MAX_LENGTH", col("REQUIRED_COMPLEX_TYPE").rlike("^.{50,}").eqNullSafe(False))
        data_with_validations = data_with_validations.withColumn("REQUIRED_COMPLEX_TYPE_MATCHES_FORMAT", col("REQUIRED_COMPLEX_TYPE").rlike("example-regex")
            | col("REQUIRED_COMPLEX_TYPE").rlike("[A-Z]*[1-5]+")
            | col("REQUIRED_COMPLEX_TYPE").rlike("\\D*"))

        validation_columns = [x for x in data_with_validations.columns if x not in ingest_dataset.columns]

        # Schema for filtering for valid data
        filter_schema = None
        for column_name in validation_columns:
            if isinstance(filter_schema, Column):
                filter_schema = filter_schema & col(column_name).eqNullSafe(True)
            else:
                filter_schema = col(column_name).eqNullSafe(True)

        valid_data = data_with_validations
        # Isolate the valid data and drop validation columns
        if isinstance(filter_schema, Column):
            valid_data = data_with_validations.filter(filter_schema)
        valid_data = valid_data.drop(*validation_columns)
        return valid_data
