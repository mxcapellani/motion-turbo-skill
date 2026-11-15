r"""Motion Turbo: verificar, instalar as skills auxiliares (sem sobrescrever) e mostrar sugestões em imagem.

  python motion_turbo.py verificar [--repos PASTA]
      Confere cada peça e diz OK / FALTA / AVISO. Não altera nada.

  python motion_turbo.py instalar-modelos --repos PASTA
      Cria em ~/.claude/skills as 3 skills auxiliares (claude-animation-base, video-prompts, r3f-fisica-pos)
      SÓ se ainda não existirem. Se existirem iguais: pula. Se existirem diferentes: NÃO mexe, salva a versão
      nova em <pacote>/saida/ para comparação. Também grava ~/.claude/motion-turbo.json se ainda não existir.

  python motion_turbo.py mostrar --estilos art-deco whiteboard --ferramentas shotcraft clawd [--saida arq.jpg]
      Monta uma imagem com as opções sugeridas (pôster do estilo do Lemo ou imagem da ferramenta) para mostrar
      ao usuário. Lista de estilos: estilos.json. Ferramentas: ver FERRAMENTAS abaixo.
"""
import argparse
import filecmp
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

PACOTE = Path(__file__).resolve().parent
HOME = Path.home()
SKILLS = HOME / ".claude" / "skills"
CONFIG = HOME / ".claude" / "motion-turbo.json"
REPOS_PADRAO = HOME / "motion-turbo" / "repos"
REPOS_CLONE = {
    "ClaudeAnimationBase": "https://github.com/JohnHeibel/ClaudeAnimationBase.git",
    "awesome-opus5-5-videos": "https://github.com/yihui-dev/awesome-opus5-5-videos.git",
    "opus-video-prompts": "https://github.com/joeseesun/opus-video-prompts.git",
}
MODELOS = ["claude-animation-base", "video-prompts", "r3f-fisica-pos"]
FERRAMENTAS = {
    "lemo": ("01-lemo-opuscar.jpg", "Lemo Opuscar", "99 estilos de filme em código"),
    "threejs": ("02-threejs.jpg", "Three.js", "gráficos e cenas 3D"),
    "pixelfx": ("03-pixelfx.jpg", "PixelFX", "efeitos em pixel art"),
    "blender": ("04-blender-mcp.jpg", "Blender MCP", "cena 3D realista no Blender"),
    "prompts": ("05-prompt-packs.jpg", "Prompt packs", "~750 prompts testados"),
    "clawd": ("06-claude-animation-base.jpg", "Claude Animation Base", "mascote pintado à mão"),
    "rapier": ("07-react-rapier.jpg", "React Rapier", "física real (dominó, queda)"),
    "postprocessing": ("08-react-postprocessing.jpg", "React Postprocessing", "brilho, grão, glitch"),
    "librosa": ("09-librosa.jpg", "librosa", "cortes na batida da música"),
    "shotcraft": ("10-video-shotcraft.jpg", "Video ShotCraft", "promo de produto/app"),
}
POSTER_URL = "https://raw.githubusercontent.com/lemomo-ai/lemo-opuscar/main/styles/{slug}/poster.jpg"


# ---------- utilidades ----------
def rodar(cmd, timeout=90):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace",
                           shell=isinstance(cmd, str))
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:  # comando não existe, timeout etc.
        return 127, str(e)


def tem(cmd):
    return shutil.which(cmd) is not None


def repos_atual(arg):
    if arg:
        return Path(arg).expanduser()
    if CONFIG.exists():
        try:
            return Path(json.loads(CONFIG.read_text(encoding="utf-8"))["repos"])
        except Exception:
            pass
    return REPOS_PADRAO


def posix(p: Path) -> str:
    s = str(p)
    if len(s) > 1 and s[1] == ":":  # C:\x\y -> /c/x/y (Git Bash)
        return "/" + s[0].lower() + s[2:].replace("\\", "/")
    return s.replace("\\", "/")


def renderizar(texto, repos: Path):
    return texto.replace("{{REPOS_POSIX}}", posix(repos)).replace("{{REPOS}}", str(repos))


def arquivos_modelo(nome, repos):
    """{nome_final: conteúdo} de uma skill auxiliar já com o caminho dos repos."""
    out = {}
    for f in sorted((PACOTE / "modelos" / nome).iterdir()):
        if f.is_file():
            final = f.name.replace(".template", "")
            out[final] = renderizar(f.read_text(encoding="utf-8"), repos)
    return out


# ---------- verificar ----------
def verificar(a):
    repos = repos_atual(a.repos)
    linhas = []

    def add(status, nome, detalhe, como=""):
        linhas.append((status, nome, detalhe, como))

    # base
    for cmd, nome, obrig in [("git", "git", True), ("node", "Node.js 20+", True), ("npm", "npm", True),
                             ("ffmpeg", "ffmpeg", True), ("claude", "Claude Code CLI", True),
                             ("uvx", "uv/uvx (Blender MCP)", False)]:
        ok = tem(cmd)
        det = ""
        if ok and cmd == "node":
            _, v = rodar(["node", "-v"]); det = v.strip()
            try:
                if int(det.lstrip("v").split(".")[0]) < 20:
                    ok = False; det += " (precisa 20+)"
            except Exception:
                pass
        add("OK" if ok else ("FALTA" if obrig else "AVISO"), nome, det or ("encontrado" if ok else "não encontrado"))
    add("OK" if sys.version_info >= (3, 10) else "AVISO", "Python", sys.version.split()[0])
    try:
        import PIL  # noqa: F401
        add("OK", "Pillow (imagens das sugestões)", "instalado")
    except Exception:
        add("AVISO", "Pillow (imagens das sugestões)", "não instalado: o comando 'mostrar' não funciona",
            f'"{sys.executable}" -m pip install pillow')

    # plugins e skills
    _, plugins = rodar(["claude", "plugin", "list"])
    lemo = "lemo-opuscar@" in plugins or (SKILLS / "lemo-opuscar").exists()
    add("OK" if lemo else "FALTA", "Lemo Opuscar (plugin)", "instalado" if lemo else "não instalado",
        "claude plugin marketplace add lemomo-ai/lemo-opuscar && claude plugin install lemo-opuscar@lemolab")
    sc = (SKILLS / "video-shotcraft" / "SKILL.md").exists() or "video-shotcraft@" in plugins
    add("OK" if sc else "FALTA", "Video ShotCraft (skill)", "instalado" if sc else "não instalado",
        "git clone --depth 1 https://github.com/Vincentwei1021/video-shotcraft.git ~/.claude/skills/video-shotcraft")
    px = (SKILLS / "pixelfx" / "SKILL.md").exists() or "pixelfx@" in plugins
    add("OK" if px else "FALTA", "PixelFX (skill)", "instalado" if px else "não instalado",
        "claude plugin marketplace add patch-gg/pixelfx && claude plugin install pixelfx@pixelfx")
    rc, out = rodar(["claude", "mcp", "get", "blender"], timeout=120)
    add("OK" if rc == 0 else "FALTA", "Blender MCP (conector)", "configurado" if rc == 0 else "não configurado",
        "uvx mcp-for-blender setup   (instala o addon no Blender e adiciona o MCP; depois reabrir o app)")

    # librosa
    rc, out = rodar([sys.executable, "-c", "import librosa;print(librosa.__version__)"])
    add("OK" if rc == 0 else "FALTA", "librosa (Python)", out.strip().splitlines()[-1] if rc == 0 else "não instalada",
        f'"{sys.executable}" -m pip install librosa   (antes: pip freeze > backup; depois: pip check)')

    # repos
    add("OK" if repos.exists() else "FALTA", "Pasta dos repos", str(repos),
        f'mkdir -p "{posix(repos)}"  e grave {CONFIG} com {{"repos": "..."}}')
    for nome, url in REPOS_CLONE.items():
        d = repos / nome
        ok = (d / ".git").exists()
        add("OK" if ok else "FALTA", f"Repo {nome}", str(d) if ok else "não clonado",
            f'git clone --depth 1 {url} "{posix(d)}"')
    nm = repos / "ClaudeAnimationBase" / "node_modules"
    add("OK" if nm.exists() else "FALTA", "ClaudeAnimationBase: dependências", "node_modules ok" if nm.exists() else "sem node_modules",
        f'cd "{posix(repos / "ClaudeAnimationBase")}" && npm install --no-audit --no-fund')
    chrome = any(Path(p).exists() for p in [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        str(HOME / r"AppData\Local\Google\Chrome\Application\chrome.exe"),
        "/Applications/Google Chrome.app", "/usr/bin/google-chrome", "/usr/bin/chromium"]) or bool(os.environ.get("CHROME_PATH"))
    add("OK" if chrome else "AVISO", "Google Chrome (render do Clawd)", "encontrado" if chrome else "não achado; use --chrome=<caminho>")

    # skills auxiliares
    for nome in MODELOS:
        alvo = SKILLS / nome
        if not alvo.exists():
            add("FALTA", f"Skill {nome}", "não instalada", f"python motion_turbo.py instalar-modelos --repos \"{repos}\"")
            continue
        esperado = arquivos_modelo(nome, repos)
        dif = [k for k, v in esperado.items() if not (alvo / k).exists() or (alvo / k).read_text(encoding="utf-8") != v]
        add("OK" if not dif else "AVISO", f"Skill {nome}", "igual ao pacote" if not dif else
            f"existe com conteúdo diferente em {', '.join(dif)} (não foi sobrescrita)")

    mt = (SKILLS / "motion-turbo" / "SKILL.md").exists()
    add("OK" if mt else "FALTA", "Skill motion-turbo (este pacote)", "instalada" if mt else "não instalada",
        "copiar a pasta do pacote para ~/.claude/skills/motion-turbo (só se não existir)")
    add("INFO", "Three.js / Rapier / Postprocessing", "bibliotecas npm: instalar no projeto do vídeo (skill r3f-fisica-pos)")

    # extras opcionais que melhoram o vídeo (viram sugestão ao usuário, nunca erro)
    lib = Path(os.environ.get("LEMO_OPUSCAR_HOME") or HOME / "lemo-opuscar")
    setup = next(iter(sorted((HOME / ".claude" / "plugins").glob("cache/lemolab/lemo-opuscar/*/skills/lemo-opuscar/scripts/setup.sh"))), None)
    setup_cmd = f'sh "{posix(setup)}"' if setup else "sh <plugin lemo-opuscar>/skills/lemo-opuscar/scripts/setup.sh"
    if (lib / "AGENTS.md").exists():
        add("OK", "Lemo: biblioteca de estilos", str(lib))
        core = (lib / "node_modules" / ".lemo-ok").exists() and (lib / ".venv" / ".lemo-core").exists()
        add("OK" if core else "DICA", "Lemo: pacotes de render", "prontos" if core else
            "o 1º vídeo instala sozinho (alguns minutos); para adiantar: " + setup_cmd + " deps")
        for tier, nome, txt in [("voice", "Lemo: narração local (grátis)", "voz sintetizada no próprio PC"),
                                ("music", "Lemo: trilha gerada (grátis)", "música feita em código")]:
            ok = (lib / ".venv" / f".lemo-{tier}").exists()
            add("OK" if ok else "DICA", nome, "instalada" if ok else f"opcional, {txt}: {setup_cmd} deps {tier}")
    else:
        add("DICA", "Lemo: biblioteca de estilos", "baixa sozinha no 1º vídeo (~15 MB); para adiantar: " + setup_cmd)
    rc, _ = rodar([sys.executable, "-c", "import importlib.util as u,sys;sys.exit(0 if (u.find_spec('whisper') or u.find_spec('faster_whisper')) else 1)"])
    add("OK" if rc == 0 else "DICA", "Legendas automáticas (Whisper)", "instalado" if rc == 0 else
        "opcional, para legendar a narração: pip install faster-whisper (baixa modelo de ~500 MB)")
    blender = tem("blender") or any(Path(p).exists() for p in [r"C:\Program Files\Blender Foundation", "/Applications/Blender.app"])
    add("OK" if blender else "DICA", "Blender (app)", "instalado" if blender else
        "opcional, só para cenas realistas: baixar grátis em blender.org")
    gpu = tem("nvidia-smi")
    add("OK" if gpu else "DICA", "Placa de vídeo dedicada (NVIDIA)", "encontrada" if gpu else
        "não achada: renders com aquarela, 3D pesado ou Blender ficam mais lentos (funciona, só demora)")

    larg = max(len(l[1]) for l in linhas)
    for st, nome, det, como in linhas:
        print(f"[{st:5}] {nome.ljust(larg)}  {det}")
        if st in ("FALTA",) and como:
            print(f"         -> {como}")
    faltas = sum(1 for l in linhas if l[0] == "FALTA")
    print(f"\nResumo: {sum(1 for l in linhas if l[0]=='OK')} OK, {faltas} FALTA, "
          f"{sum(1 for l in linhas if l[0]=='AVISO')} AVISO, {sum(1 for l in linhas if l[0]=='DICA')} DICA "
          f"(DICA = opcional que melhora o vídeo; sugerir ao usuário, não é erro)")
    return 1 if faltas else 0


# ---------- instalar-modelos ----------
def instalar_modelos(a):
    repos = Path(a.repos).expanduser()
    if not CONFIG.exists():
        CONFIG.write_text(json.dumps({"repos": str(repos)}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"criado {CONFIG}")
    else:
        atual = repos_atual(None)
        if atual != repos:
            print(f"AVISO: {CONFIG} já aponta para {atual}; não alterado.")
    for nome in MODELOS:
        alvo = SKILLS / nome
        esperado = arquivos_modelo(nome, repos)
        if not alvo.exists():
            alvo.mkdir(parents=True)
            for k, v in esperado.items():
                (alvo / k).write_text(v, encoding="utf-8")
            print(f"[CRIADA ] {alvo}")
            continue
        dif = [k for k, v in esperado.items() if not (alvo / k).exists() or (alvo / k).read_text(encoding="utf-8") != v]
        if not dif:
            print(f"[IGUAL  ] {alvo} (nada a fazer)")
        else:
            saida = PACOTE / "saida" / f"{nome}-novo"
            saida.mkdir(parents=True, exist_ok=True)
            for k, v in esperado.items():
                (saida / k).write_text(v, encoding="utf-8")
            print(f"[MANTIDA] {alvo} já existe e é diferente ({', '.join(dif)}). Versão do pacote salva em {saida} "
                  f"para comparar; nada foi sobrescrito.")
    return 0


# ---------- mostrar ----------
def fonte(t):
    from PIL import ImageFont
    for nome in ["arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf", "arial.ttf", "DejaVuSans.ttf"]:
        try:
            return ImageFont.truetype(nome, t)
        except Exception:
            continue
    return ImageFont.load_default()


def poster(slug):
    local = PACOTE / "imagens" / "estilos" / f"{slug}.jpg"
    if local.exists():
        return local
    lib = HOME / "lemo-opuscar" / "styles" / slug / "poster.jpg"
    if lib.exists():
        return lib
    try:
        local.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(POSTER_URL.format(slug=slug), local)
        return local
    except Exception:
        return None


def mostrar(a):
    from PIL import Image, ImageDraw
    estilos = {e["slug"]: e for e in json.loads((PACOTE / "estilos.json").read_text(encoding="utf-8"))}
    itens = []
    for s in a.estilos or []:
        e = estilos.get(s)
        if not e:
            print(f"estilo desconhecido: {s} (veja estilos.json)"); continue
        p = poster(s)
        if p:
            itens.append((p, f"Estilo {e['num']}: {e['en']}", " · ".join(e.get("uses") or [])[:60]))
    for f in a.ferramentas or []:
        if f not in FERRAMENTAS:
            print(f"ferramenta desconhecida: {f} (opções: {', '.join(FERRAMENTAS)})"); continue
        arq, nome, desc = FERRAMENTAS[f]
        itens.append((PACOTE / "imagens" / arq, nome, desc))
    if not itens:
        print("nada para mostrar"); return 1
    tw, th, lh, pad = 640, 360, 76, 16
    cols = min(3, len(itens)); rows = (len(itens) + cols - 1) // cols
    W, H = cols * (tw + pad) + pad, rows * (th + lh + pad) + pad
    img = Image.new("RGB", (W, H), (246, 244, 239)); d = ImageDraw.Draw(img)
    f1, f2 = fonte(26), fonte(18)
    for i, (p, t1, t2) in enumerate(itens):
        x = pad + (i % cols) * (tw + pad); y = pad + (i // cols) * (th + lh + pad)
        im = Image.open(p).convert("RGB")
        im.thumbnail((tw, th)); bg = Image.new("RGB", (tw, th), (20, 20, 20))
        bg.paste(im, ((tw - im.width) // 2, (th - im.height) // 2)); img.paste(bg, (x, y))
        d.text((x + 4, y + th + 8), f"{i + 1}. {t1}", fill=(25, 25, 25), font=f1)
        d.text((x + 4, y + th + 44), t2, fill=(90, 90, 90), font=f2)
    saida = Path(a.saida or "motion-turbo-sugestoes.jpg").resolve()
    img.save(saida, quality=85)
    print(saida)
    return 0


def main():
    p = argparse.ArgumentParser(description="Motion Turbo")
    sub = p.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("verificar"); v.add_argument("--repos")
    m = sub.add_parser("instalar-modelos"); m.add_argument("--repos", required=True)
    s = sub.add_parser("mostrar"); s.add_argument("--estilos", nargs="*"); s.add_argument("--ferramentas", nargs="*")
    s.add_argument("--saida")
    a = p.parse_args()
    sys.exit({"verificar": verificar, "instalar-modelos": instalar_modelos, "mostrar": mostrar}[a.cmd](a))


if __name__ == "__main__":
    main()
