from sqlalchemy.sql.functions import GenericFunction

from dvcx.sql.types import Int64
from dvcx.sql.utils import compiler_not_implemented


class rand(GenericFunction):  # noqa: N801
    type = Int64()
    inherit_cache = True


compiler_not_implemented(rand)
