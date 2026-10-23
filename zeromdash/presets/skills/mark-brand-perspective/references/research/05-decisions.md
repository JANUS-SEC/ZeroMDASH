# Mark Brand - Key Decisions and Research Choices

## Overview

Mark Brand is a security researcher at Google Project Zero, active since at least early 2015. His research spans Flash exploitation, Android media stack vulnerabilities, Chrome browser security (including IPC/Mojo, V8/typer bugs, network stack), memory tagging (MTE) evaluation, and most recently AI-assisted vulnerability discovery. He has been identified with humorous self-titles including "Bypasser of Mitigations," "Invalidator of Unicode," and "Exploit Technique Archaeologist."

---

## 1. Career and Research Evolution

### 1.1 Joining Project Zero and Early Focus (2015)

**Evidence:** Brand's earliest known Project Zero publication is from February 2015 (Flash PCRE exploit). By mid-2015 he was co-authoring with Chris Evans (then P0 manager) on Flash mitigations.

- Source: https://googleprojectzero.blogspot.com/2015/02/exploitingscve-2015-0318sinsflash.html
- Source: https://googleprojectzero.blogspot.com/2015/07/significant-flash-exploit-mitigations_16.html
- Confidence: HIGH (primary sources, authored posts)

**Inferred decision logic:** Brand joined Project Zero during its very early period (founded July 2014). His earliest work targeted Flash -- the dominant browser attack surface of that era. This suggests he was recruited for (or quickly developed) expertise in browser-reachable exploitation.

### 1.2 Shift from Flash to Android (2015-2016)

**Evidence:** By September 2015, Brand was publishing Android Stagefright exploitation research. By 2016, he published the libstagefright/libutils full exploit.

- Source: https://projectzero.google/2015/09/stagefrightened.html (CVE-2015-3864)
- Source: https://projectzero.google/2016/09/return-to-libstagefright-exploiting.html (CVE-2016-3861)
- Confidence: HIGH

**Inferred decision logic:** As Flash began declining in relevance and Adobe implemented mitigations (some co-designed by Brand himself), he pivoted to the next high-impact remote attack surface: Android media parsing. This shows a pattern of following where the highest-impact attack surface lives.

### 1.3 Shift to Chrome/Mojo (2018-2019)

**Evidence:** By 2018, Brand was researching Chrome's SwiftShader (WebGL) and by 2019 published his full-chain Chrome exploit using Mojo IPC.

- Source: https://projectzero.google/2018/07/drawing-outside-box-precision-issues-in.html
- Source: https://projectzero.google/2019/04/virtually-unlimited-memory-escaping.html
- Confidence: HIGH

**Explicit stated logic:** In the "Virtually Unlimited Memory" post, Brand described building a Mojo fuzzer using MojoJS bindings and discovering sandbox escape bugs through it. He chose Chrome IPC because: (a) MojoJS bindings made it directly fuzzable from JavaScript, and (b) sandbox escape bugs represent the critical escalation step in a full chain.

### 1.4 Shift to Mitigation Evaluation (2023)

**Evidence:** Brand's 2023 MTE series represents a deliberate pivot toward evaluating defensive technologies rather than just finding offensive primitives.

- Source: https://projectzero.google/2023/08/mte-as-implemented-part-1.html
- Source: https://projectzero.google/2023/08/mte-as-implemented-part-2-mitigation.html
- Source: https://projectzero.google/2023/08/mte-as-implemented-part-3-kernel.html
- Source: https://projectzero.google/2023/11/first-handset-with-mte-on-market.html
- Confidence: HIGH

**Explicit stated logic:** Brand stated his core research question was whether MTE could "effectively implement security mitigations, or would it remain limited to debugging purposes." He evaluated it from the attacker's perspective to determine if it constituted a "hard" or "soft" mitigation.

### 1.5 Shift to AI-Assisted Research (2024)

**Evidence:** Brand co-authored Project Naptime and participated in Big Sleep.

- Source: https://googleprojectzero.blogspot.com/2024/06/project-naptime.html
- Source: https://googleprojectzero.blogspot.com/2024/10/from-naptime-to-big-sleep.html
- Confidence: HIGH

**Explicit stated logic:** "We're always looking for new approaches" to expand beyond traditional manual auditing. The team specifically identified "unfuzzable" vulnerabilities as the gap AI might fill. They chose variant analysis as the LLM use case because "providing a starting point...removes a lot of ambiguity from vulnerability research."

---

## 2. Research Target Selection Decisions

### 2.1 Why Chrome IPC/Mojo as Research Direction

**Explicit statements (from "Virtually Unlimited Memory," 2019):**
- "it's actually possible to make IPC calls directly from Javascript in Chrome! Passing the command line flag '--enable-blink-features=MojoJS' to Chrome will enable this."
- Brand "used this feature to implement a Mojo fuzzer, which found some of the bugs reported"
- "the cleanest way to implement a full Chrome chain would be to use a renderer exploit to enable these bindings in the running renderer, and then do our privilege elevation from Javascript"

**Decision logic:** Brand chose Mojo IPC because:
1. MojoJS bindings created a unique opportunity to fuzz IPC interfaces directly from JavaScript, dramatically lowering the barrier to discovery
2. Sandbox escape is the critical escalation step -- renderer bugs are common, but privilege escalation is the rare/valuable part of a full chain
3. The interface surface was relatively unaudited at the time

- Source: https://projectzero.google/2019/04/virtually-unlimited-memory-escaping.html
- Confidence: HIGH (explicit first-person statements)

### 2.2 Why Chrome Network Stack (2020)

**Explicit statements (from "Several Months" Part 1):**
- "the networking code in Chrome has been split out into a new service process"
- "the implementation of strict sandboxing for that process isn't completed yet, so it's still a highly privileged attack surface"
- "this bug alone would be enough to both get initial code execution, and to break out of the Chrome sandbox"

**Decision logic:** Brand and Glazunov chose the network stack because Chrome's servicification was incomplete -- the network process was separated but not yet sandboxed, making it simultaneously a network-reachable AND privileged target. This represents a window of opportunity during architectural transition.

- Source: https://projectzero.google/2020/02/several-months-in-life-of-part1.html
- Confidence: HIGH (explicit first-person statements)

### 2.3 Why SwiftShader (2018)

**Explicit stated logic:** Brand selected SwiftShader because it "provides fallback rendering for Chrome on all platforms" -- meaning it is always present and reachable via WebGL regardless of GPU hardware. Precision issues in iterative floating-point calculations were his hypothesis.

- Source: https://projectzero.google/2018/07/drawing-outside-box-precision-issues-in.html
- Confidence: HIGH

### 2.4 Why MTE Evaluation (2023)

**Explicit stated logic:** Brand had access to pre-production MTE hardware and wanted to determine its security utility. His framework distinguishes:
- "Soft" mitigations: attackers bypass with one-time costs (e.g., developing ROP chain)
- "Hard" mitigations: require separate vulnerabilities to circumvent (e.g., ASLR)
- "Solutions": eliminate entire vulnerability classes

He set a 95% reliability threshold as his assumed attacker target, reasoning that "any such drop in reliability should generally be expected to increase detection of in-the-wild usage of exploits."

- Source: https://projectzero.google/2023/08/mte-as-implemented-part-1.html
- Source: https://projectzero.google/2023/08/mte-as-implemented-part-2-mitigation.html
- Confidence: HIGH (explicit analytical framework)

### 2.5 Why Variant Analysis for LLMs

**Explicit stated logic:** "The continued in-the-wild discovery of exploits for variants of previously found and patched vulnerabilities" motivated the focus. Also: "fuzzing is not succeeding at catching such variants, and that for attackers, manual variant analysis is a cost-effective approach."

- Source: https://projectzero.google/2024/10/from-naptime-to-big-sleep.html
- Confidence: HIGH

---

## 3. Exploit Development Strategy Decisions

### 3.1 Vulnerability Selection Criteria

**Pattern observed across multiple exploits:** Brand consistently selects vulnerabilities based on attacker control over:
- Object lifetime (when free occurs)
- Timing of the use-after-free access
- Data content controlled by the attacker

**Explicit statement (from "Virtually Unlimited Memory"):** He selected issue 1755 because of "the high level of control the attacker has both over the lifetime of the free'd object, and over the timing of the later use of the object."

**Explicit statement (from "Stagefrightened?"):** He selected CVE-2015-3864 because it was "a linear heap-overflow giving the attacker control over the size of the allocation; the amount of overflow, and the contents of the overflowed memory region."

- Confidence: HIGH (consistent explicit pattern across multiple publications)

### 3.2 ASLR Bypass: Pragmatism over Elegance

**Pattern:** Brand consistently avoids requiring information leaks when possible:
- In Stagefright (2015): Used brute force against 8-bit ASLR randomness rather than seeking an info leak
- In Chrome sandbox escape (2019): Sprayed 3.5TB of virtual address space rather than leaking addresses

**Explicit statement (Stagefright):** "while a more sophisticated technique to exploit this bug without requiring brute-force" existed, the straightforward approach sufficed for watering-hole scenarios.

**Explicit statement (Chrome):** Described his approach as enabling exploitation "without needing an information leak" -- using unlimited memory mapping to make addresses predictable.

- Source: https://projectzero.google/2015/09/stagefrightened.html
- Source: https://projectzero.google/2019/04/virtually-unlimited-memory-escaping.html
- Confidence: HIGH (explicit pattern, consistent behavior)

### 3.3 Decision to Build Full Chains

**Evidence:** Brand has published at least three full exploitation chains:
1. Flash PCRE (CVE-2015-0318): PCRE bug -> heap corruption -> Vector length corruption -> arbitrary R/W -> code execution
2. Android libutils (CVE-2016-3861): Media file -> UTF16/UTF8 overflow -> info leak -> ROP -> privilege escalation
3. Chrome full chain (2019): V8 typer bug -> Mojo IPC FileWriter UAF -> virtual memory spray -> browser process code execution

**Inferred decision logic:** Brand builds full chains to demonstrate complete attack scenarios, which serves two purposes: (a) establishing true severity for defenders, and (b) identifying where mitigations should be placed. His closing motto "Make zeroday hard" suggests the goal is to use full chains as evidence for where hardening investments should go.

- Confidence: MEDIUM-HIGH (pattern is clear but the strategic rationale is partly inferred)

### 3.4 Reliability vs. Elegance Trade-off

**Explicit statements from multiple posts:**
- "There's no point in doing something complicated when something simple exists" (Flash mitigations post, 2015)
- "approximately 4% chance of a successful exploit each minute" was considered acceptable for Stagefright (2015)
- In Chrome network stack exploit: 12.5% per-attempt success was acceptable because process restarts gave "virtually unlimited number of retries"
- Increased reliability from 0.375 to 0.75 through cookie-based heap grooming rather than seeking a perfect solution

**Decision pattern:** Brand accepts imperfect reliability when the target architecture allows retries. He does NOT pursue 100% reliability unless the attack scenario requires it (e.g., one-shot messaging attacks need higher reliability).

- Source: multiple posts above
- Confidence: HIGH (explicit, consistent pattern)

### 3.5 Choices About What NOT to Exploit

**Explicit statement ("Several Months" Part 2):** The team evaluated NetToMojoPendingBuffer, STL containers, and WatcherDispatcher before settling on WebSocketFrame. They rejected options based on:
- WatcherDispatcher: only 2/8 (25%) success rate for pointer overwrites
- NetToMojoPendingBuffer: "lacked useful corruption targets"

They chose WebSocketFrame because "WebSocket::Send won't trigger any allocations in the 16-byte arena apart from resizing the std::vector that we're targeting."

- Source: https://projectzero.google/2020/02/several-months-in-life-of-part2.html
- Confidence: HIGH (explicit elimination reasoning)

---

## 4. Technical Route Choices: Fuzzing vs. Manual Audit vs. Variant Analysis

### 4.1 Fuzzing: Building Custom Fuzzers for Unexplored Interfaces

**Explicit evidence:** Brand built a Mojo fuzzer using MojoJS bindings that discovered sandbox escape bugs. This was a novel approach at the time -- using the browser's own test infrastructure as a fuzzing harness.

**Quote:** "we used this feature to implement a Mojo fuzzer, which found some of the bugs reported"

- Source: https://projectzero.google/2019/04/virtually-unlimited-memory-escaping.html
- Confidence: HIGH

### 4.2 Manual Code Review: For Architectural Weaknesses

**Explicit evidence:**
- Chrome IOBuffer integer truncation (2015): Found through manual code review of API design, not fuzzing
- SwiftShader precision issues (2018): Found through manual analysis of floating-point accumulation, then validated with brute-force testing
- MTE evaluation (2023): Entirely manual/analytical assessment of security properties

**Quote (IOBuffer post):** Brand identified the vulnerability by examining the IOBuffer constructor's use of `int buffer_size` despite `size_t` being standard practice, then traced the truncation path manually.

- Source: https://projectzero.google/2015/07/when-int-is-new-short.html
- Confidence: HIGH

### 4.3 Hybrid Approach: Manual + Brute Force Validation

**Evidence (SwiftShader):** "ran a brute force over all ratios of source width to destination width, comparing the two algorithms, and seeing where the results were most different"

This shows Brand using manual reasoning to identify the category of issue, then automated testing to find exploitable parameters.

- Source: https://projectzero.google/2018/07/drawing-outside-box-precision-issues-in.html
- Confidence: HIGH

### 4.4 Statement on Fuzzing Limitations

**Explicit (Naptime/Big Sleep, 2024):** "fuzzing is not succeeding at catching such variants" -- acknowledging that for variant analysis, fuzzing fails where structured reasoning succeeds.

**Explicit (libstagefright):** "The bug is quite straightforward, and since it's quite readily fuzzable, it's interesting that it's been undiscovered for so long" -- suggesting that even fuzzable bugs can be missed, and manual research complements fuzzing.

- Source: https://projectzero.google/2024/10/from-naptime-to-big-sleep.html
- Source: https://projectzero.google/2016/09/return-to-libstagefright-exploiting.html
- Confidence: HIGH

---

## 5. Disclosure Decisions and Policy

### 5.1 Standard 90-Day Policy Compliance

**Evidence:** Brand's research follows Project Zero's standard disclosure policy. No known cases of Brand personally requesting exceptions or having public disputes with vendors.

The Samsung Galaxy S6 Edge research (2015) demonstrates collaborative disclosure: all issues reported promptly, Samsung fixed 8 of 11 in the October release, remaining 3 in November -- all within 90 days.

- Source: https://projectzero.google/2015/11/hack-galaxy-hunting-bugs-in-samsung.html
- Confidence: HIGH

### 5.2 Writing Full Exploits as Disclosure Evidence

**Inferred decision logic:** Brand consistently publishes full exploitation chains rather than just crash PoCs. This appears to be a deliberate choice to:
1. Demonstrate actual severity (not theoretical risk)
2. Provide defenders with concrete evidence for prioritization
3. Force vendors to address root causes rather than superficial fixes

**Supporting evidence:** His Chrome IOBuffer post (2015) explicitly contrasted the severity of a single-bug browser-process compromise against typical Pwn2Own multi-bug chains, arguing that unsandboxed attack surface deserves more attention.

**Quote:** The bug enabled "unsandboxed arbitrary code execution from a drive-by" -- a stronger severity statement than a crash report alone.

- Source: https://projectzero.google/2015/07/when-int-is-new-short.html
- Confidence: MEDIUM-HIGH (the pattern is clear; the strategic rationale is partially inferred)

### 5.3 No Known Controversial Disclosures

**Observation:** Unlike some P0 researchers (e.g., Tavis Ormandy's Microsoft/AV disclosures), Mark Brand has no publicly documented contentious deadline-enforced disclosures. His targets (Chrome, Android, Samsung) have generally patched within the 90-day window.

- Confidence: MEDIUM (absence of evidence is not evidence of absence; private disputes may exist)

---

## 6. Judgments on Chrome's Security Architecture

### 6.1 Servicification: Initially Risky, Eventually Beneficial

**Explicit statements:**
- Part 1 (2020): Incomplete servicification creates a window where "the networking code...is still a highly privileged attack surface"
- Part 2 (2020): "Service processes implementing a relatively small number of features are inherently harder targets for exploitation than larger monolithic components; they have a reduced number of available weird-machines"

**Assessment:** Brand views Chrome's servicification as a net positive for security once sandboxing is complete, but recognizes the transition period as dangerous.

- Source: https://projectzero.google/2020/02/several-months-in-life-of-part1.html
- Source: https://projectzero.google/2020/02/several-months-in-life-of-part2.html
- Confidence: HIGH (explicit statements)

### 6.2 ASLR Weaknesses as Architectural Flaw

**Explicit statement (2019):** Brand identified two critical weaknesses:
- No inter-process ASLR on Windows (libraries at same addresses across processes)
- No address-space limits on the browser process (enabling unlimited virtual memory spraying)

These are presented as design gaps enabling his exploit to work "without needing an information leak."

- Source: https://projectzero.google/2019/04/virtually-unlimited-memory-escaping.html
- Confidence: HIGH

### 6.3 MojoJS Bindings as Attack Surface Enabler

**Explicit observation:** Brand noted that MojoJS bindings (intended for testing) can be enabled from a compromised renderer, transforming IPC into a JavaScript-accessible attack surface. This is presented as a significant architectural concern.

- Source: https://projectzero.google/2019/04/virtually-unlimited-memory-escaping.html
- Confidence: HIGH

### 6.4 Process Restarts as Double-Edged Sword

**Explicit statement (2020):** "for an exploit developer, knowing that you can have as many tries as you need takes a lot of pressure off -- you have a lot more freedom to create and use unreliable primitives"

**Assessment:** Chrome's crash recovery mechanism (restarting service processes) aids reliability-challenged exploits by providing unlimited retries without requiring page reloads visible to the user.

- Source: https://projectzero.google/2020/02/several-months-in-life-of-part2.html
- Confidence: HIGH

### 6.5 MTE Assessment for Chrome

**Explicit evaluation (2023):** In his MTE Part 2 assessment, Brand specifically evaluated four attack scenarios including:
- Chrome renderer exploitation (JavaScript-based)
- Chrome IPC sandbox escape (compromised renderer attacking browser process)

He assessed MTE's effectiveness differently for each scenario, noting that mandatory system calls between IPC messages "fundamentally constrain exploit development complexity."

- Source: https://projectzero.google/2023/08/mte-as-implemented-part-2-mitigation.html
- Confidence: HIGH

---

## 7. Research Philosophy and Self-Reflection

### 7.1 "Make Zeroday Hard"

**Explicit motto:** Brand closes his libstagefright post (2016) and his Chrome sandbox escape post (2019) with this phrase. It encapsulates his philosophy: the goal of offensive security research is to raise the cost of exploitation, not merely to find bugs.

- Source: https://projectzero.google/2016/09/return-to-libstagefright-exploiting.html
- Source: https://projectzero.google/2019/04/virtually-unlimited-memory-escaping.html
- Confidence: HIGH (explicit, repeated statement)

### 7.2 Providing Data to Defenders

**Explicit statement (Flash mitigations, 2015):** "One of the main reasons we perform this research is to provide data to defenders."

- Source: https://projectzero.google/2015/07/significant-flash-exploit-mitigations_16.html
- Confidence: HIGH

### 7.3 Honest Self-Criticism

**Explicit examples:**
- "Several Months" series (2020): "we'd just been too lazy to set up a build environment to check for ourselves" and "At this point, we were questioning our decision-making process more thoroughly"
- Same series: "many more failures than successes" and careless mistakes like "running the webserver on the wrong port"
- Naptime (2024): "a large part of security research is finding the right places to look" -- acknowledging that framing the problem is as hard as solving it

**Pattern:** Brand is unusually transparent about mistakes and inefficiencies in his research process. This reflects intellectual honesty and a willingness to document the messy reality of security research.

- Source: https://projectzero.google/2020/02/several-months-in-life-of-part1.html
- Source: https://projectzero.google/2020/02/several-months-in-life-of-part2.html
- Confidence: HIGH

### 7.4 Pragmatism Over Theoretical Elegance

**Consistent pattern across all publications:**
- Accepts brute-force when ASLR entropy is low (Stagefright 2015)
- Accepts 12.5% reliability when retries are free (Chrome network stack 2020)
- Uses "crude" techniques when they work (heap spraying, cookie grooming)
- "There's no point in doing something complicated when something simple exists" (2015)

**Assessment:** Brand is a pragmatic exploit developer who optimizes for demonstrating impact rather than demonstrating cleverness. He frequently takes the simplest path that proves the security concern.

- Confidence: HIGH (consistent across 10 years of publications)

### 7.5 Progressive Security Standards

**Explicit statements:**
- Stagefright (2015): "my initial stagefright exploit was very crude; this time around I wanted to take a bit more pride in the work"
- Libutils (2016): noted that "new mitigations that could be set in place to make the Android exploitation process harder also came out of this research"
- MTE (2023): "MTE is not a silver bullet" but "a big step forward"

**Pattern:** Brand acknowledges that both offense and defense improve over time, and his research aims to accelerate defensive progress.

- Confidence: HIGH

### 7.6 Security Research as Empirical Science

**Explicit (Naptime, 2024):** Brand articulated five principles for security research methodology:
1. Reasoning Space -- need room for verbose explanation
2. Interactivity -- iterative adjustment in live environments
3. Specialized Tools -- debugger, scripting essential
4. Perfect Verification -- vulnerabilities can be confirmed with certainty (unlike many AI tasks)
5. Sampling Strategy -- multiple independent trajectories explore diverse hypotheses

This is the most explicit meta-statement Brand has made about how security research actually works.

- Source: https://projectzero.google/2024/06/project-naptime.html
- Confidence: HIGH

---

## 8. Consistency Analysis: Stated Logic vs. Observed Behavior

### 8.1 Consistent: Attack Surface Following

Brand consistently moves to wherever the highest-impact, most-exposed attack surface is:
- 2015: Flash (dominant browser plugin)
- 2015-2016: Android media (remote, pre-auth)
- 2018-2019: Chrome IPC/Mojo (sandbox escape, the critical chain link)
- 2020: Chrome network stack (transitionally unsandboxed)
- 2023: MTE evaluation (new defensive technology needing assessment)
- 2024: AI-assisted research (new methodology needing evaluation)

**Verdict:** HIGHLY CONSISTENT. His research targets always follow the question "where is the most impactful unexamined surface?"

### 8.2 Consistent: Pragmatic Exploitation

Across all publications, Brand never pursues theoretical elegance at the expense of demonstrating impact. He consistently uses the simplest technique that proves the security concern.

**Verdict:** HIGHLY CONSISTENT.

### 8.3 Consistent: Full Chain Philosophy

Brand has published full exploitation chains in 2015, 2016, 2019, and 2020. Each time, the purpose is demonstrating that a vulnerability class is truly exploitable end-to-end, not just theoretically dangerous.

**Verdict:** HIGHLY CONSISTENT.

### 8.4 Potentially Inconsistent: Fuzzing vs. Manual Audit

Brand uses both approaches but has never published a clear statement about when to prefer one over the other. His Mojo fuzzer used fuzzing for discovery; his IOBuffer and SwiftShader work used manual review. The Naptime/Big Sleep work suggests he sees both as complementary.

**Verdict:** NOT INCONSISTENT -- but lacks explicit decision framework. The implicit rule appears to be: use fuzzing when the interface is readily testable and unexplored; use manual audit when the vulnerability class requires reasoning about design assumptions.

### 8.5 Evolution: From Pure Offense to Defensive Impact

Early Brand (2015-2016) focused primarily on exploit development. Later Brand (2023-2024) focuses increasingly on evaluating defenses and building tools. This is an evolution, not an inconsistency -- his stated goal has always been "Make zeroday hard."

**Verdict:** CONSISTENT EVOLUTION aligned with stated values.

---

## 9. Known Gaps and Limitations of This Research

1. **No conference talk transcripts found.** Brand reportedly presented at 35C3 (2018) on his Chrome full-chain exploit, but no transcript or video content was accessible.

2. **Limited bug tracker data.** The Chromium/Project Zero bug trackers did not return readable content, preventing analysis of his day-to-day disclosure interactions.

3. **No biographical/career history found.** Brand's pre-P0 background, education, and motivation for joining are not publicly documented in accessible sources.

4. **Firefox research not found.** Despite being reported as a Firefox security researcher, no Firefox-specific publications by Brand were identified.

5. **Private communications not accessible.** Any internal debates about disclosure timelines or research direction are not publicly visible.

6. **Limited information about abandoned research.** No explicit discussion found of research directions Brand started and deliberately abandoned.

---

## 10. Complete Publication List (Confirmed)

| Year | Title | Focus | Role |
|------|-------|-------|------|
| 2015 | Exploiting CVE-2015-0318 in Flash | Flash PCRE exploitation | Author |
| 2015 | Significant Flash exploit mitigations | Flash defense analysis | Co-author (with Chris Evans) |
| 2015 | When 'int' is the new 'short' | Chrome IOBuffer truncation | Author |
| 2015 | Hack The Galaxy (Samsung S6) | Samsung Android bugs | Contributor |
| 2015 | Stagefrightened? | Android Stagefright exploit | Author |
| 2016 | Return to libstagefright | Android libutils exploit | Author |
| 2018 | Drawing Outside the Box | SwiftShader/Skia precision | Co-author (with Ivan Fratric) |
| 2019 | Virtually Unlimited Memory | Chrome full-chain exploit | Author |
| 2020 | Several Months Part 1 | Chrome network stack investigation | Co-author (with Sergei Glazunov) |
| 2020 | Several Months Part 2 | Chrome network stack exploitation | Co-author (with Sergei Glazunov) |
| 2021 | In-the-Wild Series: Android Exploits | Android in-wild exploit analysis | Author |
| 2023 | MTE As Implemented (Parts 1-3) | ARM MTE security evaluation | Author |
| 2023 | First handset with MTE on the market | Pixel 8 MTE practical guide | Author |
| 2024 | Project Naptime | LLM vulnerability research | Co-author (with Sergei Glazunov) |
| 2024 | From Naptime to Big Sleep | LLM variant analysis | Team member |

---

## 11. Key Decision Heuristics (Synthesized)

Based on the above evidence, Mark Brand's research decisions appear governed by these principles:

1. **Follow the highest-impact unexamined surface.** Research targets are selected based on: exposure (remote/pre-auth preferred), privilege level (unsandboxed > sandboxed), and novelty (unaudited > well-audited).

2. **Demonstrate impact through full chains.** Don't just report crashes -- show the complete attack path to prove severity and identify where defenses should be placed.

3. **Pragmatism over elegance.** Use the simplest technique that proves the point. Accept brute-force when it works. Don't optimize reliability beyond what the attack scenario requires.

4. **Design custom tools for novel surfaces.** When an interface hasn't been tested, build bespoke tooling (Mojo fuzzer, brute-force precision tester) rather than adapting generic tools.

5. **Evaluate defenses from the attacker's perspective.** Ask "what would a motivated attacker do?" rather than "does this defense work in theory?" Set explicit reliability thresholds (95% for MTE).

6. **Provide data to defenders.** The purpose of offensive research is to generate evidence for defensive investment. Document what works, what doesn't, and what should be hardened.

7. **Be honest about failures and limitations.** Publicly document laziness, mistakes, and open questions rather than presenting a polished narrative.

8. **Accept imperfect reliability when retries are free.** Architectural features like process restart change the economics of exploitation -- factor this into severity assessment.
