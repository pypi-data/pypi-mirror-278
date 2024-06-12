from ..credential import AppCredential


def get_env_info():
    credential = AppCredential()
    tenant_info = credential.get_tenant_info()

    if not tenant_info:
        raise Exception("get tenant info failed")

    return {
        "appId": credential.namespace,
        "tenant": {
            "id": tenant_info['id'],
            "name": tenant_info['tenantName'],
            "type": tenant_info['tenantType'],
        },
    }
