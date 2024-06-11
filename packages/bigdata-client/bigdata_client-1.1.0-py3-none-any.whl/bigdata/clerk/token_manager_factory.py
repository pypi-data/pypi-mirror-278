from bigdata.clerk.authenticators.dev_instance import ClerkAuthenticatorDevInstance
from bigdata.clerk.authenticators.production_instance import (
    ClerkAuthenticatorProductionInstance,
)
from bigdata.clerk.constants import ClerkInstanceType
from bigdata.clerk.exceptions import ClerkUnexpectedSignInParametersError
from bigdata.clerk.models import SignInStrategyType
from bigdata.clerk.sign_in_strategies.password import PasswordStrategy
from bigdata.clerk.token_manager import ClerkTokenManager

TEMPLATE_NAME = "bigdata_sdk"


def token_manager_factory(
    clerk_instance: ClerkInstanceType,
    sign_in_strategy: SignInStrategyType,
    clerk_frontend_url: str,
    **kwargs,
) -> ClerkTokenManager:
    """
    Factory to be used by Clerk consumers

    Args:
        clerk_instance: Instance type DEV/PROD
        sign_in_strategy: PASSWORD
        clerk_frontend_url: URL of the Clerk frontend
        **kwargs: extra params required by the factory

    Returns:
        ClerkTokenManager is used for obtaining JWTs

    Raises:
        ClerkUnexpectedSignInParameters
    """

    strategy = _get_strategy(sign_in_strategy, kwargs)
    if clerk_instance == ClerkInstanceType.DEV:
        return ClerkAuthenticatorDevInstance.create_token_manager(
            clerk_frontend_url, strategy, clerk_jwt_template_name=TEMPLATE_NAME
        )
    elif clerk_instance == ClerkInstanceType.PROD:
        return ClerkAuthenticatorProductionInstance.create_token_manager(
            clerk_frontend_url, strategy, clerk_jwt_template_name=TEMPLATE_NAME
        )
    else:
        raise ValueError(f"Unknown clerk instance: {clerk_instance}")


def _get_strategy(sign_in_strategy: SignInStrategyType, kwargs: dict):
    if sign_in_strategy == SignInStrategyType.PASSWORD:
        return _get_password_strategy(kwargs)

    raise ValueError(f"Unknown sign in strategy: {sign_in_strategy}")


def _get_password_strategy(kwargs: dict):
    if set(kwargs) != {"password", "email"}:
        raise ClerkUnexpectedSignInParametersError

    return PasswordStrategy(email=kwargs["email"], password=kwargs["password"])
