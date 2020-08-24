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

import os
import json
import hashlib
import pickle
import glob
from flask import jsonify, send_from_directory


CWD = os.path.dirname(os.path.realpath(__file__))


##############
# tools
##############
def get_md5():
    fname = os.path.join(CWD, 'assignments/local_tests.pickle')
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def error_response(error):
    return jsonify({"error": error}), 300


def send_local_tests():
    file_dir = os.path.join(CWD, 'assignments')
    return send_from_directory(file_dir, 'local_tests.pickle')


def _user_progress_path_by(username):
    filepath = 'users/user_progress/{}.json'.format(username)
    filepath = os.path.join(CWD, filepath)
    return filepath


##############
# get
##############
def get_user_info(username):
    filepath = os.path.join(CWD, 'users/user_info/{}.json'.format(username))
    with open(filepath) as f:
        data = json.loads(f.read())
    return data


def get_users_list():
    pattern = os.path.join(CWD, 'users', 'user_info', '*.json')
    users = [os.path.basename(f) for f in glob.glob(pattern)]
    users = sorted([f.split('.')[0] for f in users])
    return users


def get_users_progress():
    # get the list of users' progress dicts
    users_progress = {}

    for username in get_users_list():
        progress_path = _user_progress_path_by(username)
        try:
            with open(progress_path) as f:
                progress = json.loads(f.read())
        except FileNotFoundError:
            progress = {}
        users_progress[username] = progress
    return users_progress


def get_data_dict():
    filepath = os.path.join(CWD, 'assignments/remote_tests.pickle')
    with open(filepath, 'rb') as f:
        data_dict = pickle.load(f, encoding='latin1')
    return data_dict


##############
# update
##############
def update_progress(username, current_progress):
    # write the current progress to the file
    filepath = _user_progress_path_by(username)
    with open(filepath, 'w') as f:
        f.write(json.dumps(current_progress))
