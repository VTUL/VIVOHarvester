import requests


class VIVO:
    """docstring for VIVO"""

    def __init__(self):
        pass

    def insert_vivo(self, objcontent, vivo_endpoint, headers, data):

        query_string = "INSERT DATA {\n" + \
            "GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2> {\n"
        query_string += objcontent
        query_string += "}\n}\n"

        data["update"] = query_string
        response = requests.post(vivo_endpoint, headers=headers, data=data)

        return response

    def describe_vivo_object(self, objecturl, vivo_endpoint, headers, data):

        query_string = "DESCRIBE <" + objecturl + ">"

        data["query"] = query_string
        response = requests.post(vivo_endpoint, headers=headers, data=data)

        return response

    def delete_vivo_object(self, objcontent, vivo_endpoint, headers, data):

        query_string = "DELETE DATA {\n" + \
            "GRAPH <http://vitro.mannlib.cornell.edu/default/vitro-kb-2> {\n"
        query_string += objcontent
        query_string += "}\n}\n"

        data["update"] = query_string
        response = requests.post(vivo_endpoint, headers=headers, data=data)

        return response
