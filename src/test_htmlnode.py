import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="div", children=[], props={"class": "container"})
        node2 = HTMLNode(tag="div", children=[], props={"class": "container"})
        self.assertEqual(node, node2)
    
    def test_neq_different_tag(self):
        node = HTMLNode(tag="div", children=[], props={"class": "container"})
        node2 = HTMLNode(tag="span", children=[], props={"class": "container"})
        self.assertNotEqual(node, node2)
        
    def test_neq_different_children(self):
        node = HTMLNode(tag="div", children=[HTMLNode(tag="p")], props={"class": "container"})
        node2 = HTMLNode(tag="div", children=[HTMLNode(tag="span")], props={"class": "container"})
        self.assertNotEqual(node, node2)
        
    def test_neq_different_props(self):
        node = HTMLNode(tag="div", children=[], props={"class": "container"})
        node2 = HTMLNode(tag="div", children=[], props={"id": "main"})
        self.assertNotEqual(node, node2)

class TestLeafNode(unittest.TestCase):
    def test_to_html_with_tag_and_value(self):
        leaf = LeafNode(tag="p", value="Hello, World!", props={"class": "text"})
        expected_html = '<p class="text">Hello, World!</p>'
        self.assertEqual(leaf.to_html(), expected_html)
    
    def test_to_html_without_tag(self):
        leaf = LeafNode(tag=None, value="Just text", props={"class": "text"})
        expected_html = 'Just text'
        self.assertEqual(leaf.to_html(), expected_html)
    
    def test_to_html_without_value_raises(self):
        leaf = LeafNode(tag="p", value=None, props={"class": "text"})
        with self.assertRaises(ValueError):
            leaf.to_html()

    def test_eq_leafnode(self):
        leaf1 = LeafNode(tag="p", value="Hello", props={"class": "text"})
        leaf2 = LeafNode(tag="p", value="Hello", props={"class": "text"})
        self.assertEqual(leaf1, leaf2)
    
    def test_neq_leafnode_different_tag(self):
        leaf1 = LeafNode(tag="p", value="Hello", props={"class": "text"})
        leaf2 = LeafNode(tag="span", value="Hello", props={"class": "text"})
        self.assertNotEqual(leaf1, leaf2)
    
    def test_neq_leafnode_different_props(self):
        leaf1 = LeafNode(tag="p", value="Hello", props={"class": "text"})
        leaf2 = LeafNode(tag="p", value="Hello", props={"id": "main"})
        self.assertNotEqual(leaf1, leaf2)
    
    def test_neq_leafnode_different_value(self):
        leaf1 = LeafNode(tag="p", value="Hello", props={"class": "text"})
        leaf2 = LeafNode(tag="p", value="Hi", props={"class": "text"})
        self.assertNotEqual(leaf1, leaf2)
    
    def test_to_html_no_props(self):
        leaf = LeafNode(tag="p", value="No props")
        expected_html = '<p>No props</p>'
        self.assertEqual(leaf.to_html(), expected_html)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child1 = LeafNode(tag="span", value="Child 1", props={"class": "child"})
        child2 = LeafNode(tag="span", value="Child 2", props={"class": "child"})
        parent = ParentNode(tag="div", children=[child1, child2], props={"id": "parent"})
        expected_html = '<div id="parent"><span class="child">Child 1</span><span class="child">Child 2</span></div>'
        self.assertEqual(parent.to_html(), expected_html)
    
    def test_to_html_without_tag_raises(self):
        child = LeafNode(tag="span", value="Child", props={"class": "child"})
        parent = ParentNode(tag=None, children=[child], props={"id": "parent"})
        with self.assertRaises(ValueError):
            parent.to_html()
    
    def test_to_html_without_children_raises(self):
        parent = ParentNode(tag="div", children=None, props={"id": "parent"})
        with self.assertRaises(ValueError):
            parent.to_html()
    
    def test_to_html_with_empty_children_raises(self):
        parent = ParentNode(tag="div", children=[], props={"id": "parent"})
        with self.assertRaises(ValueError):
            parent.to_html()
    
    def test_props_to_html_none(self):
        node = HTMLNode(tag="div", children=[], props=None)
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_multiple(self):
        node = HTMLNode(tag="div", children=[], props={"class": "container", "id": "main"})
        props_html = node.props_to_html()
        self.assertIn(' class="container"', props_html)
        self.assertIn(' id="main"', props_html)
    
    def test_props_to_html_empty(self):
        node = HTMLNode(tag="div", children=[], props={})
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_single(self):
        node = HTMLNode(tag="div", children=[], props={"class": "container"})
        self.assertEqual(node.props_to_html(), ' class="container"')

    def test_eq(self):
        node = HTMLNode(tag="div", children=[], props={"class": "container"})
        node2 = HTMLNode(tag="div", children=[], props={"class": "container"})
        self.assertEqual(node, node2)
    
    def test_neq_different_tag(self):
        node = HTMLNode(tag="div", children=[], props={"class": "container"})
        node2 = HTMLNode(tag="span", children=[], props={"class": "container"})
        self.assertNotEqual(node, node2)

    def test_neq_different_children(self):
        node = HTMLNode(tag="div", children=[HTMLNode(tag="p")], props={"class": "container"})
        node2 = HTMLNode(tag="div", children=[HTMLNode(tag="span")], props={"class": "container"})
        self.assertNotEqual(node, node2)
    
    def test_neq_different_props(self):
        node = HTMLNode(tag="div", children=[], props={"class": "container"})
        node2 = HTMLNode(tag="div", children=[], props={"id": "main"})
        self.assertNotEqual(node, node2)
    
if __name__ == "__main__":
    unittest.main()
    