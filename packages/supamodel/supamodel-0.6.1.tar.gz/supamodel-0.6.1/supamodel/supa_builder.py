"""
# Supabase API Support Models

This module contains the API support models for the supamodel package and beyond. For instance, the `ResponseModel` class is used to represent the response from an API request. 


The `SupaModel` class is used to represent a model that is stored in a Supabase database. We'll also have DecoratedRequestBuilders and SupaTypes in this module. They'll represent components that are used to interact with the Supabase API.


"""

import uuid
from typing import Any, Generic, TypeVar

from postgrest._sync.request_builder import SyncQueryRequestBuilder

from supamodel._abc import Data, Dataset
from supamodel._client import supabase
from supamodel.utils import cached_classattr, tableize

RespT = TypeVar("RespT", bound=Data)


class ResponseModel(Data, Generic[RespT]):
    data: list[dict[str, Any]] | None = []
    count: int | None = None
    error: str | None = None

    def is_error(self):
        """
        Check if there is an error.

        Returns:
            bool: True if there is an error, False otherwise.
        """
        return self.error is not None

    def empty(self) -> bool:
        """
        Check if the data is empty.

        Returns:
            bool: True if the data is empty, False otherwise.
        """
        return self.data is None or len(self.data) == 0

    def is_success(self) -> bool:
        return self.error is None and self.data is not None

    def is_failure(self) -> bool:
        return bool(self.error) and self.empty()

    def dataset(self) -> Dataset[RespT]:
        return Dataset[RespT](data=self.data)


class SupaTable(Data):

    @classmethod
    def table_name(cls) -> str:
        return tableize(cls.__name__)

    @cached_classattr
    def table(cls) -> SyncQueryRequestBuilder:
        return supabase.table(cls.table_name())

    @cached_classattr
    def class_type(cls):
        """
        Returns the class type of an instance created from the model. It must be an instance so tha we don't get the parent class type.

        It would get ModelMetaClass instead of the current model normally instead.
        """
        instance = cls.model_construct({})
        return type(instance)

    @cached_classattr
    def resolved_type(cls):
        """
        Returns the resolved type of an instance created from the model. It must be an instance so that we don't get the parent class type.

        It would get ModelMetaClass instead of the current model normally instead.
        """
        instance = cls.model_construct({})
        return type(instance)

    @cached_classattr
    def dataset(cls):
        """
        Returns the dataset associated with the class.
        """
        return Dataset[cls.class_type]


class SupaRecord(Data):
    id: uuid.UUID | None = None

    @classmethod
    def table_name(cls) -> str:
        return tableize(cls.__name__)

    @cached_classattr
    def table(cls) -> SyncQueryRequestBuilder:
        return supabase.table(cls.table_name())

    @cached_classattr
    def class_type(cls):
        """
        Returns the class type of an instance created from the model. It must be an instance so tha we don't get the parent class type.

        It would get ModelMetaClass instead of the current model normally instead.
        """
        instance = cls.model_construct({})
        return type(instance)

    @cached_classattr
    def resolved_type(cls):
        """
        Returns the resolved type of an instance created from the model. It must be an instance so that we don't get the parent class type.

        It would get ModelMetaClass instead of the current model normally instead.
        """
        instance = cls.model_construct({})
        return type(instance)

    @cached_classattr
    def dataset(cls):
        """
        Returns the dataset associated with the class.
        """
        return Dataset[cls.class_type]


# llm - ChatAntropic()
# prompt = PromptTemplate("ChatAntropic")
