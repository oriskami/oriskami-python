import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase, NOW)


DUMMY_EMAIL = {
        "description": "DUMMY EMAIL",
        "is_active": "true",
        "value": "abc@gmail.com"
        }


class UbivarAPIResourcesTests(UbivarTestCase):

    def test_notifier_email_create(self):
        response = ubivar.NotifierEmail.create(**DUMMY_EMAIL)
        notifierEmail = response.data[len(response.data)-1]
        self.assertTrue(hasattr(response, "data"))
        self.assertEqual(notifierEmail["description"], DUMMY_EMAIL["description"])
        self.assertEqual(notifierEmail["value"]      , DUMMY_EMAIL["value"])
        self.assertEqual(notifierEmail["is_active"]  , DUMMY_EMAIL["is_active"])
        self.assertEqual(response.object, "notifier_emails")

    def test_notifier_email_retrieve(self):
        response = ubivar.NotifierEmail.retrieve("0")
        print(response)
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "notifier_emails")
        self.assertTrue(len(response.data))

    def test_notifier_email_list(self):
        response = ubivar.NotifierEmail.list()
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "notifier_emails")

    def test_notifier_email_update(self):
        response = ubivar.NotifierEmail.list()
        for i in range(0, len(response.data)):
            response = ubivar.NotifierEmail.delete(str(i))
        response = ubivar.NotifierEmail.create(**DUMMY_EMAIL)
        response = ubivar.NotifierEmail.create(**DUMMY_EMAIL)

        newDescription = "new description"
        newValue = "new value"
        newStatus= "false"
        response = ubivar.NotifierEmail.update("1", description=newDescription, 
                                                 value=newValue, is_active=newStatus)
        notifierEmail = response.data[len(response.data) - 1]
        self.assertEqual(notifierEmail["description"], newDescription)
        self.assertEqual(notifierEmail["value"], newValue)
        self.assertEqual(notifierEmail["is_active"], newStatus)
        self.assertEqual(response.object, "notifier_emails")

    def test_notifier_email_delete(self):
        response = ubivar.NotifierEmail.list()
        for i in range(0, len(response.data)):
            response = ubivar.NotifierEmail.delete(str(i))
            self.assertEqual(response.object, "notifier_emails")
