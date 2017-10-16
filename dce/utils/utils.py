# encoding=utf-8
import time
import functools
from inspect import getargspec
from collections import OrderedDict
from inflection import camelize
from itsdangerous import JSONWebSignatureSerializer
from itsdangerous import TimedJSONWebSignatureSerializer

true_bool_str = {'yes', 'true', 't', '1'}
false_bool_str = {'no', 'false', 'f', '0'}


def str2bool(v, default):
    if v is None:
        return default
    if v.lower() in true_bool_str:
        return True
    if v.lower() in false_bool_str:
        return False
    return default


def is_valid_bool_str(v):
    return v is not None and \
           (v.lower() in true_bool_str or v.lower() in false_bool_str)


def check_bool_str(**kwargs):
    for k, v in kwargs.iteritems():
        if not is_valid_bool_str(v):
            raise ValueError(
                "'{0}' got a unexpected value, "
                "expected 'yes', '1', 'true', 't', 'no', '0', 'false', 'f'".format(
                    k
                )
            )


def camelize_dict(values, with_order=False):
    if with_order:
        return OrderedDict((camelize(k), v) for k, v in values.items() if v)
    return {camelize(k): v for k, v in values.items() if v}


def memoize(fn):
    cache = fn.cache = {}

    @functools.wraps(fn)
    def _memoize(*args, **kwargs):
        kwargs.update(dict(zip(getargspec(fn).args, args)))
        key = tuple(kwargs.get(k, None) for k in getargspec(fn).args if k != 'self')
        if key not in cache:
            cache[key] = fn(**kwargs)
        return cache[key]

    return _memoize


def memoize_with_expire(expire):
    def _memoize(fn):
        cache = fn.cache = {}
        cache['__last_cached_time'] = time.time()

        @functools.wraps(fn)
        def __memoize(*args, **kwargs):
            kwargs.update(dict(zip(getargspec(fn).args, args)))
            key = tuple(kwargs.get(k, None) for k in getargspec(fn).args if k != 'self')
            if key not in cache or time.time() > cache['__last_cached_time'] + expire:
                cache[key] = fn(**kwargs)
                cache['__last_cached_time'] = time.time()
            return cache[key]

        return __memoize

    return _memoize


def memoize_in_object(fn):
    @functools.wraps(fn)
    def _memoize(self, *args, **kwargs):
        kwargs.update(dict(zip(getargspec(fn).args, args)))
        key = '__cache__%s__' % fn.__name__ + ','.join(str(kwargs.get(k, None)) for k in getargspec(fn).args)
        if not hasattr(self, key):
            setattr(self, key, fn(self, **kwargs))
        return getattr(self, key)

    return _memoize


def wrap_checking_resource(cls):
    from .decorators import check_resource

    attrs = cls.__dict__
    for method in attrs:
        if not method.startswith('__'):
            args = getargspec(attrs[method]).args
            slice_ = len(args) - len((getargspec(attrs[method]).defaults or ()))
            if slice_ > 1:
                cls.__dict__[method] = check_resource(*args[1:slice_])(attrs[method])


def gen_token_serializer(expired_in=3600, is_eternal=False):
    from ..consts import SECRET_KEY

    if is_eternal:
        return JSONWebSignatureSerializer(SECRET_KEY)
    return TimedJSONWebSignatureSerializer(SECRET_KEY, expires_in=expired_in)


def gen_plugins_storage_token(plugin_name):
    if plugin_name is None:
        return plugin_name

    token = gen_token_serializer(is_eternal=True)
    token.dumps({'plugin_name': plugin_name})

    return token


