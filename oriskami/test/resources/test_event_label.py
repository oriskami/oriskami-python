import os
import oriskami
import warnings
from oriskami.test.helper import (OriskamiTestCase)

class OriskamiAPIResourcesTests(OriskamiTestCase):

    def test_event_label_retrieve(self):
        response = oriskami.EventLabel.retrieve("1")
        event = response.data[0]
        self.assertEqual(event["id"], "1")
        self.assertEqual(event["labels"], "true")

        response = oriskami.EventLabel.retrieve("2")
        event = response.data[0]
        self.assertEqual(event["id"], "2")
        self.assertEqual(event["labels"], "false")

        response = oriskami.EventLabel.retrieve("3")
        event = response.data[0]
        self.assertEqual(event["id"], "3")
        self.assertEqual(event["labels"], None)

    def test_event_label_update(self):
        eventId = "1"
        response = oriskami.EventLabel.update(eventId, label="is_loss", value="false")
        self.assertEqual(response.data[0].id, eventId)
        self.assertEqual(response.data[0].labels.is_loss, "false")
        response = oriskami.EventLabel.update(eventId, label="is_loss", value="true")
        self.assertEqual(response.data[0].labels.is_loss, "true")

    def test_event_label_delete(self):
        eventId = "1"
        response = oriskami.EventLabel.delete(eventId, label="is_loss")
        self.assertFalse(hasattr(response.data[0].labels, "is_loss"))
        response = oriskami.EventLabel.update(eventId, label="is_loss", value="true")
        self.assertTrue(hasattr(response.data[0].labels, "is_loss"))

    def test_event_label_list(self):
        response = oriskami.EventLabel.list()
        self.assertTrue(len(response.data) == 3)
