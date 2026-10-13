"""Builds seed.json (firms, contacts, variants, settings) from the Target Firms Outreach PDF.

Run: python3 build_seed.py  -> writes seed.json next to this file.
"""
import json, os

NOW = "2026-10-13T12:00:00.000Z"

firms = [
  dict(id="ms", name="Morgan Stanley", tier="Required · Bulge bracket", location="New York, NY · Purchase, NY", status="Open, closes Oct 30", statusTone="urgent",
       keyDate="2026-10-30", keyDateLabel="Early Insights deadline, 11:55 p.m. ET", priority=1,
       program="2026 Early Insights (virtual sophomore program, Nov 2 & Nov 5). First stage of summer analyst recruiting. Also 2027 Sophomore Summer Analyst programs.",
       eligibility="Sophomores graduating Dec 2028 to Jun 2029. Dec 2028 is inside the window.",
       avatar="The Gentleman Operator",
       avatarNotes="\"First-class business in a first-class way.\" Values: clients first, do the right thing, lead with exceptional ideas, diversity and inclusion, give back. Interviewers want real research on the firm, a clear link from your background to a specific group, how MS differs from peers. Iona ties: Equity Collective partnership, an MS executive director on Iona's board, Iona students in wealth management.",
       emailPattern="{first}.{last}@morganstanley.com", emailConfidence="Clay-verified"),
  dict(id="leerink", name="Leerink Partners", tier="Best fit · Healthcare-only bank", location="New York · Boston · Charlotte · San Francisco", status="Open now", statusTone="open",
       keyDate="", keyDateLabel="Open since Sept 18; interviews Jan to Mar 2027. Last cycle filled early.", priority=2,
       program="2028 Summer Analyst Program, sophomore track. Ten weeks, paid, healthcare IB.",
       eligibility="Aimed at current sophomores. Requisition lists May 2029 grads, so ask whether Dec 2028 is accepted.",
       avatar="The Healthcare Specialist",
       avatarNotes="Only bank on the list that does nothing but healthcare. Entrepreneurial, fast-growing, hiring MDs from Jefferies, Barclays, Goldman. Interviewers want a credible, evidence-based 'why healthcare' and 'why Leerink'. Expect technicals plus brain teasers. Your EMT work is the most credible 'why healthcare' a sophomore can have.",
       emailPattern="{first}.{last}@leerink.com", emailConfidence="Clay-verified"),
  dict(id="syf", name="Synchrony", tier="Best fit · Stamford HQ · CareCredit", location="Stamford, CT", status="Open now", statusTone="open",
       keyDate="", keyDateLabel="Open since Aug 2026, rolling. Interviews Oct 2026 to Feb 2027.", priority=3,
       program="Summer 2027 Business Leadership Program (BLP) internships, ~$31/hr for finance, plus the BLP Sophomore Externship (4-day on-site).",
       eligibility="No class year stated. 3.0 GPA minimum; U.S. work authorization required.",
       avatar="The High-Trust Hometown Giant",
       avatarNotes="No. 1 Best Company to Work For (Fortune/GPTW 2026). CEO Brian Doubles: 'Our culture is built on trust.' Pushes AI hard. You live 10 minutes from HQ, and CareCredit (healthcare financing) connects to your ER work.",
       emailPattern="{first}.{last}@syf.com", emailConfidence="Clay-verified"),
  dict(id="fcb", name="First Citizens Bank: Healthcare Leveraged Finance", tier="Best fit · Healthcare credit", location="New York, NY", status="Class year not listed", statusTone="neutral",
       keyDate="", keyDateLabel="Rolling review, typically Aug to Oct. Apply now.", priority=4,
       program="2027 Summer Intern: Healthcare Leveraged Finance. Underwriting, models, credit memos, live deals. ~$20-31/hr plus housing stipend.",
       eligibility="No class year listed. 3.3+ GPA; finance/accounting/econ preferred.",
       avatar="The Disciplined Lender",
       avatarNotes="Downside-first credit culture from legacy CIT and SVB teams: cash flow, covenants, protecting capital. MD Mike Coiley: 'My role is to give them the tools and space to succeed.' Healthcare-specific credit seat where ER background is relevant on day one.",
       emailPattern="{first}.{last}@firstcitizens.com", emailConfidence="Clay-verified"),
  dict(id="graham", name="Graham Capital Management", tier="Local · Small firm (~250)", location="Rowayton, CT (15 min from Stamford)", status="Class year not listed", statusTone="neutral",
       keyDate="", keyDateLabel="Posting live now (Indeed, Stamford listing).", priority=5,
       program="2027 Graham Capital Summer Internship (CT / NYC). Macro hedge fund, ~$21B AUM.",
       eligibility="No class year listed. A past Hedge Fund Analyst intern did it after sophomore year.",
       avatar="The Quiet Macro Machine",
       avatarNotes="Data-driven discretionary and systematic macro. Founder Ken Tropin: 'building a team of the best people has remained key.' Tropin won II's 2026 Lifetime Achievement Award (June 2026). Jens Foehrenbach joined from Man Group as President & Co-CIO. Intense internship: commit your summer.",
       emailPattern="{f}{last}@grahamcapital.com", emailConfidence="~93% (Mailmo)"),
  dict(id="jpm", name="JPMorgan Chase", tier="Required · Bulge bracket", location="New York, NY", status="Opening soon", statusTone="soon",
       keyDate="2027-01-12", keyDateLabel="Deadline expected mid-Jan 2027 (apps open ~Nov 2026)", priority=6,
       program="2027 JPMorganChase Fellowship Program: paid 5-week sophomore fellowship. Tracks include CIB Investment Banking.",
       eligibility="Sophomores, all majors, 3.2+ GPA preferred. Should move to the Dec 2028 class (confirm when it posts).",
       avatar="The Fortress",
       avatarNotes="Big, disciplined, proud. Client service, operational excellence, integrity, winning culture. Favorite line: 'we have to execute to win.' Respects preparation, follow-through, ownership, numbers. Turned off by generic 'passion for finance' emails. J.P. Morgan Healthcare Conference every January in SF.",
       emailPattern="{first}.{last}@jpmorgan.com", emailConfidence="Pattern; try @jpmchase.com if it bounces"),
  dict(id="gs", name="Goldman Sachs", tier="Required · Bulge bracket", location="New York, NY", status="Opens ~Dec 2026", statusTone="soon",
       keyDate="2026-12-01", keyDateLabel="2028 Summer Analyst apps expected to open", priority=7,
       program="No Summer 2027 sophomore internship in the Americas. Real target: 2028 Summer Analyst program, which recruits current sophomores this winter.",
       eligibility="Class of 2029 window; Dec 2028 fits. 3.7+ GPA is the practical floor.",
       avatar="The Elite Meritocrat",
       avatarNotes="14 Business Principles, clients first. 'Commercial instinct' is the most prized trait. Acceptance under 1%. Head of HR Jacqueline Arthur: judgment and adaptability are harder to teach than technicals; non-traditional backgrounds are an asset. CEO Solomon values how people apply AI tools.",
       emailPattern="{first}.{last}@gs.com", emailConfidence="Clay-verified"),
  dict(id="clearview", name="Clearview Capital", tier="Local · Small PE (~30 inv. pros)", location="Stamford, CT (1010 Washington Blvd)", status="No posting: ask directly", statusTone="neutral",
       keyDate="", keyDateLabel="No deadline. Small PE shops hire interns when someone asks at the right moment.", priority=8,
       program="Lower-middle-market PE, founded 1999. Healthcare services is a target sector (Advantage Behavioral Health in portfolio).",
       eligibility="No posting. Off-cycle ask: request a summer or part-time analyst role directly.",
       avatar="The Hometown Dealmaker",
       avatarNotes="Relationships first, transparency and authenticity. Lean team, so interns do real work: buy-and-build models, add-on screening, diligence. Recent deals: Capitol Services acquired Wolz (Aug 2026), new LJM Group platform (Jul 2026), UpSwell Marketing exit (Apr 2026). Respects local, humble people who've read their deals.",
       emailPattern="{f}{last}@clearviewcap.com", emailConfidence="~86% (Prospeo), confirmed on site"),
  dict(id="gamco", name="GAMCO Investors (Gabelli Funds)", tier="Local · Small firm", location="Rye, NY · Greenwich, CT office", status="Class year not listed", statusTone="neutral",
       keyDate="", keyDateLabel="No published deadline. Reach out before summer seats fill.", priority=9,
       program="Summer internship (equity research / summer analyst), runs every year.",
       eligibility="No class year published. Apply through gabelli.com/careers or Handshake.",
       avatar="The Value Patriarch",
       avatarNotes="Founder-led by Mario Gabelli (Bronx native, Fordham and Columbia MBA). 'Private Market Value with a Catalyst' method. Long-term, frugal, allergic to hype. Big Iona connection: endowed professorship at LaPenta, Gabelli Center for Teaching & Learning, 'hired and worked with many Iona graduates.' Lead with Iona tie and real stock work.",
       emailPattern="{f}{last}@gabelli.com", emailConfidence="~80% (Prospeo)"),
  dict(id="moneco", name="Moneco Advisors", tier="Local · Small firm (~65)", location="Fairfield, CT (25 min from Stamford)", status="Sophomore-eligible", statusTone="open",
       keyDate="", keyDateLabel="Posting live on Greenhouse; no deadline listed.", priority=10,
       program="Wealth Management Internship at an independent fiduciary (~$1.9B AUM): Morningstar reports, Investment Committee research, eMoney/Orion case study, CRM work.",
       eligibility="2+ years coursework by summer (sophomores qualify). 3.4+ GPA; writing samples required. Academic credit (unpaid).",
       avatar="The Fiduciary Neighbor",
       avatarNotes="Values: commitment, collaboration, humility, strategic thinking, community involvement. Mentorship, shadowing, team learning. Respects humble, coachable, client-minded people. SIE prep is directly relevant.",
       emailPattern="{f}{last}@monecoadvisors.com", emailConfidence="Low; fallback {first}@monecoadvisors.com"),
]

T, TP, MD, GK, WI = "Technician", "Team Player", "MD / Partner", "Gatekeeper", "Warm intro"

contacts = [
  ("jpm", "Jeremy Meilman", "Global Head of Healthcare Investment Banking", "jeremy.meilman@jpmorgan.com", MD, ""),
  ("jpm", "Sri Kosaraju", "Global Chair of Investment Banking, Healthcare (San Francisco)", "sri.kosaraju@jpmorgan.com", MD, "\"Sri\" may be short for a longer first name; verify."),
  ("ms", "Monique Jean", "Executive Director, Wealth Management Advisory Legal; Iona Board of Trustees", "monique.jean@morganstanley.com", MD, "Iona alum ('00)."),
  ("ms", "Carlos Muñoz", "Executive Director, Head of Asset Manager DEI Engagement; leads The Equity Collective", "carlos.munoz@morganstanley.com", TP, "Iona alum ('10 MBA)."),
  ("gs", "Jacqueline Arthur", "Global Head of Human Capital Management", "jacqueline.arthur@gs.com", GK, "Quoted in Fortune, June 2026."),
  ("gs", "Paulo Silva", "Iona alum, former Goldman VP; now CFO of Accion", "", WI, "Not at GS. LinkedIn only. Ask for a warm intro to his GS network."),
  ("gamco", "Mario J. Gabelli", "Chairman & CEO", "mgabelli@gabelli.com", MD, ""),
  ("gamco", "Kevin V. Dreyer", "Co-CIO; PM of Gabelli Healthcare & WellnessRx Trust (GRX)", "kdreyer@gabelli.com", T, ""),
  ("graham", "Kenneth G. Tropin", "Founder & Chairman", "ktropin@grahamcapital.com", MD, ""),
  ("graham", "Jens Foehrenbach", "President & Co-Chief Investment Officer", "jfoehrenbach@grahamcapital.com", MD, ""),
  ("clearview", "Matthew Blevins", "Managing Partner", "mblevins@clearviewcap.com", MD, ""),
  ("clearview", "Sam Lawler", "Associate", "slawler@clearviewcap.com", T, ""),
  ("clearview", "Erin Brunner", "Administrative Assistant", "ebrunner@clearviewcap.com", GK, "Address listed on their site."),
  ("moneco", "Charlie Rocco", "Managing Partner & CEO", "crocco@monecoadvisors.com", MD, "Verify before sending."),
  ("moneco", "Taryn DeMar", "Director of People", "tdemar@monecoadvisors.com", GK, "Verify before sending."),
  ("moneco", "Thomas Yao", "Director of Investments", "tyao@monecoadvisors.com", T, "Verify before sending."),
  ("leerink", "Barry Blake", "Global Co-Head of Healthcare Investment Banking", "barry.blake@leerink.com", MD, ""),
  ("leerink", "Philip Boyd", "Senior Managing Director, Healthcare Services & Technology (NYC)", "philip.boyd@leerink.com", MD, ""),
  ("fcb", "Mike Coiley", "Managing Director, Healthcare Finance (leads Healthcare ABL & Real Estate)", "mike.coiley@firstcitizens.com", MD, "If it bounces try michael.coiley@firstcitizens.com"),
  ("fcb", "Steve Reedy", "Managing Director, Head of Medical Office Banking", "steve.reedy@firstcitizens.com", MD, "If it bounces try steven.reedy@firstcitizens.com"),
  ("syf", "Alberto Casellas", "EVP & CEO, Health & Wellness (runs CareCredit)", "alberto.casellas@syf.com", MD, "Goes by \"Beto\". Fluent in Spanish."),
  ("syf", "Shannon Tenney", "University Recruiting Manager: Externship, Internship, BLP", "shannon.tenney@syf.com", GK, "Title as of 2021; confirm on LinkedIn."),
]

DES = {T: "Proof you can do the work", TP: "Someone reliable they'd staff", MD: "Relevance and a reason to care", GK: "Eligibility, clarity, zero extra work", WI: "A fellow alum worth helping"}

# firm, persona, subject, text, angle, mechanism, cta, closer
V = [
 ("jpm", T, "Night-shift EMT, day-shift DCFs", "I work 12-hour overnight shifts in the Stamford Hospital ER, then build DCFs and comps. Could I get 10 minutes on how you pressure-test a model as a first-year?", "ER / EMT story", "EMT overnight shifts", "Critique my work", ""),
 ("jpm", TP, "“Execute to win”: I learned it at 4 a.m.", "Your principles say “we have to execute to win.” I learned what that means running EKGs and CPR on overnight ER shifts, and I want to bring it to a deal team.", "Their own words", "EMT overnight shifts", "10-minute call", "Would you have 10 minutes in the next few weeks to tell me what separates great analysts on your team?"),
 ("jpm", MD, "From the ER floor to JPM Healthcare", "Every January at the J.P. Morgan Healthcare Conference you see the industry from the top. I see it from the bottom, as an EMT in the Stamford Hospital ED. I'm a 3.9 finance sophomore at Iona and would value 10 minutes of your view on healthcare banking.", "ER / EMT story", "EMT overnight shifts", "10-minute call", ""),
 ("jpm", GK, "Fellowship ’27: Iona, 3.9, EMT-B", "I'm applying to the 2027 Fellowship (IB track) the day it opens and wanted to put a face to the application: 3.9 finance GPA, BMC-certified, SIE in November, and 12-hour ER shifts every weekend.", "Eligibility check", "3.9 GPA + SIE + BMC", "Flag my application", "Is there anything you'd recommend I do before applications open?"),
 ("ms", T, "I pitched Ivanhoe to 1,400 people. Tear it apart?", "I placed top 500 of 1,400+ in the Perplexity stock pitch with a thesis on Ivanhoe Mines and U.S. rare-earth supply. I'd love to hear how an MS analyst would have pulled it apart.", "Stock pitch & AI", "Perplexity top 500 pitch", "Critique my work", "Would you have 10 minutes in the next couple of weeks?"),
 ("ms", TP, "A Gael 20 minutes from Purchase", "Iona and Morgan Stanley already work together through the Equity Collective. I'm a 3.9 finance sophomore from Stamford and would love 10 minutes on what makes someone great on your team.", "Iona connection", "Iona alumni ties", "10-minute call", ""),
 ("ms", MD, "“Do the right thing”: an EMT's version", "In the ER, “do the right thing” is the job, not a slogan. I've carried that into finance (3.9 GPA, BMC, SIE in November) and I'm applying to Early Insights before the Oct 30 deadline.", "Their own words", "EMT overnight shifts", "10-minute call", "Would you have 10 minutes to share what you'd want a sophomore to know going in?"),
 ("ms", GK, "Early Insights: Dec ’28 grad, inside the window", "I'm an Iona sophomore graduating December 2028, inside the Early Insights window, and I'll submit before Oct 30. Is there anything you look for in a non-target applicant that the resume screen might miss?", "Eligibility check", "3.9 GPA + SIE + BMC", "Confirm eligibility", ""),
 ("gs", T, "I used AI to build a stock pitch. Here's what broke.", "In the Perplexity stock pitch competition I used AI to build visuals and interpret data on Ivanhoe Mines, and learned exactly where it fails. Curious how your team decides what to trust the model on.", "Stock pitch & AI", "Perplexity top 500 pitch", "Critique my work", "Would you have 10 minutes in the next few weeks?"),
 ("gs", TP, "Triage is prioritization with a pulse", "On an ER shift you rank five urgent things in five seconds and hand off cleanly. I'm a finance sophomore at Iona trying to learn how that translates to a deal team.", "ER / EMT story", "EMT overnight shifts", "10-minute call", "Could I get 10 minutes of your perspective?"),
 ("gs", MD, "Commercial instinct from a non-target", "Your interviewers prize commercial instinct. Mine came from defending a rare-earths thesis against 1,400+ competitors and building a platform that placed 8th of 35+. I'd value 10 minutes on what separates the 1%.", "Their own words", "Perplexity top 500 pitch", "10-minute call", ""),
 ("gs", GK, "“Judgment can't be taught.” I agree.", "You told Fortune that judgment and adaptability are harder to teach than technicals. I've been building both on overnight shifts as an EMT in the Stamford Hospital ED while holding a 3.9 in finance.", "Their own words", "EMT overnight shifts", "Flag my application", "I'm planning to apply to the 2028 Summer Analyst program when it opens. Is there anything you'd want a non-target sophomore to know first?"),
 ("gamco", T, "PMV check on Vistra (VST)?", "I built an investment thesis on Vistra for a research application. I'd love 10 minutes to hear how a Gabelli analyst would frame its private market value and catalyst.", "Stock pitch & AI", "Investment thesis / writing sample", "Critique my work", ""),
 ("gamco", TP, "Iona to Rye, like the ones before me", "Mr. Gabelli has hired many Iona graduates. I'm the next one trying to earn it: 3.9 finance GPA, BMC-certified, SIE in November.", "Iona connection", "3.9 GPA + SIE + BMC", "10-minute call", "Would you have 10 minutes to tell me what made those Iona hires work out?"),
 ("gamco", MD, "Your Iona professorship, at work", "I'm a finance sophomore at Iona's LaPenta School, home of your endowed professorship. I'd be grateful for the chance to learn PMV research from your team this summer.", "Iona connection", "Iona alumni ties", "Any open role", ""),
 ("gamco", GK, "Summer 2027 intern: 20 minutes from Rye", "I'm a Stamford-based Iona finance sophomore (3.9 GPA) applying for your summer internship. I'm local and used to 12-hour shifts.", "Local / proximity", "Local (Stamford)", "Flag my application", "Could you make sure my application reaches the right person, or tell me who that is?"),
 ("graham", T, "Rare earths, data centers, and a macro trade", "I built a thesis on how AI data-center demand squeezes U.S. rare-earth supply (top 500 of 1,400+ in Perplexity's pitch competition). Curious how your macro team would trade that theme.", "Stock pitch & AI", "Perplexity top 500 pitch", "Critique my work", "Would you have 10 minutes to tell me where my thinking breaks?"),
 ("graham", TP, "15 minutes from Rowayton", "I live in Stamford, study finance at Iona (3.9) and work overnight ER shifts. I'm applying to Graham's 2027 summer internship and would value a quick read on what makes interns stand out.", "Local / proximity", "EMT overnight shifts", "10-minute call", ""),
 ("graham", MD, "Congrats on the Lifetime Achievement Award", "Congratulations on Institutional Investor's 2026 Lifetime Achievement Award. Graham started in Connecticut, and I'm a Stamford finance student hoping to learn macro where it's done best.", "Firm news / deal", "Local (Stamford)", "10-minute call", "Would you or someone on your team have 10 minutes for a sophomore?"),
 ("graham", GK, "2027 Summer Internship: local, sophomore, 3.9", "I'm applying to the 2027 Graham Capital Summer Internship: Iona finance, 3.9 GPA, BMC, SIE in November, and I live 15 minutes from Rowayton.", "Eligibility check", "3.9 GPA + SIE + BMC", "Confirm eligibility", "Do you consider sophomores for this program, and is there anything I should add to my application?"),
 ("clearview", T, "Your LJM deal, through a sophomore's model", "I read about your July LJM Group platform investment and tried to back into the add-on math. Would you be open to 10 minutes on how an associate here builds a buy-and-build model?", "Firm news / deal", "Investment thesis / writing sample", "Critique my work", ""),
 ("clearview", TP, "A Stamford EMT who wants to grind your diligence", "I work overnight shifts in the Stamford Hospital ED, 10 minutes from your office, and study finance at Iona (3.9). I'd take any part-time or summer work that helps your deal team.", "Local / proximity", "EMT overnight shifts", "Any open role", ""),
 ("clearview", MD, "Behavioral health, seen from the ER", "I see behavioral health patients every week as an EMT in the Stamford Hospital ED, and noticed Advantage Behavioral Health in your portfolio. I'd value 10 minutes on investing in healthcare services.", "ER / EMT story", "EMT overnight shifts", "10-minute call", ""),
 ("clearview", GK, "Local student: who should I talk to?", "I'm a Stamford-based Iona finance sophomore hoping to intern with Clearview this summer. Could you point me to the right person on the team?", "Local / proximity", "Local (Stamford)", "Point me to the right person", ""),
 ("moneco", T, "Morningstar reports + an SIE in November", "Your internship includes quarterly Morningstar reports for the Investment Committee. I'm sitting the SIE in November and want to learn portfolio research the way your team does it.", "Firm news / deal", "3.9 GPA + SIE + BMC", "10-minute call", "Would you have 10 minutes to tell me what a strong intern report looks like?"),
 ("moneco", TP, "Humility is a job requirement in the ER", "Your values list humility and collaboration. As an EMT I take direction from nurses and physicians every shift, and I'd bring that mindset to your planning team.", "Their own words", "EMT overnight shifts", "10-minute call", "Could I get 10 minutes to learn how your interns contribute?"),
 ("moneco", MD, "A local finance student for Moneco", "I'm a Stamford finance student at Iona (3.9) who wants to learn wealth management at an independent fiduciary, not a wirehouse. Moneco is the one I'd choose.", "Local / proximity", "3.9 GPA + SIE + BMC", "10-minute call", "Would you be open to a short call about the Wealth Management Internship?"),
 ("moneco", GK, "WM internship: writing sample attached", "I'm applying for your Wealth Management Internship and attached a one-page investment thesis as a writing sample. I'll have two years of coursework done by summer and a 3.9 GPA.", "Eligibility check", "Investment thesis / writing sample", "Flag my application", "Is there anything else you need from me?"),
 ("leerink", T, "How many of your analysts have run an EKG?", "I'm a 3.9 finance sophomore at Iona who runs EKGs and draws blood on overnight ER shifts. I'd love to hear how you got up to speed on the clinical side of healthcare deals.", "ER / EMT story", "EMT overnight shifts", "10-minute call", "Would you have 10 minutes in the next few weeks?"),
 ("leerink", TP, "“Why healthcare?” I work in it.", "Every banker asks “why healthcare?” My answer is 12-hour shifts in the Stamford Hospital ED, and I'm applying to Leerink's 2028 sophomore track before interviews start.", "ER / EMT story", "EMT overnight shifts", "10-minute call", "Could I get 10 minutes on what makes a sophomore stand out at Leerink?"),
 ("leerink", MD, "Healthcare services, from the provider floor", "Your team advises the kinds of healthcare providers I work inside every week as an EMT. I'd value 10 minutes on what the ER floor gets wrong about the economics.", "ER / EMT story", "EMT overnight shifts", "10-minute call", ""),
 ("leerink", GK, "2028 SA sophomore track: is a Dec ’28 grad eligible?", "I'm applying to the 2028 Summer Analyst sophomore track and graduate December 2028 (accelerated). Can you confirm that's in the window? Healthcare is the only banking I want to do.", "Eligibility check", "3.9 GPA + SIE + BMC", "Confirm eligibility", ""),
 ("fcb", T, "A healthcare borrower's worst case, from an EMT", "I've been teaching myself cash-flow analysis (DCF, comps, WACC) and want to understand how your team underwrites a healthcare borrower's downside. Could I get 10 minutes?", "ER / EMT story", "EMT overnight shifts", "10-minute call", ""),
 ("fcb", TP, "Downside protection is my day job", "In the ER we plan for the worst case first. I think that's why leveraged finance appeals to me, and why I'm applying to your 2027 Healthcare Leveraged Finance internship.", "ER / EMT story", "EMT overnight shifts", "10-minute call", "Would you have 10 minutes to tell me what your best interns did differently?"),
 ("fcb", MD, "“The tools and space to succeed”", "You said your role is to give the next generation “the tools and space to succeed.” I'm a 3.9 finance sophomore and Stamford Hospital EMT hoping to earn that in your healthcare group.", "Their own words", "EMT overnight shifts", "10-minute call", "Could I have 10 minutes of your time in the next few weeks?"),
 ("fcb", GK, "HLF intern: healthcare background, NYC-ready", "I'm applying to the 2027 Healthcare Leveraged Finance internship. The posting lists no class year, so I wanted to flag a sophomore with real healthcare experience: EMT-B in the Stamford Hospital ED.", "Eligibility check", "EMT overnight shifts", "Confirm eligibility", "Are sophomores considered for this role?"),
 ("syf", T, "AI + finance, from a Stamford student", "Nearly all of Synchrony's senior leaders use AI tools. I used Perplexity AI to build and test a stock pitch that placed top 500 of 1,400+, and I'd love to see how your finance team uses it.", "Stock pitch & AI", "Perplexity top 500 pitch", "10-minute call", "Would you have 10 minutes in the next few weeks?"),
 ("syf", TP, "Trust is earned at 4 a.m.", "Your culture is built on trust. Mine was built handing off patients to physicians and EMS at 4 a.m. I'm a Stamford finance student applying to the 2027 BLP internship.", "Their own words", "EMT overnight shifts", "10-minute call", "Could I get 10 minutes on what makes a BLP intern stand out?"),
 ("syf", MD, "Hablo español con mis pacientes", "I use Spanish with patients every shift in the Stamford Hospital ED and see firsthand what healthcare costs families. I'd value 10 minutes on how CareCredit thinks about that problem.", "ER / EMT story", "Spanish with patients", "10-minute call", ""),
 ("syf", GK, "BLP 2027: I live 10 minutes from HQ", "I'm a 3.9 Iona finance sophomore living 10 minutes from your Stamford HQ, applying to the 2027 BLP internship and the Sophomore Externship. Happy to come in anytime.", "Local / proximity", "Local (Stamford)", "Flag my application", "Is there anything that would strengthen my application?"),
 ("gs", WI, "A Gael following your path to Goldman", "I'm an Iona finance sophomore (3.9 GPA, Dec 2028) and your path from Iona to Goldman is the one I'm trying to follow. I'm preparing for the 2028 Summer Analyst program this winter.", "Iona connection", "Iona alumni ties", "Referral / intro", "Would you have 10 minutes to share what mattered most, and is there anyone in your Goldman network who might be open to talking with a sophomore?"),
 ("", T, "Iona sophomore: how did you get to {firm}?", "I found you through the Iona alumni network. I'm a 3.9 finance sophomore and an overnight EMT in the Stamford Hospital ER, and I'm recruiting for {firm}'s summer program.", "Iona connection", "EMT overnight shifts", "10-minute call", "Would you have 10 minutes in the next couple of weeks to share how you got there?"),
 ("", TP, "10 minutes for a Stamford sophomore?", "I'm a finance sophomore at Iona (3.9) who works 12-hour overnight shifts in the Stamford Hospital ER. I'm recruiting for {firm}'s summer program and trying to learn what your team actually looks for.", "ER / EMT story", "EMT overnight shifts", "10-minute call", "Could I get 10 minutes of your time in the next couple of weeks?"),
]

def body(text, closer):
    parts = ["Hi {first},", text]
    if closer: parts.append(closer)
    parts.append("{signature}")
    return "\n\n".join(parts)

seed = {"firms": {}, "contacts": {}, "variants": {}, "settings": {}}
for f in firms:
    fid = f.pop("id")
    f["createdAt"] = NOW
    seed["firms"][fid] = f
for i, (fid, name, role, email, persona, notes) in enumerate(contacts, 1):
    seed["contacts"][f"c{i:03d}"] = dict(firmId=fid, name=name, role=role, email=email, linkedin="", persona=persona,
        stage="todo", notes=notes, createdAt=NOW, sentAt="", lastTouchAt="", nextFollowUpAt="", followUps=0,
        variantId="", subject="", test={}, touches=[], source="PDF")
for i, (fid, persona, subj, text, angle, mech, cta, closer) in enumerate(V, 1):
    tag = {T: "tech", TP: "team", MD: "md", GK: "gate", WI: "warm"}[persona]
    vid = f"v-{fid or 'any'}-{tag}"
    seed["variants"][vid] = dict(firmId=fid, persona=persona, desire=DES[persona], angle=angle, mechanism=mech, cta=cta,
        hook=text.split(". ")[0].rstrip(".") + ".", subject=subj, body=body(text, closer), label=f"{(fid or 'Generic').upper()} · {persona} · PDF",
        active=True, source="PDF" if fid else "starter", createdAt=NOW)
seed["settings"]["main"] = dict(dailyGoal=50, followUpDays=[3, 7],
    signature="Best,\nBoden Grimes\nIona University, BBA Finance (Dec 2028)\nStamford, CT",
    fu1Subject="Re: {subject}",
    fu1Body="Hi {first},\n\nBumping this in case it got buried. I know your schedule is packed, so even 10 minutes in the next couple of weeks would mean a lot.\n\n{signature}",
    fu2Subject="Re: {subject}",
    fu2Body="Hi {first},\n\nLast note from me. If now isn't a good time, is there someone on your team who might be open to a quick chat with a sophomore?\n\nThanks either way,\n{signature}")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed.json")
with open(out, "w") as fh:
    json.dump(seed, fh, indent=1, ensure_ascii=False)
print({k: len(v) for k, v in seed.items()})
