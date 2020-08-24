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


---------------------------------------------------------------------

This script generates 2 assignments: matmul and sigmoid
Each assignment is included in a file of local test and in a file of remote tests.

The file of local tests is a `.pickle` file whichhas the following structure
{
    "assignment1": {
        "inputs": [
            {"input1": input1, "input2": input2, ...},
            {"input1": input1, "input2": input2, ...},
            ...
        ],
        "outputs": [output1, output2, ...],
    },
    "assignment2": {...}
}

The file of remote tests is a `.pickle` file which has the following structure
{
    "assignment1": {
        "inputs": [
            {"input1": input1, "input2": input2, ...},
            {"input1": input1, "input2": input2, ...},
            ...
        ],
        "outputs": [output1, output2, ...],
        "ipd": [ipd1, ipd2, ...]
    },
    "assignment2": {...}
}

NOTE! the local tests do not contain the "ipd" fields while the remote tests do.
`ipd` is an identifier used to match the provided and the ground truth outputs 
for a randomly picked assignment.

"""

import numpy as np


def gt_matmul(A, B):
    return np.dot(A, B)


def gt_sigmoid(x):
    return 1 / (1 + np.exp(-x))


def crdict(data):
    "Utility function to pack arrays"
    data_type = type(data).__name__
    if data_type == 'ndarray':
        return {'data': data.tolist(), 'type': data_type}
    else:
        return {'data': data, 'type': data_type}


# Assinments
def create_matmul_remote():
    data_dict = {'inputs': [], 'outputs': []}

    ipds = list(np.random.choice(10000, 100, replace=False))
    data_dict['ipd'] = ipds

    for ipd in ipds:
        n1, n2, n3 = np.random.randint(1, 7, size=3)
        A = np.random.uniform(-10.0, 10.0, size=(n1, n2))
        B = np.random.uniform(-10.0, 10.0, size=(n2, n3))
        result = gt_matmul(A, B)

        data_dict['inputs'].append({
            'A': crdict(A),
            'B': crdict(B),
        })
        data_dict['outputs'].append(result)

    return data_dict


def create_sigmoid_remote():
    data_dict = {'inputs': [], 'outputs': []}

    ipds = list(np.random.choice(10000, 100, replace=False))
    data_dict['ipd'] = ipds

    for ipd in ipds:
        n1 = np.random.randint(1, 7, size=1)
        x = np.random.uniform(-10.0, 10.0, size=n1)
        result = gt_sigmoid(x)

        data_dict['inputs'].append({
            'x': crdict(x),
        })
        data_dict['outputs'].append(result)

    return data_dict


def create_matmul_local():
    data_dict = {'inputs': [], 'outputs': []}

    for _ in range(100):
        n1, n2, n3 = np.random.randint(1, 7, size=3)
        A = np.random.uniform(-10.0, 10.0, size=(n1, n2))
        B = np.random.uniform(-10.0, 10.0, size=(n2, n3))
        result = gt_matmul(A, B)

        data_dict['inputs'].append({
            'A': A,
            'B': B,
        })
        data_dict['outputs'].append(result)

    return data_dict


def create_sigmoid_local():
    data_dict = {'inputs': [], 'outputs': []}

    for _ in range(100):
        n1 = np.random.randint(1, 7, size=1)
        x = np.random.uniform(-10.0, 10.0, size=n1)
        result = gt_sigmoid(x)

        data_dict['inputs'].append({
            'x': x,
        })
        data_dict['outputs'].append(result)

    return data_dict


if __name__ == '__main__':
    import pickle

    local_tests = {
        'sigmoid': create_sigmoid_local(),
        'matmul': create_matmul_local()
    }

    with open('../automark_server/assignments/local_tests.pickle', 'wb') as f:
        pickle.dump(local_tests, f, protocol=2)

    remote_tests = {
        'sigmoid': create_sigmoid_remote(),
        'matmul': create_matmul_remote()
    }

    with open('../automark_server/assignments/remote_tests.pickle', 'wb') as f:
        pickle.dump(remote_tests, f, protocol=2)
