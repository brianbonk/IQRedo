# Lab 03: Give It Business Meaning

**Duration:** 12 minutes
**Prerequisites:** Lab 02 complete. [`artifacts/ontology-spec.md`](../artifacts/ontology-spec.md) open in another
tab (sections *Entity type metadata*, *Property metadata*, *Relationship metadata*, *Business rules*).

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

2. **Enter** the **Description** and **Synonyms** from the spec:
   - **Description**: `A public docking station where customers rent and return bikes. Capacity is the number of docks.`
   - **Synonyms**: `docking station`, `dock`, `bike point`, `bikepoint` (add them one at a time)
   - **Click** **Update**.

3. **Repeat** for the other five entity types, using the *Entity type metadata* table in the spec. The one that
   matters most for the hero question is `Neighbourhood`, because its description carries the tier definition:

   ```text
   An operational area of the city. Priority Tier 1 neighbourhoods require a response within 15 minutes; Tier 2 within 60 minutes.
   ```

   > ✅ Expected result: each entity type's **Configure** page shows a description; five of them show synonyms.

### Part B — Property and relationship descriptions (3 min)

4. **…** next to `StationReading` → **Bind data** → **Entity type properties**. Next to `No_Bikes`, **click**
   **Metadata**, **enter** the description from the spec, **click** **Update**. **Repeat** for `No_EBikes`,
   `No_Empty_Docks` and `Status`, then **click** **Save**.

5. **Do the same** for `Van` → `VanStatus` and `Station` → `Capacity` *(skip if you're behind; these two are
   nice-to-have)*.

6. On the canvas, **select** the `servicedBy` relationship. In its configuration, **scroll** to **Metadata**,
   **click** **Edit**, **enter**:

   ```text
   The crew responsible for refilling and emptying every station in this neighbourhood.
   ```

   **Click** **Update**. **Repeat** for `basedAt` and `hasReading` with the texts from the spec.

### Part C — Business rules (4 min)

7. In the **Explorer**, **expand** **Overview** and **select** **Rules**. **Click** **+ Create rule**.

8. **Enter** the first rule and **Save**, then **Cancel** to close it:
   - **Name**: `Empty station`
   - **Definition**:
     ```text
     A station is empty when its latest reading has No_Bikes = 0. A station has been empty for N minutes when every reading in the last N minutes has No_Bikes = 0.
     ```
   - **Linked ontology concepts**: `Station`, `StationReading`

9. **Click** **New rule** and add the other four from the spec's *Business rules* table: `Needs rebalancing`,
   `Responsible crew`, `Bikes needed`, `Dispatchable van`. Copy the definitions exactly; they're written so an
   agent can turn them into a query.

   > ✅ Expected result: the **Business rules** page lists five rules, each with its linked concepts.

   > 💡 **These rules don't fire anything.** In the ontology they're *definitions* that agents read to ground their
   > answers ("which stations need rebalancing?"). Lab 07 shows an operations agent that *watches* the data and
   > acts on the same language. Compare with the RTI Activator rule *"No_Bikes < 1 for 5 minutes"*: same idea, but
   > that one knew nothing about tiers, crews or vans.

<details>
<summary>Troubleshooting</summary>

- **I can't find Rules**: in the Explorer, the **Overview** node is collapsed by default. Expand it.
- **Update is greyed out**: a required field is empty, or the text didn't change. Click into the box and type.
- **I'm behind**: the descriptions on `Neighbourhood` (tiers) and the five rules are what the hero question needs.
  Skip property and relationship metadata.
</details>

## Checkpoint

At the end of this lab, `BikeOpsOntology` also has:
- Descriptions on all six entity types, synonyms on five
- Property descriptions on `StationReading` (at least `No_Bikes` and `Status`)
- Descriptions on `servicedBy`, `basedAt`, `hasReading`
- Business rules **`Empty station`**, **`Needs rebalancing`**, **`Responsible crew`**, **`Bikes needed`**,
  **`Dispatchable van`**

Continue to [Lab 04: Explore the graph](lab-04-explore-the-graph.md).
