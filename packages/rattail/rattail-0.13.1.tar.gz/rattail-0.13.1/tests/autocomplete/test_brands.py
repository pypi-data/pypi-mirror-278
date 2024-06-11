# -*- coding: utf-8; -*-

from __future__ import unicode_literals, absolute_import

from unittest import TestCase

import sqlalchemy as sa

from rattail.autocomplete import brands as mod
from rattail.config import make_config
from rattail.db import Session


class TestBrandAutocompleter(TestCase):

    def setUp(self):
        self.config = self.make_config()
        self.autocompleter = self.make_autocompleter()

    def make_config(self):
        return make_config([], extend=False)

    def make_autocompleter(self):
        return mod.BrandAutocompleter(self.config)

    def test_autocomplete(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)

        # first create a few brands
        alpha = model.Brand(name='Alpha Natural Foods')
        session.add(alpha)
        beta = model.Brand(name='Beta Natural Foods')
        session.add(beta)
        gamma = model.Brand(name='Gamma Natural Foods')
        session.add(gamma)

        # searching for nothing yields no results
        result = self.autocompleter.autocomplete(session, '')
        self.assertEqual(len(result), 0)

        # search for 'natural' yields all 3 brands
        result = self.autocompleter.autocomplete(session, 'natural')
        self.assertEqual(len(result), 3)

        # search for 'gamma' yields just that brand
        result = self.autocompleter.autocomplete(session, 'gamma')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['value'], gamma.uuid)
