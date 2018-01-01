import os
import oriskami
import warnings
from oriskami.test.helper import (OriskamiTestCase, NOW)

class OriskamiAPIResourcesTests(OriskamiTestCase):

    def test_router_flow_backup_create(self):
        response = oriskami.RouterFlowBackup.create(**{"name": NOW})
        self.assertTrue(hasattr(response, "data"))
        self.assertTrue(len(response.data) >= 1)
        backup = response.data[len(response.data)-1]
        self.assertTrue(hasattr(backup, "name"))
        self.assertTrue(hasattr(backup, "date"))
        self.assertTrue(hasattr(backup, "flows"))
        self.assertTrue(hasattr(backup, "data"))
        self.assertTrue(hasattr(backup, "parameters"))

    def test_router_flow_backup_retrieve(self):
        # init 
        response = oriskami.RouterFlow.list()
        for i in range(1, len(response.data)):
            response = oriskami.RouterFlow.delete(i)
            self.assertEqual(response.object, "router_flows")

        response = oriskami.RouterFlow.list()
        flowBeforeCreate = response.data 
        response = oriskami.RouterFlowBackup.create(**{"name": "Before create"})
        backupIdBeforeCreate = response.flow_backup_id

        oriskami.RouterFlow.create(**{"flow_template": "fraud-risk"})
        oriskami.RouterFlow.create(**{"flow_template": "fraud-risk"})
        oriskami.RouterFlow.create(**{"flow_template": "fraud-risk"})

        response = oriskami.RouterFlow.list()
        flowAfterCreate = response.data
        response = oriskami.RouterFlowBackup.create(**{"name": "After create"})
        backupIdAfterCreate = response.flow_backup_id

        oriskami.RouterFlowBackup.retrieve(backupIdBeforeCreate)
        response = oriskami.RouterFlow.list() 
        flowAfterRestore = response.data 
        
        response = oriskami.RouterFlowBackup.list() 
        for i in range(0, len(response.data)):
            response = oriskami.RouterFlowBackup.delete(i)
            self.assertEqual(response.object, "router_flow_backups")

        self.assertTrue(len(flowBeforeCreate), 1)
        self.assertTrue(len(flowAfterCreate ), 4)
        self.assertTrue(len(flowAfterRestore), 1)


    def test_router_flow_backup_delete(self):
        response = oriskami.RouterFlowBackup.list()
        for i in range(0, len(response.data)):
            response = oriskami.RouterFlowBackup.delete(i)
            self.assertEqual(response.object, "router_flow_backups")

    def test_router_flow_backup_list(self):
        response = oriskami.RouterFlowBackup.list()
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "router_flow_backups")
