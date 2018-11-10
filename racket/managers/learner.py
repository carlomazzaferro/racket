import logging
import os
from typing import Tuple

from racket.managers.base import BaseConfigManager
from racket.models.exceptions import VersionError
from racket.operations.schema import max_version, compare

log = logging.getLogger('root')


class LearnerManager(BaseConfigManager):

    CONFIG_FILE_NAME = 'racket.yaml'
    INPUT_KEYS = 'x'
    OUTPUT_KEYS = 'y'
    PLATFORM = 'tensorflow'

    @classmethod
    def get_path(cls, name: str) -> str:
        return os.path.join(cls.get_value('saved-models'), name)

    @classmethod
    def latest_version(cls, name: str, semantic: str) -> Tuple[str, str]:
        return max_version(name, semantic)

    @classmethod
    def check_version(cls, semantic: str, name: str) -> Tuple[str, str]:
        latest_smv, latest_disk = cls.latest_version(name, semantic)

        if compare(semantic, latest_smv) == 'GT':
            return semantic, cls.bump_disk(latest_disk)
        elif compare(semantic, latest_smv) == 'EQ':
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
    def bump_disk(cls, v: str) -> str:
        return str(int(v) + 1)
