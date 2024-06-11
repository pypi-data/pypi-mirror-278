from cleo.application import Application

# from iaptoolkit_cli.commands.curl import CurlCommand_OIDC
# from iaptoolkit_cli.commands.curl import CurlHeaderString_OIDC
from iaptoolkit_cli.commands.oidc import TokenCommand_OIDC
from iaptoolkit_cli.commands.oidc import RequestCommand_OIDC
# from iaptoolkit_cli.commands.wget import WgetCommand_OIDC

# from iaptoolkit_cli.commands.curl import CurlCommand_OAuth2
# from iaptoolkit_cli.commands.curl import CurlHeaderString_OAuth2
# from iaptoolkit_cli.commands.oauth2 import InitCommand_OAuth2
# from iaptoolkit_cli.commands.oauth2 import TokenCommand_OAuth2
# from iaptoolkit_cli.commands.oauth2 import RequestCommand_OAuth2
# from iaptoolkit_cli.commands.wget import WgetCommand_OAuth2


application = Application()

application.add(TokenCommand_OIDC())
application.add(RequestCommand_OIDC())

# application.add(InitCommand_OAuth2())
# application.add(TokenCommand_OAuth2())
# application.add(RequestCommand_OAuth2())

# application.add(CurlCommand())
# application.add(CurlHeaderString_OIDC())
# application.add(WgetCommand())


if __name__ == "__main__":
    application.run()
