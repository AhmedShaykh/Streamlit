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

import { AppNode, BlockNode } from "~lib/AppNode"
import { ComponentRegistry } from "~lib/components/widgets/CustomComponent"
import { FileUploadClient } from "~lib/FileUploadClient"
import { ScriptRunState } from "~lib/ScriptRunState"
import { StreamlitEndpoints } from "~lib/StreamlitEndpoints"
import { EmotionTheme, getDividerColors } from "~lib/theme"
import { isValidElementId } from "~lib/util/utils"
import { FormsData, WidgetStateManager } from "~lib/WidgetStateManager"

export function shouldComponentBeEnabled(
  elementType: string,
  scriptRunState: ScriptRunState
): boolean {
  return elementType !== "empty" || scriptRunState !== ScriptRunState.RUNNING
}

export function isElementStale(
  node: AppNode,
  scriptRunState: ScriptRunState,
  scriptRunId: string,
  fragmentIdsThisRun?: Array<string>
): boolean {
  if (scriptRunState === ScriptRunState.RERUN_REQUESTED) {
    // If a rerun was just requested, all of our current elements
    // are about to become stale.
    return true
  }

  if (scriptRunState === ScriptRunState.RUNNING) {
    if (fragmentIdsThisRun && fragmentIdsThisRun.length) {
      // if the fragmentId is set, we only want to mark elements as stale
      // that belong to the same fragmentId and have a different scriptRunId.
      // If they have the same scriptRunId, they were just updated.
      return Boolean(
        node.fragmentId &&
          fragmentIdsThisRun.includes(node.fragmentId) &&
          node.scriptRunId !== scriptRunId
      )
    }
    return node.scriptRunId !== scriptRunId
  }

  return false
}

export function isComponentStale(
  enable: boolean,
  node: AppNode,
  scriptRunState: ScriptRunState,
  scriptRunId: string,
  fragmentIdsThisRun?: Array<string>
): boolean {
  return (
    !enable ||
    isElementStale(node, scriptRunState, scriptRunId, fragmentIdsThisRun)
  )
}

export function assignDividerColor(
  node: BlockNode,
  theme: EmotionTheme
): void {
  // All available divider colors
  const allColorMap = getDividerColors(theme)
  const allColorKeys = Object.keys(allColorMap)

  // Limited colors for auto assignment
  const { blue, green, orange, red, violet } = allColorMap
  const autoColorMap = { blue, green, orange, red, violet }
  const autoColorKeys = Object.keys(autoColorMap)
  let dividerIndex = 0

  Array.from(node.getElements()).forEach(element => {
    const divider = element.heading?.divider
    if (element.type === "heading" && divider) {
      if (divider === "auto") {
        const colorKey = autoColorKeys[dividerIndex]
        // @ts-expect-error - heading.divider is not undefined at this point
        element.heading.divider = autoColorMap[colorKey]
        dividerIndex += 1
        if (dividerIndex === autoColorKeys.length) dividerIndex = 0
      } else if (allColorKeys.includes(divider)) {
        // @ts-expect-error
        element.heading.divider = allColorMap[divider]
      }
    }
  })
}
export interface BaseBlockProps {
  /**
   * The app's StreamlitEndpoints instance. Exposes non-websocket endpoint logic
   * used by various Streamlit elements.
   */
  endpoints: StreamlitEndpoints

  /**
   * The app's WidgetStateManager instance. Used by all widget elements to
   * store and retrieve widget state. When the user interacts with a widget,
   * the WidgetStateManager initiates the "rerun BackMsg" data flow to kick
   * off a script rerun.
   */
  widgetMgr: WidgetStateManager

  /**
   * The app's FileUploadClient instance. Used by the FileUploader component
   * to send files to the Streamlit backend.
   */
  uploadClient: FileUploadClient

  /**
   * The app's ComponentRegistry instance. Dispatches "Custom Component"
   * iframe messages to ComponentInstances.
   */
  componentRegistry: ComponentRegistry

  /**
   * The ID of the current "script run". When a Streamlit script is re-run
   * (usually as a result of the user interacting with a widget), the Streamlit
   * backend sends a new scriptRunId to the frontend. When the script run ends,
   * the frontend discards "stale" elements (that is, elements with a non-current
   * scriptRunId).
   */
  scriptRunId: string

  /**
   * The app's current ScriptRunState. This is used in combination with
   * scriptRunId to prune stale elements. It's also used by the app to
   * display the "running man" indicator when the app's script is being re-run.
   */
  scriptRunState: ScriptRunState

  /**
   * If true, all widgets will be disabled and the app will be non-interactive.
   * This is generally set when the frontend is disconnected from the backend.
   */
  widgetsDisabled: boolean

  /**
   * Data about all forms in the app. The WidgetStateManager creates its own
   * internal FormsData instance, and calls a callback (`formsDataChanged`)
   * when forms are updated. This FormsData instance should be updated
   * from that callback.
   */
  formsData: FormsData

  /**
   * If true , the element should not allow going into fullscreen. Right now we plan
   * to use it, for example, in Dialogs to prevent fullscreen issues.
   */
  disableFullscreenMode?: boolean
}

/**
 * Converts a user-specified key to a valid CSS class name.
 *
 * @param key - The key to convert.
 * @returns A valid CSS class name.
 */
export function convertKeyToClassName(key: string | undefined | null): string {
  if (!key) {
    return ""
  }
  const className = key.trim().replace(/[^a-zA-Z0-9_-]/g, "-")
  return "st-key-" + className
}

/**
 * Returns the user-specified key extracted from the element id, or undefined if the id does
 * not have a user-specified key.
 */
export function getKeyFromId(
  elementId: string | undefined | null
): string | undefined {
  if (!elementId || !isValidElementId(elementId)) {
    return undefined
  }

  // Split the elementId by hyphens
  const parts = elementId.split("-")
  // Extract all parts after the second hyphen
  const userKey = parts.slice(2).join("-")
  return userKey === "None" ? undefined : userKey
}
