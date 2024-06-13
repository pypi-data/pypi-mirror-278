# Aparat

A Python library to interact with the Aparat API.

## Installation

```bash
pip install AparatLib
```

## Login

```python
from aparat import Aparat

def main():
    aparat = Aparat()
    if aparat.login('your_username', 'your_password'):
        print("Login successful")
    else:
        print("Login failed.")

if __name__ == "__main__":
    main()
```

For more detailed information, please refer to the [documentation](https://aparatlib.readthedocs.io/en/latest/).
