// gta6-meme-x-01 — hand in the X post's address.
//
// The meme itself lives in assets/meme.png and is posted to X by hand; the
// post's address goes in POST.json at this repository's root. This program
// is the whole graded entry: it copies POST.json into the output directory
// so the house can read it. It does nothing else — no network, no clock,
// no files outside the repository — and it prints nothing on success.
//
// The grader runs it as an unprivileged user on a read-only filesystem
// with an empty writable output directory, so this program only ever
// writes inside MAKEFUN_OUTPUT_DIR and never deletes anything.
import { copyFileSync, existsSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? ".";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";

// Resolve the path so error messages name the exact file that was missing,
// even when MAKEFUN_BOT_DIR is relative (the grader runs from elsewhere).
const source = resolve(botDir, "POST.json");
if (!existsSync(source)) {
  console.error(`POST.json not found: ${source}`);
  process.exit(1);
}

// Sanity-check the hand-in before copying: it must be a JSON object with
// a url string naming an X post. A malformed file is a failed entry, so
// fail loudly here instead of handing in garbage.
const parsed: unknown = JSON.parse(readFileSync(source, "utf8"));
if (
  typeof parsed !== "object" ||
  parsed === null ||
  typeof (parsed as { url?: unknown }).url !== "string"
) {
  console.error("POST.json must be an object with a string url field");
  process.exit(1);
}

copyFileSync(source, join(outDir, "POST.json"));
