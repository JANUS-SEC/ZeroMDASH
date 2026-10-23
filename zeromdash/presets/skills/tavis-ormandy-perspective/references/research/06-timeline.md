# Tavis Ormandy - Complete Career Timeline

## Overview

Tavis Ormandy is an English computer security researcher (white hat hacker) who spent nearly 20 years at Google, including 11 years on Project Zero (2014-2025). He departed Google on October 10, 2025 and became an independent vulnerability researcher based in the San Francisco Bay Area. Personal website: lock.cmpxchg8b.com

---

## Pre-Google Era (~2003-2007)

### ~2003-2006: Early Career
- **Location**: England, later Switzerland
- **Activities**: Active in open source security community, UNIX security research
- **Online Presence**: taviso.decsystem.org (now deprecated)
- **Research Focus**: UNIX security, open source auditing, Linux kernel internals
- **Confidence**: Medium (inferred from archived personal site and Wikipedia)

### 2006: LibTIFF Vulnerability Research
- **Date**: CVE-2006-3459 published August 2, 2006
- **Finding**: Multiple stack-based buffer overflows in LibTIFF before 3.8.2
- **Significance**: One of earliest publicly attributable discoveries
- **Confidence**: High (NVD confirmed)

### ~2007: Joins Google
- **Date**: Approximately 2007 (left Oct 2025 after "nearly 20 years")
- **Role**: Information Security Engineer
- **Location**: Initially Switzerland, later San Francisco Bay Area
- **Confidence**: High (Wikipedia + personal site)

---

## Google Information Security Era (2007-2014)

### 2007: Linux Kernel ia32 Syscall (CVE-2007-4573)
- **Date**: September 24, 2007
- **Finding**: Privilege escalation via IA32 system call emulation on x86_64
- **Confidence**: High (NVD confirmed)

### 2009: Linux sendpage NULL Pointer (CVE-2009-2692)
- **Date**: August 2009
- **Finding**: Local privilege escalation via uninitialized function pointers
- **Co-researcher**: Julien Tinnes
- **Confidence**: High

### 2009: udev NETLINK (CVE-2009-1185)
- **Date**: April 2009
- **Finding**: udev fails to verify kernel origin of NETLINK messages
- **Confidence**: Medium

### 2010: Linux compat Layer (CVE-2010-3081)
- **Date**: September 2010
- **Finding**: Stack pointer underflow in 32-bit compat layer; local root
- **Confidence**: High

### June 2010: Windows HCP 5-Day Disclosure (KEY TURNING POINT)
- **Date**: Reported June 5; disclosed June 10, 2010
- **Finding**: Windows Help Centre RCE via malformed URL escape sequences
- **Significance**: Most controversial disclosure of his career; established transparency-first stance
- **Confidence**: High (Full Disclosure mailing list archive)

### November 2012: Sophail Report (KEY TURNING POINT)
- **Date**: November 2012
- **Finding**: 30-page paper documenting severe Sophos AV vulnerabilities
- **Quote**: "ill-equipped to handle the output of one co-operative security researcher"
- **Significance**: Launched the "security products as attack surface" thesis
- **Confidence**: High (lock.cmpxchg8b.com/sophail.pdf)

---

## Project Zero Era (2014-2025)

### July 15, 2014: Project Zero Founded
- **Event**: Google announces Project Zero
- **Team**: Chris Evans (lead), Ian Beer, Ben Hawkes, Tavis Ormandy, others
- **Confidence**: High (Google Security Blog)

### August 25, 2014: glibc "Poisoned NUL Byte"
- **Blog**: "The poisoned NUL byte, 2014 edition"
- **Co-author**: Chris Evans
- **Finding**: Proved a 2005 off-by-one NUL byte exploitable; 9-stage chain to root
- **Key thesis**: "Exploitability determinations should not delay fixes"
- **Confidence**: High (Project Zero blog)

### September 22, 2015: Kaspersky Unpacker Vulnerabilities
- **Finding**: Stack overflow in Thinstall unpacker; no /GS; SYSTEM execution
- **Quote**: "record breaking response times" (praising Kaspersky)
- **Confidence**: High (Project Zero blog)

### June 2015: ESET Emulator RCE
- **Finding**: Multi-stage exploitation of AV emulator; shadow stack bypass + ROP
- **Significance**: macOS-specific weakness (missing heap execution prevention)
- **Confidence**: High (Project Zero blog)

### December 15, 2015: FireEye "Vulnerability of the Beast" (Issue #666)
- **Finding**: RCE via passive network monitoring (JODE decompiler exploit)
- **Co-researcher**: Natalie Silvanovich
- **Quote**: "And now we're root, with complete control"
- **Confidence**: High (Project Zero blog)

### January 2016: Trend Micro Password Manager
- **Finding**: Critical vulnerabilities in Trend Micro Password Manager
- **Confidence**: Medium-High (Wikipedia)

### May-June 2016: Symantec/Norton (PEAK AV CAMPAIGN)
- **CVE**: CVE-2016-2208 (ASPack kernel buffer overflow, CVSS 9.1)
- **Blog**: "How to Compromise the Enterprise Endpoint" (June 28)
- **Finding**: Wormable RCE; 7-year-old unpatched libraries; kernel-mode parsing
- **Quote**: "Symantec dropped the ball" / "as bad as it gets"
- **Confidence**: High (Project Zero blog + NVD)

### February 2017: Cloudbleed Discovery
- **Dates**: Feb 17 reported → Feb 19 P0 tracker → Feb 23 public
- **Finding**: Buffer over-read leaking secrets from millions of Cloudflare sites
- **Response**: 21 minutes to first contact; 47 minutes to initial mitigation
- **Significance**: Most cooperative disclosure in his career
- **Confidence**: High (Cloudflare incident report)

### March 2017: LastPass Vulnerability + "crazy bad"
- **Date**: March 27, 2017 (LastPass); May 2017 ("crazy bad" MsMpEng)
- **Finding**: Critical RCE in LastPass; Windows Defender memory corruption
- **Tweet quote**: "OK, exploit working. Now time to put some pants on."
- **Confidence**: High (Wikipedia + media)

### ~2017: loadlibrary Released
- **Project**: Port Windows DLLs to Linux for containerized fuzzing
- **GitHub**: 4.5k stars
- **Philosophy**: "distributed, scalable fuzzing on Windows can be challenging"
- **Confidence**: High (GitHub)

### September 2018: GhostScript -dSAFER Series (CVE-2018-16509)
- **Finding**: PostScript sandbox escape; -dSAFER "fragile security boundary"
- **Recommendation**: Disable PS/EPS/PDF/XPS coders in policy.xml by default
- **Confidence**: High (NVD + oss-security)

### August 13, 2019: Windows CTF Protocol
- **Blog**: "Down the Rabbit-Hole"
- **Finding**: 20-year-old undocumented IPC protocol; no access control; sandbox escape
- **Quote**: "Sometimes, hacking is just someone spending more time..."
- **Tool**: ctftool released (1.7k stars)
- **Confidence**: High (Project Zero blog)

### December 1, 2021: NSS "BigSig" (CVE-2021-43527)
- **Blog**: "This shouldn't have happened"
- **Finding**: Trivial buffer overflow in heavily-fuzzed crypto library
- **Innovation**: "Stack Coverage" concept (call stack combinations vs code blocks)
- **Key lesson**: "Even extremely well-maintained C/C++ can have fatal, trivial mistakes"
- **Confidence**: High (Project Zero blog)

### June 2021: Password Manager Evaluation
- **Blog**: lock.cmpxchg8b.com/passmgrs.html
- **Finding**: Architecture-level flaws in browser extension password managers
- **Quote**: "'use a password manager' is vague and potentially dangerous advice"
- **Recommendation**: Browser-native managers over extensions
- **Confidence**: High

### May 15, 2023: Zenbleed Reported (CVE-2023-20593)
- **Disclosure**: Reported May 15; public July 24, 2023
- **Finding**: Zen 2 CPU register file use-after-free; 30KB/s data leakage per core
- **Method**: Oracle Serialization + performance counter feedback
- **Quote**: "memory management is hard, even in silicon :)"
- **Confidence**: High (NVD + lock.cmpxchg8b.com/zenbleed.html)

### August 2023: Reptar Discovery (Internal)
- **Event**: Google validation pipeline detects anomaly with redundant rex.r prefixes
- **Confidence**: High (lock.cmpxchg8b.com/reptar.html)

### November 14, 2023: Reptar Public Disclosure (CVE-2023-23583)
- **CVSS**: 7.8-8.8
- **Finding**: Intel frontend miscalculates instruction size; corrupts ROB state across cores
- **Affected**: Ice Lake through Sapphire Rapids
- **Team**: Tavis Ormandy + Josh Eads + Eduardo Vela Nava + Alexandra Sandulescu + Daniel Moghimi + silifuzz/ISE teams
- **Confidence**: High (NVD + Intel SA-00950)

### September 25, 2024: EntrySign Reported (CVE-2024-56161)
- **Finding**: Insecure hash function (CMAC-AES) in AMD CPU microcode signature validation
- **Impact**: Load arbitrary microcode on Zen 1-4; compromise SEV-SNP
- **Method**: Meet-in-the-middle attack + RSA key forgery
- **Team**: Josh Eads, Matteo Rizzo, Kristoffer Janke, Eduardo Vela Nava, Tavis Ormandy, Sophie Schmieg
- **PoC**: Modified RDRAND to return constant 4
- **Note**: No blog post exists; details only in code (github.com/google/security-research)
- **Confidence**: High (oss-security + NVD)

### December 13-16, 2024: AMD Ships EntrySign Fix
- **Dec 13**: Zen 1/2/3 patched
- **Dec 16**: Zen 4 patched
- **Dec 17**: Embargoed fix to OEM customers
- **Confidence**: High (oss-security timeline)

---

## Departure from Google (October 2025)

### February 3, 2025: EntrySign Public Disclosure
- **Date**: NVD publication; oss-security post
- **CVSS**: 7.2 (High)
- **Quote**: "the vendor has been really excruciating to deal with, this is the first time I've been allowed to see the patch!!"
- **Confidence**: High (NVD + oss-security)

### March 5, 2025: zentool Released
- **Project**: AMD microcode manipulation/analysis tool
- **Includes**: "Microcoding Quickstart" 436-line tutorial
- **Zen 5 note**: "Zen 5 uses a different CMAC key"
- **Confidence**: High (GitHub)

### April 7, 2025: Zen 5 (Turin) Added to EntrySign Advisory
- **Confidence**: High (AMD bulletin)

### July 2024: "Terminal Lag" Blog Post
- **Blog**: lock.cmpxchg8b.com/slowterm.html
- **Topic**: Systematic debugging of WSL xterm 5x performance gap
- **Confidence**: High (blog index)

### July 27, 2024: defermap Repository Created
- **Project**: X11 server mode for fast terminal launch (pre-cached instances)
- **Confidence**: High (GitHub)

### August 2025: Anubis Blog Post
- **Blog**: lock.cmpxchg8b.com/anubis.html
- **Topic**: Proof-of-work anti-bot economic demolition
- **Hook**: "why are anime catgirls blocking my access to the Linux kernel?"
- **Finding**: ~$0 monthly cost to bypass all 11,500 deployments
- **Significance**: Possibly last article written while at Google
- **Confidence**: High (blog)

### October 10, 2025: Leaves Google
- **Event**: Departs after ~18-20 years
- **No farewell**: No blog post, no P0 blog mention
- **Confidence**: High (Wikipedia)

---

## Independent Researcher Era (October 2025 - Present)

### Post-October 2025: Key Observation
**Zero vulnerability disclosures in 7+ months.** All activity is personal tool development for WSL1/Windows environment.

### November 4, 2025: First Post-Departure Code
- **Project**: matrix3 commits (uMatrix replacement for Manifest V3)
- **Confidence**: High (GitHub)

### December 2025: selectwin + wslcompat
- **Dec 9**: Released selectwin utility
- **Dec 22**: Merged ctypes.sh PR
- **Dec 25**: Resumed wslcompat work
- **Confidence**: High (GitHub)

### February 2025: dpapi Repository
- **Feb 18**: Started dpapi utility development
- **Apr 21**: Published dpapi repo
- **Confidence**: High (GitHub)

### July 2025: wslcompat + endperiod
- **Jul 26**: Started wslcompat (WSL1 LD_PRELOAD polyfill library)
- **Jul 31**: Released endperiod utility
- **Confidence**: High (GitHub)

### September 2025: matrix3
- **Sep 17**: Created matrix3 (uMatrix replacement for Chrome MV3)
- **Confidence**: High (GitHub)

### 2026 Activity (January-May)
- **Feb 9**: wslcompat TCGETS2 work
- **Feb 21**: Merged 123elf bugfix PR
- **Mar-Apr**: Ongoing wslcompat development
- **Apr 14**: Forked `lxdk` (WSL1 kernel driver development kit)
- **May 2-8**: Intensive 26-commit sprint on wslcompat (polyfills, file locking, tests)
- **Confidence**: High (GitHub API)

---

## Blog Index (Complete: 18 Posts, Oct 2020 - Aug 2025)

| Date | Slug | Topic |
|------|------|-------|
| Oct 2020 | lotusagenda | Lotus Agenda appreciation |
| Nov 2020 | spreadsheet | Spreadsheet software review |
| Nov 2020 | watch | Casio Protrek watch |
| Dec 2020 | tektronix | XTerm Tektronix popup ads |
| Dec 2020 | symcoll | Dual library version linking |
| Feb 2021 | lotus123 | Lotus 1-2-3 custom display driver |
| Jun 2021 | passmgrs | Password manager evaluation |
| May 2022 | linux123 | Recovered Lotus 1-2-3 for Linux |
| Jul 2022 | wordperfect | WordPerfect Sixel graphics |
| Aug 2022 | symbols | Restoring debug symbols |
| Nov 2022 | watch | (same slug, different content?) |
| Jan 2023 | doom | Templates of Doom |
| Dec 2023 | hiew | Hiew hex editor |
| Dec 2023 | ledger | Personal finance with Ledger |
| Jul 2024 | slowterm | Terminal startup performance |
| Aug 2025 | anubis | Anubis proof-of-work critique |

**Note**: No new blog posts after August 2025 as of May 2026.

---

## Research Phase Transitions

### Phase 1: Linux Kernel (2007-2012)
Focus: privilege escalation, syscall interfaces, memory management

### Phase 2: AV/Security Products as Attack Surface (2012-2018)
Trigger: Sophos research (2011-2012)
Peak: Symantec (June 2016)
Tool: loadlibrary (2017)

### Phase 3: Protocol & Application Security (2017-2021)
Cloudbleed, LastPass, GhostScript, Windows CTF, NSS BigSig

### Phase 4: CPU/Hardware (2023-2025)
Trigger: Zenbleed (reported May 2023)
Method: Oracle Serialization + performance counter feedback
Capstone: EntrySign (AMD microcode signing bypass)

### Phase 5: Independent/Personal Tools (2025.10-Present)
Focus: WSL1 compatibility (wslcompat, lxdk), browser extension (matrix3), utilities
Pattern: Zero security publications; building personal infrastructure
Interpretation: "fix the environment, don't change your workflow"

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Years at Google | ~18-20 (2007 - Oct 2025) |
| Years on Project Zero | ~11 (2014-2025) |
| Notable CVEs | 20+ confirmed high/critical |
| AV vendors targeted | 6+ |
| CPU vendors targeted | 2 (AMD, Intel) |
| GitHub repos | 40 |
| GitHub followers | 3,200+ |
| GitHub following | 3 (jcs, jafl, stealth) |
| Blog posts | 18 (Oct 2020 - Aug 2025) |
| Post-departure vuln publications | 0 (7+ months) |

---

## Source Reliability Notes

- **High confidence**: NVD (exact dates), Project Zero blog, Cloudflare incident report, lock.cmpxchg8b.com, GitHub API, oss-security archives
- **Medium confidence**: Wikipedia (cross-referenced), blog date indicators, GitHub commit timestamps
- **Low confidence**: Inferred motivations, pre-2007 career details
- **Research date**: 2026-05-09
