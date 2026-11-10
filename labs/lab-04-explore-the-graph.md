# Lab 04: Explore the Graph

**Duration:** 13 minutes
**Prerequisites:** Lab 03 complete. All five Lakehouse entity types have an entity type key (Lab 02 step 7–8).

**Learning objectives**
- Browse **entity instances** behind an entity type.
- **Materialize** a graph from the ontology, and know what can and can't go into it.
- Answer a **multi-hop** question with a **path query**.

## Before you begin

- [ ] `Station`, `Neighbourhood`, `Crew`, `Depot`, `Van` each show a key on their **Configure** page.

> 💡 **The graph is optional, and a snapshot.** The ontology answers most questions by querying the sources
> directly (SQL on the Lakehouse, KQL on the Eventhouse). A materialized graph copies the *Lakehouse* entities
> into Fabric Graph so relationship-heavy questions ("what's connected to what, how many hops away?") are cheap.
> It doesn't refresh by itself, and today it can't hold Eventhouse-bound entity types, so `StationReading` stays
> out.

## Steps

### Part A — Start the materialization first (3 min)

1. On the ontology's **Home** canvas, **click** **Manage graph** in the ribbon.

2. The **Configure Graph** page opens with **Use the entire Ontology**. In **Entities**, **check** the **Status**
   column:
   - `Station`, `Neighbourhood`, `Crew`, `Depot`, `Van`: **Eligible**
   - `StationReading`: not eligible (hover the status to read why: eventhouse source)

   Make sure all five eligible ones are selected. **Click** **Continue**.

3. On **Projection Summary**, **check** that you see five entities, then **click** **Materialize**.

   > ✅ Expected result: materialization starts. It takes a few minutes; carry on with Part B meanwhile.

   <details>
   <summary>Troubleshooting</summary>

   - **An entity shows "Ineligible: no key"**: open it → **View Entity Type details** → **Define entity type
     key** (`Station` → `BikepointID`, `Neighbourhood` → `NeighbourhoodName`, `Crew` → `CrewId`,
     `Depot` → `DepotName`, `Van` → `VanId`), save, and open **Manage graph** again.
   - **Manage graph isn't in the ribbon**: graph isn't available in your tenant or region. Do Part B, then watch
     the facilitator's screen for Part C.
   </details>

### Part B — Instances while you wait (4 min)

4. **Select** `Van` on the canvas → **View Entity Type details** → **Instances** tab.

   > ✅ Expected result: ten vans, `V01`–`V10`, with `VanStatus` Available or InService.

5. **Do the same** for `StationReading`.

   > ✅ Expected result: readings from the Eventhouse, with `Timestamp` values from the last three hours. The
   > ontology is reading the KQL table live; nothing was imported.

6. **Switch** the canvas between **Full ontology**, **Lineage** and **Relationship** views, with `Crew` selected in
   the Explorer. **Notice**: the *Relationship* view shows `Crew` with everything one hop away: the
   neighbourhoods it services, the vans assigned to it, the depot it's based at.

### Part C — Ask the graph a multi-hop question (6 min)

7. When materialization has finished, **go back** to the **Home** canvas and **click** **Explore graph** in the
   ribbon (it appears once the graph exists).

8. On the right of the graph queryset, **click** the puzzle-piece icon to open **Components**. **Select** the
   nodes `Station`, `Neighbourhood`, `Crew`, `Depot` and the edges between them.

   > ✅ Expected result: the canvas draws stations around their neighbourhoods, neighbourhoods around crews,
   > crews next to their depots.

9. **Click** **Path query** in the ribbon and **confirm** **Switch** if asked. **Enter**:
   - **Start node**: `Station`
   - **End node**: `Depot`
   - **Filter start node**: `StationName` = `Argyle Street, Kings Cross`
   - **Max hops**: `3`
   - **Click** **Run**.

   > ✅ Expected result: one path: **Argyle Street, Kings Cross → Kings Cross → North Loop → Kings Cross Depot**.
   > That's the answer to *"where does the van for this station come from?"*, found by following business
   > relationships instead of writing three joins.

10. **Change** the start filter to `Waterloo Road, Waterloo` and **run** again.

    > ✅ Expected result: **Waterloo Road, Waterloo → Waterloo → Night Owls → Waterloo Depot**.

### *(stretch)* GQL in the code editor

11. **Switch** the graph queryset to the code editor and **run**:

    ```gql
    MATCH (s:Station)-[]->(n:Neighbourhood)-[]->(c:Crew)-[]->(d:Depot)
    RETURN d.DepotName AS Depot, c.CrewName AS Crew, count(s) AS Stations
    GROUP BY d.DepotName, c.CrewName
    ```

    > ✅ Expected result: six rows, one per crew and depot, each with 12 stations. The `-[]->` patterns match any
    > edge, so the query works whatever label Fabric gave each edge. Look in **Components** to see the labels.

<details>
<summary>Troubleshooting</summary>

- **Path query returns nothing**: the start filter must match the value exactly, including the comma. Or the graph
  was materialized before a relationship was saved: **Manage graph** → check **Entity usage** for *changed*
  entities and materialize again.
- **Explore graph opens but shows no nodes**: open **Components** and select nodes; the canvas starts empty.
</details>

## Checkpoint

At the end of this lab:
- `BikeOpsOntology` has a **materialized graph** with five node types (`StationReading` isn't in it), and the
  workspace lists the graph model item next to the ontology
- You have run a path query from a station to its depot

> 💡 **Remember for later:** the graph is a snapshot. When the Lakehouse tables change, refresh it: workspace →
> graph model → **…** → **Schedule** → **Refresh now** (or set a schedule). The Eventhouse readings are never in
> it, so they never go stale.

Continue to [Lab 05: Ask, then extend with the ontology agent](lab-05-ontology-agent.md).
