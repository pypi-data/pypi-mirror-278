# python-eip712

Parse eip712 clear sign descriptors.

## Install

```shell
pip install eip712-clearsign
```

## Run tests

```shell
pyenv install 3.10.6
pyenv local 3.10.6
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pip install .
pytest -s --cov=./eip712
```

## Generate an EIP712 parser

You can generate a base parser file using the following python code:

```python3
import json
from eip712 import (
    EIP712ContractDescriptor,
    EIP712DAppDescriptor,
)

eip712_dapp = EIP712DAppDescriptor(
    blockchainName="ethereum", chainId=1, name="MyDApp", contracts=[]
)
contract = EIP712ContractDescriptor(
    address="0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
    contractName="MyCoolContract_V1",
    messages=[],
)
schemas = [
    {
        "EIP712Domain": [
            {"name": "chainId", "type": "uint256"},
            {"name": "name", "type": "string"},
            {"name": "verifyingContract", "type": "address"},
            {"name": "version", "type": "string"},
        ],
        "Mail": [
            {"name": "contents", "type": "string"},
            {"name": "from", "type": "Person"},
            {"name": "to", "type": "Person"},
        ],
        "Person": [
            {"name": "name", "type": "string"},
            {"name": "wallets", "type": "Wallet[]"},
        ],
        "Wallet": [
            {"name": "name", "type": "string"},
            {"name": "addr", "type": "address"},
        ],
    },
    ...
]

for schema in schemas:
    eip712_dapp.add_message(target_contract=contract, schema=schema)

with open("eip712.json", "w+") as f:
    json.dump(eip712_dapp.dict(by_alias=True), f, indent=4, sort_keys=True, ensure_ascii=False)
```

This will create one mapper field per element in your schemas, with auto generated names. You should then:

- Remove the fields you don't want to display on the Nano
- Rename the fields that you want to keep, with names that are as meaningful as possible
