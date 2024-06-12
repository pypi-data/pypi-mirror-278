###
# #%L
# aiSSEMBLE::Test::MDA::Machine Learning::Inference
# %%
# Copyright (C) 2021 Booz Allen
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from abc import ABC
from re import fullmatch
from typing import List


class EventOutcomeBase(ABC):
    """
    Base implementation of the eventOutcome dictionary type from ElasticCommonSchemaDictionary.

    GENERATED CODE - DO NOT MODIFY (add your customizations in EventOutcome).

    Generated from: templates/data-delivery-data-records/dictionary.type.base.py.vm
    """

    FORMATS: List[str] = ['^(success|failure|unknown)$']


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
        self.validate_format()


    def validate_format(self) -> None:
        if self._value and self._value.strip():
            validFormat = False
            for format in EventOutcomeBase.FORMATS:
                if fullmatch(format, self._value):
                    validFormat = True
                    break

            if not validFormat:
                raise ValueError('EventOutcome value of \'%s\' did not match any valid formats' % self._value)
