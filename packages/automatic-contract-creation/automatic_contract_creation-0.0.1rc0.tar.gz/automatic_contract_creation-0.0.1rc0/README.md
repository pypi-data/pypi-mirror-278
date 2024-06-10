# Automatic Contract Creation

**Automatic Contract Creation** is a Python library that is designed to auto-generate various types of contracts based on the soda syntax.

### Features

In the current version, connection to DB such as Clickhouse and Trino is configured.
By connecting to the database, you can generate and/or upload a statistical report, as well as generate a soda contract.

## Get Started

### Requirements
Python 3.7 or later
To use the modified contract, you must use the soda version 3.3.5.

### Install and run

You can install the library using pip:
```
pip install automatic-contract-creation
```
Import the necessary objects. To use all the functionality, you can contact SODAGenerator
```
from automatic_contract_creation import SODAGenerator
```

Create a connection object by passing the connector type and credits in dictionary format.
Use the methods to auto-generate a contract or generate a statistical report.

## Documentation
* [user guide](./docs/user_guide.md)
* [technical documentation](./docs/TECHNICAL_DOCUMENTATION.md)

