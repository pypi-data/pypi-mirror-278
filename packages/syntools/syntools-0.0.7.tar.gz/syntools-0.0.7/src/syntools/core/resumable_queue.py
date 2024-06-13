import hashlib
import os
import json
import asyncio
from datetime import datetime
from . import Utils, Logging
from .exceptions import SynToolsError


class WorkItemResult:
    def __init__(self, result=None, error=None, total_processed=0):
        self.result = result
        self.error = error
        self.total_processed = total_processed

    @property
    def can_retry(self):
        return self.error is not None and isinstance(self.error, SynToolsError) and self.error.can_retry is True

    @property
    def retry_modifier(self):
        if isinstance(self.error, SynToolsError):
            return self.error.retry_modifier
        else:
            return None

    @property
    def retry_max(self):
        if isinstance(self.error, SynToolsError):
            return self.error.retry_max
        else:
            return None


class ResumableQueue:
    NEW = 'New'
    STARTED = 'Started'
    FINISHED = 'Finished'

    def __init__(self, task_name, config_filename=None, verbose=False):
        self.task_name = task_name
        self.config_filename = config_filename
        self._queue = asyncio.PriorityQueue()
        self._verbose = verbose
        self._last_save_timestamp = None
        self._auto_save_counter = 0
        self.status = self.NEW
        self.queued = []

    @classmethod
    def load(cls, task_name, uniq_suffix=None, config_dir=None, reset=False, verbose=False):
        if config_dir is None:
            config_dir = Utils.app_resumable_queue_dir()
        Utils.ensure_dirs(config_dir)
        if uniq_suffix is None:
            uniq_suffix = task_name

        suffix = hashlib.md5(uniq_suffix.encode()).hexdigest()
        config_filename = os.path.join(Utils.expand_path(config_dir), 'syntools-{0}-{1}.json'.format(task_name, suffix))
        config = cls(task_name=task_name, config_filename=config_filename, verbose=verbose)
        if os.path.isfile(config_filename):
            if reset:
                config.delete()
            else:
                Logging.info('Loading progress from file: {0}'.format(config_filename))
                with open(config_filename) as f:
                    config.from_json(json.load(f))
                    Logging.info('Loaded progress from: {0}, with {1} queued items.'.format(
                        config_filename, config.queued_size), console=verbose)

        if config.status == cls.FINISHED:
            config.reset()

        return config

    @property
    def qsize(self):
        return self._queue.qsize()

    @property
    def queued_size(self):
        return len(self.queued)

    @property
    def has_queued(self):
        return self.queued_size > 0

    @property
    def is_new(self):
        return self.status == self.NEW

    @property
    def is_started(self):
        return self.status == self.STARTED

    @property
    def is_finished(self):
        return self.status == self.FINISHED

    @property
    def can_resume(self):
        return self.queued_size > 0

    def task_done(self):
        self._queue.task_done()

    async def join(self):
        await self._queue.join()

    def save(self):
        with open(self.config_filename, 'w') as f:
            json.dump(self.to_json(), f, indent=2)
        self._last_save_timestamp = datetime.now()
        return self

    def delete(self):
        if os.path.isfile(self.config_filename):
            os.remove(self.config_filename)

    def to_json(self):
        return {
            'status': self.status,
            'queued': self.queued
        }

    def from_json(self, json_data):
        self.status = json_data.get('status')
        self.queued = json_data.get('queued') or []

    def set_started(self):
        self.status = self.STARTED
        self.save()

    def set_finished(self, delete_if_completed=True):
        self.status = self.FINISHED
        self.save()
        if delete_if_completed and not self.has_queued:
            self.delete()

    def reset(self):
        self.status = self.NEW
        self.queued = []
        self.save()

    def _auto_save(self):
        if self._last_save_timestamp is None:
            self._last_save_timestamp = datetime.now()

        self._auto_save_counter += 1
        last_save = round((datetime.now() - self._last_save_timestamp).total_seconds(), 2)
        if last_save >= 60 or (self._auto_save_counter >= 500 and last_save >= 10):
            self.save()
            self._auto_save_counter = 0

    def to_queue_item(self, func, *args, **kwargs):
        func_name = func if isinstance(func, str) else func.__name__
        arg_list = [func_name]
        for arg in args:
            if isinstance(arg, str):
                arg_list.append(arg)
            else:
                if isinstance(arg, dict):
                    str_dict = json.dumps(arg)
                    arg_list.append('json#{0}'.format(str_dict))
                elif hasattr(arg, 'id'):
                    arg_list.append(arg.id)
                else:
                    arg_list.append(str(arg))

        for key, arg in kwargs.items():
            if isinstance(arg, dict):
                str_dict = json.dumps(arg)
                arg_list.append('{0}::json#{1}'.format(key, str_dict))
            elif isinstance(arg, str):
                arg_value = arg
            else:
                if hasattr(arg, 'id'):
                    arg_value = arg.id
                else:
                    arg_value = str(arg)
            arg_list.append('{0}::{1}'.format(key, arg_value))

        return '$'.join(arg_list)

    def from_queue_item(self, item, func_target=None):
        """
        Returns:
            func, args, kwargs
        """
        parts = item.split('$')
        func = parts.pop(0)
        if func_target is not None:
            func = getattr(func_target, func)
        args = []
        kwargs = {}

        for part in parts:
            if '::' in part:
                k, v = part.split('::')
                if v.startswith('json#'):
                    d = part.replace('json#', '')
                    v = json.loads(d)
                kwargs[k] = v
            else:
                if part.startswith('json#'):
                    d = part.replace('json#', '')
                    args.append(json.loads(d))
                else:
                    args.append(part)

        return func, args, kwargs

    async def add_queued(self, priority, func, *args, item=None, **kwargs):
        item = self.to_queue_item(func, *args, **kwargs) if item is None else item
        if item not in self.queued:
            self.queued.append(item)
            self._auto_save()
        await self._queue.put((priority, item))
        return item

    async def get_queued(self, func_target=None):
        priority, item = await self._queue.get()
        if isinstance(item, str):
            func, args, kwargs = self.from_queue_item(item, func_target=func_target)
        else:
            func, args, kwargs = item
            if isinstance(func, str) and func_target is not None:
                func = getattr(func_target, func)

        return func, args, kwargs

    def remove_queued(self, func, *args, **kwargs):
        item = self.to_queue_item(func, *args, **kwargs)
        if item in self.queued:
            self.queued.remove(item)
            self._auto_save()
            return item
        return None
