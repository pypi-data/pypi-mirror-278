from dataclasses import dataclass

import jwt
from fastapi import Request, status
from pydantic_settings import BaseSettings

from skys_llc_auth.exceptions import ParamsError, TokenError
from skys_llc_auth.utils import Singleton, TokenType, UserRole


class DefaultTokenParams(Singleton):
    def __init__(
        self,
        key: str | None = None,
        algorithms: str | None = None,
        *,
        config: BaseSettings | None = None,
    ) -> None:
        if key is not None and algorithms is not None:
            self.key = key
            self.algorithms = algorithms
        elif issubclass(config.__class__, BaseSettings):
            if hasattr(config, "public_key"):
                self.key = config.public_key  # pyright: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]
            if hasattr(config, "ALGORITHMS"):
                self.algorithms = config.ALGORITHMS  # pyright: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]
        else:
            raise ParamsError("key and algorithms, or config class must be provided")


@dataclass(slots=True, frozen=True)
class TokenValidation:
    token: str
    role: UserRole | list[UserRole] | None
    deftokenpar: DefaultTokenParams

    def __post_init__(self):
        if self.deftokenpar.key is None:
            raise ParamsError("key is not provided")
        if self.deftokenpar.algorithms is None:
            raise ParamsError("algorithm is not provided")

    def _decode(self) -> dict[str, str]:
        try:
            token = jwt.decode(
                self.token,
                key=self.deftokenpar.key,
                algorithms=[self.deftokenpar.algorithms],
            )
            return dict(token)
        except jwt.PyJWTError as exp_err:
            raise TokenError(
                detail=str(exp_err.args),
                status_code=status.HTTP_401_UNAUTHORIZED,
            ) from exp_err

    def _has_access(self) -> bool:
        if isinstance(self.role, list):
            return self._decode().get("role", None) in [i.value for i in self.role]
        elif isinstance(self.role, UserRole):
            return self._decode().get("role", None) == self.role.value
        else:
            raise ParamsError("expected type role is list[UserRole] or UserRole")

    def _not_access(self) -> bool:
        if isinstance(self.role, list):
            return self._decode().get("role", None) not in [i.value for i in self.role]
        elif isinstance(self.role, UserRole):
            return self._decode().get("role", None) != self.role.value
        else:
            raise ParamsError("expected type role is list[UserRole] or UserRole")

    def check_permission(self, *, exclude: bool) -> None:
        if exclude:
            access_token = self._not_access()
        else:
            access_token = self._has_access()
        if not access_token:
            raise TokenError(
                detail="Permission denied",
                status_code=status.HTTP_403_FORBIDDEN,
            )

    def user_id(self) -> str:
        user_id = self._decode().get("id", None)
        if user_id:
            return user_id
        raise TokenError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token must have key id",
        )

    def _token_type_jwt(self) -> str | None:
        return self._decode().get("token_type_jwt", None)

    def is_access(self) -> bool:
        return self._token_type_jwt() == TokenType.access.value

    def is_refresh(self) -> bool:
        return self._token_type_jwt() == TokenType.refresh.value

    def user_role(self) -> str | None:
        return self._decode().get("role", None)


async def get_token_from_request(request: Request) -> str:  # pragma: no cover
    if not request.headers.get("Authorization", None):
        raise TokenError(
            detail="Request must have a Authorization token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    token = request.headers["Authorization"].split(" ")
    if token[0] != "Bearer":
        raise TokenError(
            detail="Предоставлен не Bearer токен",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    if len(token) != 2:
        raise TokenError(
            detail="Invalid basic header. Credentials string should not contain spaces.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return token[1]
