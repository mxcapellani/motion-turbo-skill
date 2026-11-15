# Instalar o Motion Turbo (protocolo para IA)

Para a IA que for instalar (Claude Code ou outro agente). O objetivo é deixar tudo disponível **em qualquer sessão** (escopo global do usuário) **sem impactar o que já existe**.

## Regras que não se negociam

1. **Verificar antes, instalar só o que falta.** Rode o verificador primeiro e aja apenas nas linhas `FALTA`.
2. **Nunca sobrescrever.** Não use `--force`, `rm -rf`, `git reset --hard`, `pip install --upgrade` nem `npm update` em nada que já existe. Se uma pasta ou skill com o mesmo nome já existir e for diferente, **pare naquele item**, deixe como está e relate.
3. **Não mexer em projetos do usuário.** Three.js, React Rapier e React Postprocessing são bibliotecas npm: instalam-se no projeto do vídeo, na hora de usar (skill `r3f-fisica-pos`), nunca "globalmente" e nunca em projeto existente sem pedir.
4. **Backup antes de mexer em configuração:**
   - Antes de instalar plugin: copie `~/.claude/settings.json` para `~/.claude/settings.json.bak-motion-turbo-AAAA-MM-DD`.
   - Antes de `pip install`: `python -m pip freeze > ~/.claude/pip-freeze-antes-motion-turbo.txt`.
5. **Nada pago.** Tudo aqui é gratuito. Se algum passo pedir conta, chave ou crédito, pare e pergunte.
6. **Validar no fim** e relatar em tabela o que estava instalado, o que foi instalado agora e o que ficou pendente.
7. **Falar simples.** Quase sempre quem pede é uma pessoa não técnica. Antes de cada passo, diga em uma frase o que vai fazer e por quê ("vou baixar a ferramenta de estilos de vídeo, leva 1 minuto"). Não despeje logs: resuma. Ao terminar, diga o que ela precisa fazer (abrir uma conversa nova) e dê uma frase pronta para pedir o primeiro vídeo.

## Passo 0: pré-requisitos

Precisa de `git`, `node` 20+, `npm`, `python` 3.10+ (com Pillow para as imagens: `python -c "import PIL"`), `ffmpeg` e o `claude` CLI. Se faltar algum, **não instale sem perguntar**. Explique o que é ("o Node é o programa que roda as animações; é grátis") e, com o ok, use o instalador oficial do sistema:

| Programa | Windows (winget) | Mac (Homebrew) | Linux (Debian/Ubuntu) |
|---|---|---|---|
| Git | `winget install --id Git.Git -e` | `brew install git` | `sudo apt install git` |
| Node.js LTS | `winget install --id OpenJS.NodeJS.LTS -e` | `brew install node` | site oficial nodejs.org |
| Python 3 | `winget install --id Python.Python.3.12 -e` | `brew install python` | `sudo apt install python3 python3-pip` |
| ffmpeg | `winget install --id Gyan.FFmpeg -e` | `brew install ffmpeg` | `sudo apt install ffmpeg` |
| Pillow | `python -m pip install pillow` | idem | idem |

Depois de instalar um programa novo no Windows, pode ser preciso abrir um terminal ou sessão nova para ele aparecer.

## Passo 1: colocar o pacote como skill global

Repositório oficial: **https://github.com/mxcapellani/motion-turbo-skill**
- Se `~/.claude/skills/motion-turbo` **não existe**: `git clone --depth 1 https://github.com/mxcapellani/motion-turbo-skill.git ~/.claude/skills/motion-turbo`. Se você já tiver a pasta do pacote baixada, pode copiá-la para lá.
- Se **existe e é este mesmo repositório** (`git -C ~/.claude/skills/motion-turbo remote get-url origin`): pergunte se o usuário quer atualizar; com o sim, `git -C ~/.claude/skills/motion-turbo pull --ff-only`.
- Se **existe e é outra coisa**: não mexa. Avise e pergunte o que fazer.

Daqui em diante, `MT=~/.claude/skills/motion-turbo` (ou a pasta do pacote, se ainda não copiou).

## Passo 2: verificar

```bash
python "$MT/motion_turbo.py" verificar
```
Saída: uma linha por peça, com `OK`, `FALTA`, `AVISO`, `INFO` ou `DICA`, e o comando sugerido embaixo de cada `FALTA`. `DICA` é opcional (narração, trilha, legendas, Blender, GPU): **não instale sozinho**. No relatório final, ofereça cada DICA ao usuário em linguagem simples, com o ganho para o vídeo, e instale só as que ele aceitar.

**Pasta dos repos:** o padrão é `~/motion-turbo/repos`. Antes de clonar, procure se os repos já existem em outro lugar (ex.: `find ~ /d -maxdepth 4 -type d -name ClaudeAnimationBase 2>/dev/null`). Se já existirem, **reaproveite** com `--repos <pasta>` em vez de clonar de novo.

## Passo 3: instalar só o que deu FALTA

| Peça | Como instalar (só se FALTA) | Observação |
|---|---|---|
| Lemo Opuscar | `claude plugin marketplace add lemomo-ai/lemo-opuscar` e depois `claude plugin install lemo-opuscar@lemolab` | Plugin oficial. No primeiro uso ele baixa a biblioteca (~15 MB) em `~/lemo-opuscar`. |
| Video ShotCraft | `git clone --depth 1 https://github.com/Vincentwei1021/video-shotcraft.git ~/.claude/skills/video-shotcraft` | Só se a pasta não existir. |
| PixelFX | `claude plugin marketplace add patch-gg/pixelfx` e depois `claude plugin install pixelfx@pixelfx` | Se já houver `~/.claude/skills/pixelfx`, conta como instalado: não instale o plugin em duplicidade. |
| Blender MCP | `uvx mcp-for-blender setup` | Mexe no Blender e na configuração dos apps (faz `.bak` sozinho). **Pergunte antes** e peça para o usuário reabrir o app e o Blender depois. Se já existir um MCP `blender`, não mexa. |
| librosa | `python -m pip install librosa` e depois `python -m pip check` | Sem `--upgrade`. Se o `pip check` acusar conflito, mostre ao usuário e não tente "consertar" atualizando pacotes. |
| Repos (3) | `git clone --depth 1 <url> "<REPOS>/<nome>"` (URLs na saída do verificador) | Só os que faltam. |
| Dependências do Clawd | `cd "<REPOS>/ClaudeAnimationBase" && npm install --no-audit --no-fund` | Instala só dentro da pasta do kit. |
| Skills auxiliares (3) | `python "$MT/motion_turbo.py" instalar-modelos --repos "<REPOS>"` | Cria `claude-animation-base`, `video-prompts` e `r3f-fisica-pos` só se não existirem. Se existirem diferentes, não toca e salva a versão nova em `$MT/saida/` para comparar. Também grava `~/.claude/motion-turbo.json` com a pasta dos repos (se ainda não existir). |
| Three.js / Rapier / Postprocessing | nada agora | Instalam no projeto do vídeo, via skill `r3f-fisica-pos`. |

## Passo 4: validar

1. `python "$MT/motion_turbo.py" verificar`: precisa sair `0 FALTA`. `AVISO` pode ficar, desde que seja explicado ao usuário.
2. Testes rápidos (nenhum gera arquivo fora de pasta temporária):
   - `python ~/.claude/skills/video-prompts/buscar.py product launch --n 3` → lista 3 prompts.
   - `python -c "import numpy as np, librosa; sr=22050; y=np.zeros(sr*4); y[::sr//2]=1; print(librosa.beat.beat_track(y=y, sr=sr)[0])"` → imprime um BPM perto de 120.
   - `python "$MT/motion_turbo.py" mostrar --estilos whiteboard dark-keynote --ferramentas clawd --saida <temp>/teste.jpg` → gera a imagem (abra para conferir).
   - `claude plugin list` → mostra `lemo-opuscar@lemolab` habilitado.
3. Confirme que nada antigo mudou:
   - `python -m pip check` limpo.
   - Os plugins e skills que já existiam continuam listados.
   - `settings.json` continua um JSON válido e com os plugins de antes.
4. Avise: **skills e plugins novos só aparecem numa sessão nova** do Claude Code.

## Passo 5: relatório para o usuário

Em linguagem simples:
1. Tabela com: peça (nome amigável), status antes, ação feita (nenhuma / instalada / mantida por ser diferente) e status depois.
2. Backups criados e o que ficou pendente (e por quê).
3. Os extras opcionais (`DICA`), cada um com uma frase sobre o que melhora no vídeo. Pergunte quais ela quer.
4. O próximo passo: "abra uma conversa nova e escreva: **/motion-turbo quero um vídeo sobre ...**".

## Desinstalar (só se o usuário pedir)

- `claude plugin uninstall lemo-opuscar@lemolab` (e `pixelfx@pixelfx`, se foi instalado por aqui).
- Apagar só as pastas criadas por este pacote: `~/.claude/skills/{motion-turbo,video-shotcraft,claude-animation-base,video-prompts,r3f-fisica-pos}`, a pasta dos repos e `~/.claude/motion-turbo.json`. Confirme com o usuário antes, porque apagar não tem volta.
- `python -m pip uninstall librosa`, só se ela não existia antes (confira no `pip-freeze-antes-motion-turbo.txt`).
