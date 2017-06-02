import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase, NOW)


DUMMY_WEBHOOK = {
        "description": "DUMMY WEBHOOK",
        "value": "http://a-webhook-url",
        "is_active": "true"
        }


class UbivarAPIResourcesTests(UbivarTestCase):

    def test_notifier_webhook_create(self):
        response = ubivar.NotifierWebhook.create(**DUMMY_WEBHOOK)
        notifierWebhook = response.data[len(response.data)-1]
        self.assertTrue(hasattr(response, "data"))
        self.assertEqual(notifierWebhook["description"], DUMMY_WEBHOOK["description"])
        self.assertEqual(notifierWebhook["value"]      , DUMMY_WEBHOOK["value"])
        self.assertEqual(notifierWebhook["is_active"]  , DUMMY_WEBHOOK["is_active"])
        self.assertEqual(response.object, "notifier_webhooks")

    def test_notifier_webhook_list(self):
        response = ubivar.NotifierWebhook.list()
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "notifier_webhooks")

    def test_notifier_webhook_update(self):
        response = ubivar.NotifierWebhook.list()
        for i in range(0, len(response.data)):
            response = ubivar.NotifierWebhook.delete(str(i))
        response = ubivar.NotifierWebhook.create(**DUMMY_WEBHOOK)
        response = ubivar.NotifierWebhook.create(**DUMMY_WEBHOOK)

        newDescription = "new description"
        newValue = "new value"
        newStatus= "false"
        response = ubivar.NotifierWebhook.update("1", description=newDescription, 
                                                 value=newValue, is_active=newStatus)
        notifierWebhook = response.data[len(response.data) - 1]
        self.assertEqual(notifierWebhook["description"], newDescription)
        self.assertEqual(notifierWebhook["value"], newValue)
        self.assertEqual(notifierWebhook["is_active"], newStatus)
        self.assertEqual(response.object, "notifier_webhooks")

    def test_notifier_webhook_delete(self):
        response = ubivar.NotifierWebhook.list()
        for i in range(0, len(response.data)):
            response = ubivar.NotifierWebhook.delete(str(i))
            self.assertEqual(response.object, "notifier_webhooks")
