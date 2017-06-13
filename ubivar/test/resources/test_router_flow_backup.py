import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase, NOW)

class UbivarAPIResourcesTests(UbivarTestCase):

    def test_router_flow_backup_create(self):
        response = ubivar.RouterFlowBackup.create(**{"name": NOW})
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
        response = ubivar.RouterFlow.list()
        for i in range(1, len(response.data)):
            response = ubivar.RouterFlow.delete(i)
            self.assertEqual(response.object, "router_flows")

        response = ubivar.RouterFlow.list()
        flowBeforeCreate = response.data 
        response = ubivar.RouterFlowBackup.create(**{"name": "Before create"})
        backupIdBeforeCreate = response.flow_backup_id

        ubivar.RouterFlow.create(**{"flow_template": "fraud-risk"})
        ubivar.RouterFlow.create(**{"flow_template": "fraud-risk"})
        ubivar.RouterFlow.create(**{"flow_template": "fraud-risk"})

        response = ubivar.RouterFlow.list()
        flowAfterCreate = response.data
        response = ubivar.RouterFlowBackup.create(**{"name": "After create"})
        backupIdAfterCreate = response.flow_backup_id

        ubivar.RouterFlowBackup.retrieve(backupIdBeforeCreate)
        response = ubivar.RouterFlow.list() 
        flowAfterRestore = response.data 
        
        response = ubivar.RouterFlowBackup.list() 
        for i in range(0, len(response.data)):
            response = ubivar.RouterFlowBackup.delete(i)
            self.assertEqual(response.object, "router_flow_backups")

        self.assertTrue(len(flowBeforeCreate), 1)
        self.assertTrue(len(flowAfterCreate ), 4)
        self.assertTrue(len(flowAfterRestore), 1)


    def test_router_flow_backup_delete(self):
        response = ubivar.RouterFlowBackup.list()
        for i in range(0, len(response.data)):
            response = ubivar.RouterFlowBackup.delete(i)
            self.assertEqual(response.object, "router_flow_backups")

    def test_router_flow_backup_list(self):
        response = ubivar.RouterFlowBackup.list()
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "router_flow_backups")
