from .codes import (
    CLASS_BASE,
    DATETIME,
    INT,
    FLOAT,
    STRING,
    BOOL,
    RELATIONSHIP_CHILD,
    RELATIONSHIP_CHILD_FK,
    RELATIONSHIP_PARENT,
)


class DBClass:

    def __init__(self):
        self._classname: str = ""
        self._tablename: str = ""
        self.fields: dict = {}
        self.relationships: dict = {}

    def generate_relationships(self, code):
        for field, user_data in self.relationships.items():
            match user_data[0]:
                case "FK":
                    code = code + DBClass.f_relationship_fk(user_data[1])

                case "Child":
                    code = code + DBClass.f_relationship_child(
                        user_data[1], user_data[2], user_data[3]
                    )

                case "Parent":
                    code = code + DBClass.f_relationship_parent(
                        user_data[1], user_data[2], user_data[3]
                    )
        return code

    def generate_code(self):
        code = CLASS_BASE.replace("%classname%", self.classname).replace(
            "%tablename%", self.tablename
        )

        for field, field_type in self.fields.items():
            match field_type[0]:
                case "Integer":
                    code = code + DBClass.f_int(field_type[1])
                case "Float":
                    code = code + DBClass.f_float(field_type[1])
                case "String":
                    code = code + DBClass.f_string(field_type[1])
                case "DateTime":
                    code = code + DBClass.f_datetime(field_type[1])
                case "Boolean":
                    code = code + DBClass.f_bool(field_type[1])
        return self.generate_relationships(code)

    @property
    def classname(self):
        return self._classname

    @classname.setter
    def classname(self, new_classname):
        self._classname = new_classname

    @property
    def tablename(self):
        return self._tablename

    @tablename.setter
    def tablename(self, new_tablename):
        self._tablename = new_tablename

    def add_field(self, field_tag, field_name, field_type, pk=False):
        self.fields.update({field_tag: [field_type, field_name, pk]})

    def add_relationship_field_child_fk(self, field_tag, field_name, parent_tablename):
        self.relationships.update({field_tag: ["FK", field_name, parent_tablename]})

    def add_relationship_field_child(
        self, field_tag, field_name, parent_table, back_populates
    ):
        self.relationships.update(
            {field_tag: ["Child", field_name, parent_table, back_populates]}
        )

    def add_relationship_field_parent(
        self, field_tag, field_name, child_table, back_populates
    ):
        self.relationships.update(
            {field_tag: ["Parent", field_name, child_table, back_populates]}
        )

    @staticmethod
    def f_datetime(field_name):
        return DATETIME.replace("%fieldname%", field_name)

    @staticmethod
    def f_int(field_name):
        return INT.replace("%fieldname%", field_name)

    @staticmethod
    def f_float(field_name):
        return FLOAT.replace("%fieldname%", field_name)

    @staticmethod
    def f_string(field_name):
        return STRING.replace("%fieldname%", field_name)

    @staticmethod
    def f_bool(field_name):
        return BOOL.replace("%fieldname%", field_name)

    @staticmethod
    def f_relationship_fk(parent_tablename):
        return RELATIONSHIP_CHILD_FK.replace("%parent_tablename%", parent_tablename)

    @staticmethod
    def f_relationship_child(parent_tablename, parent_class, child_tablename):
        return (
            RELATIONSHIP_CHILD.replace("%parent_tablename%", parent_tablename)
            .replace("%parent_class%", parent_class)
            .replace(
                "%child_tablename%",
                child_tablename,
            )
        )

    @staticmethod
    def f_relationship_parent(child_tablename, child_class, parent_tablename):
        return (
            RELATIONSHIP_PARENT.replace("%child_tablename%", child_tablename)
            .replace("%child_class%", child_class)
            .replace(
                "%parent_tablename%",
                parent_tablename,
            )
        )
