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

from playwright.sync_api import Page, expect


def test_display_altair(app: Page):
    """Test that st.write displays altair charts."""
    altair_elements = app.get_by_test_id("stVegaLiteChart")
    expect(altair_elements).to_have_count(1)


def test_display_plotly(app: Page):
    """Test that st.write displays plotly charts."""
    plotly_elements = app.get_by_test_id("stPlotlyChart")
    expect(plotly_elements).to_have_count(1)


def test_display_graphviz(app: Page):
    """Test that st.write displays graphviz charts."""
    plotly_elements = app.get_by_test_id("stGraphVizChart")
    expect(plotly_elements).to_have_count(1)


def test_display_pydeck_chart(app: Page):
    """Test that st.write displays pydeck charts."""
    pydeck_elements = app.get_by_test_id("stDeckGlJsonChart")
    # The pydeck chart takes a while to load so check that
    # it gets attached with an increased timeout.
    expect(pydeck_elements).to_have_count(1, timeout=15000)
