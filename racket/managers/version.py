import logging
from distutils.version import StrictVersion
from typing import Tuple

from racket.utils import Printer as p
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
            return semantic, cls.bump_disk(latest_disk)
        elif cls.compare(semantic, latest_smv) == 'EQ':
            new_v = cls.bump_version(semantic)
            p.print_warning(f'Model with version {semantic} already exists. Bumping version to {new_v}')
            return new_v, cls.bump_disk(latest_disk)
        else:
            raise VersionError(f'Version provided is strictly smaller than latest version for the model named: {name}, '
                               f'please increase the version on your model instantiation')

    @classmethod
    def bump_version(cls, semantic: str) -> str:
        vvv = cls.split_(semantic)
        return cls.join_([vvv[0], vvv[1], str(cls.bump_disk(vvv[-1]))])

    @classmethod
    def split_(cls, v):
        return v.split('.')

    @classmethod
    def join_(cls, vvv):
        return '.'.join([str(i) for i in vvv])

    @classmethod
    def decr_version(cls, semantic: str) -> str:
        vvv = cls.split_(semantic)
        return cls.join_([vvv[0], vvv[1], str(cls.decr_disk(vvv[-1]))])

    @classmethod
    def bump_disk(cls, v: str) -> str:
        return str(int(v) + 1)

    @classmethod
    def decr_disk(cls, v: str) -> str:
        return str(int(v) - 1)

    @classmethod
    def max_v_from_name(cls, model_name: str):
        app = ServerManager.create_app('prod', False)
        with app.app_context():
            version = db.session.query(MLModel.major, MLModel.minor, MLModel.patch, MLModel.version_dir) \
                .filter(MLModel.model_name == model_name) \
                .order_by(MLModel.major.desc(),
                          MLModel.minor.desc(),
                          MLModel.patch.desc())
            print(version.all())
            return version.first()

    @classmethod
    def max_version(cls, model_name: str, semantic: str) -> Tuple[str, str]:
        v = cls.max_v_from_name(model_name)
        if not v:
            return cls.decr_version(semantic), '1'
        return cls.join_([v.major, v.minor, v.patch]), v.version_dir

    @classmethod
    def compare(cls, v: str, vv: str) -> str:
        if any(['-1' in cls.split_(p) for p in [v, vv]]):
            v, vv = cls.bump_version(v), cls.bump_version(vv)
        sv, svv = StrictVersion(v), StrictVersion(vv)
        if sv > svv:
            return 'GT'
        elif sv == svv:
            return 'EQ'
        else:
            return 'LT'

    @classmethod
    def semantic_to_tuple(cls, semantic: str) -> Tuple[int, ...]:
        mmp = [int(i) for i in cls.split_(semantic)]
        if len(mmp) != 3 or any([i < 0 for i in mmp]):
            raise VersionError('Version must be of form X.X.X where X is a positive integer')
        return tuple(mmp)

    @classmethod
    def parse_cli_v(cls, v) -> Tuple[str, int]:
        t = v[0]
        n = int(v[1:])
        if t not in {'M', 'm', 'p'}:
            raise VersionError('Version provided is invalid')
        return {'M': 'major', 'm': 'minor', 'p': 'patch'}[t], n
