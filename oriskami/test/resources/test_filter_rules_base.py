import os
import oriskami
import warnings
from oriskami.test.helper import (OriskamiTestCase)

DUMMY_RULES_BASE = {
        "description": "a_rule_description",
        "feature": "a_rule_feature",
        "value": "1 Days",
        "is_active": "false"
        }


class OriskamiAPIResourcesTests(OriskamiTestCase):

    def test_filter_rules_base_list(self):
        response = oriskami.FilterRulesBase.list()

        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertEqual(response.object, "filter_rules_base")

    def test_filter_rules_base_update(self):
        response = oriskami.FilterRulesBase.list()
        originalRulesBase = response.data[0]

        response = oriskami.FilterRulesBase.update("0", **DUMMY_RULES_BASE)
        filterRulesBase = response.data[0]
        self.assertEqual(filterRulesBase["feature"]     , originalRulesBase["feature"])
        self.assertEqual(filterRulesBase["value"]       , DUMMY_RULES_BASE["value"])
        self.assertEqual(filterRulesBase["is_active"]   , DUMMY_RULES_BASE["is_active"])

        self.assertRaises(oriskami.error.APIError, oriskami.FilterRulesBase.update, "0", value="new value")

        response = oriskami.FilterRulesBase.update("0", value="1 Months")
        self.assertEqual(response.object, "filter_rules_base")
