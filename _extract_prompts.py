"""Extract all prompt blocks from session HTML files."""
import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent / "index"

SESSION_TITLES = {
    0: "Sesión 0 · Inaugural · Mapa del curso",
    1: "Sesión 1 · IA generativa en la investigación científica",
    2: "Sesión 2 · Ética y prompting con rigor",
    3: "Sesión 3 · Problema y objetivos",
    4: "Sesión 4 · Marco teórico y método",
    5: "Sesión 5 · Búsqueda sistemática",
    6: "Sesión 6 · Síntesis de literatura",
    7: "Sesión 7 · Redacción de la revisión",
    8: "Sesión 8 · Estructura IMRyD",
    9: "Sesión 9 · Datos con Colab + Gemini",
    10: "Sesión 10 · Publicación y envío",
}

SESSION_COLORS = {
    0: "#ff6b3d", 1: "#ff6b3d", 2: "#3dd6c4",
    3: "#e8b04b", 4: "#8a7dff",
    5: "#36b3f0", 6: "#3ddc97", 7: "#ff7e5f",
    8: "#7c8cff", 9: "#f0a830", 10: "#19c2a8",
}


def find_blocks(text: str) -> list[str]:
    """Find every div whose class contains 'promptbox' or 'promptbig'."""
    blocks = []
    # Iterate over opening tags
    for m in re.finditer(r'<div\s+class="([^"]*?(?:promptbox|promptbig)[^"]*?)"[^>]*>', text):
        start = m.end()
        # walk forward balancing <div> ... </div>
        depth = 1
        i = start
        while i < len(text) and depth > 0:
            nxt_open = text.find("<div", i)
            nxt_close = text.find("</div>", i)
            if nxt_close == -1:
                break
            if nxt_open != -1 and nxt_open < nxt_close:
                depth += 1
                i = nxt_open + 4
            else:
                depth -= 1
                if depth == 0:
                    blocks.append(text[start:nxt_close])
                    break
                i = nxt_close + 6
    return blocks


def session_number(filename: str) -> int:
    m = re.search(r"Sesion(\d+)", filename)
    return int(m.group(1)) if m else -1


def main() -> int:
    all_prompts = []
    for f in sorted(glob.glob(str(ROOT / "Sesion*.html"))):
        path = Path(f)
        n = session_number(path.name)
        text = path.read_text(encoding="utf-8")
        blocks = find_blocks(text)
        for i, b in enumerate(blocks, 1):
            all_prompts.append({
                "session": n,
                "session_title": SESSION_TITLES.get(n, path.name),
                "color": SESSION_COLORS.get(n, "#ff6b3d"),
                "index": i,
                "html": b.strip(),
            })
    out = ROOT.parent / "_prompts.json"
    out.write_text(json.dumps(all_prompts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Extracted {len(all_prompts)} prompts -> {out}")
    by_session = {}
    for p in all_prompts:
        by_session.setdefault(p["session"], 0)
        by_session[p["session"]] += 1
    for s in sorted(by_session):
        print(f"  S{s}: {by_session[s]} prompts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
