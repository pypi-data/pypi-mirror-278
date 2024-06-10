import asyncio
import functools

from fastdup.vldbaccess.dataset import DatasetDB
from fastdup.vldbaccess.models.exploration_context import ExplorationContext


def can_access_dataset(exc: Exception):
    def _decor(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            context: ExplorationContext = kwargs['context']
            ds = DatasetDB.get_by_id(context.dataset_id, context.user_id)
            if ds is None:
                raise exc
            res = func(*args, **kwargs)
            return res

        @functools.wraps(func)
        async def awrapper(*args, **kwargs):
            context: ExplorationContext = kwargs['context']
            ds = DatasetDB.get_by_id(context.dataset_id, context.user_id)
            if ds is None:
                raise exc
            res = await func(*args, **kwargs)
            return res

        if asyncio.iscoroutinefunction(func):
            return awrapper
        else:
            return wrapper

    return _decor
