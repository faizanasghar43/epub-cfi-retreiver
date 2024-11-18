# # import os
# #
# # from fastapi import FastAPI, Request
# # from fastapi.responses import HTMLResponse, JSONResponse
# # import asyncio
# # from pyppeteer import launch
# # from starlette.staticfiles import StaticFiles
# #
# # app = FastAPI()
# # app.mount("/static", StaticFiles(directory=os.path.dirname(__file__)), name="static")
# #
# #
# # # Route to serve the HTML page
# # @app.get("/", response_class=HTMLResponse)
# # async def get_epub_viewer():
# #     with open("viewer.html", "r") as file:
# #         html_content = file.read()
# #     return HTMLResponse(content=html_content)
# #
# #
# # # Endpoint to search text in the EPUB using pyppeteer
# # @app.post("/search")
# # async def search_text_in_epub(request: Request):
# #     data = await request.json()
# #     search_text = data.get("searchText")
# #
# #     # Check if searchText is provided
# #     if not search_text:
# #         return JSONResponse(content={"error": "No search text provided"}, status_code=400)
# #
# #     # Use pyppeteer to perform the search and retrieve results
# #     results = await search_with_pyppeteer(search_text)
# #     return JSONResponse(content=results)
# #
# #
# # # Function to use pyppeteer for automation
# # async def search_with_pyppeteer(search_text):
# #     browser = await launch(headless=True)
# #     page = await browser.newPage()
# #
# #     # Load the viewer page
# #     await page.goto("http://localhost:8000/")  # FastAPI app should run on localhost:8000
# #
# #     # Type search text and click the search button
# #     await page.type("#searchInput", search_text)
# #     await page.click("#searchButton")
# #
# #     # Wait for results to load
# #     await page.waitForSelector("#searchResults")
# #
# #     # Retrieve search results
# #     search_results = await page.evaluate('''
# #         () => {
# #             let results = [];
# #             document.querySelectorAll("#searchResults ul li").forEach(item => {
# #                 let excerpt = item.querySelector("strong").nextSibling.nodeValue;
# #                 let cfi = item.querySelector("strong").nextElementSibling.nextSibling.nodeValue;
# #                 results.push({ excerpt: excerpt.trim(), cfi: cfi.trim() });
# #             });
# #             console.log(results);
# #             return results;
# #         }
# #     ''')
# #     print(search_results)
# #
# #     await browser.close()
# #     return {"results": search_results}
# import os
#
# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse, JSONResponse
# import asyncio
# from pyppeteer import launch
# from starlette.staticfiles import StaticFiles
# from fastapi.middleware.cors import CORSMiddleware
#
# app = FastAPI()
#
# # Configure CORS to allow all origins
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all HTTP methods
#     allow_headers=["*"],  # Allows all headers
# )
# # app = FastAPI()
# app.mount("/static", StaticFiles(directory=os.path.dirname(__file__)), name="static")
#
#
# # Route to serve the HTML page
# @app.get("/", response_class=HTMLResponse)
# async def get_epub_viewer():
#     with open("viewer.html", "r") as file:
#         html_content = file.read()
#     return HTMLResponse(content=html_content)
#
#
# # Endpoint to search text in the EPUB using pyppeteer
# @app.post("/search")
# async def search_text_in_epub(request: Request):
#     data = await request.json()
#     search_text = data.get("searchText")
#
#     if not search_text:
#         return JSONResponse(content={"error": "No search text provided"}, status_code=400)
#
#     results = await search_with_pyppeteer(search_text)
#     return JSONResponse(content=results)
#
#
# # @app.webhooks.post("new-subscription")
#
# async def search_with_pyppeteer(search_text):
#     browser = await launch(headless=True)
#     page = await browser.newPage()
#
#     # Debugging: Listen to console messages
#     page.on("console", lambda msg: print("Console message:", msg.text))
#
#     # Load the viewer page
#     await page.goto("http://localhost:8000/")
#
#     # Type search text and click the search button
#     await page.type("#searchInput", search_text)
#     await page.click("#searchButton")
#
#     # Wait for results to load
#     await page.waitForSelector("#searchResults")
#
#     # Add delay to ensure the search function has completed processing
#     await asyncio.sleep(2)  # Adjust the delay as necessary
#
#     # Retrieve search results
#     search_results = await page.evaluate('''
#         () => {
#             let results = [];
#             document.querySelectorAll("#searchResults ul li").forEach(item => {
#                 let excerptElement = item.querySelector("strong:nth-of-type(1)");
#                 let cfiElement = item.querySelector("strong:nth-of-type(2)");
#
#                 // Check if both elements are present to avoid errors
#                 if (excerptElement && cfiElement) {
#                     let excerpt = excerptElement.nextSibling ? excerptElement.nextSibling.nodeValue.trim() : "";
#                     let cfi = cfiElement.nextSibling ? cfiElement.nextSibling.nodeValue.trim() : "";
#                     results.push({ excerpt, cfi });
#                 }
#             });
#             return results;
#         }
#     ''')
#
#     await browser.close()
#     return {"results": search_results}
# import os
# from fastapi import FastAPI, Request, HTTPException
# from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.staticfiles import StaticFiles
# import asyncio
# from pyppeteer import launch
#
# app = FastAPI()
#
# # Configure CORS to allow all origins
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all HTTP methods
#     allow_headers=["*"],  # Allows all headers
# )
#
# # Serve static files
# app.mount("/static", StaticFiles(directory=os.path.dirname(__file__)), name="static")
#
#
# # Route to serve the default page (redirect to default book)
# @app.get("/", response_class=HTMLResponse)
# async def root():
#     return RedirectResponse(url="/book/default_book_id")
#
#
# # Route to serve the book viewer based on `book_id`
# @app.get("/book/{book_id}", response_class=HTMLResponse)
# async def get_epub_viewer(book_id: str):
#     book_file = f"books/{book_id}.epub"
#     if not os.path.exists(book_file):
#         print("NAE LABBI KITAAB")
#         raise HTTPException(status_code=404, detail="Book not found")
#     with open("viewer.html", "r") as file:
#         html_content = file.read()
#     return HTMLResponse(content=html_content.replace("./static/book.epub", f'./static/books/{book_id}.epub'))
#
#
# # Endpoint to search text in the EPUB using pyppeteer
# @app.post("/search")
# async def search_text_in_epub(request: Request):
#     data = await request.json()
#     search_text = data.get("searchText")
#
#     if not search_text:
#         return JSONResponse(content={"error": "No search text provided"}, status_code=400)
#
#     results = await search_with_pyppeteer(search_text)
#     return JSONResponse(content=results)
#
#
# async def search_with_pyppeteer(search_text):
#     browser = await launch(headless=True)
#     page = await browser.newPage()
#
#     # Debugging: Listen to console messages
#     page.on("console", lambda msg: print("Console message:", msg.text))
#
#     # Load the viewer page
#     await page.goto("http://localhost:9000/")
#
#     # Type search text and click the search button
#     await page.type("#searchInput", search_text)
#     await page.click("#searchButton")
#
#     # Wait for results to load
#     await page.waitForSelector("#searchResults")
#
#     # Add delay to ensure the search function has completed processing
#     await asyncio.sleep(2)  # Adjust the delay as necessary
#
#     # Retrieve search results
#     search_results = await page.evaluate('''
#         () => {
#             let results = [];
#             document.querySelectorAll("#searchResults ul li").forEach(item => {
#                 let excerptElement = item.querySelector("strong:nth-of-type(1)");
#                 let cfiElement = item.querySelector("strong:nth-of-type(2)");
#
#                 // Check if both elements are present to avoid errors
#                 if (excerptElement && cfiElement) {
#                     let excerpt = excerptElement.nextSibling ? excerptElement.nextSibling.nodeValue.trim() : "";
#                     let cfi = cfiElement.nextSibling ? cfiElement.nextSibling.nodeValue.trim() : "";
#                     results.push({ excerpt, cfi });
#                 }
#             });
#             return results;
#         }
#     ''')
#
#     await browser.close()
#     return {"results": search_results}
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
import asyncio
from pyppeteer import launch

app = FastAPI()

# Configure CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Mount static files
app.mount("/books", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "books")), name="books")



# Redirect root to default book
@app.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url="/book/default_book_id")


@app.get("/book/{book_id}", response_class=HTMLResponse)
async def get_epub_viewer(book_id: str):
    # Check the file in the actual `books` directory
    book_file = os.path.join("books", f"{book_id}.epub")
    if not os.path.exists(book_file):
        print(f"Book not found: {book_file}")
        raise HTTPException(status_code=404, detail="Book not found")

    # Read the viewer.html template
    with open("viewer.html", "r") as file:
        html_content = file.read()

    # Replace the placeholder path with the actual `/books/{book_id}.epub` path
    return HTMLResponse(content=html_content.replace("./static/book.epub", f'/books/{book_id}.epub'))


# # Endpoint for searching text
# @app.post("/search")
# async def search_text_in_epub(request: Request):
#     data = await request.json()
#     search_text = data.get("searchText")
#
#     if not search_text:
#         return JSONResponse(content={"error": "No search text provided"}, status_code=400)
#
#     results = await search_with_pyppeteer(search_text)
#     return JSONResponse(content=results)
#
#
# async def search_with_pyppeteer(search_text):
#     browser = await launch(headless=True)
#     page = await browser.newPage()
#
#     # Debugging: Listen to console messages
#     page.on("console", lambda msg: print("Console message:", msg.text))
#
#     # Load the viewer page
#     await page.goto("http://localhost:8000/")
#
#     # Type search text and click the search button
#     await page.type("#searchInput", search_text)
#     await page.click("#searchButton")
#
#     # Wait for results to load
#     await page.waitForSelector("#searchResults")
#
#     # Add delay to ensure the search function has completed processing
#     await asyncio.sleep(2)  # Adjust the delay as necessary
#
#     # Retrieve search results
#     search_results = await page.evaluate('''
#         () => {
#             let results = [];
#             document.querySelectorAll("#searchResults ul li").forEach(item => {
#                 let excerptElement = item.querySelector("strong:nth-of-type(1)");
#                 let cfiElement = item.querySelector("strong:nth-of-type(2)");
#
#                 // Check if both elements are present to avoid errors
#                 if (excerptElement && cfiElement) {
#                     let excerpt = excerptElement.nextSibling ? excerptElement.nextSibling.nodeValue.trim() : "";
#                     let cfi = cfiElement.nextSibling ? cfiElement.nextSibling.nodeValue.trim() : "";
#                     results.push({ excerpt, cfi });
#                 }
#             });
#             return results;
#         }
#     ''')
#
#     await browser.close()
#     return {"results": search_results}
