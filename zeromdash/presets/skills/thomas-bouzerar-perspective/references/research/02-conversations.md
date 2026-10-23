# Thomas Bouzerar - Conversations, Talks, and Interviews

## Research Summary

Thomas Bouzerar is a security researcher at Synacktiv specializing in reverse engineering, virtualization exploitation (VirtualBox, QEMU, VMware), embedded devices (PlayStation Vita, Philips TV), and iOS security. He has a confirmed Pwn2Own victory at Vancouver 2023 (VirtualBox VM escape with Windows LPE, with Thomas Imbert). His Twitter/X handle is @MajorTomSec and his GitHub is github.com/MajorTomSec.

**Key finding:** Thomas Bouzerar has a relatively small public conversation footprint compared to many prominent security researchers. He has given exactly two confirmed conference presentations (both in 2023), has no known podcast appearances, and no published interviews. His communication style must be inferred primarily from his presentation topics and brief bio statements.

---

## Confirmed Conference Presentations

### 1. "Breaking Out of the Box: Technical analysis of VirtualBox VM escape with Windows LPE"

- **Event:** Hexacon 2023 (Paris, France, October 2023)
- **Co-speaker:** Thomas Imbert (@masthoon)
- **Slides PDF:** https://www.synacktiv.com/sites/default/files/2023-10/hexacon_breaking_out_of_the_box.pdf
- **Video:** No public recording found (Hexacon does not always publish all talk videos)
- **Credibility:** PRIMARY (confirmed via Hexacon 2023 program at 2023.hexacon.fr and Synacktiv resources page)

**Abstract (from conference program):**
The speakers presented a three-bug chain exploited at Pwn2Own Vancouver 2023 targeting VirtualBox and Windows 11. Their attack escaped a virtual machine and gained administrator privileges on the host. The presentation covered methodology for finding bugs from within a guest machine, approaching hypervisor architecture from an attacker's perspective, and exploiting logical vulnerabilities in the Windows kernel for privilege escalation.

**Key insights about thinking process:**
- The talk demonstrates a *chain-building* methodology: finding individual bugs and composing them into a full exploitation path (guest-to-host escape + host privilege escalation)
- Approach is described as working "from within a guest machine" -- starting from the attacker's constrained position rather than the defender's full-system view
- Covers both hypervisor-level bugs (VirtualBox escape) AND OS-level bugs (Windows kernel LPE), suggesting breadth across target layers
- Collaboration model: co-presented with Thomas Imbert (Windows kernel specialist, ex-Microsoft), suggesting division of labor by expertise domain

**Speaker Bio (from Hexacon 2023):**
"Thomas Bouzerar is a security researcher and member of Synacktiv's Reverse Engineering team, specializing in iOS and embedded devices, with prior experience in PlayStation console hacking scene."

---

### 2. "Virtualization from an attacker point of view"

- **Event:** Grehack 2023 (Grenoble, France, November 2023)
- **Co-speaker:** Corentin Bayet
- **Slides PDF:** https://www.synacktiv.com/sites/default/files/2023-11/virtu_attacker_pov_grehack2023.pdf
- **Video:** https://www.youtube.com/live/6KddjKKKEL4?si=f18bh8wJ8hAqqUtn&t=5651
- **Credibility:** PRIMARY (confirmed via Synacktiv resources page, PDF metadata shows Author: "corentin;thomas", creation date: 2023-10-06)

**Content (inferred from PDF references found):**
The presentation references the following resources, revealing its scope:
- Virtualization internals (Saferwall blog)
- VMware paravirtualization architecture
- "Matryoshka Trap" (QEMU exploitation paper by qiuhao.org)
- "Hypervisor Vulnerability Research 2020" (alisa.sh slides)
- "Speedpwning VMware Workstation" (Synacktiv's 2020 work by Bruno Pujos and Corentin Bayet)
- "Awesome Hyper-V Exploitation" (GitHub resource)
- ESXi heap overflow CVE-2021-21974
- Google Project Zero "An EPYC Escape: Case Study of KVM" (2021)

**Key insights about thinking process:**
- The title "from an attacker point of view" signals a deliberate methodological framing: examining virtualization not as an architecture to defend but as a target to compromise
- Co-presented with Corentin Bayet (now CTO of REverse Tactics, 7+ years in vulnerability research on low-level systems, VMware specialist since Ekoparty 2020)
- This appears to be more of a survey/educational talk (covering multiple hypervisors: VMware, QEMU, KVM, Hyper-V) rather than a single-exploit deep-dive
- Presented at Grehack (French regional conference, less specialized than Hexacon), suggesting this was a broader-audience version of their virtualization expertise

**Relationship to Hexacon talk:**
The Grehack talk (November 2023) provides the *conceptual framework* (how to think about attacking hypervisors), while the Hexacon talk (October 2023) provides the *specific case study* (their VirtualBox chain). Presented in reverse chronological order -- the specific before the general -- suggesting they developed understanding through practice first, then abstracted it.

---

## Pwn2Own Competition Results (Direct Evidence of Live Work)

### Pwn2Own Vancouver 2023 - Day Two

- **Target:** Oracle VirtualBox (with Host EoP to Windows 11)
- **Team:** Thomas Bouzerar and Thomas Imbert (Synacktiv)
- **Achievement:** "demonstrated a 3-bug chain against Oracle VirtualBox with a Host EoP"
- **Reward:** $80,000 and 8 Master of Pwn points
- **Source:** https://www.zerodayinitiative.com/blog/2023/3/23/pwn2own-vancouver-2023-day-two-results
- **Credibility:** PRIMARY (ZDI official blog, individual names credited)

**Context notes:**
- Synacktiv as a whole dominated Pwn2Own Vancouver 2023, with multiple team members exploiting different targets (Tesla Gateway via TOCTOU, macOS LPE via TOCTOU, Ubuntu via incorrect pointer scaling, Tesla Infotainment via heap overflow + OOB write)
- Thomas Bouzerar and Thomas Imbert were the *virtualization specialists* on the team, the pair assigned to the hypervisor escape category
- The 3-bug chain indicates significant complexity: likely (1) VirtualBox guest escape bug, (2) host code execution, (3) Windows kernel privilege escalation

---

## GitHub Profile (Technical Background Evidence)

- **Handle:** MajorTomSec (github.com/MajorTomSec)
- **Bio:** "I try to pwn things"
- **Blog:** majortomsec.github.io (redirects to balklanissou.me, currently offline)
- **Credibility:** PRIMARY (matches @MajorTomSec Twitter handle from Hexacon bio)

**Notable repositories (revealing pre-Synacktiv background):**
- **VitaRW** (50 stars, 2018): Enables read-write access to read-only PS Vita partitions. Demonstrates deep understanding of filesystem mounting, partition layouts, and hardware security boundaries.
- **VitaCID** (22 stars, 2016): Retrieves PS Vita ConsoleID -- hardware identification bypass.
- **VitaMailWriter** (16 stars, 2015): Exploits email application vulnerability to write arbitrary files on PS Vita memory card -- turning a mail client bug into filesystem access.
- **UPG_Tools** (7 stars, 2019): Tools for manipulating Philips TV firmware files (UPG format) -- embedded device firmware analysis.
- **fixreg_vita** (11 stars, 2015): Registry repair tool for PS Vita.
- **2020submissions** (fork, 2020): Pwn2Win CTF 2020 flag submissions -- active CTF participant.
- **pycon_2018**: CTF challenges for PyconFR 2018 -- likely a CTF organizer.
- **CCTFd** (2018): Plugin for CTFd platform -- CTF infrastructure contributor.

**Career trajectory inference:**
PlayStation Vita hacking (2015-2018) -> Philips TV firmware (2019) -> CTF scene (2018-2020) -> Synacktiv (reverse engineering team) -> Pwn2Own 2023 (VirtualBox escape). This shows a progression from consumer device hacking to professional hypervisor exploitation.

---

## Conversations NOT Found (Negative Evidence)

The following sources were searched without finding Thomas Bouzerar appearances:

1. **NoLimitSecu podcast** - No episodes featuring him (searched for "bouzerar", "synacktiv virtualbox", "pwn2own 2023")
2. **Le Comptoir Secu podcast** - No episodes found
3. **OffensiveCon 2024/2025** - Not in speaker list
4. **HITB 2024 Bangkok** - Not in speaker list
5. **SSTIC 2023/2024** - Not listed as presenter
6. **Hexacon 2025/2026** - Not in current speaker list
7. **Personal blog (balklanissou.me)** - Site offline, no cached content accessible
8. **Synacktiv blog (synacktiv.com/publications)** - No articles attributed to him found (note: Synacktiv's listing does not show author names in the index page)
9. **Written interviews** - None found
10. **Panel discussions** - None found
11. **AMAs or Q&A sessions** - None found
12. **Pwn2Own Automotive 2024** - Synacktiv participated but individual researchers not named by ZDI

---

## Analysis: Improvisational Style and Communication Patterns

### What we can infer from the available evidence:

**1. Collaborative by default:**
Both of his known talks are co-presentations. He never appears as a solo speaker in any confirmed source. This suggests either (a) preference for collaborative work, (b) his exploits are naturally multi-person due to complexity (hypervisor escape + kernel LPE requires two domains), or (c) he is earlier in his public speaking career and presents with more experienced speakers.

**2. Practice before theory:**
The chronological ordering of his 2023 talks (Hexacon October = specific exploit, Grehack November = general framework) suggests he develops concrete exploits first and then abstracts the methodology. He does not appear to be someone who publishes theoretical attack surface analyses without working exploits.

**3. Low public profile despite high achievement:**
$80,000 Pwn2Own win, Hexacon speaker, Grehack speaker -- yet no podcast appearances, no interviews, no blog posts, no Twitter threads explaining his work. This is a deliberate or personality-driven choice to let the technical work speak for itself rather than building a personal brand.

**4. PlayStation-to-hypervisor pipeline:**
His background in PS Vita hacking (2015-2018) demonstrates comfort with hardware/software boundaries, proprietary systems, and undocumented interfaces. The VitaMailWriter project (exploiting an email app to get filesystem write) shows the *lateral thinking* that translates directly to hypervisor exploitation (exploiting a peripheral device interface to escape containment).

**5. French security research ecosystem:**
Presents exclusively at French/European conferences (Hexacon, Grehack). No US conference appearances found (not at BlackHat, DEF CON, or US OffensiveCon despite having Pwn2Own-caliber work). This suggests preference for the French-language security community or that his public speaking is still relatively new (both talks are from 2023, the same year as his Pwn2Own debut).

**6. Title/framing choices:**
- "Breaking Out of the Box" -- metaphorical, playful, accessible title for a deeply technical VM escape talk
- "Virtualization from an attacker point of view" -- explicitly positions as methodology/perspective shift, not just a bug report

### How he likely handles questions (inferred):

Based on the collaborative pattern, the "I try to pwn things" minimal bio, and the absence of long-form writing:
- Likely gives concise, technically precise answers
- Probably deflects "how did you find this?" toward methodology (given the Grehack talk's framing)
- May be more comfortable with technical depth than narrative/storytelling
- The PlayStation background suggests comfort with "hobby hacker" identity -- not purely corporate/professional framing

---

## Topics He Refuses to Discuss (Inferred)

No direct evidence of refusals, but notable gaps suggest boundaries:
- No discussion of responsible disclosure timelines or vendor interactions
- No discussion of his iOS research (mentioned in bio but zero public work found)
- No discussion of current/future Synacktiv targets
- No personal blog content preserved (site offline, possibly intentionally taken down)

---

## Analogies and Explanation Style

No direct quotes available from transcripts. The talk title "Breaking Out of the Box" is the strongest evidence of his preferred metaphorical framing -- the physical containment metaphor for VM isolation. The Grehack talk's "attacker point of view" framing suggests he values *perspective shift* as an explanatory device.

---

## Source Quality Summary

| Source | Type | Credibility |
|--------|------|-------------|
| Hexacon 2023 program (2023.hexacon.fr) | Speaker bio + abstract | PRIMARY |
| ZDI Pwn2Own Vancouver 2023 Day 2 blog | Named achievement | PRIMARY |
| Synacktiv resources page (synacktiv.com/ressources) | Talk listings with URLs | PRIMARY |
| Grehack 2023 PDF metadata | Author field: "corentin;thomas" | PRIMARY |
| GitHub profile (MajorTomSec) | Repository history | PRIMARY |
| VitaRW README | Technical writing sample | PRIMARY |
| OffensiveCon 2025 - Corentin Bayet/Bruno Pujos talk | Related context | SECONDARY |
| Synacktiv Pwn2Own history (ZDI blogs) | Team context | SECONDARY |

---

## Key URLs

- Hexacon 2023 slides: https://www.synacktiv.com/sites/default/files/2023-10/hexacon_breaking_out_of_the_box.pdf
- Grehack 2023 slides: https://www.synacktiv.com/sites/default/files/2023-11/virtu_attacker_pov_grehack2023.pdf
- Grehack 2023 video: https://www.youtube.com/live/6KddjKKKEL4?si=f18bh8wJ8hAqqUtn&t=5651
- Pwn2Own results: https://www.zerodayinitiative.com/blog/2023/3/23/pwn2own-vancouver-2023-day-two-results
- GitHub: https://github.com/MajorTomSec
- Synacktiv resources: https://www.synacktiv.com/ressources

---

## Research Gaps and Follow-up Needed

1. **Grehack 2023 video content** - The YouTube livestream (6KddjKKKEL4) starting at timestamp 5651 should contain the actual talk recording with Q&A. This is the single best primary source for understanding his live explanation style and how he handles audience questions. Transcription would be extremely valuable.

2. **Hexacon 2023 recording** - Hexacon sometimes publishes talks on their YouTube channel months later. Check periodically.

3. **iOS research** - His bio mentions iOS specialization but no public work is visible. This may be under NDA or not yet published.

4. **Personal blog archive** - balklanissou.me is offline. Wayback Machine might have cached content.

5. **French-language content** - Some appearances may exist in French-language media not easily searchable.

6. **Synacktiv blog attribution** - Individual Synacktiv blog posts don't show author names in the listing; some may be authored by him.

7. **REverse Tactics connection** - Corentin Bayet (his Grehack co-speaker) has since left Synacktiv to co-found REverse Tactics with Bruno Pujos. Whether Thomas Bouzerar followed or remained at Synacktiv is unclear.
