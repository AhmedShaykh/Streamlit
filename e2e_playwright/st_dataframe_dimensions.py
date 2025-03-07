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

import numpy as np
import pandas as pd

import streamlit as st

# Explicitly seed the RNG for deterministic results
np.random.seed(0)

data = np.random.randn(100, 100)

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=False)
st.dataframe(df, 250, 150)
st.dataframe(df, width=250)
st.dataframe(df, height=150, use_container_width=False)
st.dataframe(df, 5000, 5000)
st.dataframe(df, use_container_width=True)

small_df = pd.DataFrame(np.random.randn(100, 3))
st.dataframe(small_df, width=500)
st.dataframe(small_df, use_container_width=True)
st.dataframe(small_df, width=200, use_container_width=True)
st.dataframe(small_df, width=200, use_container_width=False)

one_col_df = pd.DataFrame(np.random.randn(100, 1))
st.dataframe(one_col_df, use_container_width=True)

if st.button("Resize dataframe"):
    st.dataframe(small_df, width=400, height=200)
else:
    st.dataframe(small_df, width=200, height=100)
