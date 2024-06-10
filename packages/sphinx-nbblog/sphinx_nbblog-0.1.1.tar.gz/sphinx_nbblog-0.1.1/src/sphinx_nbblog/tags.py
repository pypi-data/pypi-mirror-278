"""This file contains modified source code from:
    https://github.com/melissawm/sphinx-tags

MIT License

Copyright (c) 2022 Melissa Weber Mendonça

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os
from pathlib import Path

from sphinx.util.logging import getLogger

logger = getLogger("sphinx-nbblog")


class Tag:
    """A tag contains entries"""

    def __init__(self, name):
        self.name = name
        self.items = []

    def create_file(
        self,
        items,
        tags_output_dir,
        srcdir,
        tags_page_title,
    ):
        """Create file with list of documents associated with a given tag in
        toctree format.

        This file is reached as a link from the tag name in each documentation
        file, or from the tag overview page.

        If we are using md files, generate and md file; otherwise, go with rst.

        Parameters
        ----------

        tags_output_dir : Path
            path where the file for this tag will be created
        items : list
            list of files associated with this tag (instance of Entry)
        extension : {["rst"], ["md"], ["rst", "md"]}
            list of file extensions used.
        srcdir : str
            root folder for the documentation (usually, project/docs)
        tags_page_title: str
            the title of the tag page,
            after which the tag is listed (e.g. "Tag: programming")
        tags_page_header: str
            the words after which the pages with the tag are listed,
            e.g. "With this tag: Hello World")
        tag_intro_text: str
            the words after which the tags of a given page are listed,
            e.g. "Tags: programming, python")
        """
        content = []
        filename = f"{self.name}.rst"
        content.append(f"{tags_page_title}: {self.name}")
        content.append("#" * (len(self.name) + len(tags_page_title) + 2))
        content.append("")
        content.append(f".. tagpage:: {self.name}")
        content.append("")
        content.append(".. toctree::")
        content.append("    :maxdepth: 1")
        content.append("    :hidden:")
        # content.append(f"    :caption: {tags_page_header}")
        content.append("")
         # items is a list of files associated with this tag
        for item in sorted(items, key=lambda i: i.filepath):
            relpath = item.filepath.relative_to(srcdir)
            content.append(f"    ../{relpath}")

        content.append("")
        with open(os.path.join(srcdir, tags_output_dir, filename), "w", encoding="utf8") as f:
            f.write("\n".join(content))


class Entry:
    """Extracted info from source file (*.rst/*.md)"""

    def __init__(self, entrypath):
        self.filepath = entrypath
        self.tags = []
        with open(self.filepath, encoding="utf8") as f:
            self.lines = f.read().split("\n")
        if self.filepath.name.endswith(".rst"):
            tagstart = ":tags:"
        elif self.filepath.name.endswith(".ipynb"):
            tagstart = ":tags:"
        elif self.filepath.name.endswith(".md"):
            tagstart = "```{tags}"
        else:
            return
        tagline = [line for line in self.lines if tagstart in line]
        if tagline:
            tagline = tagline[0]
            tagline = tagline[tagline.find(tagstart) + len(tagstart) :]
            if "\\n" in tagline:
                tagline = tagline[: tagline.find("\\n")]
            tagline = (
                tagline.replace('"', "")
                .rstrip(",")
                .replace(" ", "")
                .replace("\\n", "")
                .replace("'", "")
            )
            self.tags = [tag.strip() for tag in tagline.split(",")]

    def assign_to_tags(self, tag_dict):
        """Append ourself to tags"""
        for tag in self.tags:
            if tag not in tag_dict:
                tag_dict[tag] = Tag(tag)
            tag_dict[tag].items.append(self)


def tagpage(tags, outdir, title):
    """Creates Tag overview page.
    This page contains a list of all available tags.
    """
    tags = list(tags.values())

    content = []
    content.append(title)
    content.append("#" * len(title))
    content.append("")
    # toctree for the page
    content.append(".. toctree::")
    # content.append(f"    :caption: {tags_index_head}")
    content.append("    :maxdepth: 1")
    content.append("")
    for tag in sorted(tags, key=lambda t: t.name):
        content.append(f"    {tag.name} ({len(tag.items)}) <{tag.name}.rst>")
    content.append("")
    filename = os.path.join(outdir, "index.rst")

    with open(filename, "w", encoding="utf8") as f:
        f.write("\n".join(content))


def assign_entries(app):
    """Assign all found entries to their tag."""
    pages = []
    tags = {}
    result = []
    for extension in app.config.tags_extension:
        result.extend(
            [
                r
                for r in Path(app.srcdir).rglob(f"*.{extension}")
                if all(x not in str(r) for x in [".ipynb_checkpoints", "docs/build"])
            ]
        )
    for entrypath in result:
        entry = Entry(entrypath)
        entry.assign_to_tags(tags)
        pages.append(entry)
    return tags, pages


def update_tags(app):
    """
    find all tags and create the tags folder and a tag page for each tag
    with links back to the tagged pages
    Update tags according to pages found
    """
    if app.config.include_nbblogs:
        tags_output_dir = Path(app.config.tags_output_dir)

        if not os.path.exists(os.path.join(app.srcdir, tags_output_dir)):
            os.makedirs(os.path.join(app.srcdir, tags_output_dir))

        for file in os.listdir(os.path.join(app.srcdir, tags_output_dir)):
            if file.endswith("md") or file.endswith("rst") or file.endswith("html"):
                os.remove(os.path.join(app.srcdir, tags_output_dir, file))

        # Create pages for each tag
        tags, pages = assign_entries(app)
        for tag in tags.values():
            tag.create_file(
                [item for item in pages if tag.name in item.tags],
                tags_output_dir,
                app.srcdir,
                app.config.tags_page_title,
            )
        # Create tags overview page
        tagpage(
            tags,
            os.path.join(app.srcdir, tags_output_dir),
            app.config.tags_overview_title,
        )
        logger.info("Tags updated", color="white")
    else:
        logger.info("Tags were not created (tags_create_tags=False in conf.py)", color="white")


def setup(app):
    """Setup for Sphinx."""

    # Create config keys (with default values)
    # These values will be updated after config-inited
    app.add_config_value("tags_output_dir", "tags", "html")
    app.add_config_value("tags_overview_title", "Tags", "html")
    app.add_config_value("tags_extension", ["ipynb", "rst"], "html")
    app.add_config_value("tags_intro_text", "Tags:", "html")
    app.add_config_value("tags_page_title", "Tag", "html")
    app.add_config_value("tags_page_header", "With this tag", "html")
    app.add_config_value("tags_index_head", "Tags", "html")

    # internal config values
    app.add_config_value(
        "remove_from_toctrees",
        [
            app.config.tags_output_dir,
        ],
        "html",
    )

    # Update tags
    # TODO: tags should be updated after sphinx-gallery is generated, and the
    # gallery is also connected to builder-inited. Are there situations when
    # this will not work?
    app.connect("builder-inited", update_tags)
