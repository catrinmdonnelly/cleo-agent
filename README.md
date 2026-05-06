# Cleo

A weekly growth strategist for small businesses, who replaces the strategy meeting nobody books with a five-minute brief that lands in your repo every Monday morning before the working week starts.

Most owners are too busy doing the work to think about whether they're doing the right work, and strategy quietly becomes whatever is loudest first thing on Monday. Cleo replaces that with a forced reading exercise: every week, before anything else has a chance to demand your attention, she writes a brief that names what worked last week, what didn't, and the one thing to focus on this week. She is the friend who has been thinking about your business while you slept and has one specific recommendation by the time you wake up.

> **Status:** Free to use. Take the code, point it at your business. MIT licensed.

## What Cleo actually does for a business

Picture a small ecommerce brand turning over £40,000 a month, with two people running it, no marketing team, and the founder making the actual product most days. Every Monday at seven in the morning, before that founder opens her laptop, Cleo reads what's happening inside the business, scans the web for what's happening outside, and writes a brief that lands like this:

> Last week three of your four sales came from the newsletter rather than social, so stop pushing posts about new arrivals on Instagram (you're posting into a void) and send two newsletters this week instead of one. The "behind the scenes of how it's made" angle is the one that worked, so try it again on Wednesday with a different product. Mother's Day is also four weeks away and you don't have a campaign yet, which is your real focus this month, not Instagram.

The value isn't the brief itself, since anyone could write something similar given the inputs. The value is that **someone is writing it for you every Monday, on time, without you ever having to remember it's Monday**.

## Who Cleo helps

- A solo founder or small team already doing the work
- A business with at least a few months of activity to react to
- An owner who'll actually read the brief Monday and act on one thing

## Who Cleo doesn't help

- A business that won't update `state.md`, Cleo is only as sharp as the input
- An owner who reads the brief but never acts
- A business that needs sales help (Cleo has no view of your CRM)
- A pre-product startup with nothing to react to yet

## What success looks like

Success isn't a stack of beautifully-written briefs piling up in your repo. It's three or four things that actually changed in your business across a quarter because Cleo flagged them: a campaign that ran because she said Mother's Day was coming, a failed channel that got killed because she said it wasn't working and you finally stopped spending on it, a product that got more attention because the data showed it was the one customers actually liked. If a year goes by and nothing in the business looks any different, Cleo wasn't doing her job, or you weren't reading her.

## What you get every Monday

A markdown file at `briefs/YYYY-MM-DD.md` with five sections:

1. **This week's focus**, one paragraph, the headline
2. **What worked / what isn't working**, last week's signals
3. **This week's experiment**, one thing to try, in under 30 minutes, with a metric and a decide-by date
4. **Outside inspiration**, one brand or creator outside your space worth learning from
5. **Growth horizon**, what's coming up in the next 4-6 weeks so you don't get caught off guard

You also get a one-liner at `exchange/cleo-direction-latest.md` for any dashboard or downstream agent, and a Station inbox JSON if you use the [Station widget](https://github.com/catrinmdonnelly/station).

## What it costs

About £2 a month in Anthropic API spend. GitHub Actions usage is free at this volume.

## What you'll need before you start

1. A GitHub account, free is fine
2. An Anthropic API key, [from console.anthropic.com](https://console.anthropic.com)
3. About 30-45 minutes to fill in `state.md` and `north-star.md` properly. **This is the work that matters.** Cleo is only as sharp as her inputs.

## Set up

See [SETUP.md](SETUP.md) for the full step-by-step. The short version:

1. Fork this repo
2. Edit `config/state.md` and `config/north-star.md` with your real business context
3. Add your `ANTHROPIC_API_KEY` as a GitHub Actions secret
4. Set the `BUSINESS_NAME` repo variable
5. Wait until Monday morning, or trigger a manual run

## Running it locally

```sh
cp .env.example .env
# fill in ANTHROPIC_API_KEY and BUSINESS_NAME

pip install -r requirements.txt
python cleo.py
```

The brief will appear in `briefs/`.

## Customising

- **Voice and tone.** Edit `config/system-prompt.md` to give Cleo a different personality. Leave it blank to use the default.
- **Schedule.** Edit `.github/workflows/weekly.yml`. Two cron lines cover BST and GMT for UK users. Replace with whatever fires at 07:00 your local time if you're elsewhere.
- **Model.** Set `ANTHROPIC_MODEL` to switch model. Default is `claude-sonnet-4-6`.
- **Timezone.** Set `AGENT_TIMEZONE` to any IANA name, e.g. `America/New_York`.

## The bigger picture

Cleo can run alongside two siblings if you want a fuller setup:

| Agent | Role | Cadence |
|-------|------|---------|
| **Cleo** | Weekly growth strategy. Reads what's happening, decides the focus. | Mondays |
| **[Alex](https://github.com/catrinmdonnelly/alex-agent)** | SEO. Pulls Search Console, finds rising queries and ranking opportunities. | Wednesdays |
| **[Jess](https://github.com/catrinmdonnelly/jess-agent)** | Social content. Plans and posts daily Instagram carousels. | Daily |

Each one runs on its own. You don't need to run all three.

## Help

Issues and pull requests welcome. If your brief feels generic, that's almost always a `state.md` problem, open an issue with what you've got in there and I'll suggest where it could be sharper.

## Licence

MIT. See [LICENSE](LICENSE).
