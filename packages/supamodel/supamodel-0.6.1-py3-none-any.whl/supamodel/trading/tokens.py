from datetime import datetime
from typing import Dict, Generic, List, Optional, TypeVar

import pandas as pd
import pendulum as pen
from pydantic import (
    BaseModel as _BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_validator,
)
from pydantic.alias_generators import to_camel as to_camel_case

from supamodel._types import TruncatedFloat
from supamodel.enums import TimeInt


class BaseModel(_BaseModel):
    model_config: ConfigDict = ConfigDict(
        arbitrary_types_allowed=True,
        alias_generator=to_camel_case,
        populate_by_name=True,
        extra="ignore",
        use_enum_values=True,
    )


class Bar(BaseModel):
    address: str = Field(..., exclude=True)
    type: TimeInt
    close: float = Field(..., alias="c")
    high: float = Field(..., alias="h")
    low: float = Field(..., alias="l")
    open: float = Field(..., alias="o")
    volume: float = Field(..., alias="v")
    timestamp: datetime = Field(..., alias="unixTime")


class OhlcvData(BaseModel):
    items: List[Bar]


class OhlcvResponse(BaseModel):
    data: OhlcvData
    success: bool


class OverviewExtensions(BaseModel):
    coingecko_id: Optional[str] = None
    website: Optional[str] = None
    telegram: Optional[str] = None
    twitter: Optional[str] = None
    description: Optional[str] = None
    discord: Optional[str] = None
    medium: Optional[str] = None


class TokenItem(BaseModel):
    address: Optional[str] = None
    decimals: Optional[int] = None
    market_cap: Optional[float] = Field(None, alias="mc")
    symbol: Optional[str] = None
    name: Optional[str] = None
    last_trade: Optional[datetime] = Field(None, alias="lastTradeUnixTime")
    volume_change: Optional[float] = Field(0.0, alias="v24hChangePercent")


class TokenList(BaseModel):
    updateUnixTime: Optional[int] = 0
    updateTime: Optional[str] = 0
    tokens: Optional[List[TokenItem]] = 0
    total: Optional[int] = 0


# Method that checks if string is a valid URL
def is_url(s: str) -> bool:
    return s.startswith("http://") or s.startswith("https://")


class AssetOverview(BaseModel):
    address: Optional[str] = None
    decimals: Optional[int] = None
    symbol: Optional[str] = None
    name: Optional[str] = None
    logo_uri: Optional[str] = None
    liquidity: Optional[float] = None
    price: Optional[float] = None
    sell_amount: Optional[int] = None
    buy_amount: Optional[int] = None
    supply: Optional[float] = None
    market_cap: Optional[float] = None
    buy_volume: Optional[float] = None
    sell_volume: Optional[float] = None
    views: Optional[TruncatedFloat] = Field(None)
    unique_views: Optional[TruncatedFloat] = Field(None)
    unique_wallet: Optional[float] = None
    volume: Optional[float] = None
    volume_usd: Optional[float] = None
    number_markets: Optional[int] = None
    price_change1h_percent: Optional[float] = None
    total_trades: Optional[int] = None
    total_trade_volume: Optional[float] = None

    model_config: ConfigDict = ConfigDict(extra="ignore")

    @field_validator("unique_views", mode="before")
    @classmethod
    def check_unique_views(cls, value):
        if (
            value is None
            or value == float("nan")
            or value == float("inf")
            or value == float("-inf")
        ):
            return 0
        return value


class Overview(BaseModel):
    """
    Represents overview data for a specific entity.

    Attributes:
        address (Optional[str]): The address of the entity.
        decimals (Optional[int]): The number of decimal places for the entity's value.
        symbol (Optional[str]): The symbol representing the entity.
        name (Optional[str]): The name of the entity.
        extensions (Optional[OverviewExtensions]): Additional extensions for the entity.
        logo_uri (Optional[str]): The URI of the entity's logo.
        liquidity (Optional[float]): The liquidity value of the entity.
        price (Optional[float]): The price of the entity.
        sell_amount (Optional[int]): The amount of entity sold in the last hour.
        buy_amount (Optional[int]): The amount of entity bought in the last hour.
        supply (Optional[float]): The supply of the entity.
        market_cap (Optional[float]): The market capitalization of the entity.
        buy_volume (Optional[float]): The volume of entity bought in the last hour.
        sell_volume (Optional[float]): The volume of entity sold in the last hour.
        watch (Optional[int]): The number of times the entity is being watched.
        views (Optional[int]): The number of views in the last hour.
        unique_views (Optional[int]): The number of unique views in the last hour.
        unique_wallet (Optional[int]): The number of unique wallets in the last hour.
        volume (Optional[float]): The volume of the entity in the last hour.
        volume_usd (Optional[float]): The volume of the entity in USD in the last hour.
        number_markets (Optional[int]): The number of markets the entity is listed in.
        price_change1h_percent (Optional[float]): The percentage change in price in the last hour.

    Properties:
        total_trades: The total number of trades made in the last hour.
        total_trade_volume: The total trade volume in the last hour.

    Methods:
        get_extensions: Returns the extensions of the entity.

    """

    address: Optional[str] = None
    decimals: Optional[int] = None
    symbol: Optional[str] = None
    name: Optional[str] = None
    extensions: Optional[OverviewExtensions] = Field(None, exclude=True)
    logo_uri: Optional[str] = Field(None, alias="logoURI")
    # pay attention to this number as well
    liquidity: Optional[float] = None
    price: Optional[float] = None
    sell_amount: Optional[int] = Field(0, alias="sell1h")
    buy_amount: Optional[int] = Field(0, alias="buy1h")
    supply: Optional[float] = 0.0
    market_cap: Optional[float] = Field(0.0, alias="mc")
    # Can get this volume over time and see what's rising
    # Buy volume might be wrong. Will have to look at normal volume to made decisions
    buy_volume: Optional[float] = Field(None, alias="vBuy1h")
    sell_volume: Optional[float] = Field(None, alias="vSell1h")
    views: Optional[int] = Field(None, alias="view1h")
    unique_views: Optional[int] = Field(None, alias="uniqueView1h")
    unique_wallet: Optional[int] = Field(
        None,
        alias="uniqueWallet1h",
    )
    volume: Optional[float] = Field(None, alias="v1h")
    volume_usd: Optional[float] = Field(None, alias="v1hUSD")
    # Check to see the distribution of the number of markets
    # Most are 1-2 markets, there are probably some that are a lot more
    number_markets: Optional[int] = None
    price_change1h_percent: Optional[float] = Field(None, alias="priceChange1hPercent")

    @computed_field
    @property
    def total_trades(self) -> int:
        """Get the total number of trades that are made in the last hour"""
        if not self.buy_amount or not self.sell_amount:
            return 0
        return self.buy_amount + self.sell_amount

    @computed_field
    @property
    def total_trade_volume(self) -> float:
        # Look for lots of this perhaps you can see a trend
        """Get the total trade volume in the last hour"""
        if not self.buy_volume or not self.sell_volume:
            return 0.0
        return self.buy_volume + self.sell_volume

    @computed_field
    @property
    def links(self) -> Dict[str, str]:
        extensions = self.get_extensions()
        if not extensions:
            return {}

        return {
            key: val
            for key, val in extensions.items()
            if val is not None and is_url(val)
        }

    def get_extensions(self):
        """
        Returns the extensions of the entity.

        Returns:
            Optional[dict]: The extensions of the entity, or None if there are no extensions.
        """
        if not self.extensions:
            return None
        return self.extensions.model_dump(exclude_none=True)


class OverviewResponse(BaseModel):
    data: Optional[Overview]
    success: Optional[bool]


class SecurityData(BaseModel):
    creation_time: Optional[datetime] = None
    creator_balance: Optional[float] = None

    owner_balance: Optional[float] = None
    # Probably want these to be about average
    owner_percentage: Optional[float] = None
    top10_user_percent: Optional[float] = None
    creator_percentage: Optional[float] = None

    freezeable: Optional[bool] = False
    pre_market_holder: Optional[List] = []
    lock_info: Optional[Dict] = {}
    non_transferable: Optional[bool] = None


class SecurityResponse(BaseModel):
    data: Optional[SecurityData] = None
    success: Optional[bool] = None
    status_code: Optional[int] = None


class TokenData(BaseModel):
    address: Optional[str] = None
    value: Optional[float] = None
    timestamp: Optional[datetime] = Field(None, alias="updateUnixTime")

    @computed_field
    @property
    def human_time(self) -> str:
        """Get the total trade volume in the last hour"""
        pen_time = pen.instance(self.timestamp)
        return pen_time.to_datetime_string()


class MultiPriceResponse(BaseModel):
    data: Optional[List[TokenData]] = None
    success: Optional[bool] = None


class PriceResponse(BaseModel):
    data: Optional[TokenData] = None
    success: Optional[bool] = None


class WalletToken(BaseModel):
    address: Optional[str] = None
    decimals: Optional[int] = None
    lamports: Optional[int] = Field(
        None, alias="balance", description="Balance in lamports. 1 billion = 1 SOL"
    )
    amount: Optional[float] = Field(None, alias="uiAmount", description="Amount in SOL")
    chain_id: Optional[str] = None
    name: Optional[str] = None
    symbol: Optional[str] = None
    logo_uri: Optional[str] = Field(None, alias="logoURI")
    price_usd: Optional[float] = None
    value_usd: Optional[float] = None


class WalletResponse(BaseModel):
    wallet_address: Optional[str] = Field(None, alias="wallet")
    balance: Optional[float] = Field(None, alias="totalUsd")
    items: Optional[List[WalletToken]] = []

    def is_time_df(self, time_df: pd.DataFrame) -> bool:
        columns = time_df.columns.tolist()
        if "timestamp" not in columns:
            return False

        timestamp_type = time_df["timestamp"].dtype
        if time_df["timestamp"].empty:
            return False

        # Check if the timestamp column is of type datetime or timestamp
        if timestamp_type != "datetime64[ns]":
            return False

        return True

    def items_df(self) -> pd.DataFrame:
        if not self.items:
            return pd.DataFrame([{}])
        _df = pd.DataFrame([item.model_dump() for item in self.items])
        columns = _df.columns.tolist()
        #
        if "timestamp" in columns:
            # Get the type of the timestamp column
            # timestamp_type = _df["timestamp"].dtype
            _df.set_index("timestamp", inplace=True)

        return _df


T = TypeVar("T", bound=BaseModel)


class ResponseContainer(BaseModel, Generic[T]):
    data: List[T] = []

    def df(self) -> pd.DataFrame:
        if not self.data:
            raise pd.DataFrame([{}])
        _df = pd.DataFrame([item.model_dump() for item in self.data])
        columns = _df.columns.tolist()
        #
        if "timestamp" in columns:
            # Get the type of the timestamp column
            # timestamp_type = _df["timestamp"].dtype
            _df.set_index("timestamp", inplace=True)

        return _df

    @computed_field
    def count(self) -> int:
        return len(self.data)


def main():
    pass


if __name__ == "__main__":
    main()
