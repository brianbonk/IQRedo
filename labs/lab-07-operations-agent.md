# Lab 07: An Operations Agent That Watches

**Duration:** 10 minutes
**Prerequisites:** Labs 01–05 complete. Microsoft Teams on this account (desktop, web or phone). The agent
instructions and the KQL are in this lab, ready to copy.

**Learning objectives**
- Create an **operations agent** with the ontology as its **knowledge**.
- Read the **playbook** the agent generates from your instructions and the ontology.
- Trigger a realistic incident and receive the agent's recommendation in **Teams**.

## Before you begin

- [ ] **Operations agent** appears when you search **+ New item**. Operations agents don't run on trial
      capacities. If it's missing, follow along on the facilitator's screen.

> 💡 **From RTI to IQ in one picture.** In Real-Time Intelligence you'd build an Activator rule: *"`No_Bikes` < 1
> for 5 minutes → email"*. It fires, and someone still has to work out where the station is, whose patch it is,
> and which van to send. An operations agent watches the same data **through the ontology**, so its message can
> already say *"Bayswater Road, Hyde Park, empty 12 min, West Wheels from Paddington Depot, take V06, 18 bikes"*,
> and it asks before it acts.

## Steps

### Part A — Create and configure the agent (4 min)

1. In your workspace, **click** **+ New item**, **search** for and **select** **Operations agent**. **Name**:
   `BikeOpsOperationsAgent`. **Click** **Create**.

2. On **Agent setup**:
   - **Agent instructions**: **paste**:

     ```text
     You monitor the bike-share network for the control room.

     Goal: no station in the network stays empty for more than 10 minutes without the responsible crew being told.

     - A station is empty when its latest StationReading has No_Bikes = 0.
     - When a station has been empty for 10 minutes or more, message me with: the station name, its neighbourhood and its priority tier, how long it has been empty, the responsible crew and its home depot, how many bikes are needed (round(Capacity x 0.5) - No_Bikes), and a dispatchable van from that crew.
     - Tier 1 neighbourhoods first.
     - Don't message again about the same station until it has had bikes again.
     ```
   - **Knowledge**: **click** **Add data** and **select** `BikeOpsOntology`.
   - **Actions**: leave empty. By default the agent messages you in Teams.
   - **Click** **Save**.

3. **Click** **Generate playbook**.

   > ✅ Expected result: a playbook listing the concepts the agent monitors and the rules it evaluates. **Check**
   > that it refers to *ontology* names (`Station`, `StationReading`, `No_Bikes`, `Crew`, `Van`), not raw tables, and
   > that there's a rule for "empty for 10 minutes or more".

   <details>
   <summary>Troubleshooting</summary>

   - **The playbook has no rule about empty stations**: make the instruction more explicit (for example add
     *"Check every station's latest StationReading."*), **Save**, and **Generate playbook** again.
   - **Generate playbook fails**: wait a minute and retry; the agent needs the ontology to be reachable with your
     identity.
   </details>

4. **Install** the **Fabric Operations Agent** app in Microsoft Teams (Teams → **Apps** → search *Fabric Operations
   Agent* → **Add**). The agent can only reach you once the app is installed.

5. **Click** **Start** in the agent's toolbar.

### Part B — Make something happen (4 min)

6. In `BikeOpsEventhouse_queryset`, **run** these four blocks one at a time, in order. **K3** makes the data end
   *now* again; **K6a** and **K6b** make Bayswater Road, Hyde Park (`BP-043`) empty for the last 12 minutes; **K7**
   checks it.

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

   **K6a**: remove BP-043's normal readings for the last 12 minutes
   ```kql
   .delete table StationReadings records <| StationReadings | where BikepointID == "BP-043" and Timestamp > ago(12m)
   ```

   **K6b**: add 12 one-minute "Empty" readings ending now
   ```kql
   .set-or-append StationReadings <|
       range i from 0 to 11 step 1
       | project Timestamp = now() - i * 1m, BikepointID = "BP-043", No_Bikes = long(0), No_EBikes = long(0),
                 No_Empty_Docks = long(36), Status = "Empty"
   ```

   **K7**
   ```kql
   StationReadings
   | where BikepointID == "BP-043"
   | top 15 by Timestamp desc
   ```

   > ✅ Expected result: **K7** shows `BP-043` with `No_Bikes` 0 and `Status` Empty for the last 12 minutes.
   > That's Bayswater Road, Hyde Park: a Tier 2 station, so not part of the hero answer, but well past the agent's
   > 10-minute goal.

7. **Wait** for the agent's message in Teams. Depending on how often the agent evaluates, this takes from a minute
   to several minutes. Meanwhile, look at the agent's activity in Fabric.

   > ✅ Expected result: a Teams message that names **Bayswater Road, Hyde Park**, about 12 minutes empty, **West
   > Wheels** from **Paddington Depot**, about **18 bikes**, van **V06**. It may also report the stations from the
   > hero question (Kings Cross, Waterloo): they're still empty in the data. When it proposes something, you
   > answer **Yes** or **No**: the agent recommends, a human approves.

### Part C — Stop it (1 min)

8. In `BikeOpsOperationsAgent`, **click** **Stop**. An operations agent keeps evaluating, and consuming capacity,
   until you stop it.

<details>
<summary>Troubleshooting</summary>

- **No message after 10 minutes**: check the agent is **started**, the Teams app is installed for the same
  account, and that K7 shows the incident. Then check the agent's run history in Fabric for errors.
- **"Operations agent isn't supported on this capacity"**: trial capacities aren't supported. Watch the
  facilitator's run, or the recording linked in the facilitator guide.
- **The agent messages about many stations**: that's the data, not a fault: five stations are empty. Tighten the
  instructions (for example *"Only Tier 1 neighbourhoods"*), **Save**, **Generate playbook**, **Start**.
</details>

## Checkpoint

At the end of this lab:
- Operations agent **`BikeOpsOperationsAgent`** with `BikeOpsOntology` as knowledge, a generated playbook, and
  **stopped**
- A Teams message about Bayswater Road (or the facilitator's, if your tenant doesn't allow operations agents)

Continue to the [wrap-up and clean-up](../README.md#wrap-up) in the README.
