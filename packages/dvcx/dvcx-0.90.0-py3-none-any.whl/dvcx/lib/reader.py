from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from dvcx.lib.feature_types import FeatureLike


class FeatureReader(ABC):
    def __init__(self, fr_class: "FeatureLike"):
        """
        Class to call on feature values to perform post-processing. Used when
        iterating over dataset with `ds.to_pytorch()` and `ds.get_values()`.

        The class must include:
        - `self.fr_class` to define the feature class to read.
        - `self.__call__(self, value)` to call on the feature value returned by
          `self.fr_class.get_value()`.

        Examples:
            >>> class PrefixReader(FeatureReader):
            >>>     def __call__(self, value):
            >>>         return "prefix-" + value
            >>> for row in ds.get_values(PrefixReader(MyFeature)):
            >>>     print(row)

            >>> class SuffixReader(FeatureReader):
            >>>     def __init__(self, fr_class, suffix):
            >>>         self.suffix = suffix
            >>>         super().__init__(fr_class)
            >>>     def __call__(self, value):
            >>>         return value + self.suffix
            >>> for row in ds.get_values(SuffixReader(MyFeature, "-suffix")):
            >>>     print(row)
        """
        self.fr_class = fr_class

    @abstractmethod
    def __call__(self, value: Any) -> Any:
        pass


class LabelReader(FeatureReader):
    def __init__(self, fr_class: "FeatureLike", classes: list):
        """Get column values as 0-based integer index of classes."""
        self.classes = classes
        super().__init__(fr_class)

    def __call__(self, value: str) -> int:
        return self.classes.index(value)
