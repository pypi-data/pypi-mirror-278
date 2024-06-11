# -*- coding: utf-8; -*-

from __future__ import unicode_literals, absolute_import

from unittest import TestCase

import sqlalchemy as sa

from rattail.autocomplete import people as mod
from rattail.config import make_config
from rattail.db import Session


class TestPersonAutocompleter(TestCase):

    def setUp(self):
        self.config = self.make_config()
        self.autocompleter = self.make_autocompleter()

    def make_config(self):
        return make_config([], extend=False)

    def make_autocompleter(self):
        return mod.PersonAutocompleter(self.config)

    def test_autocomplete(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)
        enum = self.config.get_enum()

        # first create some people
        alice = model.Person(display_name='Alice Chalmers')
        session.add(alice)
        bob = model.Person(display_name='Bob Loblaw')
        session.add(bob)
        charlie = model.Person(display_name='Charlie Chaplin')
        session.add(charlie)

        # searching for nothing yields no results
        result = self.autocompleter.autocomplete(session, '')
        self.assertEqual(len(result), 0)

        # search for 'l' yields all 3 people
        result = self.autocompleter.autocomplete(session, 'l')
        self.assertEqual(len(result), 3)

        # search for 'cha' yields just 2 people
        result = self.autocompleter.autocomplete(session, 'cha')
        self.assertEqual(len(result), 2)
        uuids = [info['value'] for info in result]
        self.assertIn(alice.uuid, uuids)
        self.assertIn(charlie.uuid, uuids)


class TestPersonEmployeeAutocompleter(TestCase):

    def setUp(self):
        self.config = self.make_config()
        self.autocompleter = self.make_autocompleter()

    def make_config(self):
        return make_config([], extend=False)

    def make_autocompleter(self):
        return mod.PersonEmployeeAutocompleter(self.config)

    def test_autocomplete(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)
        enum = self.config.get_enum()

        # first create some people
        alice = model.Person(display_name='Alice Chalmers')
        session.add(alice)
        bob = model.Person(display_name='Bob Loblaw')
        bob.employee = model.Employee(status=enum.EMPLOYEE_STATUS_CURRENT)
        session.add(bob)
        charlie = model.Person(display_name='Charlie Chaplin')
        charlie.employee = model.Employee(status=enum.EMPLOYEE_STATUS_FORMER)
        session.add(charlie)

        # searching for nothing yields no results
        result = self.autocompleter.autocomplete(session, '')
        self.assertEqual(len(result), 0)

        # search for 'l' yields only Bob, Charlie
        result = self.autocompleter.autocomplete(session, 'l')
        self.assertEqual(len(result), 2)
        uuids = [info['value'] for info in result]
        self.assertIn(bob.uuid, uuids)
        self.assertIn(charlie.uuid, uuids)

        # search for 'cha' yields just Charlie
        result = self.autocompleter.autocomplete(session, 'cha')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['value'], charlie.uuid)
