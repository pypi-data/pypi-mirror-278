"""
Decorators for the STAC module.
"""


def with_rioxarray(func):
    def wrapper(self, *args, **kwargs):
        try:
            import rioxarray as rxr

            return func(self, *args, **kwargs)
        except ImportError:
            raise ImportError(
                "The rioxarray and dask diagnostics packages are required. Please install them with 'pip install rioxarray dask[diagnostics]' and try again."
            )

    return wrapper
