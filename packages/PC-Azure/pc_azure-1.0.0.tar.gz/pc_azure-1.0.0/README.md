# PC_Azure
ABK Productivity &amp; Collaboration Python code to interact with Microsoft Azure

## Requirements
In order to use the Python classes contained in this package you'll need:
* An Azure account - https://portal.azure.com/
* Install the Azure command line interface (Azure CLI)
* Authenticate in Azure using Azure CLI

See section below for more information about Azure CLI.

### Azure CLI resources
* <a href=https://learn.microsoft.com/en-us/cli/azure/>Azure CLI</a>
* <a href=https://learn.microsoft.com/en-us/cli/azure/install-azure-cli>Install Azure CLI</a>
* <a href=https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli>Authenticate through Azure CLI
  
## Troubleshooting
If you have already installed Azure CLI, but you keep getting prompted to sign in using a web browser, you may need to re-log in. To fix this, type `az login` on a terminal.

## Classes
### Azure_Key_Vault
#### Methods
  * constructor : Receives the name of the Azure Key Vault
  * get_secret : Receives a secret name and returns the corresponding secret value stored in the Azure Key Vault that is defined in the constructor
  
  #### References
  https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python
