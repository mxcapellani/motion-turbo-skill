---
name: motion-turbo
description: Motion Turbo, o kit de 10 ferramentas open source que deixa o motion feito pelo Claude com cara de estúdio (99 estilos de filme do Lemo Opuscar, 3D com Three.js e Blender, física, brilho/glitch, pixel art, mascote pintado à mão, cortes na batida e promos de produto). Use quando pedirem "motion turbo", "/motion-turbo", "quero um vídeo em motion e não sei o estilo", "me sugere um estilo de vídeo", "qual ferramenta uso pra esse vídeo", "mostra os estilos", ou para instalar/verificar o pacote ("instala o motion turbo", "o motion turbo está funcionando?").
---

# Motion Turbo

Kit que junta 10 repositórios open source para fazer vídeos em motion com o Claude. O trabalho desta skill é **ser a porta de entrada**: entender o tema, sugerir o caminho e o estilo, mostrar imagens das opções e só então passar para a skill que executa.

## Fale com quem não é técnico

Assuma que o usuário **não é técnico**, a menos que ele mostre o contrário.
- Use português simples. Nada de "npm", "repo", "render pipeline" sem explicar: diga "baixar a ferramenta", "a pasta do projeto", "gerar o arquivo de vídeo".
- Antes de cada etapa demorada, diga **o que vai acontecer e quanto tempo leva** (ex.: "vou desenhar o vídeo quadro a quadro, leva uns 5 a 10 minutos").
- Quando o app pedir permissão para um comando, explique em uma frase o que ele faz antes de rodar.
- Ofereça escolhas fechadas ("1, 2 ou 3?") em vez de perguntas abertas técnicas.
- Erro: explique em uma frase o que aconteceu e o que você vai fazer. Nunca despeje o log inteiro.
- Entregue o vídeo dizendo **onde está o arquivo** (caminho clicável) e como postar.

O guia para leigos está em `COMECE-AQUI.md`. Mostre esse guia se a pessoa estiver perdida.

Arquivos deste pacote (`~/.claude/skills/motion-turbo/`):
- `COMECE-AQUI.md`: guia para quem não é técnico (instalar, pedir vídeo, dúvidas).
- `CREDITOS.md`: créditos e licenças das ferramentas e imagens.
- `README.md`: guia para pessoas, com imagem de cada ferramenta.
- `INSTALAR.md`: protocolo para uma IA instalar/verificar sem sobrescrever nada.
- `motion_turbo.py`: `verificar`, `instalar-modelos` e `mostrar` (monta a imagem das sugestões).
- `estilos.json`: os 99 estilos do Lemo Opuscar com categoria, usos e filme de demonstração.
- `imagens/`: uma imagem por ferramenta, `estilos/<slug>.jpg` (pôster de cada estilo) e `catalogo-estilos-lemo.jpg` (os 99 numa imagem só).

## 1. Como chamar

O usuário pode dizer, por exemplo:
- "/motion-turbo" ou "abre o motion turbo"
- "quero um vídeo sobre <tema>, me sugere um estilo"
- "mostra os estilos de vídeo que eu tenho"
- "qual ferramenta uso para um vídeo de lançamento do meu app?"
- "instala / verifica o motion turbo" → siga o `INSTALAR.md` (não o fluxo abaixo).

Se alguma peça necessária parecer ausente (skill não aparece, comando falha), rode antes:
`python ~/.claude/skills/motion-turbo/motion_turbo.py verificar` e resolva pelo `INSTALAR.md`.

## 2. Perguntar o tema (uma mensagem só, curta)

Se o pedido ainda não disser, pergunte de uma vez (no máximo 4 perguntas, com exemplos para a pessoa só escolher):
1. **Tema:** sobre o que é o vídeo? (ex.: "como funciona o GPS", "lançamento do meu app", "história do café")
2. **Objetivo:** explicar, vender/lançar, contar uma história ou entreter?
3. **Formato e duração:** vertical 9:16 (Reels/Shorts/TikTok) ou horizontal 16:9; 15s, 30s, 60s?
4. **Extras:** tem marca/cores, narração ou música própria? Alguma referência de que gosta?

Se o projeto atual tiver identidade visual ou regras (CLAUDE.md, memórias), use-as e não pergunte de novo o que já está escrito.

## 3. Sugerir 3 opções

Monte **3 opções diferentes entre si** (não três variações do mesmo). Cada opção = caminho + estilo + por que combina, em 1 a 2 linhas. Use esta tabela para escolher o caminho:

| Objetivo / tema | Caminho (skill que executa) | Estilos do Lemo que costumam combinar |
|---|---|---|
| Explicar um conceito, ciência, "como funciona" | `lemo-opuscar` | `whiteboard`, `sketchnote`, `flat-space-explainer`, `colored-pencil`, `stick-explainer`, `oscilloscope-math` |
| Explicar máquina, produto físico, peças | `lemo-opuscar` | `teardown`, `blueprint`, `precise-mechanism`, `hardcore-info`, `security-xray` |
| Números, dados, finanças, relatório | `lemo-opuscar` ou 3D com `r3f-fisica-pos` (gráfico 3D + brilho) | `dataviz`, `data-physical`, `spreadsheet`, `bauhaus-shapes`, `transit-map` |
| Notícia, geopolítica, clima, mapa | `lemo-opuscar` | `caption-news`, `news-package`, `map-explainer`, `satellite-briefing`, `comic-history` |
| História, época, curiosidade histórica | `lemo-opuscar` | `newsreel`, `vintage-collage`, `archive-lighttable`, `dark-documentary`, `silent-film` |
| Lançar app/SaaS/site | `video-shotcraft` (+ `librosa` para cortar na batida) | `dark-keynote`, `desktop-flythrough`, `living-screencast`, `hologram-hud` |
| Lançar produto físico / beleza / tech | `video-shotcraft` ou `lemo-opuscar` | `glass-product`, `teardown`, `dark-keynote` |
| História fofa, infantil, mascote | `claude-animation-base` (Clawd) ou `lemo-opuscar` | `crayon-book`, `paper-popup`, `firefly-pointillism`, `rubber-hose` |
| Emoção, música, arte, viagem | `lemo-opuscar` (+ `librosa`) | `impasto`, `watercolor`, `ukiyoe`, `silhouette-rhythm`, `double-exposure` |
| Games, retrô, nostalgia | `pixelfx` ou `lemo-opuscar` | `pixel-rpg`, `hd-2d`, `microgame`, `cel-anime-80s`, `ascii-crt` |
| Objeto 3D realista, cena de produto | Blender MCP (skills de Blender) ou `r3f-fisica-pos` | `glass-product`, `tilt-shift`, `lowpoly-island` |
| Algo "satisfatório": dominó, queda, colisão | `r3f-fisica-pos` (física) + pós (brilho/grão) | `brick-toy`, `pip-simulation` |
| Suspense, terror, trailer | `lemo-opuscar` | `text-flash-cuts`, `backrooms`, `spy-titles`, `scratch-film` |

Para achar outros estilos, leia `estilos.json` e compare o tema com `uses`, `category_en` e `line` (estão em inglês: traduza ao apresentar). Sem ideia clara, busque inspiração com a skill `video-prompts`.

## 4. Apresentar com imagens (obrigatório)

Depois de escolher as 3 opções, gere uma imagem com elas:

```bash
python ~/.claude/skills/motion-turbo/motion_turbo.py mostrar \
  --estilos <slug1> <slug2> --ferramentas <ferramenta> \
  --saida "<pasta-de-trabalho>/motion-turbo-sugestoes.jpg"
```
- `--estilos`: slugs do `estilos.json` (usa o pôster do estilo).
- `--ferramentas`: `lemo`, `threejs`, `pixelfx`, `blender`, `prompts`, `clawd`, `rapier`, `postprocessing`, `librosa`, `shotcraft` (usa a imagem da ferramenta).
- A imagem numera as opções 1, 2, 3 na ordem passada. Mantenha a mesma numeração no texto.

Mostre a imagem ao usuário com a ferramenta de enviar/exibir arquivos que a sessão tiver. Se não houver nenhuma, abra a imagem você mesmo para conferir e informe o caminho clicável. Junto, escreva para cada opção:
- **Nome em português** do estilo + caminho (qual skill vai fazer).
- **Por que combina** com o tema (1 linha).
- **Como vai ficar** (1 linha: cenas, ritmo, cores).

Ofereça também: "quer ver todos os 99 estilos?" → mostre `imagens/catalogo-estilos-lemo.jpg` e o link da galeria animada https://lemomo-ai.github.io/lemo-opuscar/ .

## 5. Depois da escolha

Passe para a skill do caminho escolhido e siga as regras dela:

| Caminho | Skill |
|---|---|
| Estilos de filme | `lemo-opuscar` (diga o estilo escolhido pelo nome/slug) |
| Promo de produto/app | `video-shotcraft` |
| Mascote pintado à mão | `claude-animation-base` |
| Pixel art / efeitos | `pixelfx` |
| 3D com física, brilho, grão | `r3f-fisica-pos` (+ Three.js no projeto) |
| Cena no Blender | skills de Blender + MCP `blender` |
| Ideias/prompts prontos | `video-prompts` |
| Cortes na batida | `librosa` (Python): `librosa.beat.beat_track` na música, e use os tempos das batidas para os cortes |

## 6. Sugerir o que falta para um vídeo melhor

O vídeo fica muito melhor com material do próprio cliente e com alguns extras opcionais. **Sempre** que fizer sentido para o caminho escolhido, sugira o que está faltando, com uma frase sobre o ganho, e deixe a pessoa decidir. Nunca trave o vídeo por causa disso: se ela não tiver, siga com um bom padrão.

**Material do cliente** (pergunte junto com o tema, ou na hora em que fizer diferença):

| Falta | Sugestão ao cliente | Ganho |
|---|---|---|
| Identidade visual | "Tem logo (PNG/SVG) e as cores da marca?" | o vídeo fica com a cara da marca |
| Texto | "Quer me mandar a mensagem principal ou um roteiro, mesmo simples?" | a mensagem sai exata |
| Música | "Tem uma música que você pode usar? Eu corto o vídeo no ritmo dela." | ritmo de lançamento (`librosa`) |
| Voz | "Quer gravar a narração pelo celular? Eu sincronizo e legendo." | mais pessoal e confiável |
| Telas reais | "Me manda o link ou prints do app/site." | promo com telas de verdade (`video-shotcraft`) |
| Referência | "Tem algum vídeo de que você gosta para eu usar de referência?" | acerta o estilo de primeira |
| Formato | confirmar a plataforma (Reels/Shorts 9:16, YouTube 16:9, LinkedIn 1:1) | não precisa refazer depois |

**Extras técnicos opcionais.** Rode `python ~/.claude/skills/motion-turbo/motion_turbo.py verificar` e veja as linhas `DICA`:
- **Narração local grátis** (voz sintetizada do Lemo) quando o vídeo pede voz e o cliente não vai gravar.
- **Trilha gerada grátis** (música do Lemo) quando não há música.
- **Legendas automáticas** (Whisper) quando há narração; vídeo curto de rede social quase sempre ganha com legenda.
- **Blender** só se a escolha for cena 3D realista.
- **Sem placa de vídeo dedicada:** avise que estilos de aquarela e 3D pesado demoram mais e ofereça um teste curto ou um estilo mais leve.

Como sugerir: "Para ficar ainda melhor, posso **[extra]** ([ganho]). É grátis e leva uns [tempo] para instalar. Quer?" Só instale com o sim da pessoa. Tudo que for pago (voz profissional, imagem ou vídeo gerado por serviço externo) exige dizer o serviço e o custo e esperar o ok.

Regras que valem sempre:
- Mostre o roteiro/storyboard e um **quadro parado** antes de renderizar o vídeo inteiro; espere o ok.
- Tudo aqui é gratuito e roda local. Se o caminho escolhido envolver serviço pago (voz, imagem ou vídeo gerado), diga qual e quanto custa e espere o ok antes.
- Se o usuário tiver uma skill própria de avatar ou um estúdio já configurado, respeite as regras desse estúdio.
