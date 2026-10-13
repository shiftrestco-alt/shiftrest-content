"""International contacts (Australia + London) from Boden's research notes -> international.json.

Only emails the research marked as published are filled in, plus one flagged guess (Hardik Madlani).
Everyone else is reached through LinkedIn or the firm's recruiting inbox.
"""
import json, os

NOW = "2026-10-13T19:30:00.000Z"
T, TP, MD, GK = "Technician", "Team Player", "MD / Partner", "Gatekeeper"
VISA = "International role: confirm eligibility for US students and work rights before applying."

def firm(name, tier, loc, pri, status, tone, avatar, notes, pattern="", conf="", keyDate="", keyLabel="", program="", elig=""):
    return dict(name=name, tier=tier, location=loc, priority=pri, status=status, statusTone=tone, avatar=avatar, avatarNotes=notes,
                emailPattern=pattern, emailConfidence=conf, keyDate=keyDate, keyDateLabel=keyLabel, program=program,
                eligibility=elig or VISA, createdAt=NOW)

firms = {
 "hsbc": firm("HSBC (London)", "International · Bulge bracket", "London, UK", 1, "Closes Oct 15", "urgent", "The Global Connector",
    "Global Head of IB per the 2025 restructuring: Adam Bagshaw. Senior names only; no verified emails. Apply first, then network.",
    keyDate="2026-10-15", keyLabel="2027 London IB Summer Internship closes",
    program="2027 London Investment Banking Summer Internship. Posting says 2028 graduates are eligible and visa sponsorship may be considered.",
    elig="2028 graduates eligible per posting; visa sponsorship may be considered."),
 "jefferies": firm("Jefferies (London)", "International · Investment bank", "London, UK", 19, "Published emails", "open", "The Hungry Challenger",
    "Published professional emails in an April 2025 research deck (roles may have changed). Hardik Madlani runs healthcare IB in London: lead with the ER angle.",
    pattern="{f}{last}@jefferies.com", conf="Mixed: flast@ and first.last@ both used"),
 "lazard-au": firm("Lazard Australia", "International · M&A advisory", "Sydney / Melbourne", 20, "Ask directly", "neutral", "The Quiet Advisor",
    "Strong public team directory. Contact associates and analysts before the CEO: they have recent internship experience. Australian summer runs Dec–Feb.",
    conf="No individual emails verified; use recruitment@lazardaustralia.com or LinkedIn"),
 "adastra": firm("Ad Astra Corporate Advisory", "International · Boutique M&A", "Sydney, Australia", 21, "Ask directly", "neutral", "The Bulge-Bracket Alumni Boutique",
    "Team includes ex-Goldman, Citi and JPMorgan bankers. Edmond Chan and Priyanka Garg cover healthcare. Melanie Trezise handles HR and admin.",
    conf="Only info@adastraca.com.au published"),
 "optilic": firm("Optilic", "International · Quant prop trading", "Sydney, Australia", 22, "Ask directly", "neutral", "The Garage Quant Shop",
    "Small, newly established firm. Founder Nima Entazami supervises intern projects directly. Pay and terms agreed individually.",
    conf="careers@optilic.com for internships"),
 "recordpoint": firm("Record Point", "International · IB boutique", "Sydney, Australia", 23, "Deadline passed", "neutral", "The Deal Floor",
    "Interns work with senior bankers on live transactions. Dec 2026–Jan 2027 program (penultimate-year students) closed July 30, 2026. Ask about the next intake.",
    conf="careers@record-point.com"),
}

# name, role, firm, persona, rank, email, notes, variantPref
P = [
 ("Robin Basra","Associate","lazard-au",TP,1,"","No verified email; connect on LinkedIn or write via recruitment@lazardaustralia.com.",""),
 ("Chloe Kostopoulos","Analyst","lazard-au",T,1,"","No verified email; connect on LinkedIn.",""),
 ("Summer Haidar","Vice President","lazard-au",TP,1,"","No verified email; connect on LinkedIn.",""),
 ("Will Manuell","Associate","lazard-au",TP,2,"","No verified email; connect on LinkedIn.",""),
 ("Matthew Bailey","Analyst","lazard-au",T,2,"","No verified email; connect on LinkedIn.",""),
 ("Rohan Bhatt","Analyst","lazard-au",T,2,"","No verified email; connect on LinkedIn.",""),
 ("Juliet McBurney","Analyst","lazard-au",T,2,"","No verified email; connect on LinkedIn.",""),
 ("Campbell Ray","Managing Director","lazard-au",MD,2,"","No verified email.",""),
 ("Michael Sandford","Director","lazard-au",MD,2,"","No verified email.",""),
 ("Andrew Leyden","CEO / Managing Director","lazard-au",MD,3,"","Very senior. Contact last, if at all.",""),
 ("Lazard Australia Recruitment","Recruiting inbox","lazard-au",GK,1,"recruitment@lazardaustralia.com","Verified recruiting email. Ask about eligibility for US students and timing.",""),
 ("Edmond Chan","Partner · Healthcare, financial services, M&A","adastra",MD,1,"","Ex-JPMorgan. Healthcare M&A: lead with the ER angle. No direct email; LinkedIn, or info@adastraca.com.au addressed to him.","v-hc-md"),
 ("Priyanka Garg","Partner · Valuation, strategic reviews, healthcare","adastra",MD,1,"","Ex-Goldman (international). No direct email; LinkedIn, or info@ addressed to her.","v-hc-md"),
 ("Peng Ly","Managing Partner · M&A, infrastructure, healthcare, government","adastra",MD,2,"","No direct email.","v-hc-md"),
 ("Melanie Trezise","Head of Operations (HR, admin, compliance)","adastra",GK,1,"info@adastraca.com.au","General company inbox: put 'Attn: Melanie Trezise' in the subject. Ask about internship eligibility.",""),
 ("Ben Smith","Managing Partner / Chair","adastra",MD,3,"","Very senior. No direct email.",""),
 ("James Ye","Partner · M&A, technology and services","adastra",MD,3,"","No direct email.",""),
 ("Ze Hu","Partner · Technology M&A and capital markets","adastra",MD,3,"","No direct email.",""),
 ("Nima Entazami","Founder · quant trading research","optilic",MD,1,"careers@optilic.com","Supervises intern projects directly. careers@ is the published internship inbox; address it to him.",""),
 ("Record Point Recruiting","Careers inbox","recordpoint",GK,2,"careers@record-point.com","Ask when the next intake opens and whether an analyst or associate would talk.",""),
 ("Hardik Madlani","Managing Director, Healthcare Investment Banking (London)","jefferies",MD,1,"hmadlani@jefferies.com","Email is a guess from Jefferies' flast@ format; verify. Your EMT background is the hook here.","v-hc-md"),
 ("Nandan Shinkre","European Head of TMT","jefferies",MD,1,"nshinkre@jefferies.com","Email published by Jefferies (Apr 2025); role may have changed.",""),
 ("Justin Liu","Senior Vice President, Americas","jefferies",TP,2,"justin.liu@jefferies.com","Email published by Jefferies (Apr 2025). US-based: easiest time zone.",""),
 ("Gaurav Kittur","Global Head of Internet Investment Banking","jefferies",MD,3,"gkittur@jefferies.com","Email published by Jefferies (Apr 2025). Very senior.",""),
 ("Cameron Lester","Global Co-Head of TMT","jefferies",MD,3,"clester@jefferies.com","Email published by Jefferies (Apr 2025). Very senior.",""),
 ("Dominic Lester","Head of EMEA","jefferies",MD,3,"dlester@jefferies.com","Email published by Jefferies (Apr 2025). Very senior.",""),
 ("Joe Porter","Global Co-Head, Software Investment Banking (London)","gs",MD,2,"","London-based. No verified email; don't assume first.last@gs.com. LinkedIn.",""),
]
contacts = {}
for i,(name,role,fid,persona,rank,email,note,pref) in enumerate(P,1):
    contacts[f"in{i:03d}"] = dict(firmId=fid, name=name, role=role, email=email, linkedin="", persona=persona, rank=rank,
        variantPref=pref, stage="todo", notes=note + (" " + VISA if fid not in ("gs","jefferies") or "London" in role else ""),
        createdAt=NOW, sentAt="", lastTouchAt="", nextFollowUpAt="", followUps=0, variantId="", subject="", test={}, touches=[], source="intl-research")

def V(firmId, persona, subject, body, angle, mech, cta, desire, **kw):
    return dict(firmId=firmId, persona=persona, desire=desire, angle=angle, mechanism=mech, cta=cta, subject=subject, hook=body.split("\n\n")[1].split(". ")[0]+".",
                body=body, label=f"{(firmId or 'generic').upper()} · {persona}", active=True, source="starter", createdAt=NOW, **kw)
D = {MD:"Relevance and a reason to care", T:"Proof you can do the work", GK:"Eligibility, clarity, zero extra work"}
variants = {
 "v-hc-md": V("", MD, "Healthcare deals, seen from the ER",
   "Hi {first},\n\nI'm a finance sophomore at Iona University in New York (3.9 GPA), and I work overnight shifts as an EMT in the Stamford Hospital ER, so I see the provider side of healthcare up close. Your healthcare work at {firm} is the side of finance I most want to learn.\n\nWould you have 10 minutes for a call? Happy to work around the time difference.\n\n{signature}",
   "ER / EMT story","EMT overnight shifts","10-minute call",D[MD], prefOnly=True),
 "v-any-md": V("", MD, "10 minutes for a sophomore from the ER?",
   "Hi {first},\n\nI'm a finance sophomore at Iona University in New York (3.9 GPA) who works overnight shifts as an EMT in the Stamford Hospital ER. I'm recruiting for investment banking internships and would value 10 minutes of your perspective on what {firm} looks for in students from non-target schools.\n\nHappy to work around your schedule.\n\n{signature}",
   "ER / EMT story","EMT overnight shifts","10-minute call",D[MD]),
 "v-any-tech-cold": V("", T, "A sophomore's question about your work at {firm}",
   "Hi {first},\n\nI'm a finance sophomore at Iona University in New York (3.9 GPA) and an overnight EMT in the Stamford Hospital ER. I'm teaching myself DCFs and comps, and I'd love to hear how you got up to speed as an analyst at {firm}.\n\nWould you have 10 minutes in the next few weeks?\n\n{signature}",
   "ER / EMT story","EMT overnight shifts","10-minute call",D[T]),
 "v-lazard-au-gate": V("lazard-au", GK, "US sophomore: eligible for Lazard Australia?",
   "Hi {first},\n\nI'm a finance sophomore at Iona University in New York (3.9 GPA, graduating Dec 2028) and an EMT in the Stamford Hospital ER. Lazard's Australian advisory practice is one I'd love to learn from.\n\nBefore I apply, could you tell me whether students at US universities are eligible for your internship program, and whether any intake lines up with a US winter break?\n\n{signature}",
   "Eligibility check","3.9 GPA + SIE + BMC","Confirm eligibility",D[GK]),
 "v-adastra-gate": V("adastra", GK, "Attn: Melanie Trezise, internship question",
   "Hi {first},\n\nI'm a finance sophomore at Iona University in New York (3.9 GPA) and an overnight EMT in the Stamford Hospital ER. Ad Astra's healthcare and M&A work is exactly what I want to learn.\n\nDoes Ad Astra take interns, and are students at US universities eligible? If there's a better person to ask, I'd be grateful for the pointer.\n\n{signature}",
   "Eligibility check","EMT overnight shifts","Confirm eligibility",D[GK]),
 "v-recordpoint-gate": V("recordpoint", GK, "Next intake: open to a US sophomore?",
   "Hi {first},\n\nI read that Record Point interns work with senior bankers on live transactions, and I saw the Dec 2026–Jan 2027 intake has closed. I'm a finance sophomore at Iona University in New York (3.9 GPA).\n\nCould you tell me when the next intake opens, whether US students are eligible, and whether an analyst might have 10 minutes to talk about the work?\n\n{signature}",
   "Eligibility check","3.9 GPA + SIE + BMC","Confirm eligibility",D[GK]),
 "v-optilic-md": V("optilic", MD, "Quant research internship: US sophomore",
   "Hi {first},\n\nI'm a finance sophomore at Iona University in New York (3.9 GPA). I placed top 500 of 1,400+ in the Perplexity stock pitch competition and I'm building my quantitative skills.\n\nYour site says you supervise intern projects directly, so I wanted to ask: do you take remote or short-term interns from US universities, and what would you want to see from an applicant?\n\n{signature}",
   "Stock pitch & AI","Perplexity top 500 pitch","Confirm eligibility",D[MD]),
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "international.json")
json.dump({"firms":firms,"contacts":contacts,"variants":variants}, open(out,"w"), indent=1, ensure_ascii=False)
print(len(firms), len(contacts), len(variants))
