# Outreach Desk

Cold-outreach tracker for summer internship recruiting (10 target firms from the Target Firms Outreach PDF).

- Live app: https://claude.ai/artifact/HteCWMbpZfKKs1GiUo382k
- `index.html`: the app (published as a claude.ai artifact with a shared database, Claude, and Gmail access)
- `build_seed.py` → `seed.json`: firms, contacts, 43 hook variants and settings pulled from the PDF (already loaded into the live app)

Data model (artifact database):
- `firms/{id}`: name, tier, status, keyDate, avatar, avatarNotes, emailPattern, priority
- `contacts/{id}`: firmId, name, role, email, linkedin, persona (avatar), stage, sentAt, nextFollowUpAt, variantId, test{persona,desire,angle,mechanism,cta}, touches[]
- `variants/{id}`: firmId ("" = any firm), persona, desire, angle, mechanism, cta, subject, body, active
- `settings/main`: dailyGoal, followUpDays, signature, follow-up templates
