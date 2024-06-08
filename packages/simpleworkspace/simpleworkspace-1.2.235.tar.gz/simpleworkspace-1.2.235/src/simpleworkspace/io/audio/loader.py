from simpleworkspace.__lazyimporter__ import __LazyImporter__, TYPE_CHECKING
if(TYPE_CHECKING):
    from . import play as _play

play: '_play' = __LazyImporter__(__package__, '.play')
