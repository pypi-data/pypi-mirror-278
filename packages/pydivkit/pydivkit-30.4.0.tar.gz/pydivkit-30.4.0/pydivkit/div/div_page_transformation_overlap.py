# Generated code. Do not modify.
# flake8: noqa: F401, F405, F811

from __future__ import annotations

import enum
import typing

from pydivkit.core import BaseDiv, Expr, Field

from . import div_animation_interpolator


# The pages are stacked when the pager is scrolled overlapping each other.
class DivPageTransformationOverlap(BaseDiv):

    def __init__(
        self, *,
        type: str = "overlap",
        interpolator: typing.Optional[typing.Union[Expr, div_animation_interpolator.DivAnimationInterpolator]] = None,
        next_page_alpha: typing.Optional[typing.Union[Expr, float]] = None,
        next_page_scale: typing.Optional[typing.Union[Expr, float]] = None,
        previous_page_alpha: typing.Optional[typing.Union[Expr, float]] = None,
        previous_page_scale: typing.Optional[typing.Union[Expr, float]] = None,
        reversed_stacking_order: typing.Optional[typing.Union[Expr, bool]] = None,
        **kwargs: typing.Any,
    ):
        super().__init__(
            type=type,
            interpolator=interpolator,
            next_page_alpha=next_page_alpha,
            next_page_scale=next_page_scale,
            previous_page_alpha=previous_page_alpha,
            previous_page_scale=previous_page_scale,
            reversed_stacking_order=reversed_stacking_order,
            **kwargs,
        )

    type: str = Field(default="overlap")
    interpolator: typing.Optional[typing.Union[Expr, div_animation_interpolator.DivAnimationInterpolator]] = Field(
        description=(
            "Tranformation speed nature. When the value is set to "
            "`spring` — animation ofdamping fluctuations cut to 0.7 with "
            "the `damping=1` parameter. Other optionscorrespond to the "
            "Bezier curve:`linear` — cubic-bezier(0, 0, 1, 1);`ease` "
            "—cubic-bezier(0.25, 0.1, 0.25, 1);`ease_in` — "
            "cubic-bezier(0.42, 0, 1,1);`ease_out` — cubic-bezier(0, 0, "
            "0.58, 1);`ease_in_out` — cubic-bezier(0.42, 0,0.58, 1)."
        ),
    )
    next_page_alpha: typing.Optional[typing.Union[Expr, float]] = Field(
        description=(
            "Minimum alpha of the next page during pager scrolling in "
            "bounds [0, 1]. The nextpage is always a page with a large "
            "sequential number in the list of `items`,regardless of the "
            "direction of scrolling."
        ),
    )
    next_page_scale: typing.Optional[typing.Union[Expr, float]] = Field(
        description=(
            "Scale of the next page during pager scrolling. The next "
            "page is always a pagewith a large sequential number in the "
            "list of `items`, regardless of thedirection of scrolling."
        ),
    )
    previous_page_alpha: typing.Optional[typing.Union[Expr, float]] = Field(
        description=(
            "Minimum alpha of the previous page during pager scrolling "
            "in bounds [0, 1]. Theprevious page is always a page with a "
            "lower sequential number in the list of`items`, regardless "
            "of the direction of scrolling."
        ),
    )
    previous_page_scale: typing.Optional[typing.Union[Expr, float]] = Field(
        description=(
            "Scale of the previous page during pager scrolling. The "
            "previous page is always apage with a lower sequential "
            "number in the list of `items`, regardless of thedirection "
            "of scrolling."
        ),
    )
    reversed_stacking_order: typing.Optional[typing.Union[Expr, bool]] = Field(
        description=(
            "If the value set to false, the next pages will be stacked "
            "on top the previousones. If the value set to true, then the "
            "opposite will occur. The next page isalways a page with a "
            "large sequential number in the list of `items`, "
            "regardlessof the direction of scrolling."
        ),
    )


DivPageTransformationOverlap.update_forward_refs()
