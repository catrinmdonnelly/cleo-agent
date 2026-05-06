# Cleo's config

Cleo reads four files in this folder before each weekly run. Edit them so they describe your business. The agent's quality depends almost entirely on what's in here.

| File | What it's for | When to update |
|------|---------------|----------------|
| `north-star.md` | The big picture. Where the business is going. Who it's for. The thing that doesn't change month to month. | Once at setup. Revisit every 6 months. |
| `state.md` | What's happening right now. Current revenue, traffic, what shipped this month, what's broken, what you're testing. | Whenever something material changes. Cleo reads it every Monday. |
| `memory.md` | Lessons learned across runs. "We tried X, it didn't work because Y." Cleo updates this implicitly through repetition, but you can write into it directly too. | Optional. Can start empty. |
| `system-prompt.md` | The Cleo persona. How she writes, what she pays attention to, the tone. | Optional. Leave blank to use the default. Edit if you want a different voice. |

## How to fill them in

Start with `north-star.md` and `state.md`. The other two are optional.

The more specific you are, the better the brief. "We're a small ecommerce brand" is weak input. "We sell handmade ceramic plant pots, £45 average order, 80% of customers are women aged 30-45 in the UK, we make the pots ourselves in a Cornwall studio, our wedge is that big chains don't sell anything this irregular and tactile" is strong input.

Cleo doesn't need polished prose. Bullet points, fragments, half-thoughts are all fine. She'll work with what's there.
