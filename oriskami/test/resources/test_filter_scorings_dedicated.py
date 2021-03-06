import os
import oriskami
import warnings
from oriskami.test.helper import (OriskamiTestCase)

DUMMY_DEDICATED_SCORINGS = {
        "score_id": "124",
        "is_active": "false"
        }


class OriskamiAPIResourcesTests(OriskamiTestCase):

    def test_filter_scorings_dedicated_list(self):
        response = oriskami.FilterScoringsDedicated.list()

        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "filter_scorings_dedicated")

    def test_filter_scorings_dedicated_update(self):
        response = oriskami.FilterScoringsDedicated.update("0", **DUMMY_DEDICATED_SCORINGS)
        filterScoringsDedicated = response.data[0]
        self.assertEqual(filterScoringsDedicated["score_id"] , DUMMY_DEDICATED_SCORINGS["score_id"])
        self.assertEqual(filterScoringsDedicated["is_active"], DUMMY_DEDICATED_SCORINGS["is_active"])

        response = oriskami.FilterScoringsDedicated.update("0", is_active="true", score_id="123")
        filterScoringsDedicated = response.data[0]
        self.assertEqual(filterScoringsDedicated["is_active"]   , "true")
        self.assertEqual(response.object, "filter_scorings_dedicated")
