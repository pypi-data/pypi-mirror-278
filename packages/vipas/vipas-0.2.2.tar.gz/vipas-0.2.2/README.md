# VIPAS
Python SDK for Vipas AI Platform

- Package version: 0.0.1

## Requirements.

Python 3.7+

## Installation & Usage
### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/vipas-engineering/vipas-python-sdk.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/vipas-engineering/vipas-python-sdk.git`)

Then import the package:
```python
import vipas
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import vipas
```

### Tests

Execute `pytest` to run the tests.

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python

from vipas import model
from pprint import pprint
from vipas.exceptions import UnauthorizedException

def main():
    try:
        vps_model_client = model.ModelClient()
        model_id = "mdl-test"
        try:
            api_response = vps_model_client.predict(model_id=model_id, input_data="Test input")
            pprint(api_response)
        except UnauthorizedException as e:
            print("Exception when calling model->predict: %s\n" % e)
        except Exception as e:
            print("Exception when calling model->predict: %s\n" % e)
    except Exception as e:
        print("Exception when calling model->predicrt: %s\n" % e)

main()

```

## Author
VIPAS.AI




