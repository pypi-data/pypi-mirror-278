from simpleworkspace.__lazyimporter__ import __LazyImporter__, TYPE_CHECKING
if(TYPE_CHECKING):
    from . import locking as _locking
    from . import parallel as _parallel

locking: '_locking' = __LazyImporter__(__package__, '.locking')
parallel: '_parallel' = __LazyImporter__(__package__, '.parallel')