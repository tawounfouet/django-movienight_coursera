from html.parser import HTMLParser

from django.test import TestCase


class BootstrapDataParser(HTMLParser):
    in_head = False
    link_href_correct = False
    link_rel_correct = False
    script_correct = False
    container_div_found = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "head":
            if self.in_head:
                raise ValueError("Found another head inside the head")
            self.in_head = True
            return

        if tag == "link":
            if not self.in_head:
                raise ValueError("Found link outside of head")

            if attrs.get("href").endswith("bootstrap.min.css"):
                if self.link_href_correct:
                    raise ValueError("Found bootstrap.min.css link more that once")
                self.link_href_correct = True

            if attrs.get("rel") == "stylesheet":
                if self.link_rel_correct:
                    raise ValueError("Found rel stylesheet more than once")
                self.link_rel_correct = True
            return

        if tag == "script":
            if self.in_head:
                raise ValueError("script should not be in the head")

            if self.script_correct:
                raise ValueError("Found more than one script")

            if attrs.get("src").endswith("bootstrap.bundle.min.js"):
                self.script_correct = True

        if tag == "div":
            classes = attrs.get("class", "").split()
            if "container-fluid" in classes and "pt-3" in classes:
                if self.container_div_found:
                    raise ValueError("Container div found more than once")
                self.container_div_found = True

    def handle_endtag(self, tag):
        if tag == "head":
            if not self.in_head:
                raise ValueError("Closing head found without opening head")
            self.in_head = False

    def error(self, message):
        raise ValueError(message)


class Question2TestCase(TestCase):
    def setUp(self):
        resp = self.client.get("/")
        self.parser = BootstrapDataParser()
        self.parser.feed(resp.content.decode("utf8"))

    def test_head_content(self):
        self.assertTrue(self.parser.link_href_correct)
        self.assertTrue(self.parser.link_rel_correct)

    def test_script(self):
        self.assertTrue(self.parser.script_correct)

    def test_container_div(self):
        self.assertTrue(self.parser.container_div_found)
