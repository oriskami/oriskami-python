import os
import oriskami
import warnings
from oriskami.test.helper import (OriskamiTestCase)

class OriskamiAPIResourcesTests(OriskamiTestCase):

    def test_event_last_id_list(self):
        response = oriskami.EventLastId.list()
        self.assertEqual(len(response.data), 1)
        lastId = response.data[0]["id"]
        self.assertEqual(str(lastId), str(3))
