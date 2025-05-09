from requests_html import HTMLSession
import csv
from io import StringIO
import pandas as pd

def checkSheet():
    sheetId = "10vNsyTFX0BTr_yTHGMzApH6iGOCk-NAjFdR3M9S40t8"
    url = f"https://docs.google.com/spreadsheets/d/{sheetId}/htmlview"
    sess = HTMLSession()                     # Uses no Google API
    resp = sess.get(url, headers={"User-Agent":"Mozilla/5.0"})
    resp.html.render(timeout=30)             # Runs the sheet's JS to build the table

    # Find the first <table> on the page
    table = resp.html.find("table", first=True)
    if not table:
        raise RuntimeError("No table found—sheet still requires publishing")

    # Extract rows
    rows = []
    for tr in table.find("tr"):
        rows.append([cell.text for cell in tr.find("th, td")])

    # Convert to CSV text
    buf = StringIO()
    writer = csv.writer(buf)
    writer.writerows(rows)
    csvText = buf.getvalue()
    # print(csvText) # Print the CSV text for debugging
    csvText = trimCsvCsvmodule(csvText, skipRows=3, keepCols=3) # drop first 3 rows, keep only first 3 columns
    return csvText

def trimCsvCsvmodule(csvString, skipRows=4, keepCols=6):
    """
    Drop the first `skipRows` rows of the CSV string, then keep only the first `keepCols` columns.
    Returns a new CSV‑formatted string.
    """

    df = pd.read_csv(
        StringIO(csvString),
        header=0,
        skiprows=4,
        dtype=str               # preserve everything as string
    )
    # select & reorder
    df = df[['Programme Name', 'Company Name', 'Opening Date']]
    # rename
    df.columns = ['Position Name', 'Company Name', 'Open Date']
    # output CSV
    return df.to_csv(index=False)