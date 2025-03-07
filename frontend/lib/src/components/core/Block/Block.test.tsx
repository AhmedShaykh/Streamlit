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

import React, { ReactElement } from "react"

import { screen } from "@testing-library/react"

import { Block as BlockProto } from "@streamlit/protobuf"

import { render } from "~lib/test_util"
import { BlockNode } from "~lib/AppNode"
import { ScriptRunState } from "~lib/ScriptRunState"
import * as UseResizeObserver from "~lib/hooks/useResizeObserver"

import VerticalBlock from "./Block"

const FAKE_SCRIPT_HASH = "fake_script_hash"
class ResizeObserver {
  observe(): void {}

  unobserve(): void {}

  disconnect(): void {}
}

function makeColumn(weight: number, children: BlockNode[] = []): BlockNode {
  return new BlockNode(
    FAKE_SCRIPT_HASH,
    children,
    new BlockProto({ allowEmpty: true, column: { weight } })
  )
}

function makeHorizontalBlock(numColumns: number): BlockNode {
  const weight = 1 / numColumns

  return new BlockNode(
    FAKE_SCRIPT_HASH,
    Array.from({ length: numColumns }, () => makeColumn(weight)),
    new BlockProto({ allowEmpty: true, horizontal: { gap: "small" } })
  )
}

function makeVerticalBlock(
  children: BlockNode[] = [],
  additionalProps: Partial<BlockProto> = {}
): BlockNode {
  return new BlockNode(
    FAKE_SCRIPT_HASH,
    children,
    new BlockProto({ allowEmpty: true, ...additionalProps })
  )
}

function makeVerticalBlockComponent(node: BlockNode): ReactElement {
  return (
    <VerticalBlock
      node={node}
      scriptRunId={""}
      scriptRunState={ScriptRunState.NOT_RUNNING}
      widgetsDisabled={false}
      // @ts-expect-error
      widgetMgr={undefined}
      // @ts-expect-error
      uploadClient={undefined}
      // @ts-expect-error
      componentRegistry={undefined}
      // @ts-expect-error
      formsData={undefined}
    />
  )
}

describe("Vertical Block Component", () => {
  window.ResizeObserver = ResizeObserver
  it("should render a horizontal block with empty columns", () => {
    const block: BlockNode = makeVerticalBlock([makeHorizontalBlock(4)])
    render(makeVerticalBlockComponent(block))

    expect(screen.getAllByTestId("stColumn")).toHaveLength(4)
    expect(
      screen.getAllByTestId("stVerticalBlockBorderWrapper")[0]
    ).not.toHaveStyle("overflow: auto")
  })

  it("should add the user-specified key as class", () => {
    const block: BlockNode = makeVerticalBlock([], {
      id: "$$ID-899e9b72e1539f21f8e82565d36609d0-first container",
    })
    render(makeVerticalBlockComponent(block))

    expect(screen.getByTestId("stVerticalBlock")).toBeVisible()
    expect(screen.getByTestId("stVerticalBlock")).toHaveClass(
      "st-key-first-container"
    )
  })

  it("should activate scrolling when height is set", () => {
    const block: BlockNode = makeVerticalBlock([makeHorizontalBlock(4)], {
      vertical: { height: 100 },
    })

    render(makeVerticalBlockComponent(block))

    expect(
      screen.getAllByTestId("stVerticalBlockBorderWrapper")[0]
    ).toHaveStyle("overflow: auto")
  })

  it("should show border when border is True", () => {
    const block: BlockNode = makeVerticalBlock([makeHorizontalBlock(4)], {
      vertical: { border: true },
    })

    render(makeVerticalBlockComponent(block))

    expect(
      screen.getAllByTestId("stVerticalBlockBorderWrapper")[0]
    ).toHaveStyle("border: 1px solid rgba(49, 51, 63, 0.2);")
  })

  describe("should never have a width of 0", () => {
    describe("when observed width is 0", () => {
      beforeEach(() => {
        vi.spyOn(UseResizeObserver, "useResizeObserver").mockReturnValue({
          elementRef: React.createRef(),
          forceRecalculate: vitest.fn(),
          values: [0],
        })
      })

      it("should have a width of -1px", () => {
        const block = makeVerticalBlock([makeHorizontalBlock(4)])
        render(makeVerticalBlockComponent(block))

        expect(screen.getAllByTestId("stVerticalBlock")[0]).toHaveStyle(
          "width: -1px"
        )
      })
    })

    describe("when observed width is a positive value", () => {
      beforeEach(() => {
        vi.spyOn(UseResizeObserver, "useResizeObserver").mockReturnValue({
          elementRef: React.createRef(),
          forceRecalculate: vitest.fn(),
          values: [100],
        })
      })

      it("should have the observed width", () => {
        const block = makeVerticalBlock([makeHorizontalBlock(4)])
        render(makeVerticalBlockComponent(block))

        expect(screen.getAllByTestId("stVerticalBlock")[0]).toHaveStyle(
          "width: 100px"
        )
      })
    })
  })
})
