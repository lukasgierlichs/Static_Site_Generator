from enum import Enum

class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
        
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return NotImplemented
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)
    
    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        props_str = ""
        for key, value in self.props.items():
            props_str += f' {key}="{value}"'
        return props_str
    
    
    def __repr__(self):
        return f"HTMLNode({self.tag!r}, {self.children!r}, {self.props!r})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value to convert to HTML")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag!r}, {self.value!r}, {self.props!r})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag to convert to HTML")
        if not self.children:
            raise ValueError("ParentNode must have children to convert to HTML")
        return f"<{self.tag}{self.props_to_html()}>" + "".join(child.to_html() for child in self.children) + f"</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag!r}, {self.children!r}, {self.props!r})"