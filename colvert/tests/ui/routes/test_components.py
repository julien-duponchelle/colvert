import pytest

from colvert.ui.components import error_box, info_box, warning_box


@pytest.mark.asyncio
async def test_info_box(get_request):
    response = await info_box("This is an info message", get_request)
    assert response.status == 200
    assert "This is an info message" in str(response.body)


@pytest.mark.asyncio
async def test_error_box(get_request):
    response = await error_box("This is an error message", get_request)
    assert response.status == 200
    assert "This is an error message" in str(response.body)


@pytest.mark.asyncio
async def test_warning_box(get_request):
    response = await warning_box("This is a warning message", get_request)
    assert response.status == 200
    assert "This is a warning message" in str(response.body)
