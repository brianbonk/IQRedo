# Lab 02: Build the Ontology by Hand

**Duration:** 25 minutes
**Prerequisites:** Lab 01 complete. Open [`artifacts/ontology-spec.md`](../artifacts/ontology-spec.md) in another
tab: every name you type is in its tables.

**Learning objectives**
- Create an **ontology (preview)** item and add **entity types**.
- **Bind** entity types to Lakehouse tables (master data) and to an Eventhouse table (time series), without
  copying any data.
- Set an **entity type key**, and know why the graph needs it.
- Model **relationship types** by matching a property on one entity type to a property on another.

## Before you begin

- [ ] `BikeOpsLakehouse` has the five tables from Lab 01, and `StationReadings` exists in `BikeOpsEventhouse`.
- [ ] You can explain the difference between the two kinds of data you loaded: *things* that change rarely
      (stations, crews, vans) and *readings* that arrive every minute.

## What you're building

Six entity types and six relationship types:

```
                       servicedBy                basedAt
 Station ──locatedIn──▶ Neighbourhood ─────────▶ Crew ─────────▶ Depot
    │                                              ▲                ▲
    │ hasReading                       assignedTo  │                │ parkedAt
    ▼                                              └───── Van ──────┘
 StationReading   (Eventhouse, minute by minute)
```

Everything except `StationReading` comes from the Lakehouse. (Same picture, drawn properly:
[`docs/ontology-diagram.svg`](../docs/ontology-diagram.svg). The dashed `VanMaintenanceTicket` comes in Lab 05.)

## Steps

### Part A — Create the ontology (2 min)

1. In your workspace, **click** **+ New item**, **search** for and **select** **Ontology (preview)**. **Name**:
   `BikeOpsOntology`, **Location**: your workspace. **Click** **Create**.

   > ✅ Expected result: the ontology opens on a **Get started** page that offers **Start with Ontology agent**.
   > Don't use the agent yet: you build this one by hand so you know what the agent does for you in Lab 05.

   <details>
   <summary>Troubleshooting — "Unable to create the ontology item"</summary>

   The tenant settings **Users can create ontology (preview) items** and **Users can create Fabric items** must be
   on. Tell the facilitator; see [`docs/prerequisites.md`](../docs/prerequisites.md).
   </details>

   *Adapted from: [Ontology tutorial part 1: Create an ontology](https://learn.microsoft.com/fabric/iq/ontology/tutorial-1-create-ontology)*

### Part B — The first entity type, step by step: `Station` (6 min)

2. From the top ribbon, **click** **+ Add entity type**. **Type** `Station` and **click** **Add Entity Type**.

   > ✅ Expected result: `Station` appears on the configuration canvas and in the **Explorer**.

3. On the canvas (or in the Explorer), **click** **…** next to `Station` → **Bind data**.

4. **Click** **Add** to add a data source. In the OneLake catalog, **expand** `BikeOpsLakehouse` → `dbo`,
   **select** the `stations` table, and **click** **Select table**.

5. **Click** **Entity type properties** in the left pane. The table's nine columns are proposed as properties.
   **Don't change anything**. **Click** **Create**.

   > ✅ Expected result: a banner says **Entity type updated successfully**.

6. **Click** **Cancel** to close the binding page. You're on the **Configure** page of `Station`, which lists the
   nine properties and their binding to `stations`.

7. On the same **Configure** page, **click** **Define entity type key**, **select** `BikepointID`, and **click**
   **Save**.

   > 💡 **The key is what makes "a station" a thing.** It tells the ontology which property identifies one row as
   > one real-world station. Without a key the entity type works for queries, but it can't become a node in the
   > graph (Lab 04). Readings don't get a key: one station has thousands of them.

### Part C — Four more Lakehouse entity types (8 min)

8. **Click** **Home** to return to the canvas. **Repeat steps 2–7** for each row below. Every one binds to a table
   in `BikeOpsLakehouse` → `dbo` and keeps all columns as properties.

   | Entity type | Table | Entity type key |
   |---|---|---|
   | `Neighbourhood` | `neighbourhoods` | `NeighbourhoodName` |
   | `Crew` | `crews` | `CrewId` |
   | `Depot` | `depots` | `DepotName` |
   | `Van` | `vans` | `VanId` |

   > ✅ Expected result: the Explorer lists five entity types, each with a key.

   <details>
   <summary>Troubleshooting</summary>

   - **Bind data opens an empty catalog**: wait a few seconds; the OneLake catalog loads lazily. Use its search
     box and type the table name.
   - **I forgot the key on one of them**: open it from the Explorer → **View Entity Type details** →
     **Define entity type key**.
   </details>

### Part D — The time-series entity type: `StationReading` (3 min)

9. **Click** **Home**, **+ Add entity type**, **type** `StationReading`, **Add Entity Type**.

10. **…** next to `StationReading` → **Bind data** → **Add**. In the OneLake catalog, **expand**
    `BikeOpsEventhouse` → the KQL database `BikeOpsEventhouse`, **select** the `StationReadings` table (not
    `StationReadingsRaw`), and **click** **Select table**.

11. **Click** **Entity type properties**, keep the six proposed properties, **click** **Create**, then **Cancel**.
    **Don't** define a key.

    > 💡 **Nothing was copied.** `Station` reads from the Lakehouse, `StationReading` from the Eventhouse, at
    > query time. When a new reading lands in `StationReadings`, the ontology agent and the data agent see it on
    > their next query. (The materialized *graph* in Lab 04 is the exception: it's a snapshot you refresh.)

    *Adapted from: [Data binding in ontology](https://learn.microsoft.com/fabric/iq/ontology/how-to-bind-data)*

### Part E — Relationship types (6 min)

12. In the **Explorer**, **select** `Station`, then **click** **Add relationship** on the ribbon. **Enter**:
    - **Relationship type name**: `locatedIn`
    - **Origin entity type**: `Station`
    - **Target entity type**: `Neighbourhood`
    - **Click** **Create**.

13. The relationship appears on the canvas. **Select** it to open its configuration:
    - **Origin entity type** → **Property**: `Neighbourhood`
    - **Target entity type** → **Property**: `NeighbourhoodName`
    - **Click** **Save**, then **Cancel**.

    > ✅ Expected result: a banner says **Successfully updated the relationship type**, and `Station`'s
    > **Configure** page lists `locatedIn` under **Relationships**.

    > 💡 This is a join you'll never write again. The rule "a station's `Neighbourhood` matches a neighbourhood's
    > `NeighbourhoodName`" now lives in one governed place, with a business name, and every agent uses it.

14. **Click** **Home** and **repeat steps 12–13** for the other five:

    | Relationship type | Origin (property) | Target (property) |
    |---|---|---|
    | `servicedBy` | `Neighbourhood` (`CrewId`) | `Crew` (`CrewId`) |
    | `basedAt` | `Crew` (`HomeDepot`) | `Depot` (`DepotName`) |
    | `assignedTo` | `Van` (`CrewId`) | `Crew` (`CrewId`) |
    | `parkedAt` | `Van` (`DepotName`) | `Depot` (`DepotName`) |
    | `hasReading` | `Station` (`BikepointID`) | `StationReading` (`BikepointID`) |

    > ✅ Expected result: the **Full ontology** view of the canvas shows six entity types connected by six
    > relationships, the same shape as the diagram at the top of this lab.

    <details>
    <summary>Troubleshooting</summary>

    - **The property drop-down is empty**: the entity type has no binding yet. Go back and bind it (Part C/D).
    - **Two relationships with the same name**: rename one. Duplicate relationship names break natural-language
      queries in the current preview.
    - **I picked the wrong direction**: delete the relationship (**…** → **Delete**) and create it again.
      Direction matters for how agents read it: *Van assignedTo Crew*, not *Crew assignedTo Van*.
    </details>

### Part F — Quick check (*optional, 1 min*)

15. **Select** `Station` → **View Entity Type details** → **Instances** tab.

    > ✅ Expected result: 72 rows from `stations`. If the tab is empty, see troubleshooting below.

    <details>
    <summary>Troubleshooting — no instances</summary>

    Confirm the source table exists with the exact column names, and that you have access to the Lakehouse. A
    `403` means your identity can't read `BikeOpsLakehouse`. Wait a minute and refresh: the first load can be slow.
    </details>

<!-- facilitator: Part E is where people fall behind. At ~18 minutes in, put the finished canvas on the big screen
     and let people copy the remaining relationships from the table. -->

## Checkpoint

At the end of this lab, `BikeOpsOntology` contains:
- Entity types **`Station`**, **`Neighbourhood`**, **`Crew`**, **`Depot`**, **`Van`** (each bound to a Lakehouse
  table and with an entity type key) and **`StationReading`** (bound to the Eventhouse table `StationReadings`, no
  key)
- Relationship types **`locatedIn`**, **`servicedBy`**, **`basedAt`**, **`assignedTo`**, **`parkedAt`**,
  **`hasReading`**

Continue to [Lab 03: Give it business meaning](lab-03-business-meaning.md).
