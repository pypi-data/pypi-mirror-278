# expressions.py
from .utils import validate_type


def eq(field, value):
    validate_type(field, str, "Field eq")
    return {"eq": {field: value}}


def neq(field, value):
    validate_type(field, str, "Field neq")
    return {"neq": {field: value}}


def like(field, value):
    validate_type(field, str, "Field like")
    validate_type(value, str, "Value like")
    return {"like": {field: value}}


def gt(field, value):
    validate_type(field, str, "Field gt")
    return {"gt": {field: value}}


def lt(field, value):
    validate_type(field, str, "Field lt")
    return {"lt": {field: value}}


def gte(field, value):
    validate_type(field, str, "Field gte")
    return {"gte": {field: value}}


def lte(field, value):
    validate_type(field, str, "Field lte")
    return {"lte": {field: value}}


def in_(field, values):
    validate_type(field, str, "Field in")
    validate_type(values, list, "Value in")
    return {"in": {field: values}}


def nin(field, values):
    validate_type(field, str, "Field nin")
    validate_type(values, list, "Value nin")
    return {"nin": {field: values}}


def exists(field):
    validate_type(field, str, "Field exists")
    return {"exists": field}

