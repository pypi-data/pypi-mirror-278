"""Client interfaces for the Robust Intelligence API"""
from typing import Any, Optional, TYPE_CHECKING

from ri.bases.client_base import (
    DEFAULT_CHANNEL_TIMEOUT,
    FIREWALL_AUTH_TOKEN_NAME,
    FIREWALL_API_KEY_NAME,
    RIME_API_KEY_NAME,
    BaseClient,
)

if TYPE_CHECKING:
    from ri.apiclient.api import GenerativeModelTestingApi
    from ri.fwclient.api import FirewallApi
    from ri.fwclient.api import FirewallInstanceManagerApi


class RIClient(BaseClient):
    """Robust Intelligence client to interact with the RI API

    :param domain: str
        The base URL of the API server.
    :param api_key: str
        The API key used for authentication. Each entry in the dict specifies an API key.
        The dict key is the name of the security scheme in the OAS specification.
        The dict value is the API key secret.
    :param channel_timeout: float
        The timeout for network connections in seconds. Default is 300 seconds.
    :param username: Optional[str]
        Username for HTTP basic authentication.
    :param password: Optional[str]
        Password for HTTP basic authentication.
    :param access_token: Optional[str]
        Access token for bearer authentication.
    :param ssl_ca_cert: Optional[str]
        Path to a file of concatenated CA certificates in PEM format.
    :param proxy: Optional[str]
        URL of the proxy server to use for requests.
    :param verify_ssl: bool
        Whether to verify SSL certificates. Default is True.
    :param cert_file: Optional[str]
        Path to a client certificate file (PEM).
    :param key_file: Optional[str]
        Path to a client key file (PEM).
    :param api_key_prefix: Optional[Dict[str, str]]
        Dict to store API prefix (e.g., Bearer). The dict key is the name of the security scheme in the OAS specification.
        The dict value is an API key prefix when generating the auth data.
    :param server_index: Optional[int]
        Index to servers configuration for selecting the base URL.
    :param server_variables: Optional[Dict[str, str]]
        Variables to replace in the templated server URL.
    :param server_operation_index: Optional[Dict[str, int]]
        Mapping from operation ID to an index to server configuration.
    :param server_operation_variables: Optional[Dict[str, Dict[str, str]]]
        Mapping from operation ID to variables for templated server URLs.
    """

    def __init__(
        self,
        domain: str,
        api_key: str,
        channel_timeout: float = DEFAULT_CHANNEL_TIMEOUT,
        api_key_prefix: Optional[dict[Any, Any]] = None,
        username=None,
        password=None,
        access_token=None,
        ssl_ca_cert=None,
        verify_ssl=True,
        cert_file=None,
        key_file=None,
        proxy=None,
        server_index=None,
        server_variables=None,
        server_operation_index=None,
        server_operation_variables=None,
    ):
        super().__init__(
            domain=domain,
            api_key=api_key,
            api_key_prefix=api_key_prefix,
            channel_timeout=channel_timeout,
            username=username,
            password=password,
            access_token=access_token,
            ssl_ca_cert=ssl_ca_cert,
            verify_ssl=verify_ssl,
            cert_file=cert_file,
            key_file=key_file,
            proxy=proxy,
            server_index=server_index,
            server_variables=server_variables,
            server_operation_index=server_operation_index,
            server_operation_variables=server_operation_variables,
            api_key_header_name=RIME_API_KEY_NAME,
        )

        self._generative_testing: Optional["GenerativeModelTestingApi"] = None

    @property
    def generative_testing(self) -> "GenerativeModelTestingApi":
        """Access the generative testing API.

        :return: GenerativeModelTestingApi: the generative Testing api
        """
        if not self._generative_testing:
            from ri.apiclient.api import GenerativeModelTestingApi

            self._generative_testing = GenerativeModelTestingApi(self._api_client)

        return self._generative_testing


class FirewallClient(BaseClient):
    """Robust Intelligence firewall client to interact with the Firewall API

    :param domain: str
        The base URL of the API server.
    :param api_key: str
        The API key used for authentication. Each entry in the dict specifies an API key.
        The dict key is the name of the security scheme in the OAS specification.
        The dict value is the API key secret.
    :param api_key_header_name: str
        The header name for the API key.  Either "X-Firewall-API-Key" or "X-Firewall-Auth-Token".
    :param api_key_header_name: str
        The header name for the API key.
    :param channel_timeout: float
        The timeout for network connections in seconds. Default is 300 seconds.
    :param username: Optional[str]
        Username for HTTP basic authentication.
    :param password: Optional[str]
        Password for HTTP basic authentication.
    :param access_token: Optional[str]
        Access token for bearer authentication.
    :param ssl_ca_cert: Optional[str]
        Path to a file of concatenated CA certificates in PEM format.
    :param proxy: Optional[str]
        URL of the proxy server to use for requests.
    :param verify_ssl: bool
        Whether to verify SSL certificates. Default is True.
    :param cert_file: Optional[str]
        Path to a client certificate file (PEM).
    :param key_file: Optional[str]
        Path to a client key file (PEM).
    :param api_key_prefix: Optional[Dict[str, str]]
        Dict to store API prefix (e.g., Bearer). The dict key is the name of the security scheme in the OAS specification.
        The dict value is an API key prefix when generating the auth data.
    :param server_index: Optional[int]
        Index to servers configuration for selecting the base URL.
    :param server_variables: Optional[Dict[str, str]]
        Variables to replace in the templated server URL.
    :param server_operation_index: Optional[Dict[str, int]]
        Mapping from operation ID to an index to server configuration.
    :param server_operation_variables: Optional[Dict[str, Dict[str, str]]]
        Mapping from operation ID to variables for templated server URLs.
    """

    def __init__(
        self,
        domain: str,
        api_key: str,
        api_key_header_name: str,
        channel_timeout: float = DEFAULT_CHANNEL_TIMEOUT,
        api_key_prefix: Optional[dict[Any, Any]] = None,
        username=None,
        password=None,
        access_token=None,
        ssl_ca_cert=None,
        verify_ssl=True,
        cert_file=None,
        key_file=None,
        proxy=None,
        server_index=None,
        server_variables=None,
        server_operation_index=None,
        server_operation_variables=None,
    ):
        if api_key_header_name not in [FIREWALL_API_KEY_NAME, FIREWALL_AUTH_TOKEN_NAME]:
            raise ValueError(
                f"Invalid api_key_header_name: '{api_key_header_name}'. "
                f"Expected values are either '{FIREWALL_API_KEY_NAME}' or '{FIREWALL_AUTH_TOKEN_NAME}'."
            )

        super().__init__(
            domain=domain,
            api_key=api_key,
            api_key_header_name=api_key_header_name,
            api_key_prefix=api_key_prefix,
            channel_timeout=channel_timeout,
            username=username,
            password=password,
            access_token=access_token,
            ssl_ca_cert=ssl_ca_cert,
            verify_ssl=verify_ssl,
            cert_file=cert_file,
            key_file=key_file,
            proxy=proxy,
            server_index=server_index,
            server_variables=server_variables,
            server_operation_index=server_operation_index,
            server_operation_variables=server_operation_variables,
        )
        self._firewall: Optional["FirewallApi"] = None
        self._firewall_instance_manager: Optional["FirewallInstanceManagerApi"] = None

    @property
    def firewall(self) -> "FirewallApi":
        if not self._firewall:
            from ri.fwclient.api import FirewallApi

            self._firewall = FirewallApi(self._api_client)

        return self._firewall

    @property
    def firewall_instance_manager(self) -> "FirewallInstanceManagerApi":
        if not self._firewall_instance_manager:
            from ri.fwclient.api import FirewallInstanceManagerApi

            self._firewall_instance_manager = FirewallInstanceManagerApi(
                self._api_client
            )

        return self._firewall_instance_manager
