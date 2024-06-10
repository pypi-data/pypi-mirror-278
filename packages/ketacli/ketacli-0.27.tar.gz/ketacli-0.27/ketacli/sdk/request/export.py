from .asset_map import get_request_path
import json
from ..util import template_render


def export_asset_request(asset_type, name=None, data=None, **kwargs):
    path, method, example = get_request_path(asset_type, "download")

    example = json.dumps(example, ensure_ascii=False)
    if name is not None and "name" not in kwargs:
        kwargs.update({"name": name})
    path = template_render(path, **kwargs)
    example = template_render(example, **kwargs)
    example = json.loads(example)
    if not data:
        data = example
    return {
        "path": path,
        "query_params": {},
        # list 操作用不到的内容
        "method": method,
        "data": data,
        "custom_headers": {},
    }
