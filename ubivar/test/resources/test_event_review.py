import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase)

class UbivarAPIResourcesTests(UbivarTestCase):

    def test_event_review_retrieve(self):
        response = ubivar.EventReview.retrieve("1")
        reviews = response.data
        self.assertEqual(str(reviews[0].review.reviewer_id), "123")

        response = ubivar.EventReview.retrieve("2")
        reviews = response.data
        self.assertEqual(str(reviews[0].review.reviewer_id), "124")
        self.assertEqual(str(reviews[1].review.reviewer_id), "125")

        response = ubivar.EventReview.retrieve("3")
        reviews = response.data
        self.assertEqual(reviews, None)

    def test_event_review_update(self):
        eventId = "1"

        response = ubivar.EventReview.update(eventId, review_id=0, reviewer_id="124")
        self.assertEqual(str(response.data[0].review.reviewer_id), "124")

        response = ubivar.EventReview.update(eventId, review_id=0, reviewer_id="123")
        self.assertEqual(str(response.data[0].review.reviewer_id), "123")

    def test_event_review_delete(self):
        eventId = "1"

        response = ubivar.EventReview.delete(eventId, review_id=0)
        self.assertEqual(len(response.data), 0)

        response = ubivar.EventReview.update("1", reviewer_id="123", message="a review")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(str(response.data[0].review.reviewer_id), "123")

    def test_event_review_list(self):
        response = ubivar.EventReview.list()
        self.assertTrue(len(response.data) == 3)
