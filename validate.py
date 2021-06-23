# -*- coding: utf-8 -*-
"""
"""

import shutil
import os
import unittest
import sys
import ast
import re
from subprocess import run, PIPE

tc = unittest.TestCase()
bin, in_path, with_clang, architecture = sys.argv[1:]

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

C_CODE = """
#include <stdio.h>
#include <stdint.h>

int main() {
    printf("Hello World!\\n");
    printf("Size of pointer is %i.\\n", sizeof(size_t));
    return 0;
}
"""

def test_compile(cc):
    exe = "./test-executable"
    run([cc, "-o", exe, "-x", "c", "-"],
        input=C_CODE, universal_newlines=True, check=True)
    p = run([exe], check=True, stdout=PIPE, universal_newlines=True)
    tc.assertRegex(p.stdout, r"Hello World!\nSize of pointer is \d\.\n")

    tc.assertEqual(
        re.search(r"Size of pointer is (\d)", p.stdout).group(1),
        "8" if architecture == "x86_64" else "4",
    )

test_compile(gcc)
if with_clang:
    test_compile(clang)
