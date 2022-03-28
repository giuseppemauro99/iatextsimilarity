from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

import spacy

from .views import index


class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get("/")
        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = index(request)
        self.assertEqual(response.status_code, 200)
    
    def spacyTest(self):
        nlp = spacy.load("it_core_news_md")

        doc1 = nlp("test spacy1")
        doc2 = nlp("test spacy2")

        self.assertTrue(doc1.similarity(doc2) > 0.5)
