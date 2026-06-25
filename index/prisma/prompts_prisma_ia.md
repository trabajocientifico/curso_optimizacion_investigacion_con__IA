# Aplicar el método PRISMA con ayuda de IA — Guía de prompts

> Material complementario de la presentación **«El método PRISMA»**.
> Sirve para que **cualquiera** replique el ejercicio con su propio tema, partiendo de un
> archivo exportado de Web of Science / Scopus con la **misma estructura** que `wos_scopus.txt`.
>
> Cómo leer esta guía: cada paso trae una **🟦 PLANTILLA** (con campos `«...»` para que la rellenes
> con tu tema) y un **🟩 EJEMPLO RESUELTO** (huella hídrica en cultivos, el caso de la presentación).
> Copia el bloque, sustituye los campos y pégalo en tu IA.

---

## 0. Cómo está hecho el archivo (entiéndelo antes de empezar)

El archivo es una exportación **en formato etiquetado de Web of Science** (texto plano). Cada
referencia es un *registro* que empieza en la etiqueta `PT` y termina en `ER` (*end of record*).
Cada campo se identifica con una etiqueta de **2 letras** al inicio de la línea:

| Etiqueta | Significado | ¿Sirve para tamizar? |
|----------|-------------|----------------------|
| `TI` | Título | ✅ sí |
| `AB` | Resumen (abstract) | ✅ sí |
| `DE` | Palabras clave del autor | ✅ sí |
| `ID` | Palabras clave indexadas (Keywords Plus) | ✅ sí |
| `PY` | Año de publicación | ✅ sí (ventana temporal) |
| `LA` | Idioma | ✅ sí (criterio de idioma) |
| `DT` | Tipo de documento (Article, Review…) | ✅ sí (tipo) |
| `SO` | Revista / fuente | contexto |
| `DI` | DOI | ✅ duplicados |
| `UT` | Identificador único WoS | ✅ id del registro |
| `AU`/`AF` | Autores | contexto |
| `CR` | Referencias citadas | ❌ ruido: bórralas antes de pegar |
| `C1`/`C3`/`FU`/`RI`/`OI` | Afiliaciones, financiación, ORCID | ❌ no necesarias para tamizar |

**Consejo práctico:** el archivo completo es muy grande (las `CR` lo inflan). Para tamizar,
trabaja solo con `UT + TI + AB + DE + PY + LA + DT` y procesa los registros **por lotes**
(p. ej. 25–50 por mensaje). Si quieres, pide ayuda para generar primero una **tabla limpia**
(ver Prompt 3).

> En este ejemplo el archivo trae **389 registros**. Los números finales del embudo
> (incluidos, excluidos, etc.) **no se inventan**: salen de ejecutar el tamizaje. Los números
> de la presentación son ilustrativos.

---

## 1. La lógica del ejercicio: qué hace la IA y qué decides tú

La IA **acelera**, tú **decides**. PRISMA exige transparencia, así que en cada paso la IA debe
**justificar** y tú **verificar**.

| Fase PRISMA | Qué le pides a la IA | Qué validas tú |
|-------------|----------------------|----------------|
| Pregunta y criterios | Redactar la pregunta PECO y los criterios de elegibilidad | Que reflejen tu objetivo real |
| Identificación | Detectar duplicados evidentes (mismo DOI/título) | Deduplicación final en Zotero/Rayyan |
| **Tamizaje (título+resumen)** | Clasificar cada registro: incluir / excluir / dudoso, con motivo | Una **muestra** de las decisiones (10–20%) |
| Elegibilidad (texto completo) | Pre-clasificar y listar motivos de exclusión | Lees el texto completo de los candidatos |
| Síntesis | Tabular y resumir los estudios incluidos | Exactitud de los datos extraídos |

> ⚠️ **Regla de oro:** la IA *asiste*, no *reemplaza* al revisor. Reporta que usaste IA, valida
> una muestra y, en lo posible, que **dos personas** revisen de forma independiente.

---

## Prompt 1 — Definir la pregunta de investigación (PECO) y los objetivos

**🟦 PLANTILLA**
```
Actúa como metodólogo experto en revisiones sistemáticas (guía PRISMA 2020).
Voy a hacer una revisión sistemática sobre: «TEMA EN UNA FRASE».
Mi marco PECO provisional es:
- P (población / contexto): «...»
- E (exposición / intervención): «...»
- C (comparador, si aplica): «...»
- O (resultado / desenlace que quiero medir): «...»

Tareas:
1. Redacta UNA pregunta de investigación principal, clara y específica, en formato PECO.
2. Propón 2–3 objetivos derivados de esa pregunta.
3. Señala cualquier ambigüedad de mi PECO que convenga acotar antes de buscar.
Devuélvelo en formato breve y listo para un protocolo.
```

**🟩 EJEMPLO RESUELTO (huella hídrica)**
```
Actúa como metodólogo experto en revisiones sistemáticas (guía PRISMA 2020).
Voy a hacer una revisión sistemática sobre: «huella hídrica de cultivos agrícolas».
Mi marco PECO provisional es:
- P (población / contexto): cultivos agrícolas (cereales, frutales, hortalizas) en sistemas de producción reales.
- E (exposición): producción y riego bajo distintos regímenes hídricos y condiciones climáticas.
- C (comparador): distintos sistemas, regiones, años o escenarios de disponibilidad de agua.
- O (resultado): huella hídrica cuantificada (verde, azul y/o gris), en m³/t o equivalente.

Tareas:
1. Redacta UNA pregunta de investigación principal, clara y específica, en formato PECO.
2. Propón 2–3 objetivos derivados de esa pregunta.
3. Señala cualquier ambigüedad de mi PECO que convenga acotar antes de buscar.
```
*Pregunta esperada:* «¿Cuál es la huella hídrica —verde, azul y gris— de los principales
cultivos agrícolas y cómo varía entre sistemas productivos, regiones y escenarios
climáticos (2010–2025)?»

---

## Prompt 2 — Derivar criterios de elegibilidad y la ecuación de búsqueda

**🟦 PLANTILLA**
```
A partir de esta pregunta PECO: «PEGA AQUÍ LA PREGUNTA».

1. Redacta los CRITERIOS DE ELEGIBILIDAD en dos listas:
   - Inclusión (3–5 criterios)
   - Exclusión (3–5 criterios)
   Cada criterio debe ser observable en el título/resumen o en metadatos (año, idioma, tipo).
2. Asigna a cada criterio de exclusión un CÓDIGO corto (E1, E2, …) que reutilizaré al tamizar.
3. Propón una ecuación de búsqueda booleana (operadores AND/OR, comodín *) con
   sinónimos en español e inglés, lista para Scopus y Web of Science.
4. Sugiere los límites de búsqueda (ventana temporal, tipo de documento, idioma).
```

**🟩 EJEMPLO RESUELTO (huella hídrica)** — criterios y códigos que usaremos al tamizar:

*Inclusión*
- Estudios **empíricos** que **cuantifican** la huella hídrica de uno o más cultivos.
- Artículos o revisiones **revisados por pares**, **2010–2025**.
- Idioma **español o inglés**.

*Exclusión (con código)*
- `E1` No cuantifica huella hídrica (solo la menciona).
- `E2` No trata de cultivos agrícolas (ganadería, industria, ciudades…).
- `E3` Trabajo teórico / modelado sin datos primarios.
- `E4` Resumen de congreso, tesis o literatura gris no revisada.
- `E5` Fuera de la ventana temporal o idioma no elegible.

*Ecuación de búsqueda (ejemplo):*
```
("water footprint" OR "huella hídrica") AND (crop* OR cultivo* OR "agricultural water")
AND (green OR blue OR grey OR gray OR verde OR azul OR gris)
```

---

## Prompt 3 — Preparar / normalizar los registros del archivo

**🟦 PLANTILLA**
```
Te voy a pegar registros exportados de Web of Science en formato etiquetado (cada campo
empieza con una etiqueta de 2 letras; el registro termina en "ER").

Extrae SOLO estos campos de cada registro y devuélvelos como una tabla:
- id  -> valor de la etiqueta UT
- titulo -> TI
- anio -> PY
- idioma -> LA
- tipo -> DT
- keywords -> DE
- resumen -> AB (resúmelo en máx. 40 palabras)

Reglas:
- Ignora por completo las etiquetas CR, C1, C3, FU, RI, OI.
- No inventes registros ni campos: si un campo no está, escribe "—".
- Mantén el id UT exactamente como aparece.

REGISTROS:
«PEGA AQUÍ UN LOTE DE 25–50 REGISTROS»
```

**🟩 NOTA del ejemplo:** en `wos_scopus.txt`, `UT` es el identificador único (p. ej.
`UT WOS:001…`), `TI` el título y `AB` el resumen. Si el archivo es muy grande, pide a la IA
(o a quien te ayude) que primero **borre las líneas `CR`** y luego procese por lotes.

---

## Prompt 4 — Tamizaje por título y resumen (la selección de artículos)

Este es el **corazón** del ejercicio: la IA clasifica cada registro contra tus criterios.

**🟦 PLANTILLA**
```
Vas a tamizar registros para una revisión sistemática siguiendo PRISMA 2020.

CRITERIOS DE INCLUSIÓN:
«pega tus criterios de inclusión»

CRITERIOS DE EXCLUSIÓN (con código):
«pega tu lista E1, E2, … »

INSTRUCCIONES:
- Evalúa cada registro SOLO con el título, las palabras clave y el resumen.
- Decide: INCLUIR / EXCLUIR / DUDOSO.
  · INCLUIR: cumple todos los criterios de inclusión y ninguno de exclusión.
  · EXCLUIR: cumple al menos un criterio de exclusión (indica su código).
  · DUDOSO: el resumen no da información suficiente para decidir.
- Sé conservador: ante la duda real, marca DUDOSO (no excluyas por si acaso).
- No inventes registros. Usa el id UT tal cual.

FORMATO DE SALIDA (tabla / CSV con estas columnas):
id | titulo_corto | anio | decision | codigo_motivo | justificacion (máx. 20 palabras)

Al final, añade un conteo: nº INCLUIR, nº EXCLUIR (por código) y nº DUDOSO.

REGISTROS:
«PEGA AQUÍ UN LOTE DE 25–50 REGISTROS»
```

**🟩 EJEMPLO RESUELTO (huella hídrica)** — cómo se vería una fila de salida:
```
id            | titulo_corto                                  | anio | decision | codigo_motivo | justificacion
WOS:0012345.. | Projecting rice water footprint under SSPs     | 2025 | INCLUIR  | —             | Cuantifica huella hídrica total de arroz por escenarios.
WOS:0067890.. | Urban water footprint in Mashhad, Iran         | 2024 | EXCLUIR  | E2            | Huella hídrica urbana, no de cultivos.
WOS:0099999.. | Plant physiology under alternate wetting       | 2023 | DUDOSO   | —             | Habla de productividad del agua; no aclara si cuantifica HH.
```
> Procesa los 389 registros en lotes; al terminar, junta todas las tablas en una sola hoja de cálculo.

---

## Prompt 5 — Resolver dudosos y registrar exclusiones a texto completo

**🟦 PLANTILLA**
```
Tengo estos registros marcados como DUDOSO en el tamizaje. Para cada uno:
1. Di qué información FALTA en el resumen para decidir.
2. Indica qué buscarías en el texto completo para confirmar inclusión/exclusión.
3. Si finalmente se excluye al leer el texto completo, asigna el código de exclusión.

Recuerda: en la fase de elegibilidad, CADA exclusión debe llevar su MOTIVO (eso es PRISMA).

REGISTROS DUDOSOS:
«pega aquí los registros marcados DUDOSO»
```

**🟩 EJEMPLO RESUELTO (huella hídrica)** — motivos típicos de exclusión a texto completo:
`E1` no cuantifica HH · `E2` población/cultivo no agrícola · *"sin datos cuantitativos
extraíbles"* · *"componente de huella no especificado"* · `E4` no revisado por pares.

---

## Prompt 6 — Construir los números del diagrama de flujo PRISMA

**🟦 PLANTILLA**
```
Con los resultados del tamizaje y de la elegibilidad, ayúdame a armar el diagrama de flujo
PRISMA 2020. Tengo estos conteos:
- Registros identificados en bases de datos: «n»  (por base: «...»)
- Duplicados eliminados: «n»
- Registros marcados por automatización (idioma/tipo/año): «n»
- Registros tamizados: «n»  → excluidos en tamizaje: «n» (desglosa por motivo)
- Informes buscados para recuperación: «n» → no recuperados: «n»
- Informes evaluados a texto completo: «n» → excluidos con razón: «n» (desglosa por código)
- Estudios incluidos: «n»

1. Verifica que las restas cuadran en cada fase.
2. Devuelve el texto de cada caja del diagrama PRISMA 2020.
3. Redacta el párrafo de "selección de estudios" para la sección de Resultados.
```

**🟩 EJEMPLO RESUELTO (huella hídrica, cifras ilustrativas de la presentación):**
`1.099 identificados (Scopus 612 + WoS 487) → −286 duplicados −81 automatización →
732 tamizados → −516 → 216 buscados → −16 no recuperados → 200 evaluados → −152 con razón →
48 incluidos`. *(Al aplicarlo a tu archivo real, estos números serán los que arroje tu tamizaje.)*

---

## Prompt 7 (opcional) — Extracción de datos de los estudios incluidos

**🟦 PLANTILLA**
```
Para cada estudio INCLUIDO, extrae los siguientes campos en una tabla:
- id (UT) · autores · año · país/región · «variable 1» · «variable 2» · «resultado principal»
No infieras datos que no estén explícitos; marca "no reportado" cuando falte.

ESTUDIOS:
«pega los registros incluidos (o sus textos completos)»
```

**🟩 EJEMPLO RESUELTO (huella hídrica):** campos útiles → *cultivo · componente (verde/azul/gris) ·
valor de huella (m³/t) · método (CROPWAT, AquaCrop…) · región · ¿aporta datos para meta-análisis?*

---

## Buenas prácticas y límites (léelo)

- **Transparencia:** guarda todos los prompts y las tablas de decisión; son tu evidencia.
- **Validación humana:** revisa a mano una muestra (10–20%) de las decisiones de la IA y
  mide el acuerdo. Si discrepa mucho, ajusta los criterios y vuelve a tamizar.
- **Dos revisores:** lo ideal es que dos personas (o dos pasadas independientes) tamicen y se
  resuelvan los desacuerdos; la IA puede ser una "segunda opinión", no la única.
- **No alucinar:** insiste siempre en «no inventes registros» y «usa el id tal cual».
- **Privacidad/lotes:** procesa por lotes; no es necesario subir el archivo entero ni las `CR`.
- **Reporta el uso de IA:** indica en Métodos qué modelo usaste y para qué fase.

---

### Para replicar con TU tema
1. Cambia el **TEMA** y el **PECO** (Prompt 1).
2. Regenera **criterios + ecuación** (Prompt 2).
3. Exporta tu búsqueda de Scopus/WoS con la **misma estructura** (formato etiquetado WoS) y
   tamiza con los Prompts 3–4.
4. Cierra el embudo con los Prompts 5–6 y arma tu diagrama PRISMA.
