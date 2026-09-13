#!/usr/bin/env node
// Patterns are written so they never match this file's own source.
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { extname } from "node:path";

const scanHistory = process.argv.includes("--history");
const findings = [];
const report = (where, why) => findings.push(`${where}: ${why}`);
const git = (args, input) => execFileSync("git", args, { input, maxBuffer: 1 << 30 });

const FORBIDDEN_PATHS = [
  [/(^|\/)\.vscode\//, "VS Code workspace config (can auto-run code when the folder is opened)"],
  [/(^|\/)(package-lock\.json|npm-shrinkwrap\.json)$/, "npm lockfile (this repo uses yarn)"],
  [/\.(bat|cmd|ps1|vbs|exe|dll|scr|jar)$/i, "executable/script type with no place in this repo"],
];

const CONTENT_IOCS = [
  [/global\.i\s*=\s*['"]/, "marker from the fake-font trojan payload"],
  [/"runOn"\s*:\s*"folder[O]pen"/, "task that auto-runs when the folder is opened"],
  [/task\.allowAutomaticTasks/, "setting that lets VS Code run tasks without asking"],
  [/eth-mainnet\.public\.blastapi\.io|ethereum-rpc\.publicnode\.com|eth\.drpc\.org|1rpc\.io\/eth/, "Ethereum RPC endpoint the trojan uses to fetch its next stage"],
  [/[\t ]{200,}\S/, "code hidden after a long run of whitespace"],
];

const ascii = (b, from, to) => b.toString("latin1", from, to);
const MAGIC = {
  ".woff2": (b) => ascii(b, 0, 4) === "wOF2",
  ".woff": (b) => ascii(b, 0, 4) === "wOFF",
  ".ttf": (b) => ["\0\x01\0\0", "true"].includes(ascii(b, 0, 4)),
  ".otf": (b) => ascii(b, 0, 4) === "OTTO",
  ".eot": (b) => b[34] === 0x4c && b[35] === 0x50,
  ".png": (b) => ascii(b, 1, 4) === "PNG",
  ".jpg": (b) => b[0] === 0xff && b[1] === 0xd8,
  ".jpeg": (b) => b[0] === 0xff && b[1] === 0xd8,
  ".gif": (b) => ascii(b, 0, 4) === "GIF8",
  ".webp": (b) => ascii(b, 8, 12) === "WEBP",
  ".ico": (b) => b[0] === 0 && b[1] === 0 && b[2] === 1 && b[3] === 0,
};

function inspect(where, path, buf) {
  for (const [re, why] of FORBIDDEN_PATHS) if (re.test(path)) report(where, why);

  const magic = MAGIC[extname(path).toLowerCase()];
  if (magic) {
    if (magic(buf)) return;
    report(where, `not a real ${extname(path)} file (disguised content)`);
  }
  if (buf.length > 5_000_000 || buf.includes(0)) return;

  const text = buf.toString("utf8");
  for (const [re, why] of CONTENT_IOCS) if (re.test(text)) report(where, why);
  if ((text.match(/_0x[0-9a-f]{4,}/g) ?? []).length >= 20) report(where, "obfuscated JavaScript");
  if (extname(path).toLowerCase() === ".svg" && /<script|javascript:|<foreignObject|\son[a-z]+\s*=/i.test(text))
    report(where, "SVG with embedded script or event handler");

  if (path === "package.json" || path.endsWith("/package.json")) {
    try {
      const scripts = JSON.parse(text).scripts ?? {};
      for (const hook of ["preinstall", "install", "postinstall", "prepare"])
        if (scripts[hook]) report(where, `"${hook}" lifecycle script runs code on install`);
    } catch {
      report(where, "package.json is not valid JSON");
    }
  }
}

const files = git(["ls-files", "--cached", "--others", "--exclude-standard", "-z"])
  .toString()
  .split("\0")
  .filter(Boolean);

for (const file of files) {
  let buf;
  try {
    buf = readFileSync(file);
  } catch {
    continue;
  }
  inspect(file, file, buf);
}

if (scanHistory) {
  const log = git(["log", "--all", "--format=%h%x09%an%x09%cn%x09%ci"]).toString().trim();
  for (const line of log ? log.split("\n") : []) {
    const [sha, author, committer, date] = line.split("\t");
    if ([author, committer].includes("github-actions[bot]") && !date.endsWith("+0000"))
      report(`commit ${sha}`, "claims to be github-actions[bot] but was committed outside GitHub Actions (forged)");
  }

  const entries = git(["rev-list", "--objects", "--all"])
    .toString()
    .split("\n")
    .map((line) => line.split(/ (.*)/s))
    .filter(([sha, path]) => sha && path);

  if (entries.length) {
    const out = git(["cat-file", "--batch"], entries.map(([sha]) => sha).join("\n") + "\n");
    let pos = 0;
    for (const [sha, path] of entries) {
      const headerEnd = out.indexOf(10, pos);
      const [, type, size] = ascii(out, pos, headerEnd).split(" ");
      const body = out.subarray(headerEnd + 1, headerEnd + 1 + Number(size));
      pos = headerEnd + 1 + Number(size) + 1;
      if (type === "blob") inspect(`history ${sha.slice(0, 7)} ${path}`, path, body);
    }
  }
}

if (findings.length) {
  console.error(`Security scan FAILED with ${findings.length} finding(s):`);
  for (const finding of [...new Set(findings)]) console.error(`  - ${finding}`);
  process.exit(1);
}
console.log(`Security scan passed: ${files.length} files${scanHistory ? " plus full git history" : ""}.`);
