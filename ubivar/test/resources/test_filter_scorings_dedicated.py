import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase)

DUMMY_DEDICATED_SCORINGS = {
        "score_id": "124",
        "is_active": "false"
        }


class UbivarAPIResourcesTests(UbivarTestCase):

    def test_filter_scorings_dedicated_list(self):
        response = ubivar.FilterScoringsDedicated.list()

        self.assertTrue(hasattr(response.data, "__iter__"))
        self.assertTrue(response.object == "filter_scorings_dedicated")

    def test_filter_scorings_dedicated_update(self):
        response = ubivar.FilterScoringsDedicated.list()
        originalScoringsDedicated = response.data[0]

        response = ubivar.FilterScoringsDedicated.update("0", **DUMMY_DEDICATED_SCORINGS)
        filterScoringsDedicated = response.data[0]
        self.assertEqual(filterScoringsDedicated["score_id"] , DUMMY_DEDICATED_SCORINGS["score_id"])
        self.assertEqual(filterScoringsDedicated["is_active"], DUMMY_DEDICATED_SCORINGS["is_active"])

        response = ubivar.FilterScoringsDedicated.update("0", is_active="true", score_id="123")
        filterScoringsDedicated = response.data[0]
        self.assertEqual(filterScoringsDedicated["is_active"]   , "true")
        self.assertEqual(response.object, "filter_scorings_dedicated")
