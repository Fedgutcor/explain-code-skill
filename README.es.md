> 🇬🇧 [English version](README.md)

# explain-code

Una [Agent Skill](https://code.claude.com/docs/en/skills) que obliga a un
asistente de IA a explicar código como lo haría un buen ingeniero: con un modelo
mental, un diagrama del mecanismo real, referencias exactas de línea, un
escenario de falla concreto y una prueba que puedes correr para verificar que
algo de todo eso es cierto.

Sin dependencias. Sin scripts. Sin llamadas de red. Es un solo archivo Markdown
que cambia lo que el asistente tiene permitido decir.

## Por qué

Le preguntas a un asistente "¿cómo funciona esto?" y la respuesta por defecto
repite la sintaxis que ya tienes delante, y cierra con un "quizás quieras
considerar posibles condiciones de carrera". Cada frase es verdadera y ninguna
sirve para actuar.

Esta skill reemplaza ese comportamiento por un contrato de cinco partes, y —lo
que de verdad importa— le da a cada parte su **criterio de falla**:

| Parte | Qué exige | Cómo falla |
|---|---|---|
| 1. Anclaje mental | Una analogía física, y *por qué* existe el patrón | Una analogía que nunca declara dónde se rompe |
| 2. Arquitectura visual | Un diagrama Mermaid del mecanismo | Un recuadro por módulo: eso es un índice, no un diagrama |
| 3. Flujo de datos | Entrada, transformaciones con `archivo.ts:L12-L24`, salida, efectos | Números de línea que nadie abrió |
| 4. Modos de falla | Un escenario concreto, con entradas y el resultado equivocado | "Podría tener una condición de carrera": una categoría, no un hallazgo |
| 5. Vector de verificación | Una prueba mínima que apunta a la falla de la parte 4 | Un test de camino feliz que pasa sobre código roto |

La sección 0 es una precondición dura: **nunca expliques código que no leíste**,
y nunca inventes una cita. Un solo número de línea fabricado le quita
credibilidad a todos los demás.

El asistente también tiene permiso explícito de **colapsar** las secciones que no
tengan sustancia. Rellenar una sección vacía es el mismo fallo que un resumen
genérico.

## Instalación

Claude Code, en un proyecto:

```bash
git clone https://github.com/Fedgutcor/explain-code-skill .claude/skills/explain-code
```

O globalmente, para todos tus proyectos:

```bash
git clone https://github.com/Fedgutcor/explain-code-skill ~/.claude/skills/explain-code
```

Las dos formas dejan un `.git/` dentro de la carpeta de la skill (~124 KB). Si
prefieres tenerlo limpio, descarga los dos archivos sueltos — o clona en
`~/projects` y symlinkea `~/.claude/skills/explain-code` hacia ahí, que es como
la uso yo.

Después basta con preguntar normal — `cómo funciona esto`, `explicame este
código`, `walk me through this`. Los disparadores viven en el campo
`description`, así que el asistente carga la skill solo. También puedes
invocarla explícitamente con `/explain-code`.

**Otros asistentes:** pega el cuerpo de [`SKILL.md`](SKILL.md) (todo lo que va
debajo del bloque YAML) en tus instrucciones personalizadas. El contrato no
depende de Claude Code.

**Sobre el idioma:** el `SKILL.md` está en inglés a propósito, y es una sola
versión. Mantener dos traducciones de un contrato es garantizar que diverjan —
de hecho así empezó este repositorio: el artículo que lo regalaba publicaba una
traducción que había perdido los disparadores del `description`, o sea una skill
que no se activaba sola nunca. Los disparadores son bilingües, así que puedes
preguntar en español sin perder nada.

## Qué hay acá

- [`SKILL.md`](SKILL.md) — el contrato. ~70 líneas.
- [`examples.md`](examples.md) — una pasada completa sobre código real (una caché
  con TTL que dispara una estampida de consultas), junto a la salida genérica que
  el contrato prohíbe. El asistente lo carga bajo demanda, y vale la pena leerlo
  tú también: la diferencia entre los dos no está en el largo, está en si el
  lector puede hacer algo con lo que leyó.

## Licencia

MIT. Úsala, bifúrcala, cambia el contrato para que se ajuste a cómo explica las
cosas tu equipo.
