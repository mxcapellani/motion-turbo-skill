r"""Busca prompts de vídeo em código nos dois pacotes locais.

Uso:
  python buscar.py <termos...> [--cat motion|3d|explainer|interactive] [--tag threejs] [--n 10]
  python buscar.py --show <slug>      # mostra o prompt completo

Pacotes (em {{REPOS}}):
  awesome-opus5-5-videos/data/videos.json  (~700 prompts)
  opus-video-prompts/cases.json + prompts/*.md  (54 casos)
"""
import argparse
import json
import sys
from pathlib import Path

BASE = Path(r"{{REPOS}}")
AW = BASE / "awesome-opus5-5-videos" / "data" / "videos.json"
OV = BASE / "opus-video-prompts"

sys.stdout.reconfigure(encoding="utf-8")


def carregar():
    itens = []
    for x in json.loads(AW.read_text(encoding="utf-8")):
        itens.append({
            "slug": x["slug"], "fonte": "awesome", "cat": x.get("category", ""),
            "tags": x.get("tech_tags", []), "titulo": x["prompt"][:90].replace("\n", " "),
            "texto": x["prompt"], "url": x.get("post_url", ""),
        })
    for md in sorted((OV / "prompts").glob("*.md")):
        t = md.read_text(encoding="utf-8")
        itens.append({
            "slug": md.stem, "fonte": "opus-video-prompts", "cat": "", "tags": [],
            "titulo": t.splitlines()[0].lstrip("# ").strip(), "texto": t, "url": str(md),
        })
    return itens


def main():
    p = argparse.ArgumentParser()
    p.add_argument("termos", nargs="*")
    p.add_argument("--cat")
    p.add_argument("--tag")
    p.add_argument("--n", type=int, default=10)
    p.add_argument("--show")
    a = p.parse_args()
    itens = carregar()

    if a.show:
        for i in itens:
            if i["slug"] == a.show:
                print(f"[{i['fonte']}] {i['slug']}  {i['url']}\n")
                print(i["texto"])
                return
        print("slug não encontrado")
        return

    res = []
    for i in itens:
        if a.cat and i["cat"] != a.cat:
            continue
        if a.tag and a.tag not in i["tags"]:
            continue
        alvo = (i["texto"] + " " + i["titulo"]).lower()
        score = sum(alvo.count(t.lower()) for t in a.termos) if a.termos else 1
        if score:
            res.append((score, i))
    res.sort(key=lambda r: -r[0])
    print(f"{len(res)} resultados (mostrando {min(a.n, len(res))})")
    for s, i in res[: a.n]:
        tags = ",".join(i["tags"])
        print(f"- {i['slug']}  [{i['fonte']} {i['cat']} {tags}]  {i['titulo']}")


if __name__ == "__main__":
    main()
