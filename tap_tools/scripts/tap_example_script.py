#!/usr/bin/env python

from __future__ import absolute_import, unicode_literals, division, print_function

"""
example script, just to show how to do it, and to test the setup
"""

import tap_tools


def main():
    print("Running the tap_example_script")
    print("tap_tools version:", tap_tools.__version__)


if __name__ == "__main__":
    main()
