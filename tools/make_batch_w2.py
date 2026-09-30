import json
CTA = {"kind": "cta", "text": "Better sleep is a skill. Get one tip a day.", "sub": "Follow for daily sleep science"}

def pt(label, title, body, source=None):
    d = {"kind": "point", "label": label, "title": title, "body": body}
    if source: d["source"] = source
    return d

SRC_NHLBI = "Source: NIH NHLBI, Stages of sleep"
SRC_EB = "Source: Ebrahim et al., Alcohol Clin Exp Res, 2013"
SRC_DEP = "Source: Depner et al., Current Biology, 2019"
SRC_SF_T = "Source: Sleep Foundation, best bedroom temperature"
SRC_AASM = "Source: AASM and SRS consensus statement, 2015"
SRC_HAG = "Source: Haghayegh et al., Sleep Med Rev, 2019"
SRC_SCU = "Source: Scullin et al., J Exp Psychol Gen, 2018"
SRC_SF_L = "Source: Sleep Foundation, light and sleep"
SRC_NIOSH = "Source: CDC NIOSH, Training for Nurses on Shift Work"
SRC_SPI = "Source: Spiegel et al., Ann Intern Med, 2004"
SRC_NAP = "Source: NASA pilot nap study, 1995"
SRC_AAA = "Source: AAA Foundation for Traffic Safety, 2016"

stage_body = [
    pt("The stages", "Sleep has light, deep, and REM stages",
       "Stage 1 is the transition into sleep, stage 2 is light sleep, and stage 3 is deep sleep. REM is when your eyes move rapidly and most dreaming happens.", SRC_NHLBI),
    pt("Early night", "Deep sleep comes first",
       "You usually spend more time in deep sleep early in the night, so the first few hours matter.", SRC_NHLBI),
    pt("Late night", "REM comes later",
       "You usually get more REM sleep later in the night, which is why cutting your sleep short tends to cut into REM.", SRC_NHLBI),
    pt("The pattern", "You cycle through it 4 to 6 times",
       "A full cycle takes roughly 80 to 100 minutes. Most people go through four to six cycles a night.", SRC_NHLBI),
    CTA,
]
cap_stage = ("Sleep runs in cycles of light, deep, and REM sleep, about 80-100 minutes each (NIH NHLBI). "
             "Deep sleep dominates early, REM later. #sleep #sleepscience #sleepcycle #healthtok #brain")

D = "2026-10-{:02d}T{}:00"
AM, MID, EVE = "07:30", "12:30", "20:30"

posts = [
 dict(id="p008", date=D.format(8, AM), pillar="why_sleep_matters", hook_style="question", slot="morning", ab_group="stages-hook",
  title="What is your brain doing while you sleep?", caption=cap_stage,
  slides=[{"text": "What is your brain doing while you sleep?", "sub": "The 4 things to know"}] + stage_body),
 dict(id="p009", date=D.format(8, EVE), pillar="myth_bust", hook_style="myth", slot="evening", ab_group="",
  title="Alcohol helps you sleep? Here's what the research says",
  caption="Alcohol can shorten the time to fall asleep, but it tends to cut REM sleep and disrupt the second half of the night (Ebrahim et al., 2013). #sleep #alcohol #sleepscience #healthtok #sleeptips",
  slides=[
   {"text": "Alcohol helps you sleep", "sub": "What the research says"},
   pt("The upside", "It can help you fall asleep faster",
      "Across studies, alcohol shortened the time it took to fall asleep at all doses tested.", SRC_EB),
   pt("The trade", "More deep sleep early, less REM",
      "Most studies found more deep sleep in the first half of the night and less REM sleep at moderate and high doses.", SRC_EB),
   pt("The cost", "The second half of the night gets worse",
      "The review found more disrupted sleep in the second half of the night, which offsets the early benefit.", SRC_EB),
   pt("So what", "Fast to fall asleep is not the same as good sleep",
      "You may drop off quickly and still get sleep that is lighter and more broken than usual."),
   CTA]),
 dict(id="p010", date=D.format(9, MID), pillar="why_sleep_matters", hook_style="question", slot="midday", ab_group="",
  title="Can you catch up on lost sleep on the weekend?",
  caption="In a small lab study, weekend recovery sleep did not prevent metabolic disruption from a week of short sleep (Depner et al., 2019). Consistency beats cramming. #sleep #sleepdebt #sleepscience #healthtok #sleeptips",
  slides=[
   {"text": "Can you catch up on lost sleep on the weekend?", "sub": "One lab study says not fully"},
   pt("The study", "Short weeknights, then a weekend to sleep in",
      "In a small lab study, people slept about 5 hours a night on weekdays, were allowed to sleep in on the weekend, then went back to 5 hours.", SRC_DEP),
   pt("The result", "Weekend recovery sleep did not prevent metabolic disruption",
      "Insulin sensitivity still dropped. The recovery group's body rhythms were also disrupted when short sleep resumed.", SRC_DEP),
   pt("Takeaway", "Sleeping in may help you feel better, but it may not undo a short week",
      "It is one small study, but it points the same way: steady sleep every night beats cramming it into the weekend."),
   CTA]),
 dict(id="p011", date=D.format(9, EVE), pillar="sleep_score_tips", hook_style="bold_claim", slot="evening", ab_group="",
  title="Your bedroom may be too warm for good sleep",
  caption="Your body cools down to fall asleep, and a bedroom around 65-68F (18-20C) supports that (Sleep Foundation). #sleeptips #sleepscore #sleephygiene #sleep #healthtok",
  slides=[
   {"text": "Your bedroom may be too warm for good sleep", "sub": "The number to aim for"},
   pt("Your body clock", "Your body cools itself to fall asleep",
      "Your temperature starts dropping about two hours before you sleep and keeps falling until the early morning.", SRC_SF_T),
   pt("The target", "Aim for 65–68°F (18–20°C)",
      "That range works with your body's natural cooling instead of against it.", SRC_SF_T),
   pt("Too warm", "A hot room interferes with cooling",
      "It can disrupt sleep quality and cut into time in the restorative stages of sleep.", SRC_SF_T),
   pt("Try this", "Turn it down before bed",
      "Lower the thermostat an hour before bedtime, use lighter bedding, or run a fan. Then watch your sleep score trend."),
   CTA]),
 dict(id="p012", date=D.format(10, AM), pillar="why_sleep_matters", hook_style="stat", slot="morning", ab_group="stages-hook",
  title="Sleeping 8 hours means a third of your life asleep. Here's what it's doing",
  caption=cap_stage,
  slides=[{"text": "You'll spend about a third of your life asleep. Here is what it is doing", "sub": "The 4 things to know"}] + stage_body),
 dict(id="p013", date=D.format(10, MID), pillar="sleep_score_tips", hook_style="list", slot="midday", ab_group="",
  title="What's actually in your sleep score?",
  caption="Sleep scores usually blend duration, stages, timing, and restlessness. Each brand weights them differently, so compare your own trend. #sleepscore #sleeptracker #sleep #sleepscience #healthtok",
  slides=[
   {"text": "What is actually in your sleep score?", "sub": "5 things trackers look at"},
   pt("1", "Duration", "Adults should get 7 or more hours on a regular basis. Most scores start here.", SRC_AASM),
   pt("2", "Sleep stages", "Trackers estimate your light, deep, and REM sleep. Deep sleep comes earlier in the night and REM later, and these are estimates, not lab measurements.", SRC_NHLBI),
   pt("3", "Timing and consistency", "Going to bed and waking at similar times each day tends to count in your favor."),
   pt("4", "Heart rate and HRV", "Many trackers include nighttime heart rate and heart rate variability. Both vary a lot from person to person, so watch your own trend."),
   pt("5", "Restlessness", "Wake-ups and movement during the night can pull a score down, even if total time in bed looks fine."),
   CTA]),
 dict(id="p014", date=D.format(11, AM), pillar="myth_bust", hook_style="myth", slot="morning", ab_group="",
  title="You need exactly 8 hours of sleep. Do you?",
  caption="The expert guideline is 7 or more hours for adults, a minimum, not a fixed target (AASM and SRS). #sleep #sleepmyths #sleepscience #healthtok #sleeptips",
  slides=[
   {"text": "You need exactly 8 hours of sleep", "sub": "What the guideline actually says"},
   pt("The guideline", "Adults should sleep 7 or more hours",
      "The American Academy of Sleep Medicine and the Sleep Research Society recommend 7 or more hours per night on a regular basis for adults 18 to 60.", SRC_AASM),
   pt("The catch", "Seven is a floor, not a target",
      "\"Seven or more\" means some people will need 8 or 9. There is no single magic number."),
   pt("Check yourself", "Go by how you feel, with 7 as the floor",
      "If you wake up rested and stay alert through the day, you are probably in your range. If you are dragging, aim higher."),
   CTA]),
 dict(id="p015", date=D.format(11, EVE), pillar="sleep_score_tips", hook_style="list", slot="evening", ab_group="",
  title="A wind-down routine backed by research",
  caption="Four evening habits with some research behind them: a warm shower, screens away, a to-do list, and a cool dark room. #sleeptips #sleephygiene #bedtimeroutine #sleep #healthtok",
  slides=[
   {"text": "A wind-down routine backed by research", "sub": "4 steps"},
   pt("1", "Take a warm shower or bath 1–2 hours before bed",
      "A review of studies found water around 104–109°F (40–43°C) at that time helped people fall asleep about 10 minutes sooner on average.", SRC_HAG),
   pt("2", "Put screens away about an hour before bed",
      "Occupational health guidance suggests avoiding computers an hour or so before bedtime, since light can signal your brain to stay alert.", SRC_NIOSH),
   pt("3", "Write tomorrow's to-do list",
      "In a sleep lab study, people who wrote a to-do list at bedtime fell asleep faster than those who wrote about what they had already done.", SRC_SCU),
   pt("4", "Keep the room cool and dark",
      "Aim for 65–68°F (18–20°C) and as dark as you can make it.", SRC_SF_T),
   CTA]),
 dict(id="p016", date=D.format(12, MID), pillar="sleep_score_tips", hook_style="question", slot="midday", ab_group="",
  title="How much light do you really need in the morning?",
  caption="Daylight can be up to 10,000 lux outdoors, while bright office lighting rarely tops 500 (Sleep Foundation). Step outside soon after waking. #sleeptips #morninglight #sleepscore #sleep #healthtok",
  slides=[
   {"text": "How much light do you really need in the morning?", "sub": "Why outside beats inside"},
   pt("The gap", "Outdoor light is far brighter than indoor light",
      "Direct sunlight can reach up to 10,000 lux. Even bright office lighting rarely goes above about 500 lux.", SRC_SF_L),
   pt("The habit", "Morning sunlight is a healthy light habit",
      "Getting morning sunlight and reducing evening light may help improve sleep quality.", SRC_SF_L),
   pt("Try this", "Step outside soon after you wake up",
      "Overcast skies are usually still brighter than indoor light, so a cloudy day still counts."),
   CTA]),
 dict(id="p017", date=D.format(12, EVE), pillar="night_shift", hook_style="list", slot="evening", ab_group="",
  title="Sleeping after a night shift: 5 tips from occupational health guidance",
  caption="Tips from CDC NIOSH guidance for night workers. Only wear sunglasses home if someone else is driving. #nightshift #shiftwork #sleeptips #sleep #healthtok",
  slides=[
   {"text": "Sleeping after a night shift: 5 tips", "sub": "From CDC NIOSH guidance"},
   pt("1", "Go straight to bed when you get home",
      "The more sleep you get before 2 pm, the better rested you will be.", SRC_NIOSH),
   pt("2", "Spend as much time in bed as you can",
      "Night workers tend to get less and poorer sleep than day workers, so protect your sleep time.", SRC_NIOSH),
   pt("3", "Make the room very dark",
      "So dark you cannot see your hand in front of your face, or wear an eye mask. Blackout shades help.", SRC_NIOSH),
   pt("4", "Block noise and interruptions",
      "Use earplugs or white noise, and ask the people around you not to disturb your sleep.", SRC_NIOSH),
   pt("5", "Sunglasses on the way home, only if someone else drives",
      "Dark sunglasses can reduce the light that signals your body to be alert. Do not wear them while driving, since they can raise drowsiness and crash risk.", SRC_NIOSH),
   CTA]),
 dict(id="p018", date=D.format(13, AM), pillar="why_sleep_matters", hook_style="stat", slot="morning", ab_group="",
  title="Two short nights raised appetite by 24% in one study",
  caption="In a small study of 12 young men, two nights of 4-hour sleep lowered leptin, raised ghrelin, and increased appetite (Spiegel et al., 2004). #sleep #sleepscience #healthtok #hunger #sleeptips",
  slides=[
   {"text": "Two short nights raised appetite by 24%", "sub": "One small study, and why tired days feel hungrier"},
   pt("The study", "12 men slept 4 hours for two nights",
      "Healthy young men in a University of Chicago study were compared after two nights of 4 hours vs two nights of 10 hours.", SRC_SPI),
   pt("The hormones", "Fullness signal down, hunger signal up",
      "Leptin, which signals fullness, fell 18%. Ghrelin, which signals hunger, rose 28%. Overall appetite rose 24%.", SRC_SPI),
   pt("The cravings", "Sweet, salty, and starchy foods won",
      "Desire for candy, cookies, chips, and bread rose, while desire for fruit, vegetables, and dairy rose much less.", SRC_SPI),
   pt("The caveat", "It is one small study",
      "It shows why tired days can feel hungrier. On short-sleep days, plan your snacks before the cravings hit."),
   CTA]),
 dict(id="p019", date=D.format(13, MID), pillar="sleep_score_tips", hook_style="bold_claim", slot="midday", ab_group="",
  title="The best nap is shorter than you think",
  caption="A 26-minute nap improved pilots' alertness by up to 54% and performance by 34% in a NASA study (1995). #nap #sleeptips #sleep #healthtok #productivity",
  slides=[
   {"text": "The best nap is shorter than you think", "sub": "What NASA found"},
   pt("The study", "A 26-minute nap helped pilots",
      "In a 1995 NASA study, pilots given a nap opportunity on long flights showed up to 54% better alertness and 34% better performance.", SRC_NAP),
   pt("The risk", "Longer naps can leave you groggy",
      "Longer naps are more likely to cause sleep inertia, that dazed, sluggish feeling. Naps of 20 to 30 minutes can boost alertness without significant grogginess.", "Source: Sleep Foundation, NASA nap"),
   pt("Try this", "Set a timer for 25 minutes",
      "Lie down somewhere dark and quiet. Give yourself a few extra minutes to fall asleep."),
   CTA]),
 dict(id="p020", date=D.format(14, AM), pillar="night_shift", hook_style="question", slot="morning", ab_group="",
  title="When should night-shift workers drink coffee?",
  caption="Guidance from CDC NIOSH: caffeine early in the shift, stop several hours before the shift ends. #nightshift #shiftwork #caffeine #sleeptips #healthtok",
  slides=[
   {"text": "When should night-shift workers drink coffee?", "sub": "What occupational health guidance says"},
   pt("The clock", "Caffeine has a half-life of 5 to 6 hours",
      "It takes about 30 minutes to kick in, and in some people it stays in the system much longer.", SRC_NIOSH),
   pt("The plan", "Use it at the start of the shift",
      "NIOSH says night workers who rely on caffeine could use it at the beginning of the shift, then stop several hours before the shift ends.", SRC_NIOSH),
   pt("The catch", "Late coffee follows you to bed",
      "A cup near the end of a night shift can leave enough caffeine to cause restlessness or waking during your sleep the next morning.", SRC_NIOSH),
   pt("Bonus", "Pair it with a nap",
      "In nurse studies, a 2.5-hour nap plus caffeine at the start of the shift had positive effects on alertness.", SRC_NIOSH),
   CTA]),
 dict(id="p021", date=D.format(14, EVE), pillar="why_sleep_matters", hook_style="stat", slot="evening", ab_group="",
  title="Under 4 hours of sleep: 11.5 times the crash risk",
  caption="Drivers who slept under 4 hours had 11.5 times the crash risk of those who slept 7 or more hours (AAA Foundation, 2016). If you're very sleepy, don't drive. #sleep #drowsydriving #sleepscience #healthtok #safety",
  slides=[
   {"text": "Under 4 hours of sleep and your crash risk is 11.5 times higher", "sub": "Compared with 7+ hours"},
   pt("The study", "7,234 drivers in 4,571 crashes",
      "The AAA Foundation analyzed a national crash survey and compared crash risk by how much the driver had slept.", SRC_AAA),
   pt("The ladder", "Risk climbs as sleep drops",
      "6–7 hours: 1.3 times. 5–6 hours: 1.9 times. 4–5 hours: 4.3 times. Under 4 hours: 11.5 times.", SRC_AAA),
   pt("The point", "Even one or two hours short matters",
      "Sleeping 5–6 hours was linked to nearly double the crash risk compared with 7 or more hours.", SRC_AAA),
   pt("Do this", "If you are very sleepy, do not drive",
      "Pull over somewhere safe or let someone else drive. Save the trip for when you have slept."),
   CTA]),
]
json.dump({"batch": "2026-10-w2", "timezone": "America/New_York", "posts": posts}, open("content/batch-2026-10-w2.json", "w"), indent=2)
print(len(posts), "posts")
