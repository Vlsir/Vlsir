"""
# VlsirTools Pytest Utilities 

Primarily adds and parses the command-line options for enabling and disabling `vlsirtools.spice` simulators. 
To use these utilities, add the following to your `conftest.py`:

```python
from vlsirtools.pytest import (
    pytest_configure,
    pytest_addoption,
    pytest_collection_modifyitems,
)
```

See VlsirTools' own `conftest.py` for an example.  
With these functions included, by those names, in `conftest.py`, invocations of `pytest` can use: 

* The `--simulator_test_mode` command-line option 
  * Values are `required`, `if_available`, or `disabled`
* Markers for each supported simulator
  * `spectre`, `xyce`, and `ngspice` are currently supported
* Command-line options for each supported simulator, to override `simulator_test_mode`


Examples: 

```
pytest --simulator_test_mode disabled       # Disables all simulation tests
pytest --simulator_test_mode required       # Requires all simulation tests
pytest --simulator_test_mode if_available   # Runs tests on available simulators

pytest --simulator_test_mode if_available --ngspice required  # Requires ngspice, tests all others available 
pytest --simulator_test_mode required --xyce disabled         # Disables xyce, requires all others
pytest --simulator_test_mode disabled --spectre required      # Requires spectre, disables all others
```

"""


from vlsirtools.pytest import (
    pytest_configure,
    pytest_addoption,
    pytest_collection_modifyitems,
)
