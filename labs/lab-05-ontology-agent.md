# Lab 05: Ask, Then Extend, with the Ontology Agent

**Duration:** 15 minutes
**Prerequisites:** Labs 01–03 complete (Lab 04's graph is nice to have, not required), and `van_maintenance.csv`
from the `data` folder at hand. Every question and request you send is in this lab, ready to copy.

**Learning objectives**
- Ask questions in natural language and **read the query** the agent ran (SQL, KQL or GQL).
- Answer the session's **hero question**, which needs live readings, rules and four hops of relationships at once.
- Use **Plan** mode to have the agent propose a change, review it in the **draft preview**, and apply it in **Act**
  mode.

## Before you begin

- [ ] The five business rules from Lab 03 are saved.
- [ ] You have K5's result from Lab 01 (the stations that are empty, and for how long). If the session started
      more than about an hour after you ran K3, run **K3** again now so the data ends *now* (in
      `BikeOpsEventhouse_queryset`):

  <details>
  <summary>K3 (same block as Lab 01 step 9)</summary>

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

  </details>

## Steps

### Part A — Warm up in Plan mode (4 min)

1. On the ontology's **Home** canvas, **click** **Ontology agent** in the ribbon. The chat opens on the right, in
   **Plan** mode (the toggle under the input box). Plan mode can query and propose, but never changes anything.

2. **Send** these warm-up questions, one at a time:

   ```text
   Explain this ontology in five bullet points.
   ```
   ```text
   Which crew services Kings Cross, and where is that crew based?
   ```
   ```text
   Which stations are Full right now?
   ```

   For each answer, **expand** the query the agent shows.

   > ✅ Expected result: Kings Cross → **North Loop**, based at **Kings Cross Depot** (a SQL or GQL query over the
   > Lakehouse tables). *Full right now*: 13 stations in Bankside, Canary Wharf and Holborn (a **KQL** query over
   > `StationReadings`). The agent picks the engine from the binding: you never told it where the readings live.

### Part B — The hero question (4 min)

3. **Send** the hero question:

   ```text
   Which Tier 1 neighbourhoods have stations that have been empty for more than 15 minutes? For each station, tell me how long it has been empty and how many bikes are needed. For each neighbourhood, name the responsible crew, its home depot, and which van can be dispatched.
   ```

   > ✅ Expected result (compare with your K5 result):
   >
   > | Neighbourhood | Stations empty > 15 min | Bikes needed | Crew, depot | Vans |
   > |---|---|---|---|---|
   > | Kings Cross | York Way (~38 min), Argyle Street (~24 min) | 14 + 18 | North Loop, Kings Cross Depot | V01, V02 |
   > | Waterloo | Waterloo Road (~31 min), Lower Marsh (~19 min) | 20 + 14 | Night Owls, Waterloo Depot | V09 (V10 is InService) |
   >
   > Millbank, Westminster is empty too, but only for ~7 minutes, so it's left out.

   > 💡 **Look at what you didn't have to say:** what "empty" means, what "Tier 1" means, how a station finds its
   > crew, how much to bring, which vans count. Those are the descriptions, relationships and rules you wrote in
   > Labs 02–03. If the answer is off, the fix is in the ontology, not in the prompt.

   <details>
   <summary>Troubleshooting — the answer is wrong or vague</summary>

   - **It includes Millbank**: the agent ignored the "more than 15 minutes" part. Ask *"Apply the Needs
     rebalancing rule"* and check that the rule text matches Lab 03 step 9.
   - **It lists every station**: it compared all readings instead of the latest one. Check the `StationReading`
     description ("Use the latest reading per station for "now" questions").
   - **Minutes are ~40–60 too high**: your data ended a while ago. Run **K3** and ask again.
   - **No answer, or an error on the first try**: ask again. The first queries after creating an ontology can be
     slow while it warms up.
   </details>

### Part C — Extend the ontology: maintenance tickets (7 min)

The control room just learned that "Available" in the van table doesn't mean a van is roadworthy: the workshop
keeps a separate list of maintenance tickets. Two of your "available" vans have serious faults.

4. **Open** `BikeOpsLakehouse` in a new browser tab. **Get data** → **Upload files** → `van_maintenance.csv`. Then
   **…** next to it → **Load to Tables** → **New table**, name `van_maintenance`, **Load**.

   > ✅ Expected result: table `van_maintenance` with six rows (tickets `T-1001`–`T-1006`).

5. **Back** in the ontology agent (still **Plan** mode), **send** this change request:

   ```text
   I uploaded a new table van_maintenance to BikeOpsLakehouse. Add an entity type called VanMaintenanceTicket bound to that table, with TicketId as the entity type key and all columns as properties. Add a relationship type hasTicket from Van (VanId) to VanMaintenanceTicket (VanId). Then change the business rule "Dispatchable van" to: A van can be dispatched when its VanStatus is Available and it has no Open maintenance ticket with Severity High. Link the rule to Van and VanMaintenanceTicket. Show me the plan first.
   ```

   > ✅ Expected result: the agent discovers the table, samples it, and replies with a plan plus validation
   > results. Nothing on the canvas changes yet.

6. **Click** the preview action in the agent's reply to open the **draft preview**. **Check**: one new entity type
   (marked as added), one new relationship from `Van`, one edited rule, nothing removed.

   > ⚠️ If the preview shows anything **removed** or renamed that you didn't ask for, don't apply it. Tell the agent
   > what's wrong (for example *"Don't change any existing entity types"*) and review the new preview.

   > 💡 *(optional)* Before you let an agent change a model, take a checkpoint: ontology supports named **version
   > history**, created by hand. If you see it in the ribbon, save a version called `Before maintenance tickets`.

7. **Switch** the toggle to **Act** and **send** `Apply the plan.`

   > ✅ Expected result: the agent reports what it applied, and `VanMaintenanceTicket` appears on the canvas,
   > connected to `Van` by `hasTicket`. **Switch back to Plan** straight away: it's the safe default.

8. **Send** the hero question again.

   > ✅ Expected result: the answer changes. **V02** has an open High ticket, so North Loop has only **V01**
   > (20 bikes for 32 needed: two trips). **V09** has an open High ticket and **V10** is InService, so **Night Owls
   > have no dispatchable van**. A good answer says so; a great one suggests another crew's available van. Same
   > question, better answer, because the *model of the business* improved.

<details>
<summary>Troubleshooting</summary>

- **The agent says it can't find van_maintenance**: the agent only sees items in this workspace, and the table
  must exist (step 4). Refresh the Lakehouse and ask again.
- **Act mode is greyed out**: you need Contributor (or higher) on the workspace. Viewers can query, not change.
- **The agent applied something you didn't want**: if you saved a named version before step 7 (see the tip there),
  restore it from the ontology's version history. Otherwise fix it by hand on the canvas (delete the extra item),
  or ask the agent in Plan mode for a patch that reverts it.
</details>

## Checkpoint

At the end of this lab:
- `BikeOpsLakehouse` has a sixth table, `van_maintenance`
- `BikeOpsOntology` has entity type **`VanMaintenanceTicket`**, relationship **`hasTicket`**, and the updated
  **`Dispatchable van`** rule
- The hero question's answer reflects the maintenance tickets

> 💡 The graph from Lab 04 doesn't know about `VanMaintenanceTicket` yet. *(stretch)* **Manage graph** → select
> it → **Continue** → **Materialize**.

Continue to [Lab 06: A data agent on top of the ontology](lab-06-data-agent.md).
