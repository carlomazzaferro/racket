import pytest

from racket.managers.version import VersionManager
from racket.models.exceptions import VersionError


@pytest.fixture
def vm():
    vm_ = VersionManager
    yield vm_


def test_compare(vm):
    v1 = '1.0.1'
    v2 = '1.1.1'
    assert vm.compare(v1, v2) == 'LT'
    assert vm.compare(v2, v1) == 'GT'
    assert vm.compare('1.0.1', v1) == 'EQ'


def test_bump_v(vm):
    assert vm.bump_version('1.0.1') == '1.0.2'


def test_decr_v(vm):
    assert vm.decr_version('1.0.1') == '1.0.0'


def test_max_v(vm, init_project):
    assert vm.max_version('non-existing-model', '1.0.1') == ('1.0.0', '1')


def test_check_v(vm, init_project):
    assert vm.check_version('1.0.1', 'n-e-m') == ('1.0.1', '1')


def test_split(vm, init_project):
    assert vm.semantic_to_tuple('1.1.1') == (1, 1, 1)
    with pytest.raises(VersionError):
        vm.semantic_to_tuple('1.1.1.1')
    with pytest.raises(VersionError):
        vm.semantic_to_tuple('1.1.-1')
