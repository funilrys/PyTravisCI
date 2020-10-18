"""
Just another Python API for Travis CI (API).

A module which provides the base of all our resource type objects.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Project link:
    https://github.com/funilrys/PyTravisCI

Project documentation:
    https://pytravisci.readthedocs.io/en/latest/

License
::


    MIT License

    Copyright (c) 2019, 2020 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import json
from datetime import datetime
from typing import Any, Optional, Union

import PyTravisCI.communicator._all as communicator
import PyTravisCI.defaults as defaults
import PyTravisCI.exceptions as exceptions
import PyTravisCI.requester as requester
from PyTravisCI.communicator.base import CommunicatorBase


class ComplexJsonEncoder(json.JSONEncoder):
    """
    Provides ours complex JSON encoder.
    """

    def default(self, o: Any):  # pragma: no cover
        """
        Implements our complex conversion to JSON.
        """

        if isinstance(o, ResourceTypesBase):
            return o.__dict__
        if isinstance(o, datetime):
            return o.strftime(defaults.formats.STANDARD_DATE_FORMAT)
        if isinstance(o, (requester.Requester, CommunicatorBase)):
            return "<<< can't be serialized >>>"

        return super().default(o)


class ResourceTypesBase:
    """
    The base of all ressource types.
    """

    _PyTravisCI: dict() = {
        "com": dict(),
        "shared": dict(),
    }
    __iter_through__: Optional[str] = None
    __iter_index: Optional[int] = None
    __iter_max: Optional[int] = None

    _at_representation: Optional[str] = None
    _at_href: Optional[str] = None
    _at_pagination: Optional[str] = None

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)

    def __getitem__(self, index: Union[str, int]) -> Any:

        if isinstance(index, str):
            index = index.replace("@", "_at_")

        try:
            if hasattr(self, index):
                return getattr(self, index)
        except TypeError:
            if self.__iter_through__:
                return getattr(self, self.__iter_through__)[index]

        raise AttributeError(f"{index} (index) not found.")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.to_dict()} />"

    def __setattr__(self, name: str, value: Any) -> None:

        if (
            name == "__dict__"
            or name.startswith("_PyTravisCI")
            or name.startswith(f"_{__class__.__name__}")
            or name.startswith(f"_{self.__class__.__name__}")
        ):
            super().__setattr__(name, value)
        else:
            raise AttributeError(f"Assignment of <name> ({name}) not authorized.")

    def __setitem__(self, name: str, value: Any) -> None:
        setattr(self, name, value)

    def __iter__(self):
        if self.__iter_through__:
            self.__iter_index = 0
            self.__iter_max = len(self[self.__iter_through__])
            return self

        raise NotImplementedError()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __lt__(self, other):
        raise NotImplementedError()

    def __le__(self, other):
        raise NotImplementedError()

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        raise NotImplementedError()

    def __ge__(self, other):
        raise NotImplementedError()

    def __next__(self):
        if self.__iter_through__:
            if self.__iter_index < self.__iter_max:
                result = self[self.__iter_through__][self.__iter_index]
                self.__iter_index += 1

                return result
            self.__iter_index = 0
            raise StopIteration

        raise NotImplementedError()

    def __get_next_endpoint(self) -> Optional[str]:
        """
        Provides the next endpoint.
        """

        return self._at_pagination["next"]["_at_href"]

    def __get_previous_endpoint(self) -> Optional[str]:
        """
        Provides the previous endpoint.
        """

        return self._at_pagination["prev"]["_at_href"]

    def __get_first_endpoint(self) -> Optional[str]:
        """
        Provides the first endpoint.
        """

        return self._at_pagination["first"]["_at_href"]

    def __get_last_endpoint(self) -> Optional[str]:
        """
        Provides the last endpoint.
        """

        return self._at_pagination["last"]["_at_href"]

    def __get_href(self) -> Optional[str]:  # pragma: no cover
        """
        Provides the href of the current object.
        """

        return self._at_href

    @staticmethod
    def _get_resource_type_module() -> str:  # pragma: no cover
        """
        Provides the resource type module of the current class.
        """

        # pylint: disable=import-outside-toplevel
        from . import _all as resource_types

        return resource_types

    def json(self, *, remove_tags: bool = False) -> str:
        """
        Alias of :code:`to_json`.
        """

        return self.to_json(remove_tags=remove_tags)

    def to_json(self, *, remove_tags: bool = False) -> str:
        """
        Converts the current object to json.

        :param remove_tags:
            Remove all :code:`@tags` and everything
            related to PyTravisCI.
        """

        return json.dumps(
            self.to_dict(remove_tags=remove_tags),
            indent=4,
            sort_keys=False,
            ensure_ascii=False,
            cls=ComplexJsonEncoder,
        )

    def dict(self, *, remove_tags: bool = False) -> str:
        """
        Alias of :code:`to_dict`.
        """

        return self.to_dict(remove_tags=remove_tags)

    @classmethod
    def __format_to_dict(cls, data: Any, *, remove_tags: bool = False) -> Any:
        """
        A helper for the dict convertion.

        :param data:
            The data to work with.
        """

        if isinstance(data, list):
            return [cls.__format_to_dict(x) for x in data]

        if isinstance(data, dict):
            result = dict()

            for key, value in data.items():
                if remove_tags and key.startswith("_at_"):
                    continue

                if key.startswith("_PyTravisCI"):
                    continue

                if key.startswith("_at_"):
                    key = key.replace("_at_", "@")

                result[key] = cls.__format_to_dict(value)

            return result

        return data

    def to_dict(self, *, remove_tags: bool = False) -> dict:
        """
        Converts the current object to dict.

        :param remove_tags:
            Remove all :code:`@tags` and everything
            related to PyTravisCI.
        """

        result = {}

        for key, value in self.__format_to_dict(
            self.__dict__, remove_tags=remove_tags
        ).items():
            if isinstance(value, ResourceTypesBase):
                result[key] = value.to_dict(remove_tags=remove_tags)
            elif isinstance(value, list):
                try:
                    result[key] = [x.to_dict(remove_tags=remove_tags) for x in value]
                except AttributeError:
                    result[key] = value
            elif isinstance(value, datetime):
                result[key] = value.strftime(defaults.formats.STANDARD_DATE_FORMAT)
            else:
                result[key] = value

        return result

    def has_next_page(self) -> bool:
        """
        Checks if there is a next page to follow.
        """

        try:
            if self.__get_next_endpoint():
                return True
        except (AttributeError, KeyError, TypeError):
            pass
        return False

    def has_previous_page(self) -> bool:
        """
        Checks if there is a previous page to follow.
        """

        try:
            if self.__get_previous_endpoint():
                return True
        except (AttributeError, KeyError, TypeError):
            pass
        return False

    def has_first_page(self) -> bool:
        """
        Checks if there is a first page to follow.
        """

        try:
            if self.__get_first_endpoint():
                return True
        except (AttributeError, KeyError, TypeError):
            pass
        return False

    def has_last_page(self) -> bool:
        """
        Checks if there is a last page to follow.
        """

        try:
            if self.__get_last_endpoint():
                return True
        except (AttributeError, KeyError, TypeError):
            pass

        return False

    def is_incomplete(self) -> bool:
        """
        Checks if the current object is incomplete.

        An object is consired as incomplete if its representation
        is :code:`minimal`.
        """

        return (
            hasattr(self, "_at_representation")
            and self._at_representation
            and self._at_representation != "standard"
        )

    @CommunicatorBase.complete_response
    def next_page(self) -> Optional["ResourceTypesBase"]:  # pragma: no cover
        """
        Provides the next page.

        :raise NextPageNotFound:
            If the next page was not found.
        """

        if self.has_next_page():
            comm = getattr(communicator, self.__class__.__name__)(
                self._PyTravisCI["com"]["requester"]
            )

            response = comm.get_standardized(
                comm.get_response(self.__get_next_endpoint())
            )

            return getattr(
                self._get_resource_type_module(),
                self.__class__.__name__,
            )(**response)
        raise exceptions.NextPageNotFound()

    @CommunicatorBase.complete_response
    def previous_page(self) -> Optional["ResourceTypesBase"]:  # pragma: no cover
        """
        Provides the previous page.

        :raise PreviousPageNotFound:
            If the previous page was not found.
        """

        if self.has_previous_page():
            comm = getattr(communicator, self.__class__.__name__)(
                self._PyTravisCI["com"]["requester"]
            )

            response = comm.get_standardized(
                comm.get_response(self.__get_previous_endpoint())
            )

            return getattr(
                self._get_resource_type_module(),
                self.__class__.__name__,
            )(**response)
        raise exceptions.PreviousPageNotFound()

    @CommunicatorBase.complete_response
    def first_page(self) -> Optional["ResourceTypesBase"]:  # pragma: no cover
        """
        Provides the first page.

        :raise FirstPageNotFound:
            If the first page was not found.
        """

        if self.has_first_page():
            comm = getattr(communicator, self.__class__.__name__)(
                self._PyTravisCI["com"]["requester"]
            )

            response = comm.get_standardized(
                comm.get_response(self.__get_first_endpoint())
            )

            return getattr(
                self._get_resource_type_module(),
                self.__class__.__name__,
            )(**response)
        raise exceptions.FirstPageNotFound()

    @CommunicatorBase.complete_response
    def last_page(self) -> Optional["ResourceTypesBase"]:  # pragma: no cover
        """
        Provides the last page.

        :raise LastPageNotFound:
            If the last page was not found.
        """

        if self.has_last_page():
            comm = getattr(communicator, self.__class__.__name__)(
                self._PyTravisCI["com"]["requester"]
            )

            response = comm.get_standardized(
                comm.get_response(self.__get_last_endpoint())
            )

            return getattr(
                self._get_resource_type_module(),
                self.__class__.__name__,
            )(**response)
        raise exceptions.LastPageNotFound()

    @CommunicatorBase.complete_response
    def get_complete(self) -> Optional["ResourceTypesBase"]:  # pragma: no cover
        """
        Provides the complete representation if the current
        representation is the minimal one.
        """

        if self.is_incomplete():
            comm = getattr(communicator, self.__class__.__name__)(
                self._PyTravisCI["com"]["requester"]
            )

            response = comm.get_standardized(comm.get_response(self.__get_href()))

            return getattr(
                self._get_resource_type_module(),
                self.__class__.__name__,
            )(**response)
        raise exceptions.NotIncomplete()
