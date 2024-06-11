# -*- coding: utf-8; -*-

from __future__ import unicode_literals, absolute_import

from unittest import TestCase

import sqlalchemy as sa

from rattail.batch import handheld as mod
from rattail.config import make_config
from rattail.db import Session


class TestHandheldBatchHandler(TestCase):

    def setUp(self):
        self.config = self.make_config()
        self.handler = self.make_handler()

    def make_config(self):
        return make_config([], extend=False)

    def make_handler(self):
        return mod.HandheldBatchHandler(self.config)

    def test_make_inventory_batch(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)

        # prep data
        betty = model.User(username='betty')
        handbatch = model.HandheldBatch(id=1, created_by=betty)
        session.add(handbatch)
        session.commit()

        # make basic inventory batch
        invbatch = self.handler.make_inventory_batch([handbatch], betty, id=2)
        self.assertIsNotNone(invbatch)
        self.assertEqual(invbatch.id, 2)

    def test_make_label_batch(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)

        # prep data
        betty = model.User(username='betty')
        handbatch = model.HandheldBatch(id=1, created_by=betty)
        session.add(handbatch)
        session.commit()

        # make basic label batch
        lblbatch = self.handler.make_label_batch([handbatch], betty, id=2)
        self.assertIsNotNone(lblbatch)
        self.assertEqual(lblbatch.id, 2)
