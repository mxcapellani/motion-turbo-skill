---
name: video-prompts
description: Biblioteca local com ~750 prompts testados de vídeos feitos em código pelo Claude (motion, 3D, explainer, interativo; canvas, SVG, Three.js, shader, GSAP). Use quando pedirem ideia, referência ou prompt de um vídeo em código, "prompt pronto", "como fizeram aquele vídeo", "estilo mosaico/explainer flat/UI motion", ou antes de começar um motion novo para buscar um ponto de partida comprovado.
---

# Pacotes de prompts de vídeo em código

Dois repos clonados em `{{REPOS}}`:
- `awesome-opus5-5-videos` (yihui-dev): ~700 prompts de vídeos virais, com categoria e tags técnicas. Dados em `data/videos.json`, um `.md` por prompt em `prompts/`.
- `opus-video-prompts` (joeseesun): 54 casos comentados em `prompts/NN-*.md` (launch de startup, explainer de negócio, promo de app em Remotion, line art, pixel art, Three.js...).

## Fonte extra online: 69 estilos da Applied AI

https://www.its-applied-ai.com/r/styles reúne 69 prompts prontos de animação com o Claude, cada um com trechos `[entre colchetes]` para trocar pelo seu tema. Quase todos usam as ferramentas do Motion Turbo (Lemo, Three.js, Blender, Rapier, PixelFX, HyperFrames). O que ele acrescenta:
- séries feitas na HyperFrames: "mundos de avião de papel" e "lançamento de foguete", em ~10 estilos cada (comic, PS2, claymation, Lego, chalkboard...);
- um prompt único com `{STYLE}` que gera 10 visuais em Canvas 2D (fur, synthwave, thermal, matrix, CRT, blueprint...).

Use quando o usuário quiser mais ideias de estilo. Leia a página na hora (ela muda) e cite a fonte (Applied AI). Os prompts não recriam o original pixel a pixel.

## Buscar

```bash
python ~/.claude/skills/video-prompts/buscar.py <termos> [--cat motion|3d|explainer|interactive] [--tag threejs|canvas|svg|shader|gsap|audio|physics|pixel] [--n 10]
python ~/.claude/skills/video-prompts/buscar.py --show <slug>
```

Exemplos: `buscar.py mosaic`, `buscar.py explainer --cat explainer`, `buscar.py product launch --tag gsap`, `buscar.py --show 0xcodez-474136`.

## Como usar

1. Busque 3 a 5 candidatos para o pedido e mostre ao usuário (slug, uma linha sobre cada, link do post original quando houver, para ele ver o vídeo).
2. Adapte o prompt escolhido ao tema, ao formato (vertical 1080x1920 para Reels/Shorts) e à marca do projeto. Não copie a ideia inteira de outra pessoa como se fosse original: use como ponto de partida.
3. Para virar MP4, combine com o estúdio do projeto (HyperFrames, Remotion, `lemo-opuscar`, `video-shotcraft`).

Atualizar: `cd {{REPOS_POSIX}}/awesome-opus5-5-videos && git pull` (idem para `opus-video-prompts`).
