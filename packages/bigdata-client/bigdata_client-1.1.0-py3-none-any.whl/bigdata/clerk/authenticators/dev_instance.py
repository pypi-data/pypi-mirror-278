from http import HTTPStatus

import requests

from bigdata.clerk.authenticators.base_instance import ClerkInstanceBase
from bigdata.clerk.exceptions import (
    ClerkAuthError,
    ClerkAuthUnsupportedError,
    ClerkInvalidCredentialsError,
    raise_errors_as_clerk_errors,
)
from bigdata.clerk.models import RefreshedTokenManagerParams
from bigdata.clerk.sign_in_strategies.base import SignInStrategy
from bigdata.clerk.sign_in_strategies.password import PasswordStrategy
from bigdata.clerk.token_manager import ClerkTokenManager


class ClerkAuthenticatorDevInstance(ClerkInstanceBase):
    @classmethod
    @raise_errors_as_clerk_errors
    def create_token_manager(
        cls,
        clerk_frontend_api_url: str,
        login_strategy: SignInStrategy,
        clerk_jwt_template_name: str = None,
    ) -> ClerkTokenManager:
        """
        Performs the authentication flow against Clerk with the chosen strategy by creating
        a session then choosing the first organization the user is a member of (activation).
        The returned TokenManager stores the sign in information to use it for refreshing.
        Args:
            clerk_frontend_api_url:
            login_strategy:
            clerk_jwt_template_name: Name of the jwt template created in Clerk

        Returns: TokenManager
        """
        if not isinstance(login_strategy, PasswordStrategy):
            raise ClerkAuthUnsupportedError("Unsupported SignInStrategy")
        dev_browser_token = ClerkAuthenticatorDevInstance._get_dev_browser_token(
            clerk_frontend_api_url
        )
        session = requests.Session()
        session.params = {"__dev_session": dev_browser_token}
        clerk_session = ClerkAuthenticatorDevInstance._sign_in(
            session, clerk_frontend_api_url, login_strategy
        )
        ClerkAuthenticatorDevInstance._activate_session(
            session, clerk_session, clerk_frontend_api_url
        )

        clerk_instance = ClerkAuthenticatorDevInstance(
            clerk_frontend_api_url=clerk_frontend_api_url,
            login_strategy=login_strategy,
            session=session,
            clerk_session=clerk_session,
        )

        return ClerkTokenManager(
            clerk_authenticator_instance=clerk_instance,
            clerk_jwt_template_name=clerk_jwt_template_name,
        )

    @staticmethod
    def get_new_token_manager_params(
        clerk_frontend_api_url: str, login_strategy: SignInStrategy
    ):
        dev_browser_token = ClerkAuthenticatorDevInstance._get_dev_browser_token(
            clerk_frontend_api_url
        )
        session = requests.Session()
        session.params = {"__dev_session": dev_browser_token}
        clerk_session = ClerkAuthenticatorDevInstance._sign_in(
            session, clerk_frontend_api_url, login_strategy
        )
        ClerkAuthenticatorDevInstance._activate_session(
            session, clerk_session, clerk_frontend_api_url
        )
        return RefreshedTokenManagerParams(session=session, clerk_session=clerk_session)

    @staticmethod
    def _get_dev_browser_token(clerk_frontend_api_url: str) -> str:
        """
        This is used to authenticate Development Instances with the DevBrowser scheme.
        It must be set before making any request to a dev instance, even for endpoints that are public.
        """
        response = requests.post(url=f"{clerk_frontend_api_url}dev_browser")
        response.raise_for_status()

        return response.json()["token"]

    @staticmethod
    def _sign_in(
        session: requests.Session, clerk_frontend_api_url: str, strategy: SignInStrategy
    ) -> str:
        url = f"{clerk_frontend_api_url}client/sign_ins"
        response = session.post(
            url=url, data=strategy.get_payload(), headers=strategy.get_headers()
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
                raise ClerkInvalidCredentialsError
            raise ClerkAuthError from e

        return response.json()["response"]["created_session_id"]
