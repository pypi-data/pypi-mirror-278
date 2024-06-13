"""The module that defines the ``SessionRestrictions`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""

import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from ..utils import to_dict


@dataclass
class SessionRestrictions:
    """Restrictions of the session."""

    #: If set and not none this is the course for which the token is valid.
    for_course: Maybe["t.Optional[int]"] = Nothing

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.OptionalArgument(
                "for_course",
                rqa.Nullable(rqa.SimpleValue.int),
                doc=(
                    "If set and not none this is the course for which the"
                    " token is valid."
                ),
            ),
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        getattr(super(), "__post_init__", lambda: None)()
        self.for_course = maybe_from_nullable(self.for_course)

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {}
        if self.for_course.is_just:
            res["for_course"] = to_dict(self.for_course.value)
        return res

    @classmethod
    def from_dict(
        cls: t.Type["SessionRestrictions"], d: t.Dict[str, t.Any]
    ) -> "SessionRestrictions":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            for_course=parsed.for_course,
        )
        res.raw_data = d
        return res
