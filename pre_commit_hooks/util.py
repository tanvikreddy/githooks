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


def added_files(include_expr: str = r'.*', exclude_expr: str = None) -> list[str]:
    """Return a list of staged files.
    
    Args:
        include_expr: Regular expression pattern for files to include
        exclude_expr: Regular expression pattern for files to exclude
    """
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
        stdout=subprocess.PIPE,
        encoding='utf-8',
        check=True,
    )
    files = result.stdout.splitlines()
    filtered_files = [f for f in files if re.search(include_expr, f)]
    
    if exclude_expr:
        filtered_files = [f for f in filtered_files if not re.search(exclude_expr, f)]
        
    return filtered_files