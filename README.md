# webservice
This is a health care web application, currently functions including :
```
  - Create user
  - Update user information
  - Get user information
```
The framework used is ```Python-Flask```

## Prerequisite & used libraries
    - Python 3.x
        - flask
        - mysql.connector
        - base64
        - json
        - hashlib
        - datetime
        - re
        (below are for unit test)
        - unittest
        - pytest

    - Database:  MySQL


## Deploy
Go to root dict and run ```python src/service.py```

The app will run on port 3333

## Unit Test
Method 1:
  Using pytest to perform the unit test without manually run python code, so as the action workflow.
```
  pip install pytest
  pytest
```

method 2:
  Manually run test_request.py
```
  python src/test_request.py
```
