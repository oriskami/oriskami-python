import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase)

class UbivarAPIResourcesTests(UbivarTestCase):

    def test_event_label_retrieve(self):
        response = ubivar.EventLabel.retrieve("1")
        event = response.data[0]
        self.assertEqual(event["id"], "1")
        self.assertEqual(event["labels"], "true")

        response = ubivar.EventLabel.retrieve("2")
        event = response.data[0]
        self.assertEqual(event["id"], "2")
        self.assertEqual(event["labels"], "false")

        response = ubivar.EventLabel.retrieve("3")
        event = response.data[0]
        self.assertEqual(event["id"], "3")
        self.assertEqual(event["labels"], None)

    def test_event_label_update(self):
        eventId = "1"
        response = ubivar.EventLabel.update(eventId, label="is_loss", value="false")
        self.assertEqual(response.data[0].id, eventId)
        self.assertEqual(response.data[0].labels.is_loss, "false")
        response = ubivar.EventLabel.update(eventId, label="is_loss", value="true")
        self.assertEqual(response.data[0].labels.is_loss, "true")

    def test_event_label_delete(self):
        eventId = "1"
        response = ubivar.EventLabel.delete(eventId, label="is_loss")
        self.assertFalse(hasattr(response.data[0].labels, "is_loss"))
        response = ubivar.EventLabel.update(eventId, label="is_loss", value="true")
        self.assertTrue(hasattr(response.data[0].labels, "is_loss"))

    def test_event_label_list(self):
        response = ubivar.EventLabel.list()
        self.assertTrue(len(response.data) == 3)
        print(response)
