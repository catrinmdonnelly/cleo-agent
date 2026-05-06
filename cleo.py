"""
Cleo, weekly growth strategy agent.

Runs once a week (default Monday 07:00 UK) and writes a one-page growth brief
for the week ahead. Cleo reads your business context, looks at what's been
working, scans the web for what's happening in your space, and decides the
focus, the experiment to run, and the direction for the week.

Pipeline:
  1. Read your config files (north-star, state, memory, system prompt)
  2. Ask Claude (with web search) to produce the weekly brief
  3. Write briefs/YYYY-MM-DD.md (the full brief, for you)
  4. Write exchange/cleo-direction-latest.md (short version any downstream agent can read)
  5. Write reports/cleo-<timestamp>.json (Station inbox JSON)
  6. Email you on failure

Exit code 0 on success, 1 on any step failing.
"""

from __future__ import annotations

import json
import os
import re
import smtplib
import sys
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from email.message import EmailMessage
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).parent
CONFIG = ROOT / "config"
EXCHANGE = ROOT / "exchange"
BRIEFS = ROOT / "briefs"
LOGS = ROOT / "logs"
REPORTS = ROOT / "reports"

TIMEZONE = ZoneInfo(os.environ.get("AGENT_TIMEZONE", "Europe/London"))


# ─── Helpers ───────────────────────────────────────────────────────────────────

def env(name: str, required: bool = True, default: str = "") -> str:
    val = os.environ.get(name, default)
    if required and not val:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return val


def now_local() -> datetime:
    return datetime.now(TIMEZONE)


def today_key() -> str:
    return now_local().strftime("%Y-%m-%d")


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def read_if_exists(path: Path, fallback: str = "") -> str:
    return path.read_text() if path.exists() else fallback


# ─── Gather inputs ─────────────────────────────────────────────────────────────

def gather_inputs() -> dict:
    """Read everything Cleo needs before calling Claude."""
    log("gathering inputs")

    north_star = read_if_exists(
        CONFIG / "north-star.md",
        "(north-star.md is missing, fill in config/north-star.md so Cleo knows where the business is going)",
    )
    state = read_if_exists(
        CONFIG / "state.md",
        "(state.md is missing, fill in config/state.md with what's happening right now. Cleo is useless without this.)",
    )
    memory = read_if_exists(
        CONFIG / "memory.md",
        "(memory.md is missing, optional, used to remember lessons across runs)",
    )

    return {
        "north_star": north_star,
        "state": state,
        "memory": memory,
        "business_name": env("BUSINESS_NAME", required=False, default="your business"),
    }


# ─── Claude call ───────────────────────────────────────────────────────────────

DEFAULT_SYSTEM_PROMPT = """You are Cleo, a weekly growth strategist.

Every Monday morning, you write a five-minute brief that tells the business what to focus on this week and why. You are the friend who's been thinking about their business overnight and has one clear, specific recommendation when they wake up.

You are not in the weeds. You read the business state, look at what's happening outside, and turn all of it into one clear direction for the week. Your job is to make a busy founder pause for five minutes and decide on one thing, instead of being pulled in seven directions by Wednesday.

Your tone is warm, direct and observational. You make sharp calls and say why. You never pad. You never say "engagement was good", you say what specifically worked, why, and what to do about it. You avoid em dashes entirely. No staccato fragments. No corporate language. No generic AI phrases like "leverage", "unlock", or "take it to the next level".

You have access to a web_search tool. Use it liberally to:
  - Spot competitors doing something worth knowing about
  - Note cultural moments, calendar events and trending conversations in the next 2-6 weeks
  - Find one piece of "outside inspiration" each week, a brand or creator outside this niche doing something the business could learn from

When you respond, return ONE JSON object matching this schema exactly. No prose, no code fences:

{
  "what_worked": ["specific observation, named with evidence", ...],
  "what_isnt_working": ["specific observation, named with evidence", ...],
  "this_weeks_focus": "one paragraph: what the business should pay attention to this week and why. Concrete enough that the owner could explain it in one sentence to a friend.",
  "this_weeks_experiment": {
    "name": "short snappy name",
    "hypothesis": "what we expect will happen and why",
    "how_to_run": "concrete steps the owner can do in under 30 minutes this week",
    "what_to_measure": "one clear metric, with a target if you can be specific",
    "decide_by": "YYYY-MM-DD"
  },
  "outside_inspiration": {
    "source": "brand or creator name",
    "url": "https://...",
    "what_they_did": "one or two sentences",
    "what_we_take_from_it": "one sentence"
  },
  "growth_horizon": "one paragraph on the next 4-6 weeks, seasonal moments, campaigns to plan, anything coming up that needs runway. The owner reads this so they're not caught off-guard."
}

Hard rules:
- Every recommendation must be specific enough to act on this week, not theoretically true
- Cite evidence from state.md or the web search when you make a claim
- If state.md is thin or missing, say so, don't invent activity that didn't happen
- Three to five items in each list. Quality over volume.
"""


def load_system_prompt() -> str:
    """Load the Cleo persona prompt. Users can edit config/system-prompt.md to customise."""
    custom = read_if_exists(CONFIG / "system-prompt.md", "")
    return custom.strip() if custom.strip() else DEFAULT_SYSTEM_PROMPT


def ask_claude(inputs: dict) -> dict:
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("anthropic package not installed, run: pip install -r requirements.txt")

    def cap(s: str, n: int) -> str:
        return s if len(s) <= n else s[:n] + "\n…(truncated)"

    user_message = f"""Today is {now_local().strftime('%A %d %B %Y')}.
Business: {inputs['business_name']}.

NORTH STAR (where the business is going):
{cap(inputs['north_star'], 3000)}

BUSINESS STATE (what's happening right now, your primary input):
{cap(inputs['state'], 5000)}

ACCUMULATED MEMORY (lessons across runs):
{cap(inputs['memory'], 5000)}

Produce this week's brief. Use web_search to check competitors and cultural moments. Return one JSON object only.
"""

    client = anthropic.Anthropic(api_key=env("ANTHROPIC_API_KEY"))

    model = env("ANTHROPIC_MODEL", required=False, default="claude-sonnet-4-6")
    log(f"claude: calling {model} with web_search enabled")
    resp = client.messages.create(
        model=model,
        max_tokens=8000,
        system=load_system_prompt(),
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 6,
        }],
        messages=[{"role": "user", "content": user_message}],
    )

    text_parts: list[str] = []
    for block in resp.content:
        if getattr(block, "type", None) == "text":
            text_parts.append(block.text)
    text = "".join(text_parts).strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise RuntimeError(f"Cleo did not return valid JSON: {e}\n---\n{text[:1000]}")


# ─── Render ────────────────────────────────────────────────────────────────────

def render_full_brief(brief: dict, business_name: str) -> str:
    """The Monday morning brief, in full. Five minutes to read."""
    date = today_key()
    out = [f"# {business_name}, growth brief, week of {date}\n",
           "*Cleo. Monday morning.*\n"]

    out.append("## This week's focus\n")
    out.append(brief.get("this_weeks_focus", ""))
    out.append("")

    out.append("## What worked\n")
    for b in brief.get("what_worked", []) or ["(nothing specific from last week)"]:
        out.append(f"- {b}")
    out.append("")

    out.append("## What isn't working\n")
    for b in brief.get("what_isnt_working", []) or ["(nothing flagged)"]:
        out.append(f"- {b}")
    out.append("")

    exp = brief.get("this_weeks_experiment", {}) or {}
    out.append("## This week's experiment\n")
    out.append(f"**{exp.get('name','(unnamed)')}**\n")
    out.append(f"- **Hypothesis:** {exp.get('hypothesis','')}")
    out.append(f"- **How to run:** {exp.get('how_to_run','')}")
    out.append(f"- **What to measure:** {exp.get('what_to_measure','')}")
    out.append(f"- **Decide by:** {exp.get('decide_by','')}")
    out.append("")

    insp = brief.get("outside_inspiration", {}) or {}
    if insp.get("source") or insp.get("what_they_did"):
        out.append("## Outside inspiration\n")
        out.append(f"**{insp.get('source','')}**, {insp.get('url','')}\n")
        out.append(f"{insp.get('what_they_did','')}\n")
        out.append(f"**What we take from it:** {insp.get('what_we_take_from_it','')}\n")

    if brief.get("growth_horizon"):
        out.append("## Growth horizon (next 4-6 weeks)\n")
        out.append(brief["growth_horizon"])
        out.append("")

    return "\n".join(out)


def render_one_liner(brief: dict) -> str:
    """The bare minimum: one sentence saying what to do this week.

    Useful if you ever pipe Cleo into another agent or display her output
    on a dashboard. Lives in exchange/cleo-direction-latest.md.
    """
    date = today_key()
    exp = brief.get("this_weeks_experiment", {}) or {}
    out = [
        f"# Cleo, week of {date}\n",
        "## Focus\n",
        brief.get("this_weeks_focus", ""),
        "",
        "## Experiment\n",
        f"**{exp.get('name','(unnamed)')}**",
        f"- {exp.get('hypothesis','')}",
        f"- Run: {exp.get('how_to_run','')}",
        f"- Measure: {exp.get('what_to_measure','')}",
        f"- Decide by: {exp.get('decide_by','')}",
    ]
    return "\n".join(out)


def render_brief_summary(brief: dict) -> str:
    """One line for the Station inbox."""
    date = today_key()
    exp = brief.get("this_weeks_experiment", {}) or {}
    return (
        f"Week of {date}. "
        f"Experiment: **{exp.get('name','(unnamed)')}**. "
        f"{exp.get('how_to_run','')}"
    )


# ─── Station + email ───────────────────────────────────────────────────────────

@dataclass
class RunResult:
    date: str
    started_at: str
    gathered: bool = False
    analysed: bool = False
    files_written: list[str] = field(default_factory=list)
    error: str = ""

    @property
    def fully_successful(self) -> bool:
        return self.gathered and self.analysed and not self.error


def write_station_report(run: RunResult, summary: str = "") -> Path:
    ts = now_local().strftime("%Y-%m-%d-%H%M")
    path = REPORTS / f"cleo-{ts}.json"
    path.parent.mkdir(exist_ok=True)

    if run.fully_successful:
        payload = {
            "agent": "cleo",
            "agent_display": "Cleo, Growth strategy",
            "timestamp": now_local().strftime("%Y-%m-%dT%H:%M:%S"),
            "status": "needs_input",
            "headline": f"Cleo's weekly growth brief is ready ({run.date})",
            "summary": summary or "Direction for the week has been written.",
            "actions_needed": [
                "Read the brief (~5 mins)",
                "Decide whether to run this week's experiment",
            ],
            "files_created": run.files_written,
            "full_brief_path": f"briefs/{run.date}.md",
        }
    else:
        payload = {
            "agent": "cleo",
            "agent_display": "Cleo, Growth strategy",
            "timestamp": now_local().strftime("%Y-%m-%dT%H:%M:%S"),
            "status": "needs_input",
            "headline": f"Cleo's weekly run failed ({run.date})",
            "summary": run.error or "See run logs on GitHub Actions.",
            "actions_needed": [
                "Check the GitHub Actions run for full logs",
                "Re-run the workflow once fixed",
            ],
            "files_created": run.files_written,
        }
    path.write_text(json.dumps(payload, indent=2, default=str))
    log(f"  report written: {path.relative_to(ROOT)}")
    return path


def send_failure_email(run: RunResult) -> None:
    to_addr = env("FAILURE_EMAIL_TO", required=False)
    if not to_addr:
        log("  (email alert skipped, FAILURE_EMAIL_TO not set)")
        return
    host = env("FAILURE_EMAIL_SMTP_HOST", required=False, default="smtp.gmail.com")
    from_addr = env("FAILURE_EMAIL_FROM", required=False, default=to_addr)
    password = env("FAILURE_EMAIL_SMTP_PASS", required=False)
    if not password:
        log("  (email alert skipped, FAILURE_EMAIL_SMTP_PASS not set)")
        return

    run_url = (f"https://github.com/{os.environ.get('GITHUB_REPOSITORY', '')}"
               f"/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}")

    body = [
        f"Cleo's weekly growth run hit a problem on {run.date}.",
        "",
        f"Error: {run.error}",
        "",
        f"GitHub Actions run: {run_url}",
    ]
    msg = EmailMessage()
    msg["Subject"] = f"Cleo: weekly growth run failed on {run.date}"
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.set_content("\n".join(body))
    with smtplib.SMTP_SSL(host, 465, timeout=30) as smtp:
        smtp.login(from_addr, password)
        smtp.send_message(msg)
    log(f"  failure email sent to {to_addr}")


# ─── main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    run = RunResult(date=today_key(), started_at=now_local().isoformat())
    log(f"cleo: weekly growth run starting ({run.date})")

    try:
        inputs = gather_inputs()
        run.gathered = True
    except Exception as e:
        traceback.print_exc()
        run.error = f"input gather failed: {e}"
        write_station_report(run)
        send_failure_email(run)
        return 1

    try:
        brief = ask_claude(inputs)
        run.analysed = True
    except Exception as e:
        traceback.print_exc()
        run.error = f"Claude analysis failed: {e}"
        write_station_report(run)
        send_failure_email(run)
        return 1

    BRIEFS.mkdir(exist_ok=True)
    brief_path = BRIEFS / f"{run.date}.md"
    brief_path.write_text(render_full_brief(brief, inputs["business_name"]))
    run.files_written.append(str(brief_path.relative_to(ROOT)))
    log(f"  full brief:   {brief_path.relative_to(ROOT)}")

    EXCHANGE.mkdir(exist_ok=True)
    direction_path = EXCHANGE / "cleo-direction-latest.md"
    direction_path.write_text(render_one_liner(brief))
    run.files_written.append(str(direction_path.relative_to(ROOT)))
    log(f"  one-liner:    {direction_path.relative_to(ROOT)}")

    LOGS.mkdir(exist_ok=True)
    (LOGS / f"cleo-analysis-{run.date}.json").write_text(json.dumps(brief, indent=2, default=str))

    write_station_report(run, summary=render_brief_summary(brief))
    log("cleo: done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
