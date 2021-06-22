# -*- coding: utf-8 -*-
"""
"""

import shutil
import os
import unittest
import sys
import ast

tc = unittest.TestCase()
bin, in_path, with_clang = sys.argv[1:]

in_path = ast.literal_eval(in_path)
with_clang = ast.literal_eval(with_clang)

# Assert that WinLib's gcc exists,
gcc = os.path.join(bin, 'gcc.exe')
assert os.path.exists(gcc), gcc

# Is the to 1st in PATH (if that is what we want),
if in_path:
    tc.assertEqual(shutil.which("gcc").lower(), gcc.lower())
elif shutil.which("gcc") is not None:
    tc.assertNotEqual(shutil.which("gcc").lower(), gcc.lower())

# Test availability of clang.
clang = os.path.join(bin, "clang.exe")
if with_clang:
    assert os.path.exists(clang), clang
    if in_path:
        tc.assertEqual(shutil.which("clang").lower(), clang.lower())
else:
    assert not os.path.exists(clang), clang
