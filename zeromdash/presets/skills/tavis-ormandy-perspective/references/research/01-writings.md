# Tavis Ormandy - Writings, Publications, and Research Philosophy

## Meta

- **Compiled**: 2026-05-09
- **Scope**: First-party writings (blog posts, papers, tool READMEs, PoC code) with secondary source supplementation
- **Primary sites**: lock.cmpxchg8b.com (personal), Project Zero blog (Google), github.com/taviso, github.com/google/security-research
- **Career span**: Google (2007-2025.10), Project Zero (2014-2025), independent researcher (2025.10-present)
- **Total entries**: 43

---

## I. Project Zero Blog Articles (Confirmed First-Hand)

### 1. "The poisoned NUL byte, 2014 edition" (2014-08-25)
- **Source**: https://projectzero.google/2014/08/the-poisoned-nul-byte-2014-edition.html
- **Source type**: First-hand (co-author with Chris Evans)
- **Confidence**: HIGH
- **Content**: Nine-stage exploitation chain proving a 2005 glibc off-by-one NUL byte (CVE-2009-1759) exploitable for root on 32-bit Fedora.
- **Core thesis**: "Exploitability determinations should not delay fixes" — a bug dismissed for 9 years as "not exploitable" was fully weaponized.
- **Methodology**: Heap feng shui, partial overwrite exploitation, systematic constraint satisfaction.
- **Chris Evans's title**: "Exploit Writer Underling to Tavis Ormandy" (characterizing their dynamic).

### 2. "Analysis and Exploitation of an ESET Vulnerability" (2015-06)
- **Source**: https://projectzero.google/2015/06/analysis-and-exploitation-of-eset.html
- **Source type**: First-hand
- **Confidence**: HIGH
- **Content**: Multi-stage exploitation of AV emulator. Shadow stack bypass, ASLR defeat via leaked addresses, ROP chain to escape emulation and reach real CPU.
- **macOS-specific weakness**: ESET omitted heap execution prevention flag → simpler exploitation path.
- **Key frame**: "Protective mechanisms becoming attack vectors when insufficiently isolated."
- **Question framing**: "Do we understand the risk vs. benefit trade-offs of security software?"

### 3. "Kaspersky: Mo Unpackers, Mo Problems" (2015-09-22)
- **Source**: https://projectzero.google/2015/09/kaspersky-mo-unpackers-mo-problems.html
- **Source type**: First-hand
- **Confidence**: HIGH
- **Content**: Stack buffer overflow in Thinstall container unpacking (no /GS protection). PAGE_EXECUTE_READWRITE. SYSTEM-level code execution.
- **Key quote**: "Attempting to reduce one's exposure to opportunistic malware should not result in an increased exposure to targeted attacks."
- **Vendor response**: "Thanks to Kaspersky for record breaking response times."
- **WikiLeaks reference**: Cited evidence of "active black market trade in antivirus exploits."

### 4. "FireEye Exploitation: Project Zero's Vulnerability of the Beast" (2015-12-15)
- **Source**: https://projectzero.google/2015/12/fireeye-exploitation-project-zeros.html
- **Source type**: First-hand (co-author with Natalie Silvanovich)
- **Confidence**: HIGH
- **Content**: RCE via passive network monitoring appliance. Exploited JODE decompiler in Malware Input Processor.
- **Self-description**: "Chief Silver Bullet Skeptic"
- **Impact**: "a nightmare scenario" — access to email, passwords, browsing history.
- **Key quote**: "And now we're root, with complete control."
- **Issue number**: #666 (dark humor: "Vulnerability of the Beast").

### 5. "How to Compromise the Enterprise Endpoint" (2016-06-28)
- **Source**: https://projectzero.google/2016/06/how-to-compromise-enterprise-endpoint.html
- **Source type**: First-hand
- **Confidence**: HIGH
- **Content**: Multiple wormable RCE in Symantec/Norton. CVE-2016-2208 (ASPack kernel overflow).
- **Key quote**: "Network administrators should keep scenarios like this in mind when deciding to deploy Antivirus, it's a significant tradeoff in terms of increasing attack surface."
- **Key finding**: 7-year-old unpatched third-party libraries.
- **Rhetorical section title**: "Unpackers in the Kernel: Maybe not the best idea?"
- **Severity framing**: "These vulnerabilities are as bad as it gets. They don't require any user interaction, they affect the default configuration, and the software runs at the highest privilege levels possible."

### 6. "Down the Rabbit-Hole..." (2019-08-13)
- **Source**: https://projectzero.google/2019/08/down-rabbit-hole.html
- **Source type**: First-hand
- **Confidence**: HIGH
- **Content**: Windows Text Services Framework (CTF/MSCTF). No access control, memory corruption, privilege escalation, sandbox escape. 20+ years since Vista.
- **Key quote**: "Sometimes, hacking is just someone spending more time on something than anyone else might reasonably expect."
- **Tool released**: ctftool

### 7. "This shouldn't have happened: A vulnerability postmortem" (2021-12-01)
- **Source**: https://projectzero.google/2021/12/this-shouldnt-have-happened.html
- **Source type**: First-hand
- **Confidence**: HIGH
- **Content**: CVE-2021-43527 (NSS BigSig). Oversized signature copied into fixed-size buffer, overwriting function pointers.
- **Three systemic failures identified**:
  1. Missing end-to-end testing
  2. Arbitrary size limits (buffer chosen for "common" case, not maximum)
  3. Misleading coverage metrics
- **Innovation**: "Stack Coverage" concept — tracking call stack combinations, not just code block coverage. Traditional coverage showed high numbers but missed the specific call chain that triggered the bug.
- **Core lesson**: "Even extremely well-maintained C/C++ can have fatal, trivial mistakes."
- **Methodology**: Object isolation on ASN.1 structures for targeted fuzzing.

---

## II. Personal Blog Articles (lock.cmpxchg8b.com) - All First-Hand

### 8. Zenbleed (CVE-2023-20593) - July 2023
- **Source**: https://lock.cmpxchg8b.com/zenbleed.html
- **Confidence**: HIGH
- **Content**: AMD Zen 2 data leakage via mispredicted vzeroupper. Register file "use-after-free" where z-bit incorrectly reset.
- **Key methodology - Oracle Serialization**: Self-coined technique. Random instruction generation + serialization fence insertion = reference oracle. Performance counters (not code coverage) as fuzzing feedback.
- **Key quote**: "memory management is hard, even in silicon :)"
- **Opening hook**: "If you remove the first word from 'hello world', what should the result be?"
- **Outsider advantage quote**: "I don't have an EE background" — frames fresh perspective as methodological strength.
- **Exploitation**: 30 KB/core/second data leakage. No privileges required.

### 9. Reptar - November 2023
- **Source**: https://lock.cmpxchg8b.com/reptar.html
- **Confidence**: HIGH
- **Content**: Intel FSRM bug. Redundant rex.r prefixes cause frontend to miscalculate instruction size → ROB corruption across cores.
- **Opening**: "We have a CPU mystery!"
- **Discovery**: Google's validation pipeline using Oracle Serialization.
- **Impact**: "even inside an unprivileged guest VM" — cloud infrastructure risk.
- **Affected**: Ice Lake through Sapphire Rapids.

### 10. Password Manager Evaluation - June 2021
- **Source**: https://lock.cmpxchg8b.com/passmgrs.html
- **Confidence**: HIGH
- **Content**: Architecture-level analysis of how "remote attackers can interact with your password manager."
- **Key analogy**: "'use a password manager' is vague and potentially dangerous advice, analogous to telling someone to take unidentified pills from a medicine cabinet."
- **Expert authority claim**: "I think I've spent more time analyzing them than practically anybody else, and I think that qualifies me to have an opinion!"
- **Conclusion**: Browser-native managers > extensions.

### 11. Anubis / Proof-of-Work Anti-Bot (August 2025)
- **Source**: https://lock.cmpxchg8b.com/anubis.html
- **Confidence**: HIGH
- **Content**: Economic demolition of Anubis proof-of-work deployed on kernel.org.
- **Opening hook**: "why are anime catgirls blocking my access to the Linux kernel?"
- **Double-spend vulnerability**: Tokens reusable before invalidation.
- **Economic calculation**: ~11,500 deployments, 6 minutes compute, $0 monthly cost.
- **Key insight**: "effectively only limiting access to those without resources."
- **Professional ethics**: Emailed maintainer before publishing. Found and reported bug.
- **Tone**: Warmer than AV criticism — scaled to target (small open source project vs negligent enterprise).

### 12. Hiew Hex Editor Introduction - December 2023
- **Source**: https://lock.cmpxchg8b.com/hiew.html
- **Confidence**: HIGH
- **Content**: Advocacy for Hiew as specialized binary analysis tool.
- **Opening**: "more people should use it!"
- **Design philosophy**: "Chaining together simple commands to perform complex tasks" (composability).
- **Audience awareness**: "maybe 0.01% of the people reading this will be intrigued"

### 13. Restoring Debugging Data to Stripped Binaries - August 2022
- **Source**: https://lock.cmpxchg8b.com/symbols.html
- **Confidence**: HIGH
- **Content**: STABS format for restoring debug info to 30-year-old binaries. BinDiff cross-architecture matching.
- **Key insight**: STABS advantage: "expressing simple stuff (_very_ simple) is so easy you can even do it by hand."

### 14. Lotus 1-2-3 Custom Display Driver - February 2021
- **Source**: https://lock.cmpxchg8b.com/lotus123.html
- **Confidence**: HIGH
- **Content**: Reverse-engineered DOS display driver. Found STABS symbols in SunOS 4 SPARC binary.
- **Philosophy**: "Well-engineered systems have intrinsic durability regardless of their age."
- **Opening**: "I tend to use a lot of retro software, partly because I'm a big nerd"

### 15. XTerm Tektronix Mode Popup Advertisements - December 2020
- **Source**: https://lock.cmpxchg8b.com/tektronix.html
- **Confidence**: HIGH
- **Content**: Terminal escape sequences rendering bitmaps in XTerm.
- **Quote**: "Nobody ever asked for or wanted this"
- **Philosophy**: Gap between user assumptions and terminal capabilities creates security surprises.

### 16. Dual Library Version Linking - December 2020
- **Source**: https://lock.cmpxchg8b.com/symcoll.html
- **Confidence**: HIGH
- **Content**: nm + objcopy --redefine-syms for dual-version comparison.
- **Philosophy**: "manually examine any cases where the new version gave different results."

### 17. Recovered Lotus 1-2-3 for UNIX/Linux - May 2022
- **Source**: https://lock.cmpxchg8b.com/linux123.html
- **Confidence**: HIGH
- **Content**: Recovered Intel 80386 COFF object file from old BBS tapes. Created coffsyrup tool.
- **Key quote**: "there is no enthusiast community, it's just me!"

### 18. WordPerfect for UNIX / Sixel Graphics - July 2022
- **Source**: https://lock.cmpxchg8b.com/wordperfect.html
- **Confidence**: HIGH
- **Content**: 1992 "document preview" on character terminals via Sixel graphics.

### 19. Templates of Doom! - January 2023
- **Source**: https://lock.cmpxchg8b.com/doom.html
- **Confidence**: HIGH
- **Content**: 1988 game in Lotus 1-2-3 macros. Lucasfilm lawsuit.
- **Key quote**: "The moment that Vim first 'clicked' for me is when I wrote my first macro."
- **Opening**: "In the late 1980s there was - believe it or not - a popular monthly magazine dedicated to spreadsheets."

### 20. Terminal Startup Performance - July 2024
- **Source**: https://lock.cmpxchg8b.com/slowterm.html
- **Confidence**: HIGH
- **Content**: 5x performance gap (xterm 1600ms Windows vs 300ms Fedora). Solution: pre-cached instances.
- **Opening**: "I think I should blog more about random troubleshooting sessions"
- **Self-awareness**: "I don't think many people care about xterm performance on Windows"

### 21. Lotus Agenda - October 2020
- **Source**: https://lock.cmpxchg8b.com/lotusagenda.html
- **Confidence**: HIGH
- **Key quote**: "There is something that appeals to me about using long-abandoned software. Perhaps it's update fatigue, there's certainly no need to dread a major update breaking something!"

### 22. Spreadsheet Software Review - November 2020
- **Source**: https://lock.cmpxchg8b.com/spreadsheet.html
- **Confidence**: HIGH
- **Key quote**: "if I only want something occasionally I just won't bother using it if I have to lookup the syntax every time."
- **Contradiction noted**: "I usually choose powerful and flexible software over simplicity" — tension with his minimalist tool design.

### 23. Personal Finance with Ledger - December 2023
- **Source**: https://lock.cmpxchg8b.com/ledger.html
- **Confidence**: HIGH
- **Content**: CLI accounting with ledger.
- **Philosophy**: "efficiency and scriptability of the commandline, along with the grep, editor and revision control friendly file format."

### 24. Watch Selection - November 2022
- **Source**: https://lock.cmpxchg8b.com/watch.html
- **Confidence**: HIGH
- **Key quote**: "it's nice to have something I can trust to do its job."
- **Contrast**: "If an unattended update hosed my laptop, or an app update breaks my workflow - oh well, that's par for the course."

---

## III. GitHub Tool READMEs - Design Philosophy (All First-Hand)

### 25. loadlibrary - Porting Windows DLLs to Linux
- **Source**: https://github.com/taviso/loadlibrary
- **Confidence**: HIGH
- **Motivation**: "Distributed, scalable fuzzing on Windows can be challenging and inefficient."
- **Opinion**: "This is just personal opinion, but I also think Linux has better tools."
- **Philosophy**: Linux's tooling ecosystem is superior for security research. Not Wine — "much simpler."
- **Stars**: 4.5k

### 26. halfempty - Parallel Test Case Minimization
- **Source**: https://github.com/taviso/halfempty (archived, from Project Zero era)
- **Innovation**: "pessimistic speculative execution" parallelization. 34min → 6min.
- **Philosophy**: "Bisection is an inherently serial process" — unless you speculate.

### 27. ctypes.sh - Foreign Function Interface for Bash
- **Source**: https://github.com/taviso/ctypes.sh
- **Confidence**: HIGH
- **Community reactions** (curated in README): "that's disgusting", "this has got to stop", "you've gone too far"
- **Stars**: 2.2k

### 28. ctftool - Windows CTF Protocol Explorer
- **Source**: https://github.com/taviso/ctftool
- **Confidence**: HIGH
- **Stars**: 1.7k
- **Note**: "it is unknown how Microsoft will change the CTF protocol"

### 29. hotcorner - Tiny Hot Corners for Windows 10
- **Source**: https://github.com/taviso/hotcorner
- **Confidence**: HIGH
- **Extreme minimalism**:
  - "Zero state is stored anywhere, no registry keys or configuration files"
  - All settings in source code; must compile to customize
  - "Simply delete the executable to uninstall"
  - Existing solutions: "Some ridiculous AutoHotKey monstrosity"

### 30. kiewtai - Kaitai Struct for Hiew
- **Source**: https://github.com/taviso/kiewtai
- **Confidence**: HIGH
- **Philosophy**: Progressive disclosure, extensibility.

### 31. 123elf - Native Port of Lotus 1-2-3 to Linux
- **Source**: https://github.com/taviso/123elf
- **Stars**: 1.3k
- **Philosophy**: Functional preservation; retrocomputing as heritage.

### 32. wslcompat - WSL1 Polyfill Library (2025-2026)
- **Source**: https://github.com/taviso/wslcompat
- **Confidence**: HIGH
- **Purpose**: LD_PRELOAD library adding missing WSL1 functionality
- **Philosophy**: "Fix the environment, don't change your workflow" — instead of migrating to WSL2, polyfill what's missing in WSL1.
- **Activity**: 26-commit sprint May 2026 (polyfills, file locking, tests)

### 33. zentool - AMD Microcode Tool (2025)
- **Source**: github.com/google/security-research
- **Confidence**: HIGH
- **Includes**: 436-line "Microcoding Quickstart" tutorial
- **Note**: "Zen 5 uses a different CMAC key"

### 34. lxdk - WSL1 Kernel Driver Dev Kit (Forked April 2026)
- **Source**: https://github.com/taviso/lxdk
- **Confidence**: HIGH
- **Significance**: Suggests exploration of kernel-level WSL1 driver development beyond LD_PRELOAD.

### 35. matrix3 - uMatrix Replacement for MV3 (2025)
- **Source**: https://github.com/taviso/matrix3
- **Confidence**: HIGH
- **Purpose**: Browser content filtering extension for Chrome Manifest V3.

### 36. defermap - X11 Fast Terminal Launch (2024)
- **Source**: https://github.com/taviso/defermap
- **Confidence**: HIGH
- **Purpose**: Pre-cached xterm instances with deferred window mapping for fast startup.

---

## IV. Academic Papers

### 37. "Flayer: Exposing Application Internals" (WOOT 2007)
- **Source**: https://www.usenix.org/legacy/events/woot07/tech/full_papers/drewry/drewry.pdf
- **Authors**: Will Drewry and Tavis Ormandy
- **Venue**: USENIX Workshop on Offensive Technologies 2007
- **Content**: Dynamic taint analysis tool built on Valgrind.
- **Confidence**: HIGH (authorship documented)

### 38. "Sophail: Applied attacks against Sophos Antivirus" (2012)
- **Source**: https://lock.cmpxchg8b.com/sophail.pdf
- **Confidence**: HIGH
- **Significance**: 30-page paper; established "AV as attack surface" thesis pre-Project Zero.

---

## V. EntrySign / AMD Microcode Research (2024-2025)

### 39. EntrySign PoC Code (CVE-2024-56161)
- **Source**: github.com/google/security-research/pocs/cpus/entrysign
- **Confidence**: HIGH
- **Technical mechanism**: CMAC-AES meet-in-the-middle attack + RSA key substitution
- **Key files**:
  - `preimage.c`: Computes forward/backward through CMAC chain using "sacrifice blocks"
  - `factor.c`: Generates forged RSA keypairs where `cmac(forged_modulus) == cmac(original_modulus)`
- **Affected**: Zen 1 through Zen 4
- **PoC**: Modified RDRAND to return constant 4
- **Note**: No dedicated blog post exists. Details live only in code and brief READMEs.
- **Significance**: Most impactful finding — compromises hardware root of trust for SEV-SNP confidential computing.

---

## VI. GhostScript -dSAFER Series (2017-2019)

### 40. GhostScript Sandbox Bypass Campaign
- **Source**: oss-security mailing list posts (2018)
- **CVE**: CVE-2018-16509 (CVSS 7.8/9.3)
- **Confidence**: HIGH
- **Content**: Multiple PostScript sandbox escapes demonstrating -dSAFER is fundamentally fragile.
- **Four vulnerability categories**: /invalidaccess exception handling, restore operator abuse, type confusion in operators, path traversal.
- **Key characterization**: "-dSAFER is a fragile security boundary at the moment"
- **Recommendation**: "Disable PS/EPS/PDF/XPS coders in policy.xml by default"
- **Pattern**: This is Model 4 (Systemic over Individual) in action — multiple rounds proving design is broken, not just individual bugs.

---

## VII. Self-Coined Terminology and Concepts

### Oracle Serialization
- **First appearance**: Zenbleed (July 2023), reused in Reptar (November 2023)
- **Definition**: Generate two program variants (with/without serialization fences), verify identical final states. Discrepancies reveal microarchitectural violations.
- **Innovation**: Hardware performance counters as fuzzing feedback (not code coverage).
- **Significance**: Core methodology behind 3+ major CPU vulnerabilities.

### Stack Coverage
- **First appearance**: NSS BigSig post (December 2021)
- **Definition**: Tracking unique call stack combinations reaching a code point, not just whether the code was reached. Traditional coverage showed high % but missed critical call chains.
- **Insight**: "Coverage" can be misleading when the same code is reached by many paths but critical combinations are never tested.

### Attack Surface Expansion Paradox
- **Not a single coined term but a recurring thesis** (2012-2021)
- **Definition**: Security products that process untrusted input with maximum privileges inherently create more attack surface than they eliminate.

---

## VIII. Recurring Core Themes (Appears in >= 3 writings)

### Theme 1: Security Products as Attack Surface (6+ appearances)
Core argument: Software designed to protect users often increases risk (highest privilege + untrusted input + no sandbox).

### Theme 2: Persistence and Time Investment (4+ appearances)
Core argument: Systemic vulnerabilities persist because nobody dedicated sufficient focused time.

### Theme 3: Tools Should Be Minimal, Composable, and Transparent (5+ appearances)
Core argument: Good tools are small, composable, transparent. Bloat and hidden state are design failures.

### Theme 4: Software Archaeology and Preservation (5+ appearances)
Core argument: Well-engineered legacy software has intrinsic durability. Individual curiosity can resurrect it.

### Theme 5: Fuzzing Infrastructure Must Scale on Linux (3+ appearances)
Core argument: Effective research requires industrial-scale fuzzing on Linux.

### Theme 6: Empirical Verification Over Assumptions (4+ appearances)
Core argument: Never assume correctness. Build automated oracles. Test empirically.

### Theme 7: Finished/Stable Software Has Value (3+ appearances)
Core argument: Update fatigue is real. Complete software that never changes has genuine value.

### Theme 8: Fresh Perspectives Beat Domain Expertise (3+ appearances)
- Zenbleed: "I don't have an EE background" — outsider finds what insiders missed
- NSS BigSig: Software fuzzing approach finds what crypto-focused testing missed
- AV research: Software security methodology applied to products whose makers assumed they were the experts
- Core argument: Domain experts share assumptions; outsiders don't share those blind spots.

### Theme 9: Exploitability Should Never Be Dismissed (3+ appearances)
- glibc 2014: 9-year-old "unexploitable" bug fully weaponized
- ESET 2015: Emulator bugs that look theoretical become practical multi-stage chains
- NSS 2021: "trivial" overflow in heavily-fuzzed code
- Core argument: "Exploitability determinations should not delay fixes." If you can't exploit it, that means YOU can't, not that nobody can.

### Theme 10: Economic Analysis of Security Mechanisms (3+ appearances)
- Anubis 2025: Proof-of-work computed cost = $0
- Password managers 2021: "zero-knowledge" marketing claims vs reality
- AV industry: Cost of added attack surface vs benefit of detection
- Core argument: Security measures must survive economic analysis. If bypass cost ≈ 0 for motivated attackers, the measure is theater.

---

## IX. Contradictions and Tensions Noted

### 1. "Powerful and flexible" vs Extreme Minimalism
- spreadsheet.html: "I usually choose powerful and flexible software over simplicity"
- hotcorner: Zero configuration, zero state, "simply delete to uninstall"
- **Possible resolution**: Powerful functionality hidden behind minimal interface. Complexity inside, simplicity outside.

### 2. Linux Advocacy vs Windows Deep Investment
- "Linux has better tools" + loads libraries on Linux for research
- Yet: 20+ years of Windows security research, WSL1 (not native Linux), Windows utilities
- **Resolution**: Uses Linux as research platform to study Windows targets. Post-Google: building tools to make Windows+WSL1 work better rather than switching.

### 3. Retro Enthusiasm vs Security Pragmatism
- Celebrates vintage software's stability
- Demonstrates ancient code harbors severe vulnerabilities
- **Genuine tension**: aged ≠ unsafe, but unmaintained likely is.

### 4. Individual Effort vs Scalable Methods
- CTF protocol: individual persistence over 20 years
- Oracle Serialization: industrial pipeline
- **Resolution**: Discovery requires individual focus; validation requires automation.

### 5. Open Source Commitment vs Private Core Tools
- loadlibrary, ctftool, halfempty: all public
- CPU fuzzer, Oracle Serialization harness, performance counter tools: never released
- **Boundary**: Exploration/audit tools public; core competitive advantage tools private.

---

## X. About/Meta Information

### Site Design
- "entirely static and written in markdown, I use pandoc and a Makefile to generate it."
- RCS tags for version control
- Source files accessible by changing .html to .md

### Site Name Etymology
- "lock.cmpxchg8b" = Pentium F00F bug (1997). Domain is a CPU vulnerability reference.

---

## XI. Summary: Research Methodology Pattern

1. **Identify neglected attack surface** — areas with less scrutiny than their privilege warrants
2. **Invest disproportionate time** — "spending more time than anyone might reasonably expect"
3. **Build custom tooling** — remove the constraint rather than work within it
4. **Scale with automation** — Oracle Serialization, containers, performance counters
5. **Verify empirically** — oracle comparison, dual-version testing
6. **Prove systemically** — not one bug but an entire class
7. **Calculate economics** — does this defense actually work at what cost?
8. **Release tools for community** — enable continuation after disclosure
9. **Document thoroughly** — show dead ends alongside successes
