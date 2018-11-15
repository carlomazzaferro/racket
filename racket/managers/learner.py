import logging
import os

from racket.models import db
from racket.models.base import MLModel
from racket.models.exceptions import ModelNotFoundError, validate_config
from racket.managers.base import BaseConfigManager
from racket.managers.server import ServerManager
from racket.managers.version import VersionManager
from racket.operations.schema import query_by_id_

log = logging.getLogger('root')


class LearnerManager(BaseConfigManager):
    CONFIG_FILE_NAME: str = 'racket.yaml'
    INPUT_KEYS: str = 'x'
    OUTPUT_KEYS: str = 'y'
    PLATFORM: str = 'tensorflow'

    @classmethod
    @validate_config
    def get_path(cls, name: str) -> str:
        return os.path.join(cls.get_value('saved-models'), name)

    @classmethod
    def bump_tf_version(cls, name: str, prev: str, new: str):
        p = cls.get_path(name)
        curr = os.path.join(p, prev)
        new = os.path.join(p, new)
        os.rename(curr, new)

    @classmethod
    @validate_config
    def query_by_id(cls, model_id: int) -> MLModel:
        return query_by_id_(model_id)

    @classmethod
    @validate_config
    def query_by_name_version(cls, name: str, version: str) -> MLModel:
        app = ServerManager.create_app('prod', False)
        with app.app_context():
            vvv = version.split('.')
            servable = db.session.query(MLModel).filter(MLModel.model_name == name) \
                                                .filter(MLModel.major == int(vvv[0])) \
                                                .filter(MLModel.minor == int(vvv[1])) \
                                                .filter(MLModel.patch == int(vvv[2])).one_or_none()
        if not servable:
            raise ModelNotFoundError(f'The model requested with name, version ({name}, {version})'
                                     f' was not found in the database')
        return servable

    @classmethod
    @validate_config
    def load_version_from_existing_servable(cls, servable: MLModel):
        current = VersionManager.max_v_from_name(servable.model_name)[-1]
        new = VersionManager.bump_disk(current)
        cls.bump_tf_version(servable.model_name, current, new)
        app = ServerManager.create_app('prod', False)
        with app.app_context():
            servable.version_dir = new
            db.session.commit()
