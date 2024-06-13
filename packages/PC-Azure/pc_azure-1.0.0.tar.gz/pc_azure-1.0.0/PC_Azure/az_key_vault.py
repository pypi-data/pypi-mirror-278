"""
Created on:     April 2023
Created by:     Marcos E. Mercado
Description:    This module contains the class that retrieves the appropriate tokens from Azure Key Vault. This is a leaner version than class SlackAPIcaller in the Slack Administration solution.
Reference:      https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python?tabs=azure-cli
"""

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


class Azure_Key_Vault:
    """Class that helps retrieve values from the Key Vault.
    """

    def __init__(self, kv_name: str):   # constructor receives the name of the Key Vault as a parameter

        KVUri = f"https://{kv_name}.vault.azure.net"
        credential = DefaultAzureCredential(exclude_interactive_browser_credential=False, additionally_allowed_tenants = "*")   # for logging, add parameter "logging_enable = True"
        self.client = SecretClient(vault_url=KVUri, credential=credential)

    def get_secret(self, secret_name: str) -> str:
        secret = self.client.get_secret(secret_name)
        
        return secret.value