
class Navigation:
    def __init__(self):
        self.sections = []
        
    class Link:
        def __init__(self, name, url, target):
            self.name = name
            self.url = url
            self.target = target
            
    class Group:
        def __init__(self, name):
            self.name = name
            self.links = []

        def add_link(self, link):
            self.links.append(link)
            
        def clear_links(self):
            self.links = []
            
    class Section:
        def __init__(self, name):
            self.name = name
            self.groups = []

        def add_group(self, group):
            self.groups.append(group)
            
        def clear_groups(self):
            self.groups = []
            
    def read(self,connection):
        nav = Navigation()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM nav_view")
        current_section = self.Section("") # empty section for comparison
        current_group = self.Group("") # empty group for comparison
        for (idLink, lcName, lGroup, lName, dValue, lUri, lDescription, lcDescription) in cursor:
            if lcName != current_section.name:
                # new section
                current_section = self.Section(lcName)
                nav.sections.append(current_section)
                current_group = self.Group(lGroup)
                current_section.add_group(current_group)
            elif lGroup != current_group.name:
                # new group
                current_group = self.Group(lGroup)
                current_section.add_group(current_group)

            # add link to group
            link = self.Link(lName, lUri, dValue)
            current_group.add_link(link)
            
        cursor.close()
        return nav