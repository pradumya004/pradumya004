<img src="assets/banner.webp" width="100%" alt="A reference-check task leaves a human's to-do list. The pipeline emails the previous manager, the reply arrives, a classifier labels it confirmed_employment 0.97, and back in the list the task ticks itself closed while the open count falls from 116 to 14.">

# Pradumya Gaurav

**Backend engineer. I turn manual ops work into automated pipelines: Node.js, queues, LLMs.**

SDE-1 at SpringWorks, a background-verification platform, in Bengaluru. Open to remote.

<img src="https://readme-typing-svg.demolab.com?font=Inter&weight=500&size=20&duration=2600&pause=2200&color=8B949E&vCenter=true&width=860&height=32&lines=86%25+of+reference+checks+start+without+a+human;11K%2B+WhatsApp+messages%2C+about+90%25+of+replies+routed+automatically;Pawse+sync%3A+6+ms+median+gap%2C+down+from+350+ms" alt="86% of reference checks start without a human. 11K+ WhatsApp messages, about 90% of replies routed automatically. Pawse sync: 6 ms median gap, down from 350 ms.">

## What I build at work

**Reference-check automation.** Checks start themselves, follow up every 24 hours, and an LLM on AWS Bedrock reads the manager's reply. 86% of checks now start without a human, manual tasks fell from 116 to 14 a day, and turnaround dropped 31%.

**WhatsApp on Meta Cloud API.** I proposed it and built it: send pipeline, webhooks, BullMQ queues, template sync, an agent inbox and a reply classifier, rolled out behind flags from 1% to 100%. 11K+ messages in 10 weeks, about 90% of replies routed with no agent.

**AI in the verification pipeline.** A YOLO + OpenCV document auto-crop service (2.25x recall on 411 production images), and LLM classification of free text that falls back to a human when unsure.

<sub>Work code is private. Numbers come from production data.</sub>

## Selected work

### BuzzBell

<a href="https://buzz-bell-ycsb.vercel.app"><img src="assets/buzzbell.webp" width="100%" alt="Two BuzzBell windows: Riya's message has landed in Sam's window. Caption: Live in every tab."></a>

Realtime chat with no app server. The browser talks straight to Postgres, Row Level Security is the whole authorization layer, and 34 SQL checks try to break it.

<sub>React · TypeScript · Supabase Realtime · Postgres RLS · Vitest</sub><br>
[Live](https://buzz-bell-ycsb.vercel.app) · [Code](https://github.com/pradumya004/BuzzBell) · [Film](https://github.com/pradumya004/BuzzBell/blob/main/docs/launch.mp4)

### Pawse

<a href="https://github.com/pradumya004/pawse"><img src="assets/pawse.webp" width="100%" alt="Two Pawse players showing the same frame and timecode, badge reads IN SYNC 6MS. Caption: One frame."></a>

Watch a movie together from two places. Clock sync and drift correction keep the players 6 ms apart (350 ms before) under 150 ms of simulated delay. The file goes peer to peer over WebRTC.

<sub>React · Node.js WebSocket relay · WebRTC DataChannel · Chrome extension</sub><br>
[Live](https://pawsetv.vercel.app) · [Code](https://github.com/pradumya004/pawse) · [Film](https://github.com/pradumya004/pawse/blob/master/docs/launch.mp4)

### Bowl n Sticks

<a href="https://bowl-n-sticks.vercel.app"><img src="assets/bowl.webp" width="100%" alt="The Maggi Meals card from the Bowl n Sticks menu: 129 rupees, highest selling, 26g protein, three add-ons."></a>

QR menu and admin panel for a cafe in Karwar, built for a freelance client. One permanent QR per table, the owner edits dishes and photos, and Postgres RLS decides who can write. 83 tests.

<sub>Next.js · Supabase · Postgres RLS · dnd-kit</sub><br>
[Live](https://bowl-n-sticks.vercel.app) · [Code](https://github.com/pradumya004/bowl-n-sticks) · [Film](https://github.com/pradumya004/bowl-n-sticks/blob/main/docs/launch.mp4)

### Swastik Platinum

<a href="https://swastik-platinum.vercel.app"><img src="assets/swastik.webp" width="100%" alt="The Swastik Platinum tower at dusk rising in front of the word Platinum."></a>

A site study I first built for a frontend assessment, then rebuilt. The page climbs the tower floor by floor, and the floor picker reads units off the developer's plans. Unofficial.

<sub>React · Tailwind CSS · scroll-driven layers · Playwright</sub><br>
[Live](https://swastik-platinum.vercel.app) · [Code](https://github.com/pradumya004/Swastik-Platinum) · [Film](https://github.com/pradumya004/Swastik-Platinum/blob/main/docs/launch.mp4)

## Experience

**SpringWorks** · SDE-1 · 2026<br>
Backend automation, queues, LLM routing, WhatsApp Cloud API. 148 merged PRs.

**GetMax Solutions** · Software Engineer Intern · 2025<br>
Built [getmaxhealthcare.com](https://www.getmaxhealthcare.com) end to end, plus internal tools for US healthcare ops.

**IIIT Vadodara** · B.Tech CSE, 2026<br>
Teaching assistant for Design and Analysis of Algorithms.

## Stack

| | |
|---|---|
| Backend | Node.js, TypeScript, Express, BullMQ, Redis, REST, webhooks |
| Data | MySQL, PostgreSQL, Supabase |
| AI and cloud | AWS Bedrock, SES, S3, LLM classification, YOLO, OpenCV |
| Frontend | React, Next.js, Tailwind CSS |
| Realtime | WebSockets, WebRTC, Supabase Realtime |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/pradumya004/pradumya004/output/activity-dark.svg">
  <img src="https://raw.githubusercontent.com/pradumya004/pradumya004/output/activity-light.svg" width="100%" alt="Contribution graph, animated">
</picture>

[pradumya.official@gmail.com](mailto:pradumya.official@gmail.com) · [LinkedIn](https://www.linkedin.com/in/pradumya2004/) · [Portfolio](https://pradumya-gaurav-portfolio.vercel.app/)
