"""Rebuild the frozen CSV from authorized Lab 14 archived chart JSON."""
import argparse
import csv
import hashlib
import io
import json
import math
from datetime import date, datetime, timezone
from pathlib import Path

TICKERS = ("BIL", "IEF", "LQD", "VT")
START = date(2021, 10, 1)
END = date(2026, 10, 1)


def rebuild(archive, data):
    series = {}
    for ticker in TICKERS:
        raw = json.loads((archive / f"{ticker}_monthly.json").read_text(encoding="utf-8"))
        result, = raw["chart"]["result"]
        if result["meta"]["symbol"] != ticker or result["meta"]["currency"] != "USD":
            raise ValueError(f"{ticker}: unexpected symbol or currency")
        values = {}
        for stamp, price in zip(result["timestamp"], result["indicators"]["adjclose"][0]["adjclose"], strict=True):
            month = datetime.fromtimestamp(stamp, timezone.utc).date()
            if START <= month < END:
                if month.day != 1 or month in values or price is None or price <= 0 or not math.isfinite(price):
                    raise ValueError(f"{ticker}: invalid or duplicate month {month}")
                values[month] = price
        if len(values) != 60:
            raise ValueError(f"{ticker}: expected 60 complete months")
        series[ticker] = values
    months = sorted(series["BIL"])
    if any(set(values) != set(months) for values in series.values()):
        raise ValueError("Monthly series do not align")
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(["date", *TICKERS])
    writer.writerows([month, *(series[ticker][month] for ticker in TICKERS)] for month in months)
    contents = buffer.getvalue().encode("utf-8")
    checks = dict(line.split()[::-1] for line in (data / "SHA256SUMS").read_text().splitlines())
    digest = hashlib.sha256(contents).hexdigest()
    if digest != checks["prices.csv"]:
        raise ValueError("Rebuilt CSV differs from frozen fingerprint; no file written")
    (data / "prices.csv").write_bytes(contents)
    return digest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    try:
        digest = rebuild(args.archive, Path(__file__).resolve().parent / "data")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    print(f"Rebuilt 60 aligned monthly prices per fund. SHA-256 {digest}")
