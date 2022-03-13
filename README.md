# Robot Framework POC for CAM test automation

Easier way to implement some test automations

## Environment (prerequisite)

[Python 3.9.1](https://www.python.org/downloads/release/python-391/)  
pip version 20.2.3

## Installation and run

Make sure you have your CAM downloaded  
Install the python packages in [requirements.txt](requirements.txt)

```
$ cd work-playground
$ git checkout ming-try-actions
$ pip3 install -r requirements.txt
```

Run the test

```
$ robot test/login_test.robot
```

Send the report to the Slack channel and update the TestRail result

```
$ python3 main.py
```
