import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase)

DUMMY_RULES_BASE = {
        "description": "a_rule_description",
        "feature": "a_rule_feature",
        "value": "1 Days",
        "is_active": "false"
        }


class UbivarAPIResourcesTests(UbivarTestCase):

    def test_filter_rules_base_list(self):
        response = ubivar.FilterRulesBase.list()

        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertEqual(response.object, "filter_rules_base")

    def test_filter_rules_base_update(self):
        response = ubivar.FilterRulesBase.list()
        originalRulesBase = response.data[0]

        response = ubivar.FilterRulesBase.update("0", **DUMMY_RULES_BASE)
        filterRulesBase = response.data[0]
        self.assertEqual(filterRulesBase["feature"]     , originalRulesBase["feature"])
        self.assertEqual(filterRulesBase["value"]       , DUMMY_RULES_BASE["value"])
        self.assertEqual(filterRulesBase["is_active"]   , DUMMY_RULES_BASE["is_active"])

        self.assertRaises(ubivar.error.APIError, ubivar.FilterRulesBase.update, "0", value="new value")

        response = ubivar.FilterRulesBase.update("0", value="1 Months")
        self.assertEqual(response.object, "filter_rules_base")
