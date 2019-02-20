import os

class Utils:
    """docstring for Utils"""

    def __init__(self):
        pass


    def save_photo_file(self, content, filename):

        file = open(filename, "w")
        for block in content.iter_content(1024):
            file.write(block)
        file.close()

    def read_file(self, filename):

        with open(filename, 'r') as file:
            rdfcontent=file.read()

        return rdfcontent

    def save_xml_file(self, content, filename):

        file = open(filename, "wb")
        file.write(content)
        file.close()


    def listfiles(self, path, extension):

        all_files = list(
            filter(
                lambda x: x.endswith(extension),
                os.listdir(path)))

        return all_files


    def listdeletefiles(self, path, pattern):

        all_files = list(
            filter(
                lambda x: x.startswith(pattern),
                os.listdir(path)))

        return all_files