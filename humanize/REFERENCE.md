# AI-associated writing pattern catalog

Use this reference to diagnose prose that feels generated, generic, or unnatural. It describes observable writing patterns, not a method for identifying who or what wrote the text. `SKILL.md` owns the workflow, output contracts, and completion gate.

## Route map

For a full `review`, inspect every family and apply the false-positive guardrails. For a targeted `rewrite` or `edit`, load the families that match the initial scan, then rescan the result against those same families.

- **Generic wording and syntax:** [1. Lexical tells](#1-language-and-lexical-tells), [2. Significance padding](#2-significance-and-notability-padding), [3. Promotional and positioning fog](#3-promotional-tone-and-product-positioning-fog), [4. Formulaic syntax and stock metaphors](#4-formulaic-syntax-and-stock-metaphors), [11. Content economy](#11-content-economy-and-treadmill-restatement), [17. Hedging and filler](#17-hedging-filler-and-sycophancy)
- **Organization and surface style:** [5. Outline artifacts](#5-structure-and-outline-artifacts), [6. Formatting and punctuation](#6-formatting-and-punctuation-tells), [12. Rhythm](#12-rhythm-and-sentence-boundary-tells), [13. Whole-text cohesion](#13-whole-text-cohesion-and-referential-continuity), [16. Openings and closings](#16-openings-closings-and-transition-residue)
- **Generation residue and evidence:** [7. Chatbot residue](#7-chatbot-residue), [8. Prompt leakage](#8-context-contamination-and-prompt-leakage), [9. Attribution and citations](#9-attribution-evidence-and-citation-patterns), [15. Tool and model artifacts](#15-emerging-model-artifacts), [18. Shadowboxing and phantom alternatives](#18-shadowboxing-and-phantom-alternatives)
- **Genre and language:** [10. Social formulas](#10-social-and-linkedin-cliches), [14. Multilingual artifacts](#14-multilingual-and-translation-artifacts)
- **Verdict safeguards:** [19. False-positive guardrails](#19-false-positive-guardrails) and [Review rubric](#review-rubric)

## Detection principles

- Look for density, repetition, and interaction. One generic phrase can be human. Five generic phrases stacked with tidy structure and no concrete detail is suspicious.
- Preserve house style. Formal, academic, legal, technical, multilingual, or accessibility-oriented prose can sound controlled without being AI-written.
- Separate observation from provenance. A pattern means "review this passage," not "infer authorship."
- Prefer concrete repairs. Replace puffery with facts, vague authority with named sources, and chatbot framing with content.
- Apply the catalog by pattern family. Pattern-specific false positives matter more than a keyword match.
- Use only details present in the source. Examples below include every fact used in their rewrites; they are demonstrations, not facts to borrow.

## 1. Language and lexical tells

**Watch for:** Clusters of broad, fashionable words and phrases that could fit almost any topic: "delve," "realm," "landscape," "tapestry," "pivotal," "crucial," "robust," "seamless," "underscore," "foster," "garner," "enhance," "valuable," "comprehensive," "transformative," "ever-evolving," "align with," "interplay," "intricate" or "intricacies," "meticulous" or "meticulously," "plays a key role," and "at the forefront." Judge repeated reliance and co-occurrence, not isolated words.

**Why suspicious:** These words often appear where plain verbs or concrete nouns would do. AI drafts lean on broadly applicable words that fit many topics but add little.

**False positives:** Academic argument, brand copy, grant proposals, institutional reports, and translated prose may use this vocabulary as house style. Do not flag a single word if the surrounding sentence is specific.

**Rewrite or detection tactic:** Replace broad language with the actual action, actor, result, or evidence. If no specific claim remains, cut the sentence.

**Example:**

- Before: "The program plays a crucial role in fostering innovation across the evolving AI landscape by funding six AI safety labs and publishing their evaluation results."
- After: "The program funds six AI safety labs and publishes their evaluation results."

## 2. Significance and notability padding

**Watch for:** Inflated importance: "serves as a testament," "marks a pivotal moment," "stands as a reminder," "reflects broader trends," "leaves an indelible mark," "contributes to the ongoing legacy." Also watch source-listing as importance: "covered by Forbes, Wired, TechCrunch, and local media" without explaining what the coverage established.

**Why suspicious:** AI writing often adds significance claims to make ordinary facts sound article-worthy. It may confuse mention, coverage, and importance.

**False positives:** Obituaries, historical analysis, awards pages, investor materials, or encyclopedia drafts may need significance framing. The problem is unsupported framing, not significance itself.

**Rewrite or detection tactic:** Ask what changed, who said so, and what evidence proves it. Name the source and claim, or remove the importance wrapper.

**Example:**

- Before: "The launch marks a pivotal shift in how teams collaborate because they can now edit the same document at the same time."
- After: "After the launch, teams could edit the same document at the same time."

## 3. Promotional tone and product-positioning fog

**Watch for:** Advertisement language such as "boasts," "nestled," "renowned," "breathtaking," "vibrant," "must-visit," "world-class," "cutting-edge," "game-changing," "supercharge," "elevate," "revolutionize," and "designed to help you thrive." Also watch product-positioning fog that replaces the actual user, task, mechanism, decision, or observed result with a broad business outcome. Common forms include "drive engagement," "unlock value," "enhance the user experience," "seamless," "frictionless," or "intuitive experience," "actionable insights," "align stakeholders," "move the needle," "single source of truth," "customer-centric," "delight users," and "optimize workflows." Treat these as patterns, not banned phrases: they become fog when the surrounding text never says who benefits, what changed, or how the claimed improvement could be observed.

**Why suspicious:** AI systems trained on marketing pages often slide into brochure copy, especially for products, places, culture, travel, education, and SaaS. Product-positioning fog states the desired impression or business result instead of explaining the product behavior, making a claim sound measurable or user-focused while withholding the information needed to understand or verify it.

**False positives:** Landing pages and product copy may intentionally sell, and strategy documents may state objectives before results exist. Terms such as "single source of truth" or "stakeholder alignment" can be precise when the text names the authoritative system, decision, owner, or conflict involved. A phrase is not fog when nearby text supplies the missing behavior or evidence. Even in promotional genres, vague praise still weakens the piece.

**Rewrite or detection tactic:** Remove the positioning language and inspect what remains. Ask who does what differently, in which task or workflow, and what supported evidence shows the result. Replace praise and broad outcomes with any user, behavior, mechanism, decision, constraint, proof, or measurement already present. If the source supplies only an objective, present it as an objective rather than a delivered result. Cut claims that add no supported meaning, and do not invent a metric, baseline, or customer need.

**Example:**

- Before: "The new onboarding flow delivered a seamless, customer-centric experience that drove engagement and unlocked value. It saved unfinished applications, restored them on the next visit, and increased application completion from 62 percent to 78 percent."
- After: "The new onboarding flow saved unfinished applications, restored them on the next visit, and increased application completion from 62 percent to 78 percent."

## 4. Formulaic syntax and stock metaphors

**Watch for:** Formulaic syntax that makes a claim sound more polished or profound than its content. Patterns include copula avoidance and ornate substitutions such as "serves as," "stands as," "represents," "boasts," or "features" where "is" or "has" is clearer; forced parallelism, including repeated rule-of-three constructions in which the third item completes a cadence rather than a real category; "not only...but also" and "it's not just X, it's Y" constructions; false "from X to Y" ranges; and sentence-ending `-ing` clauses such as "highlighting," "showcasing," "underscoring," "ensuring," or "reflecting." Repeated runs of three adjectives, abstract nouns, clauses, or bullets can make thin material feel comprehensive. Also watch stock metaphors that cast a claim as a maxim, including "X is the Y of Z," "X is not a tool but a mirror," and "X becomes a trap," especially when abstract words such as "language," "currency," or "architecture" stand in for an unnamed relationship.

**Why suspicious:** These structures can replace a direct relationship with an ornate predicate, a balanced slogan, or an underdefined metaphor. Repeated triads can make thin material feel complete and force unrelated items into matching grammar. Trailing clauses can also pretend to analyze rather than add facts.

**False positives:** Academic and legal prose may use nominal style. Essays, speeches, fiction, advertising, and an established authorial voice may use metaphor deliberately. "Language," "currency," and "architecture" can be literal domain terms, and some `-ing` clauses are normal and precise. Three items may form an exact count, a natural classification, or a deliberate rhetorical pattern. A single triad is weak evidence; repetition and low-information items make the pattern meaningful.

**Rewrite or detection tactic:** Recover the underlying proposition before changing its form. Prefer a direct verb when it preserves the claim. Translate a stock metaphor into a literal relationship only when the source supplies that relationship; preserve a deliberate or underdefined metaphor rather than inventing its meaning. For a triad, map each item to distinct source information. Keep the three-part structure when every item is real and parallel; remove padding, merge overlap, or abandon the shape when an item exists only to complete the rhythm. If a trailing clause is fake analysis, cut it, fold it into the sentence, or start a new sentence when that is the clearest connection. Split false ranges into a list of actual topics.

**Examples:**

- Before: "The report serves as a roadmap for managers, not only outlining the approval process but also highlighting where requests tend to stall."
- After: "The report shows managers how the approval process works and where requests tend to stall."
- Before: "Speed is the currency of customer support: teams that answer tickets within an hour retain more customers."
- After: "Teams that answer support tickets within an hour retain more customers."
- Before: "The release delivers speed, security, and resilience. It starts in 4 seconds instead of 12, encrypts tokens at rest, and resumes failed uploads automatically."
- After: "The release starts in 4 seconds instead of 12, encrypts tokens at rest, and resumes failed uploads automatically."

## 5. Structure and outline artifacts

**Watch for:** Formulaic sections: "Introduction," "Background," "Key Takeaways," "Challenges and Future Prospects," "Conclusion," "Final Thoughts," even when the content is short. Repeated paragraph shape: broad claim, generic explanation, neat closing sentence. Watch paragraph-closing "whether" summaries: "Whether you're a founder, marketer, or student, this tool can help."

**Why suspicious:** AI drafts often start from an outline template and fill each slot with safe generalities.

**False positives:** Reports, docs, course materials, and regulated formats may require predictable sections.

**Rewrite or detection tactic:** Keep useful headings, cut template headings, and lead with the real point. Let paragraphs end when the evidence ends.

**Example:**

- Before: "In conclusion, whether you are starting out or scaling up, the next release adds shared folders and admin audit logs."
- After: "The next release adds shared folders and admin audit logs."

## 6. Formatting and punctuation tells

**Watch for:** Overuse of bold inline labels, emoji bullets, title-case headings in casual prose, boxed takeaway lists, excessive blockquotes, mechanical tables, curly quotes or apostrophes in otherwise plain text, invisible Unicode, and repeated Markdown fences. In the prose itself, watch repeated "announcement: point" structures and em dashes (`—`) used as default connectors, dramatic pauses, or all-purpose asides.

**Why suspicious:** Chatbots often use formatting and punctuation as shortcuts for structure. A colon can delay a point behind an empty announcement, while a dash can conceal whether ideas are connected, opposed, or independent.

**False positives:** A colon naturally introduces a list, example, explanation, or result. During review, style guides may require em dashes, title case, smart punctuation, tables, or callouts; accessibility docs may use consistent labels for scanning.

**Rewrite or detection tactic:** Follow the straight-ASCII punctuation convention in `SKILL.md` for generated or edited prose and preserve other intentional typography. For a colon, remove the lead-in as a test: if the remainder already states the whole point, write it directly. For an em dash, identify the logical relationship and rebuild it with ordinary syntax, a comma and conjunction, reordered clauses, or a new sentence. Swapping in parentheses, an en dash, or a hyphen leaves the structural problem untouched.

**Examples:**

- Before: "The advantage is clear: the cache avoids repeated queries."
- After: "The cache avoids repeated queries."
- Before: "If you come from traditional automation: here you describe activation conditions instead of registering event handlers."
- After: "With traditional automation, you register event handlers. Here, you describe activation conditions."
- Keep: "The command accepts three formats: JSON, CSV, and XML."
- Before: "The change seems small — but it breaks the API."
- After: "The change seems small, but it breaks the API."
- Before: "Only one option remains — restart the server."
- After: "Only one option remains. The server must be restarted."

## 7. Chatbot residue

**Watch for:** Conversational scaffolding left in content: "Great question," "Certainly," "Of course," "I hope this helps," "Let me know if you'd like," "Here is a revised version," "As an AI," "I can't browse," "based on my training," "as of my last update," "up to my knowledge cutoff." Also watch leaked prompts, placeholders, reasoning notes, "[insert citation]," "turn0search," citation brackets, tool traces, and AI-generated UTM parameters.

**Why suspicious:** These are direct artifacts from a chat session or generation tool, not natural content.

**False positives:** Emails and support replies may use friendly openings. Technical notes may mention model limits on purpose.

**Rewrite or detection tactic:** Remove the interface layer. Keep only the content the reader came for. If a limitation matters, state the real limitation and source.

**Example:**

- Before: "Certainly. Here is an overview of the policy. I hope this helps."
- After: "The policy requires manager approval for expenses over $500."

## 8. Context contamination and prompt leakage

**Watch for:** Text refers to instructions, roles, files, or constraints that should not be visible to the reader: "as requested," "following your prompt," "the user wants," "this section should," "TODO: verify," "maintain a professional tone," "do not mention," "make it sound human," or unrelated context from another task.

**Why suspicious:** AI outputs can blend the task prompt, hidden instructions, earlier messages, or examples into the final prose.

**False positives:** Draft notes, editorial comments, and changelogs may intentionally mention requirements.

**Rewrite or detection tactic:** Remove production instructions from reader-facing copy. If the note is useful, move it to a comment, issue, or editorial checklist.

**Example:**

- Before: "This section should reassure users that the migration is simple because most teams can finish it in one afternoon."
- After: "Most teams can finish the migration in one afternoon."

## 9. Attribution, evidence, and citation patterns

**Watch for:** Vague or inflated attribution: "experts say," "observers have noted," "industry reports," "critics argue," "research suggests," "studies show," "it is widely recognized," and "the literature highlights." Also watch claims attributed to "several sources" when only one is cited, citations that do not support the sentence, fabricated precision, source laundering, and generic transitions between sources.

**Why suspicious:** Vague authority can make an opinion look established while hiding whether the evidence supports its scope, certainty, or attribution.

**False positives:** Literature reviews, field summaries, and consensus statements may need collective attribution. A plural attribution is valid when several supplied sources support it.

**Rewrite or detection tactic:** Identify who holds each claim and which source supports it. Name the source when it is available, and match singular or plural attribution to the evidence. If the source is missing, preserve the uncertainty instead of promoting the claim to fact; ask for the source when verification matters.

**Example:**

- Before: "Several industry reports show that the migration is more reliable. Acme's 2025 benchmark found that failed jobs fell from 4 percent to 1 percent."
- After: "Acme's 2025 benchmark found that failed jobs fell from 4 percent to 1 percent."

## 10. Social and LinkedIn cliches

**Watch for:** Platform formulas: "I am thrilled to announce," "humbled and honored," "big news," "after months of hard work," "here's what I learned," "agree?" "thoughts?" "comment below," "build in public," "founder journey," "10 lessons from," "I used to think X, then Y changed everything."

**Why suspicious:** AI-generated social posts often imitate engagement bait and thought-leader cadence.

**False positives:** LinkedIn has native conventions. A person may actually be announcing a job, grant, launch, or award.

**Rewrite or detection tactic:** Make it sound like the actual person. Use the real detail, one honest reaction, and no engagement bait unless the user wants it.

**Example:**

- Before: "I am humbled and honored to share this exciting milestone: I joined Render's infrastructure team this week, and I feel nervous, excited, and ready to learn."
- After: "I joined the infrastructure team at Render this week. Nervous, excited, and ready to learn."

## 11. Content economy and treadmill restatement

**Watch for:** Low-information sentences that restate the heading or previous line: "This is important because it matters," "The tool helps teams work better," "These benefits can improve outcomes." Watch paragraphs that keep moving but do not add names, numbers, examples, mechanisms, tradeoffs, or stakes.

**Why suspicious:** AI can maintain fluent motion while avoiding commitment. The prose feels smooth, but the reader learns little.

**False positives:** Executive summaries and abstracts may compress detail by design. Transitional sentences can be useful.

**Rewrite or detection tactic:** Find the shortest version that preserves the full claim, qualification, tone, and necessary context. Combine repeated points, move support next to the claim it explains, and remove a sentence when it adds no fact, example, mechanism, consequence, or useful connection.

**Examples:**

- Before: "Better onboarding improves the employee experience by giving new hires their laptop, payroll login, and first-week schedule before day one."
- After: "New hires now get their laptop, payroll login, and first-week schedule before day one."
- Before: "The user can retry again."
- After: "The user can retry."

## 12. Rhythm and sentence-boundary tells

**Watch for:** Metronomic sentence length, uniform paragraph size, repeated transition placement, too-even punctuation, choppy period-stacked prose, or abrupt breaks between ideas that belong together. Watch especially for runs of short declarations or fragments that isolate every fact as a punchline, including formulas such as "No X. No Y. Just Z." Also watch detached verdicts: short sentences built around an abstract judgment such as "The separation is deliberate," "The distinction matters," or "The tradeoff is clear," followed immediately by the mechanism or reason that makes the judgment meaningful. Related defaults, conditions, and exceptions can produce the same fragmentation when they become consecutive standalone sentences, especially with a repeated subject followed by "The exception is." Dense sentences often contain several asides, switch actors midstream, chain many actions, mix conditions with results, or make the reader revisit the opening to understand the ending.

**Why suspicious:** Uniform rhythm can make prose feel templated. At the other extreme, isolating every fact for emphasis gives ordinary information a staged cadence. A detached verdict makes the reader hold an abstract conclusion and wait for the next sentence to learn what it means, separating the judgment from its evidence or mechanism. Fragmented rules force the reader to reconstruct the policy hierarchy and decide which requirement an exception overrides. These patterns make sentence boundaries feel imposed rather than shaped by meaning.

**False positives:** Technical manuals, policies, abstracts, accessibility-oriented prose, and style-guide-compliant docs may deliberately use short sentences or a steady rhythm. Tables, checklists, legal provisions, and procedures may require one rule or exception per line. Dialogue, speeches, fiction, and advertising may use staccato cadence for effect. A short verdict may summarize evidence already presented, mark a genuine turn, or carry deliberate emphasis in the author's voice. A single short sentence can create legitimate emphasis, and a long sentence can remain clear when its parts have an obvious relationship.

**Rewrite or detection tactic:** Map the actors, actions, conditions, and sequence before choosing sentence boundaries. Let each sentence hold one understandable movement, which may include several closely related facts or clauses. Keep actions together while the actor and focus remain stable; split near a change of actor, stage, or main point, then preserve continuity with an explicit subject or natural transition. When a short verdict and its explanation keep the same actor, stage, and focus, build the judgment into the concrete relationship. If two sentences remain clearer, let the first state the mechanism and the second continue from a specific referent. For rules, map the default, affected subset, and exceptions before drafting. Keep them in one grammatical unit or in explicitly linked sentences; use scope-bearing syntax such as "those that," "except," and "unless," and make clear which requirement each exception overrides. Join ideas when grammar shows their relationship more clearly than a full stop, and split whenever nesting, ambiguity, or cognitive load makes the reader retrace the sentence. Keep a short sentence when it carries the passage's real point of emphasis rather than making every intermediate fact sound conclusive.

**Examples:**

- Before: "The deployment stopped because the nightly backup held the database lock. The backup finished. The team restarted the deployment. It completed."
- After: "The nightly backup held the database lock and stopped the deployment. Once the backup finished, the team restarted the deployment, and it completed."
- Before: "When the user posts a photo, the app, after checking the session and validating the selected file, sends the image to the server, which processes it and returns its identifier."
- After: "When the user posts a photo, the app checks the session and validates the selected file before sending the image to the server. The server processes it and returns its identifier."
- Before: "The separation is deliberate. Command modules stay small, while protocol details live in independently testable library modules."
- After: "The deliberate separation keeps command modules small by leaving protocol details out of them. Those details live in library modules, where they can be tested independently."
- Before: "Most commands are read-only. Commands that change the profile or a relationship require explicit confirmation. The exception is `note set`, which sends by default and provides `--dry-run` for previewing the operation."
- After: "Most commands are read-only. Those that change the profile or a relationship require explicit confirmation, except `note set`, which sends by default and supports `--dry-run` to preview the operation."

## 13. Whole-text cohesion and referential continuity

**Watch for:** A text that reads like separately polished fragments, preserves the source order despite weak logic, opens consecutive sentences on the same subject without a rhetorical purpose, or rotates among aliases such as a proper name, "the company," "the organization," and "the platform." Also watch referent drift, where one catch-all noun names different kinds of objects across the passage, and topic-word saturation, where the brief's central noun or adjective modifies unrelated phrases after the text has already established its scope. The local sentences may be clean while the whole piece still wanders, doubles back, or manufactures cohesion through repeated labels.

**Why suspicious:** Local rewriting can preserve boundaries and decisions that weaken the whole. It may leave redundancy, detach support, hide causal links, or produce opposite failures of cohesion: forced aliases that obscure a stable referent, catch-all nouns that collapse distinct objects, topic words that blur scope through repetition, and repeated openings that preserve sentence boundaries the thought no longer needs.

**False positives:** Technical, legal, and academic text may repeat one term or preserve a fixed order for precision. An umbrella term is useful when its members are explicit or its meaning remains defined and stable. A repeated modifier may distinguish real scopes, preserve an established term, or make standalone content understandable. Rhetorical repetition can create emphasis or rhythm. Pronouns and omitted subjects behave differently across languages, so judge cohesion in the target language rather than imposing English patterns.

**Rewrite or detection tactic:** Identify the text's throughline and rebuild around it. Move evidence beside its claim, combine ideas that do the same work, remove restatement, and reorder material when the logic improves. Keep one precise label per concept and one stable concept per label. For referent drift, map each occurrence to the concrete source-supported object and rewrite it independently; do not choose one universal synonym. For topic-word saturation, establish the default scope once, remove later modifiers that add no contrast, and name the exact scope when it matters. Do not hide repetition through synonym cycling. When consecutive sentences share an actor and focus, combine their actions. When they need separate sentences, vary the opening only if time, condition, contrast, consequence, or another real relationship provides a better entry. Use a pronoun only when its antecedent is unmistakable, and use a different role label only when that role matters to the point.

**Examples:**

- Before: "Westbridge Museum acquired the letters in 1998. Westbridge Museum digitized them in 2019. The museum now provides online access to the letters. The institution also offers downloadable transcripts."
- After: "Westbridge Museum acquired the letters in 1998, digitized them in 2019, and now provides online access to the letters and downloadable transcripts."
- Before: "Los municipios reciben señales vecinales por correo, teléfono y formularios. El piloto llevará esas señales a un canal interno que funciona como cola de moderación, sin sustituir canales de emergencia como el 112."
- After: "Los municipios reciben avisos vecinales por correo, teléfono y formularios. El piloto reunirá esos avisos en una cola de moderación sin sustituir servicios de emergencia como el 112."
- Before: "El piloto reunirá avisos locales, servicios locales y contenido local de un barrio antes de escalar la propuesta a toda la ciudad."
- After: "El piloto reunirá los avisos, servicios y contenidos de un barrio antes de extenderse a toda la ciudad."
- Keep: "La normativa distingue entre la administración local, autonómica y estatal."

## 14. Multilingual and translation artifacts

**Watch for:** Literal calques, overly formal register, unnatural idioms, English AI phrases translated word for word, inconsistent pronouns, mixed punctuation norms, overexplained cultural context, or machine-like preservation of source sentence order. For Spanish prose, treat "La señal es clara:" as a local form of the [announcement: point pattern](#6-formatting-and-punctuation-tells) when the opener adds no stance or evidence. Treat shifting abstract uses of "señal" or "canal," and repeated uses of "local" after the scope is established, as local forms of [referent drift and topic-word saturation](#13-whole-text-cohesion-and-referential-continuity). These are routing cues, not banned words.

**Why suspicious:** AI translation and multilingual rewriting can flatten voice and import English chatbot patterns into other languages.

**False positives:** Second-language writing, regional dialect, code-switching, and formal localization can look unusual to outsiders. Do not erase identity or dialect.

**Rewrite or detection tactic:** Match the target language, region, and audience. Preserve intentional code-switching. Fix only unnatural phrasing, generic padding, and imported chatbot structure.

**Example:**

- Before: "Es importante notar que esta herramienta facilita un paisaje robusto de productividad al ayudar a organizar tareas y revisar avances."
- After: "Esta herramienta ayuda a organizar tareas y revisar avances."

## 15. Emerging model artifacts

**Watch for:** Hidden model fingerprints: repeated safety caveats, generic compliance language, unexplained refusal residue, "I cannot verify," fake browsing confidence, tool output pasted into prose, JSON fragments, Markdown tables from prompts, hallucinated anchors, broken footnotes, synthetic URLs, and placeholder source names.

**Why suspicious:** Newer model workflows mix generation, tools, citations, and wrappers. Artifacts may survive even after surface editing.

**False positives:** Technical docs may intentionally include JSON, tables, warnings, or limitations.

**Rewrite or detection tactic:** Verify every citation, URL, and claim. Remove tool scaffolding. Preserve machine-readable examples only when they are part of the deliverable.

**Example:**

- Before: "According to search result [3], the 2024 CNCF survey reports adoption at 38 percent, so this is widely adopted."
- After: "The 2024 CNCF survey reports adoption at 38 percent."

## 16. Openings, closings, and transition residue

**Watch for:** Formulaic openings such as "In today's fast-paced world," "As technology continues to evolve," "In an era where," or "It goes without saying." Watch fake-candid hooks and pause-and-reveal fragments, including the standalone question "Honestly?" and phrases such as "Look," "Here's the thing," "The thing is," "Let's be honest," or "Real talk," when they precede an ordinary claim without changing its stance or meaning. Meta-announcements such as "Let's dive in," "Let's explore," "Let's break this down," "Here's what you need to know," "Now let's look at," and "Without further ado" announce the next point instead of presenting it. Treat "a deep dive into" as the same pattern when it promises depth instead of establishing useful scope. Casual recastings such as "Heads up," "Quick note," and "Before I forget" have the same defect when they serve only as introductions. Formulaic closings include "The future looks bright," "Only time will tell," "This is just the beginning," and "Exciting times lie ahead." Overused transitions include "Moving forward," "Furthermore," "Additionally," "Moreover," and "In conclusion."

**Why suspicious:** These phrases can buy time, simulate candor, make an ordinary point sound consequential, or replace content with commentary about the content. A casual register does not repair an announcement whose only job is to introduce the next point.

**False positives:** Dialogue, speeches, personal essays, informal correspondence, advertising, and an established authorial voice may use conversational openers naturally. An opener can mark a genuine concession, correction, disagreement, or personal admission. School essays and formal articles may require explicit transitions; long documents, procedures, presentations, and accessibility-oriented writing may need signposting. Warnings and navigation cues are functional when they change what the reader notices or does.

**Rewrite or detection tactic:** Remove the framing as a test. If the claim, stance, sequence, and reader guidance remain intact, state the point directly. Preserve an opener or signpost when it carries a real change in attitude, navigation, warning, sequence, or accessibility; express that function in natural syntax or functional formatting. Start with the claim, scene, question, or fact; use transitions only when they clarify a relationship; and end on the most useful consequence rather than a generic moral.

**Examples:**

- Before: "Is it worth the price? Honestly? It depends on how often you'll use it."
- After: "Whether it's worth the price depends on how often you'll use it."
- Before (scripted): "Let's break down the retry policy. Here's what you need to know: the API retries a failed request twice."
- Before (casual): "Quick heads-up before we continue: the API retries a failed request twice."
- After either: "The API retries a failed request twice."
- Before: "The release fixed the login bug. Moving forward, the team will monitor error rates. Only time will tell whether the fix holds."
- After: "The release fixed the login bug. The team will monitor error rates. It is not yet clear whether the fix will hold."

## 17. Hedging, filler, and sycophancy

**Watch for:** Excessive or stacked hedging such as "could potentially," "may possibly," and "might arguably"; repeated fairness clauses such as "to be fair"; or several uncertainty markers attached to the same claim. Treat "it's also possible" and "this is an inference" as signals only when they add no distinct alternative, attribution, or epistemic status. Filler: "it is important to note," "in order to," "due to the fact that," "at this point in time." Sycophancy: "great question," "you are absolutely right," "excellent point," "I completely agree."

**Why suspicious:** Stacked qualifiers blur which limitation is real. Repeated cautious edits can leave a sentence defending against a stronger claim it no longer makes. Filler delays the point, while servile praise replaces substantive engagement.

**False positives:** Risk, medicine, law, science, and policy writing may need careful uncertainty or explicit inference labels, and a claim may need several qualifiers when each marks a different limit. Polite correspondence may need warmth.

**Rewrite or detection tactic:** Map each qualifier to certainty, scope, attribution, condition, or stance in the meaning contract. Keep every truth-changing limit, but express each one once. Collapse qualifiers that perform the same job. When a caveat only shields an unsupported stronger version of the claim, state the supported claim directly. Cut filler and servile praise; keep warmth when the genre requires it.

**Example:**

- Before: "To be fair, the change could potentially reduce latency in some cases, although this is only an inference from the benchmark."
- After: "The benchmark suggests that the change reduces latency in some cases."

## 18. Shadowboxing and phantom alternatives

**Watch for:** Unattributed defenses against positions the text never raises, or alternatives introduced only to be dismissed: "This isn't about," "I'm not saying" or "I'm not arguing," "To be clear," "Don't get me wrong," "This is not to say," "You could frame this differently, but," "Some might say... but," "A tempting approach would be," "One might be tempted to," "An obvious approach would be," "You might think... but," "It would be easy to just," and "Some would suggest." A phantom alternative usually appears nowhere else, is dismissed within a clause or two, and contributes no decision, constraint, evidence, or useful comparison. One occurrence is ambiguous; repeated digressions across unrelated points strengthen the pattern.

**Why suspicious:** Drafting can leave replies to objections and alternatives that the published argument no longer needs. The reader is forced to follow branches that do not advance the point.

**False positives:** An object-level negation is a claim: "The API is not thread-safe." Preserve a defense or alternative that documents an actual decision, explains a relevant tradeoff, establishes a constraint, answers an attributed objection, or compares options the reader genuinely needs to understand.

**Rewrite or detection tactic:** Ask what unique information the objection or alternative contributes. If the answer is none, remove the entire digression and reconnect the surrounding argument. If its rebuttal carries a real constraint or concession, state that claim affirmatively where it belongs. Keep genuine comparisons and counterarguments, and attribute them when attribution matters.

**Examples:**

- Before: "Some might frame this differently, but the parser fails when the input lacks a closing bracket."
- After: "The parser fails when the input lacks a closing bracket."
- Before: "The client retries a failed request twice. It would be easy to keep retrying until it succeeds, but the client stops after the second retry. It then returns the error to the caller."
- After: "The client retries a failed request twice, then returns the error to the caller."
- Before: "The importer validates the entire file before writing any records. An obvious approach would be to write each row as it is parsed, but a later error would leave a partial import. Invalid files add no records."
- After: "The importer validates the entire file before writing any records, so invalid files cannot leave a partial import."
- Keep: "The API is not thread-safe."

## 19. False-positive guardrails

Use these checks before flagging text:

- Does the suspected phrase appear alone, or in a cluster?
- Is the phrase required by a style guide, legal template, academic convention, accessibility pattern, or brand voice?
- Is the punctuation part of quoted/source text, a provided writing sample, house style, or a deliberate author habit?
- Does the sentence contain concrete detail despite the flagged phrase?
- Is the writer using a second language, dialect, or regional convention?
- Is the text a draft, outline, transcript, support reply, or generated artifact by design?
- Would rewriting remove useful precision, citation discipline, or the author's real voice?

If the answer is yes, soften the finding. Recommend a targeted edit, not a full rewrite. These guardrails protect existing human choices; they do not license adding AI-tell punctuation, formatting, or structure during a rewrite.

## Review rubric

Rate the prose by cluster strength, not presumed authorship. Weigh density, repetition across the piece, severity, and interaction between families. Concrete detail, distinctive voice, functional formatting, and genre conventions count as counterevidence.

- **Low concern:** A few isolated markers appear, while the prose remains specific, coherent, and suited to its genre.
- **Medium concern:** Multiple families recur or combine in ways that flatten voice, obscure claims, or make the structure feel generated.
- **High concern:** Strong provenance residue, prompt leakage, unsupported evidence, or dense interacting clusters affect much of the piece.

Report this as concern about the writing patterns. Prose alone cannot establish human or model authorship.
