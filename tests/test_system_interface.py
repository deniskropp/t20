import unittest
from t20.core.system_interface import SystemInterfaceLayer
from t20.lang.spec import ActionType

class TestSystemInterfaceLayer(unittest.TestCase):
    def setUp(self):
        self.interface = SystemInterfaceLayer()

    def test_map_analyze(self):
        # "GENERATE INSIGHTS FROM" -> ANALYZE
        action = self.interface.e("REASONING", "GENERATE INSIGHTS FROM <1>", "<1>: some data")
        self.assertEqual(action.verb, ActionType.ANALYZE)
        self.assertEqual(action.target, "<1>")
        self.assertEqual(action.parameters["context_refs"], "<1>: some data")

    def test_map_create(self):
        # "CREATE NEW NODE" -> CREATE
        action = self.interface.e("KNOWLEDGE", "CREATE NEW NODE FOR Entity", None)
        self.assertEqual(action.verb, ActionType.CREATE)
        self.assertIn("Entity", action.target)

    def test_map_query(self):
        # "FIND ALL USERS" -> QUERY
        action = self.interface.e("KNOWLEDGE", "FIND ALL USERS", None)
        self.assertEqual(action.verb, ActionType.QUERY)
        
    def test_map_query_fallback(self):
            # Unknown verb -> QUERY (default)
            action = self.interface.e("UNKNOWN", "SOMETHING ELSE", None)
            self.assertEqual(action.verb, ActionType.QUERY)

if __name__ == '__main__':
    unittest.main()
