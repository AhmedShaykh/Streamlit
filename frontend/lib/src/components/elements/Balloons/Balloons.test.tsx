/**
 * Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2025)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import React from "react"

import { screen } from "@testing-library/react"

import { render } from "~lib/test_util"

import Balloons, { NUM_BALLOONS, Props } from "./Balloons"

const getProps = (): Props => ({
  scriptRunId: "51522269",
})

describe("Balloons element", () => {
  vi.useFakeTimers()

  beforeEach(() => {
    vi.clearAllMocks()
    vi.clearAllTimers()
  })

  it("renders without crashing", () => {
    const props = getProps()
    render(<Balloons {...props} />)

    const balloonElement = screen.getByTestId("stBalloons")
    expect(balloonElement).toBeInTheDocument()
    expect(balloonElement).toHaveClass("stBalloons")

    const balloonImages = screen.getAllByRole("img")
    expect(balloonImages.length).toBe(NUM_BALLOONS)

    balloonImages.forEach(node => {
      expect(node).toHaveAttribute("src")
    })
  })

  it("uses correct top-level class", () => {
    const props = getProps()
    render(<Balloons {...props} />)

    const balloonElement = screen.getByTestId("stBalloons")
    expect(balloonElement).toHaveClass("stBalloons")
  })
})
