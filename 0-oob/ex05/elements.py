#!/usr/bin/python3

from elem import Text, Elem

class Html(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="html", content=content, attr=attr)

class Head(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="head", content=content, attr=attr)

class Body(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="body", content=content, attr=attr)

class Meta(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="meta", tag_type="simple", content=content, attr=attr)

class Img(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="img", tag_type="simple", content=content, attr=attr)

class Table(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="table", content=content, attr=attr)

class Th(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="th", content=content, attr=attr)

class Tr(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="tr", content=content, attr=attr)

class Td(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="td", content=content, attr=attr)

class Ul(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="ul", content=content, attr=attr)

class Ol(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="ol", content=content, attr=attr)

class Li(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="li", content=content, attr=attr)

class H1(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="h1", content=content, attr=attr)

class H2(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="h2", content=content, attr=attr)

class P(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="p", content=content, attr=attr)

class Div(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="div", content=content, attr=attr)

class Span(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="span", content=content, attr=attr)

class Hr(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="hr", tag_type="simple", content=content, attr=attr)

class Br(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="br", tag_type="simple", content=content, attr=attr)

class Title(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__(tag="title", content=content, attr=attr)

if __name__ == '__main__':
    basic_test = Html([Meta(attr={"charset" : "UTF-8"}), 
                  Head([Title(Text("Titre"))]),
                  Body([Div(Text("div"))])])
                
    table_test = Html([Meta(attr={"charset" : "UTF-8"}), 
                       Head([Title(Text("Tables"))]),
                       Body([Div(Table([
                           Tr([Th(Text("Month")), Th(Text("Number"))]),
                           Tr([Td(Text("January")), Td(Text(1))]),
                           Tr([Td(Text("April")), Td(Text(4))]),
                           Tr([Td(Text("June")), Td(Text(6))])]))])])

    list_test = Html([Meta(attr={"charset" : "UTF-8"}), 
                      Head([Title(Text("List"))]),
                      Body([Div([
                            Ul([Li(Text("Elem")),
                                Li(Text("Elem"))]),
                            Ol([Li(Text("Elem1")),
                                Li(Text("Elem2"))])])])])

    misc_test = Html([Meta(attr={"charset" : "UTF-8"}), 
                      Head([Title(Text("Titre"))]),
                      Body([Div(Text("div")),
                            Hr(),
                            Span(Text("span")),
                            Br(),
                            P(Text("p"))])])

    previous_exercice = Html([Head(Title(Text('"Hello ground!"'))),
                              Body([H1(Text('"Oh no, not again!"')),
                                    Img(attr={"src": "http://i.imgur.com/pfp3T.jpg"})])])

    print(basic_test)
    print(table_test)
    print(list_test)
    print(misc_test)
    print(previous_exercice)