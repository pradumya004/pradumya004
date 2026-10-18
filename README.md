<img src="assets/showreel.webp" width="100%" alt="Showreel: a BuzzBell message lands live in a second window, Pawse pulls two players into sync, Bowl n Sticks opens a cafe menu with no app or signup, and the Swastik Platinum tower rises at dusk.">

# Pradumya Gaurav

**Backend engineer. I turn manual ops work into automated pipelines: Node.js, queues, LLMs.**

SDE-1 at SpringWorks (background verification) · Bengaluru, IST (UTC+5:30) · open to remote roles and freelance work

[**Email me**](mailto:pradumya.official@gmail.com) · [LinkedIn](https://www.linkedin.com/in/pradumya2004/) · [Portfolio](https://pradumya-gaurav-portfolio.vercel.app/)

## Results in production

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/impact-dark.svg">
  <img src="assets/impact-light.svg" width="100%" alt="86% of reference checks start with no human. Manual tasks fell from 116 to 14 a day. 11K+ WhatsApp messages with about 90% of replies auto-routed. Turnaround 31% faster, 22.4 to 15.4 days.">
</picture>

- **Reference-check automation.** Checks start themselves, follow up every 24 hours, and an LLM on AWS Bedrock reads each reply and decides the next step.
- **WhatsApp on Meta Cloud API.** I proposed and built it: send pipeline, webhooks, BullMQ queues, template sync, an agent inbox and a reply classifier, rolled out behind flags from 1% to 100%.
- **AI in the pipeline.** A YOLO + OpenCV document auto-crop service (2.25x recall on 411 production images), and LLM triage that hands anything unsure to a human.

<details>
<summary><b>How one of these pipelines works</b></summary>

```mermaid
flowchart LR
  T[Case created] --> Q[(BullMQ queue)]
  Q --> S[Send: email / WhatsApp]
  S --> W[Reply arrives<br/>webhook or inbox]
  W --> L{LLM classifier<br/>AWS Bedrock}
  L -- confident --> A[Auto-close or<br/>next step]
  L -- unsure --> H[Human task]
  Q -. no reply in 24h .-> F[Follow-up]
  F --> S
```

Every step is a queued job with retries, rate limits and a feature flag per rollout stage. The model never closes a case it is unsure about.
</details>

<sub>Work code is private. Numbers come from production data.</sub>

## Selected work

<table>
<tr>
<td width="50%" valign="top">
<a href="https://buzz-bell-ycsb.vercel.app"><img src="https://github.com/pradumya004/BuzzBell/raw/main/docs/film.webp" width="100%" alt="BuzzBell: a message travels from one window to another and opens into the Postgres policy that guards it."></a>
<h3>BuzzBell</h3>
Realtime chat with no app server. Postgres Row Level Security is the whole authorization layer, and 34 SQL checks try to break it.
<p><img src="https://skillicons.dev/icons?i=react,ts,supabase,postgres,vitest" height="30" alt="React, TypeScript, Supabase, Postgres, Vitest"></p>
<a href="https://buzz-bell-ycsb.vercel.app">Live</a> · <a href="https://github.com/pradumya004/BuzzBell">Code</a> · <a href="https://github.com/pradumya004/BuzzBell/blob/main/docs/launch.mp4">Film</a>
</td>
<td width="50%" valign="top">
<a href="https://pawsetv.vercel.app"><img src="https://github.com/pradumya004/pawse/raw/master/docs/film.webp" width="100%" alt="Pawse: two players drift 350 ms apart, then the sync engine pulls them to 6 ms."></a>
<h3>Pawse</h3>
Watch a movie together from two cities. Clock sync and drift correction keep players 6 ms apart (350 ms before); the file goes peer to peer.
<p><img src="https://skillicons.dev/icons?i=react,nodejs,js,vercel" height="30" alt="React, Node.js WebSocket relay, WebRTC, Vercel"></p>
<a href="https://pawsetv.vercel.app">Live</a> · <a href="https://github.com/pradumya004/pawse">Code</a> · <a href="https://github.com/pradumya004/pawse/blob/master/docs/launch.mp4">Film</a>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://bowl-n-sticks.vercel.app"><img src="https://github.com/pradumya004/bowl-n-sticks/raw/main/docs/film.webp" width="100%" alt="Bowl n Sticks: a phone reads the table QR, the menu opens with no app, and one tap filters to veg."></a>
<h3>Bowl n Sticks</h3>
QR menu and admin panel for a cafe in Karwar, built for a freelance client. The owners run the menu themselves; RLS decides who can write. 83 tests.
<p><img src="https://skillicons.dev/icons?i=nextjs,supabase,postgres,tailwind,vercel" height="30" alt="Next.js, Supabase, Postgres, Tailwind, Vercel"></p>
<a href="https://bowl-n-sticks.vercel.app">Live</a> · <a href="https://github.com/pradumya004/bowl-n-sticks">Code</a> · <a href="https://github.com/pradumya004/bowl-n-sticks/blob/main/docs/launch.mp4">Film</a>
</td>
<td width="50%" valign="top">
<a href="https://swastik-platinum.vercel.app"><img src="https://github.com/pradumya004/Swastik-Platinum/raw/main/docs/film.webp" width="100%" alt="Swastik Platinum: the tower rises at dusk and the page scrolls from the crown to the street."></a>
<h3>Swastik Platinum</h3>
A real-estate site study, first built for an assessment, then rebuilt. The page climbs the tower floor by floor and reads units off the plans.
<p><img src="https://skillicons.dev/icons?i=react,tailwind,vite,vercel" height="30" alt="React, Tailwind, Vite, Vercel"></p>
<a href="https://swastik-platinum.vercel.app">Live</a> · <a href="https://github.com/pradumya004/Swastik-Platinum">Code</a> · <a href="https://github.com/pradumya004/Swastik-Platinum/blob/main/docs/launch.mp4">Film</a>
</td>
</tr>
</table>

## What I can build for you

<table>
<tr><td width="34%" valign="top"><b>Automate a manual workflow</b></td><td valign="top">The repetitive steps your team does by hand: queued jobs, follow-ups, webhooks, and LLM triage with a human fallback.</td></tr>
<tr><td width="34%" valign="top"><b>Messaging and integrations</b></td><td valign="top">WhatsApp Cloud API, email (SES), third-party APIs and webhooks, with retries and delivery tracking.</td></tr>
<tr><td width="34%" valign="top"><b>Postgres and realtime backends</b></td><td valign="top">Supabase or plain Postgres: schema, Row Level Security, realtime, and tests that try to break it.</td></tr>
<tr><td width="34%" valign="top"><b>Product frontends</b></td><td valign="top">React and Next.js apps that ship with the backend, not after it.</td></tr>
</table>

## Stack

<table>
<tr><td><b>Backend</b></td><td><img src="https://skillicons.dev/icons?i=nodejs,ts,express,redis,sequelize" height="36" alt="Node.js, TypeScript, Express, Redis (BullMQ), Sequelize"></td></tr>
<tr><td><b>Data</b></td><td><img src="https://skillicons.dev/icons?i=mysql,postgres,supabase,mongodb" height="36" alt="MySQL, PostgreSQL, Supabase, MongoDB"></td></tr>
<tr><td><b>Cloud and AI</b></td><td><img src="https://skillicons.dev/icons?i=aws,py,opencv,githubactions,vercel" height="36" alt="AWS (Bedrock, SES, S3), Python, OpenCV, GitHub Actions, Vercel"></td></tr>
<tr><td><b>Frontend</b></td><td><img src="https://skillicons.dev/icons?i=react,nextjs,tailwind,vite,vitest" height="36" alt="React, Next.js, Tailwind CSS, Vite, Vitest"></td></tr>
</table>

## Experience

<table>
<tr><td width="20%" valign="top"><b>SpringWorks</b></td><td width="26%" valign="top">SDE-1 · 2026 to now</td><td valign="top">Backend automation, queues, LLM routing, WhatsApp Cloud API. 148 merged PRs.</td></tr>
<tr><td width="20%" valign="top"><b>GetMax Solutions</b></td><td width="26%" valign="top">Software Engineer Intern · 2025</td><td valign="top">Built <a href=\"https://www.getmaxhealthcare.com\">getmaxhealthcare.com</a> end to end and internal tools for US healthcare ops.</td></tr>
<tr><td width="20%" valign="top"><b>IIIT Vadodara</b></td><td width="26%" valign="top">B.Tech CSE · 2026</td><td valign="top">Teaching assistant for Design and Analysis of Algorithms (200+ students).</td></tr>
</table>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/pradumya004/pradumya004/output/activity-dark.svg">
  <img src="https://raw.githubusercontent.com/pradumya004/pradumya004/output/activity-light.svg" width="100%" alt="Contribution graph, animated">
</picture>

**Have a process that eats hours every week?** [Email me](mailto:pradumya.official@gmail.com) with what it is, and I'll tell you how I'd automate it.
