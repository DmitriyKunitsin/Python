

class FormatDatParser:
    def __init__(self, title, file_format):
        self.__title = title
        self.__file_format = file_format
    @property
    def file_format(self):
        return self.__file_format
    @property
    def title(self, decription):
        if len(self.description) > 0:
            self.__title = self.description
    def description(self):
        return f"Парсер формата {self.__file_format}, описание : {self.__title}"
    