# Prerequisites

Forward this page to the tenant admin **at least two weeks before** the session. Everything here has to be in
place before the day: none of it can be fixed live in the room.

Fabric IQ moves fast. Re-check every link below in the week of the session; the labs were written against the
"new experience" of ontology (preview) as documented in November 2026.

## 1. Tenant settings (Fabric admin)

In Fabric: **OneLake catalog** (or **Settings**) → **Govern** → **Configurations** → **Tenant settings**. Enable for
the attendees' security group, or the whole organisation:

| Setting | Needed for | Reference |
|---|---|---|
| **Users can create Fabric items** | Everything, including the ontology "new experience" | [Ontology tenant settings](https://learn.microsoft.com/fabric/iq/ontology/overview-tenant-settings) |
| **Users can create ontology (preview) items** | Lab 02 onwards | same |
| **Users can use Copilot and other features powered by Azure OpenAI** | Ontology agent (Lab 05), data agent (Lab 06), operations agent (Lab 07) | [Enable Copilot in Fabric](https://learn.microsoft.com/fabric/fundamentals/copilot-enable-fabric) |
| **Data agent** tenant settings (data agent item types) | Lab 06 | [Data agent tenant settings](https://learn.microsoft.com/fabric/data-science/data-agent-tenant-settings) |
| **Operations agent** tenant setting | Lab 07 | [Operations agent prerequisites](https://learn.microsoft.com/fabric/real-time-intelligence/operations-agent#prerequisites) |
| **Data sent to Azure OpenAI can be processed outside your capacity's geographic region…** | Only if the capacity is **outside** the US and the EU Data Boundary: the ontology agent is off by default there | [Ontology agent: regions](https://learn.microsoft.com/fabric/iq/ontology/how-to-use-ontology-agent#regions) |

Graph (Lab 04) must be available in the capacity's region:
[graph region availability](https://learn.microsoft.com/fabric/graph/overview#region-availability). If it isn't, Lab
04 is a demo and everything else still works.

## 2. Capacity

- A **paid** Fabric capacity: **F2 or higher**, or Power BI Premium **P1+**. **Trial capacities don't support
  operations agents**, and the Copilot-backed agents need a paid SKU.
- Plan the size for the room: every attendee runs a small Eventhouse, a Lakehouse, a graph materialization and
  three agents. One F64 for 25–30 attendees is a reasonable starting point; **verify it in the dry run** (see the
  facilitator guide) with the Capacity Metrics app open.
- Eventhouses keep a minimum compute running. After the session, attendees (or you) delete the workspaces or
  at least stop the operations agents.

## 3. Workspaces and accounts

- One workspace per attendee, on that capacity, with the attendee as **Contributor** or higher. (Viewers can't
  create items or apply ontology changes.)
- Each attendee signs in with an account that has **Microsoft Teams** (Lab 07) and can install the **Fabric
  Operations Agent** Teams app. If your organisation blocks custom Teams apps, allow that app or make Lab 07 a demo.

## 4. On the attendee's laptop

- A modern browser (Edge or Chrome), signed in to Fabric with the session account.
- The `data` folder of this repository (GitHub **Code** → **Download ZIP**).
- Nothing to install.

## 5. Quick self-test (attendee, 2 minutes)

In your workspace, **+ New item**, and search for each of: **Lakehouse**, **Eventhouse**, **Ontology (preview)**,
**Data agent**, **Operations agent**. All five should appear. If one doesn't, tell the organiser which.
