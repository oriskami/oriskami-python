import os
import oriskami
import warnings
from oriskami.test.helper import (OriskamiTestCase, NOW)

class OriskamiAPIResourcesTests(OriskamiTestCase):

    def test_router_flow_create(self):
        response = oriskami.RouterFlow.create(**{"flow_template": "fraud-risk"})
        routerFlow = response.data[len(response.data)-1]
        self.assertTrue(hasattr(response, "data"))
        self.assertTrue(len(response.data) >= 1)

    def test_router_flow_update(self):
        response = oriskami.RouterFlow.list()

        for i in range(1, len(response.data)):
            response = oriskami.RouterFlow.delete(str(i))

        response = oriskami.RouterFlow.create(**{"flow_template": "fraud-risk"})
        response = oriskami.RouterFlow.create(**{"flow_template": "fraud-risk"})

        oriskami.RouterFlow.update("1", is_active="false")
        response = oriskami.RouterFlow.list()
        self.assertEqual(response.data[1]["is_active"], "false")

        oriskami.RouterFlow.update("1", is_active="true")
        response = oriskami.RouterFlow.list()
        self.assertEqual(response.data[1]["is_active"], "true")

    def test_router_flow_delete(self):
        response = oriskami.RouterFlow.list()

        for i in range(1, len(response.data)):
            response = oriskami.RouterFlow.delete(str(i))
            self.assertEqual(response.object, "router_flows")

    def test_router_flow_list(self):
        response = oriskami.RouterFlow.list()
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "router_flows")
