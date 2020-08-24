"""
AutoMark is a lightweight tool for testing programming assignments
 
Copyright (C) 2020 Ivan Sosnovik

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import utils
import math
import time


class ServerError(AssertionError):
    pass


def catch_error(func):
    def wrapper(**kwargs):
        try:
            return func(**kwargs)
        except ServerError as e:
            return utils.error_response(str(e))

    wrapper.__name__ = "catch_error_" + func.__name__
    return wrapper


def check_username(storage):
    def _check_username(func):
        def wrapper(**kwargs):
            username = kwargs['username']
            if not username in storage.users:
                raise ServerError("user '{}' is not registered.".format(username))
            return func(**kwargs)

        wrapper.__name__ = "check_username_" + func.__name__
        return wrapper

    return _check_username


def check_timeout(storage):
    def _check_timeout(func):
        def wrapper(**kwargs):
            username = kwargs['username']
            if username in storage.timeout:
                delta = math.ceil(storage.timeout[username] - time.time())
                if delta > 0.0:
                    raise ServerError("your timeout expires in {} sec.".format(delta))
            return func(**kwargs)

        wrapper.__name__ = "check_timeout_" + func.__name__
        return wrapper

    return _check_timeout


def check_assignment(storage):
    def _check_assignment(func):
        def wrapper(**kwargs):
            assignment = kwargs['assignment']
            if not assignment in storage.data_dict:
                raise ServerError("assignment '{}' is not found.".format(assignment))
            return func(**kwargs)

        wrapper.__name__ = "check_assignment_" + func.__name__
        return wrapper

    return _check_assignment


def add_timeout(storage, timeout):
    def _add_timeout(func):
        def wrapper(**kwargs):
            username = kwargs['username']
            storage.timeout[username] = time.time() + timeout
            return func(**kwargs)

        wrapper.__name__ = "add_timeout_" + func.__name__
        return wrapper

    return _add_timeout
