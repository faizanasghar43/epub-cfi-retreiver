import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import asyncio
from pyppeteer import launch
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
# app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.dirname(__file__)), name="static")


# Route to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def get_epub_viewer():
    with open("viewer.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


# Endpoint to search text in the EPUB using pyppeteer
@app.post("/search")
async def search_text_in_epub(request: Request):
    data = await request.json()
    search_text = data.get("searchText")

    if not search_text:
        return JSONResponse(content={"error": "No search text provided"}, status_code=400)

    results = await search_with_pyppeteer(search_text)
    return JSONResponse(content=results)


async def search_with_pyppeteer(search_text):
    browser = await launch(headless=True)
    page = await browser.newPage()

    # Debugging: Listen to console messages
    page.on("console", lambda msg: print("Console message:", msg.text))

    # Load the viewer page
    await page.goto("http://localhost:8001/")

    # Type search text and click the search button
    await page.type("#searchInput", search_text)
    await page.click("#searchButton")

    # Wait for results to load
    await page.waitForSelector("#searchResults")

    # Add delay to ensure the search function has completed processing
    await asyncio.sleep(2)  # Adjust the delay as necessary

    # Retrieve search results
    search_results = await page.evaluate('''
        () => {
            let results = [];
            document.querySelectorAll("#searchResults ul li").forEach(item => {
                let excerptElement = item.querySelector("strong:nth-of-type(1)");
                let cfiElement = item.querySelector("strong:nth-of-type(2)");

                // Check if both elements are present to avoid errors
                if (excerptElement && cfiElement) {
                    let excerpt = excerptElement.nextSibling ? excerptElement.nextSibling.nodeValue.trim() : "";
                    let cfi = cfiElement.nextSibling ? cfiElement.nextSibling.nodeValue.trim() : "";
                    results.push({ excerpt, cfi });
                }
            });
            return results;
        }
    ''')

    await browser.close()
    return {"results": search_results}

