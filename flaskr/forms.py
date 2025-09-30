# Copyright (c) 2025 Claus Ilginnis
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from abc import ABC, abstractmethod


class FormFields:
    class Field(ABC):

        @abstractmethod
        def get_type(self):
            pass

    class Text(Field):
        def __init__(self, name, id, value, required, max_length=255, min_length=0, regexp=""):
            self.name = name
            self.id = id
            self.value = value
            self.required = required
            self.max_length = max_length
            self.min_length = min_length
            self.regexp = regexp

        def get_type(self):
            return "text"

    class FixedOptions(Field):
        def __init__(self, name, id, options, value, required):
            self.name = name
            self.id = id
            self.options = options
            self.value = value
            self.required = required

        def get_type(self):
            return "options"

    class Hidden(Field):
        def __init__(self, name, id, value):
            self.name = name
            self.id = id
            self.value = value

        def get_type(self):
            return "hidden"


class Form:
    def __init__(self, caption, action, id_name=None, id_value=None):
        self.caption = caption
        self.action = action
        self.fields = []
        self.fields_dict = {}
        if id_name is not None and id_value is not None:
            self.new = False
            self.add_field(FormFields.Hidden(id_name, id_value))
        else:
            self.new = True

    def add_field(self, field):
        assert isinstance(field, FormFields.Field)
        self.fields.append(field)
        if field.id in self.fields_dict:
            raise ValueError(f"Field with id '{field.id}' already exists.")
        self.fields_dict[field.id] = field

