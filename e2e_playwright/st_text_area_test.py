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
from playwright.sync_api import Page, expect

from e2e_playwright.conftest import ImageCompareFunction
from e2e_playwright.shared.app_utils import (
    check_top_level_class,
    expect_exception,
    expect_help_tooltip,
    get_element_by_key,
)


def test_text_area_widget_rendering(
    themed_app: Page, assert_snapshot: ImageCompareFunction
):
    """Test that the st.text_area widgets are correctly rendered via screenshot matching."""
    text_area_widgets = themed_app.get_by_test_id("stTextArea")
    expect(text_area_widgets).to_have_count(15)

    assert_snapshot(text_area_widgets.nth(0), name="st_text_area-default")
    assert_snapshot(text_area_widgets.nth(1), name="st_text_area-value_some_text")
    assert_snapshot(text_area_widgets.nth(2), name="st_text_area-value_1234")
    assert_snapshot(text_area_widgets.nth(3), name="st_text_area-value_None")
    assert_snapshot(text_area_widgets.nth(4), name="st_text_area-placeholder")
    assert_snapshot(text_area_widgets.nth(5), name="st_text_area-disabled")
    assert_snapshot(text_area_widgets.nth(6), name="st_text_area-hidden_label")
    assert_snapshot(text_area_widgets.nth(7), name="st_text_area-collapsed_label")
    assert_snapshot(text_area_widgets.nth(8), name="st_text_area-callback_help")
    assert_snapshot(text_area_widgets.nth(9), name="st_text_area-max_chars_5")
    assert_snapshot(text_area_widgets.nth(10), name="st_text_area-height_250")
    assert_snapshot(text_area_widgets.nth(11), name="st_text_area-height_75")
    assert_snapshot(text_area_widgets.nth(14), name="st_text_area-markdown_label")


def test_help_tooltip_works(app: Page):
    element_with_help = app.get_by_test_id("stTextArea").nth(8)
    expect_help_tooltip(app, element_with_help, "Help text")


def test_text_area_has_correct_initial_values(app: Page):
    """Test that st.text_area has the correct initial values."""
    markdown_elements = app.get_by_test_id("stMarkdown")
    expect(markdown_elements).to_have_count(15)

    expected = [
        "value 1: ",
        "value 2: some text",
        "value 3: 1234",
        "value 4: None",
        "value 5: ",
        "value 6: default text",
        "value 7: default text",
        "value 8: default text",
        "value 9: ",
        "text area changed: False",
        "value 10: 1234",
        "value 11: default text",
        "value 12: default text",
        "text area 13 (value from state) - value: xyz",
        "text area 14 (value from form) - value: ",
    ]

    for markdown_element, expected_text in zip(markdown_elements.all(), expected):
        expect(markdown_element).to_have_text(expected_text, use_inner_text=True)


def test_text_area_shows_state_value(app: Page):
    expect(
        app.get_by_test_id("stTextArea").nth(12).locator("textarea").first
    ).to_have_text("xyz")


def test_text_area_shows_instructions_when_dirty(
    app: Page, assert_snapshot: ImageCompareFunction
):
    """Test that st.text_area shows the instructions correctly when dirty."""
    text_area = app.get_by_test_id("stTextArea").nth(9)

    text_area_field = text_area.locator("textarea").first
    text_area_field.fill("123")

    assert_snapshot(text_area, name="st_text_area-input_instructions")


def test_text_area_limits_input_via_max_chars(app: Page):
    """Test that st.text_area correctly limits the number of characters via max_chars."""
    text_area_field = app.get_by_test_id("stTextArea").nth(9).locator("textarea").first
    # Try typing in char by char:
    text_area_field.clear()
    text_area_field.type("12345678")
    text_area_field.press("Control+Enter")

    expect(app.get_by_test_id("stMarkdown").nth(10)).to_have_text(
        "value 10: 12345", use_inner_text=True
    )

    # Try filling in everything at once:
    text_area_field.focus()
    text_area_field.fill("12345678")
    text_area_field.press("Control+Enter")

    expect(app.get_by_test_id("stMarkdown").nth(10)).to_have_text(
        "value 10: 12345", use_inner_text=True
    )


def test_text_area_has_correct_value_on_blur(app: Page):
    """Test that st.text_area has the correct value on blur."""

    first_text_area_field = (
        app.get_by_test_id("stTextArea").first.locator("textarea").first
    )
    first_text_area_field.focus()
    first_text_area_field.fill("hello world")
    first_text_area_field.blur()

    expect(app.get_by_test_id("stMarkdown").first).to_have_text(
        "value 1: hello world", use_inner_text=True
    )


@pytest.mark.skip_browser(
    "firefox"  # The meta key + enter press doesn't work in the playwright firefox test
)
def test_text_area_has_correct_value_on_enter(app: Page):
    """Test that st.text_area has the correct value on enter."""

    first_text_area_field = (
        app.get_by_test_id("stTextArea").first.locator("textarea").first
    )
    # Test control + enter:
    first_text_area_field.focus()
    first_text_area_field.fill("hello world")
    first_text_area_field.press("Control+Enter")

    expect(app.get_by_test_id("stMarkdown").first).to_have_text(
        "value 1: hello world", use_inner_text=True
    )

    # Test command (Meta key) + enter:
    first_text_area_field.focus()
    first_text_area_field.fill("different value")
    first_text_area_field.press("Meta+Enter")

    expect(app.get_by_test_id("stMarkdown").first).to_have_text(
        "value 1: different value", use_inner_text=True
    )


def test_text_area_has_correct_value_on_click_outside(app: Page):
    """Test that st.text_area has the correct value on click outside."""

    first_text_area_field = (
        app.get_by_test_id("stTextArea").first.locator("textarea").first
    )
    first_text_area_field.focus()
    first_text_area_field.fill("hello world")
    app.get_by_test_id("stMarkdown").first.click()

    expect(app.get_by_test_id("stMarkdown").first).to_have_text(
        "value 1: hello world", use_inner_text=True
    )


def test_empty_text_area_behaves_correctly(app: Page):
    """Test that st.text_area behaves correctly when empty."""
    # Should return None as value:
    expect(app.get_by_test_id("stMarkdown").nth(3)).to_have_text(
        "value 4: None", use_inner_text=True
    )

    # Enter value in the empty widget:
    empty_text_area = app.get_by_test_id("stTextArea").nth(3)
    empty_text_area_field = empty_text_area.locator("textarea").first
    empty_text_area_field.fill("hello world")
    empty_text_area_field.press("Control+Enter")

    expect(app.get_by_test_id("stMarkdown").nth(3)).to_have_text(
        "value 4: hello world", use_inner_text=True
    )

    # Press escape to clear value:
    empty_text_area_field.focus()
    empty_text_area_field.clear()
    empty_text_area_field.press("Control+Enter")

    # Should be set to empty string (we don't clear to None for text area):
    expect(app.get_by_test_id("stMarkdown").nth(3)).to_have_text(
        "value 4: ", use_inner_text=True
    )


def test_calls_callback_on_change(app: Page):
    """Test that it correctly calls the callback on change."""
    text_area_field = app.get_by_test_id("stTextArea").nth(8).locator("textarea").first

    text_area_field.fill("hello world")
    text_area_field.press("Control+Enter")

    expect(app.get_by_test_id("stMarkdown").nth(8)).to_have_text(
        "value 9: hello world",
        use_inner_text=True,
    )
    expect(app.get_by_test_id("stMarkdown").nth(9)).to_have_text(
        "text area changed: True",
        use_inner_text=True,
    )

    # Change different widget to trigger delta path change
    first_text_area_field = (
        app.get_by_test_id("stTextArea").first.locator("textarea").first
    )
    first_text_area_field.fill("hello world")
    first_text_area_field.press("Control+Enter")

    expect(app.get_by_test_id("stMarkdown").first).to_have_text(
        "value 1: hello world", use_inner_text=True
    )

    # Test if value is still correct after delta path change
    expect(app.get_by_test_id("stMarkdown").nth(8)).to_have_text(
        "value 9: hello world",
        use_inner_text=True,
    )
    expect(app.get_by_test_id("stMarkdown").nth(9)).to_have_text(
        "text area changed: False",
        use_inner_text=True,
    )


def test_text_area_in_form_with_submit_by_enter(app: Page):
    """Test that text area in form can be submitted by pressing Command+Enter"""
    text_area_field = app.get_by_test_id("stTextArea").nth(13).locator("textarea").first
    text_area_field.fill("hello world")
    text_area_field.press("Control+Enter")
    expect(app.get_by_test_id("stMarkdown").nth(14)).to_have_text(
        "text area 14 (value from form) - value: hello world",
        use_inner_text=True,
    )


def test_invalid_height(app: Page):
    """Test that it raises an error when passed an invalid height."""
    expect_exception(
        app,
        "StreamlitAPIException: Invalid height 65px for st.text_area - must be at least 68 pixels.",
    )


def test_check_top_level_class(app: Page):
    """Check that the top level class is correctly set."""
    check_top_level_class(app, "stTextArea")


def test_custom_css_class_via_key(app: Page):
    """Test that the element can have a custom css class via the key argument."""
    expect(get_element_by_key(app, "text_area9")).to_be_visible()
