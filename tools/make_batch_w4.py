import json

# Viral-carousel rules applied (from research, Oct 2026):
# - Slide 1 has one job: earn the swipe. <10 words, curiosity gap or pattern interrupt.
# - One idea per slide, short text; every slide ends on an open loop that earns the next swipe.
# - Relatable "this is you" slide mid-carousel; save-worthy payoff near the end (saves weigh heavily).
# - Comment-bait CTA asking for a number or confession. Keywords on-screen for TikTok search.

CTA_SUB = "Follow for daily sleep science"


def pt(label, title, body, source=None):
    d = {"kind": "point", "label": label, "title": title, "body": body}
    if source:
        d["source"] = source
    return d


def cta(text, sub):
    return {"kind": "cta", "text": text, "sub": sub}


SRC_DR = "Source: Dawson & Reid, Nature, 1997"
SRC_CR = "Source: Crowley et al., J Biol Rhythms, 2003"
SRC_NIOSH = "Source: CDC NIOSH, shift work training"
SRC_AK = "Source: Akerstedt, Sleep Med Rev, 1998"

posts = [
    dict(id="p029", date="2026-10-07T20:30:00", pillar="night_shift", hook_style="pattern_interrupt", slot="evening", ab_group="",
         title="You drove home drunk this morning",
         why_shared="Shock hook night workers screenshot and send to the coworker who drives home after doubles.",
         caption=("You'd never drive after drinks. But after a night shift? In one study, 24 hours awake impaired performance "
                  "about as much as a 0.10% blood alcohol level (Dawson & Reid, Nature, 1997). What's your longest shift? "
                  "#nightshift #drowsydriving #nurselife #emtlife #sleepscience"),
         slides=[
             {"text": "You drove home drunk this morning.", "sub": "You just didn't drink anything"},
             pt("17 hours awake", "Your brain hits ~0.05%",
                "That's what one study found: performance like a 0.05% blood alcohol level.", SRC_DR),
             pt("24 hours awake", "Now it's ~0.10%",
                "Over the legal driving limit in every US state. And here's the part that gets you...", SRC_DR),
             pt("Do the math", "Up at 8am. Off at 7am.",
                "First night of the week? That's 23 hours awake before you even start the car."),
             pt("The scary part", "It doesn't feel that bad",
                "Willpower and experience don't cancel it out. Coffee in the parking lot isn't a fix either."),
             pt("Save this", "Before you drive home",
                "Nap 15-20 min first, carpool after long stretches, or get a ride. Nodding off? Pull over."),
             cta("What's your longest shift ever?", "Comment your hours. " + CTA_SUB),
         ]),
    dict(id="p030", date="2026-10-09T20:30:00", pillar="night_shift", hook_style="curiosity_gap", slot="evening", ab_group="",
         title="The 20 minutes that ruin your day sleep",
         why_shared="Names a mistake every night worker makes daily; high save value for the drive-home tip.",
         caption=("Can't fall asleep after a night shift? Your commute home might be why. Morning light is your body clock's "
                  "strongest wake-up signal. In one study, dark sunglasses on the way home helped night workers adapt (Crowley et al., 2003). "
                  "Only wear very dark lenses if someone else is driving. #nightshift #nightshiftnurse #sleeptips #circadianrhythm #shiftwork"),
         slides=[
             {"text": "The 20 minutes that ruin your day sleep", "sub": "It happens before you get home"},
             pt("It's not your bed", "It's your drive home",
                "Clock out at 7am and walk straight into sunrise. That's the problem."),
             pt("Here's why", "Morning light = 'wake up'",
                "Bright morning light is the strongest signal your body clock gets to start the day."),
             pt("So your brain thinks...", "'Great, it's daytime'",
                "Right when you need to sleep. Exhausted, but staring at the ceiling at 9am? This is you."),
             pt("The research", "Dark lenses on the way home",
                "Night workers who blocked morning light on the commute adapted far better to night shifts.", SRC_CR),
             pt("Save this", "How to block it safely",
                "Riding home? Dark wraparound sunglasses. Driving? Only normal driving sunglasses. Skip errands, go straight to a dark room."),
             cta("Do you wear sunglasses home after a shift?", "Yes or no below. " + CTA_SUB),
         ]),
    dict(id="p031", date="2026-10-13T20:30:00", pillar="night_shift", hook_style="contrarian", slot="evening", ab_group="",
         title="Your 8 hours of day sleep isn't 8 hours",
         why_shared="Challenges a belief night workers hold; the 'how many do you really get' question floods comments.",
         caption=("Time in bed isn't time asleep. More than half of night-shift workers report 6 hours of sleep or less (CDC NIOSH), "
                  "partly because your body clock fights day sleep. How many hours do you actually get after a night shift? "
                  "#nightshift #shiftwork #sleepscience #nurselife #sleepbetter"),
         slides=[
             {"text": "Your 8 hours of day sleep isn't 8 hours", "sub": "Night shifters, read this"},
             pt("The reality", "Over half get 6 hours or less",
                "That's night-shift workers in CDC NIOSH training data. But why, if you're in bed long enough?", SRC_NIOSH),
             pt("The reason", "Your body clock fights back",
                "It pushes you awake late morning, no matter how tired you are.", SRC_AK),
             pt("Then add...", "Daylight. Traffic. Texts.",
                "Every wake-up you don't remember still cuts your real sleep. In bed 8, asleep maybe 5."),
             pt("Most people miss this", "It stacks up all week",
                "A short night after every shift adds up. That's the 'tired on my day off' feeling."),
             pt("Save this", "Protect your day sleep",
                "Full blackout. Earplugs or white noise. Phone on Do Not Disturb. Same sleep window every work day."),
             cta("Be honest: how many hours do you really get?", "Comment your number. " + CTA_SUB),
         ]),
]

batch = {"batch": "2026-10-w4-extra", "timezone": "America/New_York", "posts": posts}
json.dump(batch, open("content/batch-2026-10-w4-extra.json", "w"), indent=2)

for p in posts:
    assert p["caption"].count("#") == 5, (p["id"], p["caption"].count("#"))
    assert len(p["slides"][0]["text"].split()) < 10, p["id"]
    assert 5 <= len(p["slides"]) <= 7, p["id"]
    for i, s in enumerate(p["slides"], 1):
        n = len((s.get("title", "") + " " + s.get("body", "")).split())
        if n > 24:
            print("LONG", p["id"], i, n)
print(len(posts), "posts")
