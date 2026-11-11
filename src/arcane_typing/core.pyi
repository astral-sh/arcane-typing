from ty_extensions import Bottom as Bottom
from ty_extensions import Intersection as Intersection
from ty_extensions import Not as Not
from ty_extensions import Top as Top
from ty_extensions import static_assert as static_assert
from ty_extensions._internal import CallableTypeOf
from ty_extensions._internal import TypeOf as TypeOf

class _Signature[**P, R]:
    @staticmethod
    def call(*args: P.args, **kwargs: P.kwargs) -> R: ...

# It would be great to write this as `Callabe[P, R] & FunctionType`, but `FunctionType`
# has a permissively typed `__call__` method which would allow arbitrary calls and intersect
# the return type with `Any`, so we use this hack:
type FunctionLikeCallable[**P, R] = CallableTypeOf[_Signature[P, R].call]
