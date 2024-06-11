# Django Carpet 0.2.0

This package contains the base function and classes for a Django project

The project has the following sections:
- env
- exceptions
- mixins
- paginate
- response
- validators
- xml_element

```text
Note: This package requires python 3.11 and higher
```

## Installation
```text
pip install django-carpet
```


## ENV
The `env` checks the execution mode and deployment status of the application and contains the following functions:
- `exec_mode` -> Gets the execution mode of the application. The options are `normal`, `test`, and `e2e` (accessed through `EnvChoices`)
- `is_debug` -> Checks the `DEBUG` constant in `settings.py`
- `is_production` -> Checks if the application is in the production mode. For the application to be in production mode, the `DEBUG` has to be false and `exec_mode` should be normal
- `is_testing` -> Checks if the application is in unit test or e2e test

In order for these functions to behave as intended, you need 3 settings to differentiate between the three execution modes. The execution mode is determined using `EXEC_MODE` constant. If no such constant is provided, the default value is `normal`. The name of the files is up to you:
- `settings.py`: The settings for the production. The `DEBUG` must be set to false.
- `settings_dev.py`: The settings for the development mode. This setting sets the DEBUG to false and detects if we are `test` command. It should have the following:
```python
DEBUG = True
if 'test' in sys.argv:
    EXEC_MODE = "test"
```
- `settings_e2e.py`: The settings for the E2E tests, allowing you to differentiate between the E2E tests and normal dev server. It should contain the following:
```python
DEBUG = True
EXEC_MODE = "e2e"
```
