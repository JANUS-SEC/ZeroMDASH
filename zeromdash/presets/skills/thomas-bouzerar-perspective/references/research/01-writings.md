# Thomas Bouzerar - Writings and Systematic Long-Form Content

## Researcher Profile Summary

- **Affiliation**: Synacktiv (French cybersecurity firm)
- **Twitter/X**: @MajorTomSec
- **Specializations**: Virtualization/hypervisor exploitation, VM escapes, embedded security, iOS security, console hacking (PlayStation)
- **Notable Achievement**: Member of the team that won Pwn2Own Vancouver 2023
- **Frequent Collaborators**: Thomas Imbert (@masthoon), Corentin Bayet, Etienne Helluy-Lafont

---

## PRIMARY WRITINGS (His Own Authorship - Confirmed)

### 1. "On the Clock: Escaping VMware Workstation at Pwn2Own Berlin 2025"

- **Date**: January 23, 2026
- **URL**: https://www.synacktiv.com/publications/on-the-clock-escaping-vmware-workstation-at-pwn2own-berlin-2025.html
- **Co-author**: Etienne Helluy-Lafont
- **Credibility**: PRIMARY (his own writing, long-form blog post on Synacktiv)
- **Language**: French original with English translation available
- **CVE**: CVE-2025-41238

**Core Argument/Contribution**:
Demonstrates a complete VMware Workstation guest-to-host escape through exploitation of a heap-overflow vulnerability in the PVSCSI (Paravirtualized SCSI) controller. The key technical innovations are:

1. **"Ping-Pong" technique**: A novel method to defeat Windows 11 Low Fragmentation Heap (LFH) randomization by forcing the allocator into deterministic alternation between two memory locations during repeated reallocations. The allocator "will bounce incessantly between two available locations."

2. **PVSCSI coalescing exploitation**: Weaponizing the segment coalescing algorithm within the PVSCSI controller to propagate corrupted data into arbitrary memory structures.

3. **Timing side-channel for LFH state recovery**: Discovered 2 days before competition. Uses VMware's synchronous backdoor channel (vmx.capability.unified_loop) to trigger controlled allocations and measure timing variations when new LFH buckets are created versus reused, defeating heap ASLR.

4. **URB (USB Request Block) fabrication**: Creating hybrid URB structures that combine metadata from different objects to achieve information leaks and arbitrary memory access.

**Methodology Revealed**:
- Reverse engineering of vmware-vmx process (binary analysis, not source review)
- Focused on device emulation as known VM escape attack surface
- Found the vulnerability "fairly quickly" once focused on PVSCSI controller audit
- 3-month timeline: Month 1 = RE and vuln discovery, Month 2 = procrastination, Month 3 = exploitation sprint (core exploit developed in final 5 days)
- Exploit succeeded on first attempt during live competition

**Writing Style Observations**:
- Chronological narrative structure mirroring the actual research process
- Self-deprecating humor about timeline management
- Blends technical precision with conversational tone
- Candidly discusses failed approaches and dead ends
- Uses concrete analogies (Ping-Pong metaphor) for abstract heap concepts
- References prior art contextually rather than in separate bibliography
- French technical vocabulary: "debordement" (overflow), "fusionner" (coalesce), "faconner" (shape), "agencement du tas" (heap layout)

**Key Quotes** (paraphrased from article):
- "Convinced that exploitation would be simple, we spent the second month procrastinating."
- "We formally advise against reproducing our timeline - unless you particularly enjoy sleep deprivation."
- "The first month was dedicated to reverse-engineering VMware... The third month was a harsh return to reality."

**Referenced Prior Art**:
- Saar Amar's LFH exploitation research
- Zilis Sialveras and Corentin Bayet on VMware SVGA exploitation
- Yuhao Jiang and Xinlei Ying's URB-based VM escapes
- Nafod's UHCI bridge work

---

### 2. "Virtualization from an Attacker Point of View" (Conference Presentation)

- **Date**: October 6, 2023 (creation date from PDF metadata)
- **Conference**: GreHack 2023
- **URL (slides)**: https://www.synacktiv.com/sites/default/files/2023-11/virtu_attacker_pov_grehack2023.pdf
- **URL (video)**: https://www.youtube.com/live/6KddjKKKEL4?si=f18bh8wJ8hAqqUtn&t=5651
- **Co-author**: Corentin Bayet
- **Credibility**: PRIMARY (his own presentation)
- **PDF Metadata Author field**: "corentin;thomas"

**Core Argument/Contribution**:
A survey/introduction talk covering virtualization from an offensive security perspective. Based on the references extracted from the PDF, it covers:

- Virtualization internals and architecture
- VMware paravirtualization mechanisms
- Known hypervisor vulnerability classes (heap overflows in ESXi - CVE-2021-21974)
- KVM/AMD SEV exploitation (references Google Project Zero's "An EPYC Escape" case study)
- VMware Workstation exploitation history (references Synacktiv's prior "Speedpwning VMware Workstation" work)
- Hyper-V exploitation landscape (references awesome-hyper-v-exploitation)
- General hypervisor vulnerability research methodology (references Alisa Esage's "Hypervisor Vulnerability Research 2020")

**Referenced Resources** (extracted from PDF):
- https://docs.saferwall.com/blog/virtualization-internals-part-1-intro-to-virtualization
- https://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/techpaper/VMware_paravirtualization.pdf
- https://qiuhao.org/Matryoshka_Trap.pdf
- https://alisa.sh/slides/HypervisorVulnerabilityResearch2020.pdf
- https://www.synacktiv.com/sites/default/files/2020-10/Speedpwning_VMware_Workstation.pdf (cited twice)
- https://github.com/shogunlab/awesome-hyper-v-exploitation
- https://www.keysight.com/blogs/tech/nwvs/2023/02/24/remote-code-execution-with-esxi-cve-2021-21974-vmware-esxi-heap-overflow (cited twice)
- https://googleprojectzero.blogspot.com/2021/06/an-epyc-escape-case-study-of-kvm.html

---

### 3. "Breaking Out of the Box: Technical Analysis of VirtualBox VM Escape with Windows LPE" (Conference Presentation)

- **Date**: October 13-14, 2023 (Hexacon 2023 conference dates)
- **Conference**: Hexacon 2023 (Paris, France)
- **URL (slides)**: https://www.synacktiv.com/sites/default/files/2023-10/hexacon_breaking_out_of_the_box.pdf
- **Co-author**: Thomas Imbert (@masthoon)
- **Credibility**: PRIMARY (his own presentation at a prestigious single-track conference)

**Core Argument/Contribution**:
Details "a chain of three bugs demonstrated at Pwn2Own Vancouver 2023 targeting VirtualBox and Windows 11 kernel." The presentation covers:

1. **Methodology used to find bugs reachable from inside a guest machine** - this is a key methodological contribution showing how to systematically identify VM escape attack surfaces
2. **How to exploit and chain together multiple bugs** - multi-bug chaining from guest VM escape to host privilege escalation
3. **VirtualBox guest-to-host escape + Windows 11 kernel LPE** - full exploit chain

**Context**:
This work was part of Synacktiv's winning Pwn2Own Vancouver 2023 campaign. The team demonstrated a complete guest-to-host escape from an Oracle VirtualBox VM combined with a Windows 11 kernel local privilege escalation.

---

## SECONDARY/CONTEXTUAL INFORMATION

### Biographical Data (from Hexacon 2023 speaker page)

- **Credibility**: SECONDARY (conference organizer's description)
- **Source**: Hexacon 2023 website

Thomas Bouzerar is described as a "security researcher specializing in iOS and embedded devices, with prior PlayStation console hacking experience." His team won Pwn2Own Vancouver 2023.

His co-presenter Thomas Imbert is described as having "reverse engineering expertise focused on Windows," previously worked at Microsoft, and won Pwn2Own Austin 2021 and Vancouver 2023.

---

### Pwn2Own Track Record (from various sources)

- **Credibility**: SECONDARY (competition results, third-party reporting)

- **Pwn2Own Vancouver 2023**: Part of winning Synacktiv team. Contributed to VirtualBox guest-to-host escape + Windows 11 LPE chain (3 bugs chained)
- **Pwn2Own Berlin 2025**: VMware Workstation escape via PVSCSI heap overflow (CVE-2025-41238), co-authored with Etienne Helluy-Lafont

---

## RECURRING THEMES AND PATTERNS (Appearing >= 2 times)

### 1. Device Emulation as Primary Attack Surface
- In VMware article: "Devices represent a well-known attack surface for VM escape exploits"
- In Grehack talk: Covers device emulation vulnerabilities across VMware, VirtualBox
- In Hexacon talk: "Methodology used to find bugs reachable from inside a guest machine"
- **Pattern**: Consistently focuses on virtual device emulation code (PVSCSI, USB, network, graphics) as the entry point for hypervisor exploitation

### 2. Heap Exploitation Under Modern Mitigations
- In VMware article: Core contribution is defeating Windows 11 LFH mitigations
- In VirtualBox exploit: Chained bugs including host-side exploitation
- **Pattern**: Specializes in heap manipulation techniques that work despite modern allocator hardening (LFH randomization, metadata verification)

### 3. Time-Pressured Competition Exploitation
- VMware article: "Core exploit developed in final five days," timing solution found "two days before the contest"
- VirtualBox exploit: Demonstrated live at Pwn2Own Vancouver 2023
- **Pattern**: Works under extreme time pressure for competition targets; admits to procrastination followed by productive sprints

### 4. Multi-Bug Chaining
- VirtualBox: 3 bugs chained (VM escape + kernel LPE)
- VMware: Multiple primitives chained (info leak + memory read/write + code execution)
- **Pattern**: Approaches exploitation as constructing chains of primitives rather than single-shot exploits

### 5. Reverse Engineering Over Fuzzing
- VMware article: "First month was dedicated to reverse-engineering VMware"
- VMware article: Found vulnerability through focused manual audit of PVSCSI controller
- Grehack talk: Positions as understanding virtualization internals deeply
- **Pattern**: Prefers manual reverse engineering and targeted code audit over automated fuzzing for vulnerability discovery

---

## TECHNICAL APPROACH CHARACTERIZATION

Based on confirmed writings:

1. **Attack surface selection**: Identifies well-understood attack surfaces (device emulation) but applies novel exploitation techniques
2. **Vulnerability discovery**: Manual reverse engineering and focused code audit rather than fuzzing
3. **Exploitation philosophy**: Develops novel techniques to defeat specific mitigations (LFH Ping-Pong, timing side-channels) rather than avoiding them
4. **Innovation pattern**: Core innovations emerge under time pressure ("two days before the contest")
5. **Documentation style**: Narrative chronological structure, candid about failures and procrastination, uses humor and analogies
6. **Collaboration model**: Works with specialized partners (Imbert for Windows kernel, Helluy-Lafont for VMware, Bayet for virtualization surveys)

---

## SELF-CREATED TERMINOLOGY/CONCEPTS

1. **"Ping-Pong" technique** - Method to force deterministic heap allocation behavior despite LFH randomization by controlling free chunk pointers to alternate between exactly two locations
2. **Coalescing exploitation** - Weaponizing the PVSCSI scatter-gather coalescing algorithm to propagate controlled data through heap structures
3. **"On the Clock"** framing - Presenting exploit development as a race against competition deadlines, making timeline management part of the technical narrative

---

## CONTRADICTIONS AND GAPS

1. **Hexacon bio says "iOS and embedded devices"** but his most substantial published work is on hypervisor/VM exploitation. This may indicate unpublished iOS/embedded work or that his focus shifted over time.
2. **"PlayStation console hacking experience"** mentioned in bio but no published writeups found about this work.
3. **No standalone QEMU exploitation writeup found** despite being frequently associated with QEMU/hypervisor research in descriptions of his expertise.
4. **No identified personal blog or independent publication channel** - all confirmed writing is through Synacktiv's platform.
5. **Grehack 2023 talk is listed as co-authored with "Corentin Bayet"** on Synacktiv resources page, but PDF metadata says "corentin;thomas" (likely Corentin Bayet and Thomas Bouzerar, possibly also Thomas Imbert given the resources page listing).

---

## PUBLICATIONS NOT FOUND / UNCONFIRMED

The following were searched for but NOT found as confirmed Thomas Bouzerar publications:
- Any standalone QEMU exploitation writeup
- Any iOS exploitation writeup
- Any PlayStation hacking writeup
- Any embedded device exploitation writeup (despite bio claiming this specialization)
- Any blog posts prior to 2023
- Any academic papers or whitepapers
- Any individual CVE advisories authored solely by him

---

## SOURCES CONSULTED

- Synacktiv publications page (https://www.synacktiv.com/en/publications)
- Synacktiv resources page (https://www.synacktiv.com/ressources) - confirmed 2 presentations
- Synacktiv sitemap.xml - full publication list checked
- Hexacon 2023 speakers page - confirmed talk details and bio
- GreHack 2023 program - confirmed presentation
- GitHub (synacktiv organization, Bouzerar user) - no repos attributed to him
- PDF metadata extraction from both presentation slide decks
- Full text of "On the Clock" VMware article (the most substantial confirmed writing)
- 20+ other Synacktiv publications checked for his authorship (none found)

---

## ASSESSMENT OF WRITING VOLUME

Thomas Bouzerar has a **relatively small public writing footprint** compared to other top-tier security researchers:
- 1 confirmed long-form blog post (VMware Workstation, Jan 2026)
- 2 confirmed conference presentations (Hexacon 2023, Grehack 2023)
- Both presentations are slides-only (PDF), not written papers

This suggests either:
(a) He is early-career and building his publication record
(b) Much of his work remains unpublished/proprietary
(c) He prioritizes competition results over publication
(d) Some work may be under embargo or NDA

The VMware article is by far the most substantial and revealing piece of his technical thinking available publicly.
