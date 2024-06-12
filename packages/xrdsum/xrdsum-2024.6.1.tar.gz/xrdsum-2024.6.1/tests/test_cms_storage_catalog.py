from __future__ import annotations

import pytest

from xrdsum import storage_catalog
from xrdsum.storage_catalog import AVAILABLE_STORAGE_CATALOGS

ConfigType = tuple[str, str]


@pytest.fixture()
def cms_config() -> ConfigType:
    return "tests/storage.xml", "direct"


@pytest.mark.parametrize(
    ("path", "result"),
    [
        ("/store/user/johndoe/test.txt", True),
        ("/xrootd/cms/store/user/johndoe/test.txt", False),
        ("/xrootd/othervo/test.txt", False),
    ],
)
def test_is_cms_path(cms_config: ConfigType, path: str, result: bool) -> None:
    cms = storage_catalog.CMSStorageCatalog(*cms_config)
    assert cms.is_cms_path(path) == result


@pytest.mark.parametrize(
    ("lfn", "pfn"),
    [
        ("/store/user/johndoe/test.txt", "/xrootd/cms/store/user/johndoe/test.txt"),
        (
            "/xrootd/cms/store/user/johndoe/test.txt",
            "/xrootd/cms/store/user/johndoe/test.txt",
        ),
        ("/xrootd/othervo/test.txt", "/xrootd/othervo/test.txt"),
    ],
)
def test_cms_catalog(cms_config: ConfigType, lfn: str, pfn: str) -> None:
    assert "cms" in AVAILABLE_STORAGE_CATALOGS
    storage_catalog, protocol = cms_config
    catalog = AVAILABLE_STORAGE_CATALOGS["cms"](storage_catalog, protocol)
    assert catalog.lfn2pfn(lfn) == pfn
