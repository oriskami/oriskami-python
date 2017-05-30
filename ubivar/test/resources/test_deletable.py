from ubivar.test.helper import (
    UbivarApiTestCase, MyDeletable
)


class DeletableAPIResourceTests(UbivarApiTestCase):

    def test_delete(self):
        self.mock_response({'id': 'mid', 'deleted': True})

        obj = MyDeletable.construct_from({'resource_id': 'mid'}, 'mykey')
        obj = obj.delete(resource_id='mid')

        self.assertEqual(True, obj.deleted)
        self.assertEqual('mid', obj.id)
