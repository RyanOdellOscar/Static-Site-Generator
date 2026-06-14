class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        return (
            isinstance(other, HTMLNode)
            and self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        node = ""
        if self.tag is not None:
            node = node + self.tag + " "
        if self.value is not None:
            node = node + self.value + " "
        if self.children is not None:
            node = node + self.tag + " "
        node += self.props_to_html()
        return node

    def to_html(self):
        raise NotImplementedError("Not implemented")

    def props_to_html(self):
        if self.props is None or self.props == {}:
            return ""
        
        attributes = ""
        for prop in self.props:
            attributes += f' {prop}="{self.props[prop]}"'
        return attributes

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        node = ""
        if self.tag is not None:
            node = node + self.tag + " "
        if self.value is not None:
            node = node + self.value + " "
        node += self.props_to_html()
        return node

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)


    def to_html(self):
        if self.tag is None:
            raise ValueError("parent must have tag")
        if self.children is None:
            raise ValueError("parent must have child node")
        
        node = f"<{self.tag}>"
        for child in self.children:
            node += child.to_html()
        return node + f"</{self.tag}>"