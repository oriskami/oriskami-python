import os
import ubivar
from ubivar.test.helper import (UbivarTestCase)

def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            test_func(self, *args, **kwargs)
    return do_test

class ListResourcesTests(UbivarTestCase):


    @ignore_warnings
    def test_event_list(self):
        response = ubivar.Event.list()
        self.assertTrue(hasattr(response.data, "__iter__"))

    @ignore_warnings
    def test_filter_whitelist_list(self):
        response = ubivar.FilterWhitelist.list()
        self.assertTrue(hasattr(response.data, "__iter__"))

    @ignore_warnings
    def test_filter_blacklist_list(self):
        response = ubivar.FilterBlacklist.list()
        self.assertTrue(hasattr(response.data, "__iter__"))

    @ignore_warnings
    def test_filter_rules_custom_list(self):
        response = ubivar.FilterRulesCustom.list()
        self.assertTrue(hasattr(response.data, "__iter__"))

    @ignore_warnings
    def test_filter_rules_base_list(self):
        response = ubivar.FilterRulesBase.list()
        self.assertTrue(hasattr(response.data, "__iter__"))

    @ignore_warnings
    def test_filter_rules_ai_list(self):
        response = ubivar.FilterRulesAI.list()
        self.assertTrue(hasattr(response.data, "__iter__"))

    @ignore_warnings
    def test_filter_scorings_dedicated_list(self):
        response = ubivar.FilterScoringsDedicated.list()
        self.assertTrue(hasattr(response.data, "__iter__"))
