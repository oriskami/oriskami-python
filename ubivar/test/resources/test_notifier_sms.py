import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase, NOW)


DUMMY_SMS = {
        "description": "DUMMY SMS",
        "feature": "sms_domain",
        "is_active": "true",
        "value": "abc@gmail.com"
        }


class UbivarAPIResourcesTests(UbivarTestCase):

    def test_notifier_sms_create(self):
        response = ubivar.NotifierSms.create(**DUMMY_SMS)
        notifierSms = response.data[len(response.data)-1]
        self.assertTrue(hasattr(response, "data"))
        self.assertEqual(notifierSms["description"], DUMMY_SMS["description"])
        self.assertEqual(notifierSms["feature"]    , DUMMY_SMS["feature"])
        self.assertEqual(notifierSms["value"]      , DUMMY_SMS["value"])
        self.assertEqual(notifierSms["is_active"]  , DUMMY_SMS["is_active"])
        self.assertEqual(response.object, "notifier_sms")

    def test_notifier_sms_list(self):
        response = ubivar.NotifierSms.list()
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "notifier_sms")

    def test_notifier_sms_update(self):
        response = ubivar.NotifierSms.list()
        for i in range(0, len(response.data)):
            response = ubivar.NotifierSms.delete(str(i))
        response = ubivar.NotifierSms.create(**DUMMY_SMS)
        response = ubivar.NotifierSms.create(**DUMMY_SMS)

        newDescription = "new description"
        newValue = "new value"
        newStatus= "false"
        newFeature = "new feature"
        response = ubivar.NotifierSms.update("1", description=newDescription, 
                                                 value=newValue, is_active=newStatus,
                                                 feature=newFeature)
        notifierSms = response.data[len(response.data) - 1]
        self.assertEqual(notifierSms["description"], newDescription)
        self.assertEqual(notifierSms["value"], newValue)
        self.assertEqual(notifierSms["is_active"], newStatus)
        self.assertEqual(notifierSms["feature"], newFeature)
        self.assertEqual(response.object, "notifier_sms")

    def test_notifier_sms_delete(self):
        response = ubivar.NotifierSms.list()
        for i in range(0, len(response.data)):
            response = ubivar.NotifierSms.delete(str(i))
            self.assertEqual(response.object, "notifier_sms")
