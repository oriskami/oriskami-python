from oriskami.test.helper import (OriskamiApiTestCase, MyUpdatable)


class UpdateableAPIResourceTests(OriskamiApiTestCase):

    def setUp(self):
        super(UpdateableAPIResourceTests, self).setUp()

        self.mock_response({'thats': 'it'})

        self.obj = MyUpdatable.construct_from({
            'id': 'myid',
            'foo': 'bar',
            'baz': 'boz',
            'metadata': {
                'size': 'l',
                'score': 4,
                'height': 10
            }
        }, 'mykey')

