# -*- coding: utf-8; -*-

from __future__ import unicode_literals, absolute_import

from unittest import TestCase

import sqlalchemy as sa

from rattail.autocomplete import employees as mod
from rattail.config import make_config
from rattail.db import Session


class TestEmployeeAutocompleter(TestCase):

    def setUp(self):
        self.config = self.make_config()
        self.autocompleter = self.make_autocompleter()

    def make_config(self):
        return make_config([], extend=False)

    def make_autocompleter(self):
        return mod.EmployeeAutocompleter(self.config)

    def test_autocomplete(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)
        enum = self.config.get_enum()

        # first create some employees
        alice = model.Person(display_name='Alice Chalmers')
        alice.employee = model.Employee(status=enum.EMPLOYEE_STATUS_CURRENT)
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

        # search for 'l' yields only 2 current employees
        result = self.autocompleter.autocomplete(session, 'l')
        self.assertEqual(len(result), 2)

        # search for 'alice' yields just Alice Chalmers
        result = self.autocompleter.autocomplete(session, 'alice')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['value'], alice.employee.uuid)
