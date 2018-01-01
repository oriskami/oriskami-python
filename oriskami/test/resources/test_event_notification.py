import os
import oriskami
import warnings
from oriskami.test.helper import (OriskamiTestCase)

class OriskamiAPIResourcesTests(OriskamiTestCase):

    def test_event_notification_retrieve(self):
        response = oriskami.EventNotification.retrieve("1")
        self.assertTrue(len(response.data) == 1)

    def test_event_notification_list(self):
        response = oriskami.EventNotification.list()
        self.assertTrue(len(response.data) == 3)
