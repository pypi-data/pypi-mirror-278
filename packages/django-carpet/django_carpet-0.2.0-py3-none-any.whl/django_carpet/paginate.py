# Python
from typing import Any, TypeVar, Callable

# Django
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.manager import BaseManager


_Z = TypeVar("_Z")


def paginate(entries: BaseManager[Any], page_number: int, limit: int, sort: str | None, serializer: Callable, *args, **kwargs) -> dict:
    
    paginator = Paginator(entries, limit)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return {
        "data": serializer(page.object_list, *args, **kwargs),
        "limit": limit,
        "page": page_number,
        "startIndex": page.start_index(),
        "hasNext": page.has_next(),
        "sort": sort,
        "total": paginator.count,
        "totalPage": paginator.num_pages,
    }


def paginate_without_serialization(entries: BaseManager[_Z], page_number: int, limit: int, sort: str | None) -> tuple[BaseManager[_Z], dict]: # type: ignore
    paginator = Paginator(entries, limit)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page.object_list, { # type: ignore
        "limit": limit,
        "page": page_number,
        "startIndex": page.start_index(),
        "hasNext": page.has_next(),
        "sort": sort,
        "total": paginator.count,
        "totalPage": paginator.num_pages,
    }