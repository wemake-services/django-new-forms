from typing import Final

from typing_extensions import Sentinel, TypeVar

EMPTY: Final = Sentinel('EMPTY')
ModelT = TypeVar('ModelT')
