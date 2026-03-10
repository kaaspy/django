#!/usr/bin/python3

class Text(str):
    """
    A Text class to represent a text you could use with your HTML elements.

    Because directly using str class was too mainstream.
    """

    def __str__(self):
        """
        Do you really need a comment to understand this method?..
        """
        return (super().__str__()
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace('\n', '\n<br />\n'))

class Elem:
    """
    Elem will permit us to represent our HTML elements.
    """
    [...]

    def __init__(self, tag='div', attr={}, content=None, tag_type='double', indent=0):
        """
        __init__() method.

        Obviously.
        """
        if not Elem.check_type(content) and not content == None:
            raise Elem.ValidationError

        self.tag = tag
        self.attr = attr
        self.content = content
        self.tag_type = tag_type
        self.indent = indent

    def __str__(self):
        """
        The __str__() method will permit us to make a plain HTML representation
        of our elements.
        Make sure it renders everything (tag, attributes, embedded
        elements...).
        """
        result = f"<{self.tag}"
        if len(self.attr):
            result += self.__make_attr()
        if self.tag_type == 'double':
            result += ">"
        if self.content:
            self.indent += 1
            try:
                iter(self.content)
            except:
                self.content = [self.content,]
            if type(self.content) == list:
                self.content = list(filter(lambda elem: elem != Text(""), self.content))
            result += self.__make_content()
        self.indent -= 1
        if self.tag_type == 'double':
            if self.content:
                result += "  " * self.indent
            result += f"</{self.tag}>"
        elif self.tag_type == 'simple':
            result += " />"

        return result

    def __make_attr(self):
        """
        Here is a function to render our elements attributes.
        """
        result = ''
        for pair in sorted(self.attr.items()):
            result += ' ' + str(pair[0]) + '="' + str(pair[1]) + '"'
        return result

    def __make_content(self):
        """
        Here is a method to render the content, including embedded elements.
        """

        if len(self.content) == 0:
            return ''
        result = '\n'

        if isinstance(self.content, Text):
            result += "  " * self.indent + str(self.content) + "\n" 
            return result

        for elem in self.content:
            if isinstance(elem, Elem):
                elem.indent = self.indent
            result += "  " * self.indent + str(elem) + "\n" 
        return result

    def add_content(self, content):
        if self.content == None:
            self.content = []
        if not Elem.check_type(content):
            raise Elem.ValidationError
        if type(content) == list:
            self.content += [elem for elem in content if elem != Text('')]
        elif content != Text(''):
            self.content.append(content)

    @staticmethod
    def check_type(content):
        """
        Is this object a HTML-compatible Text instance or a Elem, or even a
        list of both?
        """
        return (isinstance(content, Elem) or type(content) == Text or
                (type(content) == list and all([type(elem) == Text or
                                                isinstance(elem, Elem)
                                                for elem in content])))
    class ValidationError(Exception):
        def __init__(self):
            super().__init__
