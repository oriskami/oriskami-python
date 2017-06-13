import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase)

class UbivarAPIResourcesTests(UbivarTestCase):

    def test_event_queue_retrieve(self):
        response = ubivar.EventQueue.retrieve("1")
        event = response.data[0]
        self.assertEqual(event["id"], "1")
        self.assertEqual(event.queues.active, "rules_base")

        response = ubivar.EventQueue.retrieve("2")
        event = response.data[0]
        self.assertEqual(event["id"], "2")
        self.assertEqual(event.queues.active, "peer_review")

        response = ubivar.EventQueue.retrieve("3")
        event = response.data[0]
        self.assertEqual(event["id"], "3")
        self.assertEqual(event.queues, None)

    def test_event_queue_update(self):
        eventId = "1"

        response = ubivar.EventQueue.update(eventId, active="rules_custom")
        self.assertEqual(response.data[0].id, eventId)
        self.assertEqual(response.data[0].queues.active, "rules_custom")

        response = ubivar.EventQueue.update(eventId, active="rules_base")
        self.assertEqual(response.data[0].queues.active, "rules_base")

    def test_event_queue_delete(self):
        eventId = "1"

        response = ubivar.EventQueue.delete(eventId)
        self.assertFalse(hasattr(response.data[0].queues, "active"))

        response = ubivar.EventQueue.update(eventId, active="rules_base")
        self.assertTrue(hasattr(response.data[0].queues, "active"))
        self.assertEqual(response.data[0].queues.active, "rules_base")

    def test_event_queue_list(self):
        response = ubivar.EventQueue.list()
        self.assertTrue(len(response.data) == 2)
