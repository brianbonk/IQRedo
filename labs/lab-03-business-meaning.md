# Lab 03: Give It Business Meaning

**Duration:** 12 minutes
**Prerequisites:** Lab 02 complete. Every text you need is in this lab, ready to copy (use the copy button on each
grey block).

**Learning objectives**
- Add **descriptions** and **synonyms** so people and agents can use their own words.
- Document what a **property** means, not just its type.
- Write **business rules** in natural language and link them to ontology concepts.

## Before you begin

- [ ] `BikeOpsOntology` has six entity types and six relationship types.

> 💡 **Why bother?** A schema says `No_Bikes: long`. A business says *"a station is empty when nobody can rent a
> bike there, and Tier 1 areas need someone on it within 15 minutes"*. Agents only know the second if you write it
> down. Everything in this lab is plain text, and it's what turns a correct query into a useful answer.

## Steps

### Part A — Entity type descriptions and synonyms (5 min)

1. On the canvas, **select** `Station` → **View Entity Type details**. On the **Configure** page, **scroll** to
   **Entity metadata**.

2. **Enter** the **Description**, then add the **Synonyms** one at a time, then **click** **Update**:

   **Description**
   ```text
   A public docking station where customers rent and return bikes. Capacity is the number of docks.
   ```
   **Synonyms**: `docking station`, `dock`, `bike point`, `bikepoint`

3. **Repeat** steps 1–2 for the other five entity types:

   **`Neighbourhood`**: the one that matters most for the hero question, because it carries the tier definition.
   ```text
   An operational area of the city. Priority Tier 1 neighbourhoods require a response within 15 minutes; Tier 2 within 60 minutes.
   ```
   **Synonyms**: `area`, `district`, `zone`

   **`Crew`**
   ```text
   A rebalancing crew that moves bikes between stations and depots with vans. Each crew services its own neighbourhoods.
   ```
   **Synonyms**: `team`, `rebalancing crew`, `van crew`

   **`Depot`**
   ```text
   A depot where vans park and spare bikes are stored.
   ```
   **Synonyms**: `warehouse`, `base`, `yard`

   **`Van`**
   ```text
   A van that carries bikes between depots and stations. BikeCapacity is the number of bikes it can carry in one trip.
   ```
   **Synonyms**: `vehicle`, `truck`, `rebalancing van`

   **`StationReading`**
   ```text
   One reading per station per minute: how many bikes and empty docks the station has at that moment. Use the latest reading per station for "now" questions.
   ```
   **Synonyms**: `reading`, `telemetry`, `station status`, `occupancy`

   > ✅ Expected result: all six entity types show a description and synonyms on their **Configure** page.

### Part B — Property and relationship descriptions (3 min)

4. **…** next to `StationReading` → **Bind data** → **Entity type properties**. Next to each property below,
   **click** **Metadata**, **paste** the description, **click** **Update**. When all four are done, **click**
   **Save**.

   **`No_Bikes`**
   ```text
   Bikes available to rent at the station at this moment, including e-bikes.
   ```
   **`No_EBikes`**
   ```text
   Of No_Bikes, how many are e-bikes.
   ```
   **`No_Empty_Docks`**
   ```text
   Free docks where a customer can return a bike.
   ```
   **`Status`**
   ```text
   Empty = 0 bikes; Full = 0 empty docks; Low = under 20 % of capacity; otherwise OK.
   ```

5. *(skip if you're behind)* **Do the same** for these two:

   **`Van`** → **`VanStatus`**
   ```text
   Available = parked at its depot and free to dispatch; InService = already out on a run.
   ```
   **`Station`** → **`Capacity`**
   ```text
   Total number of docks at the station.
   ```

6. On the canvas, **select** the `servicedBy` relationship. In its configuration, **scroll** to **Metadata**,
   **click** **Edit**, **paste** the description, **click** **Update**. **Repeat** for `basedAt` and `hasReading`.

   **`servicedBy`**
   ```text
   The crew responsible for refilling and emptying every station in this neighbourhood.
   ```
   **`basedAt`**
   ```text
   The depot a crew starts its shift from and returns bikes to.
   ```
   **`hasReading`**
   ```text
   Minute-by-minute readings from the station's docks.
   ```

### Part C — Business rules (4 min)

7. In the **Explorer**, **expand** **Overview** and **select** **Rules**. **Click** **+ Create rule**.

8. **Enter** the first rule, **Save**, then **Cancel** to close it:

   - **Name**: `Empty station`
   - **Definition**:
     ```text
     A station is empty when its latest reading has No_Bikes = 0. A station has been empty for N minutes when every reading in the last N minutes has No_Bikes = 0.
     ```
   - **Linked ontology concepts**: `Station`, `StationReading`

9. **Click** **New rule** for each of the other four. Copy the definitions exactly; they're written so an agent
   can turn them into a query.

   **Name**: `Needs rebalancing` · **Linked concepts**: `Station`, `StationReading`, `Neighbourhood`
   ```text
   A station needs rebalancing when it has been empty for more than 15 minutes, or when its latest reading has Status Low and it is in a Tier 1 neighbourhood.
   ```

   **Name**: `Responsible crew` · **Linked concepts**: `Station`, `Neighbourhood`, `Crew`, `Depot`
   ```text
   The crew responsible for a station is the crew that services the station's neighbourhood. That crew's home depot is where the van leaves from.
   ```

   **Name**: `Bikes needed` · **Linked concepts**: `Station`, `StationReading`
   ```text
   Bikes needed to rebalance a station = round(Capacity × 0.5) − No_Bikes from its latest reading. A refill brings a station to half full.
   ```

   **Name**: `Dispatchable van` · **Linked concepts**: `Van`, `Crew`
   ```text
   A van can be dispatched when its VanStatus is Available. One van can carry up to BikeCapacity bikes per trip.
   ```

   > ✅ Expected result: the **Business rules** page lists five rules, each with its linked concepts.

   > 💡 **These rules don't fire anything.** In the ontology they're *definitions* that agents read to ground their
   > answers ("which stations need rebalancing?"). Lab 07 shows an operations agent that *watches* the data and
   > acts on the same language. Compare with the RTI Activator rule *"No_Bikes < 1 for 5 minutes"*: same idea, but
   > that one knew nothing about tiers, crews or vans. And notice that `Dispatchable van` is naive on purpose:
   > Lab 05 makes it smarter.

<details>
<summary>Troubleshooting</summary>

- **I can't find Rules**: in the Explorer, the **Overview** node is collapsed by default. Expand it.
- **Update is greyed out**: a required field is empty, or the text didn't change. Click into the box and type.
- **I'm behind**: the description on `Neighbourhood` (tiers) and the five rules are what the hero question needs.
  Skip the other descriptions and synonyms.
</details>

## Checkpoint

At the end of this lab, `BikeOpsOntology` also has:
- Descriptions and synonyms on all six entity types
- Property descriptions on `StationReading` (at least `No_Bikes` and `Status`)
- Descriptions on `servicedBy`, `basedAt`, `hasReading`
- Business rules **`Empty station`**, **`Needs rebalancing`**, **`Responsible crew`**, **`Bikes needed`**,
  **`Dispatchable van`**

Continue to [Lab 04: Explore the graph](lab-04-explore-the-graph.md).
