"""A simplistic text string access specification for deep structures."""

from __future__ import annotations
from typing import Any

__VERSION__ = "1.0"

class DotNest:
    """A class implementing data access by dotted-strings."""

    def __init__(self, data: dict | list, allow_creation: bool = False):
        """Initialize the class with an existing data structure."""
        self._data = data
        self._separator = "."
        self._allow_creation = allow_creation

    @property
    def data(self) -> dict | list:
        """The encapsulated data."""
        return self._data

    @data.setter
    def data(self, newdata: Any) -> None:
        self._data = newdata

    @property
    def separator(self) -> str:
        """The separator to use between tokens."""
        return self._separator

    @separator.setter
    def separator(self, newvalue) -> None:
        self._separator = newvalue

    def get(self, keys: str | list, create_dicts: bool = False) -> Any:
        """Return the value at a spot given a list of keys.

        keys must be either a dotted string ("element.other.3.foo")
        or a list of keys already parsed (["element", "other", "3",
        "foo"]).

        keys will be used as either keys to access a dict or an
        integer for accessing list elements.
        """
        keys = self.parse_keys(keys)
        ptr = self.data

        for n, k in enumerate(keys):
            if isinstance(ptr, list):
                if isinstance(k, str):
                    k = int(k)
                if len(ptr) <= k:
                    raise ValueError(f"list key #{n} int({k}) too large")
            if isinstance(ptr, dict) and k not in ptr:
                if create_dicts:
                    ptr[k] = {}
                else:
                    raise ValueError(f"key #{n} '{k}' not found in data")
            if ptr is None:
                return None

            ptr = ptr[k]

        return ptr

    def set(self, keys: str | list, value: Any) -> None:
        """Given a key set (see get()), set the value at this spot to value."""
        keys = self.parse_keys(keys)
        ptr = self.get(keys[0:-1], create_dicts=self._allow_creation)
        ptr[keys[-1]] = value

    def parse_keys(self, values: str | list) -> list:
        """Separate a list of keys by a '.' specifier.  AKA, split.

        If values is already a list, this will simply return it as is.
        """
        if isinstance(values, list):
            return values
        # TODO(hardaker): allow / pathing if values starts with a /?
        # TODO(hardaker): deal with escapes
        return values.split(self._separator)

    def __eq__(self, other: DotNest) -> bool:
        """Report whether this instance's data is equal to anothers."""
        return self.deep_compare(self.data, other.data)

    # from https://stackoverflow.com/questions/25044073/comparing-python-objects-from-deepcopy
    def deep_compare(self, left, right, excluded_keys = []) -> bool:
        """Deeply compare two structures."""
        # TODO(hardaker): why can't we use an existing compare?  I don't remember.
        # convert left and right to dicts if possible, skip if they can't be converted
        try:
            left = left.__dict__
            right = right.__dict__
        except Exception:
            pass

        # both sides must be of the same type
        if type(left) != type(right):
            return False

        # compare the two objects or dicts key by key
        if isinstance(left, dict):
            for key in left:
                # make sure that we did not exclude this key
                if key not in excluded_keys:
                    # check if the key is present in the right dict, if not, we are not equals
                    if key not in right:
                        return False

                    # compare the values if the key is present in both sides
                    if not self.deep_compare(left[key], right[key], excluded_keys):
                        return False

            # check if any keys are present in right, but not in left
            for key in right:
                if key not in left and key not in excluded_keys:
                    return False

            return True

        # check for each item in lists
        if isinstance(left, list):
            # right and left must have the same length
            if len(left) != len(right):
                return False

            # compare each item in the list
            for index in range(len(left)):
                if not self.deep_compare(left[index], right[index], excluded_keys):
                    return False

        # do a standard comparison
        return left == right
