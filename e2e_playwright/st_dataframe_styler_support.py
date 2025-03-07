# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2025)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random

import numpy as np
import pandas as pd

import streamlit as st

# Explicitly seed the RNG for deterministic results
np.random.seed(0)
random.seed(0)


st.header("Pandas Styler: Value formatting")
df = pd.DataFrame({"test": [3.1423424, 3.1]})
st.dataframe(df.style.format({"test": "{:.2f}"}), use_container_width=False)

st.header("Pandas Styler: Background color")


def highlight_first(value):
    return "background-color: yellow" if value == 0 else ""


df = pd.DataFrame(np.arange(0, 100, 1).reshape(10, 10))
st.dataframe(df.style.map(highlight_first))

st.header("Pandas Styler: Background and font styling")

df = pd.DataFrame(np.random.randn(20, 4), columns=["A", "B", "C", "D"])


def style_negative(v, props=""):
    return props if v < 0 else None


def highlight_max(s, props=""):
    return np.where(s == np.nanmax(s.values), props, "")


# Passing style values w/ all color formats to test css-style-string parsing robustness.
styled_df = df.style.map(style_negative, props="color:#FF0000;").map(
    lambda v: "opacity: 20%;" if (v < 0.3) and (v > -0.3) else None
)

styled_df.apply(
    highlight_max, props="color:white;background-color:rgb(255, 0, 0)", axis=0
)

styled_df.apply(
    highlight_max, props="color:white;background-color:hsl(273, 98%, 60%);", axis=1
).apply(highlight_max, props="color:white;background-color:purple", axis=None)

st.dataframe(styled_df)

st.header("Pandas Styler: Gradient Styling")

weather_df = pd.DataFrame(
    np.random.rand(10, 2) * 5,
    index=pd.date_range(start="2021-01-01", periods=10),
    columns=["Tokyo", "Beijing"],
)


def rain_condition(v):
    if v < 1.75:
        return "Dry"
    elif v < 2.75:
        return "Rain"
    return "Heavy Rain"


def make_pretty(styler):
    styler.set_caption("Weather Conditions")
    styler.format(rain_condition)
    styler.background_gradient(axis=None, vmin=1, vmax=5, cmap="YlGnBu")
    return styler


styled_df = weather_df.style.pipe(make_pretty)

st.dataframe(styled_df)

st.header("LinkColumn with display value:")
st.dataframe(
    pd.DataFrame(
        {
            "col_0": [
                "https://streamlit.io",
                "https://docs.streamlit.io",
                "https://streamlit.io/gallery",
                None,
            ]
        }
    ).style.format(lambda url: url.replace("https://", "Website: ") if url else ""),
    column_config={"col_0": st.column_config.LinkColumn()},
)

st.header("Column config takes prio over Pandas Styler")
st.dataframe(
    pd.DataFrame(
        {
            "number (formatted)": [1, 2, 3],
            "url (formatted)": [
                "https://streamlit.io",
                "https://docs.streamlit.io",
                "https://docs.streamlit.io",
            ],
            "datetime (formatted)": [
                pd.Timestamp("2024-01-01"),
                pd.Timestamp("2024-01-02"),
                pd.Timestamp("2024-01-03"),
            ],
            "text": ["foo", "bar", "foobar"],
            "number": [1, 2, 3],
            "url": [
                "https://streamlit.io",
                "https://docs.streamlit.io",
                "https://docs.streamlit.io",
            ],
            "datetime": [
                pd.Timestamp("2024-01-01"),
                pd.Timestamp("2024-01-02"),
                pd.Timestamp("2024-01-03"),
            ],
        }
    ).style.format(lambda v: "pd styler"),
    column_config={
        "number (formatted)": st.column_config.NumberColumn(format="$%.2f"),
        "url (formatted)": st.column_config.LinkColumn(display_text="Open"),
        "datetime (formatted)": st.column_config.DatetimeColumn(format="MMM DD, YYYY"),
        "number": st.column_config.NumberColumn(),
        "url": st.column_config.LinkColumn(),
        "datetime": st.column_config.DatetimeColumn(),
    },
    hide_index=True,
)
