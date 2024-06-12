import abc
import datetime
import random
from typing import Any, Dict, Generic, Optional, Set, TypeVar
from uuid import UUID

import pendulum
from pydantic import (
    Field,
    ValidationInfo,
    computed_field,
    field_validator,
    model_validator,
)

from supamodel._abc import BaseModel, Data

DataT = TypeVar("DataT", bound=Data)
InputModelT = TypeVar("InputModelT", bound=BaseModel)


class DataBox(BaseModel, Generic[DataT]):
    data: Optional[DataT] = None

    def is_list(self) -> bool:
        return isinstance(self.data, list)

    def is_dict(self) -> bool:
        return isinstance(self.data, dict)

    def pick_one(self) -> DataT:
        """
        Selects and returns a random item from the data.

        If the data is a list, a random item from the list is returned.
        If the data is a dictionary, a random item from the dictionary values is returned.
        If the data is neither a list nor a dictionary, the data itself is returned.

        Returns:
            Any: A random item from the data.
        """
        if self.is_list():
            return random.choice(self.data)
        elif self.is_dict():
            return random.choice(list(self.data.values()))
        return self.data

    # Add iterator methods if the data is a list
    def __iter__(self):
        if self.is_list():
            return iter(self.data)
        return iter([])

    def __getitem__(self, item):
        if self.is_list():
            return self.data[item]
        return None

    def __len__(self):
        if self.is_list():
            return len(self.data)
        return 0

    def __contains__(self, item):
        if self.is_list():
            return item in self.data
        return False


class AssetData(BaseModel, Generic[InputModelT]):
    """
    Represents asset data.

    Attributes:
        _asset_id (Union[UUID, str, None]): The asset ID.
        data (Union[list[InputModelT], InputModelT, None]): The asset data.

    Methods:
        asset_id (property): Gets the asset ID.
        asset_id (setter): Sets the asset ID.
        exclude_list: Excludes the first item from the data list.
        check_data: Checks the validity of the asset data.
        is_data_object: Checks if the asset data is an object.
        is_data_list: Checks if the asset data is a list.
        save_dump: Saves the asset data as a dictionary.
        asset_dump: Returns a dictionary representation of the asset data.
    """

    asset_id: UUID | str | None = Field(None, exclude=True, repr=False)
    data: list[InputModelT] | InputModelT | None = None

    # @computed_field
    # @property
    # def asset_id(self) -> str:
    #     return str(self._asset_id)

    # @asset_id.setter
    # def asset_id(self, value: str) -> str:
    #     self._asset_id = value

    def exclude_list(self) -> Dict:
        """
        Excludes the first item from the data list.

        Returns:
            None: If the data list is empty or not a list.
            Dict: The dictionary representation of the excluded item.
        """
        if self.is_list() and self.data:
            item = self.data[0]
            item.model_dump()
            return
        return

    @model_validator(mode="after")
    def check_data(self) -> Any:
        """
        Checks the validity of the asset data.

        Returns:
            Any: The instance of the class if the data is valid.

        Raises:
            ValueError: If the asset ID is None when adding data.
        """
        if self.data is None:
            return self
        if self.asset_id is None:
            raise ValueError("Asset ID is required when adding data")
        if isinstance(self.data, list):
            return self
        if isinstance(self.data, (BaseModel, Data)):
            self.data = [self.data]
            return self
        return self

    def is_data_object(self) -> bool:
        """
        Checks if the asset data is an object.

        Returns:
            bool: True if the asset data is an object, False otherwise.
        """
        return isinstance(self.data, InputModelT)

    def is_data_list(self) -> bool:
        """
        Checks if the asset data is a list.

        Returns:
            bool: True if the asset data is a list, False otherwise.
        """
        return isinstance(self.data, list)

    def save_dump(self) -> list[Dict]:
        """
        Saves the asset data as a dictionary.

        Returns:
            Dict: The dictionary representation of the asset data.
        """
        return self.model_dump(mode="json", exclude_none=True).get("data", [])

    def container_dump(self) -> list[Dict]:
        """
        Returns a dictionary representation of the asset data.

        Returns:
            Dict: The dictionary representation of the asset data.
        """
        records = self.save_dump()
        for record in records:
            record["asset_id"] = self.asset_id

        return records


class Handler(abc.ABC, BaseModel):

    @abc.abstractmethod
    def required(self) -> Set[str]:
        # Can use a set or list to store the required fields and exclude them from the model_dump
        # It's also possible to access those fields and add them into any list of dictionaries from a model dump.
        # It's an improvement to the AssetData class.
        raise NotImplementedError

    def required_dict(self) -> Dict:
        return self.model_dump(include=self.required(), exclude_none=True)

    def exclude_required(self) -> Dict:
        return self.model_dump(exclude=self.required(), exclude_none=True)


class Metric(BaseModel):
    type_: str = Field(
        ...,
        alias="type",
        description="The type of entity the metric is associated with (user, portfolio, performance, server, etc.).",
    )
    name: str = Field(..., alias="name", description="The name of the metric.")
    value: float = Field(..., alias="value", description="The value of the metric.")
    timestamp: datetime.datetime = Field(
        ...,
        alias="timestamp",
        description="The timestamp when the metric was recorded.",
    )
    metadata: Optional[Dict] = Field(
        {},
        alias="metadata",
        description="Additional metadata associated with the metric.",
    )


class TimeData(BaseModel):
    start_time: pendulum.DateTime = Field(
        ..., alias="startTime", description="The start time of the event or activity."
    )
    end_time: pendulum.DateTime = Field(
        ..., alias="endTime", description="The end time of the event or activity."
    )

    # duration: pendulum.Duration = Field(
    #     None,
    #     alias="duration",
    #     description="The duration of the event or activity (calculated from start_time and end_time)."
    # )
    timezone: str = Field(
        "UTC",
        alias="timezone",
        description="The timezone of the start_time and end_time.",
    )
    metadata: Optional[Dict] = Field(
        {},
        alias="metadata",
        description="Additional metadata associated with the time data.",
    )

    @computed_field
    def duration(self) -> pendulum.Duration:
        dur = self.end_time - self.start_time

        return dur

    @field_validator("end_time", mode="before")
    @classmethod
    def check_end_before_start(
        cls, val: pendulum.datetime, info: ValidationInfo
    ) -> pendulum.datetime:
        if (
            "start_time" in info.data
            and info.data.get("start_time")
            and val <= info.data.get("start_time")
        ):
            message = "end_time must be after start_time"
            raise ValueError(message)
        return val

    # @validator("end_time")
    # def end_time_after_start_time(cls, v, values):
    #     if "start_time" in values and v <= values["start_time"]:
    #         raise ValueError("end_time must be after start_time")
    #     return v


def main():
    data = Data(name="OpenBB", value=42)
    print(data)


if __name__ == "__main__":
    main()
