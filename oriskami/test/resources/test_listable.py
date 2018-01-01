import oriskami
from oriskami.test.helper import (
    OriskamiApiTestCase, MyListable
)


class ListableAPIResourceTests(OriskamiApiTestCase):

    def test_all(self):
        self.mock_response({
            'object': 'events',
            'data': [
                {
                    'object': 'events',
                    'name': 'jose',
                },
                {
                    'object': 'events',
                    'name': 'curly',
                }
            ],
            'url': '/events',
            'has_more': False,
        })

        res = MyListable.list()

        self.requestor_mock.request.assert_called_with(
            'get', '/mylistable', {})

        self.assertEqual(2, len(res.data))
        self.assertTrue(all(isinstance(obj, oriskami.Event)
                            for obj in res.data))
        self.assertEqual('jose', res.data[0].name)
        self.assertEqual('curly', res.data[1].name)
