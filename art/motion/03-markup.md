# Motion: LTX-2.5 rules for the Hall's clips: Markup

Part 3 of 4 of [`motion.md`](../motion.md).

## Markup

The website builds the component (W3). This sketch shows the rules in place. The still stays in the page as the text alternative, and the clip sits over it.

```html
<figure class="hall-clip" data-clip>
  <img src="hall.webp" alt="{the still's alt text}" width="1568" height="672">
  <video muted loop playsinline preload="none" poster="hall.webp" aria-hidden="true" hidden>
    <source data-src="hall.webm" type="video/webm">
    <source data-src="hall.mp4" type="video/mp4">
  </video>
  <button type="button" class="hall-clip__pause" aria-pressed="false" hidden>Pause motion</button>
  <figcaption class="hall-clip__label">AI-made</figcaption>
</figure>
<script>
  // The clip loads only when the reader has no reduced-motion preference (rule 4).
  if (matchMedia('(prefers-reduced-motion: no-preference)').matches) {
    for (const fig of document.querySelectorAll('[data-clip]')) {
      const video = fig.querySelector('video');
      const button = fig.querySelector('button');
      for (const s of video.querySelectorAll('source')) s.src = s.dataset.src;
      video.autoplay = true;
      video.load();
      video.hidden = false;
      button.hidden = false;
      button.addEventListener('click', () => {
        const paused = button.getAttribute('aria-pressed') !== 'true';
        if (paused) video.pause(); else video.play();
        button.setAttribute('aria-pressed', String(paused));
      });
    }
  }
</script>
```

```css
.hall-clip { position: relative; }
.hall-clip video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.hall-clip__pause { position: absolute; right: 0.5rem; bottom: 0.5rem; min-width: 24px; min-height: 24px; }
```

The pause button is a real button, reachable by keyboard, at least 24 by 24 CSS pixels (WCAG 2.5.8). Its label stays "Pause motion"; `aria-pressed` says whether motion is paused.

## Runs and records

- **Lane.** Clips run on the $0 lanes in `art/LICENSES.md` (decision 31). Each batch waits for Paul's yes in chat, with the lane's balance read before and after (`~/.claude/rules/compute.md`).
- **Never on this Mac.** LTX-2.5 needs an NVIDIA GPU with at least 32 GB of memory (research digest), and the house rule bans local video.
- **Queue.** Every planned clip is in `art/render-queue.yaml`, blocked on Paul's queue items 1 and 2.
- **Record.** Each clip keeps a provenance record beside it. It names the source still, the model, the template, the prompt, the seed, the frame count and the CFG. It also records the date, who approved the run, and the credit balance before and after.
- **Refine and matte.** The LTX-2.5 IC-LoRAs for refining detail or cutting an alpha matte run under the same rules and the same license (`art/LICENSES.md`).
