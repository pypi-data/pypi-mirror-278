from bs4 import BeautifulSoup


def test_tags_in_blog_header(sphinx_project, pages):
    """
    this tests if the tags defined in the directive
    of a page are also found in the generated html file
    for that page
    """
    html_dir = sphinx_project / "build" / "html"
    for page_name, page in pages.items():
        # if builder is dirhtml or html
        if (html_dir / page.location / page_name).is_dir():
            path = html_dir / page.location / page_name / "index.html"
        else:
            path = html_dir / page.location / (page_name + ".html")
        with open(path) as f:
            soup = BeautifulSoup(f, features="html.parser")
        tags_from_content_html = [x.string for x in soup.select("div.blogheader p.tags a")]
        assert tags_from_content_html == page.tags


def test_creation_of_tag_files(sphinx_project, pages):
    """
    this tests if all tags have a tag file
    """
    tags_from_pages = set()
    for page in pages.values():
        tags_from_pages.update(page.tags)
    tags_from_pages = list(tags_from_pages)
    tag_files = list((sphinx_project / "source" / "tags").glob("*.rst"))
    tag_file_names = sorted([f.name.split(".")[0] for f in tag_files])
    assert tag_file_names == sorted([*tags_from_pages, "index"])


def test_tags_in_tag_files(sphinx_project, pages):
    """
    this tests if pages in a tag file are actually tagged
    with that tag
    """
    tag_files = (sphinx_project / "build" / "html" / "tags").glob("*.rst")
    for tag_file in tag_files:
        with open(tag_file) as f:
            soup = BeautifulSoup(f, features="html.parser")
        pages_from_tag_file = [x.string for x in soup.select("div.toctree-wrapper ul li a")]
        for page_name in pages_from_tag_file:
            assert pages[page_name].name in pages_from_tag_file


def test_if_all_pages_are_in_archive(sphinx_project, pages):
    """
    this tests if all the pages are in the achive
    """
    html_dir = sphinx_project / "build" / "html"
    if (html_dir / "archive").is_dir():
        archive = html_dir / "archive" / "index.html"
    else:
        archive = html_dir / "archive.html"
    with open(archive) as f:
        soup = BeautifulSoup(f, features="html.parser")
    number_of_pages_in_archive = len(soup.select("#archive li a"))
    number_of_pages = len(pages)
    assert number_of_pages == number_of_pages_in_archive


def test_order_of_pages_in_archive(sphinx_project, pages):
    """
    this tests if the pages are ordered according to their date
    in the archive html file
    """
    html_dir = sphinx_project / "build" / "html"
    if (html_dir / "archive").is_dir():
        archive = html_dir / "archive" / "index.html"
    else:
        archive = html_dir / "archive.html"
    with open(archive) as f:
        soup = BeautifulSoup(f, features="html.parser")
    links = list(soup.find_all("a", "archive-link"))
    # TODO: change sphinx_project into a dataclass or something with
    # the path and the builder so i don't need to check if it's
    # dirhtml or html in such a terrible way
    if (html_dir / "archive").is_dir():
        # this is for dirhtml builder
        pages_from_archive = [x.get("href").split("/")[-2] for x in links]
    else:
        # this is for html builder
        pages_from_archive = [x.get("href").split("/")[-1].split(".")[-2] for x in links]
    sorted_pages = sorted(
        [(pages[p].date, pages[p].name) for p in pages],
        key=lambda x: int(x[0].replace("-", "")),
        reverse=True,
    )
    sorted_pages_names = [p[1] for p in sorted_pages]
    assert sorted_pages_names == pages_from_archive
