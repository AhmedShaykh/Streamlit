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

from datetime import date, datetime

import numpy as np
import pandas as pd

import streamlit as st

np.random.seed(0)
data = np.random.randint(low=0, high=20, size=(20, 3))

w1 = st.sidebar.date_input("Label 1", date(1970, 1, 1))
st.write("Value 1:", w1)

w2 = st.sidebar.date_input("Label 2", datetime(2019, 7, 6, 21, 15))
st.write("Value 2:", w2)

x = st.sidebar.text("overwrite me")
x.text("overwritten")
y = st.sidebar.text_input("type here")

with st.sidebar:
    st.header("hello world")
    st.markdown("hello world")
    st.bar_chart(pd.DataFrame(data, columns=["a", "b", "c"]))
