import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode



class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        nodedict = {
            "href": "https://www.google.com",
            "target": "_blank",
        }           
        node = HTMLNode("test_tag", "test_value", ["child1", "child2"], nodedict )
        node2 = HTMLNode("test_tag", "test_value", ["child1", "child2"], nodedict )
        self.assertEqual(node, node2)

    def test_null(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node, node2)

    def test_missing(self):
        node = HTMLNode(value="test_value")
        node2 = HTMLNode(value="test_value")
        self.assertEqual(node, node2)

    def test_unequal(self):
        nodedict = {
            "href": "https://www.google.com",
            "target": "_blank",
        }           
        nodedict2 = {
            "href": "https://www.google.com",
            "target": "_blank",
            "arg3": "stuff"
        }           
        node = HTMLNode("test_tag", "test_value", ["child1", "child2"], nodedict )
        node2 = HTMLNode("test_tag", "test_value", ["child1", "child2"], nodedict2 )
        self.assertNotEqual(node, node2)

    def test_props(self):
        nodedict = {
            "href": "https://www.google.com",
            "target": "_blank",
        }                  
        node = HTMLNode("test_tag", "test_value", ["child1", "child2"], nodedict )

        self.assertEqual(node.props_to_html(),' href="https://www.google.com" target="_blank"')

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_missing_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_missing_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>child2</span></div>")

    def test_parent_missing_children(self):
        node = ParentNode("b", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_missing_tag(self):
        child_node = LeafNode("span", "child")
        node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            node.to_html()




if __name__ == "__main__":
    unittest.main()