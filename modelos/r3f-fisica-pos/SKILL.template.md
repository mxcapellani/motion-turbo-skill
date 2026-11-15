---
name: r3f-fisica-pos
description: Física real (React Rapier) e pós-processamento (React Postprocessing - bloom/brilho, blur, grão, glitch, vinheta, aberração cromática) para cenas 3D em React Three Fiber, inclusive dentro de Remotion. Use quando pedirem dominó, torre de Jenga, queda, colisão, tabuleiro de Galton, objetos caindo/quicando, ou glow, brilho, neon, desfoque, granulado, glitch, "deixar o 3D com cara de cinema".
---

# Física e pós-processamento em React Three Fiber

Repos: https://github.com/pmndrs/react-three-rapier e https://github.com/pmndrs/react-postprocessing (MIT). São bibliotecas npm, então se instalam **no projeto do vídeo** (não existe instalação global). Esta skill garante que qualquer sessão saiba instalar e usar.

## Instalar no projeto atual

Versões conferidas em 15/11/2026 (pedem React 19 e `@react-three/fiber` 9):
```bash
npm i @react-three/rapier@^2.2 @react-three/postprocessing@^3.2 postprocessing@^6.39
```
- `postprocessing` 6.39 aceita `three` de 0.168 a 0.187. `@react-three/postprocessing` 3.2 pede `@react-three/fiber` >= 9.7.
- Projeto sem R3F: `npm i three @react-three/fiber @react-three/drei` antes.
- Se o projeto já tiver R3F, confira as versões no `package.json` dele antes de instalar e não atualize `three` ou `react` sem perguntar.

## Pós-processamento (brilho, grão, glitch)

```tsx
import { EffectComposer, Bloom, Noise, Vignette, ChromaticAberration, Glitch, DepthOfField } from '@react-three/postprocessing'
import { BlendFunction } from 'postprocessing'

<EffectComposer multisampling={4}>
  <Bloom intensity={1.2} luminanceThreshold={0.6} luminanceSmoothing={0.2} mipmapBlur />
  <Noise opacity={0.04} blendFunction={BlendFunction.OVERLAY} />
  <Vignette offset={0.3} darkness={0.7} />
</EffectComposer>
```
- O bloom só pega o que passa do threshold: para "acender" um objeto, use `emissive` + `emissiveIntensity` > 1 e `toneMapped={false}` no material.
- Em Remotion, coloque o `EffectComposer` dentro do `<ThreeCanvas>`. Efeitos com tempo próprio (Glitch, Noise animado) não são determinísticos: anime os parâmetros a partir de `useCurrentFrame()` em vez de deixar no automático.

## Física (Rapier)

```tsx
import { Physics, RigidBody, CuboidCollider } from '@react-three/rapier'

<Physics gravity={[0, -9.81, 0]}>
  <RigidBody type="fixed"><CuboidCollider args={[10, 0.1, 10]} /></RigidBody>
  <RigidBody colliders="cuboid" position={[0, 2, 0]}>
    <mesh><boxGeometry args={[0.2, 1, 0.5]} /><meshStandardMaterial /></mesh>
  </RigidBody>
</Physics>
```
- Formas: `colliders="cuboid" | "ball" | "hull" | "trimesh"`. Empurrão inicial: `ref.current.applyImpulse({x,y,z}, true)`.

### Em vídeo renderizado (Remotion/HyperFrames), a física precisa ser determinística

O Rapier roda em tempo real, e o render quadro a quadro não segue o relógio. Use um destes jeitos:
1. **Assar (recomendado):** num script Node com `@dimforge/rapier3d-compat`, simule com passo fixo (1/fps), grave posição e rotação de cada corpo por quadro num JSON e, no vídeo, só leia o JSON pelo `useCurrentFrame()`. Fica idêntico em toda renderização.
2. `<Physics paused>` + avançar o mundo manualmente até o quadro atual (`world.step()` com `timeStep = 1/fps`), sempre resimulando a partir do zero ou de um cache. Funciona, mas é mais lento.

Sempre conferir um still (vários quadros lado a lado) antes do render completo.
