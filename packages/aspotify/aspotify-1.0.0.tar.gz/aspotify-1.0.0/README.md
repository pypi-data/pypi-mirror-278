# aspotify: Asynchronous Spotify API Client

aspotify is a package created for asynchronous connection to the Spotify API.

## Installation

```
Dependencies:

- Python 3.7, 3.8, 3.9, 3.11, 3.12
- Redis
- Spotify Account

Installation:

$ pip install aspotify
```

## SHA-256 Hash

To get the SHA-256 Hash from your Spotify account:

1. **Open Your Browser:**
    - Launch your preferred web browser (e.g., Chrome, Firefox).

2. **Open Developer Tools:**
    - Press **`Ctrl+Shift+I`** to open the Developer Tools.

3. **Navigate to Spotify:**
    - In the address bar, go to https://open.spotify.com.

4. **Filter Network Requests:**
    - Within the Developer Tools, go to the "Network" tab.
    - In the "Filter" box, type **`query`** to filter the network requests.

5. **Locate the SHA-256 Hash:**
    - Look through the filtered network requests for URLs containing **`query.`**
    - Click on one of URLs and examine the details in the "Headers" tab.
    - Find and note the SHA-256 Hash from the URL data.

## Environment Variables

```
export SPOTIFY_USERNAME="<your_spotify_username>"
export SPOTIFY_PASSWORD="<your_spotify_password>"
export SPOTIFY_SCOPES="user-read-email,playlist-read-private"

export SPOTIFY_REDIS_HOST="localhost"
export SPOTIFY_REDIS_PORT=6379
export SPOTIFY_REDIS_DB=0

export SPOTIFY_SHA256HASH="<your_sha256_hash>"
```

For more details on Spotify API scopes, visit [Spotify's official documentation on scopes](https://developer.spotify.com/documentation/web-api/concepts/scopes).

## Usage

```python
import asyncio

from aspotify import API


async def main():
    api = API()

    data = await api.request("https://api.spotify.com/v1/tracks/0tgVpDi06FyKpA1z0VMD4v")
    assert data["uri"] == "spotify:track:0tgVpDi06FyKpA1z0VMD4v"

asyncio.run(main())
```
