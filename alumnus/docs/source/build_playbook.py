"""Builds playbook.html (then printed to PDF by print_pdf.js).

The asset IDs below must match the labels the theme shows in empty media slots
(snippets/placeholder.liquid calls in each section). Run:
    python3 build_playbook.py && node print_pdf.js
"""
import html
import pathlib

HERE = pathlib.Path(__file__).parent
OUT = HERE / 'playbook.html'

E = html.escape

ACCENT = '#C2410C'

DEVICE = (
    "the Alumnus AI voice recorder: an ultra-thin, credit-card-sized rectangle about 3 mm thick with softly "
    "rounded corners; satin graphite-blue anodized aluminum with about ten fine vertical grooves running from top "
    "to bottom; a glossy black glass strip across the top holding a small pill-shaped slide switch on the left, a "
    "tiny white sound-wave light in the middle and a small round silver dot on the right; flat magnetic back; no "
    "logos or text on the device"
)

STYLE = (
    "bright premium consumer-tech photography, clean white and soft cool-grey tones, large soft daylight, gentle "
    "natural shadows, realistic textures, shallow depth of field, full-frame camera look, neutral-cool color grade "
    "with clean whites, small warm orange accents only in props"
)

NEGATIVE = (
    "text, letters, numbers, logos, watermarks, brand names, user interface on the device, extra buttons, extra "
    "lights, duplicate devices, warped or bent phone, bent device, extra fingers, distorted hands, plastic skin, "
    "oversaturated colors, harsh flash, cluttered background, cartoon look"
)

CAST = (
    "diverse 19 to 30 year old students and young professionals, natural and candid, not posing for the camera, "
    "casual neutral clothing with no logos"
)

# --------------------------------------------------------------------------------------------
# Asset list. where = theme editor path (or Shopify admin path). kind = image | video | real
# --------------------------------------------------------------------------------------------
ASSETS = [
    dict(id='IMG-01', name='Hero product shot (desktop)', kind='image', priority='P1',
         where='Theme editor › Home page › Hero › Image', ratio='16:10', size='2400 × 1500 px', file='alumnus-img-01-hero.jpg',
         model='Nano Banana Pro with 2–3 reference photos of your real device',
         prompt=("Premium website hero product photo, 16:10. A modern smartphone stands upright at a slight three-quarter angle on a "
                 "seamless very light cool-grey surface, back of the phone facing the camera, with [DEVICE] snapped flat onto the "
                 "center of the phone's back. Keep the device identical to the reference photos. Large soft window light from the "
                 "left, smooth background gradient from white to pale blue-grey, delicate contact shadow, crisp detail on the grooves "
                 "and the black top strip. Subject centered with wide empty space left and right. Minimal, calm, Apple-style product "
                 "page. No text, no logos."),
         checks=['Grooves straight and evenly spaced; top strip layout matches your unit', 'No phone-brand logo visible',
                 'Nothing important near the left/right edges (the theme crops to fit)']),
    dict(id='IMG-01M', name='Hero product shot (mobile crop)', kind='image', priority='P1',
         where='Theme editor › Home page › Hero › Mobile image', ratio='4:5', size='1200 × 1500 px', file='alumnus-img-01m-hero-mobile.jpg',
         model='Nano Banana Pro (edit IMG-01, or regenerate with the same references)',
         prompt=("Same scene as IMG-01, reframed vertically at 4:5. The phone and [DEVICE] fill the middle of the frame with extra "
                 "clean space above and below. Same light, same background, same shadow. No text."),
         checks=['Matches IMG-01 colors so desktop and mobile feel like one shoot']),
    dict(id='IMG-02', name='Brand film poster frame', kind='image', priority='P1',
         where='Theme editor › Home page › Intro film › Poster image', ratio='16:9', size='1920 × 1080 px', file='alumnus-img-02-film-poster.jpg',
         model='Soul 2.0 for the scene, then Nano Banana Pro edit with your device references to fix the device',
         prompt=("Cinematic 16:9 still. A university student in a sunlit lecture hall, seated in the middle rows, looking up at the "
                 "out-of-focus lecturer with a relaxed, attentive expression; no laptop open. On the desk in front of them a smartphone "
                 "lies face-down with [DEVICE] attached to its back, the tiny white sound-wave light glowing. Warm morning light through "
                 "tall windows, shallow depth of field focused on the device and the student's hand, soft film grain. No text."),
         checks=['Also works as the first frame of shot 2 in VID-01']),
    dict(id='IMG-03', name='Wide statement image', kind='image', priority='P2',
         where='Theme editor › Home page › Image banner › Image (+ Mobile image = IMG-03M)', ratio='21:9 (mobile 4:5)', size='2400 × 1030 px (mobile 1200 × 1500)', file='alumnus-img-03-wide.jpg',
         model='Soul 2.0 or Nano Banana Pro with device references',
         prompt=("Wide cinematic 21:9 photo. A clean light-wood desk by a large window overlooking a leafy university campus in soft "
                 "morning light. On the desk: an open notebook, a cup of coffee, a pen with an orange cap, and a smartphone lying "
                 "face-down with [DEVICE] on its back, placed on the right third. Lots of calm negative space, airy, muted natural "
                 "palette, shallow depth of field. No people, no text. Mobile version (IMG-03M): same scene, vertical 4:5, device in "
                 "the lower middle."),
         checks=['Keep the device large enough to read at phone size in the 4:5 version']),
    dict(id='IMG-04', name='Real-life card: In class', kind='image', priority='P2',
         where='Theme editor › Home page › Lifestyle gallery › Photo card 1', ratio='4:5', size='1200 × 1500 px', file='alumnus-img-04-in-class.jpg',
         model='Soul 2.0 (people) → Nano Banana Pro edit to insert the exact device',
         prompt=("Vertical 4:5 lifestyle photo. A student in a bright lecture hall seen from the side at desk level, relaxed and "
                 "attentive, listening instead of typing. A smartphone with [DEVICE] on its back lies on the desk in the foreground, "
                 "slightly in focus. Soft daylight, candid, shallow depth of field. [CAST]. No logos, no text."),
         checks=['Device clearly visible in the foreground']),
    dict(id='IMG-05', name='Real-life card: At work', kind='image', priority='P2',
         where='Theme editor › Home page › Lifestyle gallery › Photo card 2', ratio='4:5', size='1200 × 1500 px', file='alumnus-img-05-at-work.jpg',
         model='Soul 2.0 → Nano Banana Pro edit',
         prompt=("Vertical 4:5 lifestyle photo. A young professional in a modern glass meeting room, mid-conversation with colleagues "
                 "who are softly out of focus. A smartphone with [DEVICE] on its back lies on the table in the foreground. Bright, "
                 "natural light, candid moment. [CAST]. No logos, no text."),
         checks=['No laptop or wall screens showing readable text']),
    dict(id='IMG-06', name='Real-life card: On a call', kind='image', priority='P2',
         where='Theme editor › Home page › Lifestyle gallery › Photo card 3', ratio='4:5', size='1200 × 1500 px', file='alumnus-img-06-on-a-call.jpg',
         model='Soul 2.0 → Nano Banana Pro edit',
         prompt=("Vertical 4:5 lifestyle photo. A person on a phone call in a bright café, phone held to their ear with [DEVICE] "
                 "clearly attached to the back of the phone and facing the camera. Natural smile, soft window light, shallow depth of "
                 "field. [CAST]. No logos, no text."),
         checks=['The device faces the camera (the back of the phone is toward the lens)']),
    dict(id='IMG-07', name='Real-life card: On the go', kind='image', priority='P2',
         where='Theme editor › Home page › Lifestyle gallery › Photo card 4', ratio='4:5', size='1200 × 1500 px', file='alumnus-img-07-on-the-go.jpg',
         model='Soul 2.0 → Nano Banana Pro edit',
         prompt=("Vertical 4:5 lifestyle photo. A student walking on a tree-lined campus path at golden hour, holding a phone near "
                 "their chin and talking an idea through, [DEVICE] on the back of the phone. Warm low sun, gentle motion, candid. "
                 "[CAST]. No logos, no text."),
         checks=['Feels like the same world as IMG-04 to IMG-06 (same grade)']),
    dict(id='IMG-08', name='Macro hero of the device', kind='image', priority='P1',
         where='Theme editor › Home page › Feature grid › Large image', ratio='16:9', size='2400 × 1350 px', file='alumnus-img-08-macro.jpg',
         model='Nano Banana Pro with device references',
         prompt=("Studio macro product photo, 16:9. [DEVICE] floats at a slight angle above a seamless pale cool-grey background, "
                 "front facing the camera. Soft large key light from the upper left plus a thin rim light that traces the vertical "
                 "grooves and the edge, showing how thin it is. Extremely sharp detail, soft shadow below, generous empty space "
                 "around it. Minimal and premium. No text."),
         checks=['This is the image people zoom into: details must be right']),
    dict(id='VID-05', name='Looping turntable video (optional, replaces IMG-08)', kind='video', priority='P3',
         where='Theme editor › Home page › Feature grid › Or a looping video', ratio='16:9', size='1920 × 1080, 6–8 s, MP4 under 10 MB', file='alumnus-vid-05-loop.mp4',
         model='Kling 3.0 image-to-video, IMG-08 as both start and end frame',
         prompt=("Slow 360-degree turntable rotation of the device in place, light glints across the vertical grooves, camera locked "
                 "off, background unchanged, ends exactly where it started so the clip loops seamlessly."),
         checks=['No morphing of the grooves during the turn', 'Plays muted; no audio needed']),
    dict(id='IMG-09', name='Feature tile: One-press recording', kind='image', priority='P2',
         where='Theme editor › Home page › Feature grid › Feature 1 › Image', ratio='4:3', size='1200 × 900 px', file='alumnus-img-09-one-press.jpg',
         model='Nano Banana Pro with device references',
         prompt=("Macro photo, 4:3. A thumb presses the slide switch on the black top strip of [DEVICE], which is attached to the "
                 "back of a phone held in one hand. Very shallow depth of field, soft daylight, the tiny white sound-wave light "
                 "glowing. No text."),
         checks=['Confirm which control starts recording on your unit and describe that control in the prompt']),
    dict(id='IMG-10', name='Feature tile: Card-thin, magnetic', kind='image', priority='P2',
         where='Theme editor › Home page › Feature grid › Feature 2 › Image', ratio='4:3', size='1200 × 900 px', file='alumnus-img-10-card-thin.jpg',
         model='Nano Banana Pro with device references',
         prompt=("Product photo, 4:3. [DEVICE] lies flat next to a plain blank card the size of a credit card (no logos, no numbers) "
                 "on a pale grey surface. Camera almost at table height so the thin edge is visible. Soft side light, crisp edges, "
                 "minimal. No text."),
         checks=['Thickness looks right next to the card (about 3 mm; confirm your real spec)']),
    dict(id='IMG-11', name='Feature tile: Records calls', kind='image', priority='P2',
         where='Theme editor › Home page › Feature grid › Feature 3 › Image', ratio='4:3', size='1200 × 900 px', file='alumnus-img-11-calls.jpg',
         model='Soul 2.0 → Nano Banana Pro edit',
         prompt=("Lifestyle photo, 4:3. Close view of a person holding a smartphone to their ear in a bright modern office, [DEVICE] "
                 "clearly attached to the back of the phone facing the camera. Face partly out of frame and softly out of focus, "
                 "natural light. No text."),
         checks=['Device sharp, person soft']),
    dict(id='IMG-12', name='Feature tile: All-day battery', kind='image', priority='P2',
         where='Theme editor › Home page › Feature grid › Feature 4 › Image', ratio='4:3', size='1200 × 900 px', file='alumnus-img-12-charging.jpg',
         model='Nano Banana Pro with device references + a photo of your real cable',
         prompt=("Product photo, 4:3. [DEVICE] on a light wood desk with its magnetic charging cable attached; the cable curves "
                 "gracefully out of frame. Soft morning light, minimal props. Match the cable and connector to the reference photo "
                 "exactly. No text."),
         checks=['Connector position matches your real device']),
    dict(id='IMG-13', name='App showcase: phone with the summary screen', kind='image', priority='P1',
         where='Theme editor › Home page › App showcase › Image', ratio='1:1', size='1600 × 1600 px', file='alumnus-img-13-app.jpg',
         model='Nano Banana Pro (scene) + composite your real screenshot APP-01 onto the screen',
         prompt=("Square product photo, 1:1, on a dark charcoal surface. A smartphone stands at a slight angle with its screen facing "
                 "the camera; the screen is plain pure white. [DEVICE] lies flat beside it at a slight angle. Soft top light, subtle "
                 "warm orange rim light, premium tech mood. Leave the screen pure white for compositing. No text. Then: \"Place this "
                 "screenshot onto the phone screen with matching perspective and glass reflection; keep everything else identical.\""),
         checks=['The screen must show your real app (APP-01), never an AI-invented interface']),
    dict(id='IMG-17', name='Export visual: one recording, many formats', kind='image', priority='P3',
         where='Theme editor › Home page › Export formats › Image', ratio='16:9', size='2400 × 1350 px', file='alumnus-img-17-export.jpg',
         model='Nano Banana Pro or Kling Image 3.0 (clean 3D render)',
         prompt=("Clean 3D render, 16:9. [DEVICE] floats in the center of a soft white-to-pale-grey space with a faint glowing sound "
                 "wave above it. Around it, five translucent frosted-glass cards float outward in a gentle arc, each showing only a "
                 "simple icon: a document, a word-processor page, an envelope, an audio waveform, a download arrow. Subtle orange "
                 "accent light, soft shadows, airy and minimal. No letters or words anywhere."),
         checks=['No fake file names or text on the cards']),
    dict(id='IMG-18', name='Product gallery 1: front packshot (main image)', kind='image', priority='P1',
         where='Shopify admin › Products › Alumnus AI Recorder › Media (first image)', ratio='1:1', size='2048 × 2048 px', file='alumnus-img-18-front.jpg',
         model='Nano Banana Pro with device references',
         prompt=("Studio packshot, 1:1. [DEVICE] stands upright facing the camera straight on, perfectly centered, filling about 65% "
                 "of the frame. Seamless light-grey background (#F4F4F6), large soft light from above-left, soft shadow, ultra sharp. "
                 "No props, no text."),
         checks=['This image feeds Google Shopping, the Shop app and Meta catalogs: product only, no text or badges']),
    dict(id='IMG-19', name='Product gallery 2: back / magnetic side', kind='image', priority='P2',
         where='Shopify admin › Products › Media', ratio='1:1', size='2048 × 2048 px', file='alumnus-img-19-back.jpg',
         model='Nano Banana Pro with a real photo of the back as reference',
         prompt=("Studio packshot, 1:1, same setup as IMG-18. The back of the device, showing its flat magnetic back exactly as in the "
                 "reference photo of the back. No text."),
         checks=['Only generate this if you have a real photo of the back; otherwise photograph it']),
    dict(id='IMG-20', name='Product gallery 3: on a phone', kind='image', priority='P1',
         where='Shopify admin › Products › Media', ratio='1:1', size='2048 × 2048 px', file='alumnus-img-20-on-phone.jpg',
         model='Nano Banana Pro with device references',
         prompt=("Studio photo, 1:1, same setup as IMG-18. Three-quarter view of the back of a modern smartphone with [DEVICE] attached "
                 "in the center. No phone-brand logo. No text."),
         checks=['Phone looks generic (no Apple/Samsung logo)']),
    dict(id='IMG-21', name='Product gallery 4: edge-on (thinness)', kind='image', priority='P2',
         where='Shopify admin › Products › Media', ratio='1:1', size='2048 × 2048 px', file='alumnus-img-21-edge.jpg',
         model='Nano Banana Pro with device references',
         prompt=("Studio photo, 1:1, same setup as IMG-18. [DEVICE] seen exactly edge-on, standing on its long side, very low camera "
                 "angle, showing the slim profile. No text."),
         checks=['Proportions match the real thickness']),
    dict(id='IMG-22', name='Product gallery 5: in hand for scale', kind='image', priority='P2',
         where='Shopify admin › Products › Media', ratio='1:1', size='2048 × 2048 px', file='alumnus-img-22-in-hand.jpg',
         model='Nano Banana Pro with device references',
         prompt=("Studio photo, 1:1, light-grey background. A hand holds [DEVICE] between thumb and fingers, front facing the camera, "
                 "to show its size. Natural skin, short clean nails. No text."),
         checks=['Five fingers, natural grip, device not oversized']),
    dict(id='IMG-23', name="Product gallery 6: what's in the box", kind='image', priority='P2',
         where='Shopify admin › Products › Media', ratio='1:1', size='2048 × 2048 px', file='alumnus-img-23-in-the-box.jpg',
         model='Nano Banana Pro with photos of every real item',
         prompt=("Top-down flat lay, 1:1, on light grey. [DEVICE], its magnetic charging cable coiled neatly, and a small blank "
                 "quick-start card, evenly spaced and aligned. Soft even light. No text."),
         checks=['Show only what you actually ship']),
    dict(id='IMG-24', name='Second color packshot (variant image)', kind='image', priority='P2',
         where='Shopify admin › Products › Media, then assign it to the second color variant', ratio='1:1', size='2048 × 2048 px', file='alumnus-img-24-color-2.jpg',
         model='Nano Banana Pro with a real photo of that color',
         prompt=("Same as IMG-18, but the device is in [your second color], matching the reference photo of that color exactly."),
         checks=['Only list colors you can actually ship']),
    dict(id='VID-06', name='Product 360° spin (product media video)', kind='video', priority='P3',
         where='Shopify admin › Products › Media (video)', ratio='1:1', size='1080 × 1080, 8 s loop, MP4', file='alumnus-vid-06-spin.mp4',
         model='Kling 3.0 image-to-video, IMG-18 as start and end frame',
         prompt=("Slow 360-degree turntable rotation of the device, camera locked off, studio light constant, background unchanged, "
                 "seamless loop."),
         checks=['Plays muted in the product gallery']),
    dict(id='IMG-25', name='FAQ image', kind='image', priority='P3',
         where='Theme editor › Home page › FAQ › Image', ratio='4:5', size='1200 × 1500 px', file='alumnus-img-25-faq.jpg',
         model='Nano Banana Pro with device references',
         prompt=("Vertical 4:5 photo, top-down at about 30 degrees. An open notebook with handwritten notes, a smartphone lying "
                 "face-down on it with [DEVICE] on its back, a pen with an orange cap, soft daylight from a window, calm and tidy. "
                 "The handwriting is blurred and unreadable. No text."),
         checks=['No readable words in the notebook']),
    dict(id='IMG-26', name='Closing offer background', kind='image', priority='P2',
         where='Theme editor › Home page › Closing offer › Background image', ratio='16:9', size='2400 × 1350 px', file='alumnus-img-26-closing.jpg',
         model='Soul 2.0 or Nano Banana Pro with device references',
         prompt=("Wide 16:9 evening desk scene. Warm desk lamp and cool laptop glow, a smartphone with [DEVICE] on its back on the "
                 "right third of the desk next to a notebook. The left 45% of the frame is dark, calm and empty for text. "
                 "Cinematic, moody but clean. No text, no readable screen."),
         checks=['Left side dark enough for white text']),
    dict(id='IMG-27', name='Discount popup image', kind='image', priority='P1',
         where='Theme editor › Discount popup (listed with the page sections) › Image', ratio='4:5', size='1000 × 1250 px', file='alumnus-img-27-popup.jpg',
         model='Nano Banana Pro with device references',
         prompt=("Vertical 4:5 bright product photo. A phone with [DEVICE] on its back lies on a pale surface beside a small white gift "
                 "box tied with an orange ribbon. Clean, cheerful, soft daylight, lots of white space. No text."),
         checks=['Reads clearly at small size']),
    dict(id='IMG-28', name='Social share image', kind='image', priority='P1',
         where='Theme editor › Theme settings › Favicon and sharing › Social share image', ratio='1.91:1', size='1200 × 630 px', file='alumnus-img-28-share.jpg',
         model='Nano Banana Pro with device references, then add your logo and headline in Canva',
         prompt=("Wide product photo, 1.91:1. A phone with [DEVICE] on its back stands at a three-quarter angle on the right side of "
                 "a white-to-pale-grey seamless background; the left half is empty for a logo and headline added later. No text."),
         checks=['This is what people see when your link is shared on iMessage, TikTok DMs and X']),
]

VIDEO_FILM = dict(
    id='VID-01', name='"Introducing Alumnus" brand film', where='Theme editor › Home page › Intro film › Shopify-hosted video (or paste a YouTube link)',
    spec='16:9, 1920 × 1080, 60–90 s, MP4 (H.264). Built from 8 short clips plus voice-over and music.',
    shots=[
        ('1', 'One press', '6 s', 'Close-up, top-down at 45°, a hand next to a phone lying face-down on a wooden lecture desk with [DEVICE] on its back.',
         'Static camera. The index finger presses the switch on the black top strip; the small white sound-wave light softly turns on. Natural hand movement, shallow depth of field.'),
        ('2', 'Eyes up', '6 s', 'IMG-02 (student in a sunlit lecture hall, device on the desk).',
         'Slow dolly in toward the student, who keeps listening and nods slightly; the lecturer stays out of focus in the background. One continuous shot.'),
        ('3', 'Card-thin', '5 s', 'Macro of the device standing on its edge on a pale grey surface.',
         'Slow 90-degree orbit around the device; a soft light sweep crosses the grooves and reveals how thin it is.'),
        ('4', 'On a call', '6 s', 'A young professional walking down a bright office corridor, phone to ear, device visible on the back of the phone.',
         'Smooth tracking shot moving backward in front of them as they walk and talk naturally.'),
        ('5', 'In the meeting', '6 s', 'Four colleagues around a light wood table; the phone with the device lies in the center among notebooks.',
         'Slow lateral pan from left to right across the table; people talk and gesture naturally.'),
        ('6', 'The notes', '5 s', 'Hands holding a phone over a desk; the screen is plain white (you place a real screen recording or APP-01 on it in editing).',
         'Static camera, the thumb scrolls gently; subtle hand movement only.'),
        ('7', 'Study time', '6 s', 'Evening desk, warm lamp, a student reviewing notes on a laptop, phone with the device beside the notebook.',
         'Slow push-in toward the device on the desk.'),
        ('8', 'End card', '5 s', 'IMG-08 (device floating on pale grey).',
         'Slow 180-degree orbit that ends facing front; hold the last second still for your logo and price card.'),
    ],
    vo=("Ever tried to take notes and actually listen at the same time? (beat) Meet Alumnus. One press, and it records your "
        "lecture, meeting or call. No unlocking your phone. No typing. Just listen. It's card-thin, snaps onto your phone, and "
        "captures calls without speakerphone. Then the app does the rest: a clean summary, a mind map and a to-do list, from 17 "
        "templates. Export to PDF, Word or email in a tap. In class. At work. On a call. On the go. Alumnus. Listen, don't type."),
)

CLIPS = [
    dict(id='VID-02', name='Use-case clip: The lecture', where='Theme editor › Home page › Video carousel › Video 1', caption='Press once. → Actually listen. → Notes ready before you leave the room.',
         shots=[('A', '5 s', 'Vertical 9:16. A student sits down in a lecture hall and places a phone face-down on the desk with [DEVICE] on its back.', 'Handheld phone-camera look; the student presses the switch on the device and leans back to listen.'),
                ('B', '6 s', 'Vertical 9:16. The same student listening and smiling at something the lecturer says (lecturer out of focus); no laptop open.', 'Slow push-in, natural reactions.'),
                ('C', '5 s', 'Vertical 9:16. After class, the student walks out holding the phone, glances at it (screen not visible) and smiles.', 'Tracking shot following them through the hallway.')]),
    dict(id='VID-03', name='Use-case clip: The client call', where='Theme editor › Home page › Video carousel › Video 2', caption='Snap it on. → Take the call. → Summary and action items, done.',
         shots=[('A', '4 s', 'Vertical 9:16 macro. A hand brings [DEVICE] to the back of a smartphone.', 'The device snaps onto the phone magnetically; slight camera shake on contact, then still.'),
                ('B', '6 s', 'Vertical 9:16. A young analyst walks outdoors near a glass office building, phone to ear, device visible on the back.', 'Tracking shot walking backward in front of them.'),
                ('C', '5 s', 'Vertical 9:16. Seated at a desk, they look at their phone (screen not visible) and nod, satisfied.', 'Static medium shot.')]),
    dict(id='VID-04', name='Use-case clip: The team meeting', where='Theme editor › Home page › Video carousel › Video 3', caption='Press. Talk. Done. → Minutes and to-dos for everyone.',
         shots=[('A', '4 s', 'Vertical 9:16 top-down. A phone with [DEVICE] is placed in the center of a meeting table; a hand presses the switch.', 'Static top-down camera.'),
                ('B', '6 s', 'Vertical 9:16. A small team discussing around the table in natural light.', 'Slow orbit around the table.'),
                ('C', '5 s', 'Vertical 9:16. The founder holds the phone and smiles, showing the screen to a colleague (screen facing away from camera).', 'Static medium shot.')]),
]

ADS = [
    ('AD-01', '"I stopped taking notes in class"', 'Creator-style talking head (Higgsfield UGC Factory or Marketing Studio, UGC preset, 9:16). Hook in the first 2 seconds, then the device, then a real screen recording of the summary.',
     'Vertical 9:16, handheld selfie framing in a dorm room. A student talks to camera: "I stopped taking notes in lectures. Here\'s why." Cut to them pressing [DEVICE] on the back of their phone. Natural vlog pacing, casual and honest.'),
    ('AD-02', '"Why not just use your phone?"', 'Split-screen comparison, 9:16. Mirrors the comparison table on the site.',
     'Vertical 9:16 split screen. Left: a stressed student typing fast on a laptop and missing what the lecturer says. Right: a relaxed student listening, phone with [DEVICE] on the desk. Same lecture hall, same light.'),
    ('AD-03', 'The snap (product ASMR)', 'Product-only macro loop, no people. Add a real recorded snap sound.',
     'Vertical 9:16 macro. [DEVICE] snaps onto the back of a phone in slow motion, the white sound-wave light turns on, then a slow orbit shows the thin edge. Clean studio light, pale grey background.'),
]

# --------------------------------------------------------------------------------------------
def fill(text):
    return (E(text)
            .replace('[DEVICE]', '<span class="tok">[DEVICE]</span>')
            .replace('[CAST]', '<span class="tok">[CAST]</span>'))


def asset_card(a):
    kind_label = {'image': 'Image', 'video': 'Video', 'real': 'Real asset'}[a['kind']]
    checks = ''.join(f'<li>{E(c)}</li>' for c in a.get('checks', []))
    return f"""
    <article class="card">
      <header class="card__head">
        <span class="pill">{E(a['id'])}</span>
        <h4>{E(a['name'])}</h4>
        <span class="prio prio--{a['priority'].lower()}">{E(a['priority'])}</span>
      </header>
      <dl class="meta">
        <div><dt>Where it goes</dt><dd>{E(a['where'])}</dd></div>
        <div><dt>Format</dt><dd>{kind_label} · {E(a['ratio'])} · {E(a['size'])}</dd></div>
        <div><dt>File name</dt><dd><code>{E(a['file'])}</code></dd></div>
        <div><dt>Higgsfield model</dt><dd>{E(a['model'])}</dd></div>
      </dl>
      <div class="prompt"><span class="prompt__label">Prompt</span>{fill(a['prompt'])}</div>
      {'<ul class="checks">' + checks + '</ul>' if checks else ''}
    </article>"""


def film_block(f):
    rows = ''.join(
        f"<tr><td class='nowrap'><b>{E(n)}</b> {E(t)}</td><td>{E(d)}</td><td>{fill(start)}</td><td>{fill(motion)}</td></tr>"
        for n, t, d, start, motion in f['shots'])
    return f"""
    <article class="card card--wide">
      <header class="card__head"><span class="pill">{f['id']}</span><h4>{E(f['name'])}</h4><span class="prio prio--p1">P1</span></header>
      <dl class="meta">
        <div><dt>Where it goes</dt><dd>{E(f['where'])}</dd></div>
        <div><dt>Format</dt><dd>{E(f['spec'])}</dd></div>
        <div><dt>File name</dt><dd><code>alumnus-vid-01-film.mp4</code></dd></div>
        <div><dt>Higgsfield model</dt><dd>Start frames: Soul 2.0 / Nano Banana Pro. Motion: Kling 3.0 or Seedance 2.0 image-to-video, one camera move per clip. Edit in CapCut or Premiere.</dd></div>
      </dl>
      <table class="tbl tbl--small">
        <thead><tr><th>Shot</th><th>Length</th><th>Start frame (image prompt)</th><th>Motion prompt (video)</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
      <div class="prompt"><span class="prompt__label">Voice-over (≈150 words ≈ 60 s)</span>{E(f['vo'])}</div>
      <ul class="checks"><li>Music: light, optimistic indie-electronic, 100–110 BPM, no vocals.</li>
      <li>Voice: record a real person (you, a friend, a student creator). If you use an AI voice, label the ad as AI-generated on TikTok and Meta.</li>
      <li>Add captions in the edit. Keep the last 2 seconds for your logo and the launch price.</li></ul>
    </article>"""


def clip_block(c):
    rows = ''.join(f"<tr><td class='nowrap'><b>{E(n)}</b> {E(t)}</td><td>{fill(start)}</td><td>{fill(motion)}</td></tr>" for n, t, start, motion in c['shots'])
    return f"""
    <article class="card card--wide">
      <header class="card__head"><span class="pill">{c['id']}</span><h4>{E(c['name'])}</h4><span class="prio prio--p2">P2</span></header>
      <dl class="meta">
        <div><dt>Where it goes</dt><dd>{E(c['where'])}</dd></div>
        <div><dt>Format</dt><dd>9:16 vertical · 1080 × 1920 · 15–20 s · MP4</dd></div>
        <div><dt>On-screen captions</dt><dd>{E(c['caption'])}</dd></div>
        <div><dt>Higgsfield model</dt><dd>Soul 2.0 start frames (+ Nano Banana Pro device fix) → Kling 3.0 image-to-video</dd></div>
      </dl>
      <table class="tbl tbl--small">
        <thead><tr><th>Shot</th><th>Start frame</th><th>Motion</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </article>"""


def table(head, rows, cls='tbl'):
    th = ''.join(f'<th>{h}</th>' for h in head)
    body = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'


def src(n):
    return f'<sup class="src">[{n}]</sup>'


# --------------------------------------------------------------------------------------------
# Section content
# --------------------------------------------------------------------------------------------
section_compare_rows = [
    ['Announcement bar', 'Blue bar with a limited-time offer', 'Orange bar, placeholder offer', 'Rotating messages + a live countdown to your real sale end date (hides itself when the sale ends)'],
    ['Header', 'Logo, anchor links, buy button', 'Same', 'Sticky, frosted header, anchor links, black <b>Buy now</b> pill, cart count, Shopify account sign-in, mobile slide-out menu'],
    ['Hero', 'Small label, big headline, large product image, CTA with price and stars', 'Similar, supplier photo with Chinese marketing text', 'Same structure on a white canvas, large rounded media frame (IMG-01 / IMG-01M), live price + compare-at, star rating, trust line'],
    ['Intro film', '"Introducing Pocket" card with video', 'Card with video placeholder', 'Grey card, play button, Shopify-hosted video or YouTube/Vimeo (VID-01 + IMG-02)'],
    ['Logo bar', '"Trusted by people at" + company logos', '[Logo] placeholders', 'Greyscale logo bar; doubles as an "As seen in" press bar'],
    ['Video stories', '3 vertical customer videos with names', '3 placeholders', 'Swipeable carousel of muted autoplay clips with sound toggle (VID-02 to VID-04) and an honest "Demo footage" note until real customer clips exist'],
    ['Statement + wide image', 'Big statement and wide brand image', 'Dark section', 'Light, airy wide image (IMG-03 / IMG-03M), like Pocket'],
    ['Real-life gallery', 'Row of lifestyle photos', '4 photo placeholders', 'Swipeable 4:5 photo cards (IMG-04 to IMG-07)'],
    ['Feature bento', '"Simple on the outside. Genius inside." with product images', 'Text cards only', 'Large macro image or loop (IMG-08 / VID-05) + 4 image feature cards (IMG-09 to IMG-12)'],
    ['Review cards', '"400,000+ Creators, Founders and Thinkers" with photos', '4 text placeholders', 'Swipeable review cards with stars; optional real customer photos'],
    ['App section', '"AI that\'s more than smart" phone + feature cards', 'Dark section, text cards', 'Dark section with phone image (IMG-13) + 3 real screenshot cards (APP-01 to APP-03)'],
    ['Integrations', '"Takes one conversation and updates all your apps"', 'Format pills', 'Format pills + export visual (IMG-17)'],
    ['<b>New</b>: comparison', 'Separate "Pocket vs Plaud" pages', '—', '"Why not just use your phone?" table on the page'],
    ['Buy box', 'Gallery + options + bundles + popup', 'Gallery, color, 2 bundle options', 'Gallery (IMG-18 to IMG-24), color swatches, 3 bundle tiers with badges and per-unit prices, countdown, Shop Pay express, Pay-in-4 message, trust badges, payment icons, sticky buy bar'],
    ['<b>New</b>: risk reversal', 'Free shipping in offer copy', 'Trust line only', '"Try it risk-free" strip: shipping, returns, warranty, pay in 4'],
    ['Specs', 'Spec grid', 'Spec grid', 'Spec grid that can pull values from product metafields'],
    ['Plans', '"Unlock your best with Pocket Pro" 3 columns', 'Free / Pro / Teams', 'Same 3 plans, highlighted Pro, "no subscription needed" note'],
    ['Privacy', '"Your data stays yours always"', 'Lock + text', 'Lock icon + 3 proof points (encrypted, delete anytime, not used for training)'],
    ['Reviews', '"400,000+ Happy Customers" review app widget', 'Manual placeholders', 'Live average + count from your reviews app (Judge.me etc.) and an app block slot for the full widget'],
    ['FAQ', 'Tabs + accordion + product image', 'Same', 'Same, plus FAQ rich-result schema for Google (IMG-25)'],
    ['<b>New</b>: closing offer', '—', '—', 'Dark banner with countdown, price and CTA (IMG-26)'],
    ['Popup', '"Claim your 45% off today" email popup', '—', 'Timed / scroll / exit-intent popup with instant code, copy button, auto-apply link, teaser tab (IMG-27)'],
    ['Cart', 'Standard Shopify cart', '—', 'Slide-out cart with savings lines, discount code field, add-on offer, Pay-in-4, express checkout'],
    ['Footer', 'Links, app badges, big logo', 'Links, newsletter, badges', 'Same, with Shopify-native email signup and big wordmark'],
]

design_rows = [
    ['Canvas', 'Pure white, light grey cards', 'Warm cream + dark sections', 'White + #F4F4F6 cards, one dark app section'],
    ['Accent', 'Bright blue', 'Burnt orange #C2410C', 'Kept your orange (one setting to switch, e.g. #2F5BFF for a Pocket-style blue)'],
    ['Type', 'Clean grotesk, semibold, tight tracking', 'Very heavy display grotesk', 'Inter Semibold headlines, tight tracking, Inter body (from Shopify\'s font library)'],
    ['Shapes', 'Large rounded corners, pill buttons', 'Rounded cards', '28 px card radius, pill buttons, soft shadows'],
    ['Imagery', 'Studio product shots + lifestyle + video everywhere', 'Supplier photos', '30 labelled slots, one consistent Higgsfield art direction'],
    ['Motion', 'Subtle fades, carousels', '—', 'Fade-up on scroll, swipe carousels with arrows, autoplay loops that pause off-screen'],
]

pocket_rows = [
    ['Price anchor', 'List $199, sells around $129–$139; "Up to 45% off" ' + src(1) + src(2), 'Big headline saving, but buyers notice a permanent "sale". Use a compare-at price only if you really sold at it.'],
    ['Quantity tiers', 'Solo 35% off, Double Pack 40%, Team Pack 45%; reported $139 / $238 / $327 (about $139 / $119 / $109 each) ' + src(2) + src(3), 'Moves people to 2–3 units and raises order value. Built into the new buy box.'],
    ['No subscription + free tier', '"No subscription required", unlimited free transcription; Pro optional, about $16.59/mo yearly or about $20 monthly ' + src(1) + src(4), 'Removes the #1 objection for AI gadgets. Copy this message if your app really works without a plan.'],
    ['Pro add-on', '"12-month access to Pocket Pro, 25% off" sold as a store product ' + src(5), 'Recurring revenue at checkout. Only possible if your supplier gives you activation codes.'],
    ['Email popup', '"Claim your 45% off today" (in your screenshot); one reviewer says the 45% email code didn\'t apply at checkout ' + src(6), 'Big list growth. Lesson: test that the code really works.'],
    ['Quiz funnel', '"Take the Pocket Quiz & Get Up to 45% Off" ' + src(7), 'Personalises the pitch and captures email. Phase 2 for Alumnus.'],
    ['Comparison pages', '"Pocket vs Plaud Note": range, one press, languages, free minutes ' + src(8), 'Catches people already comparing. On your page as a table; keep claims true.'],
    ['Persona / advertorial pages', 'Separate pages for founders and C-suite, advertorial-style pages, several homepage variants ' + src(7), 'Ads land on a page written for that audience. Use the new Landing page template.'],
    ['Affiliate program', 'Public affiliate page ' + src(7), 'Creators sell for you. Use Shopify Collabs.'],
    ['Social proof', '"160,000+" on one page, "400,000+" in your screenshot; logo bar; video testimonials ' + src(9), 'Strong, but use only real numbers.'],
]

competitor_rows = [
    ['Plaud', '"Trusted by 1,000,000+ users" (US page); 10% education discount for students, educators and healthcare, verified via ID.me / Student Beans / GoCertify; device + AI plan bundles (e.g. Note + Unlimited annual $367 vs $399); seasonal sales up to 20%; press quotes ' + src(10) + src(11) + src(12), 'Student offer fits Alumnus perfectly; device + plan bundles if you get codes'],
    ['Bee (Amazon)', '$49.99 hardware, optional subscription ' + src(13), 'Low entry price; be clear why Alumnus costs more'],
    ['Omi', 'About $89, no required subscription ' + src(13), '"No subscription" is now table stakes'],
    ['Limitless', 'Bought by Meta (Dec 2025); pendant no longer sold to new buyers ' + src(13), 'Buyers fear orphaned devices: stress export, warranty and support'],
]

tactic_rows = [
    ['Announcement bar + real countdown', 'Pocket, Plaud', 'Header › Announcement bar; countdown date in Theme settings › Product and offer', 'Set a real sale end date'],
    ['Price, compare-at and stars beside every CTA', 'Pocket', 'Hero, Buy box, Closing offer, Sticky bar', 'Set price/compare-at on the product'],
    ['Quantity tiers with badges and per-unit price', 'Pocket', 'Buy box › Bundle tier blocks', 'Create 2 automatic discounts (2+ and 3+ units)'],
    ['Free extra on bigger bundles', 'DTC standard', 'Buy box › tier "Free extra" text', 'Buy X get Y automatic discount, or ship it free'],
    ['Shop Pay express + Pay in 4', 'Shopify', 'Buy box, cart', 'Turn on Shop Pay and Installments'],
    ['Sticky buy bar', 'DTC standard', 'Buy box › Sticky bar', '—'],
    ['Email popup with instant code', 'Pocket', 'Discount popup (timer, scroll, exit intent, teaser)', 'Create WELCOME code; Shopify Messaging welcome flow'],
    ['Slide-out cart with savings, code field and add-on', 'DTC standard', 'Cart drawer; Theme settings › Cart', 'Pick an add-on product'],
    ['Logos, video stories, review cards, live stars', 'Pocket', 'Logo bar, Video carousel, Review cards, Reviews', 'Install a reviews app (Judge.me)'],
    ['Comparison table', 'Pocket (vs Plaud pages)', 'Comparison table section', 'Keep every claim true'],
    ['Risk reversal', 'Plaud, DTC standard', 'Guarantee section + buy box trust badges', 'Match your refund policy'],
    ['Subscription transparency', 'Pocket', 'Plans section + FAQ', 'Confirm app limits with supplier'],
    ['Privacy reassurance', 'Pocket', 'Privacy section', 'Confirm data handling with supplier'],
    ['FAQ objection handling + rich results', 'Pocket', 'FAQ (with FAQPage schema)', '—'],
    ['Second CTA at the end', 'Pocket', 'Closing offer section', '—'],
    ['Persona / ad landing pages', 'Pocket', 'Page template "landing"', 'Create a page, choose template "landing"'],
    ['Student discount', 'Plaud', 'Announcement message, FAQ question, buy box text block', 'Student verification app'],
    ['Creator / affiliate program', 'Pocket', 'Footer link + Collabs page', 'Install Shopify Collabs'],
    ['Honest low-stock message', 'DTC standard', 'Buy box › "Only X left" threshold', 'Track inventory'],
    ['Quiz funnel', 'Pocket', 'Not built yet (phase 2)', 'Quiz app or a landing page'],
]

shopify_rows = [
    ['1', 'Create the product', 'Products › Add: "Alumnus AI Recorder", option <b>Color</b> (Graphite + any real second color), price, compare-at (only if genuine), SKU, weight, inventory tracking. Upload IMG-18 to IMG-24 and VID-06 as media; assign IMG-24 to its color.'],
    ['2', 'Connect the theme', 'Online Store › Themes › Add theme › Upload zip. Then Customize › Theme settings › Product and offer › <b>Your Alumnus product</b> (one setting feeds hero, buy box, sticky bar, closing offer and reviews).'],
    ['3', 'Bundle discounts', 'Discounts › Create › Amount off products: "Duo bundle 10% off", minimum quantity 2; "Study group 15% off", minimum quantity 3. Same product, automatic. Shopify applies the best one. Match the % in the Buy box tiers. Their titles show in the cart as savings lines.'],
    ['4', 'Welcome code', 'Discounts › Create code <b>WELCOME10</b> (or your %), one use per customer, and decide whether it combines with the bundle discounts (recommended: no).'],
    ['5', 'Payments', 'Settings › Payments: Shop Pay, Shop Pay Installments (Pay in 4 on orders of $50–$3,000), Apple Pay, Google Pay. The theme already shows the Installments message.'],
    ['6', 'Email and SMS', 'Shopify Messaging (formerly Shopify Email): welcome series with the code, abandoned checkout, abandoned cart, browse abandonment, post-purchase review request, win-back. 10,000 free emails a month on paid plans; abandoned checkout emails don\'t count.'],
    ['7', 'Reviews', 'Install Judge.me (free plan available) or similar. It writes Shopify\'s standard rating fields, so stars and counts appear in the hero, buy box and Reviews section automatically. Add its widget as an app block in the Reviews section.'],
    ['8', 'Customer accounts', 'Settings › Customer accounts: use the new customer accounts. The header already includes Shopify\'s sign-in component.'],
    ['9', 'Policies and contact', 'Settings › Policies: refund (30 days), shipping (real times), privacy, terms. Create a Contact page with the "contact" template.'],
    ['10', 'Channels', 'Add TikTok, Facebook & Instagram, and Google & YouTube sales channels so your catalog and pixels sync. You already post on TikTok, so TikTok is the first to set up.'],
]

apps_rows = [
    ['Shopify Messaging', 'Email/SMS automations and campaigns', 'Free allowance', 'Welcome code, abandoned cart, review requests'],
    ['Shopify Flow', 'Automations', 'Free on Basic and up', 'Tag VIPs, alert on low stock, tag students, route reviews'],
    ['Shopify Collabs', 'Creator and affiliate program', 'Free install, 2.9% fee on automatic payouts', 'Seed devices to student creators; replace AI demos with real clips'],
    ['Search & Discovery', 'Complementary products', 'Free', 'Pick the cart add-on and recommendations'],
    ['Shopify Bundles', 'Fixed bundles', 'Free', 'e.g. Alumnus + sleeve as one product (optional)'],
    ['Shopify Inbox', 'Chat', 'Free', 'Answer pre-sale questions'],
    ['Judge.me', 'Reviews with photos/videos', 'Free plan available', 'Live stars + UGC for the review cards'],
    ['Student discount app', 'Verified student pricing', 'Varies (e.g. Easy Student Discounts, StudyPerks)', 'Match Plaud\'s education offer'],
    ['Shop app / Shop Campaigns', 'Shop app audience', 'Pay per sale (if eligible)', 'Follow on Shop button is in the footer settings'],
]

offer_rows = [
    ['Everyday price', 'Your real price (competitors sit around $129–$189)', 'Use compare-at only if you genuinely sold at that price for a meaningful period'],
    ['Bundles', 'Solo 0% · Duo 10% · Study group (3) 15% (theme defaults)', 'Raise only if your margin allows; Pocket\'s 35–45% is measured from a high list price'],
    ['Welcome offer', '10% off the first order via the popup', 'Don\'t let it stack with bundle tiers'],
    ['Student offer', '10% with verification', 'Same as Plaud; your brand name fits students'],
    ['Risk reversal', 'Free US shipping, 30-day returns, 1-year warranty', 'Only promise what your supplier and margin can back'],
    ['Holiday', 'BFCM: Thu Nov 26 to Mon Nov 30, 2026; gift message "one for you, one to gift" through December', 'Set the countdown to the real end date'],
    ['Add-on', 'Sleeve, spare cable or Pro plan card in the cart (about $15–$25)', 'Lifts order value with one tap'],
]

compliance = [
    ('Fake reviews and testimonials', 'The FTC\'s rule (16 CFR Part 465) bans reviews and testimonials that claim to be from people who don\'t exist or who didn\'t use the product, including AI-generated ones, with civil penalties for knowing violations ' + src(14) + '. So: AI actors are fine for <i>demo</i> footage, never as "customers". The video carousel ships with a "Demo footage" note; review sections are for real reviews only.'),
    ('Sale prices', 'A compare-at ("was") price must be a real former price (FTC Guides Against Deceptive Pricing). Bundle savings are always truthful because they are measured against your own single-unit price.'),
    ('Urgency', 'Countdowns use your real sale end date and disappear when it passes. Low-stock messages use real inventory.'),
    ('Shipping times', 'State realistic shipping windows and email customers about delays (FTC Mail, Internet or Telephone Order Rule).'),
    ('Recording consent', 'Some US states require everyone on a call to consent. The FAQ says this; keep it.'),
    ('AI ads', 'TikTok requires a label on ads with realistic AI-generated people, voices or scenes (reported live from July 2026) ' + src(15) + '. Label AI ads and keep them away from real private individuals.'),
    ('Email and SMS', 'Use the consent checkbox wording in the popup; SMS needs express written consent (TCPA).'),
]

sources = [
    ('1', 'Plaud, "Is HeyPocket legit? A straight review of the Pocket AI recorder"', 'https://www.plaud.ai/blogs/articles/heypocket-review'),
    ('2', 'mrktcorrect, "Pocket AI pricing: what it really costs over 12 months"', 'https://mrktcorrect.com/blog/pocket-ai-pricing'),
    ('3', 'FlexGlimpse, heyPocket coupons (tier percentages)', 'https://www.flexglimpse.com/store/heypocket'),
    ('4', 'heypocket.com comparison and product pages', 'https://heypocket.com/pages/comparison'),
    ('5', 'heypocket.com, Pocket Pro 12-month access product', 'https://heypocket.com/products/pocket-pro-12-month-access-to-pocket-s-full-power-25-off-1'),
    ('6', 'Trustpilot, Pocket reviews', 'https://nz.trustpilot.com/review/heypocket.com?page=2'),
    ('7', 'heypocket.com pages: /pages/quiz, /pages/founders-csuite, /pages/this-simple-device-1, /pages/affiliate', 'https://heypocket.com/pages/quiz'),
    ('8', 'heypocket.com, "Pocket vs Plaud Note"', 'https://heypocket.com/pages/pocket-vs-plaud'),
    ('9', 'heypocket.com, Pocket summary page', 'https://heypocket.com/pages/pocket-summary'),
    ('10', 'Plaud education discount page and support article', 'https://support.plaud.ai/hc/en-us/articles/59006112625689-Student-educator-and-healthcare-discount'),
    ('11', 'DealNews, Plaud anniversary sale', 'https://www.dealnews.com/Plaud-Anniversary-Sale-Extra-20-off-free-shipping/21920626.html'),
    ('12', 'Tom\'s Guide, Plaud discount codes', 'https://www.tomsguide.com/uk/ai/plaud-ai-coupons'),
    ('13', 'Layer3 Labs, best AI wearable pendants 2026', 'https://www.layer3labs.io/guides/best-ai-wearable-pendants-2026'),
    ('14', 'Hogan Lovells, FTC final rule banning fake reviews and testimonials', 'https://www.hoganlovells.com/en/publications/ftc-publishes-final-rule-banning-fake-consumer-reviews-and-testimonials'),
    ('15', 'CineRads, TikTok AI content policy 2026; Common Thread Collective, TikTok AI ad disclosure rules', 'https://www.cinerads.com/blog/tiktok-ai-content-policy'),
    ('16', 'Higgsfield blog: Soul 2.0 vs Nano Banana Pro; AI UGC videos; Seedance prompting guide', 'https://higgsfield.ai/blog/soul-2-vs-nano-banana-pro'),
    ('17', 'Higgsfield prompt cheat sheet (camera presets, one move per clip)', 'https://memons.ai/higgsfield-prompt-cheat-sheet'),
    ('18', 'Shopify dev docs: theme architecture, Theme Store requirements, Shop Pay Installments, account component, Section Rendering API', 'https://shopify.dev/docs/storefronts/themes/architecture'),
    ('19', 'Shopify dev changelog: discounts on /cart/update.js', 'https://shopify.dev/changelog/posts/cart-ajax-api-discounts-support-on-cartupdatejs'),
    ('20', 'Shopify standard metafields (reviews.rating, reviews.rating_count)', 'https://shopify.dev/docs/apps/build/metafields/list-of-standard-definitions'),
    ('21', 'Shopify Messaging guide (free email allowance)', 'https://eseospace.com/blog/shopify-messaging/'),
    ('22', 'Shopify Flow (plans)', 'https://www.shopify.com/flow'),
    ('23', 'Shopify Collabs on the Shopify App Store', 'https://apps.shopify.com/collabs'),
    ('24', 'Shopify conversion benchmarks 2026 (Blend Commerce; DTC Pages)', 'https://blendcommerce.com/blogs/shopify/ecommerce-conversion-rate-benchmarks-2026'),
]

# --------------------------------------------------------------------------------------------
P1 = [a for a in ASSETS if a['priority'] == 'P1']
asset_map_rows = []
order = ['IMG-01', 'IMG-01M', 'VID-01', 'IMG-02', 'VID-02', 'VID-03', 'VID-04', 'IMG-03', 'IMG-04', 'IMG-05', 'IMG-06', 'IMG-07',
         'IMG-08', 'VID-05', 'IMG-09', 'IMG-10', 'IMG-11', 'IMG-12', 'IMG-13', 'APP-01–03', 'IMG-17', 'IMG-18', 'IMG-19', 'IMG-20',
         'IMG-21', 'IMG-22', 'IMG-23', 'IMG-24', 'VID-06', 'IMG-25', 'IMG-26', 'IMG-27', 'IMG-28']
lookup = {a['id']: a for a in ASSETS}
for aid in order:
    if aid in lookup:
        a = lookup[aid]
        asset_map_rows.append([f'<b>{aid}</b>', E(a['name']), E(a['ratio']), E(a['where']), a['priority']])
    elif aid == 'VID-01':
        asset_map_rows.append(['<b>VID-01</b>', 'Brand film (8 shots + VO)', '16:9', 'Home page › Intro film › Video', 'P1'])
    elif aid in ('VID-02', 'VID-03', 'VID-04'):
        c = [x for x in CLIPS if x['id'] == aid][0]
        asset_map_rows.append([f'<b>{aid}</b>', E(c['name']), '9:16', E(c['where'].replace('Theme editor › ', '')), 'P2'])
    elif aid == 'APP-01–03':
        asset_map_rows.append(['<b>APP-01–03</b>', 'Real app screenshots (summary, mind map, to-dos)', '4:3', 'Home page › App showcase › App feature blocks', 'P1 · real'])
for r in asset_map_rows:
    r[3] = r[3].replace('Theme editor › ', '')

CSS = f"""
@page {{ size: Letter; margin: 0.62in 0.62in 0.7in; }}
* {{ box-sizing: border-box; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ font-family: 'Inter', -apple-system, 'Segoe UI', Roboto, sans-serif; color: #0B0B0F; font-size: 9.6pt; line-height: 1.5; margin: 0; }}
h1, h2, h3, h4 {{ letter-spacing: -0.02em; line-height: 1.15; margin: 0; }}
h1 {{ font-size: 26pt; font-weight: 700; letter-spacing: -0.035em; }}
h2 {{ font-size: 15pt; font-weight: 700; margin: 18pt 0 8pt; }}
h3 {{ font-size: 11.5pt; font-weight: 700; margin: 14pt 0 6pt; }}
h4 {{ font-size: 10.5pt; font-weight: 700; }}
p {{ margin: 0 0 7pt; }}
ul {{ margin: 0 0 8pt; padding-left: 15pt; }}
li {{ margin-bottom: 3pt; }}
a {{ color: {ACCENT}; text-decoration: none; }}
code {{ font-family: 'JetBrains Mono', ui-monospace, Menlo, monospace; font-size: 8.4pt; background: #F4F4F6; padding: 1pt 4pt; border-radius: 4pt; }}
.muted {{ color: #5E606E; }}
.eyebrow {{ display: inline-block; font-size: 8pt; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: {ACCENT}; margin-bottom: 6pt; }}
.part {{ break-before: page; }}
.part__head {{ border-bottom: 2pt solid #0B0B0F; padding-bottom: 10pt; margin-bottom: 14pt; }}
.part__head p {{ margin: 6pt 0 0; color: #5E606E; font-size: 10.5pt; }}
.lead {{ font-size: 11pt; color: #33343C; }}
.callout {{ background: #FFF4ED; border-left: 3pt solid {ACCENT}; padding: 9pt 12pt; border-radius: 6pt; margin: 8pt 0 12pt; break-inside: avoid; }}
.callout--grey {{ background: #F4F4F6; border-left-color: #0B0B0F; }}
.callout b {{ color: #0B0B0F; }}
.tbl {{ width: 100%; border-collapse: collapse; margin: 6pt 0 12pt; font-size: 8.6pt; }}
.tbl th {{ text-align: left; font-weight: 700; font-size: 7.8pt; text-transform: uppercase; letter-spacing: .06em; color: #5E606E; border-bottom: 1.2pt solid #0B0B0F; padding: 5pt 6pt; }}
.tbl td {{ border-bottom: .6pt solid #E3E3E8; padding: 6pt 6pt; vertical-align: top; }}
.tbl tr {{ break-inside: avoid; }}
.tbl--small {{ font-size: 8.2pt; }}
.nowrap {{ white-space: nowrap; }}
.src {{ color: {ACCENT}; font-size: 6.5pt; font-weight: 700; }}
.cover {{ height: 9.6in; display: flex; flex-direction: column; justify-content: space-between; }}
.cover__brand {{ font-size: 20pt; font-weight: 700; letter-spacing: -0.05em; }}
.cover__brand span {{ color: {ACCENT}; }}
.cover h1 {{ font-size: 40pt; line-height: 1.02; letter-spacing: -0.045em; margin-top: 14pt; }}
.cover__sub {{ font-size: 13pt; color: #5E606E; margin-top: 14pt; max-width: 5.6in; }}
.cover__grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10pt; margin-top: 24pt; }}
.cover__box {{ background: #F4F4F6; border-radius: 12pt; padding: 12pt 14pt; }}
.cover__box b {{ display: block; font-size: 10.5pt; margin-bottom: 3pt; }}
.cover__box span {{ color: #5E606E; font-size: 9pt; }}
.cover__foot {{ display: flex; justify-content: space-between; color: #5E606E; font-size: 9pt; border-top: .8pt solid #E3E3E8; padding-top: 10pt; }}
.shot {{ width: 100%; border-radius: 10pt; border: .8pt solid #E3E3E8; display: block; }}
.figure {{ margin: 8pt 0 14pt; break-inside: avoid; }}
.figure figcaption {{ font-size: 8pt; color: #5E606E; margin-top: 4pt; }}
.two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12pt; }}
.anatomy {{ display: grid; grid-template-columns: auto auto 1fr; gap: 14pt; align-items: start; }}
.anatomy img {{ height: 7.6in; width: auto; display: block; border: .8pt solid #E3E3E8; border-radius: 6pt; }}
.anatomy__label {{ font-size: 7.5pt; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; color: #5E606E; margin-bottom: 4pt; }}
.card {{ border: .8pt solid #E3E3E8; border-radius: 10pt; padding: 10pt 12pt; margin: 0 0 10pt; break-inside: avoid; }}
.card--wide {{ break-inside: auto; }}
.card--wide .card__head, .card--wide .meta {{ break-after: avoid; }}
.card__head {{ display: flex; align-items: center; gap: 8pt; margin-bottom: 6pt; }}
.card__head h4 {{ flex: 1; }}
.pill {{ display: inline-block; background: {ACCENT}; color: #fff; font-family: 'JetBrains Mono', ui-monospace, monospace; font-weight: 700; font-size: 8pt; padding: 2pt 7pt; border-radius: 99pt; letter-spacing: .03em; white-space: nowrap; }}
.prio {{ font-size: 7.5pt; font-weight: 700; padding: 2pt 7pt; border-radius: 99pt; background: #F4F4F6; color: #33343C; }}
.prio--p1 {{ background: #0B0B0F; color: #fff; }}
.meta {{ display: grid; grid-template-columns: 1fr 1fr; gap: 3pt 14pt; margin: 0 0 7pt; }}
.meta div {{ display: grid; grid-template-columns: 0.95in 1fr; gap: 6pt; font-size: 8.4pt; }}
.meta dt {{ color: #5E606E; font-weight: 600; }}
.meta dd {{ margin: 0; }}
.prompt {{ background: #F7F7F9; border: .6pt solid #E3E3E8; border-left: 3pt solid {ACCENT}; border-radius: 6pt; padding: 7pt 10pt; font-size: 8.9pt; line-height: 1.5; margin-bottom: 6pt; }}
.prompt__label {{ display: block; font-size: 7pt; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: {ACCENT}; margin-bottom: 3pt; }}
.tok {{ background: #FFE8DA; color: #9A3412; border-radius: 3pt; padding: 0 2pt; font-weight: 700; font-size: 8.2pt; }}
.checks {{ margin: 0; padding-left: 13pt; font-size: 8.3pt; color: #33343C; }}
.checks li {{ margin-bottom: 1pt; }}
.blocktext {{ background: #0B0B0F; color: #F5F5F7; border-radius: 8pt; padding: 10pt 12pt; font-size: 8.8pt; margin: 6pt 0 10pt; break-inside: avoid; }}
.blocktext b {{ color: #FDBA74; display: block; font-size: 7.5pt; letter-spacing: .1em; text-transform: uppercase; margin-bottom: 4pt; }}
.steps {{ counter-reset: s; list-style: none; padding: 0; }}
.steps li {{ counter-increment: s; position: relative; padding-left: 22pt; margin-bottom: 6pt; }}
.steps li::before {{ content: counter(s); position: absolute; left: 0; top: 0; width: 15pt; height: 15pt; border-radius: 50%; background: #0B0B0F; color: #fff; font-size: 7.5pt; font-weight: 700; display: grid; place-items: center; }}
.checklist {{ columns: 2; column-gap: 18pt; list-style: none; padding: 0; }}
.checklist li {{ break-inside: avoid; padding-left: 14pt; position: relative; margin-bottom: 4pt; }}
.checklist li::before {{ content: ''; position: absolute; left: 0; top: 2.5pt; width: 8pt; height: 8pt; border: 1pt solid #0B0B0F; border-radius: 2pt; }}
.sources {{ list-style: none; padding: 0; }}
.sources li {{ font-size: 8.2pt; margin-bottom: 3pt; word-break: break-word; }}
.toc {{ list-style: none; padding: 0; margin: 10pt 0; }}
.toc li {{ display: flex; gap: 10pt; padding: 4.5pt 0; border-bottom: .6pt solid #E3E3E8; font-size: 10pt; }}
.toc li b {{ width: 0.5in; color: {ACCENT}; }}
"""


def build():
    film = film_block(VIDEO_FILM)
    clips = ''.join(clip_block(c) for c in CLIPS)
    cards = ''.join(asset_card(a) for a in ASSETS)
    ads = ''.join(
        f"<article class='card'><header class='card__head'><span class='pill'>{i}</span><h4>{E(t)}</h4><span class='prio'>Ads</span></header>"
        f"<p class='muted' style='font-size:8.6pt'>{E(d)}</p><div class='prompt'><span class='prompt__label'>Prompt</span>{fill(p)}</div></article>"
        for i, t, d, p in ADS)

    body = f"""
<section class="cover">
  <div>
    <div class="cover__brand">alumnus<span>.</span></div>
    <h1>Website playbook<br>&amp; Higgsfield prompt pack</h1>
    <p class="cover__sub">How the new Shopify theme compares with heypocket.com, the offers and conversion tactics Pocket and its competitors use (and where each one now lives on your site), how to connect the store more closely with Shopify, and a prompt for every image and video slot.</p>
    <div class="cover__grid">
      <div class="cover__box"><b>Part 1 · Pocket vs Alumnus</b><span>Section-by-section comparison and what changed</span></div>
      <div class="cover__box"><b>Part 2 · Offers &amp; conversion</b><span>Pocket, Plaud, Bee, Omi teardown and your offer stack</span></div>
      <div class="cover__box"><b>Part 3 · Shopify integration</b><span>Setup order, native features and apps</span></div>
      <div class="cover__box"><b>Part 4 · Higgsfield prompt pack</b><span>30+ assets keyed to the theme's labelled placeholders</span></div>
    </div>
  </div>
  <div class="cover__foot"><span>Prepared October 15, 2026</span><span>Theme: alumnus-theme (Shopify Online Store 2.0)</span></div>
</section>

<section class="part">
  <div class="part__head"><span class="eyebrow">Start here</span><h1>What you're getting</h1><p>Read this page first. Everything else is reference.</p></div>
  <ol class="steps">
    <li><b>A complete Shopify theme</b> in the same folder layout as your screenshot (assets, config, layout, locales, sections, snippets, templates) plus a ready-to-upload zip. It passes Shopify's Theme Check with 0 errors and 0 warnings.</li>
    <li><b>Every image and video slot shows a labelled placeholder</b> (for example <span class="pill">IMG-01</span>) until you upload the real file. Each label matches a prompt in Part 4, so you always know what goes where.</li>
    <li><b>Conversion features are built in:</b> bundle tiers, real countdowns, email popup with instant code, sticky buy bar, slide-out cart with add-on and discount field, comparison table, guarantee strip, FAQ schema, and a landing page template for ads.</li>
    <li><b>All copy is editable</b> in the theme editor. Anything in [brackets] is a fact only you or your supplier can confirm. The checklist at the end lists every one.</li>
  </ol>
  <h2>Fastest path to launch</h2>
  <ol class="steps">
    <li>Create the product in Shopify (Part 3, step 1) and upload the theme zip (Online Store › Themes › Add theme › Upload zip file).</li>
    <li>In Customize › Theme settings › Product and offer, pick <b>Your Alumnus product</b> and set the real sale end date.</li>
    <li>Create the two bundle discounts and the welcome code (Part 3, steps 3–4).</li>
    <li>Generate the <b>P1</b> assets first (hero, macro, app image, product packshots, popup, share image, brand film), then P2 and P3.</li>
    <li>Fill every [bracket] using the checklist, place a test order, then publish.</li>
  </ol>
  <div class="callout"><b>Three honesty rules that protect the store.</b> Only show real reviews, real customer counts and real logos. Use a compare-at price only if you really sold at it. Keep the "Demo footage" note on AI-made clips. The theme is built to make these the easy defaults; Part 2 explains why.</div>
  <ul class="toc">
    <li><b>Part 1</b>Pocket vs Alumnus: comparison and what changed</li>
    <li><b>Part 2</b>Offers and conversion research, and your recommended offer stack</li>
    <li><b>Part 3</b>Connecting the store more closely with Shopify</li>
    <li><b>Part 4</b>Higgsfield production guide and prompt pack</li>
    <li><b>Part 5</b>Launch checklist</li>
    <li><b>Sources</b></li>
  </ul>
</section>

<section class="part">
  <div class="part__head"><span class="eyebrow">Part 1</span><h1>Pocket vs Alumnus</h1><p>Your homepage already follows Pocket's section order. What made Pocket feel better was the execution: a white canvas, big rounded product media, video everywhere, and an offer engine around the buy box.</p></div>
  <div class="anatomy">
    <div><div class="anatomy__label">heypocket.com</div><img src="img/pocket-strip.jpg" alt="Pocket homepage"></div>
    <div><div class="anatomy__label">New Alumnus</div><img src="img/alumnus-strip.jpg" alt="New Alumnus homepage"></div>
    <div>
      <h3 style="margin-top:0">Same storyline, top to bottom</h3>
      <p>Both pages follow the classic hardware storyline: <b>promise</b> (hero) → <b>proof</b> (film, logos, real people) → <b>product</b> (design, app, formats) → <b>offer</b> (buy box, plans) → <b>reassurance</b> (privacy, reviews, FAQ).</p>
      <p>The new theme keeps that order and adds three conversion sections Pocket handles on separate pages or not at all: a <b>comparison table</b>, a <b>risk-free guarantee strip</b> and a <b>closing offer</b> with countdown.</p>
      <p class="muted">Left: your Pocket screenshot (the dark lower part is Pocket's discount popup covering the page). Right: the new Alumnus homepage rendered from the theme files, with labelled placeholders where the Higgsfield assets go.</p>
      <div class="callout callout--grey"><b>What I deliberately did not copy:</b> Pocket's exact headlines, logos and inflated "list price". Layout and conversion patterns are fair game; cloning copy or trade dress makes Alumnus look like a knock-off and invites trouble. Your accent stays orange; a Pocket-style blue is one setting away.</div>
    </div>
  </div>
</section>

<section class="part">
  <h2 style="margin-top:0">Section by section</h2>
  {table(['Section', 'heypocket.com', 'Your PDF homepage', 'New Alumnus theme'], section_compare_rows, 'tbl tbl--small')}
  <h2>Design system</h2>
  {table(['', 'Pocket', 'Your PDF homepage', 'New theme'], design_rows, 'tbl tbl--small')}
</section>

<section class="part">
  <h2 style="margin-top:0">What the new theme looks like</h2>
  <p class="muted">Rendered from the actual theme files with a sample product ($139, compare-at $199) and empty media slots.</p>
  <figure class="figure"><img class="shot" src="img/new-hero.jpg" alt=""><figcaption>Hero: announcement bar with live countdown, sticky header, labelled hero slot (IMG-01), price, rating and trust line.</figcaption></figure>
  <figure class="figure"><img class="shot" src="img/new-buybox.jpg" alt=""><figcaption>Buy box: color swatches, bundle tiers with badges and per-unit prices, countdown, Shop Pay express, Pay in 4, trust badges.</figcaption></figure>
</section>

<section class="part">
  <div class="two">
    <figure class="figure"><img class="shot" src="img/popup-desktop.jpg" alt=""><figcaption>Email popup (Pocket's "Claim your 45% off" pattern) with instant code and teaser tab.</figcaption></figure>
    <figure class="figure"><img class="shot" src="img/cart-drawer.jpg" alt=""><figcaption>Slide-out cart: bundle savings line, add-on offer, discount code field, Pay in 4, express checkout.</figcaption></figure>
  </div>
  <figure class="figure"><img class="shot" src="img/new-compare.jpg" alt=""><figcaption>New comparison section ("Why not just use your phone?").</figcaption></figure>
  <figure class="figure"><img class="shot" src="img/mobile-trio.jpg" alt=""><figcaption>Mobile: hero, buy box with thumbnail placeholders, sticky buy bar.</figcaption></figure>
</section>

<section class="part">
  <div class="part__head"><span class="eyebrow">Part 2</span><h1>Offers &amp; conversion research</h1><p>What Pocket and its competitors actually do, what works, and exactly where each tactic now lives in your theme.</p></div>
  <h2 style="margin-top:0">Pocket's offer engine</h2>
  {table(['Tactic', 'What Pocket does', 'Why it works / the catch'], pocket_rows, 'tbl tbl--small')}
  <div class="callout"><b>Read the numbers with care.</b> Pocket's prices and percentages differ across its own pages and third-party sites, and change often. Treat them as patterns, not exact benchmarks, and check heypocket.com before quoting them anywhere.</div>
</section>

<section class="part">
  <h2 style="margin-top:0">What competitors do</h2>
  {table(['Brand', 'Offers and conversion moves', 'Lesson for Alumnus'], competitor_rows, 'tbl tbl--small')}
  <h2>Benchmarks to judge your results</h2>
  {table(['Metric', 'Typical Shopify store', 'Top 20%'], [
      ['Conversion rate', '1.4%', '3.2%+'],
      ['Add-to-cart rate', '4.6%', '7.5%+'],
      ['Checkout completion', '45%', '59%+'],
      ['Mobile vs desktop conversion', '1.2% vs 1.9%', ''],
  ], 'tbl tbl--small')}
  <p class="muted" style="font-size:8.2pt">Littledata figures as quoted in 2026 roundups {src(24)}. Vendor claims put sticky add-to-cart bars at a 10–20% mobile lift; I couldn't verify those against primary data, so test rather than assume.</p>
  <h2>Every tactic, and where it lives now</h2>
  {table(['Tactic', 'Seen at', 'Where in the theme', 'What you set up'], tactic_rows, 'tbl tbl--small')}
</section>

<section class="part">
  <h2 style="margin-top:0">Recommended offer stack for Alumnus</h2>
  <p>Pocket owns founders and executives; Plaud owns professionals. <b>Alumnus can own students and early-career people</b>: the name, "In class" use case, study tips list and a student discount all point there. Build the offer around that.</p>
  {table(['Lever', 'Recommendation', 'Note'], offer_rows, 'tbl tbl--small')}
  <h3>Bundle math (example numbers)</h3>
  <p>With a $139 price and the theme's default tiers: Duo 2 × $139 × 0.90 = <b>$250.20</b> ($125.10 each); Study group 3 × $139 × 0.85 = <b>$354.45</b> ($118.15 each). If your landed cost per unit (product + shipping + fees) were $45, the Duo would keep $160.20 of margin against $94 for a single unit. Swap in your real landed cost before raising the percentages.</p>
  <h2 style="break-before: page; margin-top: 0">Guardrails (read before launch)</h2>
  {table(['Topic', 'What to do'], [[f'<b>{E(t)}</b>', d] for t, d in compliance], 'tbl tbl--small')}
  <p class="muted" style="font-size:8pt">This is practical guidance, not legal advice. When in doubt, ask a lawyer.</p>
</section>

<section class="part">
  <div class="part__head"><span class="eyebrow">Part 3</span><h1>Connecting closer with Shopify</h1><p>The theme uses Shopify's native features wherever possible, so apps and admin settings plug in instead of fighting the design.</p></div>
  <h2 style="margin-top:0">Setup in this order</h2>
  {table(['#', 'Step', 'How'], shopify_rows, 'tbl tbl--small')}
  <div class="callout callout--grey"><b>Your store today.</b> The connected store ("My Store", Basic plan, USD) still lists two streetwear products. Archive them (Products › select › Archive) so they don't appear in search, collections or Google Shopping. I haven't changed anything in the store.</div>
</section>

<section class="part">
  <h2 style="margin-top:0">Native features the theme already uses</h2>
  <ul style="font-size: 8.9pt">
    <li><b>Online Store 2.0 JSON templates and section groups</b>: every section can be added, removed and reordered in the editor. Header and footer live in section groups, as Shopify requires.</li>
    <li><b>Shopify-hosted video</b> settings for every video slot (upload once in Content › Files, pick it in the editor).</li>
    <li><b>Product form + dynamic checkout</b> (Shop Pay express) and the <b>Shop Pay Installments</b> message {src(18)}.</li>
    <li><b>Section Rendering API</b> for the cart drawer: quantities, add-ons and discount codes update without a page reload {src(18)}; discount codes use the cart <code>discount</code> parameter Shopify added to <code>/cart/update.js</code> {src(19)}.</li>
    <li><b>Standard review metafields</b> (<code>reviews.rating</code>, <code>reviews.rating_count</code>): any major reviews app makes the stars live everywhere {src(20)}.</li>
    <li><b>Customer accounts component</b> in the header (Shopify's sign-in sheet with Shop, Google and email) {src(18)}.</li>
    <li><b>Native customer forms</b> for the popup and footer signup: subscribers land in Customers with email consent, ready for Shopify Messaging.</li>
    <li><b>Dynamic sources</b>: spec values can be connected to product metafields in the editor, so specs update from the product.</li>
    <li><b>App blocks</b> in the buy box, reviews and an Apps section, so reviews, bundles or upsell apps drop in without code.</li>
    <li><b>SEO</b>: product structured data, FAQ structured data, Open Graph and X cards, plus your share image (IMG-28).</li>
  </ul>
  <h2>Apps and services worth adding</h2>
  {table(['App / feature', 'What it does', 'Cost', 'Use it for'], apps_rows, 'tbl tbl--small')}
  <p class="muted" style="font-size:8pt">Plan availability per Shopify's Flow page and Collabs listing {src(22)}{src(23)}; Messaging allowance per 2026 guides {src(21)}. Confirm in your admin, since plans change.</p>
</section>

<section class="part">
  <div class="part__head"><span class="eyebrow">Part 4</span><h1>Higgsfield prompt pack</h1><p>One art direction, product accuracy first. Every ID matches a labelled placeholder in the theme.</p></div>
  <h2 style="margin-top:0">Workflow</h2>
  <ol class="steps">
    <li><b>Collect references.</b> Get 3–5 clean photos of the real device (front, back, edge, on a phone) and the cable. Your supplier photos work if you crop out their text.</li>
    <li><b>Make stills first.</b> For product-only shots use <b>Nano Banana Pro</b> with your reference photos attached; it is the best at keeping exact geometry and handling edits. For scenes with people use <b>Soul 2.0</b> (photoreal, editorial), then run a Nano Banana Pro edit with the references to make the device exact {src(16)}.</li>
    <li><b>Animate approved stills.</b> Use image-to-video (<b>Kling 3.0</b> or <b>Seedance 2.0</b>; Veo 3.1 when you need sound). Use one camera move per clip and keep clips to 5–10 seconds {src(17)}.</li>
    <li><b>Check every frame</b> against the references: groove count and spacing, the black strip layout, no logos, hands and fingers.</li>
    <li><b>Export and name files</b> as listed, then upload: theme slots in the editor, product images in Products › Media.</li>
  </ol>
  <div class="callout"><b>Copy-ready prompts.</b> The file <code>alumnus/docs/Higgsfield-Prompts-Copy-Ready.txt</code> has every prompt below with the device description and house style already filled in, so you can paste straight into Higgsfield.</div>
  <div class="callout callout--grey"><b>Model names change fast.</b> Higgsfield adds models monthly. If a newer version of the same model is in the picker (Nano Banana, Soul, Kling, Seedance), use the newest. The prompts work across them.</div>
  <div class="figure two" style="align-items:center">
    <img class="shot" src="img/device-ref.jpg" alt="Supplier device photo" style="max-height:2.6in;object-fit:contain">
    <div>
      <h3 style="margin-top:0">Your device, described</h3>
      <p>Paste this wherever a prompt says <span class="tok">[DEVICE]</span>. It matches your supplier photos; correct anything that differs on your real unit.</p>
      <div class="blocktext"><b>[DEVICE]</b>{E(DEVICE)}</div>
    </div>
  </div>
</section>

<section class="part">
  <div class="blocktext" style="margin-top:0"><b>House style (add to every prompt)</b>{E(STYLE)}</div>
  <div class="two">
    <div class="blocktext"><b>[CAST]</b>{E(CAST)}</div>
    <div class="blocktext"><b>Negative prompt (when the model has a field for it)</b>{E(NEGATIVE)}</div>
  </div>
  <h2>Asset map</h2>
  <p class="muted">P1 = needed to launch · P2 = soon after · P3 = nice to have. "Real" = must be genuine, not generated. IMG-14 to IMG-16 are intentionally skipped: those slots take real app screenshots (APP-01 to APP-03).</p>
  {table(['ID', 'Asset', 'Ratio', 'Where it goes', 'Priority'], asset_map_rows, 'tbl tbl--small')}
</section>

<section class="part">
  <h2 style="margin-top:0">Videos</h2>
  {film}
  {clips}
</section>

<section>
  <h2>Images</h2>
  {cards}
</section>

<section>
  <h2>Assets that must be real (no Higgsfield)</h2>
  {table(['ID', 'What', 'How to get it'], [
      ['<b>APP-01–03</b>', 'App screenshots: summary, mind map, to-do list', 'Record a 5-minute sample (read an article aloud), let the app generate each view, screenshot on a clean phone, crop to 4:3. These also go on the phone screen in IMG-13 and shot 6 of VID-01.'],
      ['<b>LOGO-01–05</b>', 'Logo bar', 'Only schools, companies or press where it\'s true. Until then, hide the section or switch it to "As seen in" when you get press.'],
      ['<b>Reviews</b>', 'Review cards and Reviews section', 'Real reviews only. A reviews app sends requests after delivery and imports photos and videos.'],
      ['<b>UGC videos</b>', 'Replace VID-02–04 over time', 'Seed devices to student creators through Shopify Collabs; use their clips with permission, real names and roles, and remove the "Demo footage" note.'],
  ], 'tbl tbl--small')}
  <h2>Bonus: three ad concepts for TikTok and Reels</h2>
  <p class="muted">These aren't for the website. TikTok requires an AI label on ads with realistic AI people, voices or scenes {src(15)}. Best practice: AI for b-roll and product shots, real creators for faces.</p>
  {ads}
</section>

<section class="part">
  <div class="part__head"><span class="eyebrow">Part 5</span><h1>Launch checklist</h1><p>Every [bracket] in the theme, plus the settings that make the offers work.</p></div>
  <h3 style="margin-top:0">Facts to confirm with your supplier</h3>
  <ul class="checklist">
    <li>Thickness [3] mm and weight [X] g</li><li>Battery [X] hrs recording, [X] days standby</li><li>Storage [X] GB</li><li>Languages [X]</li>
    <li>iPhone and Android support; MagSafe or included magnetic ring</li><li>What's in the box</li><li>Free app limits ([X] minutes) and whether a Pro plan exists ([$X]/mo)</li>
    <li>Encryption, storage location, AI training use</li><li>Export formats ([More: confirm])</li><li>Which control starts recording (for IMG-09)</li>
  </ul>
  <h3>Your business decisions</h3>
  <ul class="checklist">
    <li>Sale % in the announcement bar, popup, teaser and closing offer ([X]%)</li><li>Sale end date (Theme settings › Product and offer)</li>
    <li>Bundle tier percentages (Buy box) = your automatic discounts</li><li>Welcome code (popup) created in Discounts</li>
    <li>Return window [30] days and warranty [1] year (announcement, hero, buy box, guarantee, FAQ, closing offer)</li>
    <li>Shipping time [X–X] business days (buy box, guarantee, FAQ)</li><li>Countries you ship to (FAQ)</li><li>Student discount: yes or no (FAQ)</li>
    <li>Teams plan: contact page or remove</li><li>Cart add-on product (Theme settings › Cart)</li>
  </ul>
  <h3>Social proof (real only)</h3>
  <ul class="checklist">
    <li>Hero, buy box and reviews rating [X.X] and count [X] (automatic once a reviews app is installed)</li>
    <li>"[X]+ students, interns and founders" and "[X]+ happy customers": real numbers or rewrite the headings</li>
    <li>Review cards and review blocks: real reviews or remove</li><li>Logo bar: real logos or hide</li>
  </ul>
  <h3>Before you publish</h3>
  <ul class="checklist">
    <li>Archive the old streetwear products</li><li>Upload P1 assets; turn off "Show placeholder labels" if any slot is still empty</li>
    <li>Footer: TikTok and Instagram links (replace "yourhandle"), App Store / Google Play links or hide badges</li>
    <li>Policies: refund, shipping, privacy, terms</li><li>Place a test order with each bundle tier and the welcome code</li>
    <li>Check the site on your phone: popup, sticky bar, cart drawer</li><li>Install reviews app and sales channel pixels (TikTok, Meta, Google)</li>
  </ul>
</section>

<section class="part">
  <div class="part__head"><span class="eyebrow">Sources</span><h1>Sources</h1><p>Research done October 2026. Prices and policies change; recheck before quoting.</p></div>
  <ol class="sources">
    {''.join(f'<li>[{n}] {E(t)} · <a href="{E(u)}">{E(u)}</a></li>' for n, t, u in sources)}
  </ol>
</section>
"""
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Alumnus · Website playbook & Higgsfield prompt pack</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{body}</body></html>"""
    OUT.write_text(doc)
    print(f'wrote {OUT} ({len(doc)} bytes), {len(ASSETS)} image/video cards, {len(CLIPS)} clips, film shots {len(VIDEO_FILM["shots"])}')


DEVICE_INLINE = 'the Alumnus AI voice recorder (' + DEVICE.split(': ', 1)[1].replace('no logos or text on the device', 'no logos or text on it') + ')'


def expand(text):
    return text.replace('[DEVICE]', DEVICE_INLINE).replace('[CAST]', CAST[0].upper() + CAST[1:])


def build_copy_ready():
    """Plain-text prompts with [DEVICE] and [CAST] filled in, ready to paste into Higgsfield."""
    line = '=' * 78
    out = ['ALUMNUS · HIGGSFIELD PROMPTS (COPY-READY)',
           'Every prompt below already includes the device description. Attach 2-3 photos of your real',
           'device as reference images whenever the device appears. IDs match the labels in the theme.', '',
           'NEGATIVE PROMPT (paste into the negative field when the model has one):', NEGATIVE, '']
    out += [line, 'VID-01 · ' + VIDEO_FILM['name'], VIDEO_FILM['where'], VIDEO_FILM['spec'], line]
    for n, t, d, start, motion in VIDEO_FILM['shots']:
        out += [f'Shot {n} · {t} · {d}', 'START FRAME (image): ' + expand(start) + ' Style: ' + STYLE + '.', 'MOTION (video): ' + expand(motion), '']
    out += ['VOICE-OVER: ' + VIDEO_FILM['vo'], '']
    for c in CLIPS:
        out += [line, f"{c['id']} · {c['name']}", c['where'], '9:16 vertical · 1080 x 1920 · 15-20 s', 'Captions: ' + c['caption'], line]
        for n, t, start, motion in c['shots']:
            out += [f'Shot {n} · {t}', 'START FRAME (image): ' + expand(start) + ' Style: ' + STYLE + '.', 'MOTION (video): ' + expand(motion), '']
    for a in ASSETS:
        out += [line, f"{a['id']} · {a['name']} · {a['priority']}", 'Where: ' + a['where'],
                f"Format: {a['ratio']} · {a['size']} · save as {a['file']}", 'Model: ' + a['model'], line]
        prompt = expand(a['prompt'])
        if a['kind'] == 'image':
            prompt += ' Style: ' + STYLE + '.'
        out += [prompt, '']
        for c in a.get('checks', []):
            out.append('  [ ] ' + c)
        out.append('')
    for i, t, d, pr in ADS:
        out += [line, f'{i} · {t} (ads, label as AI-generated)', d, line, expand(pr), '']
    target = HERE.parent / 'Higgsfield-Prompts-Copy-Ready.txt'
    target.write_text('\n'.join(out))
    print(f'wrote {target}')


if __name__ == '__main__':
    build()
    build_copy_ready()
