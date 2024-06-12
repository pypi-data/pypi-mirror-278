import aiohttp
import os
import typing as t
import urllib.parse

from functools import wraps

from .session import Token
from .utils import setup_logger


class ResourceUrl:
    """
    A class for constructing URLs for Spotify API operations.

    Methods
    -------
    construct
        Constructs a URL for a Spotify API operation with the given parameters.
    """

    def construct(self, operation: str, variables: t.Dict[str, t.Any] = {}) -> str:
        """
        Constructs a URL for a Spotify API operation with the given parameters.

        Parameters
        ----------
        operation : str
            The name of the operation.

        variables : Dict[str, Any]
            The variables for the query.

        Returns
        -------
        str
            The constructed URL for the Spotify API operation.

        Raises
        ------
        KeyError
            If the environment variable 'SPOTIFY_SHA256HASH' is not set.
        """
        base_url = "https://api-partner.spotify.com/pathfinder/v1/query"

        extensions = {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": os.environ["SPOTIFY_SHA256HASH"]
            }
        }

        # Encoding the variables and extensions
        variables_encoded = urllib.parse.quote(str(variables).replace("'", '"'))
        extensions_encoded = urllib.parse.quote(str(extensions).replace("'", '"'))

        return f"{base_url}?operationName={operation}&variables={variables_encoded}&extensions={extensions_encoded}"


class API(ResourceUrl):
    """
    A class for handling API requests with retry logic for a Spotify user.

    Methods
    -------
    retry
        A decorator that retries the wrapped function up to three times in case of failure.

    request
        Sends an asynchronous GET request to the specified URL and returns the response as a dictionary.

    References
    ----------
    SCOPES
        https://developer.spotify.com/documentation/web-api/concepts/scopes
    """
    def retry(func):
        """
        A decorator that retries the wrapped function up to three times in case of failure.

        Parameters
        ----------
        func : callable
            The function to be wrapped with retry logic.

        Returns
        -------
        callable
            The wrapped function with retry logic.

        Raises
        ------
        KeyError
            If environment variables 'SPOTIFY_USERNAME', 'SPOTIFY_PASSWORD', 'SPOTIFY_SCOPES' are not set.
        """
        @wraps(func)
        async def wrapper(self, *args, **kwargs) -> t.Optional[t.Any]:
            username = os.environ["SPOTIFY_USERNAME"]
            password = os.environ["SPOTIFY_PASSWORD"]
            scopes = os.environ["SPOTIFY_SCOPES"]
            max_retries = 3
            while max_retries:
                try:
                    response = await func(self, *args, **kwargs)
                    if response:
                        if "error" in response:
                            raise ValueError("The access token expired.")
                        return response
                except Exception as e:
                    logger = setup_logger("Query:API", "query.log")
                    logger.error(str(e))
                    token = Token(username, password, scopes.split(","))
                    token.generate()  # Token not found nor might be expired
                max_retries -= 1
            return None
        return wrapper

    @retry
    async def request(self, url: str) -> t.Optional[t.Dict[str, t.Any]]:
        """
        Sends an asynchronous GET request to the specified URL and returns the response as a dictionary.

        Parameters
        ----------
        url : str
            The URL to send the GET request to.

        Returns
        -------
        Optional[Dict[str, Any]]
            The JSON response from the GET request as a dictionary, or None if the request fails.
        """
        async with aiohttp.ClientSession(headers=Token.headers()) as session:
            async with session.get(url=url) as resp:
                return await resp.json()
