import math

from annotated_types import Annotated
from pydantic import BeforeValidator
from pydantic.functional_validators import AfterValidator

from supamodel.utils import check_int, title_case

# from typing_extensions import Annotated


# Custom validation function to handle nan, inf, and -inf
def convert_invalid_float(value: float) -> float:
    if math.isnan(value) or math.isinf(value):
        return 0.0
    return value


# from typing_extensions import Annotated

TruncatedFloat = Annotated[
    float,
    AfterValidator(convert_invalid_float),  # Applying the invalid float conversion
]

CapitalStr = Annotated[str, AfterValidator(title_case)]
ForceInt = Annotated[int, BeforeValidator(check_int)]
