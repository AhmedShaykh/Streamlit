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

import pytest
from playwright.sync_api import Page

from e2e_playwright.shared.app_utils import expect_prefixed_markdown


@pytest.mark.browser_context_args(timezone_id="Europe/Berlin")
def test_timezone(app: Page):
    """Test that the timezone is correctly set."""
    expect_prefixed_markdown(app, "Timezone name:", "Europe/Berlin")


@pytest.mark.browser_context_args(timezone_id="Asia/Yerevan")
def test_timezone_offset(app: Page):
    """Test that the timezone offset is correctly set."""
    expect_prefixed_markdown(app, "Timezone offset:", "-240")
