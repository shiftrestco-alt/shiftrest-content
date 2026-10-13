"""Lazard (global) contacts from Boden's list -> lazard.json. Emails as supplied; "Check" notes kept."""
import json, os
NOW = "2026-10-13T20:00:00.000Z"
T, TP = "Technician", "Team Player"
L = """Kamel Habiballah||kamel.habiballah@lazard.com|Verified
Jason Sendek|Investment Banking Analyst|jason.sendek@lazard.com|
Alex Kirchgäßner|Investment Banking Analyst|alex.kirchgaessner@lazard.com|Check: may be alexander.
Aidan Mcclish|Investment Banking Analyst|aidan.mcclish@lazard.com|
Isabelle Carpenter|Investment Banking Analyst|isabelle.carpenter@lazard.com|
Zachary Bryant|Investment Banking Analyst|zachary.bryant@lazard.com|List had bryantz@lazard.com (off-pattern); using the standard format. If it bounces, try bryantz@.
Helena Kagan|Investment Banking Analyst|helena.kagan@lazard.com|
Tyler Pagaduan|Investment Banking Analyst|tyler.pagaduan@lazard.com|
Anna McFadzean|Investment Banking Analyst|anna.mcfadzean@lazard.com|
Kai Jackson|Investment Banking Analyst|kai.jackson@lazard.com|Common name: may have variant
Hattie Norman|Investment Banking Analyst|hattie.norman@lazard.com|
Rebecka Mofors|Investment Banking Analyst|rebecka.mofors@lazard.com|Check location
Avi Kapadia|Investment Banking Analyst|avi.kapadia@lazard.com|
Audrey Granmayeh|Investment Banking Analyst|audrey.granmayeh@lazard.com|
Michael Negrea|Investment Banking Analyst|michael.negrea@lazard.com|
Amrit Aggarwal|Investment Banking Analyst|amrit.aggarwal@lazard.com|
Erica Sinha|Investment Banking Analyst|erica.sinha@lazard.com|
David Villarroel|Investment Banking Analyst|david.villarroel@lazard.com|
Yannick Brugger|Investment Banking Analyst|yannick.brugger@lazard.com|Check location
Enrique Tombas|Investment Banking Analyst|enrique.tombas@lazard.com|
Anne Victoire Hénon|M&A Analyst|anne-victoire.henon@lazard.com|Check: hyphenated name; check location
Lilou Biche|M&A Analyst|lilou.biche@lazard.com|Check location
Tadhg Downey|Private Equity Analyst|tadhg.downey@lazard.com|
Daniel Sung|Investment Banking Associate|daniel.sung@lazard.com|Common name: may have variant
Clare Everts|Investment Banking Associate|clare.everts@lazard.com|
Maximilian Molinari|Investment Banking Associate|maximilian.molinari@lazard.com|
Eric Bostrom|Investment Banking Associate|eric.bostrom@lazard.com|List had eric.bostroem@; name is spelled Bostrom, so using eric.bostrom@. If it bounces, try bostroem.
Sacha Moorhouse|Investment Banking Associate|sacha.moorhouse@lazard.com|Check location
Lydia Kirsch|Investment Banking Associate|lydia.kirsch@lazard.com|
David Warren|Investment Banking Associate|david.warren@lazard.com|Common name: may have variant
Yasemin Kaca|Investment Banking Associate|yasemin.kaca@lazard.com|Check location
Jack Giletto|Investment Banking Associate|jack.giletto@lazard.com|
Emily Sanchez|Investment Banking Associate|emily.sanchez@lazard.com|Common name: may have variant
Vivek Singh|Investment Banking Associate|vivek.p.singh@lazard.com|Middle initial: plausible, verify
Zain Baquer|Investment Banking Associate|zain.baquer@lazard.com|
Corentin Giroux|M&A Associate|corentin.giroux@lazard.com|Check location
Sona Mkrttchian|Restructuring Associate|sona.mkrttchian@lazard.com|Check: spelling on LinkedIn
Sebastian Laso|Director Vice President Associate|sebastian.laso@lazard.com|Senior: confirm group
Tobi Clarke|Associate|tobi.clarke@lazard.com|Confirm group
Olivia Zhang|Analyst|olivia.zhang@lazard.com|Confirm group; common name
Ally Chan|Analyst|ally.chan@lazard.com|Confirm group; common name
Caitlin Martin|Analyst|caitlin.martin@lazard.com|Confirm group; common name
Sam Ende|Strategy Analyst|sam.ende@lazard.com|Non-IB
Lirim Begoli|Quantitative Risk Analyst|lirim.begoli@lazard.com|Non-IB
Alice Cousins|Corporate Events Associate|alice.cousins@lazard.com|Non-IB
Alexa Weil|Global Communications Associate|alexa.weil@lazard.com|Non-IB
Arjita Jaiswal|Full Stack Associate|arjita.jaiswal@lazard.com|Non-IB
Alvin Cheriyan|IT Support Analyst|alvin.cheriyan@lazard.com|Non-IB
Ashley Bustos|IT Analyst|ashley.bustos@lazard.com|Non-IB
Shaina Davis|Information Security Analyst|shaina.davis@lazard.com|Non-IB
Kirsty Tew|Client Services Associate|kirsty.tew@lazard.com|Non-IB"""

contacts = {}
for i, line in enumerate(L.splitlines(), 1):
    name, role, email, note = line.split("|")
    nonib = note == "Non-IB"
    ib = role in ("Investment Banking Analyst","M&A Analyst","Private Equity Analyst","Investment Banking Associate","M&A Associate","Restructuring Associate")
    persona = TP if ("Associate" in role and not nonib) or "Vice President" in role else T
    rank = 3 if nonib else (1 if ib and not note.startswith("Check") else 2)
    notes = "Lazard (from Boden's list). " + (note + ". " if note and not note.endswith(".") else (note + " " if note else ""))
    if "location" in note.lower(): notes += "May be outside the US: check their office before pitching a US summer role. "
    if nonib: notes += "Not in banking: ask for a pointer to an analyst or recruiter."
    contacts[f"lz{i:03d}"] = dict(firmId="lazard", name=name, role=role or "Title not listed", email=email, linkedin="", persona=persona, rank=rank,
        variantPref="v-lazard-nonib" if nonib else "", stage="todo", notes=notes.strip(), createdAt=NOW, sentAt="", lastTouchAt="",
        nextFollowUpAt="", followUps=0, variantId="", subject="", test={}, touches=[], source="lazard-list")

firms = {"lazard": dict(name="Lazard", tier="Elite boutique · Financial advisory", location="New York · London · Paris · global", priority=2,
    status="Today's focus", statusTone="urgent", keyDate="", keyDateLabel="Check Lazard careers for 2028 summer analyst timing.",
    program="Financial Advisory (M&A, restructuring, capital markets advisory). Summer analyst programs; confirm sophomore/2028 timing on the careers site.",
    eligibility="Confirm class-year eligibility on the posting. Some contacts may sit in non-US offices.",
    avatar="The Pure Advisor",
    avatarNotes="Independent advisory firm: no lending book, so the pitch is judgment and advice. Known for M&A and restructuring. Analysts and associates are your best contacts.",
    emailPattern="{first}.{last}@lazard.com", emailConfidence="first.last@ (one address verified)", createdAt=NOW)}

D = {T:"Proof you can do the work", TP:"Someone reliable they'd staff"}
def V(persona, subject, body, angle, mech, cta, **kw):
    return dict(firmId="lazard", persona=persona, desire=D[persona], angle=angle, mechanism=mech, cta=cta, subject=subject,
        hook=body.split("\n\n")[1].split(". ")[0]+".", body=body, label=f"LAZARD · {persona}", active=True, source="starter", createdAt=NOW, **kw)
SIG = "\n\n{signature}"
variants = {
 "v-lazard-tech-advice": V(T, "Pure advice, from a sophomore's seat",
   "Hi {first},\n\nLazard is one of the few banks that only advises, with no balance sheet to sell, and that's what draws me to it. I'm a finance sophomore at Iona University (3.9 GPA) and an overnight EMT in the Stamford Hospital ER.\n\nWould you have 10 minutes to tell me what your first year as an analyst actually looked like?" + SIG,
   "Firm model (pure advisory)", "3.9 GPA + SIE + BMC", "10-minute call"),
 "v-lazard-tech-er": V(T, "Night-shift EMT, learning to model",
   "Hi {first},\n\nI work 12-hour overnight shifts in the Stamford Hospital ER and spend my days learning DCFs and comps. I'm a 3.9 finance sophomore at Iona, recruiting for 2028 summer analyst roles.\n\nCould I get 10 minutes on how you pressure-test a model as an analyst at Lazard?" + SIG,
   "ER / EMT story", "EMT overnight shifts", "Critique my work"),
 "v-lazard-team-great": V(TP, "What makes a great Lazard analyst?",
   "Hi {first},\n\nI'm a finance sophomore at Iona University (3.9 GPA) who works overnight shifts as an EMT in the Stamford Hospital ER. You staff analysts every week, so you'd know better than anyone what separates the great ones at Lazard.\n\nWould you have 10 minutes to share your perspective?" + SIG,
   "Their own words", "EMT overnight shifts", "10-minute call"),
 "v-lazard-team-triage": V(TP, "Triage, then the model",
   "Hi {first},\n\nIn the ER, triage means ranking five urgent things in seconds and handing off cleanly. I think that's most of an analyst's job on a live deal. I'm a 3.9 finance sophomore at Iona, recruiting for 2028 summer analyst roles.\n\nWould you have 10 minutes to tell me if I've got that right?" + SIG,
   "ER / EMT story", "EMT overnight shifts", "10-minute call"),
 "v-lazard-nonib": V(T, "Quick pointer at Lazard?",
   "Hi {first},\n\nI'm a finance sophomore at Iona University (3.9 GPA) recruiting for Lazard's summer analyst program. I know banking isn't your team, but you know the firm far better than I do.\n\nIs there an analyst or recruiter you'd suggest I talk to? Even a name would help." + SIG,
   "Their own words", "3.9 GPA + SIE + BMC", "Point me to the right person", prefOnly=True),
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lazard.json")
json.dump({"firms":firms,"contacts":contacts,"variants":variants}, open(out,"w"), indent=1, ensure_ascii=False)
from collections import Counter
print(len(contacts), Counter(c["rank"] for c in contacts.values()), Counter(c["persona"] for c in contacts.values()))
