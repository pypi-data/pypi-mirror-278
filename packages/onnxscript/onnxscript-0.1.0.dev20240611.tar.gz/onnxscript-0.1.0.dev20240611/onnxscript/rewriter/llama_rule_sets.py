# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
from __future__ import annotations

import onnxscript.ir as ir
import onnxscript.rewriter.no_op as no_op
import onnxscript.rewriter.pattern as orp

op = orp.onnxop


def transpose_identity_pattern(op, x, perm):
    return op.Transpose(x, perm=perm)


def transpose_identity_check(context, x: ir.Value, perm: ir.Attr | ir.RefAttr) -> bool:
    if isinstance(perm, ir.RefAttr):
        return False
    if perm.type == ir.AttributeType.INTS:
        if perm.value == list(range(len(perm.value))):
            return True
    return False


def transpose_identity_rewrite(op, x: ir.Value, perm: ir.Attr | None = None):
    return op.Identity(x)


def transpose_transpose_pattern(op, x, perm1, perm2):
    return op.Transpose(op.Transpose(x, perm=perm1), perm=perm2)


def transpose_transpose_check(
    context, x: ir.Value, perm1: ir.Attr | ir.RefAttr, perm2: ir.Attr | ir.RefAttr
) -> bool:
    if isinstance(perm1, ir.RefAttr) or isinstance(perm2, ir.RefAttr):
        return False
    return True


def _apply_transpose(perm: tuple[int, ...], on: list[int]) -> list[int]:
    assert len(perm) == len(on), "length mismatch"
    res = [-1 for i in on]
    for i, p in enumerate(perm):
        res[i] = on[p]
    return res


def _apply_transposes(perms: list[tuple[int, ...]], on: list[int] | None = None) -> list[int]:
    if on is None:
        on = list(range(len(perms[0])))
    for p in perms:
        on = _apply_transpose(p, on)
    return on


def transpose_transpose_rewrite(op, x: ir.Value, perm1: ir.Attr, perm2: ir.Attr):
    first = list(range(len(perm1.value)))
    last = _apply_transposes([perm1.value, perm2.value])
    if first == last:
        return op.Identity(x)
    return op.Transpose(x, perm=last)


transpose_identity_rule = orp.RewriteRule(
    transpose_identity_pattern, transpose_identity_rewrite, transpose_identity_check
)
transpose_transpose_rule = orp.RewriteRule(
    transpose_transpose_pattern, transpose_transpose_rewrite, transpose_transpose_check
)


def llama_p0_rule_set() -> orp.RewriteRuleSet:
    """Returns a set of rules which should be applied
    before any other one as they usually remove unnecessary computation
    such as the multiplication by 1 or two consecutive transpose.

    Returns:
        RewriteRuleSet
    """
    return orp.RewriteRuleSet(
        [
            no_op.mul_by_1_rule,
            no_op.add_0_rule,
            no_op.add_0_rule,
            no_op.div_by_1_rule,
            transpose_identity_rule,
            transpose_transpose_rule,
        ]
    )
