# Dixa API Wrapper

[![Python](https://img.shields.io/pypi/pyversions/dixa-api.svg)](https://badge.fury.io/py/recharge-api)
[![PyPI](https://badge.fury.io/py/dixa-api.svg)](https://badge.fury.io/py/recharge-api)
[![PyPI](https://github.com/ChemicalLuck/dixa-api/actions/workflows/python-publish.yml/badge.svg)](https://github.com/ChemicalLuck/recharge-api/actions/workflows/python-publish.yml)
![PyPI - Downloads](https://img.shields.io/pypi/dm/dixa-api)

## Installation

```bash
pip install dixa-api
```

## Usage

```python
from dixa import DixaAPI

client = dixa(access_token='XXXXX')

agents = client.Agents.list()

for agent in agents:
    print(agent['id'])
```

For more details on the content of the reponses, visit the [official dixa API docs](https://docs.dixa.io/openapi/dixa-api/v1/overview/).

## Resources Available
### v1
- Agents
- Analytics
- Anonymization
- Contact Endpoints
- Conversations
- Custom Attributes
- End Users
- Internal Notes
- Messages
- Queues
- Ratings
- Search
- Tags
- Teams
- Webhooks

## Resources

- [dixa API v1](https://docs.dixa.io/openapi/dixa-api/v1/overview/)

## License

[MIT](LICENSE)
