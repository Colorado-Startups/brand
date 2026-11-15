# guide

| Item | Value |
|---|---|
| What | The interactive brand guide (owner S8): 14 sections, each a visual with a control (decision 47) |
| Live | [colorado-startups.github.io/brand](https://colorado-startups.github.io/brand/), public (decision 28) |
| Data | `dist/brand.json`, built by `tools/build_guide_data.py` from `data/` and the other sources it names |
| Files | `public/index.html`, `guide.css`, `guide.js` (no libraries), `tokens.css`, `fonts/` (Aileron, CC0) |
| Built by | `.github/workflows/pages.yml`: `public/` at `/`, `dist/brand.json`, `dist/social/` and `dist/places/` at `/dist/`, the Quality and Process pages under `/quality/` |
| Goals | At most 900 visible words, a visual and a control in every section, readable at 375 px and in both themes (decision 15) |
| Words on load | 853, the `document.body.innerText` word count at 375 px and 1024 px, both themes (decision 51). Detail sits behind controls, so a closed panel adds no words |
| Optional `logo` key | Name shows a tier only when `dist/brand.json` has one: `{"emblem": {...}, "wordmark": {...}, "icon": {...}}`, or a list of rows with `id`. Each row has `files` (paths from `dist/`, such as `logo/emblem-512.png`, where decision 50 put them; a bare name means `logo/`), and optional `use` and `size`. A wordmark file named with `white` shows on dark grounds, one with `blue` on light. Without the key, the type specimen shows |
| Optional `templates` key | Files lists Applications first when it is present: a list (or `{"items": [...]}`) of rows with `name`, `file` or `files` (paths from `dist/`, such as `templates/slide.png`), `size` (text or `{width, height}`) and `use` |
| Never | On a coloradostartups.org address (decision 18) |
