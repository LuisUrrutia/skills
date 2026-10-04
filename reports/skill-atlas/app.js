"use strict";

const atlas = window.SKILL_ATLAS;
const repositoryInventory = atlas.repositoryInventory;
const repositorySkills = new Map(repositoryInventory.skills.map((skill) => [skill.name, skill]));
const sourceReviews = new Map([...atlas.authorReview.skills, ...atlas.accessibilityReview.skills, ...atlas.accessibilityReview.assessments, ...atlas.typescriptReview.skills, ...atlas.typescriptReview.assessments, ...atlas.ciCdReview.skills, ...atlas.ciCdReview.assessments, ...atlas.handoffReview.assessments, ...atlas.activityReview.skills, ...atlas.activityReview.assessments, ...atlas.reviewCodeChangesReview.dylReviewAdoption.assessments, ...atlas.communicationReview.assessments, ...atlas.upstreamAdoptionReview.skills, ...atlas.upstreamAdoptionReview.assessments, ...atlas.teachingReview.skills, ...atlas.teachingReview.assessments].map((skill) => [skill.key, skill]));
const originalKeys = new Set(atlas.skills.map((skill) => skill.key));
const catalogSkills = [...atlas.skills, ...atlas.authorReview.skills.filter((skill) => !originalKeys.has(skill.key)), ...atlas.accessibilityReview.skills, ...atlas.typescriptReview.skills, ...atlas.ciCdReview.skills, ...atlas.activityReview.skills, ...atlas.communicationReview.skills, ...atlas.upstreamAdoptionReview.skills, ...atlas.teachingReview.skills];
const byKey = new Map(catalogSkills.map((skill) => [skill.key, skill]));
const byId = new Map(catalogSkills.map((skill) => [skill.id, skill]));
const recommendationFor = (skill) => sourceReviews.get(skill.key) || skill;
const progressFor = (skill) => atlas.sourceProgress.skills[skill.key];
const supplements = new Map(atlas.supplementary.map((source) => [source.id, source]));
const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[character]);
const slug = (value) => value.toLowerCase().replace(/[^a-z0-9]+/g, "-");
const decisionLabels = { Keep: "Conservar", Adopt: "Adoptar", Blend: "Combinar", Optional: "Opcional", "Adapt first": "Adaptar primero", Skip: "No añadir" };
const kindLabels = { Policy: "Política", Duplicate: "Duplicado", Runtime: "Entorno", Correction: "Corrección" };
const groupLabels = { Local: "Original local snapshots", "Cursor team": "Equipo de Cursor" };
const normalizedSearch = (value) => value.toLocaleLowerCase("es").normalize("NFD").replace(/\p{Diacritic}/gu, "");

const clusters = [
  {
    title: "Activity, contribution and outstanding work",
    winner: "report-work-activity, replacing daily-meeting-update",
    keys: ["Cursor team/what-did-i-get-done", "Cursor team/weekly-review", "Matthew Blode/chat-history", "Compound Engineering/session-history", "pstack/why-source-guides", "Local/daily-meeting-update"],
    text: "Cursor supplies concise period summaries; chat-history and Compound contribute bounded extraction; pstack supplies source context and gaps. None covers the complete requested report alone.",
    why: "Share one collection and retained evidence bundle. Keep historical activity separate from current commitments, use Luna per source, and let deterministic helpers count verified events."
  },
  {
    title: "CI/CD pipeline structure",
    winner: "ci-cd-automation, with provider specialists for implementation",
    keys: ["Addy Osmani/ci-cd-and-automation", "wshobson/deployment-pipeline-design", "Matthew Blode/ci-speedup", "Compound Engineering/deployment-verification-agent", "pstack/principle-make-operations-idempotent", "pstack/principle-separate-before-serializing-shared-state"],
    text: "The selected sources cover stage design, quality gates, measured efficiency, delivery evidence and partial effects. Their templates and fixed thresholds do not fit every product.",
    why: "Use ci-cd-automation to decide what permits each transition. Keep GitHub syntax with github-actions, execution evidence with verify, and existing PR repair with pr-followup."
  },
  {
    "title": "Escribir instrucciones y extraer flujos",
    "winner": "agent-instructions, create-project-instructions and workflow-to-skill",
    "keys": [
      "Local/skill-creator",
      "Matt Pocock/writing-for-agents",
      "Anthropic/skill-creator",
      "pstack/reflect",
      "pstack/automate-me",
      "HumanLayer/improve-claude-md"
    ],
    "text": "Codex aporta estructura; Matt, escritura; Anthropic, captura de intención y evaluación. reflect aporta filtros para extraer aprendizajes. automate-me se centra en modos personales, no en flujos concretos.",
    "why": "Elegir instalación, capa de invocación, derivación o creación según el encaje. workflow-to-skill conserva una extracción pequeña y delega la escritura a agent-instructions. Crear instrucciones no exige repetición."
  },
  {
    "title": "Prototipos para decidir",
    "winner": "prototype: created, with an independent entrypoint",
    "keys": [
      "Matt Pocock/prototype",
      "pstack/prototype",
      "pstack/principle-exhaust-the-design-space"
    ],
    "text": "Matt ofrece una skill con demos de lógica y variantes de interfaz en contexto. pstack ofrece un procedimiento dentro de poteto-mode, orientado al experimento aislado y la evidencia observada.",
    "why": "The repository skill combines Matt's experiment formats with pstack's observed evidence. It ends with an experiment and a decision; implementation and publication keep their own scope."
  },
  {
    "title": "Comparar intentos completos",
    "winner": "compare-solutions, con especialistas cuando corresponda",
    "keys": ["pstack/arena", "pstack/principle-separate-before-serializing-shared-state", "Local/review-audit", "pstack/blast-radius"],
    "text": "compare-solutions coordina intentos independientes de la misma tarea, un juez y una síntesis comprobada. review-code-changes produce auditorías; analyze-change-effects investiga efectos indirectos. Pueden actuar como trabajadores sin convertirse en la misma skill.",
    "why": "La derivación conserva el ciclo de pstack y adapta modelos, aislamiento y fallos parciales. El acuerdo no sustituye la evidencia. No necesita work-mode ni convierte al auditor individual en coordinador."
  },
  {
    "title": "Implementación completa",
    "winner": "work-mode, después de elegir las demás skills",
    "keys": [
      "pstack/poteto-mode",
      "pstack/figure-it-out",
      "Matt Pocock/implement",
      "Matt Pocock/implement-spec",
      "orchestrate/orchestrate"
    ],
    "text": "poteto-mode ofrece la selección de tareas más amplia. implement es deliberadamente breve. implement-spec ejecuta un grafo de tareas y orchestrate gestiona un programa en la nube de Cursor; ambos resuelven problemas mayores que una funcionalidad corriente.",
    "why": "Diseñarlo al final, sobre las skills que hayamos elegido y verificado. Tomar procedimientos de poteto y la sencillez de implement. Escalar a grafos o coordinación en la nube solo cuando lo justifique el alcance."
  },
  {
    "title": "Entender y depurar",
    "winner": "debug, explain-code, explain-decisions and analyze-change-effects",
    "keys": [
      "Matt Pocock/diagnosing-bugs",
      "pstack/how",
      "pstack/why",
      "pstack/blast-radius",
      "Matt Pocock/research"
    ],
    "text": "El diagnóstico reproduce fallos y contrasta causas. explain-code explica estructura y ejecución; explain-decisions reconstruye motivos; analyze-change-effects comprueba efectos indirectos con código real; research consulta hechos externos. Son ramas complementarias, no cinco fases obligatorias.",
    "why": "Las cuatro capacidades están creadas: debug investiga fallos; explain-code explica mecanismos; explain-decisions reconstruye decisiones; analyze-change-effects prueba los supuestos que determinan qué puede romper un cambio en otra parte."
  },
  {
    "title": "Entrevistas, especificaciones y tareas",
    "winner": "Planificación opcional",
    "keys": [
      "Matt Pocock/grilling",
      "Matt Pocock/grill-me",
      "Matt Pocock/grill-with-docs",
      "Matt Pocock/to-spec",
      "Matt Pocock/to-tickets",
      "Matt Pocock/wayfinder",
      "Matt Pocock/to-questionnaire",
      "Matt Pocock/triage"
    ],
    "text": "grill-me y grill-with-docs invocan otros métodos; grilling realiza la entrevista. La especificación recoge el objetivo, las tareas dividen la ejecución y wayfinder organiza decisiones que exceden una sesión. El cuestionario pide conocimiento a otra persona.",
    "why": "Elegir el entregable mínimo que resuelva una duda real. No entrevistar, publicar una especificación, crear tareas y dibujar un mapa para cada arreglo."
  },
  {
    "title": "Arquitectura y modelado de dominio",
    "winner": "design-code-structure, creada e independiente",
    "keys": [
      "Matt Pocock/codebase-design",
      "Matt Pocock/domain-modeling",
      "Matt Pocock/improve-codebase-architecture",
      "pstack/architect",
      "pstack/principle-model-the-domain",
      "pstack/principle-minimize-reader-load"
    ],
    "text": "Matt destaca interfaces pequeñas con comportamiento sustancial y límites públicos de prueba. pstack propone definir datos pronto y comparar diseños. domain-modeling aclara el lenguaje; la auditoría arquitectónica busca oportunidades de refactorización más amplias.",
    "why": "design-code-structure parte del uso real, compara estructuras y recomienda una con sus invariantes y costes. Conserva explain-code, explain-decisions, compare-solutions y prototype como apoyos condicionales. La auditoría del repositorio completo sigue siendo otra tarea."
  },
  {
    "title": "Regresiones y TDD",
    "winner": "tdd derivada de Matt; regresiones de pstack en debug",
    "keys": [
      "pstack/tdd",
      "Matt Pocock/tdd",
      "pstack/principle-test-behavior-not-implementation",
      "ECC/react-testing"
    ],
    "text": "El TDD de pstack prioriza fallos con una prueba local barata y útil. Matt aporta límites públicos, expectativas independientes y ciclos verticales. react-testing aporta técnicas concretas de pruebas de componentes.",
    "why": "tdd ya deriva de Matt y se puede usar directamente para implementar por incrementos de pruebas. debug conserva el criterio de pstack para regresiones; ejecutar una verificación existente sigue siendo otra tarea."
  },
  {
    "title": "Revisión de código",
    "winner": "review-code-changes, creada desde tu auditoría",
    "keys": [
      "Local/review-audit",
      "Matt Pocock/code-review",
      "Addy Osmani/code-review-and-quality",
      "pstack/interrogate",
      "thermos/thermos",
      "dyl-stack/dyl-review",
      "Local/draft-review"
    ],
    "text": "Tu auditoría ya traza causas, impacto, seguridad, controles de activación y cada ruta modificada. Matt distingue normas y requisitos; Addy aporta criterios prácticos; thermos profundiza en estructura; interrogate contrasta opiniones. draft-review prepara comentarios en línea.",
    "why": "Un único responsable con criterios y profundidad opcionales. La evidencia decide qué hallazgo es válido; el número de revisores o su acuerdo no demuestra que tengan razón."
  },
  {
    "title": "Comentarios y limpieza de código",
    "winner": "simplify-code, creada e independiente",
    "keys": [
      "Cursor team/deslop",
      "pstack/no-comments",
      "pstack/principle-laziness-protocol",
      "pstack/principle-subtract-before-you-add"
    ],
    "text": "deslop aporta limpieza del diff; no-comments examina comentarios y restricciones con una política más fuerte. De code-simplification de Addy conservamos criterios de claridad, abstracciones útiles y coste, sin sus ejemplos por lenguaje.",
    "why": "simplify-code aplica criterios independientes del lenguaje al diff real. Conserva motivos, invariantes, errores, datos y recursos; una petición de limpieza no autoriza cambiar el contrato."
  },
  {
    "title": "Clear communication and documentation",
    "winner": "communicate-clearly + write-documentation",
    "keys": [
      "Local/humanize",
      "pstack/unslop",
      "pstack/technical-writing",
      "Matt Pocock/writing-for-agents"
    ],
    "text": "communicate-clearly preserves the local prose safeguards and adds selected eli5, ghostwriter and pstack guidance. write-documentation owns document structure and source accuracy.",
    "why": "Use one default prose owner across languages, load documentation checks when relevant, and keep agent-consumed instructions with agent-instructions."
  },
  {
    "title": "Descripción del PR y orientación del revisor",
    "winner": "pr, actualizada con evidencia visual proporcional",
    "keys": [
      "Local/pr",
      "HumanLayer/visual-pr",
      "Cursor team/make-pr-easy-to-review",
      "Local/walkthrough",
      "HumanLayer/show-me"
    ],
    "text": "Tu skill pr tiene controles más precisos de afirmaciones y convenciones. visual-pr aporta diagramas estructurales; make-pr-easy-to-review añade puntos de entrada y evidencia de que limpiar el historial no cambió el contenido.",
    "why": "The current pr skill preserves the repository template, captures visible changes and uploads images with supported gh --attach operations. It verifies the saved body, recovers partial uploads and retains valid attachment URLs during rewrites."
  },
  {
    "title": "CI, comentarios y preparación",
    "winner": "pr-followup, creada con responsables separados",
    "keys": [
      "Cursor team/fix-ci",
      "Cursor team/loop-on-ci",
      "Cursor team/fix-merge-conflicts",
      "dyl-stack/dyl-ready-pr",
      "pstack/poteto-mode",
      "Local/pr",
      "Local/stacked-pr"
    ],
    "text": "Reparar CI, observar checks, resolver conflictos y evaluar bots forman un mismo ciclo. Babysit de pstack se detiene ante conflictos; dyl-ready-pr los resuelve fusionando la base. Tu política exige rebase desde el checkout responsable.",
    "why": "Un responsable con estado recoge todo el feedback, lo clasifica, delega Git, verifica cada nuevo commit y termina al quedar preparado o al identificar un requisito pendiente."
  },
  {
    "title": "Rendimiento y composición de React",
    "winner": "Vercel y aportes concretos de ECC",
    "keys": [
      "Vercel/react-best-practices",
      "ECC/react-performance",
      "Vercel/composition-patterns",
      "ECC/react-patterns",
      "Addy Osmani/performance-optimization"
    ],
    "text": "react-performance de ECC declara que adapta Vercel. Composición trata la API y el estado; rendimiento trata el coste. react-patterns cubre hooks, estado y servidor/cliente. Addy aporta el método de medición.",
    "why": "Preferir la fuente original de Vercel. Mantener composición separada, consultar recetas generales según necesidad y medir las optimizaciones que se afirmen."
  },
  {
    "title": "Accesibilidad y diseño visual",
    "winner": "accessibility: created, with platform guidance",
    "keys": [
      "ECC/accessibility",
      "ECC/frontend-a11y",
      "Vercel/web-design-guidelines",
      "Anthropic/frontend-design"
    ],
    "text": "The new accessibility skill combines selected ECC, GSD, Blode and Addy coverage with primary standards. Native and terminal guidance loads only for those surfaces. Visual design keeps its own scope.",
    "why": "Check whether the user can complete the flow, including errors and recovery. verify owns execution; accessibility supplies the criteria and interprets the evidence. A scan, screenshot or semantic tree cannot certify the whole experience."
  },
  {
    "title": "Verificación en ejecución",
    "winner": "verify y verification-authoring, tareas distintas",
    "keys": [
      "pstack/create-verification-skill",
      "pstack/maintain-verification-skill",
      "Addy Osmani/browser-testing-with-devtools",
      "ECC/e2e-testing",
      "ECC/react-testing"
    ],
    "text": "pstack aporta la receta local y su mantenimiento. Superpowers y GSD refuerzan qué evidencia permite afirmar que algo funciona; Addy concreta la observación en navegador. ECC queda como referencia de pruebas, sin convertirse en una dependencia de estas dos skills.",
    "why": "Ya creadas: verify es la entrada común y selecciona verify-<app>. verification-authoring crea y mantiene esas recetas con agent-instructions. Crear exige demostrar una funcionalidad; mantener exige revisar y conducir todo el mapa. La evidencia actual decide el resultado."
  },
  {
    "title": "Reflexión, memoria y transferencia",
    "winner": "Mantenimiento y continuación condicionales",
    "keys": [
      "pstack/reflect",
      "Matt Pocock/retro",
      "pstack/recall",
      "Matt Pocock/handoff",
      "pstack/show-me-your-work",
      "Addy Osmani/context-engineering"
    ],
    "text": "reflect y retro mejoran el trabajo futuro; recall reconstruye estado; handoff permite continuar; el registro de decisiones hace revisable una ejecución larga. Actúan en momentos distintos.",
    "why": "Continue from current evidence and a concise record. workflow-to-skill already extracts reusable decisions from completed work; agent-instructions owns writing and validation. Recurrence helps establish value, but a supported reusable lesson need not have happened repeatedly."
  },
  {
    "title": "Enseñanza, resúmenes y visualizaciones",
    "winner": "teach for lessons; learning-plan for courses; explain-code for mechanisms",
    "keys": [
      "pstack/teach",
      "Matt Pocock/teach",
      "Local/visual-change-explainer",
      "HumanLayer/show-me"
    ],
    "text": "Las dos teach comparten nombre, pero una explica código y la otra mantiene un curso. Un resumen de actividad y un informe visual también atienden necesidades distintas.",
    "why": "teach owns lessons and optional practice; learning-plan owns courses and learning progressions. explain-code and explain-decisions replace how and why. report-work-activity owns activity reporting; daily-meeting-update is a deprecated alias. walkthrough is absent, and visual-change-explainer is recorded only in the original local inventory."
  }
];

const conflicts = [
  {
    "title": "PR en borrador frente a PR listo",
    "kind": "Policy",
    "before": "El procedimiento de apertura de poteto-mode exige crear todos los PR listos. Tu skill pr usa borrador por defecto, salvo preferencia del usuario. dyl-ready-pr también puede marcar un borrador como listo automáticamente.",
    "after": "pr debe decidir el estado inicial y sus cambios explícitos. El coordinador transmite la preferencia autorizada y no cambia el borrador solo para activar un revisor.",
    "keys": [
      "opening-a-pr#L27-L33",
      "Local/pr",
      "dyl-stack/dyl-ready-pr#L53-L69"
    ]
  },
  {
    "title": "Fusionar la base frente a hacer rebase",
    "kind": "Policy",
    "before": "loop-on-ci de Cursor recomienda fusionar main en un caso de fallo; dyl-ready-pr también fusiona la base al resolver conflictos. Tu regla exige actualizar una rama de PR mediante rebase.",
    "after": "Usar rebase desde el checkout responsable, verificar el commit remoto esperado, resolver la intención, repetir comprobaciones y publicar con la condición autorizada sobre ese commit. stacked-pr conserva el control de la cadena.",
    "keys": [
      "Cursor team/loop-on-ci#L38-L44",
      "dyl-stack/dyl-ready-pr#L55-L61",
      "Local/stacked-pr"
    ]
  },
  {
    "title": "Aislamiento de worktrees y atajos destructivos",
    "kind": "Policy",
    "before": "poteto-mode exige un worktree separado de main e incluye alternativas con restablecimiento destructivo. implement-spec de Matt crea y restablece worktrees por tarea. Tus reglas exigen Worktrunk y transferencia Orca cuando cambia la propiedad.",
    "after": "Decidir primero si hace falta aislamiento, usar wt, conservar trabajo ajeno y transferir el trabajo en Orca al cambiar de destino. Excluir los atajos destructivos.",
    "keys": [
      "opening-a-pr#L3-L7",
      "Matt Pocock/implement-spec#L21-L40",
      "Local/worktrunk"
    ]
  },
  {
    "title": "Dos copias de la misma revisión",
    "kind": "Duplicate",
    "before": "Los archivos principales thermo-nuclear-code-quality-review de Cursor Team Kit y thermos tienen bytes y nombre idénticos. SHA-256: 7faca08b51b643b2ddd0836f92af15574444024685dcc1e677dbbb39ae8c9e8f.",
    "after": "Conservar una sola referencia. No contar las copias como revisores independientes ni instalar ambas con el mismo disparador.",
    "keys": [
      "Cursor team/thermo-nuclear-code-quality-review",
      "thermos/thermo-nuclear-code-quality-review"
    ]
  },
  {
    "title": "Reglas de Vercel adaptadas por ECC",
    "kind": "Duplicate",
    "before": "react-performance de ECC declara que adapta React Best Practices de Vercel y mantiene sus categorías de prioridad. Añade presentación, por lo que no es una copia idéntica como la de thermos.",
    "after": "Conservar Vercel como fuente principal. Extraer una ayuda para decidir solo cuando cubra una carencia demostrada y conserve procedencia.",
    "keys": [
      "ECC/react-performance#L1-L10",
      "Vercel/react-best-practices"
    ]
  },
  {
    "title": "Dependencias del entorno de ejecución",
    "kind": "Runtime",
    "before": "pstack usa opciones Task, agentes con nombre, configuración de modelos, create-skill y /loop de Cursor. orchestrate necesita su SDK y una clave personal. La evaluación de activación de Anthropic utiliza el CLI de Claude.",
    "after": "Definir primero la capacidad y adaptarla a herramientas reales de T3/Codex. Usar delegación real cuando la tarea la requiera y declarar los modelos solicitados que no estén disponibles. No inventar comandos, agentes ni programadores.",
    "keys": [
      "pstack/poteto-mode",
      "pstack/arena",
      "orchestrate/orchestrate",
      "Anthropic/skill-creator"
    ]
  },
  {
    "title": "Terminar al crear el PR o continuar",
    "kind": "Policy",
    "before": "The initial local pr snapshot ended the turn after creation or update. poteto-mode did not start monitoring merely because it opened a PR. The requested full workflow also needs PR follow-up.",
    "after": "Implemented: pr returns the verified result to its caller. pr-followup handles monitoring and feedback when the enclosing request authorizes that phase. Creating a PR alone does not start monitoring or merge it.",
    "keys": [
      "Local/pr#L14-L20",
      "opening-a-pr#L29-L33",
      "babysit#L1-L7"
    ]
  },
  {
    "title": "Permiso vigente frente a preguntas repetidas",
    "kind": "Policy",
    "before": "Tus reglas autorizan commits atómicos en ramas de trabajo, actualizar descripciones tras publicar y publicar rebases con protección. Las versiones anteriores de commit y pr pedían permiso en la misma petición o para cada operación.",
    "after": "Las versiones revisadas respetan la autorización vigente de la sesión y las reglas. Preguntan solo por decisiones nuevas o límites no autorizados, conservando identidad de cuenta y destino exacto.",
    "keys": [
      "Local/commit",
      "Local/pr"
    ]
  },
  {
    "title": "La autonomía no autoriza cualquier acción externa",
    "kind": "Policy",
    "before": "La sección de autonomía de poteto-mode permite chats de equipo, cambios en tareas y evaluaciones sin preguntar. El principio never-block enumera por separado mensajes externos como límite. Varias skills de planificación publican en gestores.",
    "after": "La autoridad viene del alcance y los permisos del usuario. Distinguir redactar, implementar, publicar un PR, comentar, integrar, desplegar y programar ejecuciones.",
    "keys": [
      "pstack/poteto-mode#L78-L86",
      "pstack/principle-never-block-on-the-human",
      "Matt Pocock/to-spec",
      "ECC/github-ops#L27-L35"
    ]
  },
  {
    "title": "Entrevistas obligatorias durante trabajo autónomo",
    "kind": "Policy",
    "before": "El TDD de Matt pide confirmar con el usuario cada límite público de prueba. grilling explora todas las decisiones y espera un acuerdo. Es adecuado para una entrevista deliberada, pero interrumpe la implementación corriente.",
    "after": "Resolver hechos y límites establecidos desde el repositorio. Preguntar si las respuestas plausibles cambian materialmente alcance, contrato, arquitectura, seguridad o validez. Conservar las entrevistas explícitas.",
    "keys": [
      "Matt Pocock/tdd#L18-L24",
      "Matt Pocock/grilling#L24-L28"
    ]
  },
  {
    "title": "Fases de TDD y commits verificables",
    "kind": "Policy",
    "before": "Matt excluye refactorizar del ciclo de fallo y éxito. El procedimiento de fallos y la secuenciación de pstack prefieren guardar primero una prueba fallida, aunque hablan de unidades verificadas y entregables. ECC permite refactorizar dentro del ciclo.",
    "after": "Adoptar una sola secuencia: demostrar el fallo, corregir, refactorizar si aporta valor y volver a comprobar. Agrupar prueba y arreglo cuando el commit deba pasar CI; conservar aparte la evidencia del fallo inicial.",
    "keys": [
      "Matt Pocock/tdd#L28-L38",
      "pstack/principle-sequence-verifiable-units",
      "bug-fix#L7-L15",
      "ECC/react-testing#L320-L336"
    ]
  },
  {
    "title": "La limpieza puede borrar un motivo importante",
    "kind": "Policy",
    "before": "no-comments puede borrar un comentario de restricción ambiguo y dejar la restricción sin aplicación, señalada como pendiente. Tu política conserva motivos no evidentes, invariancias, restricciones externas y particularidades importantes.",
    "after": "Usar simplify-code. Confirmar la necesidad actual de la restricción, codificarla cuando encaje en el alcance y conservar la explicación que el código no expresa. La duda no autoriza el borrado.",
    "keys": [
      "pstack/no-comments#L19-L24",
      "Cursor team/deslop#L10-L21"
    ]
  },
  {
    "title": "Confianza interna y tipos demasiado absolutos",
    "kind": "Policy",
    "before": "Boundary Discipline exige confiar incondicionalmente en el código interno. La guía TypeScript rechaza conversiones de forma amplia y prefiere argumentos objeto. Puede chocar con estado mutable, contratos externos, aserciones justificadas o API establecidas.",
    "after": "Demostrar la invariancia en el límite real. Usar tipos precisos y validar datos no fiables, conservando comprobaciones legítimas y convenciones compatibles. No debilitar errores para quitar aparente ruido.",
    "keys": [
      "pstack/principle-boundary-discipline#L9-L16",
      "pstack/typescript-best-practices#L14-L28",
      "ECC/error-handling"
    ]
  },
  {
    "title": "Activaciones amplias frente a selección precisa",
    "kind": "Policy",
    "before": "El creador de Anthropic recomienda descripciones más insistentes para compensar activaciones omitidas. El de Codex pide descripciones que distingan casos y evita reglas generales. Además, varias fuentes comparten nombres como tdd, teach y skill-creator.",
    "after": "Mantener identidad de autor durante la comparación e instalar un responsable principal por capacidad. Medir tanto activaciones omitidas como falsas con casos realistas antes de ampliar descripciones.",
    "keys": [
      "Anthropic/skill-creator#L65-L77",
      "Local/skill-creator",
      "Matt Pocock/tdd",
      "pstack/tdd",
      "Matt Pocock/teach",
      "pstack/teach"
    ]
  },
  {
    "title": "XML condicional frente a referencias selectivas",
    "kind": "Policy",
    "before": "improve-claude-md de HumanLayer prefiere instrucciones integradas en bloques XML y desaconseja separarlas. Matt y el creador de Codex favorecen referencias explícitas para contenido condicional.",
    "after": "Usar por defecto una entrada pequeña con referencias condicionales. Considerar el XML un experimento específico de Claude que debe medirse; no sustituye la selección real de contexto.",
    "keys": [
      "HumanLayer/improve-claude-md#L16-L61",
      "Matt Pocock/writing-for-agents",
      "Local/skill-creator"
    ]
  },
  {
    "title": "Información de disponibilidad desactualizada",
    "kind": "Correction",
    "before": "La skill de View Transitions de Vercel afirma que fuera de Next hace falta React Canary porque la API no es estable. El anuncio oficial del 9 de septiembre de 2026 indica que ViewTransition pasó a ser estable en React 19.3.",
    "after": "Actualizar esa sección antes de adoptarla, inspeccionar versiones instaladas y comprobar la integración del framework. No actualizar a Canary solo para cumplir una instrucción desactualizada.",
    "keys": [
      "Vercel/react-view-transitions#L43-L49",
      "react-stable",
      "react-api"
    ]
  },
  {
    "title": "Omitir pruebas o esperar networkidle no verifica",
    "kind": "Correction",
    "before": "Los ejemplos E2E de ECC incluyen omitir una prueba intermitente en CI y esperar networkidle alrededor de una animación. Playwright desaconseja explícitamente usar networkidle como señal de preparación en pruebas.",
    "after": "Comprobar el estado esperado mediante aserciones y mantener evidencia del fallo durante el diagnóstico. Una cuarentena deliberada necesita responsable, motivo y plan de restauración; no demuestra que el fallo esté arreglado.",
    "keys": [
      "ECC/e2e-testing#L140-L193",
      "playwright-readiness"
    ]
  },
  {
    "title": "El requisito de ejecución manual es otro",
    "kind": "Correction",
    "before": "design-control-loop de HumanLayer dice que un workflow no puede ejecutarse manualmente hasta haber corrido una vez y propone añadir temporalmente push. GitHub documenta que debe existir en la rama predeterminada con workflow_dispatch.",
    "after": "Diseñar y validar el evento real con github-actions. Una primera ejecución por push no sustituye el requisito de la rama predeterminada.",
    "keys": [
      "HumanLayer/design-control-loop#L147-L157",
      "workflow-dispatch",
      "Local/github-actions"
    ]
  },
  {
    "title": "Estilo de interfaz y estilo de prosa",
    "kind": "Policy",
    "before": "Vercel's web guide requests typographic quotation marks and title case. communicate-clearly uses straight ASCII in place of English-style curly marks while preserving protected text and each language's own forms. pstack unslop prefers sentence case.",
    "after": "Tratar estas preferencias como estilo del repositorio, no como requisitos de accesibilidad. Respetar idioma y texto protegido, conservando comprobaciones semánticas y de interacción pertinentes.",
    "keys": [
      "web-guidelines",
      "Local/humanize",
      "pstack/unslop#L34-L42"
    ]
  },
  {
    "title": "Temporary storage is not a handoff conflict",
    "kind": "Correction",
    "before": "The earlier atlas treated Matt's OS temporary destination and local transfer machinery as reasons to adapt its handoff skill. The user accepts /tmp and wants a tool-agnostic document capability.",
    "after": "Keep temporary storage as a valid choice. The concrete portability edit is the literal Skill tool reference. Useful content improvements concern continuation evidence and receiver access; execution transfer belongs to its own owner.",
    "keys": [
      "Matt Pocock/handoff#L8-L16",
      "Compound Engineering/ce-handoff"
    ]
  },
  {
    "title": "Scratch files and reusable scripts",
    "kind": "Policy",
    "before": "pstack may use .audit or decisions.tsv, and its reusable-script principle asks for an executable result for almost every nontrivial task. Local rules distinguish temporary work from scripts that serve a recurring workflow.",
    "after": "Place disposable task work according to the checkout convention and deliverables in their established location. Do not turn every one-off operation into a versioned script. A requested handoff artifact can use the user-accepted temporary destination.",
    "keys": [
      "pstack/show-me-your-work#L44-L53",
      "pstack/principle-build-the-lever"
    ]
  },
  {
    "title": "Una lista breve no sustituye todo el feedback",
    "kind": "Policy",
    "before": "dyl-review limita la presentación a siete peticiones. thermos e interrogate valoran el consenso. Sirven para priorizar, pero tu contrato de feedback cubre todos los canales y cada elemento accionable.",
    "after": "Mantener un registro completo de decisiones. Presentar lo más importante sin perder el resto y contrastar cada afirmación en lugar de votar. Revisar el feedback aplicable tras publicar un nuevo commit.",
    "keys": [
      "dyl-stack/dyl-review#L60-L71",
      "thermos/thermos",
      "pstack/interrogate#L59-L67",
      "Local/review-audit"
    ]
  },
  {
    "title": "Base del diff y adaptación del informe visual",
    "kind": "Policy",
    "before": "walkthrough puede elegir el upstream antes de la base real y comparar la rama contra su propia cabecera remota. visual-change-explainer fija temporal del sistema, CSS integrado y Dia. Tus reglas de almacenamiento difieren y el navegador depende de la petición y del entorno.",
    "after": "Resolver la base real del PR o la rama predeterminada verificada. Conservar los diagramas causales y adaptar almacenamiento y CSS. Respetar el navegador solicitado, como Dia en este informe; en su ausencia, usar la preferencia del entorno.",
    "keys": [
      "Local/walkthrough",
      "Local/visual-change-explainer"
    ]
  }
];

const scenarios = {
  "cicd": {
    title: "Design a CI/CD pipeline",
    stages: [
      ["Discover", "ci-cd-automation establishes release units, project commands, consumer boundaries and existing release policy."],
      ["Design and implement", "Choose the stage graph, required evidence, trust boundaries, artifact identity and recovery contract. The platform specialist implements its mechanics within the authorized scope."],
      ["Verify", "Exercise normal and relevant failure paths. Preserve unobserved provider or deployment behavior as an explicit gap; a parsed workflow is not a verified release."]
    ],
    note: "When only provider syntax or permissions change, use the platform specialist directly. A pipeline design request does not authorize publishing or deployment."
  },
  "react": {
    "title": "Una funcionalidad de React",
    "stages": [
      [
        "Antes",
        "work-mode selecciona reglas pertinentes de React; composición si cambia la API; accesibilidad y frontend-design cuando la interfaz lo necesita."
      ],
      [
        "Durante",
        "Implementar un comportamiento coherente con las herramientas del repositorio y recetas de react-testing. Modelar el estado y verificar la interacción real."
      ],
      [
        "Después",
        "review-code-changes, limpieza acotada, commit, pr y pr-followup en la ejecución completa autorizada. Revisar las reglas pertinentes sobre el diff final."
      ]
    ],
    "note": "React Native, View Transitions y GitHub Actions se cargan solo si la tarea introduce esas necesidades."
  },
  "bug": {
    "title": "Un fallo intermitente",
    "stages": [
      [
        "Antes",
        "debug construye una observación del fallo y reduce el desencadenante. Carga su referencia de investigación si falta la reproducción o necesita rastrear comportamiento, historia o consumidores."
      ],
      [
        "Durante",
        "Contrastar explicaciones, obtener evidencia de ejecución y corregir la causa mínima. Añadir una regresión significativa cuando haya un límite práctico de prueba."
      ],
      [
        "Después",
        "Repetir el caso original, retirar instrumentación, comprobar comportamiento cercano, compilar, revisar, guardar y completar el recorrido de PR solicitado."
      ]
    ],
    "note": "Sin evidencia reproducible, declarar los límites del diagnóstico. No presentar una hipótesis como solución probada ni añadir refactorizaciones ajenas para ocultar el síntoma."
  },
  "actions": {
    "title": "Un cambio en GitHub Actions",
    "stages": [
      [
        "Antes",
        "github-actions identifica evento, cuenta, confianza, permisos, llamadores y checks obligatorios. stacked-pr solo si la semántica depende de la cadena."
      ],
      [
        "Durante",
        "Respetar herramientas del repositorio y fijar referencias externas a versiones inmutables verificadas. Diseñar concurrencia, cancelación, resultados y errores."
      ],
      [
        "Después",
        "Ejecutar análisis configurado o actionlint, comprobaciones de seguridad y comandos subyacentes seguros. Revisar el grafo y observar CI del commit publicado."
      ]
    ],
    "note": "Use ci-cd-automation when the stage structure or delivery contract changes. github-actions owns provider mechanics; pr-followup owns an existing PR's failing checks and feedback."
  },
  "followup": {
    "title": "Preparar un PR existente",
    "stages": [
      [
        "Observar",
        "pr-followup identifica PR, cabecera y base exactos, responsable del checkout, checks, canales de revisión y bots tardíos aplicables."
      ],
      [
        "Reparar",
        "Clasificar cada hallazgo. Delegar el rebase al responsable de la rama o cadena y los fallos reales a debug. Verificar, guardar, publicar y actualizar la descripción."
      ],
      [
        "Comprobar de nuevo",
        "Invalidar la preparación anterior. Leer checks y feedback del nuevo commit hasta quedar preparado, necesitar intervención o alcanzar el límite configurado."
      ]
    ],
    "note": "Esta ruta no integra el PR. Los checks antiguos, las omisiones inesperadas, los bots requeridos ausentes y las aprobaciones pendientes no son éxito."
  },
  "research": {
    "title": "Explicar una decisión de arquitectura",
    "stages": [
      [
        "Acotar",
        "Investigate with explain-code for behavior and explain-decisions for historical reasons. Leer solo fuentes relacionadas con la pregunta."
      ],
      [
        "Contrastar",
        "Trazar código y fuentes primarias. Separar decisiones documentadas, inferencias e información ausente. No inventar motivos a partir del código."
      ],
      [
        "Explicar",
        "Use explain-code for a concrete mechanism and a diagram when it clarifies the relationship. Return the sources and remaining assumptions."
      ]
    ],
    "note": "Una consulta de lectura no necesita cambiar de checkout, crear ramas, commits, incidencias, PR ni seguimiento."
  },
  "small": {
    "title": "Una edición pequeña de documentación",
    "stages": [
      [
        "Leer",
        "Examinar el pasaje, su público y contexto suficiente para conservar el significado."
      ],
      [
        "Editar",
        "Use communicate-clearly for prose fidelity and write-documentation for the relevant document checks. Preserve protected text, citations and useful existing structure."
      ],
      [
        "Verificar",
        "Revisar el diff y ejecutar la validación documental aplicable. Guardar en la rama de trabajo según la regla vigente y publicar si forma parte de la petición."
      ]
    ],
    "note": "Sin experimentos de arquitectura, infraestructura TDD, revisión entre agentes ni reescritura del repositorio obligatorios."
  }
};

function sourceMarkup(key) {
  const [baseKey, anchor] = key.split("#");
  const skill = byKey.get(baseKey);
  const extra = supplements.get(baseKey);
  if (!skill && !extra) throw new Error(`Unknown source: ${key}`);
  const label = skill ? `${groupLabels[skill.group] || skill.group} / ${skill.name}` : extra.label;
  const baseUrl = skill ? skill.source : extra.url;
  const url = baseUrl ? baseUrl + (anchor ? `#${anchor}` : "") : null;
  const path = skill ? skill.path : extra.path;
  const hash = skill ? skill.sha256 : extra.sha256;
  return `<li><strong>${escapeHtml(label)}</strong>${url ? `<a href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(url)}</a>` : `<code>${escapeHtml(path)}</code>`}${!url && hash ? `<small>SHA-256 ${escapeHtml(hash)}</small>` : ""}</li>`;
}

function evidenceMarkup(keys) {
  return `<details class="evidence"><summary>Fuentes (${keys.length})</summary><ul>${keys.map(sourceMarkup).join("")}</ul></details>`;
}

function skillLinks(keys) {
  return `<div class="skill-links">${keys.map((key) => {
    const skill = byKey.get(key);
    if (!skill) throw new Error(`Unknown skill: ${key}`);
    return `<a class="skill-link" href="#${skill.id}">${escapeHtml(groupLabels[skill.group] || skill.group)} / ${escapeHtml(skill.name)}</a>`;
  }).join("")}</div>`;
}

function repositoryReference(skill) {
  if (skill.kind !== "personal") return "";
  const currentName = repositoryInventory.replacements[skill.name] || skill.name;
  const current = repositorySkills.get(currentName);
  const status = current
    ? `Current repository package: <a href="#repository-${escapeHtml(current.name)}"><code>${escapeHtml(current.name)}</code></a>.`
    : "This name is not present in the repository inventory. Its installation was not rechecked.";
  return `<p class="notice" lang="en">${status} The description and source below record the original local snapshot.</p>`;
}

function progressMarkup(skill) {
  const progress = progressFor(skill);
  const owners = progress.owners.map((name) => `<a href="#repository-${escapeHtml(name)}"><code>${escapeHtml(name)}</code></a>`).join(", ");
  const evidence = progress.evidence.map((record) => `<li><code>${escapeHtml(record.path)}:${record.line}</code>${record.baselineCommit ? ` · adopted baseline <code>${escapeHtml(record.baselineCommit.slice(0, 12))}</code>` : ""}${record.borrowed?.length ? `<p>${escapeHtml(record.borrowed.join(" "))}</p>` : ""}</li>`).join("");
  return `<div class="source-progress" lang="en"><p><strong>${progress.status === "ready" ? "✓ " : ""}${escapeHtml(progress.label)}</strong>${owners ? ` in ${owners}` : ""}. ${escapeHtml(progress.note)}</p>${evidence ? `<details class="evidence"><summary>Completion evidence (${progress.evidence.length})</summary><ul>${evidence}</ul></details>` : ""}</div>`;
}

function reviewEvidenceMarkup(skill) {
  const review = sourceReviews.get(skill.key);
  if (!review) return evidenceMarkup([skill.key]);
  const references = review.references.map((ref) => `<li><strong>${escapeHtml(ref.path)}</strong><span>${escapeHtml(ref.coverage)}</span><a href="${escapeHtml(ref.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(ref.url)}</a></li>`).join("");
  const prior = originalKeys.has(skill.key) ? `<details class="evidence"><summary>Original review snapshot</summary><p>${escapeHtml(skill.summary)}</p><p>${escapeHtml(skill.reason)}</p><ul>${sourceMarkup(skill.key)}</ul></details>` : "";
  return `<p class="skill-meta" lang="en">Review: ${escapeHtml(review.inspection)}</p><details class="evidence" lang="en"><summary>Current pinned source and inspected references (${review.references.length + 1})</summary><ul><li><strong>${escapeHtml(review.group)} / ${escapeHtml(review.name)}</strong><a href="${escapeHtml(review.source)}" target="_blank" rel="noopener noreferrer">${escapeHtml(review.source)}</a></li>${references}</ul></details>${prior}`;
}

document.querySelectorAll("[data-catalog-count]").forEach((element) => { element.textContent = catalogSkills.length; });
document.querySelector("#ci-cd-repositories").innerHTML = atlas.ciCdReview.repositories.map((repository) => `<tr><th><a href="${escapeHtml(repository.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(repository.repository)}</a><small>${escapeHtml(repository.commit.slice(0, 12))}</small></th><td>${escapeHtml(repository.decision)}</td><td>${escapeHtml(repository.reason)}<details class="evidence"><summary>Scope and exclusions</summary><p>${escapeHtml(repository.reviewDepth)}</p><p>${escapeHtml(repository.excluded)}</p></details></td></tr>`).join("");
document.querySelector("#typescript-repositories").innerHTML = atlas.typescriptReview.repositories.map((repository) => `<tr><th><a href="${escapeHtml(repository.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(repository.repository)}</a><small>${escapeHtml(repository.commit.slice(0, 12))}</small></th><td>${escapeHtml(repository.decision)}</td><td>${escapeHtml(repository.reason)}<details class="evidence"><summary>Scope and exclusions</summary><p>${escapeHtml(repository.reviewDepth)}</p><p>${escapeHtml(repository.excluded)}</p></details></td></tr>`).join("");
document.querySelector("#typescript-principles").innerHTML = atlas.typescriptReview.principles.map((principle) => `<li><a href="${escapeHtml(principle.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(principle.name)}</a> — ${escapeHtml(principle.status)}</li>`).join("");
document.querySelector("#accessibility-repositories").innerHTML = atlas.accessibilityReview.repositories.map((repository) => `<tr><th><a href="${escapeHtml(repository.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(repository.repository)}</a></th><td>${escapeHtml(repository.decision)}</td><td>${escapeHtml(repository.reason)}</td></tr>`).join("");
document.querySelector("#author-collections").innerHTML = atlas.authorReview.collections.map((collection) => `<article class="surface"><h3>${escapeHtml(collection.name)}</h3><p><strong>${collection.count}</strong> skills · <strong>${atlas.authorReview.skills.filter((skill) => skill.group === collection.name && progressFor(skill).status === "ready").length}</strong> sources already incorporated</p><a href="?group=${encodeURIComponent(collection.name)}#catalog">Browse this collection</a><details class="evidence"><summary>Pinned repository</summary><p><a href="${escapeHtml(collection.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(collection.url)}</a></p></details></article>`).join("");
document.querySelector("#author-shortlist").innerHTML = atlas.authorReview.shortlist.map((item, index) => `<article class="surface"><p class="kicker">${index + 1}. ${escapeHtml(item.route)}</p><h3>${escapeHtml(item.title)}</h3><p>${escapeHtml(item.why)}</p><p><strong>Owner:</strong> ${escapeHtml(item.owner)}.</p><p class="skill-meta">${escapeHtml(item.boundary)}</p>${skillLinks(item.keys)}</article>`).join("");
document.querySelector("#author-internal-references").innerHTML = atlas.authorReview.internalReferences.map((item) => `<article class="surface review-boundaries"><p class="kicker">Additional internal reference · ${escapeHtml(item.status)}</p><h3>${escapeHtml(item.collection)} / ${escapeHtml(item.name)}</h3><p>${escapeHtml(item.summary)}</p><p><strong>Proposed owner:</strong> <code>${escapeHtml(item.owner)}</code>. ${escapeHtml(item.reason)}</p><p>${escapeHtml(item.action)}. ${escapeHtml(item.caution)}</p><details class="evidence"><summary>Inspected internal procedure and supporting guidance</summary><ul>${item.files.map((file) => `<li><strong>${escapeHtml(file.path)}</strong><span>${escapeHtml(file.coverage)}</span><a href="${escapeHtml(file.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(file.url)}</a></li>`).join("")}</ul></details></article>`).join("");
document.querySelector("#author-review-limits").innerHTML = `<p>${escapeHtml(atlas.authorReview.scope)}</p><ul>${atlas.authorReview.limitations.map((limit) => `<li>${escapeHtml(limit)}</li>`).join("")}</ul>`;
document.querySelector("#source-progress-summary").innerHTML = `<strong>${atlas.sourceProgress.counts.ready} sources ready</strong> · ${atlas.sourceProgress.counts.pending} pending · ${atlas.sourceProgress.counts.optional} optional · ${atlas.sourceProgress.counts["not-selected"]} not selected. <a href="?progress=ready#catalog">Show ready sources</a>.`;

document.querySelectorAll("[data-repository-count]").forEach((element) => { element.textContent = repositoryInventory.skills.length; });
document.querySelectorAll("[data-pending-count]").forEach((element) => { element.textContent = repositoryInventory.pending.length; });
document.querySelector("#repository-inventory").innerHTML = repositoryInventory.groups.map((group) => {
  const skills = repositoryInventory.skills.filter((skill) => skill.category === group);
  return `<article class="surface"><h3>${escapeHtml(group)} <span class="badge keep">${skills.length}</span></h3><dl class="repository-skills">${skills.map((skill) => `<div id="repository-${escapeHtml(skill.name)}"><dt>${skill.section ? `<a href="#${escapeHtml(skill.section)}"><code>${escapeHtml(skill.name)}</code></a>` : `<code>${escapeHtml(skill.name)}</code>`}</dt><dd>${escapeHtml(skill.summary)}<span class="skill-meta">${escapeHtml(skill.path)}</span></dd></div>`).join("")}</dl></article>`;
}).join("");
document.querySelector("#pending-skills").innerHTML = `<dl class="repository-skills">${repositoryInventory.pending.map((skill) => `<div><dt><a href="#${escapeHtml(skill.section)}"><code>${escapeHtml(skill.name)}</code></a> <span class="badge adapt-first">${escapeHtml(skill.status)}</span></dt><dd>${escapeHtml(skill.summary)}</dd></div>`).join("")}</dl>`;

document.querySelectorAll("[data-evidence]").forEach((element) => {
  element.innerHTML = evidenceMarkup(element.dataset.evidence.split(";"));
});

document.querySelector("#cluster-list").innerHTML = clusters.map((cluster) => `<article class="cluster"><div class="cluster-header"><h3>${escapeHtml(cluster.title)}</h3><span>${escapeHtml(cluster.winner)}</span></div><p>${escapeHtml(cluster.text)}</p><p><strong>Recomendación.</strong> ${escapeHtml(cluster.why)}</p>${skillLinks(cluster.keys)}${evidenceMarkup(cluster.keys)}</article>`).join("");

document.querySelector("#conflict-list").innerHTML = conflicts.map((conflict, index) => `<details class="conflict" ${index < 3 ? "open" : ""}><summary><h3>${escapeHtml(conflict.title)}</h3><span class="badge ${slug(conflict.kind)}">${escapeHtml(kindLabels[conflict.kind])}</span></summary><div><p><strong>Qué pide la fuente.</strong> ${escapeHtml(conflict.before)}</p><p class="resolution"><strong>Resolución recomendada.</strong> ${escapeHtml(conflict.after)}</p>${evidenceMarkup(conflict.keys)}</div></details>`).join("");

document.querySelector("#skill-list").innerHTML = catalogSkills.map((skill) => {
  const review = recommendationFor(skill);
  const progress = progressFor(skill);
  const owner = progress.owners.length ? progress.owners.join(", ") : review.owner;
  const historicalNote = sourceReviews.has(skill.key) ? "" : '<p class="skill-meta" lang="en">The rationale below is the original assessment. Current incorporation and its evidence are shown above.</p>';
  return `<details class="skill-row" id="${skill.id}"><summary><span><span class="skill-title">${escapeHtml(skill.name)}</span><span class="skill-meta">${escapeHtml(skill.group === "Local" ? skill.kind === "system" ? "Included in Codex" : "Original local snapshot" : groupLabels[skill.group] || skill.group)} · ${escapeHtml(review.category)}${skill.entryType === "playbook" ? " · poteto-mode procedure" : ""}</span></span><span class="source-badges"><span class="badge progress-${progress.status}" lang="en">${progress.status === "ready" ? "✓ " : ""}${escapeHtml(progress.label)}</span><span class="badge ${slug(review.decision)}">${escapeHtml(review.action || decisionLabels[review.decision])}</span></span></summary><div class="skill-body">${progressMarkup(skill)}${repositoryReference(skill)}<p>${escapeHtml(review.summary)}</p><p class="skill-owner" lang="en">${progress.status === "ready" ? "Current recipient or source role" : "Proposed owner"}: <strong>${escapeHtml(owner)}</strong>${review.priority ? ` · ${escapeHtml(review.priority)}` : ""}</p>${historicalNote}<dl><div><dt lang="en">Why use it</dt><dd>${escapeHtml(review.reason)}</dd></div><div><dt lang="en">What to adapt or preserve</dt><dd>${escapeHtml(review.caution)}</dd></div></dl><p class="skill-meta">${escapeHtml(skill.author)}. <code>${escapeHtml(skill.declaredName)}</code> · ${review.lines} source lines.</p>${reviewEvidenceMarkup(skill)}</div></details>`;
}).join("");

document.querySelector("#repository-sources").innerHTML = atlas.repositories.map((repository) => `<article class="repo-source"><strong>${escapeHtml(repository.repo)}</strong><span>${repository.count} entradas revisadas</span><a href="${escapeHtml(repository.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(repository.url)}</a></article>`).join("");
document.querySelector("#additional-sources").innerHTML = `<ul class="evidence">${atlas.supplementary.map((source) => sourceMarkup(source.id)).join("")}</ul><h3>Fuentes locales e incluidas</h3><ul class="evidence">${atlas.skills.filter((skill) => skill.kind !== "upstream" && !skill.source).map((skill) => sourceMarkup(skill.key)).join("")}</ul>`;

const search = document.querySelector("#search");
const groupFilter = document.querySelector("#group-filter");
const categoryFilter = document.querySelector("#category-filter");
const decisionFilter = document.querySelector("#decision-filter");
const progressFilter = document.querySelector("#progress-filter");
const filters = document.querySelector("#filters");
const skillRows = new Map(catalogSkills.map((skill) => [skill.id, document.getElementById(skill.id)]));
const searchable = new Map(catalogSkills.map((skill) => {
  const review = recommendationFor(skill);
  const progress = progressFor(skill);
  return [skill.id, normalizedSearch([skill.key, skill.declaredName, skill.author, review.category, review.owner, review.summary, review.reason, review.caution, review.action || "", progress.label, ...progress.owners].join(" "))];
}));

function fillOptions(select, values) {
  [...new Set(values)].sort().forEach((value) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value === "Local" ? "Original local and bundled sources" : decisionLabels[value] || groupLabels[value] || value;
    select.append(option);
  });
}

fillOptions(groupFilter, catalogSkills.map((skill) => skill.group));
fillOptions(categoryFilter, catalogSkills.map((skill) => recommendationFor(skill).category));
fillOptions(decisionFilter, catalogSkills.map((skill) => recommendationFor(skill).decision));

function applyFilters(updateUrl = true) {
  const words = normalizedSearch(search.value.trim()).split(/\s+/).filter(Boolean);
  let count = 0;
  for (const skill of catalogSkills) {
    const review = recommendationFor(skill);
    const matches = (!groupFilter.value || skill.group === groupFilter.value) && (!categoryFilter.value || review.category === categoryFilter.value) && (!decisionFilter.value || review.decision === decisionFilter.value) && (!progressFilter.value || progressFor(skill).status === progressFilter.value) && words.every((word) => searchable.get(skill.id).includes(word));
    skillRows.get(skill.id).hidden = !matches;
    if (matches) count += 1;
  }
  document.querySelector("#result-count").textContent = `${count} de ${catalogSkills.length} fichas`;
  document.querySelector("#empty-state").hidden = count !== 0;
  if (updateUrl) {
    const url = new URL(location.href);
    for (const [key, value] of [["q", search.value], ["group", groupFilter.value], ["category", categoryFilter.value], ["decision", decisionFilter.value], ["progress", progressFilter.value]]) {
      if (value) url.searchParams.set(key, value);
      else url.searchParams.delete(key);
    }
    history.replaceState(null, "", url);
  }
}

function clearFilters() {
  search.value = "";
  groupFilter.value = "";
  categoryFilter.value = "";
  decisionFilter.value = "";
  progressFilter.value = "";
  applyFilters();
}

function readFiltersFromUrl() {
  const parameters = new URL(location.href).searchParams;
  search.value = parameters.get("q") || "";
  groupFilter.value = parameters.get("group") || "";
  categoryFilter.value = parameters.get("category") || "";
  decisionFilter.value = parameters.get("decision") || "";
  progressFilter.value = parameters.get("progress") || "";
  applyFilters(false);
}

filters.addEventListener("submit", (event) => event.preventDefault());
filters.addEventListener("input", () => applyFilters());
filters.addEventListener("change", () => applyFilters());
filters.addEventListener("reset", (event) => { event.preventDefault(); clearFilters(); });
document.querySelector("#empty-reset").addEventListener("click", () => { clearFilters(); search.focus(); });
document.querySelector("#expand-visible").addEventListener("click", () => { skillRows.forEach((row) => { if (!row.hidden) row.open = true; }); });
document.querySelector("#collapse-visible").addEventListener("click", () => { skillRows.forEach((row) => { if (!row.hidden) row.open = false; }); });

function openLinkedSkill() {
  const id = location.hash.slice(1);
  if (!byId.has(id)) return;
  const row = skillRows.get(id);
  if (row.hidden) clearFilters();
  row.open = true;
  row.scrollIntoView({ block: "start", behavior: "auto" });
  row.querySelector("summary").focus({ preventScroll: true });
}

window.addEventListener("hashchange", openLinkedSkill);
window.addEventListener("popstate", () => { readFiltersFromUrl(); openLinkedSkill(); });
document.addEventListener("click", (event) => {
  const link = event.target.closest("a.skill-link");
  if (link && link.hash === location.hash) openLinkedSkill();
});

const scenarioSelect = document.querySelector("#scenario");
function renderScenario() {
  const scenario = scenarios[scenarioSelect.value];
  document.querySelector("#scenario-result").innerHTML = `<ol class="scenario-stages" aria-label="${escapeHtml(scenario.title)}">${scenario.stages.map(([stage, text]) => `<li><h4>${escapeHtml(stage)}</h4><p>${escapeHtml(text)}</p></li>`).join("")}</ol><p class="scenario-note">${escapeHtml(scenario.note)}</p>`;
}
scenarioSelect.addEventListener("change", renderScenario);

let printState = [];
window.addEventListener("beforeprint", () => {
  printState = [...document.querySelectorAll("details")].map((details) => [details, details.open]);
  printState.forEach(([details]) => { details.open = true; });
});
window.addEventListener("afterprint", () => { printState.forEach(([details, open]) => { details.open = open; }); });
document.querySelector("#print-report").addEventListener("click", () => window.print());

const navLinks = [...document.querySelectorAll("nav a")];
const sections = [...document.querySelectorAll("main .section[id]")];
const sectionObserver = new IntersectionObserver(() => {
  const current = sections.findLast((section) => section.getBoundingClientRect().top <= innerHeight * .35);
  if (!current) return;
  const hash = `#${current.id}`;
  navLinks.forEach((link) => {
    if (link.hash === hash) link.setAttribute("aria-current", "location");
    else link.removeAttribute("aria-current");
  });
}, { rootMargin: "0px 0px -65% 0px", threshold: 0 });
sections.forEach((section) => sectionObserver.observe(section));

readFiltersFromUrl();
renderScenario();
openLinkedSkill();
