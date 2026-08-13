"""Write a scan result as a single JSON report -- the one persistent
format the entropy budget allows.
"""

from __future__ import annotations

import json
from pathlib import Path

from claim_card.scan import ScanResult


def write_report(result: ScanResult, out_path: str | Path) -> None:
    out_path = Path(out_path)
    out_path.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
