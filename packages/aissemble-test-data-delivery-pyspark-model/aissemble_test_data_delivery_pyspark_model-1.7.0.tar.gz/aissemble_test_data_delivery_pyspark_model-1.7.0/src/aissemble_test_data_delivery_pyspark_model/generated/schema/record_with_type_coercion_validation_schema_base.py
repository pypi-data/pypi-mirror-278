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
from pyspark.sql.types import FloatType
from pyspark.sql.types import IntegerType


class RecordWithTypeCoercionValidationSchemaBase(ABC):
    """
    Base implementation of the PySpark schema for RecordWithTypeCoercionValidation.

    GENERATED CODE - DO NOT MODIFY (add your customizations in RecordWithTypeCoercionValidation).

    Generated from: templates/data-delivery-data-records/pyspark.schema.base.py.vm
    """

    INTEGER_VALIDATION_COLUMN: str = 'integerValidation'
    FLOAT_VALIDATION_COLUMN: str = 'floatValidation'


    def __init__(self):
        self._schema = StructType()

        self.add(RecordWithTypeCoercionValidationSchemaBase.INTEGER_VALIDATION_COLUMN, IntegerType(), True)
        self.add(RecordWithTypeCoercionValidationSchemaBase.FLOAT_VALIDATION_COLUMN, FloatType(), True)


    def cast(self, dataset: DataFrame) -> DataFrame:
        """
        Returns the given dataset cast to this schema.
        """
        integer_validation_type = self.get_data_type(RecordWithTypeCoercionValidationSchemaBase.INTEGER_VALIDATION_COLUMN)
        float_validation_type = self.get_data_type(RecordWithTypeCoercionValidationSchemaBase.FLOAT_VALIDATION_COLUMN)

        return dataset \
            .withColumn(RecordWithTypeCoercionValidationSchemaBase.INTEGER_VALIDATION_COLUMN, dataset[RecordWithTypeCoercionValidationSchemaBase.INTEGER_VALIDATION_COLUMN].cast(integer_validation_type)) \
            .withColumn(RecordWithTypeCoercionValidationSchemaBase.FLOAT_VALIDATION_COLUMN, dataset[RecordWithTypeCoercionValidationSchemaBase.FLOAT_VALIDATION_COLUMN].cast(float_validation_type))


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
        data_with_validations = data_with_validations.withColumn("INTEGER_VALIDATION_GREATER_THAN_MIN", col("INTEGER_VALIDATION").cast('double') >= 100)
        data_with_validations = data_with_validations.withColumn("INTEGER_VALIDATION_LESS_THAN_MAX", col("INTEGER_VALIDATION").cast('double') <= 999)
        data_with_validations = data_with_validations.withColumn("FLOAT_VALIDATION_GREATER_THAN_MIN", col("FLOAT_VALIDATION").cast('double') >= 12.345)
        data_with_validations = data_with_validations.withColumn("FLOAT_VALIDATION_LESS_THAN_MAX", col("FLOAT_VALIDATION").cast('double') <= 100.0)
        data_with_validations = data_with_validations.withColumn("FLOAT_VALIDATION_MATCHES_SCALE", col("FLOAT_VALIDATION").cast(StringType()).rlike(r"^[0-9]*(?:\.[0-9]{0,3})?$"))

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
