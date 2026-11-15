---
name: claude-animation-base
description: Kit do mascote Clawd pintado à mão (p5.js + p5.brush, 31 emoções, guia de timing e storyboard) para fazer animações curtas de desenho com o Claude, renderizadas em MP4. Use quando pedirem "vídeo do Clawd", "animação pintada à mão", "mascote em aquarela/pincel", "Claude Animation Base", ou um vídeo de personagem desenhado com emoções que não seja o avatar do próprio usuário.
---

# Claude Animation Base (kit do mascote Clawd)

Kit original: https://github.com/JohnHeibel/ClaudeAnimationBase (MIT). Cópia local com dependências em:

`{{REPOS}}\ClaudeAnimationBase`

## Como usar em qualquer sessão

1. **Nunca editar a cópia original.** Para cada vídeo, copie o kit para a pasta de trabalho (sem `node_modules`, `out` e `.git`):
   ```bash
   DEST="<pasta-de-trabalho>/clawd-<tema>"
   mkdir -p "$DEST" && cd {{REPOS_POSIX}}/ClaudeAnimationBase && \
   tar --exclude=node_modules --exclude=out --exclude=.git -cf - . | (cd "$DEST" && tar -xf -)
   cd "$DEST" && npm install --no-audit --no-fund
   ```
   Se a sessão não tiver pasta de projeto, crie em `{{REPOS}}\videos\clawd-<tema>`.
2. Leia o `ANIMATION_GUIDE.md` da cópia inteiro antes de escrever código. Ele tem as regras, o fluxo e a API (`src/clawd.js`, `src/core.js`, `src/timeline.js`).
3. Mostre o storyboard ao usuário e espere o ok antes de animar.
4. Escreva as cenas em `src/scenes/` e ajuste duração/tempo em `src/config.js`.
5. Confira com contact sheets antes do MP4 final (veja as notas de uso no topo de `render.mjs`). Render final:
   ```bash
   node render.mjs --clip --out=out/video.mp4
   ```
   Precisa de Node, Google Chrome e ffmpeg (todos instalados). Se o Chrome não for achado, passe `--chrome=<caminho>`.
6. Vertical para Reels/Shorts: ajuste a resolução para 1080x1920 conforme o guia antes de animar.

## Cuidados

- Os preenchimentos de aquarela do p5.brush são lentos sem GPU dedicada (segundos por quadro). Se o render ficar lento demais, troque esses preenchimentos por algo mais leve.
- O Clawd é o personagem do kit. Para o avatar do próprio usuário, use a skill de avatar que ele já tiver (se existir).
- Para atualizar o kit: `cd {{REPOS_POSIX}}/ClaudeAnimationBase && git pull && npm install`.
