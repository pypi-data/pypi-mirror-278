# -*- coding: utf-8; -*-

from __future__ import unicode_literals, absolute_import

import os
from unittest import TestCase

import sqlalchemy as sa

from rattail.batch import handlers as mod
from rattail.config import make_config
from rattail.db import Session


class TestBatchHandler(TestCase):

    def setUp(self):
        self.config = self.make_config()
        self.handler = self.make_handler()

    def make_config(self):
        return make_config([], extend=False)

    def make_handler(self):
        return mod.BatchHandler(self.config)

    def test_consume_batch_id(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)

        # first id is 1
        result = self.handler.consume_batch_id(session)
        self.assertEqual(result, 1)

        # second is 2; test string version
        result = self.handler.consume_batch_id(session, as_str=True)
        self.assertEqual(result, '00000002')

    def test_get_effective_rows(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)

        # make batch w/ 3 rows
        user = model.User(username='patty')
        batch = model.NewProductBatch(id=1, created_by=user)
        batch.data_rows.append(model.NewProductBatchRow())
        batch.data_rows.append(model.NewProductBatchRow())
        batch.data_rows.append(model.NewProductBatchRow())
        self.assertEqual(len(batch.data_rows), 3)

        # all rows should be effective by default
        result = self.handler.get_effective_rows(batch)
        self.assertEqual(len(result), 3)

        # unless we mark one as "removed"
        batch.data_rows[1].removed = True
        result = self.handler.get_effective_rows(batch)
        self.assertEqual(len(result), 2)

        # or if we delete one
        batch.data_rows.pop(-1)
        result = self.handler.get_effective_rows(batch)
        self.assertEqual(len(result), 1)
