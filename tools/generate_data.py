"""Generate the IQRedo sample data set (deterministic, standard library only).

Writes every CSV the labs upload into ../data/. Re-run it only if you want to change the
scenario; the committed CSVs are what the labs and their expected results are written against.

    python3 tools/generate_data.py            # macOS/Linux
    python tools/generate_data.py             # Windows

The readings start at a fixed UTC time. Lab 01 rebases them to "now" in KQL, so the date in the
file doesn't matter on the day.
"""

import csv
import math
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data"
START = datetime(2026, 11, 10, 6, 0, tzinfo=timezone.utc)
MINUTES = 180  # 06:00-08:59 UTC, one reading per station per minute
rng = random.Random(20261110)

CREWS = [
    # CrewId, CrewName, Shift, VanCapacity, HomeDepot, Supervisor
    ("C01", "North Loop", "Morning", 20, "Kings Cross Depot", "Amira Patel"),
    ("C02", "River Run", "Morning", 24, "Southwark Depot", "Tom Okafor"),
    ("C03", "City Sweep", "Morning", 18, "Liverpool Street Depot", "Grace Lindqvist"),
    ("C04", "West Wheels", "Afternoon", 20, "Paddington Depot", "Marco Rossi"),
    ("C05", "East Docks", "Afternoon", 24, "Canary Wharf Depot", "Hannah Wu"),
    ("C06", "Night Owls", "Night", 16, "Waterloo Depot", "Liam Byrne"),
]

DEPOTS = [
    # DepotName, Area, Latitude, Longitude, BikeStorageCapacity, OpenHours
    ("Kings Cross Depot", "Kings Cross", 51.5320, -0.1240, 120, "05:00-23:00"),
    ("Southwark Depot", "Southwark", 51.5035, -0.1040, 90, "05:00-23:00"),
    ("Liverpool Street Depot", "City of London", 51.5180, -0.0810, 80, "05:00-22:00"),
    ("Paddington Depot", "Paddington", 51.5160, -0.1770, 100, "06:00-22:00"),
    ("Canary Wharf Depot", "Canary Wharf", 51.5040, -0.0190, 110, "05:00-23:00"),
    ("Waterloo Depot", "Waterloo", 51.5030, -0.1130, 70, "00:00-24:00"),
]

# Neighbourhood, Borough, Zone, Priority, CrewId, centre lat/lon, pattern, streets
# pattern: "drain" = commuters ride out (stations empty), "fill" = commuters ride in (stations fill up),
# "steady" = small random movement. Specific stations are overridden in HERO below.
NEIGHBOURHOODS = [
    ("Kings Cross", "Camden", "Central", "Tier 1", "C01", 51.5308, -0.1238, "drain",
     ["York Way", "Caledonian Road", "Argyle Street", "Pancras Road", "Goods Way", "Wharf Road"]),
    ("Islington", "Islington", "Inner", "Tier 2", "C01", 51.5362, -0.1033, "drain",
     ["Upper Street", "Essex Road", "Liverpool Road", "Cross Street", "Duncan Terrace", "Danbury Street"]),
    ("Bankside", "Southwark", "Central", "Tier 1", "C02", 51.5075, -0.0990, "fill",
     ["Sumner Street", "Southwark Street", "Hopton Street", "Park Street", "Bear Gardens", "Emerson Street"]),
    ("Borough", "Southwark", "Inner", "Tier 2", "C02", 51.5010, -0.0930, "drain",
     ["Borough High Street", "Long Lane", "Great Dover Street", "Tabard Street", "Trinity Street", "Marshalsea Road"]),
    ("Holborn", "Camden", "Central", "Tier 1", "C03", 51.5174, -0.1200, "fill",
     ["High Holborn", "Kingsway", "Southampton Row", "Theobalds Road", "Red Lion Street", "Lambs Conduit Street"]),
    ("Shoreditch", "Hackney", "Inner", "Tier 2", "C03", 51.5260, -0.0780, "steady",
     ["Great Eastern Street", "Old Street", "Curtain Road", "Rivington Street", "Hoxton Square", "Charlotte Road"]),
    ("Marylebone", "Westminster", "Central", "Tier 2", "C04", 51.5200, -0.1530, "drain",
     ["Marylebone High Street", "Baker Street", "George Street", "Dorset Street", "Wigmore Street", "Paddington Street"]),
    ("Hyde Park", "Westminster", "Central", "Tier 2", "C04", 51.5073, -0.1657, "steady",
     ["Bayswater Road", "Park Lane", "Serpentine Road", "Kensington Gore", "Exhibition Road", "Lancaster Gate"]),
    ("Canary Wharf", "Tower Hamlets", "Inner", "Tier 1", "C05", 51.5050, -0.0200, "fill",
     ["Westferry Circus", "South Colonnade", "Montgomery Square", "Bank Street", "Upper Bank Street", "Cabot Square"]),
    ("Whitechapel", "Tower Hamlets", "Inner", "Tier 2", "C05", 51.5180, -0.0600, "drain",
     ["Whitechapel Road", "Commercial Road", "Cannon Street Road", "New Road", "Fieldgate Street", "Vallance Road"]),
    ("Waterloo", "Lambeth", "Central", "Tier 1", "C06", 51.5033, -0.1145, "drain",
     ["Waterloo Road", "The Cut", "Baylis Road", "Lower Marsh", "York Road", "Stamford Street"]),
    ("Westminster", "Westminster", "Central", "Tier 1", "C06", 51.4995, -0.1330, "steady",
     ["Whitehall", "Victoria Street", "Great Smith Street", "Horseferry Road", "Millbank", "Tothill Street"]),
]

VANS = [
    # VanId, Registration, CrewId, DepotName, BikeCapacity, Status
    ("V01", "LX24 BKE", "C01", "Kings Cross Depot", 20, "Available"),
    ("V02", "LX24 BKF", "C01", "Kings Cross Depot", 20, "Available"),
    ("V03", "LX23 RVR", "C02", "Southwark Depot", 24, "Available"),
    ("V04", "LX23 CTY", "C03", "Liverpool Street Depot", 18, "Available"),
    ("V05", "LX25 CTZ", "C03", "Liverpool Street Depot", 18, "InService"),
    ("V06", "LX22 WST", "C04", "Paddington Depot", 20, "Available"),
    ("V07", "LX24 EST", "C05", "Canary Wharf Depot", 24, "InService"),
    ("V08", "LX25 ESU", "C05", "Canary Wharf Depot", 24, "Available"),
    ("V09", "LX22 NGT", "C06", "Waterloo Depot", 16, "Available"),
    ("V10", "LX23 NGU", "C06", "Waterloo Depot", 16, "InService"),
]

# Uploaded in Lab 05 to show the ontology agent extending the ontology. Two "Available" vans have an open
# High-severity ticket, which changes the dispatch answer once the agent has added this entity type.
MAINTENANCE = [
    # TicketId, VanId, OpenedOn, Issue, Severity, TicketStatus, ExpectedFixedOn
    ("T-1001", "V02", "2026-11-09T16:20:00Z", "Tail-lift hydraulic leak", "High", "Open", "2026-11-12T12:00:00Z"),
    ("T-1002", "V09", "2026-11-10T05:10:00Z", "Brake warning light on", "High", "Open", "2026-11-11T09:00:00Z"),
    ("T-1003", "V04", "2026-11-02T08:00:00Z", "Bike rack strap worn", "Low", "Closed", "2026-11-03T10:00:00Z"),
    ("T-1004", "V06", "2026-11-08T13:45:00Z", "Rear camera intermittent", "Medium", "Open", "2026-11-13T17:00:00Z"),
    ("T-1005", "V03", "2026-10-28T11:30:00Z", "Tyre pressure low", "Low", "Closed", "2026-10-28T15:00:00Z"),
    ("T-1006", "V08", "2026-11-10T06:40:00Z", "Loose bike rack bolt", "Low", "Open", "2026-11-10T14:00:00Z"),
]

# Stations whose story the labs rely on: (neighbourhood index, station index) -> minutes empty at the end.
# These are the stations that are "empty for more than 15 minutes" in Tier 1 neighbourhoods.
HERO_EMPTY = {
    (0, 0): 38,   # Kings Cross, York Way
    (0, 2): 24,   # Kings Cross, Argyle Street
    (10, 0): 31,  # Waterloo, Waterloo Road
    (10, 3): 19,  # Waterloo, Lower Marsh
    (11, 4): 7,   # Westminster, Millbank: empty, but only briefly (doesn't qualify)
}


def write(name, header, rows):
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


def status(bikes, empty_docks, capacity):
    if bikes == 0:
        return "Empty"
    if empty_docks == 0:
        return "Full"
    if bikes / capacity < 0.2:
        return "Low"
    return "OK"


def main():
    OUT.mkdir(exist_ok=True)
    write("crews.csv", ["CrewId", "CrewName", "Shift", "VanCapacity", "HomeDepot", "Supervisor"], CREWS)
    write("depots.csv", ["DepotName", "Area", "Latitude", "Longitude", "BikeStorageCapacity", "OpenHours"], DEPOTS)
    write("neighbourhoods.csv", ["NeighbourhoodName", "Borough", "Zone", "Priority", "CrewId"],
          [n[:5] for n in NEIGHBOURHOODS])
    write("vans.csv", ["VanId", "Registration", "CrewId", "DepotName", "BikeCapacity", "VanStatus"], VANS)
    write("van_maintenance.csv",
          ["TicketId", "VanId", "OpenedOn", "Issue", "Severity", "TicketStatus", "ExpectedFixedOn"], MAINTENANCE)

    stations, readings = [], []
    sid = 0
    for ni, (hood, _b, _z, _p, _c, lat, lon, pattern, streets) in enumerate(NEIGHBOURHOODS):
        for si, street in enumerate(streets):
            sid += 1
            bp = f"BP-{sid:03d}"
            capacity = rng.choice([15, 18, 20, 24, 27, 30, 36, 40])
            angle = rng.uniform(0, 2 * math.pi)
            dist = rng.uniform(0.002, 0.006)
            stations.append((bp, f"{street}, {hood}", street, hood,
                             round(lat + dist * math.sin(angle), 6), round(lon + dist * math.cos(angle) * 1.6, 6),
                             capacity, rng.choice([True, True, False]), rng.randint(2010, 2024)))

            empty_tail = HERO_EMPTY.get((ni, si))
            start_pct = rng.uniform(0.45, 0.75)
            if pattern == "fill":
                end_pct = rng.uniform(0.9, 1.05)
            elif pattern == "drain":
                end_pct = rng.uniform(0.12, 0.35)
            else:
                end_pct = start_pct + rng.uniform(-0.15, 0.15)
            if empty_tail is not None:
                end_pct = 0.0

            for m in range(MINUTES):
                t = START + timedelta(minutes=m)
                if empty_tail is not None and m >= MINUTES - empty_tail:
                    bikes = 0
                else:
                    span = MINUTES - (empty_tail or 0)
                    # S-curve between start and end, peaking around the 07:30-08:30 rush, plus noise
                    x = min(m / max(span, 1), 1.0)
                    pct = start_pct + (end_pct - start_pct) * (1 / (1 + math.exp(-10 * (x - 0.55))))
                    bikes = round(capacity * pct + rng.gauss(0, 1.0))
                    floor = 1 if empty_tail is not None else 0
                    bikes = max(floor, min(capacity, bikes))
                docks = capacity - bikes
                ebikes = min(bikes, max(0, round(bikes * 0.25 + rng.gauss(0, 0.6))))
                readings.append((t.strftime("%Y-%m-%dT%H:%M:%SZ"), bp, bikes, ebikes, docks,
                                 status(bikes, docks, capacity)))

    write("stations.csv", ["BikepointID", "StationName", "Street", "Neighbourhood", "Latitude", "Longitude",
                           "Capacity", "HasEBikeCharging", "InstalledYear"],
          [(a, b, c, d, e, f, g, "true" if h else "false", i) for (a, b, c, d, e, f, g, h, i) in stations])
    write("station_readings.csv", ["Timestamp", "BikepointID", "No_Bikes", "No_EBikes", "No_Empty_Docks", "Status"],
          readings)


if __name__ == "__main__":
    main()
