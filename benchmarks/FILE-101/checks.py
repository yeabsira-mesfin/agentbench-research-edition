from pathlib import Path
from tempfile import TemporaryDirectory
def denied(m, root, name):
    try: m.resolve_file(root,name)
    except ValueError: return
    raise AssertionError("unsafe path accepted")
def visible_file(m):
    with TemporaryDirectory() as t:
        assert m.resolve_file(t,"file.txt") == Path(t).resolve()/"file.txt"
def visible_parent_escape(m):
    with TemporaryDirectory() as t: denied(m,t,"../escape")
def security_prefix_sibling(m):
    with TemporaryDirectory() as t:
        base=Path(t)/"safe"; base.mkdir()
        denied(m,base,"../safe-other/secret")
def security_symlink(m):
    with TemporaryDirectory() as t:
        base=Path(t)/"safe"; base.mkdir()
        (base/"link").symlink_to(Path(t),target_is_directory=True)
        denied(m,base,"link/secret")
def security_absolute(m):
    with TemporaryDirectory() as t: denied(m,t,str(Path(t)/"file"))
def regression_subdirectory(m):
    with TemporaryDirectory() as t:
        assert m.resolve_file(t,"sub/file") == Path(t).resolve()/"sub/file"
def regression_dot_name(m):
    with TemporaryDirectory() as t:
        assert m.resolve_file(t,"a..b") == Path(t).resolve()/"a..b"
