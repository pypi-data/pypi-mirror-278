# phone-format

phone-format is a Python library for dealing with formatting phone numbers.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/)
or [poetry](https://python-poetry.org/) to install rwandaphoneformat.

```bash
pip install phone_format
```

or

```bash
poetry add phone_format
```

## Usage

```python
from phone_format.format_phone import RwandaPhoneFormat

# returns '250780000000'
RwandaPhoneFormat.format_phone('0780000000')

# returns '250780000000'
RwandaPhoneFormat.format_phone('+250780000000')

# returns '250780000000'
RwandaPhoneFormat.format_phone('780000000')

# returns '250780000000'
RwandaPhoneFormat.format_phone('250780000000')

# returns '1', here it returns the input, 
# if the input is not formatted as a Rwandan phone
RwandaPhoneFormat.format_phone('1')
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)