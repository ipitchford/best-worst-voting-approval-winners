# Review summary (internal, AI-assisted)

This is a public summary of the internal checking of version 0.1.0, without scores. It is not peer review,
independent reproduction or formal verification. No human referee has assessed the paper.

## What was done (24-25 November 2026)

1. **One combined five-perspective Claude review** (editor, methodology with a line-by-line proof check, domain,
   readability, devil's advocate, with an editorial synthesis) on the 9-page source draft, with the reviewer's own
   computations. The load-bearing sources were read in full: Terzopoulou, Lang and Zwicker (2026), Kenig (2018),
   Baumeister and Rothe (2012, arXiv version) and Schrijver (2003) chapter 44.
2. **Clean replay** of the original and the revised scripts from fresh copies. The original scripts used bare
   `assert` statements, which Python skips under `-O`; the revised scripts raise explicit errors and fail under `-O`.
3. **One revision round with an extension.** A new six-candidate classification (Theorem 12) with exact certificates;
   split-ballot versions of the four- and five-candidate results; a context-first introduction, a model section, a
   results table, a worked example and a discussion of open problems.
4. **Verification re-review and a proof audit** of the new and rewritten proofs, with independent recomputation
   (including a linear program written from scratch that reproduces the four-, five- and six-candidate regions) and a
   second negative control. One major item was found and fixed: a sentence claimed that every mixture of rules with
   the property has it, which is true only for rational mixtures. Minor wording and attribution items were applied.

No Astra/Codex second-model review took place in this batch.

## Main objections and how they were handled

| Objection | Disposition |
|---|---|
| The four-candidate necessary form is already in Terzopoulou, Lang and Zwicker (note 11) | Credited in the abstract, introduction, results table and Theorem 10; novelty narrowed to sufficiency at four candidates and to five and six candidates |
| Calling the irrational-score result a "disproof" overstated it, since replication is the original authors' device for splitting ballots | Reframed: the conjecture is proved for split ballots (all real scores) and with replication (rational scores); Theorem 15 is presented as the difference between splitting and whole copies for irrational scores |
| Scripts relied on `assert`; independence of the vertex-case check was overstated | New verify_endpoints.py with explicit failures and the certificate digest; all scripts fail under `-O`; the text says the vertex-case script relies on the reductions in the proof |
| Provenance of the base-polytope tool; possible-winner literature | Edmonds and Schrijver chapter 44 credited; Baumeister and Rothe (2012) and Kenig (2018) cited in Related work, with the difference in question stated |
| Notation clashes and hard-to-follow passages | Symbols renamed throughout; the network-flow step explained |
| "Every mixture" of rules with the property (re-review) | Restricted to rational mixtures |
| A context citation (García-Lapresta, Marley and Martínez-Panero, 2010) was not checked against the article itself | Removed; it supported only a context sentence |

## Limits of this checking

No human specialist or editorial review; no independent reproduction by an unaffiliated party; no proof-assistant
formalisation; literature search of limited scope. The scripts check the exact certificates, witness profiles and
small cases; the general theorems rest on the written proofs.
