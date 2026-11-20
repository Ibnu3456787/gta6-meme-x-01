# LEONIDA LOTTO — a GTA 6 meme for make.fun

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/Ibnu3456787/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/Ibnu3456787/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

An entry for make.fun's **"Post a GTA 6 meme on X"** bounty ($500 in USDC):
a lottery scratch-off ticket from Leonida whose winning numbers are the
thirteen-year wait itself — **13 YEARS · 2 DELAYS · 214 GB · 19 NOV · 6 GTA VI** —
sealed with make.fun's ghost and paid by an AI agent.

![The meme](assets/meme.png)

make.fun is a site where people and their AI agents build things, enter them
in paid competitions (bounties) and earn real money when they win:
https://make.fun/ — bounty page:
https://make.fun/bounty/gta6-meme-x-01

## The joke

> **WAITED 13 YEARS FOR GTA 6 — MY NUMBERS FINALLY CAME UP!**

GTA V came out in September 2013. GTA VI finally lands 19 November 2026 —
after two delays and a 214 GB download. The meme turns the wait into a
lottery ticket: every "winning number" is a fact of the wait, and the prize
is the game itself. The ticket is drawn in Vice City, Leonida; make.fun's
ghost seals it as the winner, and the red pill says what happened next:
**PAID BY MY AI AGENT**. See [MEME.md](MEME.md) for the full rationale and
the exact post text.

## The post

The meme is posted on X from the public account @JagatAirdrop with the
meme as its first picture and the post text from [MEME.md](MEME.md) (make.fun
link, @makefunai tag, play code). The post stays public until the results
are out. Its address goes in [POST.json](POST.json):

```json
{"url": "https://x.com/<handle>/status/<id>"}
```

## What this repository is

- `main.ts` — the graded program: it copies `POST.json` to
  `/output/POST.json`, which is all the program has to do. No network, no
  clock, no files outside the repository; it never deletes anything.
- `POST.json` — the post's address (placeholder until the post is live).
- `assets/meme.png` — the meme picture (1024×1024), built by
  `tools/build_meme.py` from `assets/bg-leonida.webp` (AI-made Leonida
  sunset, no text) and `assets/ghost-mark.png` (make.fun's official ghost
  mark, from https://make.fun/press/). Rebuilding the meme is
  deterministic: the same bytes every run.
- `tools/build_meme.py` — the local build script (PIL). Not part of the
  graded program; the grader only runs `main.ts`.
- `MEME.md` — the meme's rationale, the exact X post text and the posting
  instructions.

## Run it locally

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`out/POST.json` is then byte for byte this directory's `POST.json`.

## License

MIT — see [LICENSE](LICENSE).
