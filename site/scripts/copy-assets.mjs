// Runs before dev/build: self-hosts Pyodide and copies the remind package for in-browser checkpoints.
import fs from "node:fs";
import path from "node:path";
const root = path.resolve(import.meta.dirname, "..");
const pyo = path.join(root, "node_modules", "pyodide");
const out = path.join(root, "public", "pyodide");
fs.mkdirSync(out, { recursive: true });
for (const f of ["pyodide.js", "pyodide.mjs", "pyodide.asm.mjs", "pyodide.asm.wasm", "python_stdlib.zip", "pyodide-lock.json"]) {
  fs.copyFileSync(path.join(pyo, f), path.join(out, f));
}
// remind package (pure python) -> public/py/remind/...
const src = path.resolve(root, "..", "remind");
const dst = path.join(root, "public", "py");
const files = [];
function walk(d, rel = "") {
  for (const e of fs.readdirSync(d, { withFileTypes: true })) {
    if (e.name === "__pycache__") continue;
    const r = path.join(rel, e.name);
    if (e.isDirectory()) walk(path.join(d, e.name), r);
    else if (e.name.endsWith(".py") && !["llm.py", "tutor.py"].includes(e.name)) {
      fs.mkdirSync(path.join(dst, "remind", rel), { recursive: true });
      fs.copyFileSync(path.join(d, e.name), path.join(dst, "remind", r));
      files.push("remind/" + r.split(path.sep).join("/"));
    }
  }
}
if (fs.existsSync(src)) { walk(src); fs.writeFileSync(path.join(dst, "manifest.json"), JSON.stringify(files)); }
// assessment briefs -> content/assessments (committed copies, so the site builds even without the parent repo)
const ass = path.resolve(root, "..", "docs", "assessments");
if (fs.existsSync(ass)) {
  fs.mkdirSync(path.join(root, "content", "assessments"), { recursive: true });
  for (const f of fs.readdirSync(ass)) fs.copyFileSync(path.join(ass, f), path.join(root, "content", "assessments", f));
}
console.log(`copied pyodide + ${files.length} remind files`);
