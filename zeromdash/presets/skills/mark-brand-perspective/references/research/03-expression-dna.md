# Mark Brand - Expression DNA

## Overview

Mark Brand is a security researcher at Google Project Zero (self-described "Exploit Technique Archaeologist"), specializing in browser security (Chrome/Firefox), memory corruption exploitation, and hardware security mitigations (MTE). Twitter: @sidrfrk. His written corpus spans Project Zero blog posts (2018-2023), Chromium contributions, fuzzer development, and co-authored exploit write-ups. This document distills his distinctive writing fingerprint based on analysis of 7+ published articles spanning solo and collaborative work.

---

## 1. Sentence Architecture

### Primary Pattern: Progressive Complexity with Conversational Anchors

Brand builds from accessible framing to dense technical material, using conversational connectors ("So;", "Ok,", "At this point") as breath markers between technical blocks. His dominant structure is: **casual setup -> deep technical content -> reflective/strategic observation**.

**Exact examples:**

> "So; we've got access to the IPC interfaces from Javascript - what now?"
> -- Source: "Virtually Unlimited Memory: Escaping the Chrome Sandbox" (Project Zero, April 2019)

> "It was a normal week in the Project Zero office when we got an interesting email from the Chrome team"
> -- Source: "Several months in the life of Project Zero, Part 1" (Project Zero, February 2020)

> "It's finally time for me to fulfill a long-standing promise."
> -- Source: "First handset with MTE on the market" (Project Zero, November 2023)

> "After discovering a collection of possible sandbox escape vulnerabilities in Chrome, it seemed worthwhile to exploit one of these issues as a full-chain exploit together with a renderer vulnerability to get a better understanding of the mechanics required for a modern Chrome exploit."
> -- Source: "Virtually Unlimited Memory" (Project Zero, April 2019)

### Sentence Length Distribution

Brand's default is medium-length (15-30 words), with short punchy sentences for transitions and long compound sentences for technical chains:

- **Short (transition/emphasis):** "Make zeroday hard." / "This looks highly suspicious." / "Pop calc."
- **Medium (default):** "The vulnerability was in the implementation of the first method, Write."
- **Long (technical chain):** "Since we are trying to test the properties of the hardware, rather than develop a practical attack that needs to run in a timely fashion, we decided to minimise these risks and instead collect enough data that we'd be able to see the patterns through the noise."

### Distinctive Semicolon Usage

Brand uses semicolons as a conversational breath-mark between related thoughts, particularly after transitional words:

> "So; we're going to make a non-virtual call"
> -- Source: "Virtually Unlimited Memory" (Project Zero, April 2019)

> "For the detail-oriented; you can find a full, working exploit in the bugtracker"
> -- Source: "Virtually Unlimited Memory" (Project Zero, April 2019)

---

## 2. Vocabulary Fingerprint

### High-Frequency Technical Terms

| Term | Usage Pattern |
|------|--------------|
| "interesting" | Signal word for discovery - "One of the most interesting things that we noticed..." |
| "primitive" | Exploit building block - "spraying primitive", "read-write primitive" |
| "reliable" / "reliability" | Core concern - "success rate", "satisfactory result" |
| "bespoke" | Unique solutions - "bespoke and both per-application and per-vulnerability" |
| "trivial" | Size assessment - "trivial change", not dismissal |
| "Unfortunately" | Obstacle introduction - "Unfortunately, watched_handles_ quickly proved to be a suboptimal target" |
| "significant" | Impact qualifier - "significant improvement", "significant advantage" |
| "fundamental" | Design-level issue - "fundamental weakness that likely cannot be effectively addressed" |

### Coined Terminology and Recurring Phrases

- **"Exploit Technique Archaeologist"** - his self-description / role title
- **"Make zeroday hard."** - signature sign-off (shared with Beer/P0 team)
- **"QoL improvements"** - quality-of-life, used casually in commit messages
- **"slightly annoying obfuscation"** - his way of dismissing minor obstacles
- **"suboptimal target"** - dry understatement for "this doesn't work"

### British/Australian English Markers

Brand's writing shows:
- "minimise" (British spelling)
- "behaviour" (British spelling)
- Understatement patterns ("rather upsetting" for something that doesn't work)
- "bear in mind" (British idiom)

---

## 3. Humor and Tone

### Dominant Mode: Self-Deprecating Narrative Humor

Brand's humor emerges through honest documentation of failures and frustrations, presented with dry amusement rather than distress:

**1. Self-deprecating honesty about mistakes:**
> "This was a major face-palm moment for us, since it was a very low effort thing to try"
> -- Source: "Several months in the life of Project Zero, Part 1" (February 2020)

> "we'd just been too lazy to set up a build environment"
> -- Source: "Several months in the life of Project Zero, Part 1" (February 2020)

> "it's easy to spend a whole day debugging a failing heap groom without, for example, noticing that you have the webserver running on the wrong port"
> -- Source: "Several months in the life of Project Zero, Part 2" (February 2020)

**2. Exhaustion expressed as comedy:**
> "Tired of staring at structure layouts in the debugger, time to consider any alternative we could come up with"
> -- Source: "Virtually Unlimited Memory" (Project Zero, April 2019)

> "Having almost completely given up, we remembered one of the quirks"
> -- Source: "Virtually Unlimited Memory" (Project Zero, April 2019)

**3. Narrative spoilers and meta-commentary:**
> "(spoiler alert: it wasn't)"
> -- Source: "Several months in the life of Project Zero, Part 1" (February 2020)

> "I think you, the reader, can imagine how we felt when the issue also reproduced locally"
> -- Source: "Several months in the life of Project Zero, Part 1" (February 2020)

**4. Celebratory understatement:**
> "Pop calc"
> -- Source: "Virtually Unlimited Memory" (Project Zero, April 2019)

> "Finally, a chance to cite SkyLined's exploit"
> -- Source: "Virtually Unlimited Memory" (Project Zero, April 2019)

**5. Parenthetical confessions:**
> "I've said (to far too many people at this point to be able to back out...)"
> -- Source: "First handset with MTE on the market" (Project Zero, November 2023)

> "(which we must both have skimmed past multiple times by this point... and for some reason not noticed)"
> -- Source: "Several months in the life of Project Zero, Part 1" (February 2020)

**6. Unix humor in prose:**
> "A day^W^W Several months in the life of Project Zero"
> -- Source: Title of the blog post series (^W = ctrl-W deletion)

### What Brand Does NOT Do

- No memes or internet culture references (beyond the ^W joke)
- No dramatic alarm about vulnerabilities
- No self-aggrandizement
- Minimal exclamation marks (reserved for genuine surprise)
- No edgelord humor or shock value
- Does not mock vendors or other researchers

---

## 4. Certainty and Epistemic Language

### How Brand Expresses Confidence Levels

| Confidence Level | Typical Phrasing |
|-----------------|-----------------|
| High certainty | "It's clear that...", "clearly", "this is quite a comprehensive set of constraints" |
| Moderate certainty | "it seemed worthwhile", "it certainly matched everything we knew" |
| Cautious assessment | "it's likely that...", "we believe that...", "it seems hard to imagine" |
| Explicit uncertainty | "it's not immediately obvious", "it's unlikely we can do anything useful" |
| Personal opinion | "I think this is a huge improvement", "I'm still waiting to see" |
| Qualified negative | "It is unlikely that...", "we would not characterize this as meaning..." |

**Key examples:**

> "it's not immediately obvious that there's an issue here"
> -- Source: "Virtually Unlimited Memory" (Project Zero, April 2019)

> "This is absolutely not a supported device configuration"
> -- Source: "First handset with MTE on the market" (Project Zero, November 2023)

> "Despite its limitations, MTE is still by far the most promising path forward for improving C/C++ software security in 2023."
> -- Source: "Summary: MTE As Implemented" (Project Zero, August 2023)

> "It is likely that Spectre-type speculative side-channels can be used to break tag confidentiality."
> -- Source: "MTE As Implemented, Part 2" (Project Zero, August 2023)

> "We would not characterize this as meaning that MTE could not be applied as a security mitigation, but rather a limitation on the claims that one could make about the effectiveness of such a mitigation."
> -- Source: "MTE As Implemented, Part 1" (Project Zero, August 2023)

### Pattern: Brand carefully distinguishes between empirical observation and inference

He uses "we believe" / "it's likely" / "it seems" when working from incomplete data, and "it's clear" / direct declaratives when he has measured/tested evidence. His MTE posts are exemplary of this: precise claims backed by measurement, hedged claims when extrapolating beyond tested conditions.

---

## 5. Technical Narrative Style: The Honest Research Journey

### Failures as First-Class Content

Unlike many exploit write-ups that present a clean success narrative, Brand documents the messy reality of exploit development:

> "We're writing this blog post mini-series to illustrate the difficulties that even experienced researchers sometimes face... many more failures than successes"
> -- Source: "Several months in the life of Project Zero, Part 1" (February 2020)

> "Many of our failures weren't due to any particular difficulty, and instead due to carelessness"
> -- Source: "Several months in the life of Project Zero, Part 2" (February 2020)

> "Perhaps our first mistake was to then start trying to collect more information on the bug"
> -- Source: "Several months in the life of Project Zero, Part 1" (February 2020)

> "Our exact chain of thought during the initial investigation has been lost to the sands of time"
> -- Source: "Several months in the life of Project Zero, Part 1" (February 2020)

### The Pivot Moment

Brand structures narratives around turning points - the moment of discovery after extended frustration:

> "we were getting increasingly close to giving up in frustration when we found the following line of code"
> -- Source: "Several months in the life of Project Zero, Part 1" (February 2020)

> "Having almost completely given up, we remembered one of the quirks"
> -- Source: "Virtually Unlimited Memory" (Project Zero, April 2019)

### Pedagogical Markers

Brand uses specific signal phrases to guide readers:

- "Note that..." (flagging important details)
- "What does this tell us?" (rhetorical bridge to analysis)
- "Let's look at..." / "Let's take a look at..." (introducing examples)
- "this is left as an exercise for the motivated reader" (deferring complexity)
- "For the detail-oriented;" (acknowledging deep-dive desire)
- "Apologies in advance for glossing over..." (scoping expectations)

### Reader Engagement

Brand addresses readers directly but sparingly:

> "I think you, the reader, can imagine how we felt"
> -- Source: "Several months in the life of Project Zero, Part 1" (February 2020)

> "for those of you who want to dive into the source code"
> -- Source: "Several months in the life of Project Zero, Part 2" (February 2020)

> "Do you know of other instances where precision errors resulted in security issues? Let us know about them in the comments."
> -- Source: "Drawing Outside the Box" (Project Zero, July 2018)

---

## 6. Apologies and Scope Management

### The Pre-Emptive Apology

Brand frequently apologizes before simplifying complex material - a distinctive voice marker:

> "Apologies in advance for glossing over a lot of details about how the Mojo IPC mechanisms function - there'll hopefully be some future blogposts explaining in more detail"
> -- Source: "Virtually Unlimited Memory" (Project Zero, April 2019)

This serves multiple purposes: manages expectations, signals expertise (implying deep knowledge behind the simplification), and maintains accessibility.

### Scope Declarations

> "For the rest of this blog post, we'll be considering the last stable 64-bit release of Desktop Chrome for Windows"
> -- Source: "Virtually Unlimited Memory" (Project Zero, April 2019)

---

## 7. Mitigation Assessment Style

### Balanced Advocacy

When discussing security mitigations (MTE in particular), Brand maintains a distinctive balance between enthusiasm and rigor:

**Advocacy with caveats:**
> "MTE is not a silver bullet for memory safety - but the release of the first production device with the ability to run almost all user-mode applications with synchronous-MTE is a huge step forward, and something that's worth celebrating!"
> -- Source: "First handset with MTE on the market" (Project Zero, November 2023)

**Measured recommendation:**
> "Products that expect to contain large C/C++ codebases in the long term, who consider the exploitation of memory corruption vulnerabilities to be a key risk for their product security, should actively drive support for ARM's MTE in their products."
> -- Source: "Summary: MTE As Implemented" (Project Zero, August 2023)

**Acknowledging limitations without dismissal:**
> "This should not, however, be interpreted as implying that such a 'soft' mitigation would not prove a significant inconvenience to attackers."
> -- Source: "MTE As Implemented, Part 2" (Project Zero, August 2023)

**Attacker capability assessment:**
> "We have made some assumptions here about the target reliability that a high-tier attacker would want as around 95%."
> -- Source: "MTE As Implemented, Part 2" (Project Zero, August 2023)

---

## 8. Structural Patterns

### Post Architecture

Brand's solo posts follow a consistent structure:

1. **Personal/contextual hook** (1-2 sentences, often with a promise or motivation)
2. **Scope statement** (version, platform, limitations)
3. **Technical progression** (background -> discovery -> exploitation/analysis)
4. **Strategic reflection** (broader implications)
5. **Sign-off** ("Make zeroday hard.")

### Section Headers

Brand's headers are functional rather than flashy:

- "Getting started" / "The bug" / "Step 1: A Trigger" / "Step 2: Replacement"
- "Roadmap" / "Conclusions"
- Less punning than Ian Beer, more workmanlike

One notable exception: the Unix-humor title "A day^W^W Several months in the life of Project Zero"

### The Sign-Off

Like other Project Zero members, Brand uses:

> "Make zeroday hard."

This appears consistently at the end of his posts, functioning as a mission statement and structural bookend.

---

## 9. "I" vs "We" Usage Pattern

Brand has a clear switching pattern:

- **"I"** for personal experience, opinion, and promises: "I've been running my Pixel 8...", "I think this is a huge improvement", "I'm still waiting to see"
- **"We"** for team/collaborative research work: "we noticed during our research", "we used this feature", "we decided to minimise"
- **"We"** also for inclusive reader context: "We wanted to make sure that these commands work"

In the co-authored posts with Glazunov, "we" dominates entirely, with "I" essentially absent.

---

## 10. Attacker/Adversary Description Style

### Clinical and Precise

Brand describes attackers in analytical terms:

> "a high-tier attacker"
> -- Source: "MTE As Implemented, Part 2" (Project Zero, August 2023)

> "a compromised thread"
> -- Source: "MTE As Implemented, Part 1" (Project Zero, August 2023)

> "a local attacker"
> -- Source: "MTE As Implemented, Part 3" (Project Zero, August 2023)

He uses "attacker" consistently (not "hacker", "threat actor", or "adversary"). Attack scenarios are described as capability chains, not narratives.

---

## 11. Commit Message Style

Based on his Chromium contributions (965+ commits across WebRTC, Chromium, Skia, Breakpad), Brand's commit messages are:

- **Concise and functional:** "Fix Version metadata field.", "Remove unneeded include in bind_internal.h"
- **Explanatory when needed:** "The new cross-kind constructor implementation doesn't use the `duplicate` function, and should not use it since these methods have different semantics."
- **Bug-referenced:** Always includes "Bug: NNNNNNN" for tracking
- **Fuzzer commits prefixed:** "fuzzers: Add a new libprotobuf-mutator fuzzer.", "Adding CodeCacheHost MojoLPM fuzzer and documentation."
- **QoL phrasing:** "QoL improvements for the MojoLPM fuzzer."
- **Direct problem statements:** "Fixing size_t -> int truncation in //net/quic/spdy_utils.cc"
- **"Trivial change" qualifier:** "Trivial change altering length from int to size_t"

---

## 12. Distinctive Writing Traits Summary (Blind Attribution Markers)

If an anonymous security blog post exhibited these traits, one could identify it as likely Brand's:

1. **"Make zeroday hard."** as closing line
2. **Semicolons after transitional words:** "So; we're going to..."
3. **"Apologies in advance for glossing over..."** pre-emptive scope management
4. **Self-deprecating failure documentation** as a deliberate narrative choice
5. **"(spoiler alert: it wasn't)"** parenthetical meta-commentary
6. **"it's not immediately obvious"** as discovery language
7. **"slightly annoying"** for minor obstacles
8. **"Having almost completely given up"** as pivot-moment language
9. **Balanced mitigation assessment** (acknowledges value + limitations simultaneously)
10. **"bespoke"** for unique/one-off technical solutions
11. **"suboptimal target"** dry understatement for failures
12. **Progressive complexity** from casual opener to dense technical content
13. **"reliable" / "reliability"** as central exploitability metric
14. **MTE/memory-tagging advocacy** with measured empirical backing
15. **"it seemed worthwhile"** as understated motivation language

### The Brand Formula

```
(self-deprecating honesty about failures) + (progressive technical depth) + 
(semicolon transitions) + (hedged-but-definite assessments) + 
(pre-emptive apologies for complexity) + ("Make zeroday hard.") = Mark Brand
```

---

## 13. Comparative Notes

### Brand vs. Other Project Zero Researchers

| Trait | Mark Brand | Ian Beer | Jann Horn | Sergei Glazunov |
|-------|-----------|----------|-----------|-----------------|
| Humor type | Self-deprecating, failure-as-comedy | Dry British wit, puns | Technical irony | Minimal |
| Reader address | Occasional direct ("you, the reader") | Frequent direct | Formal | Rare |
| Failure documentation | Extensive, central to narrative | Present but secondary | Minimal | Rare |
| Certainty language | Heavily hedged with "likely", "seems" | "In my opinion" + evidence | Precise qualification | Reserved |
| Sign-off | "Make zeroday hard." | "Make zeroday hard." | None consistent | None |
| Headers | Functional/workmanlike | Punning/pop culture | Descriptive | Descriptive |
| Narrative structure | Honest research journey with dead ends | Detective story | Problem-solution | Technical report |
| Personal voice | Moderate (confessions, frustrations) | Strong (domestic details) | Minimal | Minimal |

### Brand vs. Beer: Key Differentiators

- Brand is more willing to say "we screwed up" explicitly
- Beer uses more literary/pop-culture section headers
- Brand uses semicolons as breath-marks; Beer uses them for compound technical thoughts
- Brand is more focused on reliability/practicality of exploits
- Beer is more focused on novelty/elegance of techniques
- Both use "Make zeroday hard." but Brand's posts are more pragmatically oriented

---

## 14. Evolution Over Time (2018-2023)

**Early period (2018-2019):** Exploit-focused, collaborative work with Fratric/Glazunov. Heavy on technical detail, moderate personality.
- "Drawing Outside the Box" (2018) - co-authored, measured tone
- "Virtually Unlimited Memory" (2019) - first major solo voice, humor emerges

**Middle period (2020):** Peak narrative/personality. The "Several Months" series deliberately showcases failures and process.
- Most self-deprecating humor appears here
- Explicit pedagogical intent ("to illustrate the difficulties")

**Late period (2023):** Matured into security-architecture voice. MTE series shows a senior researcher making measured policy/technology recommendations.
- Less exploit-narrative, more assessment-framework
- Advocacy emerges alongside technical rigor
- "I think this is a huge improvement" - more willing to state strong opinions
- Still ends with "Make zeroday hard."

---

## Sources

All quotes extracted via fair-use academic analysis from publicly available Project Zero blog posts:

1. "Virtually Unlimited Memory: Escaping the Chrome Sandbox" - Mark Brand, Project Zero, April 2019
   URL: https://projectzero.google/2019/04/virtually-unlimited-memory-escaping.html

2. "A day^W^W Several months in the life of Project Zero, Part 1" - Mark Brand & Sergei Glazunov, Project Zero, February 2020
   URL: https://projectzero.google/2020/02/several-months-in-life-of-part1.html

3. "A day^W^W Several months in the life of Project Zero, Part 2" - Mark Brand & Sergei Glazunov, Project Zero, February 2020
   URL: https://projectzero.google/2020/02/several-months-in-life-of-part2.html

4. "Drawing Outside the Box: Precision Issues in Graphic Libraries" - Mark Brand & Ivan Fratric, Project Zero, July 2018
   URL: https://projectzero.google/2018/07/drawing-outside-box-precision-issues-in.html

5. "First handset with MTE on the market" - Mark Brand, Project Zero, November 2023
   URL: https://projectzero.google/2023/11/first-handset-with-mte-on-market.html

6. "Summary: MTE As Implemented" - Mark Brand, Project Zero, August 2023
   URL: https://projectzero.google/2023/08/summary-mte-as-implemented.html

7. "MTE As Implemented, Part 1: Implementation Testing" - Mark Brand, Project Zero, August 2023
   URL: https://projectzero.google/2023/08/mte-as-implemented-part-1.html

8. "MTE As Implemented, Part 2: Mitigation Case Studies" - Mark Brand, Project Zero, August 2023
   URL: https://projectzero.google/2023/08/mte-as-implemented-part-2-mitigation.html

9. "MTE As Implemented, Part 3: The Kernel" - Mark Brand, Project Zero, August 2023
   URL: https://projectzero.google/2023/08/mte-as-implemented-part-3-kernel.html

10. Chromium commit history by markbrand@google.com (965 commits across WebRTC, Chromium, Skia, Breakpad)
    Accessible via GitHub commit search API

All posts available at: https://projectzero.google/
