from ..data.entries import get_entries

def get_entry_by_year(year: str):
    data = get_entries()
    return data['entries'].get(str(year), {})