# XGRCpy

XGRCPy is a Python package that allows users to interact with an XGRC software service to retrieve encrypted data and decrypt it for further processing. It includes methods for key generation, decryption, and interacting with remote APIs.

## Installation

To install XGRCpy, ensure you have Python installed (version 3.6 or higher), then use pip to install the package:

```bash
pip install XGRCpy

## Usage

After installation, you can use the XGRCpy package to interact with the XGRC software service. Below is an example of how to use the XGRCViewTable function to fetch and decrypt a table from the service.

### Example Code
```python
from XGRCpy import XGRCViewTable

# User credentials for accessing the service
username = "your_username"
password = "your_password"
table = "desired_table"
api_key = "your_api_key"

# Fetching and decrypting the table
response = XGRCViewTable(username, password, table, api_key)


# Fetching and decrypting the table
response = XGRCSPView(username, password, SPName, api_key)

# Display the decrypted content
print(response)

