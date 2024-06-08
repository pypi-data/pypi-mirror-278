from simpleworkspace.__lazyimporter__ import __LazyImporter__, TYPE_CHECKING
if(TYPE_CHECKING):
    from . import console as _console
    from . import commandbuilder as _commandbuilder
    from . import parser as _parser

console: '_console' = __LazyImporter__(__package__, '.console')
commandbuilder: '_commandbuilder' = __LazyImporter__(__package__, '.commandbuilder')
parser: '_parser' = __LazyImporter__(__package__, '.parser')
