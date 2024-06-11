

from typing import List, Optional, Dict, Callable, Union
from dataclasses import dataclass
import pandas as pd
import numpy as np

from matplotlib.dates import num2date
from matplotlib.ticker import FuncFormatter

# region Utils

def validate_dataframe(pd_df: pd.DataFrame,
                       cols: List[str],
                       sort_by: Optional[str] = None):
    _columns = cols.copy()
    if sort_by and sort_by not in _columns:
        _columns.append(sort_by)
    for col in _columns:
        if col not in pd_df.columns:
            raise AttributeError(f"{col} is not a DataFrame's column")


def format_func(
        format_funcs: Optional[Dict[str, Optional[Callable[[Union[int, float, str]], str]]]],
        label: Optional[str] = None,
        x: Optional[str] = None,
        y: Optional[str] = None,
        z: Optional[str] = None):

    if label and "label" in format_funcs:
        format_funcs[label] = format_funcs["label"]
    if x and "x" in format_funcs:
        format_funcs[x] = format_funcs["x"]
    if y and "y" in format_funcs:
        format_funcs[y] = format_funcs["y"]
    if z and "z" in format_funcs:
        format_funcs[z] = format_funcs["z"]
    return format_funcs

# endregion

# region Style


MAX_RESULTS = 50
X_COL = "index"
Y_COL = "overlap"
Z_COL = "users"
FIG_SIZE = (19.2, 10.8)
BACKGROUND_COLOR = 'black'
TEXT_COLOR = 'white'
PALETTE = "Greys_r"
FONT_SIZE = 14


@dataclass
class StyleTemplate:
    background_color: str = BACKGROUND_COLOR
    fig_border: str = BACKGROUND_COLOR
    font_name: str = 'Arial'
    font_size: int = FONT_SIZE
    font_color: str = TEXT_COLOR
    palette: str = PALETTE
    legend: bool = True
    xscale: Optional[str] = None
    x_ticks: int = 10
    yscale: Optional[str] = None
    y_ticks: int = 5
    format_funcs: Optional[Dict[str, Optional[Callable[[
        Union[int, float, str]], str]]]] = None
    col_widths: Optional[List[float]] = None

    @property
    def font_mapping(self):
        return {0: self.font_size-3,
                1: self.font_size-1,
                2: self.font_size,
                3: self.font_size+1,
                4: self.font_size+3}


class DynamicFuncFormatter(FuncFormatter):
    def __init__(self, func_name):
        super().__init__(func_name)


def percent_formatter(val, pos: Optional[int] = None):
    if val*100 <= 0.1:  # For 0.1%
        return f"{val*100:.2f}%"
    elif val*100 <= 1:  # For 1%
        return f"{val*100:.1f}%"
    else:
        return f"{val*100:.0f}%"


def bmk_formatter(val, pos: Optional[int] = None):
    if val >= 1_000_000_000:  # Billions
        return f"{val / 1_000_000_000:.2f}B"
    elif val >= 1_000_000:  # Millions
        return f"{val / 1_000_000:.1f}M"
    elif val >= 1_000:  # Thousands
        return f"{val / 1_000:.1f}K"
    else:
        return f"{int(val)}"


def integer_formatter(value, pos: Optional[int] = None):
    return f"{int(value)}"


def string_formatter(value, pos: Optional[int] = None):
    return str(value).replace("-", " ").replace("_", " ").title()


def yy_mm__formatter(x, pos: Optional[int] = None):
    return num2date(x).strftime('%Y-%m')


def yy_mm_dd__formatter(x, pos: Optional[int] = None):
    return num2date(x).strftime('%Y-%m-%D')


def percent_formatter(x,  pos: Optional[int] = None):
    return f"{x * 100:.0f}%"


def generate_ticks(min_val, max_val, num_ticks="10"):
    # Identify the type of the input
    try:
        min_val = float(min_val)
        max_val = float(max_val)
        is_date = False
    except ValueError:
        is_date = True

    # Convert string inputs to appropriate numerical or date types
    num_ticks = int(num_ticks)

    if is_date:
        min_val = pd.Timestamp(min_val).to_datetime64()
        max_val = pd.Timestamp(max_val).to_datetime64()
        data_range = (max_val - min_val).astype('timedelta64[D]').astype(int)
    else:
        data_range = max_val - min_val

    # Calculate a nice step size
    step_size = data_range / (num_ticks - 1)

    # If date, convert back to datetime
    if is_date:
        ticks = pd.date_range(
            start=min_val, periods=num_ticks, freq=f"{step_size}D")
    else:
        # Round the step size to a "nice" number
        exponent = np.floor(np.log10(step_size))
        fraction = step_size / 10**exponent
        nice_fraction = round(fraction)

        # Create nice step size
        nice_step = nice_fraction * 10**exponent

        # Generate the tick marks based on the nice step size
        ticks = np.arange(min_val, max_val + nice_step, nice_step)

    return ticks


# endregion
