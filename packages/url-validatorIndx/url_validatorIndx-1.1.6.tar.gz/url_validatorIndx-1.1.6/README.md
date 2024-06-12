# Foobar

Foobar is a Python library for dealing with word pluralization.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install url_validatorIndx.

```bash
pip install url_validatorIndx
```

## Usage

```python
from url_validatorIndx import isValidUrl, isValidString

# returns an dict with isValid and message key value pairs
urlExpr= isValidUrl("https://www.google.com")

isvalid = isValidString("Hello, World123")

#prints {"isValid": True, "message": "Valid expression"}
print(urlExpr)

```

## Valid Values

examples of valid url :

```
"https://google.com", "https://www.google.com", "https://www.google.com/search?q=123"
```

#

examples of valid string it should be less than 255 chars

```
"hello, world123", "Hello", "12345" , "hello ,W123"
```

#

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
