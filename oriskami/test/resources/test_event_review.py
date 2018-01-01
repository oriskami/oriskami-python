import os
import oriskami
import warnings
from oriskami.test.helper import (OriskamiTestCase)

class OriskamiAPIResourcesTests(OriskamiTestCase):

    def test_event_review_retrieve(self):
        response = oriskami.EventReview.retrieve("1")
        reviews = response.data
        self.assertEqual(str(reviews[0].review.reviewer_id), "123")

        response = oriskami.EventReview.retrieve("2")
        reviews = response.data
        self.assertEqual(str(reviews[0].review.reviewer_id), "124")
        self.assertEqual(str(reviews[1].review.reviewer_id), "125")

        response = oriskami.EventReview.retrieve("3")
        reviews = response.data
        self.assertEqual(reviews, None)

    def test_event_review_update(self):
        eventId = "1"

        response = oriskami.EventReview.update(eventId, review_id=0, reviewer_id="124")
        self.assertEqual(str(response.data[0].review.reviewer_id), "124")

        response = oriskami.EventReview.update(eventId, review_id=0, reviewer_id="123")
        self.assertEqual(str(response.data[0].review.reviewer_id), "123")

    def test_event_review_delete(self):
        eventId = "1"

        response = oriskami.EventReview.delete(eventId, review_id=0)
        self.assertEqual(len(response.data), 0)

        response = oriskami.EventReview.update("1", reviewer_id="123", message="a review")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(str(response.data[0].review.reviewer_id), "123")

    def test_event_review_list(self):
        response = oriskami.EventReview.list()
        self.assertTrue(len(response.data) == 3)
