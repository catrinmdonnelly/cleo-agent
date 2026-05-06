# Cleo setup

Plain English, end to end. About 30-45 minutes from start to first run. Most of that time is on `state.md`, that's the work that decides whether Cleo helps you or not.

## Before you start

You'll need:
- A GitHub account ([sign up free](https://github.com/join) if you don't have one)
- An Anthropic account ([sign up](https://console.anthropic.com))
- About £5 of credit on your Anthropic account (Cleo costs ~£2 a month at typical use)
- 30-45 minutes, most of it for filling in `state.md` properly

You will *not* need to write any code.

---

## Step 1. Get an Anthropic API key

1. Go to [console.anthropic.com](https://console.anthropic.com).
2. Sign up or sign in.
3. Click your profile in the top right, then **API Keys**.
4. Click **Create Key**, name it `cleo-agent`, and copy the key that appears. **You'll only see it once.** Paste it somewhere safe.
5. Click **Plans & Billing** and add £5 to £10 of credit.

---

## Step 2. Copy the repo into your GitHub

1. Click **Fork** in the top right of [the GitHub page](https://github.com/catrinmdonnelly/cleo-agent), or use **Use this template** for a clean repo.
2. Either way, you now have your own copy.

---

## Step 3. Fill in `state.md` properly. *This is the most important step.*

If you skip this or do it badly, Cleo will write generic, unhelpful briefs every Monday. If you do it well, the briefs will be sharp from week one.

`state.md` lives in the `config/` folder. It needs to answer four questions:

1. **What's happening in the business right now?** Last month's revenue, customers, what shipped, what's in progress, what's blocked.
2. **What's been working recently?** Specific channels, formats, customer types, anything you've noticed performing.
3. **What's been failing recently?** So Cleo doesn't keep suggesting it.
4. **What's launching or changing soon?** So Cleo can plan around it.

### Weak vs strong examples

This is the difference between Cleo being useful and Cleo being noise:

**Weak input:**
> Things are going okay. We had some sales last month. Newsletter is going well. Trying to grow on Instagram.

**Strong input:**
> Last month: £4,200 revenue across 38 orders. Three customers came back for a second order, biggest single repeat. Instagram traffic flat, sessions down 12% month on month. Newsletter open rate 41%, click rate 8%, the "behind the scenes" angle is the one that converts. Working on launching the new mug range in 3 weeks. Stuck on which photographer to use, three quotes in front of me. Cash position: 4 months runway at current burn. Trying to decide whether to spend on paid Instagram ads or commission a brand video, leaning toward video.

The second one gives Cleo something to work with. Specific numbers, named channels, real situations. The first one will get you a brief that sounds like a LinkedIn post.

### How to do it

1. In your forked repo on GitHub, click into the `config/` folder.
2. Click `state.md`, then click the **pencil icon** to edit.
3. Replace every placeholder with your real numbers, observations, and situations.
4. **Bullet points are fine.** Cleo doesn't need polished prose. Half-thoughts and fragments work.
5. Click **Commit changes** at the bottom of the page.

A good `state.md` is 200-500 words. Less than 100 words and it's probably not specific enough. More than 800 and you're padding.

You'll update it every couple of weeks as things change. Cleo reads it every Monday.

---

## Step 4. Fill in `north-star.md`

This is the piece that doesn't change month to month. Where the business is going. Who it's for. What it won't do.

1. Click `config/north-star.md`, edit, replace placeholders.
2. Same rule: be specific. "Grow the business" is too vague. "Hit £10k/month from organic channels in the next 6 months" gives Cleo a target to optimise toward.
3. Commit.

You only need to do this once, then revisit it every six months.

---

## Step 5. `memory.md` (optional, can stay empty)

Cleo will reference this file if there's anything in it. You can leave it empty for now. Add lessons over time, like:

> Tried Pinterest in February. Got 14k impressions but zero clicks. Don't suggest Pinterest again unless something changes.

This stops Cleo recommending the same dead ends.

---

## Step 6. `system-prompt.md` (optional)

Leave this blank to use Cleo's default voice. Edit it if you want her to sound different, maybe more formal, more aggressive, more focused on a specific framework you like.

---

## Step 7. Add your API key as a GitHub secret

Secrets are how GitHub safely stores your API key without putting it in the code.

1. In your repo on GitHub, click **Settings** (top of the repo page, not your account settings).
2. In the left sidebar: **Secrets and variables → Actions**.
3. Click **New repository secret**.
4. Name: `ANTHROPIC_API_KEY`. Value: paste the key from step 1. Click **Add secret**.

---

## Step 8. Set your business name

This makes the brief title use your real business name instead of "your business".

1. Same place: **Settings → Secrets and variables → Actions**.
2. Click the **Variables** tab (next to Secrets).
3. Click **New repository variable**.
4. Name: `BUSINESS_NAME`. Value: your business name, e.g. `Cornish Ceramics`. Click **Add variable**.

---

## Step 9. Turn on Actions

GitHub Actions is what runs Cleo every Monday. It's free for what we're doing.

1. In your repo, click **Actions** in the top tabs.
2. If you see a yellow banner asking to enable workflows, click **I understand my workflows, go ahead and enable them**.

---

## Step 10. Run Cleo for the first time

You don't have to wait until Monday.

1. In your repo, click **Actions**.
2. In the left sidebar, click **Cleo weekly growth brief**.
3. Click the **Run workflow** dropdown on the right, then **Run workflow** in the box that appears.
4. Wait two to five minutes. Refresh.
5. The run should turn green. Click into your repo's `briefs/` folder and you'll see your first brief.
6. Read it. If it feels generic or off, that's almost always a `state.md` problem, go back to step 3 and add more specifics, then re-run.

---

## Step 11 (optional). Failure email alerts

If you want Cleo to email you when a run fails, you'll need a Gmail account with an app password.

1. In your Google account, go to **Security → 2-Step Verification → App passwords**. ([Direct link](https://myaccount.google.com/apppasswords). 2-step verification needs to be on first.)
2. Generate an app password named `cleo-agent`. Copy the 16 characters.
3. In your GitHub repo: **Settings → Secrets and variables → Actions → New repository secret**, four times:
   - `FAILURE_EMAIL_TO`: where you want alerts sent
   - `FAILURE_EMAIL_FROM`: the Gmail you'll send from
   - `FAILURE_EMAIL_SMTP_HOST`: `smtp.gmail.com`
   - `FAILURE_EMAIL_SMTP_PASS`: the 16-character app password

---

## Step 12. Change the schedule (optional)

Cleo runs at 07:00 UK every Monday by default. To change:

1. Edit `.github/workflows/weekly.yml`.
2. Change the cron lines (currently 06:00 UTC for BST, 07:00 UTC for GMT).
3. Use [crontab.guru](https://crontab.guru) to design a new schedule. GitHub Actions cron is in **UTC**.

---

## What to expect after that

Every Monday morning, Cleo will:
1. Pull the latest config files
2. Read what's happening in your business
3. Look at what's happening outside (web search)
4. Write the brief to `briefs/YYYY-MM-DD.md`
5. Commit and push to your repo

You'll see it in your repo when you open GitHub. No notifications unless you set up email alerts.

**The most important thing: read it Monday morning, act on one thing, and update `state.md` over the week as things change.** That's the only way the briefs get sharper.

---

## Troubleshooting

**The first run failed.** Click the run in **Actions**, expand the **Run Cleo** step, and read the error. Almost always it's a missing or wrong API key. Re-check step 7.

**Cleo's brief is generic and unhelpful.** Almost always a `state.md` problem. Open it, look for vague phrases like "going well" or "trying to grow", and replace them with specific numbers and named situations. Re-run.

**The schedule isn't firing.** GitHub Actions pauses cron schedules in repos that have had no activity for 60 days. If you go quiet, it'll stop. Run the workflow manually once and the schedule resumes.

**The brief is great but I'm not acting on it.** That's a you problem, not a Cleo problem. Block 15 minutes in your calendar every Monday at 09:00 to read the brief and pick one thing to do that week. The agent can't do that part for you.
