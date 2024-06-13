"""The module that defines the ``UserLoginResponse`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""

import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa

from .. import parsers
from ..utils import to_dict
from .session_restrictions import SessionRestrictions
from .user import User


@dataclass
class UserLoginResponse:
    """When logging in this object will be given."""

    #: The user that was logged in.
    user: "User"
    #: A session token that can be used to do authenticated requests.
    access_token: "str"
    #: The restrictions of this access token.
    restrictions: "SessionRestrictions"

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.RequiredArgument(
                "user",
                parsers.ParserFor.make(User),
                doc="The user that was logged in.",
            ),
            rqa.RequiredArgument(
                "access_token",
                rqa.SimpleValue.str,
                doc=(
                    "A session token that can be used to do authenticated"
                    " requests."
                ),
            ),
            rqa.RequiredArgument(
                "restrictions",
                parsers.ParserFor.make(SessionRestrictions),
                doc="The restrictions of this access token.",
            ),
        ).use_readable_describe(True)
    )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {
            "user": to_dict(self.user),
            "access_token": to_dict(self.access_token),
            "restrictions": to_dict(self.restrictions),
        }
        return res

    @classmethod
    def from_dict(
        cls: t.Type["UserLoginResponse"], d: t.Dict[str, t.Any]
    ) -> "UserLoginResponse":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            user=parsed.user,
            access_token=parsed.access_token,
            restrictions=parsed.restrictions,
        )
        res.raw_data = d
        return res
