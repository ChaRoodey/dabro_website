from io import BytesIO
from typing import Any
from openpyxl import load_workbook

from app.core.config import settings


def _norm_header(head: Any) -> str:
    return str(head).strip() if head is not None else ''


def _to_int(value: Any, field: str, row: int) -> int:
    if value is None or str(value).strip() == '':
        raise ValueError(f"Row {row}: '{field}' is required")

    try:
        if isinstance(value, float):
            if not value.is_integer():
                raise ValueError(f"Row {row}: '{field}' must be an integer")
            return int(value)
        return int(str(value).strip())
    except Exception:
        raise ValueError(f"Row {row}: '{field}' must be int, got {value!r}")


def parse_products_sheet(file_bytes: bytes) -> list[dict]:
    wb = load_workbook(filename=BytesIO(file_bytes), data_only=True)

    if settings.SHEET_NAME not in wb.sheetnames:
        raise ValueError(f"Sheet '{settings.SHEET_NAME}' not found. Available: {wb.sheetnames}")

    ws = wb[settings.SHEET_NAME]
    header_row = next(ws.iter_rows(min_row=1, max_row=1, values_only=True), None)
    headers = [_norm_header(header) for header in header_row]
    col_index = {name: idx for idx, name in enumerate(headers) if name}

    missing = settings.REQUIRED_COLUMNS - set(col_index.keys())
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    items: list[dict] = []

    for r_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        if row is None or all(cell is None or str(cell).strip() == '' for cell in row):
            continue

        def get(col: str):
            i = col_index[col]
            return row[i] if i < len(row) else None

        product_id = _to_int(get('id'), 'id', r_idx)
        cost = _to_int(get('Стоимость'), 'Стоимость', r_idx)
        items_left = _to_int(get('Остаток'), 'Остаток', r_idx)

        items.append({
            "row": r_idx,
            "product_id": product_id,
            "cost": cost,
            "items_left": items_left,
        })

    return items
