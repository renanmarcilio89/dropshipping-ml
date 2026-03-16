from app.normalization.title_norm import normalize_title
from app.schemas.common import ItemRecord


PRIORITY_IDS = {'GTIN', 'EAN', 'UPC', 'MPN', 'MODEL', 'BRAND'}


def build_equivalence_key(item: ItemRecord) -> str:
    attrs = {attr.attribute_id: attr.value_name for attr in item.attributes if attr.attribute_id in PRIORITY_IDS}

    for key in ('GTIN', 'EAN', 'UPC'):
        if attrs.get(key):
            return f'{key}:{attrs[key]}'

    if attrs.get('BRAND') and attrs.get('MODEL'):
        return f"BM:{attrs['BRAND']}:{attrs['MODEL']}"

    core_title = normalize_title(item.title or '')
    return f'CAT:{item.category_id}|TITLE:{core_title}'
