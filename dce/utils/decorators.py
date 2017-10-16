import functools

from semantic_version import Version

from .. import errors


def check_resource(*resource_names):
    def decorator(f):
        @functools.wraps(f)
        def wrapped(self, *args, **kwargs):
            ags = list(args)
            for resource_name in resource_names:
                resource_id = ags.pop()
                if isinstance(resource_id, dict):
                    resource_id = resource_id.get('Id', resource_id.get('ID'))
                if not resource_id:
                    raise errors.NullResource(
                        'Resource {0} was not provided, find {1}'.format(
                            resource_name, resource_id
                        )
                    )
            return f(self, *args, **kwargs)
        return wrapped
    return decorator


def minimum_version(version):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            if Version(self.dce_version) < Version(version):
                raise errors.InvalidVersion(
                    '{0} is not available for DCE version < {1}'.format(
                        f.__name__, version
                    )
                )
            return f(self, *args, **kwargs)

        return wrapper

    return decorator


def maximum_version(version):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            if Version(self.dce_version) > Version(version):
                raise errors.InvalidVersion(
                    '{0} is not available for DCE version > {1}'.format(
                        f.__name__, version
                    )
                )
            return f(self, *args, **kwargs)

        return wrapper

    return decorator
