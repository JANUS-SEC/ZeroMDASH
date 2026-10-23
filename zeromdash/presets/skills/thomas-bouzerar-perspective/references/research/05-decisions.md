# Thomas Bouzerar - Key Decisions

## Summary of Sources

Primary sources consulted:
- Synacktiv publications and advisories website (synacktiv.com)
- Synacktiv resources/presentations archive
- Zero Day Initiative Pwn2Own results blogs (zerodayinitiative.com)
- GitHub (synacktiv organization, public repos)
- Conference programs (Grehack, Hexacon, THCON, Sthack)

---

## Decision 1: Choosing to Specialize in Virtualization/Hypervisor Security

**Context:** Thomas Bouzerar is a security researcher at Synacktiv. His conference presentation history shows he began presenting on virtualization topics publicly in 2023, with two dedicated talks at major security conferences within the same year.

**Choice made:** Focused research career on virtualization attack surfaces, including hypervisors (VMware, VirtualBox, QEMU) and virtual machine escape techniques.

**Reasoning (inferred from public evidence):**
- His Grehack 2023 talk "Virtualization from an attacker point of view" (co-presented with Corentin Bayet) systematically examines virtualization from an offensive perspective, suggesting a deliberate analytical framework for attack surface selection.
- His Hexacon 2023 talk "Breaking out of the box" (co-presented with Thomas Imbert) directly addresses VM escape techniques, the culmination of directed research.
- At Pwn2Own Vancouver 2023, he and Thomas Imbert demonstrated a "3-bug chain against Oracle VirtualBox with a Host EoP" -- this is a high-complexity, high-reward target category.
- His collaboration with Corentin Bayet (who co-authored "Speedpwning VMware Workstation" at Ekoparty 2020) suggests he apprenticed or collaborated closely with Synacktiv's existing virtualization expertise.

**Outcome:** Successful VM escape demonstration at Pwn2Own Vancouver 2023 (earning $80,000, though one bug was a collision with a previously known issue). Multiple high-profile conference presentations.

**Credibility:** MEDIUM-HIGH. The specialization is clearly documented through conference talks and Pwn2Own entries, but the specific reasoning for choosing this field is inferred from the pattern of collaborations and outputs, not from direct public statements.

---

## Decision 2: Working at Synacktiv

**Context:** Synacktiv is a French offensive security firm based in Paris, known for Pwn2Own competition success across multiple categories (Tesla, macOS, Linux, virtualization, embedded devices). They have won Master of Pwn at Pwn2Own Vancouver multiple times.

**Choice made:** Joined and remained at Synacktiv as a security researcher.

**Reasoning (inferred):**
- Synacktiv offers a team-based Pwn2Own competition structure where researchers can collaborate on complex multi-bug chains.
- The firm has deep institutional expertise in virtualization security (Corentin Bayet, Bruno Pujos previously worked on VMware Workstation exploitation; Mehdi Talbi on FreeBSD hypervisor attacks).
- Synacktiv supports researchers in presenting at security conferences (Hexacon, Grehack, THCON, Sthack) and publishing advisories.
- The firm is recognized as a top-tier French offensive security company with diverse target exposure.
- His earliest known advisory (Raft game RCE, December 2022) is already credited through Synacktiv, suggesting he was there at least since 2022.

**Outcome:** Access to team resources, mentorship from senior virtualization researchers, Pwn2Own team support, and a publication pipeline.

**Credibility:** LOW-MEDIUM. The fact he works at Synacktiv is confirmed, but the reasoning for this specific career choice (vs. other firms, vs. independent research) has no public statement.

---

## Decision 3: Target Selection at Pwn2Own Vancouver 2023 - Oracle VirtualBox

**Context:** Pwn2Own Vancouver 2023 offered multiple target categories including Enterprise Applications, Local Escalation of Privilege, Server-Side, Virtualization (VMware Workstation, Oracle VirtualBox), Automotive (Tesla), and Communication (Microsoft Teams). Synacktiv registered multiple entries across different categories.

**Choice made:** Thomas Bouzerar and Thomas Imbert specifically targeted Oracle VirtualBox in the Virtualization category, using a 3-bug chain approach.

**Reasoning (inferred):**
- VirtualBox's 3D acceleration (Chromium library) is a known complex attack surface that has been productively researched before.
- The Virtualization category carries high rewards ($150,000+ for guest-to-host escape) relative to some other categories.
- Choosing VirtualBox over VMware Workstation/ESXi may indicate a strategic calculation: VirtualBox is open-source, which provides the attacker with full source code access for vulnerability discovery, potentially making bug-finding more efficient within Pwn2Own preparation timelines.
- A 3-bug chain demonstrates sophisticated capability and likely involves: (1) a bug to gain code execution within the VM guest context, (2) a bug to escape the VM boundary, and (3) a host privilege escalation. This multi-step approach shows willingness to chain complex vulnerabilities.

**Outcome:** Successful demonstration earning $80,000 and 8 Master of Pwn points. However, one bug was a "collision" (previously known), which reduced the novelty credit.

**Credibility:** HIGH for the facts (ZDI official results confirm this entry). MEDIUM for reasoning (strategic rationale inferred from target properties, not stated publicly).

---

## Decision 4: Team Composition Strategy - Pairing with Thomas Imbert

**Context:** At Pwn2Own, researchers can compete solo or in teams of varying sizes. Synacktiv deploys different team compositions for different targets.

**Choice made:** Bouzerar paired with Thomas Imbert for the VirtualBox escape at Pwn2Own Vancouver 2023 and co-presented "Breaking out of the box" at Hexacon 2023 with him.

**Reasoning (inferred):**
- The duo approach (rather than solo) suggests the complexity of a 3-bug chain requires collaboration -- different bugs may require different expertise or parallel research efforts.
- Imbert may bring complementary skills (e.g., privilege escalation expertise) while Bouzerar focuses on the VM escape primitive.
- The continued collaboration at Hexacon 2023 suggests this was a productive partnership that extended beyond competition to knowledge dissemination.

**Outcome:** Successful 3-bug chain demonstration. Joint Hexacon 2023 presentation.

**Credibility:** MEDIUM. The pairing is confirmed (ZDI results + Hexacon program), but the internal division of labor and rationale for this specific pairing is not publicly documented.

---

## Decision 5: Diversifying Research Beyond Virtualization

**Context:** While Bouzerar's primary public identity is virtualization research, his presentation and advisory history shows broader interests.

**Choice made:** Maintained research breadth across multiple domains:
- Virtualization/hypervisor exploitation (Grehack 2023, Hexacon 2023, Pwn2Own 2023)
- Windows security internals: authentication (THCON 2023 with Geoffrey Bertoli) and named pipes (Sthack 2025)
- Game security (Raft RCE advisory, December 2022)

**Reasoning (inferred):**
- The THCON 2023 talk on "Windows authentication over HTTP & Prox-Ez" suggests interest in Windows internals that could be synergistic with virtualization exploitation (understanding host OS behavior is critical for VM escape post-exploitation).
- The Sthack 2025 talk on "Hooking Windows Named Pipes" similarly addresses Windows IPC mechanisms relevant to both local privilege escalation and potentially VM escape chains.
- The Raft game RCE (2022) may represent earlier career exploration or a side project during game security assessments.
- This breadth is characteristic of the Synacktiv model where researchers contribute across engagements (pentesting, competition prep, advisory publication).

**Outcome:** A research profile that bridges virtualization and Windows internals, with both areas feeding into competition and consulting work.

**Credibility:** MEDIUM. The breadth is documented through multiple independent sources, but whether this was a deliberate strategic choice or organic evolution is unknown.

---

## Decision 6: Presenting Virtualization Research at Grehack 2023 (with Corentin Bayet)

**Context:** Corentin Bayet is a senior Synacktiv researcher who previously co-authored "Speedpwning VMware Workstation" (Ekoparty 2020) and has deep virtualization exploitation experience. In 2024, Bayet competed at Pwn2Own Vancouver under the team name "REverse Tactics" (with Bruno Pujos) targeting VirtualBox.

**Choice made:** Bouzerar co-presented "Virtualization from an attacker point of view" with Corentin Bayet at Grehack 2023 (November 2023).

**Reasoning (inferred):**
- This talk appears to be a more systematic/educational treatment of virtualization attack surfaces -- the "from an attacker point of view" framing suggests methodology presentation, not just exploit details.
- Co-presenting with Bayet (an established virtualization researcher) provides mentorship visibility and positions Bouzerar within the virtualization research community.
- The timing (November 2023, after Pwn2Own Vancouver in March 2023) suggests this is a knowledge consolidation and dissemination phase after the competition work.

**Outcome:** Conference presentation (slides + video available). Established public profile in virtualization security research.

**Credibility:** HIGH for the facts. MEDIUM for the strategic reasoning.

---

## Decision 7: Converting Competition Research into Conference Talks

**Context:** After Pwn2Own Vancouver 2023, Bouzerar had at least two talks about related topics within the same year.

**Choice made:** Converted Pwn2Own research into:
1. Hexacon 2023 (October): "Breaking out of the box" with Thomas Imbert -- likely detailing the VirtualBox escape chain
2. Grehack 2023 (November): "Virtualization from an attacker point of view" with Corentin Bayet -- broader methodology

**Reasoning (inferred):**
- This is a well-established pattern in the security research community: competition exploits become conference talks after patches are deployed.
- Presenting at two different conferences with two different angles (exploit-focused vs. methodology-focused) maximizes reach and demonstrates both technical depth and pedagogical ability.
- It builds personal reputation within the security community.

**Outcome:** Dual conference presence in fall 2023. Established as a recognized virtualization security researcher.

**Credibility:** HIGH. The timing and topics make the Pwn2Own-to-conference pipeline clear.

---

## Decision 8: Pursuing Responsible Disclosure via Competition

**Context:** Bouzerar's VirtualBox bugs were submitted through Pwn2Own (a coordinated disclosure competition managed by ZDI). One bug in the chain was already "previously known" (a collision).

**Choice made:** Submitted bugs through Pwn2Own rather than:
- Independent disclosure to Oracle
- Selling on the vulnerability market
- Publishing as 0-day research

**Reasoning (inferred):**
- Pwn2Own offers financial reward ($80,000 for his entry) plus professional recognition (Master of Pwn points).
- Synacktiv as an organization has a strong Pwn2Own participation history, making competition submission the natural institutional path.
- The collision issue (one bug already known) demonstrates a risk inherent in competition submission: other researchers may independently discover the same vulnerabilities, reducing payout and recognition.

**Outcome:** $80,000 earned (shared), Master of Pwn points for Synacktiv's overall ranking, but partial collision reduced novelty credit.

**Credibility:** HIGH for the facts. The choice of Pwn2Own as disclosure mechanism is definitively documented through ZDI results.

---

## Decision 9: Expanding to Embedded/IoT Security (Organizational Context)

**Context:** In 2024, Synacktiv participated in Pwn2Own Ireland (smart home devices) targeting the Philips Hue Bridge via Zigbee. The resulting article "Make it Blink" was authored by Mehdi Talbi and Matthieu Breuil. Synacktiv also entered Pwn2Own Automotive 2026 targeting EV chargers.

**Choice made (contextual):** While Bouzerar is not confirmed as a participant in these specific entries, his organization expanded into IoT/smart home targets alongside its virtualization work.

**Reasoning (team-level inference):**
- Synacktiv's strategy appears to be portfolio diversification across Pwn2Own categories (Tesla/automotive, virtualization, Linux/macOS, IoT/smart home) to maximize Master of Pwn points.
- Individual researchers specialize in specific domains while the team covers maximum breadth.

**Credibility:** LOW for any Bouzerar-specific decisions here. This is organizational context only.

---

## Decision 10: Windows Named Pipes Research Direction (2025)

**Context:** By 2025, Bouzerar presented "Hooking Windows Named Pipes" at Sthack 2025.

**Choice made:** Shifted or expanded research focus to include Windows IPC mechanisms (named pipes), which are relevant for both local privilege escalation and inter-process security.

**Reasoning (inferred):**
- Named pipes are a critical IPC mechanism in Windows that intersects with privilege boundaries.
- Understanding named pipe security is relevant for: (a) local privilege escalation in VM escape chains, (b) attacking services that communicate over named pipes, and (c) developing tools for security assessment.
- This could represent preparation for future Pwn2Own entries in Windows-related categories or ongoing client engagement work.

**Outcome:** Sthack 2025 conference presentation. Synacktiv subsequently published a related blog post "Hooking Windows Named Pipes" (April 2026) by Thomas Borot (note: different author name on the blog post, possibly different scoping of the topic or a name variation).

**Credibility:** MEDIUM. The presentation is documented, but whether this is a strategic pivot or routine diversification is unclear.

---

## Patterns in Decision-Making Style

### 1. Collaborative Over Solo
- Every major output has a co-author/co-presenter: Imbert (VirtualBox escape + Hexacon), Bayet (Grehack), Bertoli (THCON).
- This suggests he values collaboration and/or that the problems he tackles require team effort.
- **Pattern: Collaborative, builds on team strengths.**

### 2. Systematic/Methodological Approach
- The Grehack 2023 title ("from an attacker point of view") suggests a structured methodology for evaluating attack surfaces rather than ad-hoc bug hunting.
- The multi-conference presentation approach (exploit talk + methodology talk) shows deliberate knowledge organization.
- **Pattern: Analytical, framework-oriented.**

### 3. Leveraging Institutional Knowledge
- Collaboration with Corentin Bayet (VMware expert) and working within Synacktiv's established virtualization research practice.
- His VirtualBox target at Pwn2Own fits within Synacktiv's broader virtualization coverage.
- **Pattern: Builds on existing institutional foundations rather than starting from scratch.**

### 4. High-Complexity Targets
- A 3-bug chain VM escape is among the most technically demanding achievements in security competitions.
- Virtualization escape requires understanding hardware emulation, memory management, and multi-layer security boundaries.
- **Pattern: Gravitates toward technically challenging, high-reward problems.**

### 5. Research-to-Publication Pipeline
- Competition (March 2023) -> Conference talks (October/November 2023) -> continued research (2025).
- Each research investment produces multiple outputs (competition entry, conference talks, advisory).
- **Pattern: Maximizes return on research investment through multiple publication channels.**

### 6. Calculated Risk-Taking
- The collision at Pwn2Own 2023 (one previously known bug) is an inherent risk in competitive vulnerability research.
- Choosing VirtualBox (open source, analyzable) over closed-source VMware shows pragmatic target selection.
- **Pattern: Bold in target ambition but pragmatic in choosing targets that are analyzable within time constraints.**

---

## Timeline Reconstruction

| Date | Event | Decision Point |
|------|-------|---------------|
| ~2022 or earlier | Joined Synacktiv | Career choice: French offensive security firm |
| Dec 2022 | Raft game RCE advisory | Early public vulnerability disclosure |
| Mar 2023 | Pwn2Own Vancouver: VirtualBox 3-bug chain (with Imbert) | Target selection: virtualization category |
| Oct 2023 | Hexacon: "Breaking out of the box" (with Imbert) | Knowledge dissemination of VirtualBox research |
| Nov 2023 | Grehack: "Virtualization from attacker POV" (with Bayet) | Methodology-focused knowledge sharing |
| 2023 | THCON: Windows auth over HTTP (with Bertoli) | Research diversification into Windows internals |
| 2025 | Sthack: "Hooking Windows Named Pipes" | Continued Windows IPC research |

---

## What Is NOT Publicly Known

The following decisions lack public documentation:

1. **Why virtualization specifically?** No interview or blog post explains his personal motivation for choosing this field over web security, mobile, or other domains.
2. **Educational/career background.** No public bio describes his education, prior roles, or path into security research.
3. **The "music" connection.** His name "Bouzerar" and possible earlier interests remain unconfirmed in the security context.
4. **Internal Synacktiv team dynamics.** How targets are assigned or chosen within the firm's Pwn2Own preparation is not publicly documented.
5. **Regrets or trade-offs.** No public statement about research choices he would change, bug collision frustrations, or targets abandoned.
6. **Solo vs team preference reasoning.** Whether collaboration is a personal preference or an organizational requirement is unclear.
7. **Future research direction.** Whether he will continue in virtualization, pivot to another domain, or pursue a different career path.
8. **Why not compete independently?** In 2024, his Grehack co-presenter Corentin Bayet competed at Pwn2Own under "REverse Tactics" (not Synacktiv). Whether Bouzerar considered similar independence is unknown.

---

## Credibility Summary

| Decision | Credibility Level | Basis |
|----------|------------------|-------|
| Virtualization specialization | MEDIUM-HIGH | Multiple conference talks + Pwn2Own entry confirm focus |
| Working at Synacktiv | CONFIRMED fact, reasoning INFERRED | Advisory and presentations all credited through Synacktiv |
| VirtualBox at Pwn2Own 2023 | HIGH | ZDI official results |
| Pairing with Imbert | HIGH | ZDI results + Hexacon co-presentation |
| Research diversification | MEDIUM | Multiple independent sources confirm breadth |
| Grehack with Bayet | HIGH | Synacktiv resources page confirms |
| Competition-to-conference pipeline | HIGH | Timeline is unambiguous |
| Pwn2Own disclosure choice | HIGH | Demonstrated through competition participation |
| Windows internals expansion | MEDIUM | Conference presentations confirm, reasoning inferred |
| Collaborative style | HIGH | Pattern confirmed across all known outputs |

---

## Source Details

- ZDI Blog, "Pwn2Own Vancouver 2023 - Day Two Results" (March 23, 2023): Confirms Thomas Bouzerar and Thomas Imbert from Synacktiv demonstrated 3-bug chain against Oracle VirtualBox with Host EoP, earning $80,000 and 8 Master of Pwn points (one bug collision).
- Synacktiv Resources page: Lists 4 presentations by Bouzerar (Hexacon 2023, Grehack 2023, THCON 2023, Sthack 2025).
- Synacktiv Advisories: One advisory credited to Bouzerar (Raft RCE, December 2022).
- ZDI Blog, "Pwn2Own Vancouver 2024 Day One Results": Synacktiv targeted Tesla ECU (no individual names for this entry; Corentin Bayet competed separately under "REverse Tactics" with Bruno Pujos targeting VirtualBox).
- Synacktiv publications: "Make it Blink" (Pwn2Own Ireland Hue Bridge) authored by Talbi/Breuil (not Bouzerar).
- Synacktiv publications: "Old Bug, Shallow Bug" (Pwn2Own 2023 Ubuntu) authored by Tanguy Dubroca (not Bouzerar).
