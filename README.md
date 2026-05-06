# Cleo

A weekly growth strategy agent. Cleo reads what's happening in your business, scans the web for what's happening outside, and writes a one-page brief that decides the focus, the experiment to run, and the direction for the week ahead.

She runs every Monday morning, before you start work. The brief lands in your repo as a markdown file. Five minutes to read. Specific enough to act on tomorrow.

> **Status:** Free to use. Take the code, point it at your business. MIT licensed.

## What you get every Monday

- **A weekly growth brief** at `briefs/YYYY-MM-DD.md`. What worked last week, what isn't working, the focus for this week, an experiment to run, an outside inspiration, a 4-6 week growth horizon.
- **A short direction file** at `exchange/cleo-direction-latest.md`. The condensed version, designed to be picked up by other agents (an SEO agent, a social agent) or by you on a phone screen.
- **A run report** at `reports/cleo-<timestamp>.json`. For the [Station inbox widget](https://github.com/catrinmdonnelly/station) if you use it.

## What it costs

About £2 a month in Anthropic API spend at the default model. GitHub Actions usage is free at this volume.

## What you'll need before you start

1. A GitHub account, free is fine.
2. An Anthropic API key, [from console.anthropic.com](https://console.anthropic.com).
3. About 30 minutes to fill in the config files with your business context.
4. Optional: a Gmail address with an app password if you want failure email alerts.

## How it works

Cleo reads four files in `config/`:
- Your **north star** (where the business is going)
- Your **state** (what's happening right now)
- Your **memory** (lessons across runs)
- Your **system prompt** (her persona, optional)

She also reads any optional inputs from other agents in `exchange/`. She calls Claude with web search enabled, scans for cultural moments and competitor moves, and writes the weekly brief plus a short direction file other agents can pick up.

The whole pipeline runs on GitHub Actions, every Monday, on a schedule. She commits the outputs back to the repo and pushes. If anything breaks, she emails you.

## Set up

See [SETUP.md](SETUP.md) for the full step-by-step. Roughly:

1. Fork or clone this repo into your own GitHub account
2. Edit the four files in `config/` so they describe your business
3. Add your `ANTHROPIC_API_KEY` as a GitHub Actions secret
4. Set the `BUSINESS_NAME` repo variable
5. Wait until Monday morning

## Running it locally

```sh
cp .env.example .env
# fill in ANTHROPIC_API_KEY and BUSINESS_NAME in .env

pip install -r requirements.txt
python cleo.py
```

The brief will appear in `briefs/`.

## Customising

- **Voice and tone.** Edit `config/system-prompt.md` to give Cleo a different personality. Leave it blank to use the default.
- **Schedule.** Edit `.github/workflows/weekly.yml`. Two cron lines cover BST and GMT for UK users. If you're in another timezone, swap both for whatever fires at 07:00 your local time.
- **Model.** Set `ANTHROPIC_MODEL` to switch model. Default is `claude-sonnet-4-6`.
- **Timezone.** Set `AGENT_TIMEZONE` to any IANA name, e.g. `America/New_York`.

## The bigger picture

Cleo is one of three agents that work together if you run all of them:

| Agent | Role | Cadence |
|-------|------|---------|
| **Cleo** | Weekly growth strategy. Reads what's happening, decides the focus. | Mondays |
| **[Alex](https://github.com/catrinmdonnelly/alex-agent)** | SEO. Pulls Search Console, finds rising queries and declining pages, writes the weekly report. | Wednesdays |
| **[Jess](https://github.com/catrinmdonnelly/jess-agent)** | Social content. Plans and posts daily Instagram carousels. | Daily |

Each one runs on its own. Together, Cleo writes the direction Alex and Jess read at the start of their runs. They share through the `exchange/` folder, no inboxes, no queues.

## Help

Issues and pull requests welcome. If you're stuck on setup, open an issue with the step you're stuck on.

## Licence

MIT. See [LICENSE](LICENSE).
