# Facilitator Guide

Everything the presenter needs that attendees don't: the talk track, timing, room management, what breaks and
what to do about it, and the dry run.

## Before the day

### Two weeks out

- Send [`prerequisites.md`](prerequisites.md) to the tenant admin. Get written confirmation of every tenant setting,
  the capacity SKU and region, and that the **Fabric Operations Agent** Teams app is allowed.
- Decide whether Lab 01 is **pre-work**. If it is, send attendees the link to Lab 01 with a note: *"Do Lab 01 up to
  the checkpoint; at the start of the session you'll run one KQL block again."* That buys 15 minutes.

### Within 72 hours: the dry run (mandatory)

Ontology, its agent and the operations agent are preview features and change from week to week. Do the whole
session once, as an attendee, in a fresh workspace on **the capacity the room will use**:

- [ ] Lab 01: all five Lakehouse tables load with the exact names; `StationReadingsRaw` gets `Timestamp` as
      `datetime`; K4 shows OK 43 / Full 13 / Low 11 / Empty 5.
- [ ] Lab 02: every UI label in the steps still exists (**+ Add entity type**, **Bind data**, **Entity type
      properties**, **Define entity type key**, **Add relationship**). Fix the lab text where the UI moved.
- [ ] Lab 03: **Overview** → **Rules** still exists; synonyms are still a field on entity metadata.
- [ ] Lab 04: note how long **Materialize** takes on this capacity. If it's over 5 minutes, tell attendees to
      start it at the end of Lab 03.
- [ ] Lab 05: the hero question gives the answer in [`../artifacts/agent-texts.md`](../artifacts/agent-texts.md)
      before and after the change request. Note the exact wording of the agent's preview action and Act toggle.
- [ ] Lab 06: **Add sources** → **Add an ontology** works; first answer arrives.
- [ ] Lab 07: the playbook contains an "empty for 10 minutes" rule, and the Teams message arrives. **Time how long
      it takes** after K6b: that's what you tell the room.
- [ ] **Record** your screen for Labs 04, 05 (Part C), 06 and 07. These are your fallbacks when a preview feature
      misbehaves live. Put the links in the table at the end of this guide.
- [ ] Open the Capacity Metrics app during the run and note the peak. Multiply by the number of attendees per
      capacity.

### On the day, before people arrive

- Your own workspace with the finished state of every lab, so you can put any checkpoint on the big screen.
- [`../artifacts/agent-texts.md`](../artifacts/agent-texts.md) answer key printed or on a second screen.
- Rerun **K3** in your own workspace so your demo data ends *now*.

## Talk track

### Kick-off (10 min, before Lab 01)

Keep it short; the labs carry the content. Suggested beats:

1. **The gap** (2 min). Show the K5 result from Lab 01: five rows, `BikepointID` and `EmptyMinutes`. Ask the room:
   *"Who do you call?"* Nobody can answer from this table. The data is correct and useless.
2. **What an ontology is** (3 min). A shared model of the business: the *things* (entity types), what identifies
   them (keys), how they connect (relationships), what words mean (descriptions, synonyms, rules), and where the
   data lives (bindings). It doesn't copy data. Draw the diagram from Lab 02 on the whiteboard.
3. **Where Fabric IQ sits** (3 min). RTI gets data in and reacts to thresholds. IQ adds meaning on top, so
   people and agents can ask and act in business terms. Ontology is the shared layer; graph is an optional
   execution engine for relationship questions; agents consume it: ontology agent (for modellers), data agent (for
   everybody), operations agent (watches and recommends).
4. **Today's promise** (2 min). *"By 1:30 you'll ask one question in plain English and get: which stations, how
   long, who goes, from where, with which van, and which van not to send."* Then Lab 01.

### Between labs (1–2 min each, max)

- **Before Lab 02**: *"Every relationship you draw is a join you'll never write again, and the agent won't get
  wrong."* Point out the one time-series entity type, and that it has no key.
- **Before Lab 03**: *"A schema says `No_Bikes: long`. The business says 'empty means nobody can rent a bike'.
  Agents only know what you write down."* Rules here are definitions, not triggers.
- **Before Lab 04**: The graph is opt-in and a snapshot of Lakehouse data. Eventhouse entities stay out. Use it
  when the *path* is the answer.
- **Before Lab 05**: Plan mode is read-only; Act mode writes. *"Let the agent do the typing, you do the
  reviewing."* The hero question is the pay-off for Labs 02–03.
- **Before Lab 06**: two agents, two jobs: ontology agent for builders, data agent for consumers (publishable to
  Teams/Copilot/Foundry). Same ontology underneath.
- **Before Lab 07**: callback to RTI: Activator rule vs. operations agent. Same signal, but the message already
  contains the decision, and a human approves.

### Wrap-up (5 min)

Use the five lines under *Wrap-up* in the [README](../README.md#wrap-up). End on: *"When an answer is wrong, fix
the model, not the prompt."* Then the clean-up steps: stop the operations agent.

## Timing and what to cut

| If you're behind at… | Cut |
|---|---|
| End of Lab 02 (> 0:55) | Lab 03 Part B (property and relationship metadata). Keep the `Neighbourhood` description and the five rules. |
| End of Lab 03 (> 1:07) | Lab 04 becomes a 3-minute demo on your screen. |
| End of Lab 05 (> 1:35) | Lab 06 Part C step 8 and the stretch. |
| End of Lab 06 (> 1:50) | Lab 07 as a demo with your recording. |

Lab 02 is where the room spreads out most (six bindings, six relationships). At ~18 minutes into it, put your
finished canvas on screen.

## Room management

- **Names are case sensitive** and appear in agent queries. Most "it doesn't work" in Labs 02–05 is a table name
  that's `Stations` instead of `stations` or a relationship on the wrong property. Check the spec first.
- **Agents warm up.** The first question to a new ontology agent or data agent can fail or be slow. Tell the room
  up front: *"If the first answer errors, ask again."*
- **Agent answers vary in wording.** Judge them against the facts in the answer key, not the phrasing. Celebrate
  differences: compare the queries two neighbours' agents generated.
- **Rebase drift.** K3 makes the data end at the moment it ran. An hour later, "now" questions see a one-hour gap:
  minutes-empty values stay right (they're computed within the data) but "in the last 15 minutes" questions find
  nothing. If answers look odd after Lab 04, have everyone run K3 again.

## Risks and fallbacks

| Risk | Signal | Fallback |
|---|---|---|
| Ontology item can't be created | "Unable to create the ontology item" | Tenant setting missing. Pair the attendee with a neighbour; fix after the session. |
| Ontology agent disabled | No **Ontology agent** button, or it says the feature is unavailable | Copilot / cross-geo setting. Lab 05 Part C: add `VanMaintenanceTicket` and `hasTicket` **by hand** with the steps from Lab 02 and edit the rule in **Rules**. The hero question then moves to Lab 06. |
| Graph unavailable or slow | **Manage graph** missing, or materialization > 10 min | Lab 04 as demo. Nothing later depends on the graph. |
| Data agent errors on every question | Run steps show source errors | Check the attendee can open both sources; wait 2–3 minutes after creation; **Refresh** the ontology context. Else demo. |
| Operations agent not allowed (trial capacity, setting, Teams app blocked) | Item missing or Start fails | Demo with your recording. |
| Venue network blocks GitHub downloads | Attendees can't get `data/` | Use the storage account mirror below, or USB sticks with `IQRedo-data.zip`. |
| Capacity throttling | Spinners everywhere, Eventhouse queries slow | Have everyone stop their operations agent; skip stretch steps; pair people up. |

### Optional: a public storage account mirror for the data

Not needed when attendees can reach GitHub. If the venue blocks it, put the files in an Azure Storage container
with anonymous read access and give attendees the URLs:

```bash
az storage account create -n <account> -g <rg> -l <region> --sku Standard_LRS --allow-blob-public-access true
az storage container create --account-name <account> -n iqredo --public-access blob
az storage blob upload-batch --account-name <account> -d iqredo -s data
# Files are then at https://<account>.blob.core.windows.net/iqredo/<file>.csv
```

Two ways attendees use it:

- **Lakehouse files**: download from the URL in the browser, then upload as in Lab 01 Part A.
- **Eventhouse readings**: in Lab 01 step 5, choose **Get data** → **Azure Storage** instead of **Local file**, and
  paste the URL of `station_readings.csv`. The rest of the wizard is the same.

Delete the account (or turn off public access) after the session.

## Fallback recordings

Fill in after the dry run.

| Lab | Recording |
|---|---|
| 04 Explore the graph | *link* |
| 05 Part C: agent extends the ontology | *link* |
| 06 Data agent | *link* |
| 07 Operations agent incl. Teams message | *link* |
