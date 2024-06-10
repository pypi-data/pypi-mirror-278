import unittest
import io
from zenaura.client.page import Page 
from .mocks.counter_mocks import Counter
from zenaura.client.hydrator import HydratorCompilerAdapter
from zenaura.server.server import ZenauraServer, template
from zenaura.client.app import App 
from unittest.mock import MagicMock, patch


class TestZenauraServer(unittest.TestCase):

    def setUp(self):
        from zenaura.client.app import HistoryNode, PageHistory, NotFound, App, Route
        from .mocks.counter_mocks import Counter
        from .mocks.browser_mocks import MockDocument, MockWindow
        self.page = Page([Counter([])])
        self.page.id = 'test-page-id'
        self.page_content = '<div>Test Page Content</div>'
        self.compiler_adapter = HydratorCompilerAdapter()
        self.maxDiff = None
        self.middleware = MagicMock()
        self.page = Page([Counter([])])
        self.route = Route("test", "/test", self.page, self.middleware) 
        self.route_home = Route("test3", "/", self.page, self.middleware) 
        self.route2 = Route("test2", "/2", self.page, self.middleware) 
        self.new_route = Route
        self.router = App()
        self.router.add_route(self.route)
        self.router.add_route(self.route_home)
        self.router.add_route(self.route2)

        self.history_node = HistoryNode
        self.page_history = PageHistory
        self.not_found = NotFound()
        self.document = MockDocument()
        self.window = MockWindow()
        self.dom_patcher = patch("zenaura.client.app.document", self.document)
        self.dom_patcher.start()
        self.window_patcher = patch("zenaura.client.app.window", self.window)
        self.window_patcher.start()

        self.router_without_home = App()
        self.router_without_home.add_route(self.route)
        self.router_without_home.add_route(self.route2)
        
        global compiler_adapter
        compiler_adapter = self.compiler_adapter  # Mocking the global instance
        
        self.template_content = template

    def tearDown(self):
        self.dom_patcher.stop()
        self.window_patcher.stop()

    def test_hydrate_page(self):
        result = ZenauraServer.hydrate_page(self.page)
        self.assertEqual(result, self.template_content(self.compiler_adapter.hyd_comp_compile_page(self.page), title="zenaura", meta_description="this app created with zenaura", icon="./public/favicon.ico", pydide="https://pyscript.net/releases/2024.1.1/core.js"))

    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_hydrate_app_home_defined(self, mock_open):
        result = ZenauraServer.hydrate_app(self.router)
        
        # / path is not hidden
        self.assertIn(
            '<div data-zenaura="f933743a">',
            result, 
        )
        # rest are hidden
        self.assertIn(
            '<div hidden data-zenaura="f933743a">',
            result, 
        )
        self.assertIn(
            '<div hidden data-zenaura="f933743a">',
            result, 
        )
    
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_hydrate_app_home_not_defined_first_in_stack_shown(self, mock_open):
        result = ZenauraServer.hydrate_app(self.router)
        
        print(result)
        # / path is not hidden
        self.assertIn(
            '<div hidden data-zenaura="79627492">',
            result, 
        )
        # rest are hidden
        self.assertIn(
            '<div hidden data-zenaura="79627492">',
            result, 
        )

if __name__ == '__main__':
    unittest.main()
