import os
import oriskami
import warnings
from oriskami.test.helper import (OriskamiTestCase, NOW)


DUMMY_SMS = {
        "description": "DUMMY SMS",
        "value": "+1 123 123 123",
        "is_active": "true"
        }


class OriskamiAPIResourcesTests(OriskamiTestCase):

    def test_notifier_sms_create(self):
        response = oriskami.NotifierSms.create(**DUMMY_SMS)
        notifierSms = response.data[len(response.data)-1]
        self.assertTrue(hasattr(response, "data"))
        self.assertEqual(notifierSms["description"], DUMMY_SMS["description"])
        self.assertEqual(notifierSms["value"]      , DUMMY_SMS["value"])
        self.assertEqual(notifierSms["is_active"]  , DUMMY_SMS["is_active"])
        self.assertEqual(response.object, "notifier_sms")

    def test_notifier_sms_retrieve(self):
        response = oriskami.NotifierSms.retrieve("0")
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "notifier_sms")
        self.assertTrue(len(response.data))

    def test_notifier_sms_list(self):
        response = oriskami.NotifierSms.list()
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "notifier_sms")

    def test_notifier_sms_update(self):
        response = oriskami.NotifierSms.list()
        for i in range(0, len(response.data)):
            response = oriskami.NotifierSms.delete(str(i))
        response = oriskami.NotifierSms.create(**DUMMY_SMS)
        response = oriskami.NotifierSms.create(**DUMMY_SMS)

        newDescription = "new description"
        newValue = "new value"
        newStatus= "false"
        response = oriskami.NotifierSms.update("1", description=newDescription, 
                                                 value=newValue, is_active=newStatus)
        notifierSms = response.data[len(response.data) - 1]
        self.assertEqual(notifierSms["description"], newDescription)
        self.assertEqual(notifierSms["value"], newValue)
        self.assertEqual(notifierSms["is_active"], newStatus)
        self.assertEqual(response.object, "notifier_sms")

    def test_notifier_sms_delete(self):
        response = oriskami.NotifierSms.list()
        for i in range(0, len(response.data)):
            response = oriskami.NotifierSms.delete(str(i))
            self.assertEqual(response.object, "notifier_sms")
