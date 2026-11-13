# Brand health survey (draft)

**Precedence.** `data/kpis.yaml` names what each answer measures and wins over this page. If they disagree, fix this page in the same session.

Eight questions, about three minutes (a goal). It feeds the survey KPIs in `data/kpis.yaml`. Sending it as Paul is Paul's queue item 5; until he does, those KPIs stay "not measured yet".

## Rules for running it

- **Anonymous.** No name or email is asked; the tool must not record either.
- **Order matters.** Questions 1 and 2 come before the brand name appears anywhere, including the invitation, its subject and the form's title. Use a neutral title such as "Colorado founder survey".
- **Two samples.** From our own lists, record the reading as `members`. For awareness and the masked asset, a clean reading needs people reached outside our lists (a partner's audience); record that as `outside`. Never pool the two.
- **The masked asset.** Show the lead shape asset alone: one color, no name, no lettering. For the before reading, that is the 2014 shield's mountains-in-a-C with its lettering removed; from `v3.0.0`, the v3 mark from `logo/`.
- **Coding.** A reviewer agent codes the open answers with one sheet and counts an unclear answer as "other".

## Questions

| # | Question | Answer | KPI |
|---|---|---|---|
| 1 | Name the groups or organizations that help founders build companies in Colorado. | Open text | `unaided-awareness` |
| 2 | *(Show the masked asset.)* Which organization uses this symbol? If you're not sure, say so. | Open text | `asset-fame`, `asset-uniqueness` |
| 3 | Before today, which of these had you heard of? | Checklist: Colorado Startups, four peers from `data/strategy.yaml`'s ecosystem map, "None of these" | `aided-awareness` |
| 4 | How likely are you to recommend Colorado Startups to a founder you know? | 0 to 10 | `member-nps` |
| 5 | "Colorado Startups shares accurate, useful information." | Strongly disagree 1 to strongly agree 5 | `trust` |
| 6 | "I plan to keep taking part in Colorado Startups over the next year." | Strongly disagree 1 to strongly agree 5 | `commitment` |
| 7 | Which best describes you? | Founder at the idea stage; founder building a company; building a team or looking for a role; investor; service provider; student or curious | segment for every KPI |
| 8 | What one thing should Colorado Startups do next? | Open text | read by the orchestrator; no KPI |

People who do not tick Colorado Startups in question 3 skip questions 4 to 6.

Question 7 folds the website's eight welcome doors into six choices, because Discord's onboarding keeps each question to about six options (https://support.discord.com/hc/en-us/articles/11074987197975, read by the research agent 2026-11-02).

## Scoring

- **Fame:** the share of all respondents who name Colorado Startups for the masked asset.
- **Uniqueness:** of every organization named for the masked asset, the share that is Colorado Startups.
- **NPS:** the share answering 9 or 10, minus the share answering 0 to 6 (https://www.netpromotersystem.com/about/measuring-your-net-promoter-score/, read 2026-11-02).
- **Trust and commitment:** the mean of the 1 to 5 answers.
