from playwright.sync_api import sync_playwright


def insert_text(page, text):
    for letter in text:
        page.keyboard.press(letter)
        page.wait_for_timeout(110)

def reset_sql(sql, page):
    sql.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Delete")

def select_chart(page, chart_name):
    page.get_by_label("Chart type").select_option(chart_name)
    page.wait_for_timeout(100)

def demo_chart(page, sql, chart_name, query):
    reset_sql(sql, page)
    insert_text(page, query)
    page.wait_for_timeout(500)
    select_chart(page, chart_name)
    page.wait_for_timeout(4000)
    select_chart(page, 'Table')
    page.wait_for_timeout(1000)
    

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    context = browser.new_context(
        record_video_dir="videos/",
        viewport={"width": 1280, "height": 720},
    )
    page = context.new_page()
    page.goto("http://localhost:8000")
    page.wait_for_load_state()

    sql = page.get_by_text("SELECT")
    reset_sql(sql, page)
    insert_text(page, 'SELECT COUNT(*) FROM test')
    page.wait_for_timeout(500)
    insert_text(page, " WHERE City = 'Paris'")
    page.wait_for_timeout(1000)
    
    demo_chart(page, sql, 'Pie Chart', 'SELECT City,COUNT(*) FROM test GROUP BY City')
    demo_chart(page, sql, 'Line Chart', 'SELECT "Birth Date",Salary FROM test ORDER BY "Birth Date"')

    page.get_by_role("tab", name="Prompt").click()
    page.locator("#prompt").press_sequentially("Get max salary by office location", delay=100)
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="Prompt to SQL").click()

    page.wait_for_timeout(2000)
    browser.close()