import ubivar
from ubivar.test.helper import (
    UbivarApiTestCase, MyCreatable
)


class CreateableAPIResourceTests(UbivarApiTestCase):

    def test_create(self):
        self.mock_response({
            'object': 'charge',
            'foo': 'bar',
        })

        res = MyCreatable.create()

        self.requestor_mock.request.assert_called_with(
            'post', '/v1/mycreatables', {}, None)

        self.assertTrue(isinstance(res, ubivar.Charge))
        self.assertEqual('bar', res.foo)

    def test_idempotent_create(self):
        self.mock_response({
            'object': 'charge',
            'foo': 'bar',
        })

        res = MyCreatable.create(idempotency_key='foo')

        self.requestor_mock.request.assert_called_with(
            'post', '/v1/mycreatables', {}, {'Idempotency-Key': 'foo'})

        self.assertTrue(isinstance(res, ubivar.Charge))
        self.assertEqual('bar', res.foo)
