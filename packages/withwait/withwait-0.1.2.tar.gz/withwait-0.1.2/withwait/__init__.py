"""
# Withwait

A simple utility to ensure that sleep operations always complete, even if an
exception happens within the with statement.

Authors:
* Maddy Guthridge

Licensed under the MIT license
"""
__all__ = [
    'wait',
    'WithwaitAbort',
    'WithwaitAbortAll',
]

from .__withwait import wait, WithwaitAbort, WithwaitAbortAll
