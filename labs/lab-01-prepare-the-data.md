# Lab 01: Prepare the Data

**Duration:** 15 minutes (or do it before the session; see the tip below)
**Prerequisites:** a Fabric workspace of your own on a paid capacity (see the [README](../README.md#prerequisites)),
and the [`data/`](../data/) folder of this repository on your laptop.

**Learning objectives**
- Land **master data** (stations, neighbourhoods, crews, depots, vans) as managed Delta tables in a Lakehouse.
- Land **time-series data** (station readings) in an Eventhouse table.
- Understand why an ontology needs both, and why it doesn't copy either of them.

> 💡 **Do this before the session if you can.** Lab 01 is plain data loading. If you finish it the day before, run
> K3 again at the start of the session (step 13) so the readings end "now" again.

## Before you begin

- [ ] You have downloaded the data: on the repository's GitHub page, **click** **Code** → **Download ZIP**, unzip
      it, and find the `data` folder.
- [ ] The folder contains seven CSV files: `stations.csv`, `neighbourhoods.csv`, `crews.csv`, `depots.csv`,
      `vans.csv`, `van_maintenance.csv`, `station_readings.csv`.
- [ ] Your workspace shows **+ New item**, and **Ontology (preview)** appears when you search for it there.
      If it doesn't, stop here and tell the facilitator: a tenant setting is missing.

## The scenario in one paragraph

You are the data team of a city bike-share scheme in London. Seventy-two docking stations report how many bikes
they hold every minute. The operations team doesn't think in `BikepointID`s and rows: they think *"Argyle
Street has been empty for twenty minutes, that's North Loop's patch, their van leaves from Kings Cross"*. Today
you teach Fabric to think the same way.

## Steps

### Part A — Master data in a Lakehouse (8 min)

1. In your workspace, **click** **+ New item**, **search** for **Lakehouse**, **type** `BikeOpsLakehouse`,
   keep **Lakehouse schemas** checked, and **click** **Create**.

2. In the Lakehouse ribbon, **click** **Get data** → **Upload files**. **Select these five files** (not the other
   two): `stations.csv`, `neighbourhoods.csv`, `crews.csv`, `depots.csv`, `vans.csv`. **Click** **Upload**.

   > ✅ Expected result: **Files** in the Explorer lists the five CSV files.

   > ⚠️ Don't upload `van_maintenance.csv` yet: Lab 05 uses it to show the ontology agent extending the ontology.
   > `station_readings.csv` goes to the Eventhouse in Part B.

3. For **each** of the five files: **click** **…** next to the file name → **Load to Tables** → **New table**.
   Keep the proposed table name (the file name without `.csv`, all lower case), keep **Use header for column
   names** checked, and **click** **Load**.

   | File | Table name |
   |---|---|
   | `stations.csv` | `stations` |
   | `neighbourhoods.csv` | `neighbourhoods` |
   | `crews.csv` | `crews` |
   | `depots.csv` | `depots` |
   | `vans.csv` | `vans` |

   > ✅ Expected result: **Tables** → **dbo** lists the five tables. **Click** `stations`: 72 rows, with columns
   > `BikepointID`, `StationName`, `Street`, `Neighbourhood`, `Latitude`, `Longitude`, `Capacity`,
   > `HasEBikeCharging`, `InstalledYear`.

   <details>
   <summary>Troubleshooting</summary>

   - **The table name has a different spelling**: delete the table (**…** → **Delete**) and load it again with the
     name from the table above. The ontology binds by table name.
   - **Load to Tables is greyed out**: wait for the upload to finish and refresh the Explorer.
   - **Why it matters that column names have no spaces**: Fabric turns on Delta *column mapping* for column names
     with spaces or special characters, and the ontology's graph can't read such tables. Every CSV here uses plain
     names on purpose.
   </details>

### Part B — Readings in an Eventhouse (7 min)

4. **Go back** to the workspace, **click** **+ New item**, **select** **Eventhouse**, **type**
   `BikeOpsEventhouse`, and **click** **Create**.

   > ✅ Expected result: the Eventhouse opens with a KQL database also called `BikeOpsEventhouse`, and the
   > workspace now also lists `BikeOpsEventhouse_queryset`.

5. In the Explorer, **select** the KQL database `BikeOpsEventhouse`. In the ribbon, **click** **Get data** →
   **Local file**.

6. In the **Get data** wizard:
   - **Select or create a destination table**: **+ New table** → `StationReadingsRaw`
   - **Browse for files** → `station_readings.csv`
   - **Click** **Next**. On **Inspect the data**: **Format** = **CSV**, and switch **First row is column header**
     on. Check that `Timestamp` shows type **datetime** (open the column's drop-down to change it if not).
   - **Click** **Finish**, wait for the green ticks, and **click** **Close**.

   > ✅ Expected result: the database lists table `StationReadingsRaw` with roughly 13,000 rows.

7. **Open** `BikeOpsEventhouse_queryset` from the workspace. **Check** that the database selector at the top says
   `BikeOpsEventhouse`. The KQL blocks below are labelled K1–K5; copy them from here.

   > 💡 The editor runs **only the block your cursor is in**, where blocks are separated by blank lines. Paste a
   > block, run it, paste the next.

8. **Run** **K1** (did the upload land?) and then **K2** (column types), as two separate blocks.

   **K1**
   ```kql
   StationReadingsRaw
   | summarize Rows = count(), Stations = dcount(BikepointID), Oldest = min(Timestamp), Newest = max(Timestamp)
   ```

   **K2**
   ```kql
   StationReadingsRaw
   | getschema
   | project ColumnName, ColumnType
   ```

   > ✅ Expected result: K1 shows `Rows` 12960 and `Stations` 72. K2 lists `Timestamp` as `datetime` and the three
   > count columns as `long` or `int`.

9. **Run** **K3**. It copies the readings into a new table `StationReadings` and shifts every timestamp so the
   newest reading is *now*.

   **K3**
   ```kql
   .set-or-replace StationReadings <|
       let shift = now() - toscalar(StationReadingsRaw | summarize max(todatetime(Timestamp)));
       StationReadingsRaw
       | project Timestamp = todatetime(Timestamp) + shift,
                 BikepointID = tostring(BikepointID),
                 No_Bikes = tolong(No_Bikes),
                 No_EBikes = tolong(No_EBikes),
                 No_Empty_Docks = tolong(No_Empty_Docks),
                 Status = tostring(Status)
   ```

   > 💡 **Why rebase?** The file holds three hours of readings from a fixed morning. Agents answer questions like
   > *"right now"* and *"in the last 15 minutes"* against the clock, so the data has to end at the clock. This is
   > the only "trick" in the session: everything else is real Fabric behaviour.

10. **Run** **K4**: the current state of every station, counted by status.

    **K4**
    ```kql
    StationReadings
    | summarize arg_max(Timestamp, *) by BikepointID
    | summarize Stations = count() by Status
    ```

    > ✅ Expected result: four rows: **OK 43**, **Full 13**, **Low 11**, **Empty 5**.

11. **Run** **K5** and **keep the result** (screenshot or leave the tab open). It lists the stations that are
    empty now, and for how long.

    **K5**
    ```kql
    StationReadings
    | summarize LastNotEmpty = maxif(Timestamp, Status != "Empty"), arg_max(Timestamp, Status, No_Bikes) by BikepointID
    | where Status == "Empty"
    | extend EmptyMinutes = datetime_diff('minute', Timestamp, LastNotEmpty)
    | order by EmptyMinutes desc
    ```

    > ✅ Expected result: five stations, `EmptyMinutes` 38, 31, 24, 19 and 7. This is the KQL answer to the
    > question you'll ask the agents in Labs 05 and 06. Notice what K5 *can't* tell you: which of these matter
    > most, who should go, and with which van. That needs business context, which is what the ontology adds.

### Part C — If you did Lab 01 before the session

12. Nothing to redo in the Lakehouse.

13. **Run** **K3** (step 9) again at the start of the session. It rebuilds `StationReadings` from the raw table so
    the data ends *now* again. Then **run** **K4** (step 10) to confirm the four statuses.

<details>
<summary>Troubleshooting</summary>

- **K1 fails with "Failed to resolve table"**: the table name in step 6 isn't exactly `StationReadingsRaw`, or the
  queryset points at another database. Fix the selector at the top of the queryset.
- **K1 shows 12961 rows and a weird first row**: **First row is column header** was off. Drop the table
  (`.drop table StationReadingsRaw`) and repeat step 6.
- **`Timestamp` is a string**: K3 converts it with `todatetime()`, so you can continue. K1's `Oldest`/`Newest`
  just sort as text.
</details>

## Checkpoint

At the end of this lab, your workspace contains:
- Lakehouse **`BikeOpsLakehouse`** with tables `stations` (72), `neighbourhoods` (12), `crews` (6), `depots` (6),
  `vans` (10)
- Eventhouse **`BikeOpsEventhouse`** with tables `StationReadingsRaw` and **`StationReadings`** (12,960 rows ending
  now)
- Queryset `BikeOpsEventhouse_queryset`
- `van_maintenance.csv` still on your laptop, not uploaded

Continue to [Lab 02: Build the ontology](lab-02-build-the-ontology.md).
