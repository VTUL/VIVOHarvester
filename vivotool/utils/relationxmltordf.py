import xmltodict

from rdflib import Graph, Literal, BNode, RDF, RDFS, URIRef, Namespace
from rdflib.namespace import FOAF, DC

from vivotool.utils.models.user_model import User
from vivotool.utils.models.publication_model import Publication, Authorship

VIVO = Namespace('http://vivoweb.org/ontology/core#')


class RelationshipTranslator(object):

    def __add_bindings(self, graph):
        graph.bind('vivo', VIVO)

    def __get_user(self, doc, user):
        user_doc = None
        for related in doc['entry']['api:relationship']['api:related']:
            if related['@category'] == 'user':
                user_doc = related
        if user_doc is not None:
            self.__make_user(user_doc, user)

    def __make_user(self, user_doc, user):
        user.user_id = user_doc['api:object']['@id']
        user.username = user_doc['api:object']['@username']

        for assoc in user_doc['api:object']['api:user-identifier-associations']['api:user-identifier-association']:
            if assoc['@scheme'] == 'email-address':
                email = assoc
        if email is not None:
            user.email = email['#text']

    def __get_publication(self, doc, publication):
        pub_doc = None
        for related in doc['entry']['api:relationship']['api:related']:
            if related['@category'] == 'publication':
                pub_doc = related

        if pub_doc is None:
            publication.is_publication = False
        else:
            self.__make_publication(pub_doc, publication)

    def __make_publication(self, pub_doc, publication):
        publication.id = pub_doc['api:object']['@id']

    def run(self, input_file, target_dir=""):
        with open(input_file) as fd:
            doc = xmltodict.parse(fd.read())
            feed = doc['feed']

        vivo_user = User()
        self.__get_user(feed, vivo_user)

        vivo_publication = Publication()
        self.__get_publication(feed, vivo_publication)
        vivo_authorship = Authorship(vivo_user, vivo_publication)
        vivo_authorship.id = feed['entry']['api:relationship']['@id']

        # only generate rdf if relationship references a publication
        if vivo_publication.is_publication:
            g = Graph()
            self.__add_bindings(g)
            vivo_authorship.add_to_graph(g)
            g.serialize(target_dir + vivo_authorship.id + ".rdf", format='nt')
