import os
import oriskami
import warnings
from oriskami.test.helper import (OriskamiTestCase, DUMMY_EVENT_1, DUMMY_EVENT_2, DUMMY_EVENT_3)

class OriskamiAPIResourcesTests(OriskamiTestCase):

    def test_event_create(self):
        response = oriskami.Event.create(parameters=DUMMY_EVENT_1)
        event = response.data[0]
        self.assertTrue(hasattr(event, "parameters"))
        self.assertTrue(event["id"] == DUMMY_EVENT_1["id"])

        response = oriskami.Event.create(parameters=DUMMY_EVENT_2)
        event = response.data[0]
        self.assertTrue(hasattr(event, "parameters"))
        self.assertTrue(event["id"] == DUMMY_EVENT_2["id"])

        response = oriskami.Event.create(parameters=DUMMY_EVENT_3)
        event = response.data[0]
        self.assertTrue(hasattr(event, "parameters"))
        self.assertTrue(event["id"] == DUMMY_EVENT_3["id"])

    def test_event_list(self):
        response = oriskami.Event.list()
        self.assertTrue(len(response.data) == 3)

    def test_event_list_filter_id_limit(self):
        response = oriskami.Event.list(limit=1)
        self.assertTrue(len(response.data) == 1)
        self.assertTrue(hasattr(response.data, "__iter__"))

    def test_event_list_filter_id_order(self):
        response = oriskami.Event.list(order="-id")
        self.assertTrue(len(response.data) == 3)
        self.assertTrue(response.data[0]['id'] == DUMMY_EVENT_3['id'])

        response = oriskami.Event.list(order="id")
        self.assertTrue(len(response.data) == 3)
        self.assertTrue(response.data[0]['id'] == DUMMY_EVENT_1['id'])

    def test_event_list_filter_id_gte(self):
        response = oriskami.Event.list(id={"gte": 2}, order="id")
        self.assertTrue(len(response.data) == 2)
        self.assertTrue(response.data[0]['id'] == DUMMY_EVENT_2['id'])
        self.assertTrue(response.data[1]['id'] == DUMMY_EVENT_3['id'])

    def test_event_list_filter_id_gt(self):
        response = oriskami.Event.list(id={"gt": 1}, order="id")
        self.assertTrue(len(response.data) == 2)
        self.assertTrue(response.data[0]['id'] == DUMMY_EVENT_2['id'])
        self.assertTrue(response.data[1]['id'] == DUMMY_EVENT_3['id'])

    def test_event_list_filter_id_lte(self):
        response = oriskami.Event.list(id={"lte": 2}, order="id")
        self.assertTrue(len(response.data) == 2)
        self.assertTrue(response.data[0]['id'] == DUMMY_EVENT_1['id'])
        self.assertTrue(response.data[1]['id'] == DUMMY_EVENT_2['id'])

    def test_event_list_filter_id_lt(self):
        response = oriskami.Event.list(id={"lt": 3}, order="id")
        self.assertTrue(len(response.data) == 2)
        self.assertTrue(response.data[0]['id'] == DUMMY_EVENT_1['id'])
        self.assertTrue(response.data[1]['id'] == DUMMY_EVENT_2['id'])

