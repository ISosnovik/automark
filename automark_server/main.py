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

----------------------------------------------------------------------

This scipt runs the server application of AutoMark.

/get_test_input/<username>/<assignment> 
    Returns the input data to test the assignment.

/check_answer/<username>/<assignment>/<int:ipd>/<answer>
    Returns `True` if the answer is correct, otherwise returns `False`.

/load_tests/<username>
    Sends the local tests.

/check_sum/<md5>
    Returns the md5 sum of the up-to-date local tests.

/get_progress/<username>
    Returns a json with the current progress of the user.
"""

from flask import Flask, jsonify, render_template
from werkzeug.serving import run_simple
from random import randrange
import numpy as np
import json

import utils
import wrappers

app = Flask(__name__)
app.config.from_object(__name__)


class Global:
    users = utils.get_users_list()
    progress = utils.get_users_progress()
    timeout = {}
    data_dict = utils.get_data_dict()

    def md5():
        return utils.get_md5()


#######################################
# Check I/O
#######################################
@app.route('/get_test_input/<username>/<assignment>', methods=['GET'])
@wrappers.catch_error
@wrappers.check_username(Global)
@wrappers.check_timeout(Global)
@wrappers.check_assignment(Global)
def get_test_input(username='', assignment=''):
    random_ipd = randrange(len(Global.data_dict[assignment]["ipd"]))
    dict_ = {
        "username": username,
        "ipd": int(Global.data_dict[assignment]["ipd"][random_ipd]),
        "input": Global.data_dict[assignment]['inputs'][random_ipd]
    }
    return jsonify(dict_)


@app.route('/check_answer/<username>/<assignment>/<int:ipd>/<answer>', methods=['GET'])
@wrappers.catch_error
@wrappers.check_username(Global)
@wrappers.check_timeout(Global)
@wrappers.check_assignment(Global)
@wrappers.add_timeout(Global, 30)
def check_answer(username='', assignment='', ipd=-1, answer=''):
    if not assignment in Global.progress[username]:
        Global.progress[username][assignment] = False
        utils.update_progress(username, Global.progress[username])

    ipd_idx = Global.data_dict[assignment]['ipd'].index(ipd)
    x_answer = np.array(json.loads(answer))
    x_true = Global.data_dict[assignment]['outputs'][ipd_idx]

    answer_is_correct = np.allclose(x_true, x_answer, atol=1e-5)
    if not Global.progress[username][assignment] and answer_is_correct:
        Global.progress[username][assignment] = answer_is_correct
        utils.update_progress(username, Global.progress[username])

    return jsonify({'success': answer_is_correct})


#######################################
# Local test
#######################################
@app.route('/load_tests/<username>')
@wrappers.catch_error
@wrappers.check_username(Global)
@wrappers.check_timeout(Global)
def load_tests(username=''):
    return utils.send_local_tests()


@app.route('/check_sum/<md5>')
def check_sum(md5):
    return jsonify({'success': md5 == Global.md5()})


#######################################
# etc
#######################################
@app.route('/get_progress/<username>')
@wrappers.catch_error
@wrappers.check_username(Global)
def get_progress(username=''):
    fancy_progress = {}
    user_progress = Global.progress[username]

    for func_desc in Global.data_dict.keys():
        if func_desc in user_progress:
            fancy_progress[func_desc] = 'completed' if user_progress[func_desc] else 'attempted'
        else:
            fancy_progress[func_desc] = 'not attempted'

    user_data = utils.get_user_info(username)
    data = {
        'name': user_data['name'],
        'mail': user_data['mail'],
        'progress': fancy_progress
    }
    return jsonify(data)


if __name__ == '__main__':
    run_simple('0.0.0.0',
               port=1234,
               application=app,
               use_reloader=True,
               reloader_interval=60 * 10,
               threaded=True)
