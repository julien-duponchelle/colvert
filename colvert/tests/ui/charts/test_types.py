from colvert.ui.charts.types import (
    OptionTypeFloat,
    OptionTypeResultColumn,
    OptionTypeString,
)


def test_type_str():
    t = OptionTypeString("title", label="Title")
    assert t.render("hello \" world", []) == '<label for="title" class="form-label">Title</label><input value="hello &quot; world" type="text" id="title" name="title" class="form-control" onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))">'
    assert t.render("", []) == '<label for="title" class="form-label">Title</label><input type="text" id="title" name="title" class="form-control" onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))">'
    assert t.render(None, []) == '<label for="title" class="form-label">Title</label><input type="text" id="title" name="title" class="form-control" onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))">'
    t = OptionTypeString("title", label="Title", default="Hello")
    assert t.render(None, []) == '<label for="title" class="form-label">Title</label><input value="Hello" type="text" id="title" name="title" class="form-control" onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))">'


def test_type_float():
    t = OptionTypeFloat("title", label="Title", step=0.1)
    assert t.render(0.5, []) == '<label for="title" class="form-label">Title</label><input value="0.5" type="number" step="0.1" id="title" name="title" class="form-control" onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))">'
    t = OptionTypeFloat("title", label="Title", step=0.1, default=1)


def test_type_result_column():
    t = OptionTypeResultColumn("title", label="Title")
    assert t.render("hello", ["hello", "world"]) == '<label for="title" class="form-label">Title</label><select autocomplete="on" id="title" name="title" class="form-control" onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))"><option value=""></option><option value="hello" selected>hello</option><option value="world" >world</option></select>'
    assert t.render(None, ["hello", "world"]) == '<label for="title" class="form-label">Title</label><select autocomplete="on" id="title" name="title" class="form-control" onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))"><option value=""></option><option value="hello" >hello</option><option value="world" >world</option></select>'
