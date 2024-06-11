from cleo.helpers import argument, option

from iaptoolkit import IAPToolkit_OAuth2
from iaptoolkit import IAPToolkit_OIDC
from iaptoolkit.tokens.structs import TokenRefreshStruct

from typehints_cleo2 import TypeHintedCommand


class CommonArguments:

    iap_client_id = argument(
        "iap_client_id",
        description="IAP Client ID string (OAuth2.0 Client ID in GCP Credentials)(JWT Audience).",
        optional=False,
    )

    client_secret = argument(
        "client_secret",
        description="IAP Client Secret (OAuth2.0 Client Secret in GCP Credentials).",
        optional=False,
    )

    client_id = argument(
        "client_id",
        description="OAuth2.0 Client ID for User/Application",
        optional=False,
    )

    url = argument(
        name="url",
        description="Destination URL",
        optional=False,
    )

    http_method = argument(
        name="http_method",
        description="HTTP Method [GET/POST/PUT/PATCH/HEAD] (not case-sensitive)",
        default="GET",
        optional=True,
    )


class CommonOptions:
    use_auth_header = option(
        long_name="use-auth-header",
        short_name=None,
        description=(
            "If true, use the `Authorization` header instead of `Proxy-Authorization` when making "
            "authenticated requests through IAP."
        ),
    )
    bypass_cache = option(
        long_name="bypass-cache",
        short_name="nc",
        description="Bypass cache when retrieving tokens",
    )
    dump_content = option(
        long_name="dump-content",
        description="If true, dump the response.content to stdout",
    )


class IAPToolkitCLICommand(TypeHintedCommand):
    pass


def get_token_struct_oidc(iap_client_id: str) -> TokenRefreshStruct:
    iaptk = IAPToolkit_OIDC(google_iap_client_id=iap_client_id)
    return iaptk.get_token()


def get_token_string_oidc(iap_client_id: str) -> str:
    struct = get_token_struct_oidc(iap_client_id=iap_client_id)
    return struct.id_token


def get_token_struct_oauth2(
    iap_client_id: str, client_id: str, client_secret: str, refresh_token: str
) -> TokenRefreshStruct:
    iaptk = IAPToolkit_OAuth2(
        google_iap_client_id=iap_client_id,
        google_client_id=client_id,
        google_client_secret=client_secret,
    )
    return iaptk.get_token(refresh_token=refresh_token)


def get_token_string_oauth2(
    iap_client_id: str, client_id: str, client_secret: str, refresh_token: str
) -> str:
    struct = get_token_struct_oauth2(
        iap_client_id=iap_client_id,
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token,
    )
    return struct.id_token
