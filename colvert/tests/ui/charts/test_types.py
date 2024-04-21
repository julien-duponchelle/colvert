from colvert.ui.charts.types import OptionTypeFloat, OptionTypeString


def test_type_str():
    t = OptionTypeString("title", label="Title")
    assert t.render("hello \" world") == '<label for="title" class="form-label">Title</label><input value="hello &quot; world" type="text" id="title" name="title" class="form-control" onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))">'
    assert t.render("") == '<label for="title" class="form-label">Title</label><input type="text" id="title" name="title" class="form-control" onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))">'
    assert t.render(None) == '<label for="title" class="form-label">Title</label><input type="text" id="title" name="title" class="form-control" onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))">'
    t = OptionTypeString("title", label="Title", default="Hello")
    assert t.render(None) == '<label for="title" class="form-label">Title</label><input value="Hello" type="text" id="title" name="title" class="form-control" onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))">'


def test_type_float():
    t = OptionTypeFloat("title", label="Title", step=0.1)
    assert t.render(0.5) == '<label for="title" class="form-label">Title</label><input value="0.5" type="number" step="0.1" id="title" name="title" class="form-control" onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))">'
    t = OptionTypeFloat("title", label="Title", step=0.1, default=1)
