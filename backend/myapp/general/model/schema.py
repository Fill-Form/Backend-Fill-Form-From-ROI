# from general.util import convert_mm_to_pixel

class SchemaObject:

    def __init__(self, type, position, width, height, rotate, opacity, border_width, border_color, color, read_only):
        self.type = type
        self.position = position
        self.width = width
        self.height = height
        self.rotate = rotate
        self.opacity = opacity
        self.border_width = border_width
        self.border_color = border_color
        self.color = color
        self.read_only = read_only

    @classmethod
    def from_dict(cls, json_data):
        return cls(
            type=json_data['type'],
            position=json_data['position'],
            width=json_data['width'],
            height=json_data['height'],
            rotate=json_data['rotate'],
            opacity=json_data['opacity'],
            border_width=json_data['borderWidth'],
            border_color=json_data['borderColor'],
            color=json_data['color'],
            read_only=json_data['readOnly'],
        )

class Schema:
    def __init__(self):
        self.objects = {}

    def add_object(self, name, schema_object):
        self.objects[name] = schema_object

    @classmethod
    def from_dict(cls, dict_data):
        schema = cls()
        for name, obj_data in dict_data.items():
            schema.add_object(name, SchemaObject.from_dict(obj_data))
        return schema

class Document:
    def __init__(self, schema_list ):
        self.schemas = [Schema.from_dict(schema) for schema in schema_list]
        self.ocr_results = {}

    @staticmethod
    def convert_mm_to_pixel(mm, dpi=200):
        pixel = mm * dpi / 25.4
        return pixel

    @staticmethod
    def get_roi(document):
        header = []
        roi = {}
        for page_number, schema in enumerate(document.schemas, start=1):
            roi[page_number] = []
            for name, schema_object in schema.objects.items():
                x = Document.convert_mm_to_pixel(schema_object.position['x'])
                y = Document.convert_mm_to_pixel(schema_object.position['y'])
                width = Document.convert_mm_to_pixel(schema_object.width) + x
                height = Document.convert_mm_to_pixel(schema_object.height) + y

                header.append(name)
                roi[page_number].append([x, y, width, height])
        return header, roi
