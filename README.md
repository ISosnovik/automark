# AutoMark :pencil2:

AutoMark is a lightweight tool for testing programming assignments written in Python.

It consists of a server application and a client-side script. The script should be placed in the same folder as the notebook (or the script with user functions) which is needed to be tested.

It was developed for the *Applied Machine Learning* course at the University of Amsterdam. You can check the application of its earlier versions for the course. 
- [AML 2017](https://github.com/ISosnovik/UVA_AML17)
- [AML 2018](https://github.com/JanJetze/UVA_AML18)
- [AML 2019](https://github.com/davzha/UVA_AML19)

Check [the example](https://github.com/ISosnovik/automark/tree/master/example)


## Server
The client-server interaction works as follows:

1) A user runs [`automark.test_student_function`](./automark.py)
2) The client script checks if there are local tests available. If so, it compares their MD5 with the one from the server. If the MD5 is different or if no tests are available, the script downloads the up-to-date local tests
3) If all tests are successfully passed, it makes a request to the server
2) The server checks
    1) if the requested assignment exists
    2) if the user is registered
    3) if the user is not making too many requests (*1 every 30 seconds*)
3) The server chooses a random set of inputs and sends it to the user
4) The client script evaluates the function with the received set of inputs, obtains an output and sends it to the server
5) The server compares the received output and the ground truth. If they are identical up to sum error (1e-8) the server returns `True` and marks the assignment as completed for this user.

The server application has the following structure, part of which is created at runtime:

```
automark_server/
├── assignments/
│   ├── local_tests.pickle
│   └── remote_tests.pickle
├── users/
│   ├── user_info/
│   │   ├── user_1.json
│   │   └── ...
│   └── user_progress/
│       ├── user_1.json
│       └── ...
├── main.py
├── utils.py
└── wrappers.py
```

## Client
The client script has two public methods
- `automark.get_progress(username)` prints the progress
```
---------------------------------------------
| username                                  |
| user@mail.xyz                             |
---------------------------------------------
| assignment1               | not attempted |
| assignment1               | attempted     |
| assignment3               | completed     |
---------------------------------------------
```
- `automark.test_student_function(username, function, arg_keys)` - the main function to test student functions.

## Requirements
For server:
```
flask 
werkzeug
numpy
```

For client
```
requests
numpy
```

## Credits
The earlier version of AutoMark is based on [dxdydz/automark](https://github.com/dxdydz/automark). I'd like to thank Thomas Mensink for his suggestions for the development of AutoMark.
