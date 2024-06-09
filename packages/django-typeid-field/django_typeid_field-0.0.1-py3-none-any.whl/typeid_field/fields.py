from django.db import models
import re

from typeid import TypeID


class TypeidField(models.CharField):
    def __init__(self, *args, **kwargs) -> None:
        self.prefix = kwargs.pop("prefix", None)
        if self.prefix and len(self.prefix) > 63:
            raise ValueError("Prefix can't be longer than 63 characters.")
        if self.prefix and not re.match(r"^([a-z]([a-z_]{0,61}[a-z])?)?$", self.prefix):
            raise ValueError("Invalid prefix format.")

        if self.prefix:
            length = len(self.prefix) + 1 + 26  # prefix + 1 (separator) + 26
        else:
            length = 26
        kwargs["max_length"] = kwargs.pop("max_length", length)
        kwargs["default"] = self.typeid

        super(TypeidField, self).__init__(*args, **kwargs)

    def typeid(self):
        return str(TypeID(prefix=self.prefix))

    def get_internal_type(self):
        return "CharField"

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["prefix"] = self.prefix
        kwargs.pop("default", None)

        return name, path, args, kwargs
