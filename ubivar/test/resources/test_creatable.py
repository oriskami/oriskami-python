import ubivar
from ubivar.test.helper import (
    UbivarApiTestCase, MyCreatable
)


class CreateableAPIResourceTests(UbivarApiTestCase):

    def test_create(self):
        self.mock_response({'object': 'events', 'foo': 'bar'})

        res = MyCreatable.create()

        self.requestor_mock.request.assert_called_with(
            'post', '/mycreatable', {})

        self.assertTrue(isinstance(res, ubivar.Event))
        self.assertEqual('bar', res.foo)
