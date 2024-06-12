import asyncio

from aspotify import API


def test_api():
    async def main():
        api = API()

        data = await api.request("https://api.spotify.com/v1/tracks/0tgVpDi06FyKpA1z0VMD4v")
        assert data["uri"] == "spotify:track:0tgVpDi06FyKpA1z0VMD4v"

    asyncio.run(main())
