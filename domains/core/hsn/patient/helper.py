from sqlalchemy import asc, desc


def apply_ordering(query, model, columnKey, order):
    if columnKey and hasattr(model, columnKey):
        column_attribute = getattr(model, columnKey)
        if order == "ascend":
            query = query.order_by(asc(column_attribute))
        else:
            query = query.order_by(desc(column_attribute))
    return query
