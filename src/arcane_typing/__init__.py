"""Experimental and advanced Python typing patterns for ty users."""

from .core import Bottom as Bottom
from .core import FunctionLikeCallable as FunctionLikeCallable
from .core import Intersection as Intersection
from .core import Not as Not
from .core import Top as Top
from .core import TypeOf as TypeOf
from .core import static_assert as static_assert
from .narrowing import hasattr_of_type as hasattr_of_type
from .narrowing import is_sequence_of as is_sequence_of
from .typed_dict import Keys as Keys
from .typed_dict import Values as Values
