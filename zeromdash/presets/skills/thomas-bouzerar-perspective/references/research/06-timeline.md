# Thomas Bouzerar - Career Timeline

**Alias/Handle:** @MajorTomSec (Twitter/X), MajorTomSec (GitHub)
**Current Role:** Security Expert, Reverse Engineering Team, Synacktiv
**Location:** France
**Focus Areas:** Hypervisor/virtualization exploitation (VMware, VirtualBox), embedded systems, game hacking, IoT

---

## Chronological Timeline

| Date | Event | Source | Notes | Credibility |
|------|-------|--------|-------|-------------|
| 2015-06-27 | First GitHub repo: VitaMailWriter (PSVita email app file write exploit) | github.com/MajorTomSec | Exploits email app vulnerability to write files to PSVita memory card. 16 stars. | Confirmed (GitHub) |
| 2015-09-24 | Published fixreg_vita (PSVita registry repair tool) | github.com/MajorTomSec | Part of PSVita homebrew/hacking scene. 11 stars. | Confirmed (GitHub) |
| 2016-08-18 | Published VitaCID (PSVita console ID retrieval tool) | github.com/MajorTomSec | Gets console identification info. 22 stars. | Confirmed (GitHub) |
| 2016-08-19 | Published VitaRW (PSVita read-write partition access tool) | github.com/MajorTomSec | Enables RW access to read-only partitions (vs0, os0). Most popular repo, 50 stars. Labeled "Don't use it." | Confirmed (GitHub) |
| 2018-04-19 | Published CCTFd (CTFd platform plugin) | github.com/MajorTomSec | Plugin for open-source CTF hosting platform. Indicates active CTF participation/organization. | Confirmed (GitHub) |
| 2018-08-11 | Created PyConFR 2018 CTF challenges repo | github.com/MajorTomSec/pycon_2018 | "Challenges du CTF de la PyconFR 2018" - authored CTF challenges for French Python conference. | Confirmed (GitHub) |
| 2018-10-22 | Published UPG_Tools (Philips TV firmware manipulation) | github.com/MajorTomSec | Tools for manipulating Philips TV firmware UPG files. 7 stars. Updated as recently as 2026-04-14. | Confirmed (GitHub) |
| 2019-03-13 | Published WaREhawkPS3 (Warhawk PS3 dedicated server) | github.com/MajorTomSec | Dedicated LAN server for Warhawk PS3 game. Python. 2 stars. | Confirmed (GitHub) |
| 2019-04-06 | Published connector_linux (server discovery tool) | github.com/MajorTomSec | Linux connector for server discovery. C++. | Confirmed (GitHub) |
| 2019-10-22 | Created personal blog (majortomsec.github.io) | github.com/MajorTomSec | "Major_Tom's blog" - used HTML5 UP Strata template. Never populated with real content (remained template). | Confirmed (GitHub) |
| 2020-05-29 | Participated in Pwn2Win CTF 2020 | github.com/MajorTomSec/2020submissions | Flag submissions repo for international CTF competition. | Confirmed (GitHub) |
| 2021-01 | Contributed to HybridDriver (VR project) | GitHub commits (MajorTomSec in melvieren/HybridDriver) | Commits related to body tracking, Kinect, SHM. VR/OpenVR driver work. | Confirmed (GitHub commits API) |
| ~2021-2022 | Joined Synacktiv (estimated) | synacktiv.com/en/our-team/reverse | Listed as "Security Expert" in Reverse Engineering team. First Synacktiv advisory is Dec 2022, suggesting joining around 2021-2022. | Inferred (first advisory date + team listing) |
| 2022-12-13 | First Synacktiv advisory: "Raft Remote Code Execution" | synacktiv.com/en/advisories | RCE vulnerability in Raft survival game. Solo author. No CVE assigned. | Confirmed (Synacktiv advisories) |
| 2023-03-23 | **TURNING POINT: Pwn2Own Vancouver 2023 - VirtualBox escape** | zerodayinitiative.com (Day Two results) | With Thomas Imbert (@masthoon): 3-bug chain exploiting Oracle VirtualBox with Host Elevation of Privilege. $80,000 + 8 Master of Pwn points. One bug was previously disclosed (collision). First Pwn2Own appearance. | Confirmed (ZDI blog) |
| 2023-03 | Synacktiv wins Master of Pwn at Pwn2Own Vancouver 2023 | zerodayinitiative.com | Team total: $530,000+ across 5 successful attempts (Tesla Gateway, macOS, VirtualBox, Tesla Infotainment, Ubuntu). Bouzerar contributed the VirtualBox category. | Confirmed (ZDI blog, multiple day results) |
| 2024-01-24 | Pwn2Own Automotive 2024 (Tokyo) - Synacktiv team | zerodayinitiative.com (Day One results) | Synacktiv earned $356,000+ on Day One alone (Tesla Modem, Ubiquiti, ChargePoint, Autel, JuiceBox). Thomas Bouzerar not individually named in results. | Confirmed team, Individual participation uncertain |
| 2024-03-20 | Pwn2Own Vancouver 2024 - Synacktiv Tesla ECU | zerodayinitiative.com (Day One results) | Synacktiv exploited Tesla ECU with integer overflow for Vehicle CAN BUS Control. $200,000 + Tesla Model 3 (team's second). Bouzerar not individually named. | Confirmed team, Individual participation uncertain |
| 2025-05-17 | **KEY ACHIEVEMENT: Pwn2Own Berlin 2025 - VMware Workstation escape** | zerodayinitiative.com (Day Three results) | With Etienne Helluy-Lafont: exploited VMware Workstation using heap-based buffer overflow (PVSCSI). $80,000 + 8 Master of Pwn points. Exploit worked on first attempt despite Windows 11 LFH mitigations. | Confirmed (ZDI blog + Synacktiv blog + ZDI advisory) |
| 2025-05-17 | CVE-2025-41238 assigned (VMware Workstation PVSCSI heap-overflow) | ZDI-26-190 (published 2026-03-16) | CVSS 8.2. Credited to "Thomas Bouzerar (@MajorSec) from @Synacktiv, Etienne Helluy-Lafont from @Synacktiv". Heap-overflow in PVSCSI controller when guest transmits >1024 scatter-gather segments. | Confirmed (ZDI advisory) |
| 2026-01-22 | Pwn2Own Automotive 2026 - Synacktiv (Autel charger) | zerodayinitiative.com (Day Two results) | Synacktiv exploited Autel MaxiCharger AC Elite Home 40A with stack-based buffer overflow via charging connector protocol/signal manipulation. $30,000 + 5 points. Bouzerar not individually named. | Confirmed team, Individual participation uncertain |
| 2026-01-23 | Published: "On the clock: Escaping VMware Workstation at Pwn2Own Berlin 2025" | synacktiv.com/en/publications | Co-authored with Etienne Helluy-Lafont. Deep technical writeup of CVE-2025-41238 exploitation including LFH randomization defeat via side-channel, heap layout shaping, shader spray, URB corruption. | Confirmed (Synacktiv blog) |
| 2026-03-16 | ZDI-26-190 advisory published | zerodayinitiative.com/advisories/ZDI-26-190/ | Official public disclosure of VMware Workstation PVSCSI vulnerability. | Confirmed (ZDI) |
| 2026-04-14 | UPG_Tools GitHub repo updated | github.com/MajorTomSec/UPG_Tools | Philips TV firmware tools still maintained. Suggests ongoing embedded/IoT interest. | Confirmed (GitHub) |

---

## Career Phase Analysis

### Phase 1: Console Hacking and Hobbyist (2015-2019)
- PSVita scene: Published 4 tools (VitaMailWriter, fixreg_vita, VitaCID, VitaRW)
- Embedded/firmware: Philips TV firmware tools (UPG_Tools)
- CTF: Organized PyConFR 2018 CTF, participated in Pwn2Win 2020
- Gaming: PS3 server reimplementation (WaREhawkPS3)
- **Evolution**: Self-taught/hobbyist researcher developing low-level skills on consumer hardware

### Phase 2: Professional Security Research at Synacktiv (2022-present)
- Joined Synacktiv's Reverse Engineering team (~2021-2022)
- First advisory: game exploitation (Raft RCE, Dec 2022) - transition from hobbyist to professional
- **TURNING POINT (2023)**: VirtualBox escape at Pwn2Own Vancouver 2023 - hypervisor exploitation debut
- **SPECIALIZATION (2025)**: VMware Workstation escape at Pwn2Own Berlin 2025 - established hypervisor expert

---

## Key Collaborators

| Name | Handle | Collaboration |
|------|--------|---------------|
| Thomas Imbert | @masthoon | VirtualBox escape, Pwn2Own Vancouver 2023 |
| Etienne Helluy-Lafont | - | VMware Workstation escape, Pwn2Own Berlin 2025 |
| David Berard | @_p0ly_ | Synacktiv Reverse team lead, Tesla research |
| Vincent Dehors | @vdehors | Synacktiv Tesla team |
| Tanguy Dubroca | @SidewayRE | Synacktiv Ubuntu team (Pwn2Own 2023) |

---

## Known CVEs

| CVE | Product | Year | Type | Co-credited |
|-----|---------|------|------|-------------|
| CVE-2025-41238 | VMware Workstation (PVSCSI) | 2025 | Heap-based buffer overflow | Etienne Helluy-Lafont |
| (VirtualBox bugs from Pwn2Own 2023) | Oracle VirtualBox | 2023 | 3-bug chain (partially collided) | Thomas Imbert |
| (Raft RCE - no CVE assigned) | Raft Survival Game | 2022 | Remote Code Execution | Solo |

---

## Technical Expertise Progression

1. **2015-2019**: Firmware reverse engineering, memory manipulation (PSVita kernel), embedded device hacking (Philips TV)
2. **2022**: Game exploitation (Raft RCE)
3. **2023**: Virtualization exploitation debut (VirtualBox 3-bug chain escape with host EoP)
4. **2025**: Advanced hypervisor exploitation (VMware Workstation PVSCSI heap overflow, defeating Windows 11 LFH mitigations, side-channel attacks on heap randomization)

---

## Pwn2Own Summary

| Year | Event | Category | Target | Result | Individual? | Prize |
|------|-------|----------|--------|--------|-------------|-------|
| 2023 | Vancouver | Virtualization | Oracle VirtualBox (Host EoP) | SUCCESS (collision on 1 bug) | Yes (with T. Imbert) | $80,000 |
| 2025 | Berlin | Virtualization | VMware Workstation | SUCCESS | Yes (with E. Helluy-Lafont) | $80,000 |

Note: Synacktiv team broadly participates in many categories (Tesla, EV chargers, NAS, smart home, etc.) but Thomas Bouzerar appears to specialize in the virtualization/hypervisor category.

---

## Most Recent 12 Months (May 2025 - May 2026)

| Date | Activity | Status |
|------|----------|--------|
| 2025-05-17 | Pwn2Own Berlin 2025: VMware Workstation escape (Day Three) | Confirmed |
| 2025 (H2) | Pwn2Own Ireland 2025: Not individually named in any attempt | No evidence of individual participation |
| 2026-01-22 | Pwn2Own Automotive 2026: Synacktiv team active, Bouzerar not individually named | Uncertain |
| 2026-01-23 | Published VMware Workstation exploit writeup on Synacktiv blog | Confirmed |
| 2026-03-16 | ZDI-26-190 published (CVE-2025-41238 disclosure) | Confirmed |
| 2026-04-14 | UPG_Tools (Philips TV firmware) repo updated on GitHub | Confirmed |
| 2026 (ongoing) | Likely preparing for Pwn2Own Berlin 2026 (announced March 2026) | Inferred |

---

## Education Background

- Not publicly documented
- Based on timeline: Active in French security community (PyConFR 2018 CTF), based in France
- CTF background suggests CS/engineering education in France (grandes ecoles or university)
- Joined Synacktiv likely as junior researcher around 2021-2022 given the advisory timeline

---

## Open Questions / Gaps

1. **Education**: No public information about university or degree
2. **VirtualBox Pwn2Own 2023 writeup**: No public blog post found detailing the 3-bug chain
3. **Conference talks**: No confirmed public conference presentations found (HITB, Hexacon, SSTIC, OffensiveCon)
4. **Exact Synacktiv join date**: Estimated 2021-2022 based on first advisory (Dec 2022)
5. **Pwn2Own Automotive participation**: Whether he personally participated in 2024/2026 EV charger attempts
6. **VirtualBox CVEs**: The specific CVE numbers from Pwn2Own Vancouver 2023 VirtualBox escape not found

---

## Source Index

| Source | URL | Last Accessed |
|--------|-----|---------------|
| GitHub Profile | https://github.com/MajorTomSec | 2026-05-09 |
| Synacktiv Team Page | https://www.synacktiv.com/en/our-team/reverse | 2026-05-09 |
| Synacktiv Advisories | https://www.synacktiv.com/en/advisories | 2026-05-09 |
| Synacktiv Blog (VMware) | https://www.synacktiv.com/en/publications/on-the-clock-escaping-vmware-workstation-at-pwn2own-berlin-2025.html | 2026-05-09 |
| ZDI Advisory ZDI-26-190 | https://www.zerodayinitiative.com/advisories/ZDI-26-190/ | 2026-05-09 |
| ZDI Blog (Pwn2Own Vancouver 2023 Day Two) | https://www.zerodayinitiative.com/blog/2023/3/23/pwn2own-vancouver-2023-day-two-results | 2026-05-09 |
| ZDI Blog (Pwn2Own Berlin 2025 Day Three) | https://www.zerodayinitiative.com/blog/2025/5/17/pwn2own-berlin-2025-day-three-results | 2026-05-09 |
| ZDI Blog (Pwn2Own Vancouver 2024 Day One) | https://www.zerodayinitiative.com/blog/2024/3/20/pwn2own-vancouver-2024-day-one-results | 2026-05-09 |
| Synacktiv Raft RCE PDF | https://www.synacktiv.com/sites/default/files/2022-12/Raft_RCE.pdf | 2026-05-09 |
