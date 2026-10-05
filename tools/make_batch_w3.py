import json

CTA_SUB = "Follow for daily sleep science"


def pt(label, title, body, source=None):
    d = {"kind": "point", "label": label, "title": title, "body": body}
    if source:
        d["source"] = source
    return d


def cta(text, sub):
    return {"kind": "cta", "text": text, "sub": sub}


SRC_NIOSH = "Source: CDC NIOSH, shift work training"
SRC_YOO = "Source: Yoo et al., Current Biology, 2007"
SRC_COCH = "Source: Cochrane review, 2023"
SRC_PRA = "Source: Prather et al., Sleep, 2015"
SRC_WIN = "Source: Windred et al., Sleep, 2024"

D = "2026-10-{:02d}T12:30:00"

# A/B pair: same body, caption and CTA; only the hook slide differs.
cold_body = [
    pt("The study", "164 adults tracked their sleep",
       "A week on wrist trackers. Then cold-virus nasal drops and 5 days in quarantine.", SRC_PRA),
    pt("The result", "Short sleepers caught more colds",
       "Versus 7+ hours, under 5 hours meant about 4.5x the odds. 5 to 6 hours: about 4.2x.", SRC_PRA),
    pt("The catch", "Small study, wide error bars",
       "Only 164 people, and the ranges were wide. Treat it as a signal, not a promise.", SRC_PRA),
    pt("Most people miss this", "Sleep was tracked before the virus",
       "So the virus didn't cause the short nights. Guard your sleep in cold season.", SRC_PRA),
    cta("How many hours did you sleep last night?", "Comment your number. " + CTA_SUB),
]
cold_caption = ("In one study of 164 adults, wrist-tracked sleep under 6 hours was linked to about 4 times the odds of "
                "catching a cold after virus exposure, versus 7+ hours (Prather et al., Sleep, 2015). "
                "How many hours did you get last night? #sleep #immunity #sleepscience #healthtok #coldseason")

posts = [
    dict(id="p022", date=D.format(15), pillar="night_shift", hook_style="relatable", slot="midday", ab_group="",
         title="Your 3am crash isn't weakness",
         why_shared="Every night worker has felt this; easy 'this is you at 3am' tag for a coworker.",
         caption=("Sleepiness tends to peak between 2 a.m. and 6 a.m., and the end of a night shift is the riskiest time to be "
                  "behind the wheel (CDC NIOSH). If you're nodding off, pull over or get a ride. When does your crash hit? "
                  "#nightshift #shiftwork #sleepscience #healthtok #3amcrash"),
         slides=[
             {"text": "Your 3am crash isn't weakness", "sub": "It's your body clock"},
             pt("The dip", "Sleepiness peaks from 2 to 6 a.m.",
                "That's when your body clock's drive to stay awake is lowest.", SRC_NIOSH),
             pt("The double hit", "Night shift stacks the deck",
                "Sleep pressure builds all shift while your body clock says sleep. Both at once.", SRC_NIOSH),
             pt("Most people miss this", "The drive home is the danger",
                "End of shift is peak sleepiness. Nodding off? Pull over or get a ride.", SRC_NIOSH),
             cta("Night shifters: when does your crash hit?", "Comment your time. " + CTA_SUB),
         ]),
    dict(id="p023", date=D.format(16), pillar="why_sleep_matters", hook_style="bold_claim", slot="midday", ab_group="",
         title="One bad night makes your brain overreact",
         why_shared="Everyone has a 'snappy when tired' story; invites tagging a friend who is hangry-tired.",
         caption=("In a small brain-scan study, people kept awake overnight showed about 60% more amygdala activity to "
                  "upsetting images than people who slept (Yoo et al., 2007). What does tired you get annoyed by? "
                  "#sleep #sleepscience #brain #healthtok #psychology"),
         slides=[
             {"text": "One bad night makes your brain overreact", "sub": "What a brain-scan study found"},
             pt("The study", "26 adults, one night",
                "14 skipped sleep for a night, 12 slept normally. All then viewed images, neutral to upsetting.", SRC_YOO),
             pt("The result", "Emotional reaction: about 60% stronger",
                "Their amygdala, a brain region tied to emotion, responded about 60% more.", SRC_YOO),
             pt("The why", "The brake got weaker",
                "Its link to the prefrontal cortex, which helps keep emotions in check, was weaker.", SRC_YOO),
             pt("Most people miss this", "That 'everything is annoying' mood?",
                "Short sleep may be part of it. One small study, so it's a clue, not a diagnosis.", SRC_YOO),
             cta("What does tired you get annoyed by?", "Tell us below. " + CTA_SUB),
         ]),
    dict(id="p024", date=D.format(17), pillar="myth_bust", hook_style="myth", slot="midday", ab_group="",
         title="Blue-light glasses fix sleep? Not so fast",
         why_shared="Lots of people own a pair; the 'did yours work?' question splits the comments.",
         caption=("A 2023 Cochrane review found very low-certainty evidence on sleep and low-certainty evidence that "
                  "blue-light glasses may not ease computer eyestrain (Singh et al.). Did they work for you? "
                  "#bluelightglasses #sleep #sleepmyths #sleepscience #healthtok"),
         slides=[
             {"text": "Blue-light glasses fix sleep? Not so fast.", "sub": "What a 2023 Cochrane review found"},
             pt("Sleep", "Results were mixed",
                "6 trials, 148 people: three found better sleep, three found no difference. Evidence quality: very low.", SRC_COCH),
             pt("Eye strain", "Computer eyestrain? Maybe no help",
                "3 trials, 166 people: they may not reduce short-term eyestrain. Low-certainty evidence.", SRC_COCH),
             pt("Most people miss this", "'Unproven' isn't 'useless'",
                "The trials were small. Occupational health guidance suggests skipping the computer an hour or so before bed.", SRC_NIOSH),
             cta("Did blue-light glasses work for you?", "Yes or no in the comments. " + CTA_SUB),
         ]),
    dict(id="p025", date=D.format(18), pillar="why_sleep_matters", hook_style="stat", slot="midday", ab_group="cold-hook",
         title="Under 6 hours of sleep: 4x the cold odds",
         why_shared="A concrete number people repeat to friends who 'run on 5 hours'.",
         caption=cold_caption,
         slides=[{"text": "Under 6 hours of sleep: 4x the cold odds", "sub": "One study of 164 adults"}] + cold_body),
    dict(id="p026", date=D.format(19), pillar="sleep_score_tips", hook_style="bold_claim", slot="midday", ab_group="",
         title="Consistent sleep may beat long sleep",
         why_shared="Challenges the 'just get 8 hours' rule and calls out weekend sleep-ins.",
         caption=("In an observational study of 60,977 UK adults, more regular sleep timing was linked to lower all-cause "
                  "mortality risk, and regularity predicted it better than sleep duration (Windred et al., Sleep, 2024). "
                  "How far apart are your weekday and weekend wake times? "
                  "#sleep #sleepscore #sleepschedule #sleepscience #healthtok"),
         slides=[
             {"text": "Consistent sleep may beat long sleep", "sub": "A 61,000-person study"},
             pt("The study", "60,977 adults wore trackers",
                "Researchers measured how regular their sleep timing was, then followed them for about 6 years.", SRC_WIN),
             pt("The finding", "Steadier sleepers had lower risk",
                "The more regular groups had 20% to 48% lower risk of death from any cause.", SRC_WIN),
             pt("Head to head", "Regularity beat duration",
                "It predicted risk better than hours slept, and hours added little once regularity was counted.", SRC_WIN),
             pt("The caveat", "It shows a link, not proof",
                "Observational study: people with irregular sleep may differ in other ways.", SRC_WIN),
             pt("Most people miss this", "Your weekend wake-up time counts",
                "Try keeping it close to your weekday time, then watch your sleep score trend."),
             cta("How far apart are your weekday and weekend wake times?", "Comment your gap. " + CTA_SUB),
         ]),
    dict(id="p027", date=D.format(20), pillar="night_shift", hook_style="list", slot="midday", ab_group="",
         title="You're probably eating wrong on nights",
         why_shared="Night workers will send it to the coworker who lives on vending-machine candy.",
         caption=("Four diet suggestions for night-shift nurses from CDC NIOSH: limit eating from midnight to 6 a.m., keep a "
                  "normal meal rhythm, skip sugar-rich and low-fiber carbs when sleepy, and eat away from the work site. "
                  "General guidance, not medical advice. What's your go-to night-shift snack? "
                  "#nightshift #shiftwork #nursetok #sleepscience #healthtok"),
         slides=[
             {"text": "You're probably eating wrong on nights", "sub": "4 tips from CDC NIOSH guidance"},
             pt("Mistake 1", "Heavy eating from midnight to 6 a.m.",
                "NIOSH suggests avoiding or reducing food intake in those hours.", SRC_NIOSH),
             pt("Mistake 2", "Ignoring your normal meal rhythm",
                "Stick to normal meal timing as much as you can: three meals per 24 hours.", SRC_NIOSH),
             pt("Mistake 3", "Sugar and low-fiber carbs for energy",
                "They can increase sleepiness. Try vegetables, fruit, yogurt, eggs, nuts, or whole-grain sandwiches.", SRC_NIOSH),
             pt("Most people miss this", "Eat away from your workstation",
                "NIOSH suggests eating with colleagues in a pleasant place away from the work site.", SRC_NIOSH),
             cta("What's your go-to night-shift snack?", "Drop it below. " + CTA_SUB),
         ]),
    dict(id="p028", date=D.format(21), pillar="why_sleep_matters", hook_style="question", slot="midday", ab_group="cold-hook",
         title="Why do you get sick when you're exhausted?",
         why_shared="Relatable question; people tag the friend who always gets sick after all-nighters.",
         caption=cold_caption,
         slides=[{"text": "Why do you get sick when you're exhausted?", "sub": "One cold-virus study has a clue"}] + cold_body),
]

batch = {"batch": "2026-10-w3", "timezone": "America/New_York", "posts": posts}
json.dump(batch, open("content/batch-2026-10-w3.json", "w"), indent=2)

# sanity checks
for p in posts:
    assert len(p["title"]) <= 90, p["id"]
    assert p["caption"].count("#") == 5, (p["id"], p["caption"].count("#"))
    assert 5 <= len(p["slides"]) <= 7, p["id"]
    assert len(p["slides"][0]["text"].split()) < 10, p["id"]
    for i, s in enumerate(p["slides"], 1):
        n = len((s.get("title", "") + " " + s.get("body", "")).split())
        if n > 24:
            print("LONG", p["id"], i, n)
print(len(posts), "posts")
