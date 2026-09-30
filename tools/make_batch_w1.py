import json
# Revision 2: wording tightened to match sources (see git history for rev 1).
CTA = {"kind": "cta", "text": "Better sleep is a skill. Get one tip a day.", "sub": "Follow for daily sleep science"}
SRC_WF = "Source: Williamson & Feyer, Occup Environ Med, 2000"
SRC_DR = "Source: Drake et al., J Clin Sleep Med, 2013"
SRC_PR = "Source: Prather et al., Sleep, 2015"

def pt(label, title, body, source=None):
    d = {"kind": "point", "label": label, "title": title, "body": body}
    if source: d["source"] = source
    return d

coffee_body = [
    pt("The study", "Caffeine 6 hours before bed still cost over an hour of sleep",
       "Researchers gave people 400 mg of caffeine 0, 3, or 6 hours before bedtime. Even the 6-hour group slept over an hour less.", SRC_DR),
    pt("The catch", "You may not notice it",
       "Participants were unaware of the sleep disturbance, even though it showed up when their sleep was measured objectively."),
    pt("The dose", "400 mg is roughly 2 to 4 cups of coffee",
       "The exact number depends on cup size and how strong the coffee is. Sensitivity also varies from person to person."),
    pt("Try this", "Set a caffeine cutoff more than 6 hours before bed",
       "Bed at 11 pm? Last coffee by 5 pm or earlier. Give it a week and watch your sleep score trend."),
    CTA,
]
cap_coffee = ("Caffeine taken 6 hours before bed cut sleep by over an hour in a lab study (Drake et al., J Clin Sleep Med, 2013). "
              "Try an earlier cutoff for a week and see what your sleep trend does. #sleep #sleeptips #sleepscore #caffeine #healthtok")

posts = [
 dict(id="p001", rev=2, date="2026-10-01T07:30:00", pillar="why_sleep_matters", hook_style="stat", slot="morning", ab_group="",
  title="17 hours awake can impair you like a drink",
  caption="After 17-19 hours awake, response speed and accuracy were as poor as at 0.05% blood alcohol, or worse, in one well-known study (Williamson & Feyer, 2000). Protect your sleep. #sleep #sleepscience #healthtok #sleeptips #sleepscore",
  slides=[
   {"text": "17 hours awake and your brain performs like you've had a drink", "sub": "What sleep loss does to you"},
   pt("The research", "After 17–19 hours awake, performance was as poor as at 0.05% blood alcohol, or worse",
      "In a widely cited study, response speeds were up to 50% slower on some tests and accuracy was worse than at a blood alcohol level of 0.05%.", SRC_WF),
   pt("Go further", "After longer without sleep, it reached the 0.10% level",
      "Performance matched the level seen at 0.10%, the highest alcohol dose in the study. That is above the 0.08% US legal driving limit.", SRC_WF),
   pt("Why it matters", "Speed and accuracy both dropped",
      "Slower responses and more mistakes are a bad combination for driving, clinical work, or anything safety-critical."),
   pt("What helps", "Protect a consistent wake time",
      "Get light in your first hour awake and keep caffeine earlier in the day. Small habits that support better sleep."),
   CTA]),
 dict(id="p002", rev=2, date="2026-10-02T12:30:00", pillar="sleep_score_tips", hook_style="list", slot="midday", ab_group="",
  title="5 things that can raise your sleep score",
  caption="Five habits that tend to support better sleep and a better sleep score. Pick one and run it for a week. #sleepscore #sleeptips #sleep #sleephygiene #healthtok",
  slides=[
   {"text": "5 things that can raise your sleep score", "sub": "Start with number 1"},
   pt("1", "Wake at the same time every day", "Even weekends. A steady wake time helps anchor your body clock."),
   pt("2", "Get morning light", "Step outside soon after waking. Daylight is far brighter than indoor light, which helps set your body clock."),
   pt("3", "Cool and dark", "Aim for about 65–68°F (18–20°C) and as dark as you can make it. Blackout curtains or a mask both work."),
   pt("4", "Set a caffeine cutoff", "Stop well before bed. In one study, caffeine 6 hours before bed still cut sleep by over an hour."),
   pt("5", "Wind down for 30 minutes", "Dim the lights and do something calm. Give your brain a runway instead of a cliff."),
   CTA]),
 dict(id="p003", rev=2, date="2026-10-03T20:30:00", pillar="myth_bust", hook_style="myth", slot="evening", ab_group="",
  title="Your sleep score is not a medical number",
  caption="Wearable sleep scores are estimates, not a sleep lab. Trends over weeks are more useful than any single night. #sleepscore #sleep #sleepscience #wearables #healthtok",
  slides=[
   {"text": "Your sleep score is not a medical number", "sub": "Here is how to use it anyway"},
   pt("What it is", "An estimate from movement and heart rate", "Most wearables model your sleep. A sleep lab measures brain activity directly, and that is the gold standard."),
   pt("Why trends win", "One bad night means very little", "Look at your two-week average. Trends show what your habits are doing, and single nights are mostly noise."),
   pt("What moves it", "Duration, consistency, and a calmer night", "Habits like alcohol and late meals can make nights more restless, which trackers may score lower."),
   pt("How to use it", "Change one habit, watch the trend", "Pick one change for a week: caffeine cutoff, wake time, or room temperature. Then compare."),
   CTA]),
 dict(id="p004", rev=2, date="2026-10-04T07:30:00", pillar="why_sleep_matters", hook_style="question", slot="morning", ab_group="",
  title="Why do you wake up tired after 8 hours?",
  caption="Hours are only part of the story. Timing, sleep quality, and sometimes a sleep disorder matter too. If you're tired every day, talk to a doctor. #sleep #sleeptips #sleepscience #healthtok #tired",
  slides=[
   {"text": "Why do you wake up tired after 8 hours?", "sub": "4 common reasons"},
   pt("1", "Your schedule is inconsistent", "Shifting sleep by a couple of hours on weekends is sometimes called social jet lag, and it can leave you groggy on Monday."),
   pt("2", "Sleep inertia", "Waking from deep sleep can cause grogginess called sleep inertia. It usually fades, and light and movement can help."),
   pt("3", "Quality, not just quantity", "Alcohol, noise, light, and heat can fragment sleep so 8 hours in bed is less than 8 hours of good sleep."),
   pt("4", "Something medical", "If you are tired every day despite enough time in bed, ask a doctor. Sleep apnea is common and often missed."),
   CTA]),
 dict(id="p005", rev=2, date="2026-10-05T12:30:00", pillar="sleep_score_tips", hook_style="stat", slot="midday", ab_group="coffee-hook",
  title="Caffeine 6 hours before bed cost people over an hour of sleep",
  caption=cap_coffee,
  slides=[{"text": "Caffeine 6 hours before bed cost people over an hour of sleep", "sub": "One study, and what to do about it"}] + coffee_body),
 dict(id="p006", rev=2, date="2026-10-06T20:30:00", pillar="why_sleep_matters", hook_style="bold_claim", slot="evening", ab_group="",
  title="Sleep is the most underrated performance upgrade",
  caption="Memory, mood, immunity, and safety all lean on sleep. Adults should get 7 or more hours (AASM and SRS). #sleep #sleepscience #healthtok #sleeptips #sleepscore",
  slides=[
   {"text": "Sleep is the most underrated performance upgrade", "sub": "It's free. Here's what it does."},
   pt("Memory", "Sleep helps lock in what you learned", "While you sleep, your brain consolidates memories from the day. Cutting sleep short cuts that process."),
   pt("Mood", "Short sleep is linked to lower mood and higher stress", "When you're underslept, small problems tend to feel bigger."),
   pt("Immunity", "Short sleepers were more likely to catch a cold", "In one study of 164 adults, those sleeping under 6 hours were about 4.2 times more likely to catch a cold than those sleeping over 7 hours.", SRC_PR),
   pt("Safety", "Reaction time and accuracy drop with less sleep", "That is why fatigue is a factor in many accidents, from driving to the workplace."),
   pt("How much", "Adults should get 7 or more hours", "That is the consensus recommendation from the American Academy of Sleep Medicine and the Sleep Research Society.", "Source: AASM and SRS consensus statement, 2015"),
   CTA]),
 dict(id="p007", rev=2, date="2026-10-07T12:30:00", pillar="sleep_score_tips", hook_style="question", slot="midday", ab_group="coffee-hook",
  title="Is your afternoon coffee ruining your sleep?",
  caption=cap_coffee,
  slides=[{"text": "Is your afternoon coffee ruining your sleep?", "sub": "One study, and what to do about it"}] + coffee_body),
]
json.dump({"batch": "2026-10-w1", "timezone": "America/New_York", "posts": posts}, open("content/batch-2026-10-w1.json", "w"), indent=2)
print(len(posts), "posts")
