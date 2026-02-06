import sys
from pathlib import Path
from shutil import rmtree
from uuid import uuid4

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def workspace_tmp_dir() -> Path:
    base_dir = ROOT / ".tmp_test_runs"
    base_dir.mkdir(exist_ok=True)

    run_dir = base_dir / f"run_{uuid4().hex}"
    run_dir.mkdir()
    try:
        yield run_dir
    finally:
        rmtree(run_dir, ignore_errors=True)
