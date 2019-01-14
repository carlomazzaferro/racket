import os

import pytest

from racket.managers.learner import LearnerManager
from racket.managers.project import ProjectManager
from racket.models.base import MLModel
from racket.models.exceptions import ModelNotFoundError


def test_bump_tf_v(init_project):
    os.chdir('tests/sample_project')
    ProjectManager.RACKET_DIR = '.'

    LearnerManager.bump_tf_version('base', '1', '2')
    assert os.path.exists('serialized/base/2')

    assert isinstance(LearnerManager.query_by_id(1), MLModel)

    with pytest.raises(ModelNotFoundError):
        LearnerManager.query_by_name_version('nomodel', '1.2.1')

    queried = LearnerManager.query_by_name_version('base', '0.1.0')
    assert isinstance(queried, MLModel)

    os.rename('serialized/base/2', 'serialized/base/1')
    LearnerManager.load_version_from_existing_servable(queried)
    assert os.path.exists('serialized/base/2')
    # os.chdir('../../')
