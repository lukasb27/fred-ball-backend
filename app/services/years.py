from ..data.entries import get_entries


def get_years():
    data = get_entries()

    # `data['entries'].keys()` returns a dict_keys view which FastAPI's
    # encoder may attempt to convert with `dict(...)` and fail. Return a
    # plain list of strings so it is JSON serializable.
    return list(data.get("entries", {}).keys())
