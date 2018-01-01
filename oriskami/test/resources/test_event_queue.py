import os
import oriskami
import warnings
from oriskami.test.helper import (OriskamiTestCase)

class OriskamiAPIResourcesTests(OriskamiTestCase):

    def test_event_queue_retrieve(self):
        response = oriskami.EventQueue.retrieve("1")
        event = response.data[0]
        self.assertEqual(event["id"], "1")
        self.assertEqual(event.queues.active, "rules_base")

        response = oriskami.EventQueue.retrieve("2")
        event = response.data[0]
        self.assertEqual(event["id"], "2")
        self.assertEqual(event.queues.active, "peer_review")

        response = oriskami.EventQueue.retrieve("3")
        event = response.data[0]
        self.assertEqual(event["id"], "3")
        self.assertEqual(event.queues, None)

    def test_event_queue_update(self):
        eventId = "1"

        response = oriskami.EventQueue.update(eventId, active="rules_custom")
        self.assertEqual(response.data[0].id, eventId)
        self.assertEqual(response.data[0].queues.active, "rules_custom")

        response = oriskami.EventQueue.update(eventId, active="rules_base")
        self.assertEqual(response.data[0].queues.active, "rules_base")

    def test_event_queue_delete(self):
        eventId = "1"

        response = oriskami.EventQueue.delete(eventId)
        self.assertFalse(hasattr(response.data[0].queues, "active"))

        response = oriskami.EventQueue.update(eventId, active="rules_base")
        self.assertTrue(hasattr(response.data[0].queues, "active"))
        self.assertEqual(response.data[0].queues.active, "rules_base")

    def test_event_queue_list(self):
        response = oriskami.EventQueue.list()
        self.assertTrue(len(response.data) == 2)
