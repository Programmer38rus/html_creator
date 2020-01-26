
class Tag:
    """ КЛАСС ДЛЯ БОЛЕЕ СЛОЖНЫХ КОНТЕКСТОВ """

    def __init__(self, tag, is_single = False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}

        self.is_single = is_single
        self.children = []

        if klass is not None:
            self.attributes["class"] = " ".join(klass)
            print(self.attributes)

        for attr, val in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = val
    
        
    def __iadd__(self, other):
        self.children.append(other)
        return self

        # print(self.tag)
    def __enter__(self):
        return self
    def __exit__(self, *args, **kwargs):
        pass

    def __str__(self):
        attrs = []
        for atribute, value in self.attributes.items():
            attrs.append('{}="{}"'.format(atribute, value))
        attrs = " ".join(attrs)

        if len(self.children) > 0:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            if self.text:
                internal = "{}".format(self.text)
            else:
                internal = ""
            for child in self.children:
                internal += str(child)
            ending = "</{}>".format(self.tag)
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{} {}/>".format(self.tag, attrs)
            else:
                return "<{tag}>{text}</{tag}>".format(tag=self.tag, text=self.text)
class HTML:
    """ КЛАСС ДЛЯ ОСНОВНОГО ХТМЛ """

    def __init__(self, output):
        self.output = output
        self.children = []
    
    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        if self.output is not None:
            with open(self.output, "w") as fp:
                fp.write(str(self))
    def __str__(self):
        html = "<html>\n"
        for child in self.children:
            html += str(child)
        html += "\n</html"
        return html

class TopLevelTag:
    """ КЛАСС ДЛЯ РОДИТЕЛЬСКИХ ТЕГОВ """

    def __init__(self, tag):
        self.tag = tag
        self.children = []
    # метод для конкатенации строк
    def __iadd__(self, other):
        self.children.append(other)
        return self

        # print(self.tag)
    def __enter__(self):
        return self
    def __exit__(self, *args, **kwargs):
        pass
    # МЕТОД ДЛЯ ВЫВОДА ПРИНТОВ.
    # В НЁМ МЫ ОБРАБАТЫВАЕМ ТЭГИ РОДИТЕЛЬСКИЕ И ДОЧЕРНИЕ КОНКОТЕНИРОВАННЫЕ ТЭГИ
    def __str__(self):

        html = "<{tag}>\n".format(tag=self.tag)
        for child in self.children:
            html += str(child)
        html += "\n<{tag}>".format(tag=self.tag)
        return html


def main(output=None):
    with HTML(output=output) as doc:
        with TopLevelTag("head") as head:
            print(head.tag)
            with Tag("title") as title:
                title.text = "hello"
                head += title   
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img

                body += div

            doc += body

if __name__ == "__main__":
    main("b3-hw.html")