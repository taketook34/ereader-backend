from .test_setup import TestSetUP

class TestViews(TestSetUP):
    def test_user_can_watch(self):
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, 200)

