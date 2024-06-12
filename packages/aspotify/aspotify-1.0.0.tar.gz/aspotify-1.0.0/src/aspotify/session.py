import os
import pathlib
import typing as t
import uuid

from librespot.core import Session as _Session
from redis import Redis


class Session:
    """
    Manages a session for a Spotify user.

    Parameters
    ----------
    username : str
        The Spotify username.

    password : str
        The Spotify password.

    Properties
    ----------
    session
        Creates and returns a Spotify session.
    """
    os.makedirs(pathlib.Path.home() / ".spotify/log/", exist_ok=True)

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @property
    def session(self) -> _Session:
        """
        Creates and returns a Spotify session.

        This handles credential storage by creating a credential file at the
        user's home directory and removing it after the session is created.

        Returns
        -------
        Session
            Returns the session for the user.

        Raises
        ------
        Exception
            If the session creation fails, an exception will be raised.
        """
        creds = pathlib.Path.home() / f".spotify/{uuid.uuid4()}.json"
        build = _Session.Configuration.Builder().set_stored_credential_file(creds.as_posix()).build()
        session = _Session.Builder(build).user_pass(self.username, self.password).create()
        if os.path.exists(creds):
            os.remove(creds)
        return session


class Token(Session):
    """
    Manages tokens for a Spotify user.

    Parameters
    ----------
    username : str
        The Spotify username.

    password : str
        The Spotify password.

    scopes : Iterable[str]
        The scopes for which the token is valid.

    Methods
    -------
    generate
        Generates a new access token and stores it to Redis.

    read
        Reads the access token from Redis.

    headers
        Returns the headers required for authorization.

    References
    ----------
    SCOPES
        https://developer.spotify.com/documentation/web-api/concepts/scopes
    """
    redis = Redis(
        host=os.environ["SPOTIFY_REDIS_HOST"],
        port=os.environ["SPOTIFY_REDIS_PORT"],
        db=os.environ["SPOTIFY_REDIS_DB"],
    )

    def __init__(self, username: str, password: str, scopes: t.Iterable[str]):
        self.username = username
        self.password = password
        self.scopes = scopes

    def generate(self) -> str:
        """
        Generates a new access token and stores it to Redis.

        Returns
        -------
        str
            The generated access token.
        """
        access_token = self.session.tokens().get_token(*self.scopes).access_token
        self.redis.set("token", access_token)
        return access_token

    @staticmethod
    def read() -> str:
        """
        Reads the access token from Redis.

        Returns
        -------
        str
            The stored access token.

        Raises
        ------
        FileNotFoundError
            If the access token file does not exist.
        """
        access_token = __class__.redis.get("token")
        if access_token:
            return access_token.decode()
        else:
            raise FileNotFoundError("Access token does not exist.")

    @staticmethod
    def headers() -> t.Dict[str, str]:
        """
        Returns the headers required for authorization.

        Returns
        -------
        Dict[str, str]
            The headers for authorization.
        """
        return {
            "Authorization": f"Bearer {__class__.read()}",
            "Accept-Language": "en",
            "Accept": "application/json"
        }
