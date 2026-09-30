import json
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
       "Participants did not always feel that their sleep was worse. The effect can be there even when you feel fine."),
    pt("The dose", "400 mg is about four cups of coffee",
       "Smaller amounts have smaller effects, but timing still matters. Sensitivity varies a lot from person to person."),
    pt("Try this", "Set a caffeine cutoff at least 8 hours before bed",
       "Bed at 11 pm? Last coffee around 3 pm. Give it a week and watch your sleep score trend."),
    CTA,
]
cap_coffee = ("Caffeine is linked to less sleep even when taken 6 hours before bed (Drake et al., J Clin Sleep Med, 2013). "
              "Try an earlier cutoff for a week and see what your sleep trend does. #sleep #sleeptips #sleepscore #caffeine #healthtok")

posts = [
 dict(id="p001", date="2026-10-01T07:30:00", pillar="why_sleep_matters", hook_style="stat", slot="morning", ab_group="",
  title="17 hours awake can impair you like a drink",
  caption="After 17-19 hours awake, performance dropped to the level seen at 0.05% blood alcohol in one well-known study (Williamson & Feyer, 2000). Protect your sleep. #sleep #sleepscience #healthtok #sleeptips #sleepscore",
  slides=[
   {"text": "17 hours awake and your brain performs like you've had a drink", "sub": "What sleep loss does to you"},
   pt("The research", "After 17–19 hours awake, performance matched 0.05% blood alcohol",
      "In a widely cited study, reaction time and accuracy on tests dropped to the level seen at a blood alcohol concentration of 0.05%.", SRC_WF),
   pt("Go further", "At 24 hours awake it was around 0.10%",
      "That is above the 0.08% US legal driving limit. Being awake a full day is not a small thing."),
   pt("The trap", "People tend to underestimate how impaired they are",
      "Attention, reaction time, and judgement slip first, and those are the skills you use to notice that you're slipping."),
   pt("What helps", "Protect a consistent wake time",
      "Get light in your first hour awake and keep caffeine earlier in the day. Small habits that support better sleep."),
   CTA]),
 dict(id="p002", date="2026-10-02T12:30:00", pillar="sleep_score_tips", hook_style="list", slot="midday", ab_group="",
  title="5 things that can raise your sleep score",
  caption="Five habits that tend to support better sleep and a better sleep score. Pick one and run it for a week. #sleepscore #sleeptips #sleep #sleephygiene #healthtok",
  slides=[
   {"text": "5 things that can raise your sleep score", "sub": "Start with number 1"},
   pt("1", "Wake at the same time every day", "Even weekends. A steady wake time helps anchor your body clock, and regular sleep is linked to better sleep quality."),
   pt("2", "Get morning light", "A few minutes to half an hour outside in your first hour awake helps set your body clock for the night ahead."),
   pt("3", "Cool and dark", "Around 65°F (18°C) and as dark as you can make it. Blackout curtains or a mask both work."),
   pt("4", "Set a caffeine cutoff", "Many experts suggest stopping 8 or more hours before bed. Caffeine can cut sleep even 6 hours out."),
   pt("5", "Wind down for 30 minutes", "Dim the lights and do something calm. Give your brain a runway instead of a cliff."),
   CTA]),
 dict(id="p003", date="2026-10-03T20:30:00", pillar="myth_bust", hook_style="myth", slot="evening", ab_group="",
  title="Your sleep score is not a medical number",
  caption="Wearable sleep scores are estimates, not a sleep lab. Trends over weeks are more useful than any single night. #sleepscore #sleep #sleepscience #wearables #healthtok",
  slides=[
   {"text": "Your sleep score is not a medical number", "sub": "Here is how to use it anyway"},
   pt("What it is", "An estimate from movement and heart rate", "Most wearables model your sleep. A sleep lab measures brain activity directly, and that is the gold standard."),
   pt("Why trends win", "One bad night means very little", "Look at your two-week average. Trends show what your habits are doing, and single nights are mostly noise."),
   pt("What moves it", "Duration, consistency, and a calmer night", "Alcohol and late heavy meals tend to raise nighttime heart rate, which tends to pull scores down."),
   pt("How to use it", "Change one habit, watch the trend", "Pick one change for a week: caffeine cutoff, wake time, or room temperature. Then compare."),
   CTA]),
 dict(id="p004", date="2026-10-04T07:30:00", pillar="why_sleep_matters", hook_style="question", slot="morning", ab_group="",
  title="Why do you wake up tired after 8 hours?",
  caption="Hours are only part of the story. Timing, sleep quality, and sometimes a sleep disorder matter too. If you're tired every day, talk to a doctor. #sleep #sleeptips #sleepscience #healthtok #tired",
  slides=[
   {"text": "Why do you wake up tired after 8 hours?", "sub": "4 common reasons"},
   pt("1", "Your schedule is inconsistent", "Shifting sleep by a couple of hours on weekends is sometimes called social jet lag, and it can leave you groggy on Monday."),
   pt("2", "Sleep inertia", "Waking from deep sleep can cause grogginess that typically fades within about 30 minutes. Light and movement help."),
   pt("3", "Quality, not just quantity", "Alcohol, noise, light, and heat can fragment sleep so 8 hours in bed is less than 8 hours of good sleep."),
   pt("4", "Something medical", "If you are tired every day despite enough time in bed, ask a doctor. Sleep apnea is common and often missed."),
   CTA]),
 dict(id="p005", date="2026-10-05T12:30:00", pillar="sleep_score_tips", hook_style="stat", slot="midday", ab_group="coffee-hook",
  title="Coffee 6 hours before bed cost over an hour of sleep",
  caption=cap_coffee,
  slides=[{"text": "Coffee 6 hours before bed cost people over an hour of sleep", "sub": "One study, and what to do about it"}] + coffee_body),
 dict(id="p006", date="2026-10-06T20:30:00", pillar="why_sleep_matters", hook_style="bold_claim", slot="evening", ab_group="",
  title="Sleep is the most underrated performance upgrade",
  caption="Memory, mood, immunity, and safety all lean on sleep. Most adults need 7 or more hours. #sleep #sleepscience #healthtok #sleeptips #sleepscore",
  slides=[
   {"text": "Sleep is the most underrated performance upgrade", "sub": "It's free. Here's what it does."},
   pt("Memory", "Sleep helps lock in what you learned", "While you sleep, your brain consolidates memories from the day. Cutting sleep short cuts that process."),
   pt("Mood", "Short sleep is linked to lower mood and higher stress", "When you're underslept, small problems tend to feel bigger."),
   pt("Immunity", "Short sleepers caught more colds", "In one study, people sleeping under 6 hours had roughly four times the odds of catching a cold after virus exposure versus 7+ hours.", SRC_PR),
   pt("Safety", "Reaction time and accuracy drop with less sleep", "That is why fatigue is a factor in many accidents, from driving to the workplace."),
   pt("How much", "Most adults need 7 or more hours", "That is the consensus recommendation from the American Academy of Sleep Medicine and the Sleep Research Society."),
   CTA]),
 dict(id="p007", date="2026-10-07T12:30:00", pillar="sleep_score_tips", hook_style="question", slot="midday", ab_group="coffee-hook",
  title="Is your afternoon coffee ruining your sleep?",
  caption=cap_coffee,
  slides=[{"text": "Is your afternoon coffee ruining your sleep?", "sub": "One study, and what to do about it"}] + coffee_body),
]
json.dump({"batch": "2026-10-w1", "timezone": "America/New_York", "posts": posts}, open("content/batch-2026-10-w1.json", "w"), indent=2)
print(len(posts), "posts")
