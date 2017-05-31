import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase)

class UbivarAPIResourcesTests(UbivarTestCase):

    def test_filter_whitelist_list(self):
        response = ubivar.FilterWhitelist.list()
        self.assertTrue(hasattr(response.data, "__iter__"))

    def test_filter_blacklist_list(self):
        response = ubivar.FilterBlacklist.list()
        self.assertTrue(hasattr(response.data, "__iter__"))

    def test_filter_rules_custom_list(self):
        response = ubivar.FilterRulesCustom.list()
        self.assertTrue(hasattr(response.data, "__iter__"))

    def test_filter_rules_base_list(self):
        response = ubivar.FilterRulesBase.list()
        self.assertTrue(hasattr(response.data, "__iter__"))

    def test_filter_rules_ai_list(self):
        response = ubivar.FilterRulesAI.list()
        self.assertTrue(hasattr(response.data, "__iter__"))

    def test_filter_scorings_dedicated_list(self):
        response = ubivar.FilterScoringsDedicated.list()
        self.assertTrue(hasattr(response.data, "__iter__"))

    def test_notifier_emails_list(self):
        response = ubivar.NotifierEmail.list()
        self.assertTrue(hasattr(response.data, "__iter__"))

    def test_notifier_sms_list(self):
        response = ubivar.NotifierSms.list()
        self.assertTrue(hasattr(response.data, "__iter__"))

    def test_notifier_webhook_list(self):
        response = ubivar.NotifierWebhook.list()
        self.assertTrue(hasattr(response.data, "__iter__"))

    def test_notifier_ecommerce_list(self):
        response = ubivar.NotifierECommerce.list()
        self.assertTrue(hasattr(response.data, "__iter__"))

    def test_notifier_slack_list(self):
        response = ubivar.NotifierSlack.list()
        self.assertTrue(hasattr(response.data, "__iter__"))


