import logging
from distutils.version import StrictVersion
from typing import Tuple

from racket.managers.server import ServerManager
from racket.models import db
from racket.models.base import MLModel
from racket.models.exceptions import VersionError

log = logging.getLogger('root')


class VersionManager:

    @classmethod
    def check_version(cls, semantic: str, name: str) -> Tuple[str, str]:
        latest_smv, latest_disk = cls.max_version(name, semantic)

        if cls.compare(semantic, latest_smv) == 'GT':
            return semantic, latest_disk
        elif cls.compare(semantic, latest_smv) == 'EQ':
            new_v = cls.bump_version(semantic)
            log.warning(f'Model with version {semantic} already exists. Bumping version to {new_v}')
            return new_v, cls.bump_disk(latest_disk)
        else:
            raise VersionError(f'Version provided is strictly smaller than latest version for the model named: {name}, '
                               f'please increase the version on your model instantiation')

    @classmethod
    def bump_version(cls, semantic: str) -> str:
        return semantic[0:-1] + cls.bump_disk(semantic[-1])

    @classmethod
    def decr_version(cls, semantic: str) -> str:
        return semantic[0:-1] + cls.decr_disk(semantic[-1])

    @classmethod
    def bump_disk(cls, v: str) -> str:
        return str(int(v) + 1)

    @classmethod
    def decr_disk(cls, v: str) -> str:
        return str(int(v) - 1)

    @classmethod
    def max_version(cls, model_name: str, semantic: str) -> Tuple[str, str]:
        app = ServerManager.create_app('dev', False)
        with app.app_context():
            version = db.session.query(MLModel.major, MLModel.minor, MLModel.patch, MLModel.version_dir) \
                .filter(MLModel.model_name == model_name) \
                .order_by(MLModel.major.desc(),
                          MLModel.minor.desc(),
                          MLModel.patch.desc()).first()
            if not version:
                return cls.decr_version(semantic), '1'
        return '.'.join([str(version.major), str(version.minor), str(version.patch)]), version.version_dir

    @classmethod
    def compare(cls, v, vv):
        sv, svv = StrictVersion(v), StrictVersion(vv)
        if sv > svv:
            return 'GT'
        elif sv == svv:
            return 'EQ'
        else:
            return 'LT'