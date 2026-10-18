<img src="assets/banner.webp" width="100%" alt="A reference-check task leaves a human's to-do list. The pipeline emails the previous manager, the reply arrives, a classifier labels it confirmed_employment 0.97, and back in the list the task ticks itself closed while the open count falls from 116 to 14.">

<img src="https://readme-typing-svg.demolab.com?font=Inter&weight=500&size=21&duration=2600&pause=2200&color=8B949E&vCenter=true&width=860&height=34&lines=86%25+of+reference+checks+now+start+without+a+human;11K%2B+WhatsApp+messages%2C+about+90%25+of+replies+routed+automatically;Rebuilding+BuzzBell+on+Postgres+Row+Level+Security" alt="86% of reference checks now start without a human. 11K+ WhatsApp messages, about 90% of replies routed automatically. Rebuilding BuzzBell on Postgres Row Level Security.">

## Pradumya Gaurav

Backend engineer in Bengaluru. I turn manual ops work into automated pipelines with Node.js, queues and LLMs. SDE-1 at SpringWorks, a background-verification platform. Before that I built [getmaxhealthcare.com](https://www.getmaxhealthcare.com) and internal tools at GetMax Solutions. Open to remote.

### Production work

- **Reference-check automation.** Auto-initiation, a 24h follow-up cadence, an in-product verifier form, and LLM classification of manager replies on AWS Bedrock. 86% of checks now start without a human, manual tasks fell from 116 to 14 a day, turnaround dropped 31%.
- **WhatsApp on Meta Cloud API.** Proposed and built it: send pipeline, webhooks, BullMQ queues, template sync, an agent inbox and a reply classifier, rolled out behind flags from 1% to 100%. 11K+ messages in 10 weeks, about 90% of replies routed with no agent.
- **AI in the verification pipeline.** A YOLO + OpenCV document auto-crop service (2.25x recall on a 411-image production set) and LLM classification of free text that fails closed to a human.

<sub>Work code is private. Numbers come from production data.</sub>

### Projects

**[BuzzBell](https://github.com/pradumya004/BuzzBell)**: realtime chat on Postgres. Two guests in a DM: typing, delivery and reactions arrive live, and Row Level Security decides who reads what. 34 SQL checks try to break it.
<br><sub>React · TypeScript · Supabase Realtime · Postgres RLS · Vitest</sub>

<a href="https://github.com/pradumya004/BuzzBell"><img src="assets/buzzbell.webp" width="100%" alt="Two BuzzBell windows side by side: Riya types, Sam sees 'Riya Kapoor is typing', the message lands, Sam reacts, replies, and Riya reacts back."></a>

**[Pawse](https://github.com/pradumya004/pawse)** · [live](https://pawsetv.vercel.app): watch movies together from two places. Play, pause and seek sync over a WebSocket relay; the movie file goes peer to peer over WebRTC. The two players stayed about 0.1 s apart in a recorded test.
<br><sub>React · Node.js ws relay · WebRTC DataChannel · Chrome MV3</sub>

<a href="https://github.com/pradumya004/pawse"><img src="assets/pawse.webp" width="100%" alt="Two Pawse players side by side showing the same frame and the same timecode while the host plays, pauses and seeks."></a>

<a href="https://github.com/pradumya004/bowl-n-sticks"><img src="assets/bowl.webp" width="200" align="right" alt="The Bowl n Sticks menu on a phone: the veg filter, then a search for ramen."></a>

**[Bowl n Sticks](https://github.com/pradumya004/bowl-n-sticks)** · [live](https://bowl-n-sticks.vercel.app): QR menu and admin panel for a cafe in Karwar (freelance client). One permanent QR per table; owners edit dishes, photos and order themselves, and Postgres Row Level Security decides who can write. 83 tests on the server actions.
<br><sub>Next.js 16 · Supabase · Postgres RLS · dnd-kit</sub>

<br clear="right">

### Experience

- **SpringWorks** · SDE-1 · backend automation, queues, LLM routing, WhatsApp Cloud API. 148 merged PRs.
- **GetMax Solutions** · built getmaxhealthcare.com end to end and internal tools for US healthcare ops.
- **IIIT Vadodara** · B.Tech CSE (2026); teaching assistant for Design and Analysis of Algorithms.

### Stack

Node.js · TypeScript · Express · BullMQ · Redis · MySQL · PostgreSQL · AWS (SES, Bedrock, S3) · React · Next.js · Supabase · WebSockets · WebRTC

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/pradumya004/pradumya004/output/activity-dark.svg">
  <img src="https://raw.githubusercontent.com/pradumya004/pradumya004/output/activity-light.svg" width="100%" alt="Contribution graph, animated">
</picture>

[pradumya.official@gmail.com](mailto:pradumya.official@gmail.com) · [LinkedIn](https://www.linkedin.com/in/pradumya2004/) · [Portfolio](https://pradumya-gaurav-portfolio.vercel.app/)
