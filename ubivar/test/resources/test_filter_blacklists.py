import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase)

DUMMY_BLACKLIST = {
        "feature": "a_rule_feature",
        "value": "a_rule_value.com",
        "is_active": "false"
        }


class UbivarAPIResourcesTests(UbivarTestCase):

    def test_filter_blacklist_list(self):
        response = ubivar.FilterBlacklist.list()

        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "filter_blacklists")

    def test_filter_blacklist_update(self):
        response = ubivar.FilterBlacklist.list()
        originalBlacklist = response.data[1]

        response = ubivar.FilterBlacklist.update("1", **DUMMY_BLACKLIST)
        filterBlacklist = response.data[1]
        self.assertEqual(filterBlacklist["value"]       , originalBlacklist["value"])
        self.assertEqual(filterBlacklist["feature"]     , originalBlacklist["feature"])
        self.assertEqual(filterBlacklist["is_active"]   , DUMMY_BLACKLIST["is_active"])

        response = ubivar.FilterBlacklist.update("1", is_active="true")
        filterBlacklist = response.data[1]
        self.assertEqual(filterBlacklist["is_active"]   , "true")
        self.assertEqual(response.object, "filter_blacklists")
