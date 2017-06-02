import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase)

class UbivarAPIResourcesTests(UbivarTestCase):

    def test_event_notification_retrieve(self):
        response = ubivar.EventNotification.retrieve("1")
        self.assertTrue(len(response.data) == 1)

    def test_event_notification_list(self):
        response = ubivar.EventNotification.list()
        self.assertTrue(len(response.data) == 3)
