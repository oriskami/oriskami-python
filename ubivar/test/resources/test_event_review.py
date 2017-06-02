import os
import ubivar
import warnings
from ubivar.test.helper import (UbivarTestCase)

class UbivarAPIResourcesTests(UbivarTestCase):

    def test_event_review_retrieve(self):
        response = ubivar.EventReview.retrieve("1")
        event = response.data[0]
        self.assertEqual(event["id"], "1")
        self.assertEqual(str(event.reviews[0].reviewer_id), "123")

        response = ubivar.EventReview.retrieve("2")
        event = response.data[0]
        self.assertEqual(event["id"], "2")
        self.assertEqual(str(event.reviews[0].reviewer_id), "124")
        self.assertEqual(str(event.reviews[1].reviewer_id), "125")

        response = ubivar.EventReview.retrieve("3")
        event = response.data[0]
        self.assertEqual(event["id"], "3")
        self.assertEqual(event.reviews, None)

    def test_event_review_update(self):
        eventId = "1"

        response = ubivar.EventReview.update(eventId, review_id=0, reviewer_id="124")
        self.assertEqual(response.data[0].id, eventId)
        self.assertEqual(str(response.data[0].reviews[0].reviewer_id), "124")

        response = ubivar.EventReview.update(eventId, review_id=0, reviewer_id="123")
        self.assertEqual(str(response.data[0].reviews[0].reviewer_id), "123")

    def test_event_review_delete(self):
        eventId = "1"

        response = ubivar.EventReview.delete(eventId, review_id=0)
        self.assertEqual(len(response.data[0].reviews), 0)

        response = ubivar.EventReview.update("1", reviewer_id="123", message="a review")
        self.assertEqual(len(response.data[0].reviews), 1)
        self.assertEqual(str(response.data[0].reviews[0].reviewer_id), "123")

    def test_event_review_list(self):
        response = ubivar.EventReview.list()
        self.assertTrue(len(response.data) == 3)
