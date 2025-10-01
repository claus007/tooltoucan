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

from dataclasses import dataclass

@dataclass
class Navigation:
    sections: list

    def __init__(self):
        self.sections = []
    @dataclass        
    class Link:
        def __init__(self, name, id, url, target):
            self.name = name
            self.id = id
            self.url = url
            self.target = target
      
    @dataclass      
    class Group:
        name: str
        links: list

        def __init__(self, name):
            self.name = name
            self.links = []

        def add_link(self, link):
            self.links.append(link)
            
        def clear_links(self):
            self.links = []
    @dataclass
    class Section:
        name: str
        id: int
        groups: list

        def __init__(self, name, id):
            self.name = name
            self.id = id
            self.groups = []

        def add_group(self, group):
            self.groups.append(group)
            
        def clear_groups(self):
            self.groups = []
            
    def read(self,connection):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM nav_view")
        current_section = self.Section("",0) # empty section for comparison
        current_group = self.Group("") # empty group for comparison
        for (idLink, lcId, lcName, lGroup, lName, dValue, lUri, lDescription, lcDescription) in cursor:
            if lcName != current_section.name:
                # new section
                current_section = self.Section(lcName, lcId)
                self.sections.append(current_section)
                current_group = self.Group(lGroup)
                current_section.add_group(current_group)
            elif lGroup != current_group.name:
                # new group
                current_group = self.Group(lGroup)
                current_section.add_group(current_group)

            # add link to group
            link = self.Link(lName,idLink, lUri, dValue)
            current_group.add_link(link)
            
        cursor.close()