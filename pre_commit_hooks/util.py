from __future__ import annotations

import subprocess
from typing import List
from typing import Set


# ANSI color codes
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color


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
    
    # Apply include and exclude patterns
    import re
    include_pattern = re.compile(include_expr)
    exclude_pattern = re.compile(exclude_expr)
    
    return {
        f for f in files 
        if include_pattern.search(f) and not exclude_pattern.search(f)
    }
