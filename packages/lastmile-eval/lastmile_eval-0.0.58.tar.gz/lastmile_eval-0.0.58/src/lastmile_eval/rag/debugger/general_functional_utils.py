"""TODO: move this out into lastmile_utils"""

from typing import Callable, Iterable, ParamSpec, Tuple, TypeVar

import lastmile_utils.lib.core.api as core_utils
from result import Err, Ok, Result

# This will need untangling.
from lastmile_eval.rag.debugger.common import core as core

# TODO (@jll) move this out to core_utils

T_Inv = TypeVar("T_Inv")

U_Inv = TypeVar("U_Inv")
U_Cov = TypeVar("U_Cov", covariant=True)

T_ParamSpec = ParamSpec("T_ParamSpec")


def res_reduce_list_separate(
    lst: Iterable[core.Res[T_Inv]],
) -> Tuple[list[T_Inv], list[Exception]]:
    oks: list[T_Inv] = []
    errs: list[Exception] = []
    for item in lst:
        match item:
            case Ok(x):
                oks.append(x)
            case Err(e):
                errs.append(e)

    return oks, errs


def res_reduce_list_all_ok(
    lst: Iterable[core.Res[T_Inv]],
) -> core.Res[list[T_Inv]]:
    oks, errs = res_reduce_list_separate(lst)
    if errs:
        return Err(ValueError("\n".join(map(str, errs))))
    else:
        return Ok(oks)


def exn_to_err(
    fn: core_utils.T_UnsafeFn[T_ParamSpec, core_utils.T_Return],
) -> core_utils.T_SafeFn[T_ParamSpec, core_utils.T_Return, Exception]:
    """TODO: figure out why exception_to_err_with_traceback
    doesn't fully infer types."""

    def decorated(
        *args: T_ParamSpec.args, **kwargs: T_ParamSpec.kwargs
    ) -> Result[core_utils.T_Return, Exception]:
        try:
            return Ok(fn(*args, **kwargs))
        except Exception as e:
            return Err(e)

    return decorated


def do_list(
    fn: Callable[[T_Inv], core.Res[U_Inv]], lst: list[T_Inv]
) -> core.Res[list[U_Inv]]:
    return res_reduce_list_all_ok(list(map(fn, lst)))


def compose(
    f: Callable[T_ParamSpec, T_Inv], g: Callable[[T_Inv], U_Inv]
) -> Callable[T_ParamSpec, U_Inv]:
    """
    As close as we're going to get to elegant point-free?
    :(
    """

    def composed(
        *args: T_ParamSpec.args, **kwargs: T_ParamSpec.kwargs
    ) -> U_Inv:
        return g(f(*args, **kwargs))

    return composed


def unzip2(lst: list[tuple[T_Inv, U_Inv]]) -> tuple[list[T_Inv], list[U_Inv]]:
    return list(map(lambda x: x[0], lst)), list(map(lambda x: x[1], lst))
