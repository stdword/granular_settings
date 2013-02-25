# coding: utf-8

import glob
import os
import re
import traceback


settings_module_path = os.path.abspath(traceback.extract_stack()[-2][0])
settings_dir_path = os.path.splitext(settings_module_path)[0]

project_path = os.path.abspath(traceback.extract_stack()[0][0])
PROJECT_PATH = os.path.split(project_path)[0]
PROJECT = os.path.split(PROJECT_PATH)[-1]


__all__ = ('PROJECT_PATH', 'PROJECT')


EMPTY_SUFFIX = '.'
DEFAULT_SUFFIX = '.conf'
LOCAL_SUFFIX = '.local'


class SuffixPriorityMap(object):
    base_suffix_priorities_map = {
        EMPTY_SUFFIX: '',
        DEFAULT_SUFFIX: '.',
        LOCAL_SUFFIX: '~',  # '~' больше любой буквенной строки
    }

    @classmethod
    def get_priority(cls, suffix):
        if not suffix:
            return ''

        if suffix in cls.base_suffix_priorities_map:
            return cls.base_suffix_priorities_map[suffix]

        return suffix[1:]


def _extract_granula_data(granula):
    res = re.search(r'^(\d+)', os.path.split(granula)[1])
    priority = res.group(1) if res else '0'

    suffix = os.path.splitext(granula)[1]
    if not suffix:
        suffix = '.'

    return priority, SuffixPriorityMap.get_priority(suffix)


###############################################################################


granulas = glob.glob(os.path.join(settings_dir_path, '*' + DEFAULT_SUFFIX))
granulas += glob.glob(os.path.join(settings_dir_path,
                      '*' + DEFAULT_SUFFIX + '.' + LOCAL_SUFFIX))

granulas.sort(key=_extract_granula_data)

for granula in granulas:
    execfile(os.path.abspath(granula))
