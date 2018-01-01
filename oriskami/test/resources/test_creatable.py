import oriskami
from oriskami.test.helper import (
    OriskamiApiTestCase, MyCreatable
)


class CreateableAPIResourceTests(OriskamiApiTestCase):

    def test_create(self):
        self.mock_response({'object': 'events', 'foo': 'bar'})

        res = MyCreatable.create()

        self.requestor_mock.request.assert_called_with(
            'post', '/mycreatable', {})

        self.assertTrue(isinstance(res, oriskami.Event))
        self.assertEqual('bar', res.foo)
