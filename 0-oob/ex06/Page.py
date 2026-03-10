from elements import *

class Page():
    def __init__(self, content):
        if not Page.is_valid(content):
            raise Elem.ValidationError
        self.content = content

    def __str__(self):
        ret = ""
        if self.content.tag == "html":
            ret += "<!DOCTYPE html>\n"
        ret += str(self.content)
        return ret

    def is_valid(content):
        if type(content) == list:
            for elem in content:
                if not Page.run_all_checks(elem):
                    return False
                if isinstance(elem, Text):
                    continue
                if elem.content and not Page.is_valid(elem.content):
                    return False
            return True
        else:
            if not Page.run_all_checks(content):
                return False
            if isinstance(content, Text):
                return True
            if content.content and not Page.is_valid(content.content):
                return False
            return True

    def run_all_checks(elem):
        if not isinstance(elem, (Elem, Text)):
            return False
        if isinstance(elem, Html) and not Page.is_valid_html(elem.content):
            return False
        if isinstance(elem, (Body, Div)) and not Page.check_content(elem.content, (H1, H2, Div, Table, Ul, Ol, Span, Text)):
            return False
        if isinstance(elem, (Title, H1, H2, Li, Th, Td)) and not isinstance(elem.content, Text):
            return False
        if isinstance(elem, P) and not Page.check_content(elem.content, Text):
            return False
        if isinstance(elem, Span) and not Page.check_content(elem.content, (Text, P)):
            return False
        if isinstance(elem, (Ul, Ol)) and not Page.check_content(elem.content, Li):
            return False
        if isinstance(elem, Table) and not Page.check_content(elem.content, Tr):
            return False
        if isinstance(elem, Tr) and not Page.is_valid_table_content(elem.content):
            return False
        return True

    def check_content(content, constraint):
        if type(content) == list:
            for elem in content:
                if not isinstance(elem, constraint):
                    return False
            return True
        else:
            return isinstance(content, constraint)
            
    def is_valid_html(content):
        if not isinstance(content[0], Head):
            return False
        if not isinstance(content[1], Body):
            return False
        if len(content) > 2:
            return False
        return True
    
    def is_valid_table_content(content):
        table_type = None
        if type(content) == list:
            for elem in content:
                if not table_type:
                    table_type = type(elem)
                elif table_type != type(elem):
                    return False
                if not isinstance(elem, (Th, Td)):
                    return False
            return True
        else:
            return isinstance(content, (Th, Td))

    def write_to_file(self, filename):
        with open(filename, "w") as f:
            f.write(str(self))

if __name__ == "__main__":

    invalid_type = Html([Head([Title(Text("Titre"))]),
                         Body([Div(Text("div")),
                               Span(Text("span")),
                               Text("TOTO"),
                               Elem(), #Here
                               Div([H1(Text("TITRE")), 
                                    H2(Text("Sous-Titre"))])])])
    try:
        Page(invalid_type)
    except:
        print("Invalid type OK")

    invalid_html = Html([Head([Title(Text("Titre"))]),
                         Body(Div(Text("Double body"))), #Here
                         Body([Div(Text("div")),
                               Span(Text("span")),
                               Text("TOTO"),
                               Div([H1(Text("TITRE")), 
                                    H2(Text("Sous-Titre"))])])])
    try:
        Page(invalid_html)
    except:
        print("Invalid html OK")

    invalid_head = Html([Head([Title(Text("Titre")),
                               Div()]), #Here
                         Body([Div(Text("div")),
                               Span(Text("span")),
                               Text("TOTO"),
                               Div([H1(Text("TITRE")), 
                                    H2(Text("Sous-Titre"))])])])
    try:
        Page(invalid_head)
    except:
        print("Invalid head OK")

    invalid_body = Html([Head([Title(Text("Titre"))]),
                         Body([Div(Text("div")),
                               Span(Text("span")),
                               Text("TOTO"),
                               Div([H1(Text("TITRE")), 
                                    H2(Text("Sous-Titre"))]),
                               P(Text("p"))])]) # Here
    try:
        Page(invalid_body)
    except:
        print("Invalid body OK")

    invalid_div = Html([Head([Title(Text("Titre"))]),
                         Body([Div(Text("div")),
                               Div([Text("div2"),
                                    P(Text("p"))]), #Here
                               Span(Text("span")),
                               Text("TOTO"),
                               Div([H1(Text("TITRE")), 
                                    H2(Text("Sous-Titre"))])])])
    try:
        Page(invalid_div)
    except:
        print("Invalid div OK")

    invalid_H1 = Html([Head([Title(Text("Titre"))]),
                         Body([Div(Text("div")),
                               Span(Text("span")),
                               Text("TOTO"),
                               Div([H1(Span(Text("TITRE"))), #Here
                                    H2(Text("Sous-Titre"))])])])
    try:
        Page(invalid_H1)
    except:
        print("Invalid H1 OK")

    invalid_title = Html([Head([Title(Span(Text("Titre")))]), #Here
                         Body([Div(Text("div")),
                               Span(Text("span")),
                               Text("TOTO"),
                               Div([H1(Text("TITRE")), 
                                    H2(Text("Sous-Titre"))])])])
    try:
        Page(invalid_title)
    except:
        print("Invalid title OK")

    invalid_P = Html([Head([Title(Text("Titre"))]),
                      Body([Div(Text("div")),
                            Span(Text("span")),
                            Span(P(Div())), #Here
                            Text("TOTO"),
                            Div([H1(Text("TITRE")), 
                                 H2(Text("Titre2"))])])])
    try:
        Page(invalid_P)
    except:
        print("Invalid P OK")

    invalid_ul = Html([Head([Title(Text("Titre"))]),
                       Body([Div(Text("div")),
                             Span(Text("span")),
                             Ul([Li(Text("elem")),
                                 Li(Text("elem")),
                                 P(Text("p"))]), #Here
                             Text("TOTO"),
                             Div([H1(Text("TITRE")), 
                                  H2(Text("Titre2"))])])])
    try:
        Page(invalid_ul)
    except:
        print("Invalid ul OK")

    invalid_span = Html([Head([Title(Text("Titre"))]),
                         Body([Div(Text("div")),
                               Span([Text("span"),
                                     Title(Text("titre"))]), #Here
                               Text("TOTO"),
                               Div([H1(Text("TITRE")), 
                                    H2(Text("Titre2"))])])])
    try:
        Page(invalid_span)
    except:
        print("Invalid span OK")

    invalid_table = Html([Head([Title(Text("Titre"))]),
                      Body([Div(Text("div")),
                            Span(Text("span")),
                            Text("TOTO"),
                            Table(Td()), #Here
                            Div([H1(Text("TITRE")), 
                                 H2(Text("Titre2"))])])])
    try:
        Page(invalid_table)
    except:
        print("Invalid table OK")

    invalid_Tr = Html([Head([Title(Text("Titre"))]),
                      Body([Div(Text("div")),
                            Span(Text("span")),
                            Text("TOTO"),
                            Table(Tr([Td(),
                                      Th()])), #Here
                            Div([H1(Text("TITRE")), 
                                 H2(Text("Titre2"))])])])
    try:
        Page(invalid_Tr)
    except:
        print("Invalid Tr OK")

    misc_test = Html([Head([Title(Text("Titre"))]),
                      Body([Div(Text("div")),
                            Span(Text("span")),
                            Text("TOTO"),
                            Div([H1(Text("TITRE")), 
                                 H2(Text("Titre2"))])])])

    toto = Page(misc_test)
    print(toto)
    toto.write_to_file("toto")
    print("Done")

            