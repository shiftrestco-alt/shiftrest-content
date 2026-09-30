# Experiment framework

Goal: grow followers on sleep education (importance of sleep, how to raise sleep score). No product promotion until the account has an audience. Cast a wide net, then double down on what the analytics show.

## What every post is tagged with (in `posts_log.json`)

| Tag | Values | Question it answers |
|---|---|---|
| `pillar` | why_sleep_matters, sleep_score_tips, myth_bust, night_shift | Which topic earns views and follows? |
| `hook_style` | question, stat, myth, bold_claim, list | Which first slide stops the scroll? |
| `slides` | 5, 6, 7 | Does carousel length change completion/shares? |
| `slot` | morning (7:30), midday (12:30), evening (20:30) ET | When does the audience show up? |
| `ab_group` | shared id for A/B pairs, else blank | Which posts are a controlled comparison? |

## Rules so results mean something
1. **A/B pairs change one thing.** Same topic and slot, different hook slide only, posted on different days.
2. Everything else is rotated evenly so no variable is confounded with another.
3. **No conclusions before ~30 posts.** A new account's views are noisy; one viral post proves nothing. Compare medians, not single posts.
4. Primary metric: **follows gained per 1,000 views** (falls back to shares + saves per view when follower data is thin). Views alone reward clickbait that does not convert.
5. Weekly review: pull analytics for every logged post, rank by primary metric per tag, then shift next week's mix toward winners while keeping ~30% exploration (new hooks/topics).

## Content rules
- Only well-established claims; cite the source in the caption when a number is used.
- Phrase as "supports", "is linked to", "tends to". No cures, no medical claims.
- Sleep score is an estimate from wearables, not a medical measurement. Say so when relevant.
- Every post ends with a follow CTA (slide + caption).
