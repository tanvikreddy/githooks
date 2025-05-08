from __future__ import annotations

import argparse
import os
import subprocess
from typing import Callable
from typing import Iterable
from typing import List
from typing import Sequence
from typing import Set


def zsplit(s: str) -> List[str]:
    """Split on null bytes."""
    parts = s.split('\0')
    if parts and not parts[-1]:
        parts.pop()
    return parts


def added_files(
    include_expr: str = r'.*', exclude_expr: str = r'^$'
) -> Set[str]:
    """List all files that have been added to the git repository."""
    cmd = ('git', 'ls-files', '--cached', '--others', '--exclude-standard')
    out = subprocess.check_output(cmd).decode('utf-8')
    files = set(zsplit(out))
    return files
