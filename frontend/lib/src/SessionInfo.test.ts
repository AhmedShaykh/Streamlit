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

import { NewSession } from "@streamlit/protobuf"

import { SessionInfo } from "./SessionInfo"
import { mockSessionInfoProps } from "./mocks/mocks"

test("Throws an error when used before initialization", () => {
  const sessionInfo = new SessionInfo()
  expect(() => sessionInfo.current).toThrow()
})

describe("SessionInfo.setCurrent", () => {
  test("copies props to `current`", () => {
    const sessionInfo = new SessionInfo()
    sessionInfo.setCurrent(mockSessionInfoProps())

    expect(sessionInfo.isSet).toBe(true)
    expect(sessionInfo.current).toEqual(mockSessionInfoProps())
  })

  test("copies previous props to `last`", () => {
    const sessionInfo = new SessionInfo()
    sessionInfo.setCurrent(mockSessionInfoProps())
    expect(sessionInfo.last).toBeUndefined()

    sessionInfo.setCurrent(mockSessionInfoProps({ appId: "newValue" }))
    expect(sessionInfo.current).toEqual(
      mockSessionInfoProps({ appId: "newValue" })
    )
    expect(sessionInfo.last).toEqual(mockSessionInfoProps())
  })
})

describe("SessionInfo.isHello", () => {
  test("is true only when `isHello` is true in current SessionInfo", () => {
    const sessionInfo = new SessionInfo()
    expect(sessionInfo.isHello).toBe(false)

    sessionInfo.setCurrent(mockSessionInfoProps({ isHello: true }))
    expect(sessionInfo.isHello).toBe(true)

    sessionInfo.setCurrent(mockSessionInfoProps({ isHello: false }))
    expect(sessionInfo.isHello).toBe(false)
  })
})

test("Props can be initialized from a protobuf", () => {
  const MESSAGE = new NewSession({
    config: {
      gatherUsageStats: false,
      maxCachedMessageAge: 31,
      mapboxToken: "mapboxToken",
      allowRunOnSave: false,
    },
    initialize: {
      userInfo: {
        installationId: "installationId",
        installationIdV3: "installationIdV3",
      },
      environmentInfo: {
        streamlitVersion: "streamlitVersion",
        pythonVersion: "pythonVersion",
      },
      sessionStatus: {
        runOnSave: false,
        scriptIsRunning: false,
      },
      sessionId: "sessionId",
      isHello: false,
    },
  })

  const props = SessionInfo.propsFromNewSessionMessage(MESSAGE)
  expect(props.sessionId).toEqual("sessionId")
  expect(props.streamlitVersion).toEqual("streamlitVersion")
  expect(props.pythonVersion).toEqual("pythonVersion")
  expect(props.installationId).toEqual("installationId")
  expect(props.installationIdV3).toEqual("installationIdV3")
  expect(props.maxCachedMessageAge).toEqual(31)
  expect(props.commandLine).toBeUndefined()
  expect(props.isHello).toBeFalsy()
})
