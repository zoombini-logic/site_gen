
class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return_string = ""
        if self.props == None:
            return ""
        for key in self.props:
            return_string = return_string + ' ' + key + '="' + self.props[key] + '"'
        return return_string
    
    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        return False

    def __repr__(self):
        return f"HTMLNode: tag-{self.tag} value-{self.value} children-{self.children} props={self.props}"

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        
        html_string = f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        return html_string

    def __repr__(self):
        return f"LeafNode: tag-{self.tag} value-{self.value} props={self.props}"
    
class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)


    def to_html(self):
        if self.tag is None:
            raise ValueError ("No Tag")
        if self.children is None:
            raise ValueError ("Children missing value")


        html_string = f'<{self.tag}{self.props_to_html()}>'
        for node in self.children:
            html_string = html_string + node.to_html()
        html_string = html_string + f'</{self.tag}>'
        return html_string


