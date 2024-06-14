from functools import partial

from .utils import get_broker_url, get_backend_url
from ..core import Processor
from ..utils import lazy_property


class BeamDispatcher(Processor):

    def __init__(self, *args, name=None, broker=None, backend=None,
                 broker_username=None, broker_password=None, broker_port=None, broker_scheme=None, broker_host=None,
                 backend_username=None, backend_password=None, backend_port=None, backend_scheme=None,
                 backend_host=None, serve='local', log_level='INFO', **kwargs):

        super().__init__(*args, name=name, **kwargs)

        self.broker_url = get_broker_url(broker=broker, broker_username=broker_username,
                                         broker_password=broker_password, broker_port=broker_port,
                                         broker_scheme=broker_scheme, broker_host=broker_host)

        self.backend_url = self.backend_url = get_backend_url(backend=backend, backend_username=backend_username,
                                           backend_password=backend_password, backend_port=backend_port,
                                           backend_scheme=backend_scheme, backend_host=backend_host)

        self.log_level = log_level
        self.serve = serve

    @lazy_property
    def broker(self):
        from celery import Celery
        app = Celery(self.name, broker=self.broker_url.url, backend=self.backend_url.url)
        app.conf.update(
            worker_log_level=self.log_level,
            broker_connection_retry_on_startup=True
        )
        return app

    def __call__(self, *args, **kwargs):
        return self.dispatch('function', *args, **kwargs)

    def poll(self, task_id, *args, **kwargs):
        res = self.broker.AsyncResult(task_id)
        if res.state == 'SUCCESS':
            return res.result
        return None

    def metadata(self, task_id, *args, **kwargs):
        res = self.broker.AsyncResult(task_id)
        d = {'task_id': task_id, 'state': res.state, 'result': res.result,
             'traceback': res.traceback if res.state == 'FAILURE' else None, 'status': res.status,
             'children': res.children, 'retries': res.retries, "parent_id": res.parent.id if res.parent else None,
             'exception': str(res.result) if res.state == 'FAILURE' else None,
             'date_done': res.date_done if hasattr(res, 'date_done') else None,
             'runtime': res.runtime if hasattr(res, 'runtime') else None}

        return d

    def dispatch(self, attribute, *args, **kwargs):
        res = self.broker.send_task(attribute, args=args, kwargs=kwargs)
        if self.serve == 'local':
            return res
        return res.task_id

    def __getattr__(self, item):
        if item.startswith('_') or item in ['serve'] or not hasattr(self, 'serve'):
            return super().__getattribute__(item)
        return partial(self.dispatch, item)

