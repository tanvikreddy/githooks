from __future__ import annotations

import os
import re
import sys
from typing import Sequence

from pre_commit_hooks.util import added_files, Colors

def validate_customapi_security(filenames: Sequence[str]) -> int:
    print(f"\n{Colors.BLUE}{Colors.BOLD}🔍 CUSTOM API SECURITY VALIDATION{Colors.NC}")
    print(f"{Colors.BLUE}────────────────────────────────────────────────────────{Colors.NC}")

    if not filenames:
        print(f"{Colors.GREEN}✓ No customapi.xml files to validate{Colors.NC}")
        return 0

    print(f"{Colors.YELLOW}Found {len(filenames)} customapi.xml file(s) to validate{Colors.NC}")

    exit_code = 0

    for file in filenames:
        if not os.path.isfile(file):
            print(f"  {Colors.RED}✗ File not found: {file}{Colors.NC}")
            continue

        print(f"  {Colors.BLUE}Checking API security for:{Colors.NC} {Colors.YELLOW}{file}{Colors.NC}")

        with open(file, encoding='utf-8') as f:
            content = f.read()

        if not re.search(r'<executeprivilegename>prv[A-Za-z0-9_]*</executeprivilegename>', content):
            print(f"    {Colors.RED}Missing required privilege tag: {Colors.BOLD}<executeprivilegename>prv*</executeprivilegename>{Colors.NC}")
            exit_code = 1

    if exit_code:
        print(f"\n{Colors.RED}{Colors.BOLD}⚠️  SECURITY VALIDATION FAILED ⚠️{Colors.NC}")
        print(f"{Colors.RED}Some customapi.xml files are missing required security configuration.{Colors.NC}")
        print(f"\n{Colors.YELLOW}{Colors.BOLD}REQUIRED ACTION:{Colors.NC}")
        print(f"{Colors.YELLOW}Add {Colors.BOLD}<executeprivilegename>prvYourPrivilegeName</executeprivilegename>{Colors.NC}{Colors.YELLOW} tag to each custom API XML file{Colors.NC}")
    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ API SECURITY VALIDATION PASSED{Colors.NC}")
        print(f"{Colors.GREEN}All custom API files have proper security configuration.{Colors.NC}\n")

    return exit_code


def main() -> int:
    pattern = r'customapis?/.*?/customapi\.xml$'
    customapi_files = sorted(added_files(include_expr=pattern))
    return validate_customapi_security(customapi_files)


if __name__ == '__main__':
    sys.exit(main())
