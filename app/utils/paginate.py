import sqlite3
from math import ceil

from flask import request
from utils.log import Log


def paginate_query(db_path, count_query, select_query, params=None, per_page=9):
    """Return paginated data for a given query.

    Args:
        db_path: Path to the SQLite database.
        count_query: SQL query returning the total number of items.
        select_query: SQL query returning items without limit and offset.
        params: Parameters for the SQL queries.
        per_page: Number of items per page.

    Returns:
        tuple: (rows, page, total_pages)
    """
    if params is None:
        params = []

    page = request.args.get("page", 1, type=int)

    Log.database(f"Connecting to '{db_path}' database")

    connection = sqlite3.connect(db_path)
    connection.set_trace_callback(Log.database)
    cursor = connection.cursor()

    cursor.execute(count_query, params)
    total_items = cursor.fetchone()[0]
    total_pages = max(ceil(total_items / per_page), 1)

    offset = (page - 1) * per_page
    cursor.execute(f"{select_query} limit ? offset ?", (*params, per_page, offset))
    rows = cursor.fetchall()

    return rows, page, total_pages
