# pyconfman2

pyconfman2 is designed to handle schema configurations by loading properties from a dictionary or a YAML configuration file. It provides methods for adding, getting, and removing properties from the schema.

## Installation
```bash
python -m pip install pyconfman2
```

## Usage

### Basic
In it's most basic form, a Schema can be created which will load a local "config.yaml" or "config.yml" file present.

```python
>>> from pyconfman2 import Schema
>>> config = Schema.ConfigSchema()
>>> print(config)
{}
```

### Provide a default config
```python
>>> from pyconfman2 import Schema
>>> config=Schema.ConfigSchema({"foo": "bar"})
>>> print(config)
{'foo': 'bar'}
```

### Specify the default config file to load
```python
>>> from pyconfman2 import Schema
>>> config=Schema.ConfigSchema(default_config="default_config.yaml")
>>> print(config)
{'foo': 'bar', 'zoo': {'jar': ['car', 'far']}}
```


### Specify the config file to load
```python
>>> from pyconfman2 import Schema
>>> config=Schema.ConfigSchema(default_config="default_config.yaml", filepath="another_config.yaml")
>>> print(config)
{'foo': 'overwritten_by_another_config', 'zoo': {'jar': ['car', 'far']}}
```


## Schema Loading breakdown
1. Load the hard-coded defaults
2. Load (and override) using the "default config" file if present
3. Load (and override) using the config file if present
