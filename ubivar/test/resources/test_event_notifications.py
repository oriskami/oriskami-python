import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase)

class UbivarAPIResourcesTests(UbivarTestCase):

    def test_event_notification_list(self):
        response = ubivar.EventNotification.list()
        print(response)
        self.assertTrue(len(response.data) == 3)
