# encoding: utf-8

"""
@author: h3l
@contact: xidianlz@gmail.com
@file: functions.py
@time: 2017/2/21 11:35
"""
from django.db.models.fields import Field
from datetime import datetime


def remove_key(data, keys=None):
    if keys is None:
        keys = []
    for key in keys:
        data.pop(key, None)
    return data


def generate_fields(model, add=None, remove=None):
    if add is None:
        add = []
    if remove is None:
        remove = []

    remove.append("id")
    result = []
    for field in model._meta.get_fields():
        if isinstance(field, Field):
            result.append(field.name)
    for item in add:
        result.append(item)
    for item in remove:
        try:
            result.remove(item)
        except ValueError:
            pass

    return tuple(result)

