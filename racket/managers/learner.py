import logging
import os

from racket.managers.base import BaseConfigManager

log = logging.getLogger('root')


class LearnerManager(BaseConfigManager):

    CONFIG_FILE_NAME = 'racket.yaml'
    INPUT_KEYS = 'x'
    OUTPUT_KEYS = 'y'
    PLATFORM = 'tensorflow'

    @classmethod
    def get_path(cls, name: str) -> str:
        return os.path.join(cls.get_value('saved-models'), name)
