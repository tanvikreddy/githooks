from __future__ import annotations

import subprocess
from typing import List
from typing import Set
import re

# ANSI color codes
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color


def added_files(include_expr: str = r'.*') -> list[str]:
    """Return a list of staged files."""
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
        stdout=subprocess.PIPE,
        encoding='utf-8',
        check=True,
    )
    files = result.stdout.splitlines()
    return [
        f for f in files
        if re.search(include_expr, f)
    ]