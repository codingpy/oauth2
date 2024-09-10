from urllib.parse import urlencode


class Client:
    def __init__(self, session, auth_url, token_url, client_id, client_secret):
        self.session = session

        self.auth_url = auth_url
        self.token_url = token_url

        self.client_id = client_id
        self.client_secret = client_secret

    def get_url(self, scope="", **kwargs):
        if not isinstance(scope, str):
            scope = " ".join(scope)

        qs = urlencode(
            {
                "response_type": "code",
                "client_id": self.client_id,
                "scope": scope,
                **kwargs,
            }
        )
        return f"{self.auth_url}?{qs}"

    async def get_access_token(self, code, **kwargs):
        async with self.session.post(
            self.token_url,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                **kwargs,
            },
        ) as r:
            return await r.json()

    async def refresh_access_token(self, refresh_token, **kwargs):
        async with self.session.post(
            self.token_url,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                **kwargs,
            },
        ) as r:
            return await r.json()
