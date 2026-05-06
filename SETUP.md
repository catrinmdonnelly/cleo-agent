# Cleo setup

Plain English, end to end. About 30 minutes from start to first run.

## Before you start

You'll need:
- A GitHub account ([sign up free](https://github.com/join) if you don't have one)
- An Anthropic account ([sign up](https://console.anthropic.com))
- A small amount of credit on your Anthropic account (£5 will run Cleo for two years)
- About 30 minutes to fill in the config files

You will *not* need to write any code.

---

## Step 1 — get an Anthropic API key

1. Go to [console.anthropic.com](https://console.anthropic.com).
2. Sign up or sign in.
3. Click your profile in the top right, then **API Keys**.
4. Click **Create Key**, name it `cleo-agent`, and copy the key that appears. **You'll only see it once.** Paste it somewhere safe.
5. Click **Plans & Billing** and add £5 to £10 of credit. Cleo costs about £2 a month at typical use.

---

## Step 2 — copy the repo into your GitHub

You have two options. Pick one.

**Option A: fork it.** Click **Fork** in the top right of [the GitHub page](https://github.com/catrinmdonnelly/cleo-agent). This makes a copy under your account. Easiest.

**Option B: use it as a template.** If you want a clean repo with no commit history, click **Use this template** instead. Choose **Create a new repository**, give it a name, click **Create repository from template**.

Either way, you now have your own copy of the repo on GitHub.

---

## Step 3 — fill in your business context

Cleo's quality is almost entirely determined by the config files. Take your time on this.

1. In your new repo on GitHub, click into the `config/` folder.
2. Click `north-star.md`, then click the **pencil icon** to edit.
3. Replace the placeholder text with your real answers. Be specific. Bullet points are fine.
4. Click **Commit changes** at the bottom of the page.
5. Repeat for `state.md`. This one matters more for the weekly brief, since it's what changes week to week.
6. `memory.md` can stay empty for now. Cleo will use it as it grows.
7. `system-prompt.md` is optional. Leave it as is to use Cleo's default voice. Edit it if you want her to sound different.

---

## Step 4 — add your API key as a secret

Secrets are how GitHub safely stores your API key without putting it in the code.

1. In your repo on GitHub, click **Settings** (top of the repo page, not your account settings).
2. In the left sidebar: **Secrets and variables → Actions**.
3. Click **New repository secret**.
4. Name: `ANTHROPIC_API_KEY`. Value: paste the key you copied in step 1. Click **Add secret**.

---

## Step 5 — set your business name

This makes the brief title use your real business name instead of "your business".

1. Same place as the last step: **Settings → Secrets and variables → Actions**.
2. Click the **Variables** tab (next to Secrets).
3. Click **New repository variable**.
4. Name: `BUSINESS_NAME`. Value: your business name, e.g. `Cornish Ceramics`. Click **Add variable**.

---

## Step 6 — turn on Actions

GitHub Actions is the thing that runs Cleo every Monday. It's free for what we're doing.

1. In your repo, click **Actions** in the top tabs.
2. If you see a yellow banner asking to enable workflows, click **I understand my workflows, go ahead and enable them**.

---

## Step 7 — run Cleo for the first time

You don't have to wait until Monday to see Cleo work.

1. In your repo, click **Actions**.
2. In the left sidebar, click **Cleo weekly growth brief**.
3. Click the **Run workflow** dropdown on the right, then **Run workflow** in the box that appears.
4. Wait two to five minutes. Refresh.
5. The run should turn green. If it does, you're done. Click into your repo's `briefs/` folder and you'll see the first brief.
6. If it's red, click into the run, expand the failed step, and read the error. Most of the time it's a missing secret. Add it and re-run.

---

## Step 8 (optional) — failure email alerts

If you want Cleo to email you when a run fails, you'll need a Gmail account with an app password.

1. In your Google account, go to **Security → 2-Step Verification → App passwords**. ([Direct link](https://myaccount.google.com/apppasswords). You need 2-step verification turned on first.)
2. Generate a new app password named `cleo-agent`. Copy the 16-character password.
3. Back in your GitHub repo: **Settings → Secrets and variables → Actions → New repository secret**, four times:
   - `FAILURE_EMAIL_TO`: the email you want alerts sent to
   - `FAILURE_EMAIL_FROM`: the Gmail address you'll send from
   - `FAILURE_EMAIL_SMTP_HOST`: `smtp.gmail.com`
   - `FAILURE_EMAIL_SMTP_PASS`: the 16-character app password from Google

---

## Step 9 — change the schedule (optional)

Cleo runs at 07:00 UK every Monday by default. If you want a different time:

1. In your repo, edit `.github/workflows/weekly.yml`.
2. Find the two cron lines:
   ```yaml
   - cron: "0 6 * * 1"     # 06:00 UTC Mon = 07:00 UK BST
   - cron: "0 7 * * 1"     # 07:00 UTC Mon = 07:00 UK GMT
   ```
3. Cron syntax is `minute hour day-of-month month day-of-week`. `0 7 * * 1` means 07:00 UTC every Monday.
4. Use [crontab.guru](https://crontab.guru) if you want a different time. GitHub Actions cron is in **UTC**, not your local time.

---

## What to expect after that

Every Monday morning, Cleo will:
1. Pull the latest config files
2. Read what's happening, look outside, decide the week's focus
3. Write a brief to `briefs/`
4. Write a short direction to `exchange/`
5. Commit and push

You'll see it appear in your repo when you next look. No notifications unless you set up email alerts.

---

## Troubleshooting

**The first run failed.** Click the run in the **Actions** tab, expand the **Run Cleo** step, and read the error. Almost always it's a missing or wrong API key. Re-check step 4.

**Cleo's brief is generic and unhelpful.** That's a config problem, not a code problem. Open `config/state.md` and `config/north-star.md` and make them more specific. Cleo can only be as sharp as the inputs.

**The schedule isn't firing.** GitHub Actions pauses cron schedules in repos that have had no activity for 60 days. If you go quiet, it'll stop. Run the workflow manually once and the schedule resumes.

**I'm getting committed-to-main pull request reminders.** The workflow commits directly to `main`. If your repo has branch protection rules, either turn them off, or set up a deploy key. For most personal repos this doesn't apply.
