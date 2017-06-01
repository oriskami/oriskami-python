import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase)

class UbivarAPIResourcesTests(UbivarTestCase):

    def test_event_label_list(self):
        response = ubivar.EventLabel.list()
        self.assertTrue(len(response.data) == 3)

    def test_event_label_retrieve(self):
        response = ubivar.EventLabel.retrieve("1")
        event = response.data[0]
        self.assertEqual(event["id"], "1")
        self.assertEqual(event["labels"], True)

        response = ubivar.EventLabel.retrieve("2")
        event = response.data[0]
        self.assertEqual(event["id"], "2")
        self.assertEqual(event["labels"], False)

        response = ubivar.EventLabel.retrieve("3")
        event = response.data[0]
        self.assertEqual(event["id"], "3")
        self.assertEqual(event["labels"], None)

    def test_event_label_update(self):
        eventId = "1"
        response = ubivar.EventLabel.update(eventId, label="is_loss", value="false")
        print(response)
        response = ubivar.EventLabel.update(eventId, label="is_loss", value="true")
        print(response)
        response = ubivar.EventLabel.update(eventId, label="another_label", value="false")
        print(response)
        self.assertTrue(True)

