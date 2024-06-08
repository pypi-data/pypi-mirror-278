# --------------------------------------------------------------------------
# ⚠️ WARNING - AUTO-GENERATED CODE - DO NOT EDIT ⚠️
# ⚙️ Generated by 'python -m opgen'
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------
# pylint: disable=W0221,W0222,R0901,W0237
# mypy: disable-error-code=override
# ruff: noqa: N801,E741
# ruff: noqa: D214,D402,D405,D411,D412,D416,D417
# --------------------------------------------------------------------------

from __future__ import annotations

from typing import TypeVar

from onnx.defs import get_schema

from onnxscript.onnx_opset._impl.opset3 import Opset3
from onnxscript.onnx_types import (
    BOOL,
    COMPLEX64,
    COMPLEX128,
    DOUBLE,
    FLOAT,
    FLOAT16,
    INT8,
    INT16,
    INT32,
    INT64,
    STRING,
    UINT8,
    UINT16,
    UINT32,
    UINT64,
)
from onnxscript.values import Op, Opset


class Opset4(Opset3):
    def __new__(cls):
        return Opset.__new__(cls, "", 4)

    T_Concat = TypeVar(
        "T_Concat",
        BOOL,
        COMPLEX128,
        COMPLEX64,
        DOUBLE,
        FLOAT,
        FLOAT16,
        INT16,
        INT32,
        INT64,
        INT8,
        STRING,
        UINT16,
        UINT32,
        UINT64,
        UINT8,
    )

    def Concat(self, *inputs: T_Concat, axis: int) -> T_Concat:
        r"""[🌐 Concat(4)](https://onnx.ai/onnx/operators/onnx__Concat.html#concat-4 "Online Documentation")

        Concatenate a list of tensors into a single tensor

        Args:
            inputs: (variadic) List of tensors for concatenation

            axis: Which axis to concat on
        """

        schema = get_schema("Concat", 4, "")
        op = Op(self, "Concat", schema)
        return op(*self._prepare_inputs(schema, *inputs), axis=axis)
