# Lab 06: A Data Agent on Top of the Ontology

**Duration:** 15 minutes
**Prerequisites:** Lab 05 complete. [`artifacts/agent-texts.md`](../artifacts/agent-texts.md) open (sections *Data
agent instructions* and *Data agent test questions*).

**Learning objectives**
- Create a **Fabric data agent** and add the **ontology as a context source**.
- Give the agent **instructions** that set tone and conventions, while business meaning stays in the ontology.
- Debug an answer with **run steps** and the downloaded **ontology context**.
- Know when to use the ontology agent and when to use a data agent.

## Before you begin

- [ ] `BikeOpsOntology` contains `VanMaintenanceTicket` (Lab 05).
- [ ] **Data agent** appears when you search **+ New item** in your workspace. If it doesn't, the data agent
      tenant settings are off: watch the facilitator's screen for this lab.

> 💡 **Two agents, two jobs.** The **ontology agent** lives *inside* the ontology and is for the people who build
> and maintain it: explain, query, propose changes. A **data agent** is a separate, shareable item for the people
> who just want answers. It can be published to Copilot, Teams or Microsoft Foundry, and it reuses the ontology as
> governed context instead of its own copy of the business rules.

## Steps

### Part A — Create the agent and add the ontology (4 min)

1. In your workspace, **click** **+ New item**, **search** for and **select** **Data agent**. **Name**:
   `BikeOpsDataAgent`. **Click** **Create**.

2. In the agent's **Sources** (Explorer on the left), **click** **Add sources** → **Add an ontology**. **Select**
   `BikeOpsOntology` and **confirm**.

3. **Expand** `BikeOpsOntology` in the Explorer.

   > ✅ Expected result: the ontology's entity types are listed, and under **Ontology data sources** the two
   > underlying items: `BikeOpsLakehouse` and `BikeOpsEventhouse`. The agent will generate SQL against the first and
   > KQL against the second, using your permissions on each.

   *Adapted from: [Use Ontology as context in Fabric data agent](https://learn.microsoft.com/fabric/data-science/data-agent-ontology-sources)*

### Part B — Instructions (3 min)

4. **Click** **Agent instructions** in the ribbon and **paste** the *Data agent instructions* block from
   `agent-texts.md`.

   > 💡 Read what's *in* the instructions and what isn't. They set conventions: names over IDs, "now" means the
   > latest reading, tables first, say which rule you applied. They don't define "empty", "Tier 1" or "dispatchable":
   > those live in the ontology, where the ontology agent, this agent and the operations agent in Lab 07 all read
   > the same definition. The last line, `Support group by in GQL`, works around a known preview issue with
   > aggregations over the graph.

### Part C — Test it (6 min)

5. In the chat pane, **ask** the hero question (from `agent-texts.md`).

   > ✅ Expected result: the same facts as the ontology agent's second answer in Lab 05: Kings Cross (York Way,
   > Argyle Street, 32 bikes, North Loop, only V01 dispatchable, two trips) and Waterloo (Waterloo Road, Lower
   > Marsh, 34 bikes, Night Owls, **no dispatchable van**, with a suggestion from another crew). This time as a
   > table first, because of your instructions.

   <details>
   <summary>Troubleshooting</summary>

   - **The first questions fail**: a new data agent needs a few minutes to initialise. Wait and ask again.
   - **It still offers V02 or V09**: the data agent reads the ontology context every 10 minutes. In the Explorer,
     open the ontology's **…** menu and **Refresh** the context, then ask again.
   - **"Can't access source"**: the agent uses *your* identity on the Lakehouse and Eventhouse. Check you can open
     both.
   </details>

6. **Open** the **run steps** under the answer. **Find** the generated query for each source (SQL for the
   Lakehouse, KQL for `StationReadings`).

7. **Ask** two or three of the *Data agent test questions*, for example:
   - `How many bikes does North Loop need to bring out in total, and can one van do it in a single trip?`
   - `Which depot should the van for Waterloo Road come from, and is there a van available there?`

8. **Open** the ontology's **…** menu in the Explorer → **Download ontology context**, and **skim** the file.

   > ✅ Expected result: a readable file with your entity types, descriptions, synonyms, relationships, rules and
   > bindings: exactly what the agent knows about the business. When an answer is wrong, compare its query with
   > this file. You fix the ontology, not the downloaded file.

### *(stretch)* Without the ontology

9. **Create** a second data agent, `BikeOpsDataAgentRaw`, and add the **Lakehouse and Eventhouse directly** as
   sources (no ontology, no instructions). **Ask** the hero question.

   > ✅ Expected result: it has to guess what "Tier 1", "empty for more than 15 minutes" and "dispatchable" mean,
   > and how a station finds its crew. Expect a partial answer, a wrong join, or a question back. That gap is what
   > the ontology fills.

<details>
<summary>Troubleshooting</summary>

- **Data agent isn't in + New item**: tenant setting for data agents is off (see
  [`docs/prerequisites.md`](../docs/prerequisites.md)).
- **Add an ontology isn't offered**: your Fabric version shows ontology as a source under a different label;
  look for **Ontology** in the source type list of **Add sources**.
</details>

## Checkpoint

At the end of this lab:
- Data agent **`BikeOpsDataAgent`** with `BikeOpsOntology` as its source and instructions from `agent-texts.md`
- The hero question answered with maintenance tickets taken into account
- You know where the run steps and the ontology context are

Continue to [Lab 07: An operations agent that watches](lab-07-operations-agent.md).
