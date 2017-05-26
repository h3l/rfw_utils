# encoding: utf-8

"""
@author: h3l
@contact: xidianlz@gmail.com
@file: startapp_skeleton.py
@time: 2017/2/28 17:46
"""
import os
import json

from django.core.management.base import BaseCommand, CommandError

TYPE_AND_FIELD_MAP = {
    "str": "CharField",
    "int": "IntegerField",
    "positive_int": "PositiveIntegerField",
    "text": "TextField",
    "choice": "CharField",
    "bool": "BooleanField",
    "date": "DateField",
    "datetime": "DateTimeField"
}


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("config_file", type=str)

    def handle(self, *args, **options):
        path = options["config_file"]
        assert os.path.isfile(path), "文件不存在"
        with open(path, encoding="utf-8") as f:
            models = json.load(f)
        file_name = os.path.basename(path)
        app_name, _ = os.path.splitext(file_name)
        os.mkdir(app_name)
        for model in models:
            model["name"] = model["name"].capitalize()
            for field in model["fields"]:
                if field["type"] == "choice":
                    field["choices"] = tuple([tuple(choice) for choice in field["choices"]])
                    field["max_length"] = max([len(choice[0]) for choice in field["choices"]])
        # 生成models文件
        model_result = ""
        model_result += "from django.db import models\n"
        for model in models:
            model_result += "\n\nclass {}(models.Model):\n".format(model["name"])
            for field in model["fields"]:
                model_result += " " * 4
                field_name = field["name"]
                field_type = field["type"]
                model_field = TYPE_AND_FIELD_MAP[field_type]
                verbose_name = field["verbose_name"]
                if field_type == "str":
                    model_result += '{} = models.{}("{}", max_length={})'.format(field_name, model_field, verbose_name,
                                                                                 field.get("max_length", 64))
                elif field_type in ["positive_int", "text", "int"]:
                    model_result += '{} = models.{}("{}")'.format(field_name, model_field, verbose_name)
                elif field_type == "bool":
                    model_result += '{} = models.{}("{}", default={})'.format(field_name, model_field, verbose_name,
                                                                              field["default"])
                elif field_type == "choice":
                    model_result += '{} = models.{}("{}", choices={}, max_length={})'.format(field_name, model_field,
                                                                                             verbose_name,
                                                                                             field["choices"],
                                                                                             field["max_length"])
                elif field_type in ["datetime", "date"]:
                    model_result += '{} = models.{}("{}"{}{})'.format(field_name, model_field, verbose_name,
                                                                      ", auto_now=True" if field.get("auto_now",
                                                                                                     False) else "",
                                                                      ", auto_now_add=True" if field.get("auto_now_add",
                                                                                                         False) else "", )
                model_result += "\n"
        with open(app_name + "/models.py", "w", encoding="utf-8") as f:
            f.write(model_result)
            print("models.py is OK")

        # 生成serializers文件
        serializers_result = ""
        serializers_result += """from rest_framework import serializers

from rfw_utils.functions import generate_fields

from . import models
"""
        for model in models:
            model_name = model["name"]
            serializers_result += "\n\n"
            serializers_result += "class {}Serializer(serializers.HyperlinkedModelSerializer):".format(model_name)
            serializers_result += """
    class Meta:
        model = models.{model_name}
        fields = generate_fields(models.{model_name}, add=["url"])
""".format(model_name=model_name)

        with open(app_name + "/serializers.py", "w", encoding="utf-8") as f:
            f.write(serializers_result)
            print("serializers.py is OK")

        # 生成views
        views_result = ""
        views_result += """from . import serializers
from . import models

from rest_framework.viewsets import ModelViewSet"""
        for model in models:
            views_result += "\n\n"
            views_result += """
class {model_name}ViewSet(ModelViewSet):
    serializer_class = serializers.{model_name}Serializer
    queryset = models.{model_name}.objects.all()""".format(model_name=model["name"])
        views_result += "\n"
        with open(app_name + "/views.py", "w", encoding="utf-8") as f:
            f.write(views_result)
            print("views.py is OK")

        # 生成admin
        admin_result = ""
        admin_result += "from django.contrib import admin\n"
        admin_result += "from . import models\n"
        model_list = []
        for model in models:
            model_list.append("models." + model["name"])
        admin_result += "\n\nadmin.site.register([{}])\n".format(", ".join(model_list))
        with open(app_name + "/admin.py", "w", encoding="utf-8") as f:
            f.write(admin_result)
            print("admin.py is OK")

        # 生成urls
        urls_result = ""
        urls_result += """from rest_framework import routers

from . import views

router = routers.DefaultRouter()

"""
        for model in models:
            model_name = model["name"]
            urls_result += "router.register(r'{lower_model_name}', views.{model_name}ViewSet, \
base_name='{lower_model_name}')".format(
                lower_model_name=model_name.lower(), model_name=model_name
            )
            urls_result += "\n"
        urls_result += "\nurlpatterns = router.urls\n"

        with open(app_name + "/urls.py", "w", encoding="utf-8") as f:
            f.write(urls_result)
            print("urls.py is OK")
        # 生成apps
        apps_result = ""
        apps_result += """from django.apps import AppConfig


class {}Config(AppConfig):
    name = '{}'
""".format(app_name.capitalize(), app_name)

        with open(app_name + "/apps.py", "w", encoding="utf-8") as f:
            f.write(apps_result)
            print("apps.py is ok")

        # 生成test
        with open(app_name + "/test.py", "w", encoding="utf-8") as f:
            f.write("# Create your tests here.")
            print("test.py is OK")
        # 生成__init__.py
        with open(app_name + "/__init__.py", "w", encoding="utf-8") as f:
            f.write("")
            print("__init__.py is OK")
        print("记得添加该 app 到 INSTALLED_APPS, 以及添加该 app 的 urls 到 主urls.py 文件中。")
