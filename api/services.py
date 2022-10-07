from django.db.models import Manager, QuerySet


def only_objects_decorator(func: callable):
    def only_objects_wrapper(
        objects: Manager, only: tuple = (), *args, **kwargs
    ) -> QuerySet:
        return func(objects, *args, **kwargs).only(*only)

    return only_objects_wrapper


def order_by_objects_decorator(func: callable):
    def order_by_objects_wrapper(
        objects: Manager, order_by: tuple = (), *args, **kwargs
    ) -> QuerySet:
        return func(objects, *args, **kwargs).order_by(*order_by)

    return order_by_objects_wrapper


@order_by_objects_decorator
@only_objects_decorator
def all_objects(objects: Manager) -> QuerySet:
    """Return all objects in the database"""
    return objects.all()


@order_by_objects_decorator
@only_objects_decorator
def filter_objects(objects: Manager, **kwargs) -> QuerySet:
    """Return filtered objects in the database"""
    return objects.filter(**kwargs)
