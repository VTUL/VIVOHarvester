import os
import logging

class Utils:
    """docstring for Utils"""

    def save_photo_file(self, content, filename):

        try:
            file = open(filename, "wb")
            for block in content.iter_content(1024):
                file.write(block)
            file.close()
        except Exception:
            logging.exception("")

    def read_file(self, filename):

        rdfcontent = ""
        try:
            with open(filename, "r") as file:
                rdfcontent=file.read()
        except Exception:
            logging.exception("")

        return rdfcontent

    def save_xml_file(self, content, filename):

        try:
            with open(filename, "w") as file:
                file.write(content)
        except Exception:
            logging.exception("")

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