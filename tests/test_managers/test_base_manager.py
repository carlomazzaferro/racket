import os
import shutil
import pytest
from racket.managers.constants import TEMPLATE_PROJECT_FILES
from racket.managers.base import BaseConfigManager
from racket.managers.project import ProjectManager
from racket.models.exceptions import NotInitializedError


def test_default():
    assert BaseConfigManager.IS_GLOBAL is False
    assert BaseConfigManager.RACKET_DIR is None
    assert BaseConfigManager.CONFIG_FILE_NAME is None
    assert BaseConfigManager.CONFIG is None


def test_project():
    ProjectManager.set_path(None)
    with pytest.raises(NotInitializedError):
        ProjectManager.get_models()


def test_get_config_file_path():

    BaseConfigManager.CONFIG_FILE_NAME = 'wrongfile.yml'
    assert BaseConfigManager.get_config() is None
    assert BaseConfigManager.get_value('key') is None

    BaseConfigManager.CONFIG_FILE_NAME = 'racket.yaml'
    assert BaseConfigManager.is_initialized() is False
    assert os.path.dirname(BaseConfigManager.get_config_file_path()) == '.'

    BaseConfigManager.RACKET_DIR = 'tests/sample_project'
    assert BaseConfigManager.is_initialized() is True
    assert os.path.basename(BaseConfigManager.get_config_file_path()) == 'racket.yaml'

    with pytest.raises(AttributeError):
        BaseConfigManager.get_value('key')

    assert isinstance(BaseConfigManager.get_config(), dict)
    assert BaseConfigManager.get_value('name') == 'sample_project'
    assert BaseConfigManager.get_value('logging') == {'level': 'INFO'}

    BaseConfigManager.set_config(init=False)
    assert os.path.isfile(os.path.join(BaseConfigManager.RACKET_DIR, BaseConfigManager.CONFIG_FILE_NAME))
    assert 'name' in BaseConfigManager.CONFIG.keys()
    assert 'sample_project' == BaseConfigManager.CONFIG['name']

    assert BaseConfigManager.set_config(init=False) is None

    BaseConfigManager.create_dir('tests/test-dir')
    assert os.path.isdir('tests/test-dir')
    shutil.rmtree('tests/test-dir')


def test_project_manager():
    ProjectManager.set_path('tests/sample_project')
    assert ProjectManager.RACKET_DIR == 'tests/sample_project'

    ProjectManager.set_path('tests/sample_project-2')
    ProjectManager.create_subdirs()
    assert os.path.exists('tests/sample_project-2') is True
    shutil.rmtree('tests/sample_project-2')

    ProjectManager.set_path('tests/sample_project')
    ProjectManager.create_template()
    for file in TEMPLATE_PROJECT_FILES:
        file_path = file.replace('template/', '')
        assert os.path.isfile(os.path.join(ProjectManager.RACKET_DIR, file_path))

