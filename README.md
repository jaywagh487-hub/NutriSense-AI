# NutriSense AI — v2 Upgrade Notes

## How to run
```
pip install flask
python app.py
```
Then open http://127.0.0.1:5000 in your browser.

## What's new in this version

### 1. New feature: Vitamin & Mineral Encyclopedia (`/nutrients`)
- 15 nutrients covered: Vitamins A, B1, B3, B6, B12, C, D, E, K + Calcium, Iron,
  Zinc, Magnesium, Potassium, Iodine.
- Each entry has: RDA (recommended daily allowance), a plain-English explanation,
  deficiency warning signs, top Indian food sources, an absorption tip, an
  embedded YouTube video, and a link to an official source (NIH / WHO / ICMR).
- Live search box and Vitamins/Minerals filter chips.
- Click any card to open a detail panel (modal) with the full write-up.

### 2. New feature: Video & Official Resources page (`/resources`)
- Curated YouTube videos grouped by topic (Iron, Calcium, Vitamin D, B12,
  Protein, Yoga/Wellness).
- A grid of official/government health links: WHO, ICMR-NIN, NIH Office of
  Dietary Supplements, India's National Health Portal, FSSAI, and the Academy
  of Nutrition and Dietetics.
- Resource links/snippets were also added directly on the Step Tracker,
  Symptom Checker, Deficiency Guide, and Result pages so users hit relevant
  videos/sources without leaving their current task.

### 3. Visual redesign
- New "botanical/Ayurvedic" color identity layered on top of the original
  green palette: turmeric gold + clay terracotta accents, warm ivory
  backgrounds, and a serif display font (Fraunces) paired with Inter for body
  text.
- Rebuilt homepage hero with an animated "nutrient orbit" signature visual
  (vitamin icons orbiting a central DNA icon), animated gradient blobs,
  a botanical line-texture background, and a scroll cue.
- New homepage sections: feature grid, animated counting stat band, "how it
  works" steps, feature pill row, and a closing call-to-action band.

### 4. Animation system (new in `static/script.js` + `static/style.css`)
- Scroll-reveal: sections fade/slide into view as the user scrolls
  (IntersectionObserver-based, respects `prefers-reduced-motion`).
- Animated count-up numbers for stats.
- Subtle 3D tilt-on-hover for feature/deficiency cards.
- Parallax drift on background gradient blobs.
- All existing animations (progress bars, nav dropdown, card slide-ups) were
  preserved.

### 5. Data/content additions
- `app.py` now contains a `nutrient_db` list with the full vitamin/mineral
  encyclopedia data (RDA, sources, tips, videos, official links), served to
  `/nutrients` both as Jinja-rendered cards and as a JSON blob for the
  client-side search/filter/modal logic.
- Existing deficiency database, BMI calculator, weight plans, hair/skin care,
  yoga, workout, seasonal guide, protein calculator, immunity recipes, step
  tracker, and feedback form are all unchanged in logic — only visually
  refreshed with the new design tokens and animation classes.

## Notes
- All new YouTube embeds use the standard `https://www.youtube.com/embed/...`
  format already used elsewhere in the app — swap any video ID if you want to
  point to different videos.
- Official links (WHO, ICMR-NIN, NIH, NHP, FSSAI) are real, currently active
  government/institutional URLs.
- No external API keys are required — everything runs from the bundled Flask
  app and static data.
