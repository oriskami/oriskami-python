import os
import oriskami
import warnings
from oriskami.test.helper import (OriskamiTestCase)

DUMMY_RULES_AI = {
        "feature": "a_rule_feature",
        "value": "a_rule_value.com",
        "is_active": "false"
        }


class OriskamiAPIResourcesTests(OriskamiTestCase):

    def test_filter_rules_ai_list(self):
        response = oriskami.FilterRulesAI.list()

        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "filter_rules_ai")

    def test_filter_rules_ai_update(self):
        response = oriskami.FilterRulesAI.list()
        originalRulesAI = response.data[1]

        response = oriskami.FilterRulesAI.update("1", **DUMMY_RULES_AI)
        filterRulesAI = response.data[1]
        self.assertEqual(filterRulesAI["value"]    , originalRulesAI["value"])
        self.assertEqual(filterRulesAI["feature"]  , originalRulesAI["feature"])
        self.assertEqual(filterRulesAI["is_active"], DUMMY_RULES_AI["is_active"])

        response = oriskami.FilterRulesAI.update("1", is_active="true")
        filterRulesAI = response.data[1]
        self.assertEqual(filterRulesAI["is_active"]   , "true")
        self.assertEqual(response.object, "filter_rules_ai")
