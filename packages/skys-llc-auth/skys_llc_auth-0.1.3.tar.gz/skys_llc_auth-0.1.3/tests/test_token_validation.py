import pytest
from pydantic_settings import BaseSettings
from src.skys_llc_auth.exceptions import ParamsError, TokenError
from src.skys_llc_auth.token_validation import DefaultTokenParams, TokenValidation
from src.skys_llc_auth.utils import UserRole

from tests.fixtures import SETTINGS

default_token_params = DefaultTokenParams(config=SETTINGS)


def test_init_with_key_and_algorithms():
    key = "secret_key"
    algorithms = "HS256"
    token_params = DefaultTokenParams(key=key, algorithms=algorithms)
    assert token_params.key == key
    assert token_params.algorithms == algorithms


def test_init_with_config():
    class settings(BaseSettings):
        SECRET_KEY: str = "secret_key"
        ALGORITHMS: str = "HS256"

    config = settings()
    token_params = DefaultTokenParams(config=config)
    assert token_params.key == config.SECRET_KEY
    assert token_params.algorithms == config.ALGORITHMS


def test_init_raises_error_when_missing_params():
    with pytest.raises(ParamsError) as e:
        DefaultTokenParams()
    assert e.value.args == ("key and algorithms, or config class must be provided",)


def test_token_validation_permission(gen_token_admin: str):
    token_valid = TokenValidation(gen_token_admin, UserRole.Administrator, default_token_params)
    assert token_valid.check_permission(exclude=False) is None


def test_token_validation_permission_list_role(gen_token_admin: str):
    token_valid = TokenValidation(
        gen_token_admin,
        [UserRole.Administrator, UserRole.Instructor],
        default_token_params,
    )
    assert token_valid.check_permission(exclude=False) is None


def test_token_validation_permission_list_role_exclude(gen_token_admin: str):
    token_valid = TokenValidation(
        gen_token_admin,
        [UserRole.Server, UserRole.Student],
        default_token_params,
    )
    assert token_valid.check_permission(exclude=True) is None


def test_token_validation_permission_role_exclude(gen_token_admin: str):
    token_valid = TokenValidation(
        gen_token_admin,
        UserRole.Server,
        default_token_params,
    )
    assert token_valid.check_permission(exclude=True) is None


def test_token_validation_not_permission(gen_token_admin: str):
    with pytest.raises(TokenError) as e:
        TokenValidation(
            gen_token_admin,
            UserRole.Server,
            default_token_params,
        ).check_permission(exclude=False)
    assert e.value.detail == "Permission denied"
    assert e.value.status_code == 403


def test_method_token_validation_user_id(gen_token_admin: str):
    user_id = TokenValidation(
        gen_token_admin,
        UserRole.Server,
        default_token_params,
    ).user_id()
    assert user_id == "60db7c59-e154-46df-bbd7-217cafcf6a2d"


def test_method_token_validation_without_user_id(gen_token_admin_without_id: str):
    with pytest.raises(TokenError) as e:
        TokenValidation(
            gen_token_admin_without_id,
            UserRole.Server,
            default_token_params,
        ).user_id()
    assert e.value.detail == "Token must have key id"
    assert e.value.status_code == 400


def test_token_validation_permission_none_role(gen_token_admin: str):
    with pytest.raises(ParamsError) as e:
        TokenValidation(
            gen_token_admin,
            role="",  # pyright: ignore[reportArgumentType] checking what happens if you pass a None value as role
            deftokenpar=default_token_params,
        ).check_permission(exclude=False)

    assert e.value.args == ("expected type role is list[UserRole] or UserRole",)


def test_token_validation_permission_none_role_exclude(gen_token_admin: str):
    with pytest.raises(ParamsError) as e:
        TokenValidation(
            gen_token_admin,
            role="",  # pyright: ignore[reportArgumentType] checking what happens if you pass a None value as role
            deftokenpar=default_token_params,
        ).check_permission(exclude=True)

    assert e.value.args == ("expected type role is list[UserRole] or UserRole",)


def test_token_validation_key(gen_token_admin_wrong_key: str):
    with pytest.raises(TokenError) as e:
        TokenValidation(gen_token_admin_wrong_key, UserRole.Administrator, default_token_params).check_permission(
            exclude=False
        )
    assert e.value.detail == "('Signature verification failed',)"
    assert e.value.status_code == 401


def test_token_valid_key_error(gen_token_admin: str):
    key = None
    algorithms = "HS256"

    with pytest.raises(ParamsError) as e:
        DefaultTokenParams(key, algorithms)
    assert e.value.args == ("key and algorithms, or config class must be provided",)


def test_token_validation_key_error(gen_token_admin_wrong_key: str):
    class settings:
        key: str | None = None
        algorithms: str | None = None

    config = settings()

    with pytest.raises(ParamsError) as e:
        TokenValidation(
            gen_token_admin_wrong_key,
            UserRole.Administrator,
            config,  # pyright: ignore[reportArgumentType] checking what happens if you pass a class not based on BaseSettings
        ).check_permission(exclude=False)
    assert e.value.args == ("key is not provided",)


def test_token_validation_algo_error(gen_token_admin_wrong_key: str):
    class settings:
        key: str = "asdasd"
        algorithms: str | None = None

    config = settings()

    with pytest.raises(ParamsError) as e:
        TokenValidation(
            gen_token_admin_wrong_key,
            UserRole.Administrator,
            config,  # pyright: ignore[reportArgumentType] # pyright: ignore[reportArgumentType] checking what happens if you pass a class not based on BaseSettings
        ).check_permission(exclude=False)
    assert e.value.args == ("algorithm is not provided",)


def test_method_token_validation_token_type_access(gen_token_admin: str):
    token_type = TokenValidation(
        gen_token_admin,
        UserRole.Server,
        default_token_params,
    ).is_access()
    assert token_type is True


def test_method_token_validation_token_type(gen_token_admin: str):
    token_type = TokenValidation(
        gen_token_admin,
        UserRole.Server,
        default_token_params,
    ).is_refresh()
    assert token_type is False


def test_method_token_validation_token_type_refresh(gen_token_admin_refresh: str):
    token_type = TokenValidation(
        gen_token_admin_refresh,
        UserRole.Server,
        default_token_params,
    ).is_access()
    assert token_type is False


def test_method_token_validation_token_type_refresh_(gen_token_admin_refresh: str):
    token_type = TokenValidation(
        gen_token_admin_refresh,
        UserRole.Server,
        default_token_params,
    ).is_refresh()
    assert token_type is True


def test_method_token_validation_user_role(gen_token_admin: str):
    user_role = TokenValidation(
        gen_token_admin,
        UserRole.Server,
        default_token_params,
    ).user_role()
    assert user_role == UserRole.Administrator.value
