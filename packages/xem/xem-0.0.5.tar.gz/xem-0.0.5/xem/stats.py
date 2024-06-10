import duckdb as db
from tabulate import tabulate

if __name__ == "__main__":
    stmt = \
        """
        CREATE TABLE IF NOT EXISTS events
        AS SELECT * FROM "EventLog.jsonl"
        """
    db.execute(stmt).fetchall()

    rows = db.execute("""
        SELECT referrer, count(*)
        FROM events
        GROUP BY referrer
        ORDER BY count(*) DESC
    """).fetchall()

    print(tabulate(rows, headers=['referrer',
        'page views'], tablefmt="mixed_grid"))

    rows = db.execute("""
        SELECT ip, count(*)
        FROM events
        GROUP BY ip
        ORDER BY count(*) DESC
    """).fetchall()
    print(tabulate(rows, headers=['ip', 'page views'], tablefmt="mixed_grid"))

    rows = db.execute("""
        SELECT url, count(*)
        FROM events
        GROUP BY url
        ORDER BY count(*) DESC
    """).fetchall()
    print(tabulate(rows, headers=['url', 'page views'], tablefmt="mixed_grid"))
