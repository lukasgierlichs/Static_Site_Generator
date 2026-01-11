from generation_tools import generate_page
import os


def test_generate_page_applies_basepath(tmp_path, monkeypatch):
    # create a small content markdown file
    content_dir = tmp_path / "contenttest"
    content_dir.mkdir()
    md = content_dir / "index.md"
    md.write_text('# Title\n\n![img](/images/tolkien.png)\n\n[Home](/)')

    # create a template with a root-relative link
    tpl = tmp_path / "template.html"
    tpl.write_text('<html><head><link href="/index.css"/></head><body>{{ Content }}</body></html>')

    dest = tmp_path / "out.html"

    # run generator with basepath '/base'
    generated = generate_page(str(md), str(tpl), str(dest), basepath='/base')

    assert 'href="/base/' in generated
    assert 'src="/base/' in generated
    # ensure the file was written
    assert dest.exists()
    file_content = dest.read_text()
    assert 'href="/base/' in file_content
    assert 'src="/base/' in file_content
