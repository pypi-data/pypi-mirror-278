import os
import typing
from dataclasses import dataclass

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.logging import getLogger

import sphinx_nbblog.tags

logger = getLogger("sphinx-nbblog")


class NbblogNode(nodes.General, nodes.Element):
    pass


class ArchiveNode(nodes.General, nodes.Element):
    pass


class TagPageNode(nodes.General, nodes.Element):
    def __init__(self, *args, tag, **kwargs):
        self.tag = tag
        super().__init__(*args, **kwargs)


class ArchiveDirective(Directive):
    def run(self):
        return [ArchiveNode("")]


class TagPageDirective(SphinxDirective):
    required_arguments: typing.ClassVar = 1

    def run(self):
        tag = self.arguments[0]
        return [TagPageNode("", tag=tag)]


def create_archive_view(env, app, fromdocname, filter_by_tag=None):
    """
    iterates through env.nbblogs and returns a list of
    paragraph nodes for all the nbblogs sorted by date
    and categorized by year.

    this function defines the layout of the archive page.
    """
    content = []
    container = nodes.container()
    container["classes"] = ["toctree-wrapper", "compound"]
    sorted_posts = sorted(env.nbblogs, key=lambda p: int(p.date.replace("-", "")), reverse=True)
    if filter_by_tag is not None:
        sorted_posts = [p for p in sorted_posts if filter_by_tag in p.tags]
    years = sorted({p.date.split("-")[0] for p in sorted_posts}, reverse=True)
    for y in years:
        year_header = nodes.paragraph()
        year_header.append(nodes.Text(str(y)))
        container.append(year_header)
        posts_in_a_year = [p for p in sorted_posts if p.date.split("-")[0] == y]
        post_list = nodes.bullet_list()
        for p in posts_in_a_year:
            post_list_item = nodes.list_item()
            post_title = env.titles[p.docname].astext()

            post_par = nodes.paragraph()
            post_link = nodes.reference("", "")
            post_text = nodes.Text(post_title)
            post_link["refdocname"] = p.docname
            post_link["refuri"] = app.builder.get_relative_uri(fromdocname, p.docname)
            post_link["ids"] = [os.path.basename(p.docname)]
            post_link["classes"] = ["archive-link"]
            post_link.append(post_text)
            post_par.append(post_link)

            post_list_item.append(post_par)
            post_list.append(post_list_item)
        container.append(post_list)
    content.append(container)
    return content


def process_nbblog_nodes(app, doctree, fromdocname):
    if not app.config.include_nbblogs:
        for node in doctree.findall(NbblogNode):
            node.parent.remove(node)
        for node in doctree.findall(ArchiveNode):
            node.replace_self([])
        return

    env = app.builder.env
    if not hasattr(env, "nbblogs"):
        env.nbblogs = []

    for node in doctree.findall(ArchiveNode):
        content = create_archive_view(env, app, fromdocname)
        node.replace_self(content)

    for node in doctree.findall(TagPageNode):
        content = create_archive_view(env, app, fromdocname, filter_by_tag=node.tag)
        node.replace_self(content)


@dataclass
class Nbblog:
    date: str
    tags: list[str]
    abstract: str
    docname: str
    lineno: int
    virtual_env: str = "default"
    builder_name: typing.ClassVar = "html"

    def view_tags(self, env):
        """
        this function defines the layout of tags in an nbblog view
        """
        result = nodes.paragraph()
        result["classes"] = ["tags"]
        result += nodes.inline(text=f"{env.app.config.tags_intro_text} ")
        for idx, tag in enumerate(self.tags):
            link = f"{env.app.config.tags_url}/{tag}/"
            if self.builder_name == "html":
                link = link + ".html"
            result += nodes.reference(refuri=link, text=tag)
            if idx < len(self.tags) - 1:
                result += nodes.inline(text=", ")
        return result

    def view_date(self, env):
        """
        defines the layout of the date view in an nbblog view
        """
        link = f"{env.app.config.archive_url}/#{os.path.basename(self.docname)}"
        if self.builder_name == "html":
            link = link + ".html"
        archive_reference = nodes.paragraph()
        archive_reference.extend(
            [nodes.inline(text="Date: "), nodes.reference(refuri=link, text=self.date)]
        )
        return archive_reference

    def view(self, env):
        """
        this function defines the layout of the nbblog node
        """
        container = nodes.container()
        container["classes"] = ["blogheader"]
        container.append(self.view_date(env))
        container.append(self.view_tags(env))
        return container


class NbblogDirective(SphinxDirective):
    required_arguments: typing.ClassVar = 0
    has_content: typing.ClassVar = False
    option_spec: typing.ClassVar = {
        "date": directives.unchanged_required,
        "abstract": directives.unchanged_required,
        "tags": directives.unchanged_required,
        "virtual_env": directives.unchanged,
    }

    def run(self):
        if "tags" in self.options.keys():
            self.options["tags"] = (
                self.options["tags"].removesuffix("\n").replace(" ", "").split(",")
            )
        else:
            self.options["tags"] = []
        nbblog = Nbblog(lineno=self.lineno, docname=self.env.docname, **self.options)
        if not hasattr(self.env, "nbblogs"):
            self.env.nbblogs = []  # pyright: ignore[reportGeneralTypeIssues]
        self.env.nbblogs.append(nbblog)  # pyright: ignore[reportGeneralTypeIssues]
        return [nbblog.view(self.env)]


def set_builder_name(app: Sphinx) -> None:
    Nbblog.builder_name = app.builder.name


def setup_extension(app: Sphinx) -> None:
    sphinx_nbblog.tags.setup(app)
    app.add_config_value("include_nbblogs", True, "html")
    app.add_config_value("tags_url", "../../../../tags", "html")
    app.add_config_value("archive_url", "../../../../archive", "html")

    app.add_node(NbblogNode)
    app.add_node(ArchiveNode)
    app.connect("builder-inited", set_builder_name)
    app.connect("doctree-resolved", process_nbblog_nodes)
    app.add_directive("archive", ArchiveDirective)
    app.add_directive("nbblog", NbblogDirective)
    app.add_directive("tagpage", TagPageDirective)
