import sys

import requests

# from cleo.helpers import argument
# from cleo.helpers import option

from iaptoolkit import IAPToolkit_OIDC

from kvcommon.output import pp

from iaptoolkit_cli.common import IAPToolkitCLICommand
from iaptoolkit_cli.common import CommonArguments
from iaptoolkit_cli.common import CommonOptions
from iaptoolkit_cli.common import get_token_string_oidc


def make_request_with_oidc(
    iap_client_id: str,
    url: str,
    headers: dict | None = None,
    http_method: str = "get",
    use_auth_header: bool = False,
) -> requests.Response:
    headers = dict() if headers is None else headers
    iaptk = IAPToolkit_OIDC(google_iap_client_id=iap_client_id)
    iaptk.get_token_and_add_to_headers(request_headers=headers, use_auth_header=use_auth_header)
    return requests.request(method=http_method, url=url, headers=headers)


class TokenCommand_OIDC(IAPToolkitCLICommand):
    """
    TODO: -o arg for output destination instead of stdout (e.g.; File)
    """

    name = "token_oidc"
    description = (
        "Retrieves an IAP auth token using OIDC (for Service Accounts) and "
        "Application Default Credentials (ADC), and dumps it to stdout"
    )
    arguments = [
        CommonArguments.iap_client_id,
    ]

    options = [
        CommonOptions.bypass_cache,
    ]

    def handle(self):
        iap_client_id: str = self.argument_str(CommonArguments.iap_client_id.name)

        token: str = get_token_string_oidc(iap_client_id=iap_client_id)
        sys.stdout.write(token)
        sys.stdout.flush()
        return


class RequestCommand_OIDC(IAPToolkitCLICommand):
    name = "request_oidc"
    description = (
        "Makes a HTTP Request to the specified IAP-secured url and dumps the response "
        "using an OIDC token (e.g., for ServiceAccounts)."
    )

    arguments = [
        CommonArguments.iap_client_id,
        CommonArguments.url,
        CommonArguments.http_method,
    ]
    options = [
        CommonOptions.use_auth_header,
        CommonOptions.dump_content,
    ]

    def handle(self):
        iap_client_id = self.argument_str(CommonArguments.iap_client_id.name)
        url = self.argument_str(CommonArguments.url.name)
        http_method = self.argument_str_optional(CommonArguments.http_method.name) or "get"
        http_method = http_method.lower()

        use_auth_header = self.option_bool(CommonOptions.use_auth_header.name)
        dump_content = self.option_bool(CommonOptions.dump_content.name)

        response = make_request_with_oidc(
            iap_client_id=iap_client_id,
            url=url,
            headers=dict(),
            http_method=http_method,
            use_auth_header=use_auth_header,
        )
        self.line(f"<Response [{response.status_code}]>")
        if dump_content:
            pp(response.content)
