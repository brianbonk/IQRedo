# Agent texts and questions

Copy-paste blocks for Labs 05, 06 and 07, plus the answer key the facilitator checks the agents against.

## The hero question

This is the question the whole session builds towards. It needs the live readings (eventhouse), the
business definitions (rules), and four hops of business relationships (Station → Neighbourhood → Crew → Depot /
Van) at the same time.

```text
Which Tier 1 neighbourhoods have stations that have been empty for more than 15 minutes? For each station, tell me how long it has been empty and how many bikes are needed. For each neighbourhood, name the responsible crew, its home depot, and which van can be dispatched.
```

## Ontology agent warm-up questions (Lab 05, Plan mode)

```text
Explain this ontology in five bullet points.
```

```text
Which crew services Kings Cross, and where is that crew based?
```

```text
How many stations does each crew look after?
```

```text
Which stations are Full right now?
```

## Ontology agent change request (Lab 05, Plan mode, then Act mode)

```text
I uploaded a new table van_maintenance to BikeOpsLakehouse. Add an entity type called VanMaintenanceTicket bound to that table, with TicketId as the entity type key and all columns as properties. Add a relationship type hasTicket from Van (VanId) to VanMaintenanceTicket (VanId). Then change the business rule "Dispatchable van" to: A van can be dispatched when its VanStatus is Available and it has no Open maintenance ticket with Severity High. Link the rule to Van and VanMaintenanceTicket. Show me the plan first.
```

Then, after reviewing the preview and switching to **Act**:

```text
Apply the plan.
```

## Data agent instructions (Lab 06)

Paste into **Agent instructions** of `BikeOpsDataAgent`.

```text
You are the duty assistant in the control room of a city bike-share scheme.

- Answer in business terms: stations by StationName, crews by CrewName, vans by VanId and Registration.
- "Now", "currently" and "right now" mean the latest StationReading per station. Never sum readings over time when the question is about the current state.
- Apply the ontology's business rules (Empty station, Needs rebalancing, Responsible crew, Bikes needed, Dispatchable van) exactly as defined. Say which rule you applied.
- When you recommend a van, check that it is dispatchable. If a crew has no dispatchable van, say so clearly and suggest the nearest other crew's available van instead.
- If one van can't carry all the bikes needed, say how many trips it takes.
- Show results as a table first, then at most three sentences of explanation.
- Support group by in GQL.
```

## Data agent test questions (Lab 06)

```text
Which stations need rebalancing right now, and which crew is responsible for each?
```

```text
How many bikes does North Loop need to bring out in total, and can one van do it in a single trip?
```

```text
Which depot should the van for Waterloo Road come from, and is there a van available there?
```

```text
Compare the number of e-bikes available in Tier 1 and Tier 2 neighbourhoods right now.
```

## Operations agent instructions (Lab 07)

Paste into **Agent instructions** of `BikeOpsOperationsAgent`.

```text
You monitor the bike-share network for the control room.

Goal: no station in the network stays empty for more than 10 minutes without the responsible crew being told.

- A station is empty when its latest StationReading has No_Bikes = 0.
- When a station has been empty for 10 minutes or more, message me with: the station name, its neighbourhood and its priority tier, how long it has been empty, the responsible crew and its home depot, how many bikes are needed (round(Capacity x 0.5) - No_Bikes), and a dispatchable van from that crew.
- Tier 1 neighbourhoods first.
- Don't message again about the same station until it has had bikes again.
```

## Answer key (facilitator)

All figures assume the committed `data/` files and that `StationReadings` was built with K3.

**Current state** (K4): OK 43, Full 13, Low 11, Empty 5 stations (72 stations, 1,915 docks, 903 bikes of which 229
e-bikes).

**Hero question** (K5 shows the empty minutes):

| Neighbourhood (tier) | Station | Empty for | Capacity | Bikes needed | Crew | Depot | Vans |
|---|---|---|---|---|---|---|---|
| Kings Cross (Tier 1) | York Way, Kings Cross (BP-001) | 38 min | 27 | 14 | North Loop (C01) | Kings Cross Depot | V01, V02: Available, 20 bikes each |
| Kings Cross (Tier 1) | Argyle Street, Kings Cross (BP-003) | 24 min | 36 | 18 | | | |
| Waterloo (Tier 1) | Waterloo Road, Waterloo (BP-061) | 31 min | 40 | 20 | Night Owls (C06) | Waterloo Depot | V09 Available (16 bikes); V10 InService |
| Waterloo (Tier 1) | Lower Marsh, Waterloo (BP-064) | 19 min | 27 | 14 | | | |

- Millbank, Westminster (BP-071) is empty too, but only for 7 minutes: a correct answer leaves it out.
- An agent may count 37 instead of 38 minutes (readings vs. minutes between readings). Both are fine.
- Kings Cross needs 32 bikes; one 20-bike van can't do it in one trip. Waterloo needs 34; V09 carries 16.
- **After Lab 05** (maintenance tickets added): V02 has an open High ticket (T-1001), so North Loop has only
  **V01**. V09 has an open High ticket (T-1002) and V10 is InService, so Night Owls have **no dispatchable van**;
  a good answer says so and suggests another crew's available van (for example V03 at Southwark Depot, 24 bikes,
  or V04 at Liverpool Street Depot).
- `Needs rebalancing` also catches the two **Low** stations in Kings Cross (Tier 1): Caledonian Road (BP-002,
  5 of 36) and Goods Way (BP-005, 2 of 15).

**Warm-up questions**: Kings Cross → North Loop (C01), based at Kings Cross Depot. Every crew looks after 12
stations (2 neighbourhoods × 6). Full right now: 5 in Bankside, 5 in Canary Wharf, 3 in Holborn.

**Lab 07 incident** (K6a/K6b): Bayswater Road, Hyde Park (BP-043), Tier 2, empty 12 minutes, capacity 36 → 18
bikes needed. Crew West Wheels (C04), Paddington Depot, van V06 (Available, 20 bikes; its open ticket T-1004 is
Medium, so it's still dispatchable).
