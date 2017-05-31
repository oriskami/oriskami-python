import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase)

class UbivarAPIResourcesTests(UbivarTestCase):

    def test_event_last_id_list(self):
        response = ubivar.EventLastId.list()
        self.assertEqual(len(response.data), 1)
        lastId = response.data[0]["id"]
        self.assertEqual(lastId, 3)
