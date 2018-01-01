import os
import oriskami
import warnings
from oriskami.test.helper import (OriskamiTestCase, NOW)


DUMMY_SLACK = {
        "description": "DUMMY SLACK",
        "is_active": "true",
        "value": "https://a-slack-url"
        }


class OriskamiAPIResourcesTests(OriskamiTestCase):

    def test_notifier_slack_create(self):
        response = oriskami.NotifierSlack.create(**DUMMY_SLACK)
        notifierSlack = response.data[len(response.data)-1]
        self.assertTrue(hasattr(response, "data"))
        self.assertEqual(notifierSlack["description"], DUMMY_SLACK["description"])
        self.assertEqual(notifierSlack["value"]      , DUMMY_SLACK["value"])
        self.assertEqual(notifierSlack["is_active"]  , DUMMY_SLACK["is_active"])
        self.assertEqual(response.object, "notifier_slack")

    def test_notifier_slack_list(self):
        response = oriskami.NotifierSlack.list()
        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "notifier_slack")

    def test_notifier_slack_update(self):
        response = oriskami.NotifierSlack.list()
        for i in range(0, len(response.data)):
            response = oriskami.NotifierSlack.delete(str(i))
        response = oriskami.NotifierSlack.create(**DUMMY_SLACK)
        response = oriskami.NotifierSlack.create(**DUMMY_SLACK)

        newDescription = "new description"
        newValue = "new value"
        newStatus= "false"
        response = oriskami.NotifierSlack.update("1", description=newDescription, 
                                                 value=newValue, is_active=newStatus)
        notifierSlack = response.data[len(response.data) - 1]
        self.assertEqual(notifierSlack["description"], newDescription)
        self.assertEqual(notifierSlack["value"], newValue)
        self.assertEqual(notifierSlack["is_active"], newStatus)
        self.assertEqual(response.object, "notifier_slack")

    def test_notifier_slack_delete(self):
        response = oriskami.NotifierSlack.list()
        for i in range(0, len(response.data)):
            response = oriskami.NotifierSlack.delete(str(i))
            self.assertEqual(response.object, "notifier_slack")
