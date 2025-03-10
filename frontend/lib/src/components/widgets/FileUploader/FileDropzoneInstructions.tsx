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

import { CloudUpload } from "@emotion-icons/material-outlined"

import Icon from "~lib/components/shared/Icon"
import { FileSize, getSizeDisplay } from "~lib/util/FileHelper"
import { Small } from "~lib/components/shared/TextElements"

import {
  StyledFileDropzoneInstructions,
  StyledFileDropzoneInstructionsColumn,
  StyledFileDropzoneInstructionsFileUploaderIcon,
  StyledFileDropzoneInstructionsStyledSpan,
} from "./styled-components"

export interface Props {
  multiple: boolean
  acceptedExtensions: string[]
  maxSizeBytes: number
}

const FileDropzoneInstructions = ({
  multiple,
  acceptedExtensions,
  maxSizeBytes,
}: Props): React.ReactElement => (
  <StyledFileDropzoneInstructions data-testid="stFileUploaderDropzoneInstructions">
    <StyledFileDropzoneInstructionsFileUploaderIcon>
      <Icon content={CloudUpload} size="threeXL" />
    </StyledFileDropzoneInstructionsFileUploaderIcon>
    <StyledFileDropzoneInstructionsColumn>
      <StyledFileDropzoneInstructionsStyledSpan>
        Drag and drop file{multiple ? "s" : ""} here
      </StyledFileDropzoneInstructionsStyledSpan>
      <Small>
        {`Limit ${getSizeDisplay(maxSizeBytes, FileSize.Byte, 0)} per file`}
        {acceptedExtensions.length
          ? ` • ${acceptedExtensions
              .map(ext => ext.replace(/^\./, "").toUpperCase())
              .join(", ")}`
          : null}
      </Small>
    </StyledFileDropzoneInstructionsColumn>
  </StyledFileDropzoneInstructions>
)

export default FileDropzoneInstructions
