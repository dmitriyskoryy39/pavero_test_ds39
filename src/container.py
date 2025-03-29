
from functools import lru_cache

from punq import Container, Scope

from src.config import get_settings, Settings


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Settings, instance=get_settings(), scope=Scope.singleton)


