#!/usr/bin/env python3
"""
Smoke test for the built package.
Verifies that the package can be imported and basic functionality works.
"""

import sys


def main():
    # 1. 尝试导入包的主模块
    try:
        import pystatpower
    except ImportError as e:
        print(f"Failed to import pystatpower: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. 可选：打印版本，确认版本号正确
    try:
        print(f"Imported {pystatpower.__name__} version {pystatpower.__version__}")
    except AttributeError:
        print("Package does not expose __version__")

    # 3. 测试一个最基本的 API 调用
    try:
        result = pystatpower.models.proportion.independent.noninferiority.size(
            alpha=0.05,
            power=0.8,
            treatment_proportion=0.8,
            reference_proportion=0.8,
            margin=-0.10,
        )
        assert result is not None
    except Exception as e:
        print(f"Basic functionality test failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("Smoke test passed!")


if __name__ == "__main__":
    main()
