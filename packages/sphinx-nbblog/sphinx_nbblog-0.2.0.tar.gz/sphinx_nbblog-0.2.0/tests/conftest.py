import json
import subprocess
from dataclasses import dataclass

import pytest
from nbformat import v4 as nbf


def make_notebook(title: str, raw_rst_content: str):
    nb = nbf.new_notebook()
    cells = [
        nbf.new_markdown_cell(title + "\n" + ("=" * len(title))),
        nbf.new_raw_cell(raw_rst_content, metadata={"raw_mimetype": "text/restructuredtext"}),
    ]
    nb["cells"] = cells
    formatted_json = json.dumps(nb.dict(), indent=1)
    return formatted_json


@dataclass
class Page:
    name: str
    title: str
    extension: str
    date: str
    tags: list[str]
    location: str = ""

    @property
    def filename(self):
        if self.location:
            return f"{self.location}/{self.name}.{self.extension}"
        else:
            return f"{self.name}.{self.extension}"

    @property
    def directive(self):
        """
        directive for rst files looks like this:

        Content
        =======

        .. nbblog::
           :date: 2023-09-21
           :abstract: this is an incredibly funny text
           :tags: funny, cool, good
           :virtual_env: default
        """
        if self.extension == "rst":
            return "\n".join(
                [
                    self.title,
                    "=" * len(self.title),
                    "",
                    ".. nbblog::",
                    f"   :date: {self.date}",
                    "   :abstract: something",
                    "   :tags: " + ", ".join(self.tags),
                    "   :virtual_env: default",
                ]
            )
        elif self.extension == "ipynb":
            return make_notebook(
                self.title,
                "\n".join(
                    [
                        ".. nbblog::",
                        f"   :date: {self.date}",
                        "   :abstract: something",
                        "   :tags: " + ", ".join(self.tags),
                        "   :virtual_env: default",
                    ]
                ),
            )


@pytest.fixture(scope="module")
def pages():
    return {
        "about": Page("about", "About", "rst", "2023-09-23", ["funny", "good", "cool"]),
        "woob": Page("woob", "Woob", "rst", "2023-08-12", ["yarp", "good", "cool", "norly"]),
        "nolp": Page("nolp", "Nolp", "rst", "2022-11-02", ["yarp", "norly", "clump"]),
        "plump": Page("plump", "Plump", "rst", "2021-11-30", ["plump_tag"]),
        "nota": Page("nota", "Nota", "rst", "2022-01-01", ["tooft"]),
        "notebook": Page("notebook", "Notebook", "ipynb", "2022-02-02", ["tooft", "norly"]),
        "inasubdir": Page("inasubdir", "Inasubdir", "rst", "2002-02-02", ["clump"], "subdir"),
        "difftitle": Page(
            "difftitle", "This one has a different title", "rst", "2001-02-02", ["good"]
        ),
    }


@pytest.fixture(scope="module")
def sphinx_project(tmp_path_factory, pages):
    project_path = tmp_path_factory.mktemp("docs")
    source_folder = project_path / "source"
    build_folder = project_path / "build" / "html"
    sphinx_quickstart_cmd = [
        "sphinx-quickstart",
        str(project_path),
        "--quiet",
        "--sep",
        "--no-batchfile",
        "--no-makefile",
        "--extensions=sphinx_nbblog,nbsphinx",
        "-p",
        "Sphinx-nbblog_test",
        "-a",
        "tester",
        "-v",
        "0.0.1",
    ]
    subprocess.call(sphinx_quickstart_cmd)

    for page in pages.values():
        if page.location is not None:
            (source_folder / page.location).mkdir(parents=True, exist_ok=True)
        with open(source_folder / page.filename, "+w", encoding="utf-8") as f:
            f.write(page.directive)

    with open(source_folder / "archive.rst", "+w") as f:
        f.write("Archive\n=======\n\n.. archive::")

    sphinx_build_cmd = f"sphinx-build -Q -a -b dirhtml {source_folder} {build_folder}"
    subprocess.call(sphinx_build_cmd.split(" "))
    return project_path
