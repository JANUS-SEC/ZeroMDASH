# Mark Brand -- Career & Research Timeline

## Overview

Mark Brand is a security researcher at Google Project Zero, known for his work on
browser exploitation (Chrome), memory corruption vulnerabilities, sandbox escape
techniques, GPU/graphics attack surfaces, and hardware memory safety mitigations
(ARM MTE). His Twitter handle is @sidrfrk. He self-describes as an "Exploit
Technique Archaeologist" (per his April 2019 blog post byline).

---

## Pre-Google / Early Career

| Period | Event | Certainty | Source |
|--------|-------|-----------|--------|
| Unknown | Education and early career details are not publicly documented. No confirmed LinkedIn profile or academic publications found in open sources. | Unconfirmed | Negative search result across multiple sources |
| Pre-2017 (estimate) | Joined Google Project Zero. The exact date is unknown, but his first confirmed P0 blog post is from July 2018. His bug tracker activity and acknowledgments in 2018 posts suggest he was active by at least 2017-2018. | Medium confidence | Inference from publication timeline |

---

## Confirmed Project Zero Publications & Activities (Chronological)

### 2018

| Date | Event | Type | Source |
|------|-------|------|--------|
| July 26, 2018 | Co-authored "Drawing Outside the Box: Precision Issues in Graphic Libraries" with Ivan Fratric. Investigated floating-point precision vulnerabilities in SwiftShader (Chrome's software OpenGL implementation) leading to OOB memory access via WebGL. | Blog post | googleprojectzero.blogspot.com/2018/07/ |
| September 2018 | Acknowledged by Jann Horn in "A cache invalidation bug in Linux memory management" for exploit technique insight ("Thanks to Mark for pointing out that if you control RDI and RIP...") | Acknowledgment | googleprojectzero.blogspot.com/2018/09/ |
| October 24, 2018 | Authored "Heap Feng Shader: Exploiting SwiftShader in Chrome". Demonstrated full exploit of SwiftShader vulnerabilities: info leak via framebuffer precision bug + use-after-free via reference count overflow in egl::ImageImplementation, leading to code execution in Chrome's GPU process. Described technique of forcing Chrome to fall back to software rendering. | Blog post | googleprojectzero.blogspot.com/2018/10/ |

### 2019

| Date | Event | Type | Source |
|------|-------|------|--------|
| April 11, 2019 | Authored "Virtually Unlimited Memory: Escaping the Chrome Sandbox". Detailed a full-chain Chrome sandbox escape exploiting: (1) CVE-2019-5782 (V8 typer bug by _tsuro), (2) Issue 1755 (FileWriter UAF via base::Unretained), (3) Issue 1642 (Mojo DataPipe dispatcher shared memory bug for ASLR bypass). Demonstrated 3.5+ TB memory spray and ROP chain in browser process on Windows 64-bit. Self-described as "Exploit Technique Archaeologist". | Blog post | projectzero.google/2019/04/virtually-unlimited-memory-escaping.html |

### 2020

| Date | Event | Type | Source |
|------|-------|------|--------|
| 2020 | No solo blog posts identified for this year. However, Mark Brand was active in Chrome/browser security research during this period (his work is referenced in the January 2021 "In-the-Wild Series: Chrome Infinity Bug" post by Sergei Glazunov, which mentions Brand's full-chain exploit as a reference for typer bug exploitation). | Activity inference | projectzero.google/2021/01/ |

### 2021

| Date | Event | Type | Source |
|------|-------|------|--------|
| January 2021 | Referenced in "In-the-Wild Series: Chrome Infinity Bug" (by Sergei Glazunov) as a fellow Project Zero member whose full-chain Chrome exploit demonstrated typer bug exploitation techniques. | Reference | projectzero.google/2021/01/in-wild-series-chrome-infinity-bug.html |

### 2022

| Date | Event | Type | Source |
|------|-------|------|--------|
| 2022 (mid) | Gained access to pre-production ARM hardware with MTE support. Began systematic evaluation of Memory Tagging Extension as a security mitigation. | Research activity | Mentioned in August 2023 MTE blog series |

### 2023

| Date | Event | Type | Source |
|------|-------|------|--------|
| August 2, 2023 | Authored 4-part series "MTE As Implemented" -- the most comprehensive public evaluation of ARM Memory Tagging Extension as a security mitigation. Parts: (1) Implementation Testing, (2) Mitigation Case Studies, (3) The Kernel, (4) Summary. Key findings: no additional speculative side-channels beyond existing Spectre; identified 4 Linux kernel implementation issues; async-MTE provides "soft mitigation" only; exploits must complete within ~0.2ms; MTE is "by far the most promising path forward for improving C/C++ software security in 2023". | Blog series (4 posts) | googleprojectzero.blogspot.com/2023/08/ |
| November 3, 2023 | Authored "First handset with MTE on the market" -- announced Pixel 8/8 Pro as first production devices with MTE. Reported running personal Pixel 8 with MTE enabled since release with no app compatibility issues. Provided step-by-step ADB instructions for enabling MTE. Created demonstration app showing MTE catching use-after-free (SEGV_MTESERR). Advocated for broader MTE adoption. | Blog post | googleprojectzero.blogspot.com/2023/11/ |

### 2024

| Date | Event | Type | Source |
|------|-------|------|--------|
| June 20, 2024 | Co-authored "Project Naptime: Evaluating Offensive Security Capabilities of Large Language Models" with Sergei Glazunov. Developed framework improving LLM performance on CyberSecEval 2 benchmark by up to 20x. Proposed 5 guiding principles for LLM-assisted vulnerability research. Marks shift toward AI-assisted security research. | Blog post | projectzero.google/2024/06/project-naptime.html |
| November 1, 2024 | Listed as team member on "From Naptime to Big Sleep: Using Large Language Models To Catch Vulnerabilities In Real-World Code". The Big Sleep AI agent (collaboration between Project Zero and Google DeepMind) found first public AI-discovered exploitable memory-safety bug in real-world software (SQLite stack buffer underflow). Full team: Miltos Allamanis, Martin Arjovsky, Charles Blundell, Lars Buesing, Mark Brand, Sergei Glazunov, Dominik Maier, Petros Maniatis, Guilherme Marinho, Henryk Michalewski, Koushik Sen, Charles Sutton, Vaibhav Tulsyan, Marco Vanotti, Theophane Weber, Dan Zheng. | Blog post / Team | googleprojectzero.blogspot.com/2024/11/ |

### 2025-2026

| Date | Event | Type | Source |
|------|-------|------|--------|
| 2025 (Jan-Dec) | No solo-authored blog posts found on the Project Zero blog for this entire year. The blog published posts by James Forshaw (Jan), Ian Beer (Mar, Aug), Mateusz Jurczyk (Apr, May), Tim Willis (Jul), Jann Horn (Aug, Sep), Seth Jenkins (Nov), and Benoit Sevens (Dec). Mark Brand's name does not appear as author in any 2025 post. | Negative finding | Systematic search of all 2025 monthly archives |
| 2026 (Jan-May) | No blog posts or public announcements found. No confirmed departure announcement. | Negative finding | Search as of May 2026 |

---

## Research Direction Evolution

### Phase 1: Graphics/GPU Attack Surface (2018)
- SwiftShader precision bugs, WebGL as attack vector
- Focus: finding JS-accessible attack surface in "unlikely places"
- Software rendering as a forced fallback creating new attack surface

### Phase 2: Chrome IPC/Mojo & Sandbox Escape (2018-2019)
- Full-chain browser exploitation (renderer compromise to sandbox escape)
- Mojo IPC as a critical attack surface between renderer and browser processes
- FileWriter UAF, DataPipe dispatcher bugs
- Windows-specific ASLR bypass techniques

### Phase 3: Hardware Memory Safety Mitigations -- MTE (2022-2023)
- Major pivot to evaluating hardware-based defenses
- Comprehensive analysis of ARM MTE as deployed on real hardware
- Assessing effectiveness against memory corruption exploitation
- Advocating for industry-wide MTE adoption
- Published the most comprehensive public evaluation of MTE

### Phase 4: AI-Assisted Vulnerability Research (2024-present)
- Project Naptime: LLM frameworks for offensive security
- Big Sleep: First AI-discovered real-world exploitable bug
- Collaboration with Google DeepMind
- Focus on augmenting human researchers with AI tools

---

## Notable Vulnerability Discoveries (Confirmed)

| CVE/Issue | Year | Target | Type | Impact |
|-----------|------|--------|------|--------|
| SwiftShader precision bug | 2018 | Chrome GPU process | Floating-point precision error | Information leak |
| SwiftShader refcount overflow | 2018 | Chrome GPU process | Reference count overflow / UAF | Code execution |
| Issue 1755 (FileWriter UAF) | 2019 | Chrome browser process | Use-after-free via base::Unretained | Sandbox escape |
| Issue 1642 (Mojo DataPipe) | 2019 | Chrome browser process | Shared memory mapping bug | ASLR bypass |
| Linux kernel MTE implementation bugs (4) | 2023 | Linux kernel ARM64 | Implementation gaps in MTE | Mitigation bypass |

---

## Conference Talks (Known/Inferred)

No confirmed public conference talks were found in the available sources (HITB, Hexacon archives searched). Mark Brand's primary publication channel appears to be the Project Zero blog. It is possible he has given internal Google talks or attended invitation-only events, but no public records were found.

---

## Current Status (as of May 2026)

- **Still at Project Zero**: No departure announcement found. His name appeared on the Big Sleep team (November 2024), confirming activity through late 2024.
- **No 2025-2026 solo publications**: The absence of blog posts in 2025-2026 is notable but not conclusive -- other P0 members also have publication gaps. The shift to AI-assisted research (Naptime/Big Sleep) may indicate his work is now more team-oriented and published under group authorship.
- **No confirmed career change**: No LinkedIn updates, Twitter announcements, or other signals of departure from Google/Project Zero found in available sources.
- **Possible explanation for reduced visibility**: The Big Sleep/Naptime project is a large collaborative effort between P0 and DeepMind. Brand may be primarily contributing to this ongoing project without individual blog output.

---

## Key Characteristics (from publications)

1. **Practical exploit developer**: Every blog post includes working exploitation, not just bug discovery
2. **Systems-level thinker**: Connects renderer bugs to browser process compromises to OS-level ASLR bypasses
3. **Mitigation evaluator**: Critical but constructive assessment of security boundaries and hardware mitigations
4. **Creative attack surface identification**: Finding exploitable surfaces in unexpected components (SwiftShader, MTE implementation gaps)
5. **Cross-layer understanding**: Spans GPU hardware, browser architecture, OS kernel, and now AI/ML

---

## Source Reliability Notes

- **High confidence**: Blog posts with byline attribution, direct quotes
- **Medium confidence**: References in other researchers' posts, team listings
- **Low confidence**: Inferences about timeline gaps and career status based on absence of evidence
- **Unverified**: Pre-Google career, education, exact P0 join date

---

## Gaps in Knowledge

1. **Education**: No publicly available information about university or degree
2. **Pre-P0 career**: No confirmed employer before Google. The @sidrfrk Twitter handle has not been systematically reviewed (restricted access)
3. **Exact P0 join date**: Likely 2016-2017 based on first publications in 2018, but not confirmed
4. **2020-2021 activity**: No confirmed solo blog posts; likely active on bug reports but these are behind authentication on the issue tracker
5. **2025-2026 activity**: Complete absence from public P0 blog; status unclear but no departure signals
6. **Conference talks**: None confirmed through available web sources; may have presented at invitation-only events
