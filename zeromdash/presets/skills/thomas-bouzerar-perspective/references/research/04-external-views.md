# Thomas Bouzerar -- External Views and Peer Perception

## Source Credibility Key

- **[PRIMARY]** = First-hand source (peers, collaborators, maintainers speaking directly)
- **[SECONDARY]** = Journalist/organizational coverage (ZDI blogs, Oracle advisories)
- **[SELF]** = What Bouzerar says about himself (for contrast)

---

## I. Competition Standing and Recognition

### ZDI / Pwn2Own Official Coverage [SECONDARY]

**Pwn2Own Vancouver 2023 -- Day Two:**
> "Thomas Imbert (@masthoon) and Thomas Bouzerar (@MajorTomSec) from Synacktiv demonstrated a 3-bug chain against Oracle VirtualBox with a Host EoP."
> -- ZDI Blog, March 23, 2023

- Result: SUCCESS/COLLISION (one bug in chain was previously known)
- Award: $80,000 + 8 Master of Pwn points
- Context: Part of Synacktiv's dominant multi-entry strategy that day ($475,000 total across all Day Two entries)

**Synacktiv's overall Pwn2Own Vancouver 2023 performance (Bouzerar's team):**
- Day One: Tesla Gateway TOCTOU ($100,000 + Tesla Model 3), macOS TOCTOU ($40,000)
- Day Two: Tesla Infotainment ($250,000), VirtualBox 3-bug chain with Bouzerar ($80,000), Ubuntu privesc ($30,000)
- Led Master of Pwn standings from Day One onward
- Won Master of Pwn title for Pwn2Own Vancouver 2023

**Pwn2Own Vancouver 2024:**
- Synacktiv led Day One with Tesla ECU integer overflow ($200,000 + Tesla Model 3, 20 MoP points)
- ZDI closing statement: "Tune in tomorrow to see if Synacktive [sic] can hold on to their Master of Pwn lead"
- This indicates Synacktiv was perceived as the team to beat

**Pwn2Own Automotive 2024:**
- Synacktiv had 5 entries on Day One alone (Tesla Modem 3-bug chain, Ubiquiti, ChargePoint, JuiceBox, Autel)
- Total Day One: ~$296,000 in prizes, 31 MoP points
- Demonstrated breadth: automotive + IoT + EV chargers

### Key Observation about Bouzerar's Role

Thomas Bouzerar's personal entry at Pwn2Own Vancouver 2023 was specifically in the **virtualization category** (Oracle VirtualBox escape with Host EoP). This positions him within Synacktiv's team as the hypervisor/virtualization specialist, while other team members handled Tesla (David Berard, Vincent Dehors), macOS (unnamed), and Linux (Tanguy Dubroca).

---

## II. Vendor Acknowledgments [SECONDARY]

### Oracle Critical Patch Update, April 2023

Credit line:
> "Thomas Bouzerar (MajorTomSec) from Synacktiv: CVE-2023-21987, CVE-2023-21988"

These CVEs affect **Oracle VM VirtualBox** (versions prior to 6.1.44, prior to 7.0.8) and were addressed in the April 2023 CPU. The timing aligns precisely with the Pwn2Own Vancouver 2023 VirtualBox 3-bug chain demonstration (March 2023 competition, April 2023 patch).

This confirms:
- Bouzerar personally discovered and reported VirtualBox vulnerabilities
- Oracle formally attributes the discoveries to him by name and handle
- The bugs were significant enough to be included in a Critical Patch Update

### curl Project

- Listed in curl's official THANKS file as a contributor
- PR #5391 merged (submitted by MajorTomSec): Fixed "theoretical integer overflow in Curl_auth_create_plain_message"
- Maintainer Daniel Stenberg response: "Thanks!" -- swift merge indicating clean, acceptable code quality
- Bouzerar himself characterized the bug as "more of a theoretical vulnerability" (integer overflow on 32-bit systems with >4GB memory)
- Separately credited via "Reported-by: Thomas Bouzerar" in commit for "url: reject too long input when parsing credentials" (May 2020)

---

## III. Peer Interactions and Community Context

### GitHub Profile [SELF]

- Handle: @MajorTomSec
- Bio: "I try to pwn things"
- Location: France
- 44 followers, 11 public repos
- Minimal self-promotion; no company listed despite Synacktiv affiliation

### Open Source Security Contributions [PRIMARY - maintainer responses]

**Gitcoin (gitcoinco/web):**
- Submitted security hotfix PR for CSRF and XSS vulnerabilities (PR #5207)
- 15 comments of discussion
- Both reviewers eventually approved the changes
- Extended timeline (Sep 2019 to Feb 2020) reflected resource constraints, not quality issues
- PR was later moved to #5926 and cherry-picked into the codebase
- Demonstrates: proactive responsible disclosure to open-source projects

### Early Career / Console Hacking Community [SELF/PRIMARY]

- VitaRW (50 stars): PS Vita read-write partition access PoC
- VitaCID (22 stars): PS Vita ConsoleID extraction tool
- VitaMailWriter (16 stars): Exploiting email app vulnerability on PS Vita
- UPG_Tools (7 stars): Philips TV firmware manipulation
- Pwn2Win CTF 2020 participant (competitive CTF background)
- PyconFR 2018 CTF participant

This early history reveals a researcher trajectory from **console hacking** (PS Vita scene, 2016-2018) through **web security** (Gitcoin bug bounties, 2019-2020) to **hypervisor exploitation** (VirtualBox at Pwn2Own, 2023+).

---

## IV. How Synacktiv Brands Itself [SECONDARY]

Synacktiv's public-facing identity:
- "State-of-the-art technical expertise and thorough understanding of today's threats"
- 3,447 completed missions, 188 regular clients, 310 publicly identified vulnerabilities, 320 publications
- Core competencies: Pentest, Reverse Engineering, Development, Incident Response
- Frequent Pwn2Own participants with Master of Pwn wins

Synacktiv does NOT prominently feature individual researcher names on their main website or publications listing page. Individual contributions are buried within articles. This contrasts with firms like Google Project Zero where individual researcher names are front-and-center.

---

## V. Comparative Analysis: Hypervisor Researchers

### Thomas Bouzerar vs. Felix Wilhelm

| Dimension | Thomas Bouzerar | Felix Wilhelm |
|-----------|----------------|---------------|
| Primary domain | VirtualBox escape | Xen, KVM, cloud security |
| Affiliation model | Offensive security firm (Synacktiv) | Research lab (P0, Asymmetric) |
| Public visibility | Low; team-first culture | Low; research-first culture |
| Publication style | Team blog posts (attribution unclear) | Individual deep-dive blog posts |
| Competition participation | Active Pwn2Own competitor | No known Pwn2Own entries |
| Vendor diversity | Oracle VirtualBox, curl | Xen, KVM, HashiCorp, Palo Alto |
| Tool building | No known public tools for hypervisor research | xenpwn, weggli (2.5k stars) |
| Career trajectory | Console hacking -> web -> hypervisor | University -> ERNW -> P0 -> Asymmetric |
| Research output volume | 2 known VirtualBox CVEs (public) | Multiple XSAs, KVM CVEs, Cloud CVEs |
| Community perception | Part of elite team | Individual elite researcher |

### Thomas Bouzerar vs. Qian Wenxiang (Keen Lab / 360)

| Dimension | Thomas Bouzerar | Qian Wenxiang |
|-----------|----------------|---------------|
| Team model | Synacktiv (French firm) | Keen Lab / 360 (Chinese teams) |
| Pwn2Own focus | VirtualBox, Tesla | VMware Workstation, multiple |
| Known VMware work | Not confirmed | Famous for VMware escapes (2017-2018) |
| Publication language | French/English | Chinese/English |
| Competition dominance | Part of multi-year Synacktiv Pwn2Own streak | Pioneer era of Chinese team dominance |

### Thomas Bouzerar vs. Bruno PUJOS / Corentin BAYET (REverse Tactics)

These researchers also competed in the VirtualBox category at Pwn2Own Vancouver 2024:
- REverse Tactics: "two Oracle VirtualBox bugs including a buffer overflow, along with a Windows UAF" ($90,000)
- Both target the same technology (VirtualBox guest-to-host escape)
- Direct competitors in the same Pwn2Own category

---

## VI. Perception Patterns

### What Others Say (Synthesized)

1. **Team player over solo star**: ZDI always names him as part of a pair ("Thomas Imbert and Thomas Bouzerar from Synacktiv") or as part of the "Synacktiv team." He is never singled out as an individual standout in the way Felix Wilhelm or Tavis Ormandy are discussed.

2. **Technically capable**: The 3-bug chain against VirtualBox with Host EoP demonstrates sophisticated multi-step exploitation capability. Oracle's formal CVE attribution confirms legitimate discovery.

3. **Breadth across Synacktiv's portfolio**: Synacktiv deploys different researchers for different targets. Bouzerar is the virtualization person; Berard/Dehors handle automotive; Dubroca handles Linux. This specialization model is how Synacktiv achieves breadth.

4. **Low individual profile**: Despite Pwn2Own success, Bouzerar has minimal public presence (44 GitHub followers, no personal blog active, no known conference keynotes or solo talks found).

5. **Practical over theoretical**: His curl contribution was self-described as fixing a "theoretical" vulnerability. His Pwn2Own work, by contrast, requires working exploits under competition pressure. This suggests he values practical exploitation over paper findings.

6. **Competition-oriented**: Unlike Felix Wilhelm (who publishes research papers and blog posts for education) or Tavis Ormandy (who is active on social media discussing security philosophy), Bouzerar's public footprint is almost entirely competition results and CVE credits.

### What He Says About Himself [SELF]

- GitHub bio: "I try to pwn things" -- deliberate understatement
- No personal blog (domain redirected away from majortomsec.github.io)
- Minimal social media presence
- Does not publicly describe his methodology or philosophy
- No known interviews or podcast appearances found

---

## VII. Criticism or Controversy

**No controversy found.** Specifically:
- No public disputes about vulnerability disclosure timelines
- No criticism of research quality
- No ethical concerns raised
- No bug collision complaints (the VirtualBox "collision" at Pwn2Own 2023 was handled gracefully with full payout)
- No community backlash about any of his disclosures

The absence of controversy is consistent with someone who:
- Works within an established team/firm with professional processes
- Does not make public claims beyond what is demonstrable
- Participates in structured competitions (Pwn2Own) with clear rules
- Does not maintain a controversial public persona

---

## VIII. Synacktiv's Reputation in the Pwn2Own Circuit

### The Synacktiv Phenomenon (2022-2024)

Synacktiv has become one of the most dominant Pwn2Own teams in history:
- **Pwn2Own Vancouver 2023**: Master of Pwn winner; multiple entries across Tesla, VirtualBox, macOS, Ubuntu
- **Pwn2Own Automotive 2024**: 5+ entries on Day One alone; Tesla Modem, multiple EV chargers
- **Pwn2Own Vancouver 2024**: Led Master of Pwn standings; Tesla ECU with CAN BUS control
- **Pwn2Own Ireland 2024**: At least 2 entries (smart home devices)
- Won at least one Tesla Model 3 at competition (possibly 2-3 total)

### How This Positions Bouzerar

Bouzerar is one of several specialized researchers within a dominant competitive team. His specific value proposition within Synacktiv appears to be:
- Hypervisor/virtualization exploitation (VirtualBox escape)
- Multi-bug chain construction capability
- Complements automotive (Berard/Dehors), Linux (Dubroca), and IoT (others) specialists

The team-first model means:
- Individual recognition is lower than at Google P0 or similar researcher-branded organizations
- However, the team's collective results provide credibility by association
- Winning Master of Pwn at Pwn2Own is among the highest competitive achievements in offensive security

---

## IX. Information Gaps

The following could not be confirmed through available public sources:
1. No solo conference talks by Thomas Bouzerar found (SSTIC, Hexacon, HITB, BlackHat, OffensiveCon all checked)
2. No published technical blog posts under his individual name found on Synacktiv's site
3. No known VMware or QEMU exploitation work confirmed (only VirtualBox)
4. No peer quotes specifically discussing his individual methodology or approach
5. His specific role evolution within Synacktiv (when he joined, his title) is not publicly documented
6. No interviews, podcasts, or media profiles found
7. The Philips Hue Bridge / Pwn2Own Ireland 2024 writeup was authored by Mehdi Talbi and Matthieu Breuil, not Bouzerar

---

## X. Summary Assessment

**External perception of Thomas Bouzerar:**
- Perceived as a competent member of an elite offensive security team
- Recognized through formal vendor credits (Oracle) and competition results (ZDI/Pwn2Own)
- Not perceived as an individual thought leader or public figure in the security research community
- His reputation is primarily derivative of Synacktiv's collective dominance
- Demonstrates the "French offensive security school" model: team over individual, competition results over publications, practical exploitation over theoretical research
- Career arc (console hacking -> web -> hypervisor) shows progression but limited public documentation of the journey

**Confidence in this assessment:** Medium. The limited public footprint means there may be significant work, talks, or peer interactions not discoverable through web searches. French-language security community discussions (which would require different search strategies) may contain additional perspectives.
