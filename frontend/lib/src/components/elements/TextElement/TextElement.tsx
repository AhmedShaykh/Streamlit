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

import React, { memo, ReactElement } from "react"

import { Text as TextProto } from "@streamlit/protobuf"

import {
  InlineTooltipIcon,
  StyledLabelHelpWrapper,
} from "~lib/components/shared/TooltipIcon"

import { StyledText } from "./styled-components"

export interface TextProps {
  element: TextProto
}

/**
 * Functional element representing preformatted (plain) text.
 */
function TextElement({ element }: Readonly<TextProps>): ReactElement {
  return (
    <StyledLabelHelpWrapper className="stText" data-testid="stText">
      <StyledText>{element.body}</StyledText>
      {element.help && <InlineTooltipIcon content={element.help} />}
    </StyledLabelHelpWrapper>
  )
}

export default memo(TextElement)
