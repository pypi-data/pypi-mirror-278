from datetime import datetime
from urllib.parse import urljoin
from ..common.context import get_client_id, get_client_secret, get_domain
from ..common.util import get_http_session

AppTokenRefreshTime = 20 * 60 * 1000


class AppCredential:
    def __init__(self):
        self.expire_time = 0
        self.tenant_info = None
        self.id = get_client_id()
        self.secret = get_client_secret()

    def get_token(self):
        remain_time = self.expire_time - datetime.now().timestamp()
        if remain_time > AppTokenRefreshTime and self.token:
            return self.token
        self.fetch_token()
        return self.token

    def get_tenant_info(self):
        if not self or not self.id or not self.secret:
            self.id = get_client_id()
            self.secret = get_client_secret()
        if self.tenant_info:
            return self.tenant_info
        self.fetch_token()
        return self.tenant_info

    def fetch_token(self):
        domain = get_domain()
        if not domain:
            raise Exception("get domain failed")

        s = get_http_session()
        res = s.post(urljoin(domain, "/auth/v1/appToken"), json={
            "clientId": self.id,
            "clientSecret": self.secret,
            "withTenantInfo": True,
        })
        data = res.json()

        if not data['data']:
            raise Exception("get token failed")

        data = data['data']
        self.token = data["accessToken"]
        self.namespace = data["namespace"]
        self.expire_time = data["expireTime"]
        self.tenant_info = data["tenantInfo"]
