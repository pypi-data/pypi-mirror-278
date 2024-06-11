import duckdb as db
import datapad as dp
from tabulate import tabulate
from datetime import datetime, timedelta, timezone
from argparse import ArgumentParser

if __name__ == "__main__":
    ap = ArgumentParser()
    ap.add_argument("-l", "--log", default="EventLog.jsonl.gz",
                    help="path to where we should save event log file")

    args = ap.parse_args()
    event_log_file = args.log

    stmt = \
        """
        CREATE TABLE IF NOT EXISTS events
        AS SELECT * FROM "%s"
        """
    db.execute(stmt % event_log_file).fetchall()

    print()

    rows = db.execute("""
        SELECT referrer, count(*)
        FROM events
        WHERE name = 'PageView'
        GROUP BY referrer
        ORDER BY count(*) DESC
    """).fetchall()
    print()
    print("Top Referrers")
    print(tabulate(rows,
                   headers=['referrer', 'page views'],
                   tablefmt="mixed_grid"))

    rows = db.execute("""
        SELECT sourceIp, count(*)
        FROM events
        WHERE name = 'PageView'
        GROUP BY sourceIp
        ORDER BY count(*) DESC
    """).fetchall()
    print()
    print("Most Frequent Visitors by IP")
    print(tabulate(rows,
                   headers=['sourceIp', 'page views'],
                   tablefmt="mixed_grid"))

    rows = db.execute("""
        SELECT pageUrl, count(*)
        FROM events
        GROUP BY pageUrl
        ORDER BY count(*) DESC
    """).fetchall()
    print()
    print("Most Viewed Pages")
    print(tabulate(rows,
                   headers=['pageUrl', 'page views'],
                   tablefmt="mixed_grid"))

    rows = db.execute("""
        SELECT time
        FROM events
        WHERE date_diff('day', current_date(), time) < 7
        AND name = 'PageView'
        ORDER BY time
    """).fetchall()

    counts_by_day = dp.Sequence(rows)\
        .map(lambda row: row[0])\
        .map(lambda d: d.strftime("%Y-%m-%d"))\
        .count(distinct=True)\
        .collect()

    counts_by_day = dict(counts_by_day)

    last_seven_days = dp.Sequence(range(7))\
        .map(lambda i: datetime.now(timezone.utc) - timedelta(days=i))\
        .map(lambda d: d.strftime("%Y-%m-%d"))\
        .map(lambda d: (d, counts_by_day.get(d, 0)))\
        .collect()

    print()
    print("Visitors Last 7 Days")
    print(tabulate(last_seven_days,
                   headers=['Date', 'Page Views'],
                   tablefmt="mixed_grid"))

    print()
    print()
    print()
