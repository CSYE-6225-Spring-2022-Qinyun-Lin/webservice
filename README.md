# webservice
This is a web application based on various AWS resources with CI/CD, currently functions including:
```
  - Create user
  - Update user information
  - Get user information
  - upload user profile image
  - get user profile image
  - delete user profile image
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
        - boto3
        (below are for unit test)
        - unittest
        - pytest

    - Database:  MySQL (AWS RDS)


## Deploy
Go to root dict and run ```python3 src/service.py```

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

## Verify the status of RDS
Go to root dict and run ```python3 src/utils/verify_rds.py```


## Import SSL Certificate to AWS
```
aws acm import-certificate --profile=demo --certificate fileb://prod_linqinyun_me/prod_linqinyun_me.crt --certificate-chain fileb://prod_linqinyun_me/prod_linqinyun_me.ca-bundle --private-key fileb://prod_linqinyun_me/private.key
```

