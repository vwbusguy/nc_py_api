import pytest

from nc_py_api import Nextcloud

from gfixture import NC_TO_TEST

APP_NAME = "files_trashbin"


@pytest.mark.parametrize("nc", NC_TO_TEST)
def test_list_apps_types(nc):
    assert isinstance(nc.apps.get_list(), list)
    assert isinstance(nc.apps.get_list(enabled=True), list)
    assert isinstance(nc.apps.get_list(enabled=False), list)


@pytest.mark.parametrize("nc", NC_TO_TEST)
def test_list_apps(nc):
    apps = nc.apps.get_list()
    assert apps
    assert APP_NAME in apps


@pytest.mark.skipif(not isinstance(NC_TO_TEST[:1][0], Nextcloud), reason="Not available for NextcloudApp.")
@pytest.mark.parametrize("nc", NC_TO_TEST[:1])
def test_enable_disable_app(nc):
    assert nc.apps.is_installed(APP_NAME)
    if nc.apps.is_enabled(APP_NAME):
        nc.apps.disable(APP_NAME)
    assert nc.apps.is_disabled(APP_NAME)
    assert not nc.apps.is_enabled(APP_NAME)
    assert nc.apps.is_installed(APP_NAME)
    nc.apps.enable(APP_NAME)
    assert nc.apps.is_enabled(APP_NAME)
    assert nc.apps.is_installed(APP_NAME)


@pytest.mark.parametrize("nc", NC_TO_TEST[:1])
def test_invalid_param(nc):
    with pytest.raises(ValueError):
        nc.apps.is_enabled("")
    with pytest.raises(ValueError):
        nc.apps.is_installed("")
    with pytest.raises(ValueError):
        nc.apps.is_disabled("")
    with pytest.raises(ValueError):
        nc.apps.enable("")
    with pytest.raises(ValueError):
        nc.apps.disable("")
