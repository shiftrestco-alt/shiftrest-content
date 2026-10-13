"""Iona alumni pulled from the LinkedIn alumni search (Oct 2026) -> iona_alumni.json.

Emails are guesses from each company's common address format. Verify before sending.
"""
import json, os, unicodedata, re

NOW = "2026-10-13T18:30:00.000Z"
T, TP, MD, GK, WI = "Technician", "Team Player", "MD / Partner", "Gatekeeper", "Warm intro"

firms = {
  "ey": dict(name="EY", tier="Iona network · Big Four", location="New York, NY", priority=13, emailPattern="{first}.{last}@ey.com", emailConfidence="Common format; verify",
             avatar="The Big Four Machine", avatarNotes="Huge Iona alumni base in assurance (FSO) and tax. Most of these contacts are audit/tax, so they're best for referrals into EY's Strategy & Transactions or FSO groups and for intros to friends in banking."),
  "pwc": dict(name="PwC", tier="Iona network · Big Four", location="New York, NY", priority=14, emailPattern="{first}.{last}@pwc.com", emailConfidence="Common format; verify",
             avatar="The Big Four Machine", avatarNotes="Tax and audit alumni. Useful for Deals/Transaction Services referrals and for general recruiting advice."),
  "deloitte": dict(name="Deloitte", tier="Iona network · Big Four", location="New York, NY", priority=15, emailPattern="{f}{last}@deloitte.com", emailConfidence="Common format; verify",
             avatar="The Big Four Machine", avatarNotes="Audit & assurance and tax alumni. Ask about Deloitte's financial advisory side and who they know in banking."),
  "citi": dict(name="Citi", tier="Iona network · Bank", location="New York, NY", priority=11, emailPattern="{first}.{last}@citi.com", emailConfidence="Common format; verify",
             avatar="The Global Bank", avatarNotes="Mostly branch banking alumni plus a Director at Citigroup. The Director is the one to ask for an intro into Citi's markets or banking analyst programs."),
  "bofa": dict(name="Bank of America", tier="Iona network · Bank", location="New York, NY", priority=12, emailPattern="{first}.{last}@bofa.com", emailConfidence="Common format; verify",
             avatar="The Global Bank", avatarNotes="An Analyst and an Operations Specialist. Ask the analyst how they recruited and which BofA summer programs take sophomores."),
  "pepsico": dict(name="PepsiCo", tier="Iona network · Corporate finance", location="Purchase, NY", priority=16, emailPattern="{first}.{last}@pepsico.com", emailConfidence="Common format; verify",
             avatar="The Corporate Giant", avatarNotes="HQ in Purchase, NY, close to Iona. Accounting, pension and data analysts. Good for corporate finance internships and as a backup path."),
  "nbcu": dict(name="NBCUniversal", tier="Iona network · Media", location="New York, NY / Stamford, CT", priority=17, emailPattern="{first}.{last}@nbcuni.com", emailConfidence="Common format; verify",
             avatar="The Media Giant", avatarNotes="NBC Sports is based in Stamford. Lower priority for finance recruiting; ask for finance-side intros."),
  "iona-net": dict(name="Iona network (employer unconfirmed)", tier="Iona network", location="Various", priority=18, emailPattern="", emailConfidence="Employer not listed; reach out on LinkedIn",
             avatar="The Inside Line", avatarNotes="Iona alumni whose current employer isn't shown in their LinkedIn headline. Message them on LinkedIn and ask for intros."),
}
for f in firms.values():
    f.update(status="Iona alumni", statusTone="neutral", keyDate="", keyDateLabel="No deadline. Alumni outreach for advice and referrals.", program="", eligibility="", createdAt=NOW)

# name, headline, firm, persona, rank (1 priority, 2 normal, 3 long shot), linkedin slug, mutuals, email override ("" = guess, None = no email), extra note
P = [
 ("Frankie DelGaudio","Universal Banker at Citi","citi",T,2,"frankie-delgaudio-744b11353","Jimmy +4 mutual","", "You can message directly on LinkedIn."),
 ("Albion Rugova","Relationship Banker at JPMorganChase","jpm",T,2,"albion-rugova-12042b221","Nabil +21 mutual","albion.rugova@jpmchase.com",""),
 ("Darryl Ohene-Karikari","Audit Associate at EY","ey",T,3,"darryl-ohene-karikari","Adriana +19 mutual","darryl.ohene-karikari@ey.com",""),
 ("Elizabeth Riccio","Production Assistant at NBCUniversal","nbcu",T,3,"elizabeth-riccio-2004er","Kyle +73 mutual","",""),
 ("Danae Obermuller","Brooklyn College M.S. '26; Iona BBA '25","iona-net",WI,3,"danae8655","Adriana +56 mutual",None,"Grad student."),
 ("Raul Peralta","Real Estate Tax Senior Associate at PwC","pwc",TP,3,"raul-peralta-mba-728a7120a","Jimmy +16 mutual","",""),
 ("Dante Romano","Tax Associate","iona-net",T,3,"dante-romano-b45137179","Arif +3 mutual",None,""),
 ("Luka Nastic","Financial Services Representative at Morgan Stanley","ms",T,2,"luka-nastic-a9a3b7226","Andrea +54 mutual","",""),
 ("Kristin Furlong","FSO Assurance Analyst at EY; CPA candidate","ey",T,3,"kristinfurlong","Jay +57 mutual","",""),
 ("Eduardo Tinoco","Universal Banker","iona-net",T,3,"eduardo-tinoco-b8b295221","Jay +46 mutual",None,"Bank not listed (Universal Banker is a Citi/Chase title)."),
 ("Michael Faughnan","FSO Assurance Analyst at EY","ey",T,3,"michael-faughnan-mba-7205611b5","Antonio +66 mutual","",""),
 ("Alessandra Gabriela Chavez","Alternative Investment Subscriptions Analyst at Morgan Stanley","ms",T,1,"alessandra-gabriela-chavez-563a042a7","Antonio +63 mutual","alessandra.chavez@morganstanley.com","May use a different name format; verify."),
 ("Landon Popovic","NBC Sports Programming Intern; Research Assistant at YES Network","nbcu",T,3,"landon-popovic-22ba7a25b","Andrew +29 mutual","","Intern; address may not exist yet."),
 ("Nigel Harris","Accountant at PepsiCo","pepsico",T,3,"nigel-harris-b71206188","Lucas +10 mutual","",""),
 ("Sean McLeer","BI and Reporting Analyst at PepsiCo","pepsico",T,3,"sean-mcleer-360919270","Kyle +30 mutual","",""),
 ("Martin Negron","Assistant Vice President, Global Investment Office at Morgan Stanley","ms",TP,1,"martin-negron-8b5a0bbb","Andrea +20 mutual","",""),
 ("Aidan Connolly","Assistant Vice President, Investor Services, Funds Product","iona-net",TP,2,"aidan-connolly123","Antonio +73 mutual",None,"Employer not in headline; check profile."),
 ("Dillon Gallo","Associate at PwC","pwc",T,3,"dillon-gallo-b22599316","Nabil +9 mutual","",""),
 ("Jorgjiano Proko","Universal Banker; Iona BBA Finance; SIE in progress","iona-net",T,2,"jorgjiano-proko","Adriana +48 mutual",None,"Recent Iona finance grad on the SIE path, like you. Bank not listed."),
 ("Lauren Killen","Senior at EY; Iona MBA '24; CPA","ey",TP,3,"lauren-killen-mba-cpa-69a3261bb","Andrew +16 mutual","",""),
 ("Fabricio Lopez","Analyst at Bank of America","bofa",T,1,"fabricio-a-lopez","Colin +7 mutual","",""),
 ("Soufiane Masrour","Investment Solutions Analyst at Morgan Stanley","ms",T,1,"soufm","Jimmy +31 mutual","","You can message directly on LinkedIn."),
 ("Gabriel Cinanni","Audit & Assurance Senior at Deloitte; CPA candidate","deloitte",TP,3,"gcinanni","Andrew +8 mutual","",""),
 ("Sherlon Boothe","Audit Associate at PwC; Iona BBA '24","pwc",T,3,"sherlonboothe","Jay +39 mutual","",""),
 ("Elizabeth Lancaster","Audit & Assurance Associate at Deloitte","deloitte",T,3,"elizabeth-lancaster","Matthew +10 mutual","",""),
 ("Daniella Santelli","Audit and Assurance Senior Assistant at Deloitte","deloitte",T,3,"daniella-santelli","Antonio +33 mutual","",""),
 ("Shimar Allen","Personal Banker at Citi","citi",T,3,"shimar-allen-mbm-3a524423a","Jonathan +7 mutual","",""),
 ("Christina DeCesare","Aspiring finance professional","iona-net",WI,3,"christinandecesare","Antonio +34 mutual",None,""),
 ("Max Mahon","CCaSS Professional at EY; former D1 athlete","ey",T,3,"maxmahon","Jimmy +42 mutual","",""),
 ("Wole Olusanya","IT Auditor at EY","ey",T,3,"wole-olusanya-2bb38422b","Adriana +26 mutual","",""),
 ("Lucas Haddad","FSO Assurance Analyst at EY","ey",T,3,"lucas-haddad-a73a491b2","Jay +54 mutual","",""),
 ("Ben Danialian","Senior Tax Consultant at EY","ey",TP,3,"ben-danialian-6003b81a0","Adriana +22 mutual","",""),
 ("Briana G.","Iona University graduate; bilingual","iona-net",WI,3,"briana-g-","Adriana +23 mutual",None,"Last name hidden on LinkedIn."),
 ("Jaline Alverio","Global Operations Specialist at Bank of America","bofa",T,2,"jaline-alverio-847b49278","Anabri +4 mutual","",""),
 ("Aidan Doherty","Associate Banker at JPMorganChase; Iona MBA (LaPenta)","jpm",T,2,"aidan-doherty-51b859239","Antonio +52 mutual","aidan.doherty@jpmchase.com",""),
 ("Alize Eduardo","Operations Associate at Morgan Stanley","ms",T,2,"alize-eduardo-3359781b9","Nabil +6 mutual","",""),
 ("Liliana Preldakaj","Tax Senior","iona-net",TP,3,"liliana-preldakaj-mba-61a571161","Arif +1 mutual",None,""),
 ("Luis Gonzalez Ortega","Tax Staff at EY; CPA candidate","ey",T,3,"luisgonzalezortega","Andrew +30 mutual","luis.gonzalezortega@ey.com","Two last names; if it bounces try luis.gonzalez@ey.com."),
 ("Alexis Kostron","FSO Assurance Senior at EY; CPA","ey",TP,3,"alexis-kostron-cpa-a39691189","Jimmy +11 mutual","",""),
 ("Anthony Marricco","Asset and Wealth Management Tax Manager at PwC","pwc",TP,3,"anthony-marricco-a694281bb","Rastko +6 mutual","",""),
 ("Jason Mercado","Analyst at Morgan Stanley, Community Development Finance","ms",T,1,"jason-f-mercado","Jay +45 mutual","","You can message directly on LinkedIn."),
 ("Orlando Hernandez","US Real Estate Tax Intern at EY","ey",T,2,"orlandohernandez05","Andrew +31 mutual","","Current intern: ask how he landed it and what the recruiting timeline looked like."),
 ("Jamie Sheeran","FSO Assurance Senior at EY","ey",TP,3,"jamie-sheeran-779679220","Micaela +18 mutual","",""),
 ("Shannon Shaikhar","Strategy and Execution at Morgan Stanley","ms",TP,2,"shannon-shaikhar-60353619b","Nabil +19 mutual","",""),
 ("Amanda Maiorana","Assurance Analyst at EY","ey",T,3,"amanda-maiorana","Adriana +21 mutual","",""),
 ("Thomas Danko","Senior Associate at PwC","pwc",TP,3,"thomas-danko-mba-a28b1a205","Antonio +38 mutual","",""),
 ("Robert Guarino","Morgan Stanley Private Wealth Management; MBA candidate at NYU Stern","ms",TP,1,"robert-guarino-50a997178","Jay +22 mutual","",""),
 ("Yanitza Acosta","R&D Associate Scientist","iona-net",WI,3,"yanitza-acosta","Andrew +17 mutual",None,"Not in finance; ask only for intros."),
 ("Elvis Predakaj","Associate at Morgan Stanley","ms",TP,1,"elvis-predakaj-b3a550176","Colin +2 mutual","",""),
 ("Kendell Thomas","Tax Consultant at Deloitte","deloitte",T,3,"kendellthomas","Adriana +24 mutual","",""),
 ("Michael Cupo","Registered Client Service Associate, Lenox Group at Morgan Stanley","ms",T,2,"michael-cupo-667b8b220","Michael +5 mutual","","LinkedIn shows Follow, not Connect: email first."),
 ("Chernoh Jalloh","Sports communications and media","iona-net",WI,3,"chernoh-jalloh","Jimmy +15 mutual",None,"Not in finance; ask only for intros."),
 ("Darnell Antoine","Pension Analyst at PepsiCo","pepsico",T,3,"darnell-antoine","Krystal +8 mutual","",""),
 ("Nicole Puleo","Tax Staff at EY; CPA candidate","ey",T,3,"nicole-puleo-mba-a91a3a15a","Gazment +7 mutual","",""),
 ("James Considine","Investment Banking Associate at J.P. Morgan","jpm",TP,1,"james-considine-384375b2","Colin +3 mutual","james.considine@jpmorgan.com","Iona alum in JPM investment banking. Your best contact on this list."),
 ("Grace Sparrow","IT Operations Senior Analyst at PepsiCo; former D1 athlete","pepsico",T,3,"grace-sparrow","Andrew +24 mutual","",""),
 ("Narciso Leder","Student at Iona University","iona-net",WI,3,"narciso-leder-2a8b09283","Lucas +4 mutual",None,"Current Iona student; peer, not a recruiting contact."),
 ("Joe DaSilva","VP, Product at Morgan Stanley","ms",TP,2,"joeadasilva","Gazment +7 mutual","","LinkedIn shows Follow, not Connect: email first."),
 ("Xavier D.","Audit & Assurance at Deloitte","deloitte",T,3,"xavier-d-a388811b4","Arif +5 mutual",None,"Last name hidden on LinkedIn."),
 ("Nicholas Bertolozzi","Service Associate at Morgan Stanley","ms",T,2,"nicholas-bertolozzi-461b76253","Ryan +45 mutual","",""),
 ("Michael Schools","Senior Data Analyst at PepsiCo","pepsico",T,3,"michael-schools-19332b170","Jack +3 mutual","",""),
 ("Jason Rossi","Real Estate Tax Associate at PwC","pwc",T,3,"jason-rossi-mba-b035a1180","Nabil +4 mutual","",""),
 ("Joel Urena","Vice President at Morgan Stanley","ms",TP,1,"joel-urena-53681698","Matthew +2 mutual","",""),
 ("Felix Alejandro Perez","Senior Analyst at PepsiCo","pepsico",T,3,"felix-alejandro-perez-018865247","Brian +1 mutual","felix.perez@pepsico.com",""),
 ("Bruce Ramirez","Director at Citigroup","citi",TP,1,"bruce-ramirez-11b0972b","Johnanthony +1 mutual","",""),
 ("Dea Shpati","Audit Senior","iona-net",TP,3,"dea-shpati-gk16","Colin +3 mutual",None,""),
 ("Brianna Buck","Audit & Assurance Senior at Deloitte","deloitte",TP,3,"briannabuck","Zulfukar +2 mutual","",""),
 ("Thaiane Silva","FSO Assurance Senior Auditor","iona-net",TP,3,"thaiane-silva-37b533105","Leo (1 mutual)",None,"\"FSO Assurance\" is an EY title; probably EY. Confirm on profile."),
 ("Drew Thornton","Manager, Ad Sales Finance, Sports","iona-net",TP,3,"drew-thornton-mba-73369215","Jennifer (1 mutual)",None,"Likely NBC Sports in Stamford; confirm on profile."),
 ("Joanna Fullman","Accounting Operations Associate Manager","iona-net",TP,3,"joanna-fullman-mba-3211b789","Zulfukar (1 mutual)",None,""),
 ("Gianni R.","Assistant Vice President, Private Client Banker at JPMorganChase","jpm",TP,2,"gianni-r-a939a223b","Brian (1 mutual)",None,"Last name hidden on LinkedIn."),
 ("Jaclyn Thompson","AI Product Owner","iona-net",WI,3,"jaclyn-thompson-mba-6b421213a","Jimmy +6 mutual",None,""),
 ("Toni-Ann Loccisano","Supervising Associate, Experience Management at EY","ey",TP,3,"toni-ann-loccisano-7a9854232","Mia (1 mutual)","toni-ann.loccisano@ey.com",""),
 ("Angela Virano","Head Universal Banker at Citi","citi",TP,3,"angelavirano","Ariana +1 mutual","",""),
 ("Sidney P.","Business Administration, Finance","iona-net",WI,3,"s-piekarski","",None,"Last name hidden (URL suggests Piekarski)."),
]

def norm(s): return re.sub(r"[^a-z]", "", unicodedata.normalize("NFD", s).encode("ascii","ignore").decode().lower())
PAT = {k: v["emailPattern"] for k, v in firms.items()}
PAT.update(jpm="{first}.{last}@jpmchase.com", ms="{first}.{last}@morganstanley.com")

contacts = {}
for i, (name, role, fid, persona, rank, slug, mutual, email, note) in enumerate(P, 1):
    if email == "":
        parts = name.split(); first, last = norm(parts[0]), norm(parts[-1])
        email = PAT[fid].replace("{first}", first).replace("{last}", last).replace("{f}", first[:1]) if PAT.get(fid) else ""
    notes = "Iona alum (LinkedIn alumni search). 2nd-degree · " + (mutual or "no mutuals listed") + "."
    if email: notes += " Email guessed from company format; verify before sending."
    if note: notes += " " + note
    contacts[f"ia{i:03d}"] = dict(firmId=fid, name=name, role=role, email=email or "", linkedin=f"https://www.linkedin.com/in/{slug}/",
        persona=persona, rank=rank, stage="todo", notes=notes, createdAt=NOW, sentAt="", lastTouchAt="", nextFollowUpAt="",
        followUps=0, variantId="", subject="", test={}, touches=[], source="iona-alumni")

variants = {"v-any-warm": dict(firmId="", persona=WI, desire="A fellow alum worth helping", angle="Iona connection", mechanism="Iona alumni ties",
    cta="Referral / intro", subject="Fellow Gael, quick favor?", hook="We're both Gaels and share a few connections.",
    body="Hi {first},\n\nWe're both Gaels and share a few connections, so I wanted to reach out. I'm an Iona finance sophomore (3.9 GPA) and an overnight EMT in the Stamford Hospital ER, recruiting for summer 2027 finance internships.\n\nWould you have 10 minutes to share how you got where you are, and is there anyone you think I should talk to?\n\n{signature}",
    label="GENERIC · Warm intro", active=True, source="starter", createdAt=NOW)}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iona_alumni.json")
json.dump({"firms": firms, "contacts": contacts, "variants": variants}, open(out, "w"), indent=1, ensure_ascii=False)
print(len(firms), len(contacts), len(variants), sum(1 for c in contacts.values() if c["email"]))
