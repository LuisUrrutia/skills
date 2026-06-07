# AI-writing pattern detection catalog

Use this reference for comprehensive review, audit, or rewrite work. It expands the quick checks in `SKILL.md` without changing the main rule: clusters beat isolated false positives.

## Detection principles

- Look for density, repetition, and interaction. One generic phrase can be human. Five generic phrases stacked with tidy structure and no concrete detail is suspicious.
- Preserve house style. Formal, academic, legal, technical, multilingual, or accessibility-oriented prose can sound controlled without being AI-written.
- Separate detection from judgment. A pattern means "review this," not "accuse the author."
- Prefer concrete repairs. Replace puffery with facts, vague authority with named sources, and chatbot framing with content.
- In rewrite mode, confirmed AI tells become output constraints. Preserve legitimate source style, but do not recreate diagnosed patterns in generated wording.
- Keep the user's facts, citations, names, numbers, quoted text, code, and domain terms unless asked to change them.

## 1. Language and lexical tells

**Signal:** Clusters of statistically common AI words and phrases: "delve," "realm," "landscape," "tapestry," "pivotal," "crucial," "robust," "seamless," "underscore," "foster," "garner," "enhance," "valuable," "comprehensive," "transformative," "ever-evolving," "plays a key role," "at the forefront."

**Why suspicious:** These words often appear where plain verbs or concrete nouns would do. AI drafts lean on broadly applicable words that fit many topics but add little.

**False positives:** Academic argument, brand copy, grant proposals, institutional reports, and translated prose may use this vocabulary as house style. Do not flag a single word if the surrounding sentence is specific.

**Rewrite or detection tactic:** Replace broad language with the actual action, actor, result, or evidence. If no specific claim remains, cut the sentence.

**Example:**

- Before: "The initiative plays a crucial role in fostering innovation across the evolving AI landscape."
- After: "The program funds six AI safety labs and publishes their evaluation results."

## 2. Significance and notability padding

**Signal:** Inflated importance: "serves as a testament," "marks a pivotal moment," "stands as a reminder," "reflects broader trends," "leaves an indelible mark," "contributes to the ongoing legacy." Also watch source-listing as importance: "covered by Forbes, Wired, TechCrunch, and local media" without explaining what the coverage established.

**Why suspicious:** AI writing often adds significance claims to make ordinary facts sound article-worthy. It may confuse mention, coverage, and importance.

**False positives:** Obituaries, historical analysis, awards pages, investor materials, or encyclopedia drafts may need significance framing. The problem is unsupported framing, not significance itself.

**Rewrite or detection tactic:** Ask what changed, who said so, and what evidence proves it. Name the source and claim, or remove the importance wrapper.

**Example:**

- Before: "The launch marks a pivotal shift in how teams collaborate."
- After: "After the launch, teams could edit the same document at the same time."

## 3. Promotional and SEO tone

**Signal:** Advertisement language: "boasts," "nestled," "renowned," "breathtaking," "must-visit," "world-class," "cutting-edge," "game-changing," "unlock," "supercharge," "elevate," "revolutionize," "seamless experience," "designed to help you thrive."

**Why suspicious:** AI systems trained on marketing pages often slide into brochure copy, especially for products, places, culture, travel, education, and SaaS.

**False positives:** Landing pages and product copy may intentionally sell. Even there, vague praise still weakens the piece.

**Rewrite or detection tactic:** Convert praise into features, constraints, proof, or user outcomes. Cut adjectives that cannot be verified.

**Example:**

- Before: "Our platform delivers a seamless, world-class experience."
- After: "The app saves drafts offline and syncs them when the connection returns."

## 4. Grammar and syntax tics

**Signal:** Copula avoidance and ornate substitutions: "serves as," "stands as," "represents," "boasts," "features" where "is" or "has" is clearer. Also watch forced parallelism, "not only...but also," "it's not just X, it's Y," false "from X to Y" ranges, and sentence-ending `-ing` clauses such as "highlighting," "showcasing," "underscoring," "ensuring," "reflecting."

**Why suspicious:** AI often avoids direct sentences and adds trailing clauses that pretend to analyze rather than add facts.

**False positives:** Some academic and legal prose uses nominal style. Some `-ing` clauses are normal and precise.

**Rewrite or detection tactic:** Try the simple version. If the sentence improves with "is" or "has," use it. If a trailing clause is fake analysis, cut it, fold it into the sentence, or start a new sentence only when that is the most natural connection. Split false ranges into a list of actual topics.

**Example:**

- Before: "The report serves as a roadmap for leaders, highlighting the importance of alignment."
- After: "The report gives leaders a roadmap and recommends weekly budget reviews."

## 5. Structure and outline artifacts

**Signal:** Formulaic sections: "Introduction," "Background," "Key Takeaways," "Challenges and Future Prospects," "Conclusion," "Final Thoughts," even when the content is short. Repeated paragraph shape: broad claim, generic explanation, neat closing sentence. Watch paragraph-closing "whether" summaries: "Whether you're a founder, marketer, or student, this tool can help."

**Why suspicious:** AI drafts often start from an outline template and fill each slot with safe generalities.

**False positives:** Reports, docs, course materials, and regulated formats may require predictable sections.

**Rewrite or detection tactic:** Keep useful headings, cut template headings, and lead with the real point. Let paragraphs end when the evidence ends.

**Example:**

- Before: "In conclusion, whether you are starting out or scaling up, the future of productivity is bright."
- After: "The next release adds shared folders and admin audit logs."

## 6. Formatting tells

**Signal:** Overuse of bold inline labels, emoji bullets, title-case headings in casual prose, boxed takeaway lists, excessive blockquotes, em dash characters (`—`) as default idea connectors, too many colons, mechanical tables, curly quotes in otherwise plain text, invisible Unicode, nonbreaking spaces, zero-width characters, smart punctuation that differs from the file style, and repeated Markdown fences without need.

**Why suspicious:** Chatbots often overformat to look organized. Some tools also introduce hidden or typographic characters during generation.

**False positives:** Style guides may require title case, curly quotes, tables, or callouts. Accessibility docs may use consistent labels for scanning.

**Rewrite or detection tactic:** Match the destination format. Remove decorative formatting. Normalize invisible or inconsistent characters when editing files, but preserve intentional typography in published copy. Do not introduce em dashes unless quoted/source text, a provided writing sample, house style, or the user's explicit preference calls for them. When replacing dash-heavy AI prose, repair the connection between ideas with subordinate clauses, conjunctions, commas, colons, semicolons when natural, reordered clauses, or paragraph flow rather than chopping every link into a period.

**Example:**

- Before: "**Innovation:** The company is pushing boundaries."
- After: "The company added image search and team permissions."

## 7. Chatbot residue

**Signal:** Conversational scaffolding left in content: "Great question," "Certainly," "Of course," "I hope this helps," "Let me know if you'd like," "Here is a revised version," "As an AI," "I can't browse," "based on my training," "as of my last update," "up to my knowledge cutoff." Also watch leaked prompts, placeholders, reasoning notes, "[insert citation]," "turn0search," citation brackets, tool traces, and AI-generated UTM parameters.

**Why suspicious:** These are direct artifacts from a chat session or generation tool, not natural content.

**False positives:** Emails and support replies may use friendly openings. Technical notes may mention model limits on purpose.

**Rewrite or detection tactic:** Remove the interface layer. Keep only the content the reader came for. If a limitation matters, state the real limitation and source.

**Example:**

- Before: "Certainly. Here is an overview of the policy. I hope this helps."
- After: "The policy requires manager approval for expenses over $500."

## 8. Context contamination and prompt leakage

**Signal:** Text refers to instructions, roles, files, or constraints that should not be visible to the reader: "as requested," "following your prompt," "the user wants," "this section should," "TODO: verify," "maintain a professional tone," "do not mention," "make it sound human," or unrelated context from another task.

**Why suspicious:** AI outputs can blend the task prompt, hidden instructions, earlier messages, or examples into the final prose.

**False positives:** Draft notes, editorial comments, and changelogs may intentionally mention requirements.

**Rewrite or detection tactic:** Remove production instructions from reader-facing copy. If the note is useful, move it to a comment, issue, or editorial checklist.

**Example:**

- Before: "This section should reassure users that the migration is simple."
- After: "Most teams can finish the migration in one afternoon."

## 9. Academic and citation patterns

**Signal:** Unsupported literature gestures: "scholars have long debated," "research suggests," "studies show," "it is widely recognized," "the literature highlights." Watch fabricated precision, citations that do not support the sentence, excessive hedging, source laundering, and generic transitions between papers.

**Why suspicious:** AI often mimics academic style without doing the evidentiary work. It can preserve citation shape while weakening source accuracy.

**False positives:** Academic writing needs careful hedging, field framing, and citation density. Formality alone is not suspicious.

**Rewrite or detection tactic:** Keep claims tied to cited sources. Replace vague field claims with named authors, dates, methods, or findings. Do not invent sources.

**Example:**

- Before: "Recent studies highlight the importance of motivation in learning outcomes."
- After: "Deci and Ryan's self-determination theory links autonomy and competence to motivation."

## 10. Social and LinkedIn cliches

**Signal:** Platform formulas: "I am thrilled to announce," "humbled and honored," "big news," "after months of hard work," "here's what I learned," "agree?" "thoughts?" "comment below," "build in public," "founder journey," "10 lessons from," "I used to think X, then Y changed everything."

**Why suspicious:** AI-generated social posts often imitate engagement bait and thought-leader cadence.

**False positives:** LinkedIn has native conventions. A person may actually be announcing a job, grant, launch, or award.

**Rewrite or detection tactic:** Make it sound like the actual person. Use the real detail, one honest reaction, and no engagement bait unless the user wants it.

**Example:**

- Before: "I am humbled and honored to share this exciting milestone."
- After: "I joined the infrastructure team at Render this week. Nervous, excited, and ready to learn."

## 11. Content density and treadmill restatement

**Signal:** Low-information sentences that restate the heading or previous line: "This is important because it matters," "The tool helps teams work better," "These benefits can improve outcomes." Watch paragraphs that keep moving but do not add names, numbers, examples, mechanisms, tradeoffs, or stakes.

**Why suspicious:** AI can maintain fluent motion while avoiding commitment. The prose feels smooth, but the reader learns little.

**False positives:** Executive summaries and abstracts may compress detail by design. Transitional sentences can be useful.

**Rewrite or detection tactic:** Demand one new unit of information per sentence. Add a fact, example, mechanism, or consequence. If none exists, delete.

**Example:**

- Before: "Better onboarding improves the employee experience and creates a stronger workplace."
- After: "New hires now get their laptop, payroll login, and first-week schedule before day one."

## 12. Statistical and rhythm tells

**Signal:** Metronomic sentence length, uniform paragraph size, low burstiness, repeated transition placement, too-even punctuation, smooth but predictable cadence, low type-token variety, or weirdly high synonym variety from synonym cycling.

**Why suspicious:** AI prose often has a statistically even rhythm. It may avoid fragments, sharp turns, long messy sentences, or honest pauses.

**False positives:** Technical manuals, policies, abstracts, and style-guide-compliant docs may deliberately use steady rhythm.

**Rewrite or detection tactic:** Read aloud. Vary sentence length only where it helps meaning. Use direct repetition when it is clearer than synonym swaps.

**Example:**

- Before: Four consecutive paragraphs each have three medium sentences ending with a broad takeaway.
- After: Merge repeated points, add one concrete example, and let one paragraph end on the fact.

## 13. Multilingual and translation artifacts

**Signal:** Literal calques, overly formal register, unnatural idioms, English AI phrases translated word for word, inconsistent pronouns, mixed punctuation norms, overexplained cultural context, or machine-like preservation of source sentence order.

**Why suspicious:** AI translation and multilingual rewriting can flatten voice and import English chatbot patterns into other languages.

**False positives:** Second-language writing, regional dialect, code-switching, and formal localization can look unusual to outsiders. Do not erase identity or dialect.

**Rewrite or detection tactic:** Match the target language, region, and audience. Preserve intentional code-switching. Fix only unnatural phrasing, generic padding, and imported chatbot structure.

**Example:**

- Before: "Es importante notar que esta herramienta facilita un paisaje robusto de productividad."
- After: "Esta herramienta ayuda a organizar tareas y revisar avances."

## 14. Emerging model artifacts

**Signal:** Hidden model fingerprints: repeated safety caveats, generic compliance language, unexplained refusal residue, "I cannot verify," fake browsing confidence, tool output pasted into prose, JSON fragments, Markdown tables from prompts, hallucinated anchors, broken footnotes, synthetic URLs, and placeholder source names.

**Why suspicious:** Newer model workflows mix generation, tools, citations, and wrappers. Artifacts may survive even after surface editing.

**False positives:** Technical docs may intentionally include JSON, tables, warnings, or limitations.

**Rewrite or detection tactic:** Verify every citation, URL, and claim. Remove tool scaffolding. Preserve machine-readable examples only when they are part of the deliverable.

**Example:**

- Before: "According to search result [3], this is widely adopted."
- After: "The 2024 CNCF survey reports adoption at 38 percent."

## 15. Openings, closings, and transition residue

**Signal:** Formulaic openings: "In today's fast-paced world," "As technology continues to evolve," "In an era where," "It goes without saying." Formulaic closings: "The future looks bright," "Only time will tell," "This is just the beginning," "Exciting times lie ahead," "Moving forward." Overused transitions: "Furthermore," "Additionally," "Moreover," "In conclusion."

**Why suspicious:** These phrases buy time and sound polished without giving the reader content.

**False positives:** Speeches, school essays, and highly formal articles may use explicit transitions. Some readers need signposting.

**Rewrite or detection tactic:** Start with the claim, scene, question, or fact. End on the most useful consequence, not a generic moral.

**Example:**

- Before: "In today's fast-paced digital world, cybersecurity is more important than ever."
- After: "The breach exposed 42,000 customer records."

## 16. Hedging, filler, and sycophancy

**Signal:** Excessive hedging: "could potentially," "may possibly," "it might be argued." Filler: "it is important to note," "in order to," "due to the fact that," "at this point in time." Sycophancy: "great question," "you are absolutely right," "excellent point," "I completely agree."

**Why suspicious:** AI assistants often overqualify, over-explain, and flatter the user.

**False positives:** Risk, medicine, law, science, and policy writing may need careful uncertainty. Polite correspondence may need warmth.

**Rewrite or detection tactic:** Keep necessary uncertainty. Cut stacked qualifiers and servile praise. Say the point plainly.

**Example:**

- Before: "It could potentially be argued that this may possibly reduce costs."
- After: "This may reduce costs."

## 17. False-positive guardrails

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

For audit work, score by clusters rather than isolated words:

- **Low concern:** One or two common phrases, but the text has concrete detail, natural rhythm, and no chatbot residue.
- **Medium concern:** Several families appear together, such as AI vocabulary, generic structure, and low content density.
- **High concern:** Chatbot residue, prompt leakage, fabricated or weak citations, formulaic structure, and generic language appear across the piece.

## Rewrite checklist

- Replace importance claims with facts or sourced claims.
- Replace vague adjectives with observable details.
- Cut chatbot framing and prompt residue.
- Keep formal, technical, academic, multilingual, and house-style choices when they are legitimate.
- Vary rhythm without adding fake personality.
- Remove generated AI-tell punctuation and formatting, including unnecessary em dashes, without flattening flow into choppy period-stacked prose.
- Preserve the user's facts, citations, code, quoted text, and constraints.
