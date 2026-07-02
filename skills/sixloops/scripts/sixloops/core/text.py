"""Shared value-coercion helpers used across contract and guardrail modules.

这些是无状态的纯函数，多个契约模块（loop / autonomy / progression）和 guardrail
管道原本各自复制了一份几乎逐字相同的实现。集中到这里消除重复，保证行为一致。
"""

from __future__ import annotations

from typing import Any


def as_list(value: Any) -> list:
    # 把标量、None、列表统一成列表，便于下游逐项处理；None 视为空。
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def strings(value: Any) -> list[str]:
    # 转成非空字符串列表；纯空白项按"无内容"丢弃，避免它们让存在性检查误判为真。
    return [str(item) for item in as_list(value) if str(item).strip()]


def positive_int(value: Any, default: int) -> int:
    # 只接受严格正整数，非法输入或非正数回落到默认值（用于迭代/条数上限）。
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed > 0 else default


def merge_missing(primary: list[str], required: list[str]) -> list[str]:
    # 在保留 primary 顺序的前提下，把 required 里缺失的项补到末尾（用于契约字段兜底）。
    result = list(primary)
    seen = set(primary)
    result.extend(item for item in required if item not in seen)
    return result
