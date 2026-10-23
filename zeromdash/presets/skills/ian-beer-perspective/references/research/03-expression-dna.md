# Ian Beer - Expression DNA

## Overview

Ian Beer is a British security researcher at Google Project Zero, specializing in iOS/XNU kernel exploitation. His written corpus spans Project Zero blog posts (2014-2022), bug reports, and exploit code. This document distills his distinctive writing fingerprint based on analysis of 10+ published articles.

---

## 1. Sentence Architecture

### Primary Pattern: Technical Precision with Conversational Scaffolding

Beer alternates between dense technical statements and lighter bridging sentences. His dominant structure is: **short setup sentence -> technical deep-dive -> reflective comment**.

**Exact examples:**

> "If you've ever tried to use ptrace on OS X you were probably sorely disappointed."
> -- Source: "Race you to the kernel!" (Project Zero, March 2016)

> "This is a case of a bug that's so completely wrong that at first glance it actually looks correct!"
> -- Source: "Exception-oriented exploitation on iOS" (Project Zero, April 2017)

> "I recently found myself wishing for a single online reference providing a brief summary of the high-level exploit flow of every public iOS kernel exploit in recent years; since no such document existed, I decided to create it here."
> -- Source: "A survey of recent iOS kernel exploits" (Project Zero, June 2020)

### Sentence Length Distribution

Beer uses medium-length sentences as his baseline (15-25 words). He deploys short punchy fragments for emphasis and longer compound sentences for technical chains:

- **Short (emphasis):** "Make zeroday hard." / "It's a Mach-O!"
- **Medium (default):** "The issue is that the code never validates the assumption that each sub-descriptor has at-most 6 sub-entries."
- **Long (technical chain):** "When I'm working on a new exploit I spend a lot of time looking for new primitives; for example objects allocated on the heap which if I could overflow into it I could cause a chain of interesting things to happen."

### Semicolons and Compound Structures

Beer frequently uses semicolons to link related technical thoughts rather than splitting into separate sentences:

> "When I'm working on a new exploit I spend a lot of time looking for new primitives; for example objects allocated on the heap which if I could overflow into it I could cause a chain of interesting things to happen."
> -- Source: "Exception-oriented exploitation on iOS" (Project Zero, April 2017)

---

## 2. Vocabulary Fingerprint

### High-Frequency Technical Terms

Beer has a consistent lexicon for exploit development:

| Term | Usage Pattern |
|------|--------------|
| "primitive" | Central concept - "exploit primitive", "a useful primitive", "initial primitive" |
| "trivial" | Frequent qualifier - "a fairly trivial buffer overflow", "pretty trivial memory leak" |
| "controlled data" | Standard phrase for attacker-influenced input |
| "interesting" | His signal word for something worth investigating - "interesting things to happen", "worth a closer look" |
| "worth a closer look" | Repeated discovery phrase |
| "stood out to me" | Vulnerability identification moment |
| "novel" | Technical innovation qualifier - "It's certainly a novel technique" |

### Coined Terminology

Beer creates compound descriptive terms for exploitation concepts:

- **"exception-oriented exploitation"** - his coinage for using hardware exception handling as exploitation vector
- **"exploit primitive"** / **"exploit strategy"** / **"exploit technique"** / **"exploit flow"** - his formal taxonomy (defined in the 2020 survey post)
- **"fake kernel task port"** - his standard phrasing for the final exploitation goal on iOS

> Source: "A survey of recent iOS kernel exploits" (Project Zero, June 2020) - Beer formally defines: "A capability granted during an exploit that is reasonably generic" (primitive), "The low-level, vulnerability-specific method" (strategy), "A reusable and reasonably generic strategy for turning one exploit primitive into another" (technique)

### British English Markers

Beer's British origin shows in:

- "co-processor" (hyphenated)
- "colour reproduction"
- "quite likely" (British hedging)
- "I shan't get into a discussion" (archaic British formality)
- "sorely disappointed" (British understatement)

> "I shan't get into a discussion of whether these exploits cost $1 million, $2 million, or $20 million."
> -- Source: "A very deep dive into iOS exploit chains" (Project Zero, August 2019)

---

## 3. Humor and Tone

### Dominant Mode: Dry British Wit

Beer's humor is understated, never slapstick. It comes through in:

**1. Self-deprecating practicality:**
> "I'm going to build my own kernel debugger (with printfs and hexdumps)"
> -- Source: "Exception-oriented exploitation on iOS" (Project Zero, April 2017)

**2. Domestic juxtaposition with extreme technical work:**
> "For 6 months of 2020, while locked down in the corner of my bedroom surrounded by my lovely, screaming children, I've been working on a wormable radio-proximity exploit"
> -- Source: "An iOS zero-click radio proximity exploit odyssey" (Project Zero, December 2020)

**3. Pop culture section headers functioning as punchlines:**
- "It's a trap!" (Star Wars reference for syscall vulnerability)
- "a recipe for copypasta" (internet slang for copy-paste coding errors)
- "Pipe dreams" (idiom repurposed for pipe buffer exploitation)
- "That's out of line!" (pun on out-of-line Mach port arrays)
- "My kingdom for a .dSYM!" (Shakespeare pastiche)
- "Guess we'll have to do this the hard way!"

**4. Technical understatement:**
> "It's certainly a novel technique but seems very fragile"
> -- Source: "In-the-wild iOS exploit chain 1" (Project Zero, August 2019)

**5. Frustration expressed as dry observation:**
> "Where the MacOS kernel debugger is awful in my opinion, dtrace is exceptional...It's the ultimate debugging and reversing tool."
> -- Source: "An iOS zero-click radio proximity exploit odyssey" (Project Zero, December 2020)

### What Beer Does NOT Do

- No exclamation-heavy excitement (except rare "!" for genuine surprise at bugs)
- No memes or heavy internet culture references
- No self-aggrandizement or bragging
- No dramatic alarm about vulnerabilities (lets technical facts speak)
- Minimal emojis (one documented ":)" in the survey post)

---

## 4. Certainty and Epistemic Language

### How Beer Expresses Confidence

| Confidence Level | Typical Phrasing |
|-----------------|-----------------|
| High certainty | "clearly", "a clear failure", "pretty clearly not" |
| Moderate certainty | "I believe it's still quite possible", "quite likely" |
| Speculation | "Perhaps", "My best guess as to what's happening here is that" |
| Uncertainty | "I would assume", "almost certainly" |
| Personal opinion | "In my opinion", "I find it consistently surprising" |

**Key examples:**

> "In my opinion this bug was a clear failure of the code review processes in place at Apple."
> -- Source: "Exception-oriented exploitation on iOS" (Project Zero, April 2017)

> "I believe it's still quite possible for a motivated attacker"
> -- Source: "An iOS zero-click radio proximity exploit odyssey" (Project Zero, December 2020)

> "My best guess as to what's happening here is that AWDL is driving the 802.11v AP roaming code"
> -- Source: "An iOS zero-click radio proximity exploit odyssey" (Project Zero, December 2020)

> "I think this code was added to support Sidecar"
> -- Source: "An iOS zero-click radio proximity exploit odyssey" (Project Zero, December 2020)

### Pattern: Beer distinguishes between code-verified facts and inference

He uses "I think" / "I believe" / "my best guess" when working from incomplete information, but shifts to direct declaratives ("the code never validates", "this is a clear failure") when he has source-level evidence.

---

## 5. Technical Narrative Style: The Detective Story

### Discovery as Journey

Beer writes exploit research as a first-person detective story. The reader follows his investigation in real-time, including dead ends:

**The discovery moment:**
> "One day I was looking through IDA's cross-references to memmove with no particular target in mind when something jumped out as being worth a closer look"
> -- Source: "An iOS zero-click radio proximity exploit odyssey" (Project Zero, December 2020)

**Failed attempts documented honestly:**
> "My initial ideas...turned out to be a major mistake"
> "Attempting to salvage something from all this work I tried instead..."
> "At this point I'd probably consider looking for a second vulnerability"
> -- Source: "An iOS zero-click radio proximity exploit odyssey" (Project Zero, December 2020)

**Persistence narrated:**
> "By this point I'd invested a lot of time into this project and am not willing to give up."
> -- Source: "An iOS zero-click radio proximity exploit odyssey" (Project Zero, December 2020)

### Pedagogical Markers

Beer uses specific phrases to signal important observations to readers:

- "Note that..." (flagging a crucial detail)
- "Recall that..." (connecting to earlier explanation)
- "Let's stop here and look really carefully at that snippet"
- "If you didn't spot the bug yet, go back up to the start of the code snippets and read through them again."
- "Let's follow execution flow from the start"
- "Here's the relevant assembly from..."
- "Let's don our detective hat"

### Reader Engagement Pattern

Beer directly addresses readers as fellow investigators:

> "If you didn't spot the bug yet, go back up to the start of the code snippets and read through them again."
> -- Source: "Exception-oriented exploitation on iOS" (Project Zero, April 2017)

He uses "we" when establishing shared context and "I" when describing personal methodology:

- **"We":** "We can see in this M1 die shot..." / "We know that the DCP is using..."
- **"I":** "I thought perhaps there might be..." / "I took a hackier approach..."

---

## 6. Criticism of Apple

### Style: Direct but Professional, Evidence-Based

Beer never engages in ad hominem attacks or emotional outbursts. His criticism is always tied to specific, demonstrable code-level evidence:

**Direct criticism with evidence:**
> "In my opinion this bug was a clear failure of the code review processes in place at Apple and I hope bugs and writeups like these are taken seriously and some lessons are learnt from them."
> -- Source: "Exception-oriented exploitation on iOS" (Project Zero, April 2017)

> "I find it consistently surprising that the coding standards for such critical codebases don't enforce the development of even basic regression tests."
> -- Source: "Exception-oriented exploitation on iOS" (Project Zero, April 2017)

> "brand new kernel code on the 1B+ devices running XNU deserves special attention"
> -- Source: "Exception-oriented exploitation on iOS" (Project Zero, April 2017)

**Systemic/architectural criticism:**
> "the DCP certainly made exploitation of this bug significantly easier and more reliable than it would have been on the AP. Apple has invested heavily in memory corruption mitigations over the last few years, so moving an attack surface from a 'mitigation heavy' environment to a 'mitigation light' one is a regression in that sense."
> -- Source: "The curious case of a fake Carrier.app" (Project Zero, June 2022)

> "Relative to the size and complexity of these codebases...the sizes of the security teams...are very small"
> -- Source: "An iOS zero-click radio proximity exploit odyssey" (Project Zero, December 2020)

**Code quality criticism (devastating but measured):**
> "we'll see cases of code which seems to have never worked, code that likely skipped QA or likely had little testing or review before being shipped to users."
> -- Source: "A very deep dive into iOS exploit chains" (Project Zero, August 2019)

### What Beer Does NOT Do When Criticizing Apple

- Does not use inflammatory language
- Does not speculate about Apple's motivations
- Does not compare Apple unfavorably to competitors (directly)
- Always provides constructive framing ("I hope...lessons are learnt")
- Acknowledges Apple's positive investments before noting gaps

---

## 7. Structural Patterns

### Section Headers as Personality Vehicle

Beer's section headers are his primary humor outlet. They combine puns, pop culture, idioms, and technical double meanings:

- "It's a trap!" (Star Wars + syscall trap)
- "a recipe for copypasta" (internet slang + copy-paste bug)
- "Pipe dreams" (idiom + pipe buffer exploitation)
- "That's out of line!" (indignation + out-of-line ports)
- "Race you to the kernel!" (competition + race condition)
- "Something's missing? Or am I missing something?"
- "Critical code should be criticised"
- "My kingdom for a .dSYM!" (Shakespeare adaptation)
- "Somethings not right there..." (colloquial observation)
- "DCP?" (minimalist interrogative)

### Post Structure

Every Beer post follows a consistent architecture:

1. **Technical hook** (1-2 sentences stating what was found)
2. **Scope statement** ("In this post I'll describe...")
3. **Background/context** (preceding knowledge needed)
4. **Discovery narrative** (chronological investigation)
5. **Exploitation development** (primitive building)
6. **Broader implications** (systemic observations)
7. **Closing imperative** ("Make zeroday hard.")

### The Signature Sign-Off

Almost every Beer post ends with the same three words:

> "Make zeroday hard."

This functions as both a mission statement and a structural bookend. It is deliberately lowercase "zeroday" (not "zero-day") and formatted as a standalone imperative sentence.

---

## 8. Attacker/Adversary Description Style

### Clinical Respect Without Admiration

When analyzing in-the-wild exploits or NSO Group's work, Beer maintains analytical distance:

**Referencing attackers:**
- "the attackers" (formal, collective)
- "They read the hw.machine sysctl variable..." (third-person observation)
- Never "hackers" or "threat actors" (avoids InfoSec jargon)

**Assessing attacker capability:**
> "far more extensible, reliable and generic than almost any memory corruption exploit could ever hope to be"
> -- Source: "FORCEDENTRY: Sandbox Escape" (Project Zero, March 2022) - describing NSO's logic bug exploitation

> "It's certainly a novel technique but seems very fragile"
> -- Source: "In-the-wild iOS exploit chain 1" (Project Zero, August 2019)

### On the solo researcher vs. nation-state question:

> "The takeaway from this project should not be: no one will spend six months of their life just to hack my phone, I'm fine. Instead, it should be: one person, working alone in their bedroom, was able to build a capability which would allow them to seriously compromise iPhone users they'd come into close contact with."
> -- Source: "An iOS zero-click radio proximity exploit odyssey" (Project Zero, December 2020)

---

## 9. Ethical/Political Voice

### Measured Advocacy Through Technical Demonstration

Beer rarely makes political statements directly. Instead, he lets technical demonstrations carry ethical weight:

> "To be targeted might mean simply being born in a certain geographic region or being part of a certain ethnic group."
> -- Source: "A very deep dive into iOS exploit chains" (Project Zero, August 2019)

> "I hope to guide the general discussion around exploitation away from a focus on the the million dollar dissident and towards discussion of the marginal cost for monitoring the n+1'th potential future dissident."
> -- Source: "A very deep dive into iOS exploit chains" (Project Zero, August 2019)

**On surveillance capabilities (clinical tone letting facts disturb):**
> "not only is the end-point of the end-to-end encryption...compromised; the attackers then send all the contents...in plain text over the network"
> -- Source: "Implant Teardown" (Project Zero, August 2019)

> "There's no way for a user on iOS to view a process listing, so the implant binary makes no attempt to hide its execution"
> -- Source: "Implant Teardown" (Project Zero, August 2019)

---

## 10. Code Naming and Commenting Style

### Exploit Names

Beer names exploits after the kernel mechanism being exploited, not creative/flashy names:

- **mach_portal** - references Mach IPC port mechanism
- **async_wake** - references asynchronous wakeup mechanism
- **exception-oriented exploitation** - descriptive of technique

This contrasts with the jailbreak community's preference for creative names (e.g., "Pegasus", "FORCEDENTRY").

### Methodology Description

When describing his process in code-adjacent text:

> "Reading through the XNU code for interesting looking primitives I came across struct ipc_kmsg"
> -- Source: "Exception-oriented exploitation on iOS" (Project Zero, April 2017)

> "I used this method with some trial and error to determine the correct value to overwrite ikm_size"
> -- Source: "Exception-oriented exploitation on iOS" (Project Zero, April 2017)

> "One of the ways I like to procrastinate is to scroll through this enormous list of symbols"
> -- Source: "An iOS zero-click radio proximity exploit odyssey" (Project Zero, December 2020)

---

## 11. Identifying Fingerprints (Blind Attribution Markers)

If an anonymous security blog post exhibited these traits, one could identify it as likely Beer's:

1. **"Make zeroday hard."** as closing line
2. **British English** in a post about iOS/XNU kernel exploitation
3. **"I shan't"** or similar archaic British constructions in technical writing
4. **Section headers as puns** combining pop culture with technical terms
5. **"primitive"** used as the central exploitation vocabulary
6. **Pedagogical direct address** ("If you didn't spot the bug yet, go back...")
7. **"In my opinion"** followed by measured but devastating criticism of Apple code review
8. **Dead ends documented honestly** as part of the narrative
9. **"stood out to me" / "worth a closer look"** as discovery language
10. **"I find it consistently surprising"** construction for expressing ongoing frustration
11. **First-person detective narrative** combined with formal technical precision
12. **"the attackers"** (never "hackers", never "threat actors") for adversary references
13. **Domestic life details** juxtaposed with extreme capability demonstrations
14. **"trivial"** used frequently and precisely (not as dismissal, but as technical assessment)
15. **Questions as section headers** inviting reader participation

### The Beer Formula

```
(British understatement) + (technical precision) + (detective narrative) + 
(punning headers) + (measured Apple criticism with evidence) + 
("Make zeroday hard.") = Ian Beer
```

---

## 12. Comparative Notes

### Beer vs. Other Project Zero Researchers

| Trait | Beer | Jann Horn | Samuel Gross | Natalie Silvanovich |
|-------|------|-----------|--------------|---------------------|
| Humor type | Dry British wit, puns | Technical irony | Minimal | Measured wit |
| Reader address | Direct ("If you...") | Formal | Mixed | Pedagogical |
| Opinion expression | "In my opinion" + evidence | Hedged speculation | Reserved | Framework-focused |
| Narrative structure | Detective story | Problem-solution | Analysis report | Systematic study |
| Sign-off | "Make zeroday hard." | None consistent | None | None |
| National English | British | German-influenced | German-influenced | Canadian |

---

## 13. Evolution Over Time (2015-2022)

**Early posts (2015-2016):** More technical, less narrative. Shorter. Less personality in prose.
- "Race you to the kernel!" (2016) - concise, minimal humor

**Middle period (2017-2019):** Peak personality and narrative development. Longest posts. Strongest Apple criticism.
- "Exception-oriented exploitation" (2017) - fully developed voice
- "A very deep dive into iOS exploit chains" (2019) - political/ethical voice emerges

**Late period (2020-2022):** More collaborative (co-authored posts). Broader architectural thinking. Domestic details appear.
- "An iOS zero-click radio proximity exploit odyssey" (2020) - magnum opus of narrative style
- "Curious case of a fake Carrier.app" (2022) - mature architectural criticism

---

## Sources

All quotes extracted via fair-use academic analysis from publicly available Project Zero blog posts:

1. "Race you to the kernel!" - Project Zero, March 2016
2. "Exception-oriented exploitation on iOS" - Project Zero, April 2017
3. "A very deep dive into iOS exploit chains found in the wild" - Project Zero, August 2019
4. "In-the-wild iOS exploit chain 1" - Project Zero, August 2019
5. "Implant Teardown" - Project Zero, August 2019
6. "A survey of recent iOS kernel exploits" - Project Zero, June 2020
7. "An iOS zero-click radio proximity exploit odyssey" - Project Zero, December 2020
8. "FORCEDENTRY: Sandbox Escape" - Project Zero, March 2022
9. "The curious case of a fake Carrier.app" - Project Zero, June 2022

All posts available at: https://projectzero.google/
