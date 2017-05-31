import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase, DUMMY_EVENT_1, DUMMY_EVENT_2)

class UbivarAPIResourcesTests(UbivarTestCase):

    def test_event_create(self):
        expected_id = DUMMY_EVENT_1['id']
        response = ubivar.Event.create(parameters=DUMMY_EVENT_1)
        self.assertTrue(response.id == expected_id)
        self.assertTrue(hasattr(response, "parameters"))

        expected_id = DUMMY_EVENT_2['id']
        response = ubivar.Event.create(parameters=DUMMY_EVENT_2)
        self.assertTrue(response.id == expected_id)
        self.assertTrue(hasattr(response, "parameters"))

    def test_event_list(self):
        response = ubivar.Event.list()
        self.assertTrue(len(response.data) == 2)

    def test_event_list_filter_limit(self):
        response = ubivar.Event.list(limit=1)
        self.assertTrue(len(response.data) == 1)
        self.assertTrue(hasattr(response.data, "__iter__"))

    def test_event_list_filter_gte(self):
        response = ubivar.Event.list(id={"gte": 2})
        self.assertTrue(len(response.data) == 1)
        self.assertTrue(response.data[0]['id'] == DUMMY_EVENT_2['id'])

    def test_event_list_filter_gt(self):
        response = ubivar.Event.list(id={"gt": 1})
        self.assertTrue(len(response.data) == 1)
        self.assertTrue(response.data[0]['id'] == DUMMY_EVENT_2['id'])

    def test_event_list_filter_lte(self):
        response = ubivar.Event.list(id={"lte": 1})
        self.assertTrue(len(response.data) == 1)
        self.assertTrue(response.data[0]['id'] == DUMMY_EVENT_1['id'])

    def test_event_list_filter_lt(self):
        response = ubivar.Event.list(id={"lt": 2})
        self.assertTrue(len(response.data) == 1)
        self.assertTrue(response.data[0]['id'] == DUMMY_EVENT_1['id'])


