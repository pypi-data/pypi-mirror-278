# -*- coding: utf-8; -*-

from __future__ import unicode_literals, absolute_import

from unittest import TestCase

from rattail.vendors import catalogs as mod
from rattail.config import make_config


class TestCatalogParser(TestCase):

    def setUp(self):
        self.config = self.make_config()
        self.parser = self.make_parser()

    def make_config(self):
        return make_config([], extend=False)

    def make_parser(self):
        return mod.CatalogParser(self.config)

    def test_key_required(self):

        # someone must define the parser key
        self.assertRaises(NotImplementedError, getattr, self.parser, 'key')

    def test_make_row(self):
        model = self.config.get_model()

        # make a basic row, it should work
        row = self.parser.make_row()
        self.assertIsInstance(row, model.VendorCatalogBatchRow)
