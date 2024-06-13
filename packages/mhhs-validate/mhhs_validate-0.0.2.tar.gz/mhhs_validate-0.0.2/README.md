# mhhs-validate

Validate data against the [MHHS](https://www.mhhsprogramme.co.uk/) specifications.

# Installation

```shell
pip install mhhs-validate
```

# Usage

```shell
MHHS_VALIDATE_VERSION=1.7.3 mhhs-validate example.json
```

Other environment variables and their defaults:

```shell
# The schemas get cached locally
MHHS_VALIDATE_CACHE_DIR=~/.mhhs-validate
# Names of the domains to fetch
MHHS_VALIDATE_DOMAINS=DataCatalogue,DataTypes,RealCommonBlocks,Interfaces-EventCodes,ECS-Reports,ECS-CommonBlocks
```

# Example output

```
Failed validating 'enum' in

    schema['properties']['CommonBlock']['properties']['M0']['properties']['GSPGroupID']:

    {'$anchor': 'DI-037-GSP-Group-ID',
     'description': 'Identifies the distinct grid supply point group '
                    '(physical region of the country) where the metering '
                    'point is located.',
     'enum': ['_A',
              '_B',
              '_C',
              '_D',
              '_E',
              '_F',
              '_G',
              '_H',
              '_J',
              '_K',
              '_L',
              '_M',
              '_N',
              '_P'],
     'example': '_K',
     'maxLength': 2,
     'minLength': 2,
     'type': 'string'}

On instance['CommonBlock']['M0']['GSPGroupID']:
    '_X'
```
