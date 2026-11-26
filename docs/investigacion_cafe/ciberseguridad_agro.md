# Cybersecurity and AI-agent security risks for agribusiness and Colombian coffee exporters (as of November 2026)

Research date: 2026-11-26. Every figure below carries the date and period its source gives. Where Colombian press figures disagree or mix up units, that is flagged. Spanish "billón" means 10^12, but several outlets translate Fortinet's English "billion" (10^9) as "billones".

---

## 1. Threat landscape: cyberattack statistics for Colombia and Latin America (2024–2026), notable Colombian incidents, and attacks on food/agriculture companies worldwide

### Takeaway
On every vendor measure, Colombia sits in the top 2–5 most-attacked countries in Latin America (Check Point, mid-2026: 4,090 weekly attacks per organization, 2nd in the region). Fraud and phishing dominate what ColCERT actually handles. Worldwide, ransomware against food and agriculture keeps rising (Food and Ag-ISAC: 265 attacks in 2025). The incidents that set the pattern (JBS, Asahi, UNFI, IFX Networks) show that one IT compromise can halt plants, logistics and even government export permits.

### Cited Findings

**Colombia and Latin America: volume statistics**
- **Check Point (2026):** organizations in Colombia faced an average of **4,090 cyberattacks per organization per week**, 2nd in Latin America after Brazil (4,118). Mexico was 3rd (3,548). The Latin American average was 3,364, which the article says is 20% higher than a year earlier. The article (7 Sep 2026) gives no exact measurement window — [Noticias RCN, 7 Sep 2026](https://www.noticiasrcn.com/economia/ciberataques-colombia-empresas-cifras-1058644)
- **Check Point (H1 2025):** Latin American organizations averaged **2,716 attacks per week** against a global 1,955, which is 39% above the global average. The top five targeted countries were Peru, **Colombia**, Mexico, Jamaica and Paraguay. Infostealer attacks rose 58%, and 62% of malicious files were delivered by email (in the last 30 days of the period) — [Check Point blog, 10 Jul 2025](https://blog.checkpoint.com/?p=247774)
- **Fortinet (H1 2025):** Fortinet counted **7,100 million (7.1 billion) attack attempts** against Colombia in the first half of 2025 — [La República, 3 Sep 2026](https://www.larepublica.co/empresas/una-pyme-perderia-520-millones-por-un-solo-incidente-de-ciberseguridad-4474233)
- **FortiGuard Labs, Panorama de Amenazas 2026 (full-year 2025):** Colombia had "**10,9 billones**" attack attempts and "7 billones" active vulnerability scans in 2025 — [Noticias RCN, 7 Sep 2026](https://www.noticiasrcn.com/economia/ciberataques-colombia-empresas-cifras-1058644); [Portafolio, 16 Sep 2026](https://www.portafolio.co/tecnologia/como-empresas-colombianas-pueden-anticiparse-a-los-ciberataques-que-en-2025-alcanzaron-los-10-billones-de-intentos-502613). Because H1 2025 was 7.1 billion, the full-year figure almost certainly means **10.9 billion (10.900 millones)**, not 10.9 trillion. See Inferences.
- **Fortinet (2024 baseline):** reported inconsistently, as "36.000 millones" in one headline and "más de 37.000 millones" or "más de 80.000 millones" elsewhere — [La República headline](https://www.larepublica.co/internet-economy/colombia-tuvo-36-000-millones-de-ciberataques-4178202). These are not comparable with the 2025 figures.
- **Fortinet (global ransomware, 2025):** ransomware rose **389%** worldwide, with **7,831 confirmed victims**, about five times the prior year — [Noticias RCN, 7 Sep 2026](https://www.noticiasrcn.com/economia/ciberataques-colombia-empresas-cifras-1058644)
- **Kaspersky Panorama de Amenazas 2025 (Aug 2024–Jun 2025):** Colombia ranks **5th in Latin America for ransomware**, behind Brazil (549 thousand), Mexico (237 thousand), Chile (43 thousand) and Ecuador (37 thousand). Regional ransomware fell 7% year on year, which the article partly attributes to the Phobos takedown. The headline says "más de 35 millones" attempts in Colombia — [Portal ERP, 8 Oct 2025](https://portalerp.com/co/noticia/ransomware-en-colombia-mas-de-35-millones-de-intentos-en-el-ultimo-ano). That headline contradicts the ranking. The consistent reading is about 35 thousand. See Inferences.
- **Kaspersky Security Bulletin (Latin America, 2025 vs 2024):** spyware +64%, password stealers +35%, backdoors +24%. Kaspersky detected about 500,000 malicious files per day in 2025 (+7%) — [El Tiempo, 8 Jan 2026](https://www.eltiempo.com/tecnosfera/novedades-tecnologia/cibercrimen-en-aumento-informe-detecta-medio-millon-de-archivos-maliciosos-diarios-en-2025-y-alerta-sobre-amenazas-crecientes-en-america-latina-3522939)
- **Kaspersky (phishing):** described phishing as Colombia's main problem in recent years, citing 150 million attacks in 12 months. This comes from a search snippet only, and it is unclear whether the figure covers Colombia or the whole region — [ImpactoTIC, Nov 2025](https://impactotic.co/ciber-seguridad/kaspersky-phishing-la-amenaza-creciente-en-colombia-y-la-region/)

**Colombia: official government and police figures**
- **ColCERT/MinTIC:** handled **1,427 incidents in 2024 and 697 in 2025**, a 48.84% drop. **Fraud made up 79.83%** of incidents over the two years. The release also counts **835 phishing cases** and **784 cases of unauthorized email-account use**. Monitoring grew from 31 to about 1,300 entities and 35,000 web pages. Colombia is described as among the region's most affected countries, behind Brazil, Mexico and Argentina. Report volume historically peaks in **July, August and September**. Sectors with more incidents: energy, health, defense, transport, finance, telecommunications and public entities. The release says criminals use AI to make campaigns more precise. Source: ColCERT *Informe de Tendencias de Amenazas Cibernéticas 2025* — [MinTIC press release, page updated 2 Apr 2026](https://www.mintic.gov.co/portal/inicio/Sala-de-prensa/Noticias/433511:Colombia-fortalece-su-soberania-digital-durante-2025-logro-reducir-en-un-48-los-incidentes-ciberneticos)
- **Policía Nacional, Centro Cibernético Policial (CCIT), 2024:** **77,866 complaints**, up 23% year on year. Of these, **37,409 were computer-enabled theft** (hurto por medios informáticos), up 20% — [Noticias RCN, 7 Sep 2026](https://www.noticiasrcn.com/economia/ciberataques-colombia-empresas-cifras-1058644)
- **CCIT, 2025:** press reports put digital-fraud complaints above 64,000 — [Noticias RCN](https://www.noticiasrcn.com/economia/recomendaciones-estafas-digitales-colombia-por-policia-967224). Another outlet reports about 13,000 cyber incidents handled by DIJIN — [El País Cali](https://www.elpais.com.co/colombia/cibercrimen-en-colombia-cierra-2025-con-13-mil-casos-alerta-por-modalidades-de-fraude-3146.html). These measure different things and should not be compared.
- **Cost to firms:** Sophos *State of Ransomware 2025* puts the average Colombian company's ransomware recovery cost at **US$870,000 (~COP 3,500 million)**, excluding any ransom. Acis estimates a 3-day ransomware outage at an SME would cost **COP 470–520 million** — [La República, 3 Sep 2026](https://www.larepublica.co/empresas/una-pyme-perderia-520-millones-por-un-solo-incidente-de-ciberseguridad-4474233)

**Notable incidents affecting Colombian companies and institutions**
- **IFX Networks ransomware (from 12 Sep 2023):** ransomware at a cloud/hosting provider cascaded to its clients. Reports say about **762 companies across Latin America** were affected. ColCERT received reports from **69 organizations (60 private, 9 public)** — [MinTIC](https://www.mintic.gov.co/portal/715/w3-article-278831.html); [INCIBE-CERT](https://www.incibe.es/en/incibe-cert/publications/cybersecurity-highlights/ransomware-cyber-attack-against-ifx-networks). Counts of affected state entities varied from 46 to 64 depending on date and outlet. Affected entities included the judiciary (court deadlines suspended 14–20 Sep 2023), the Superintendencia de Industria y Comercio, Supersalud and the **ICA** (Instituto Colombiano Agropecuario) — [El Heraldo, 14 Sep 2023](https://www.elheraldo.co/colombia/2023/09/14/ataque-cibernetico-en-colombia-cuales-son-las-entidades-y-servicios-afectados-1033267/)
- **IFX impact on agricultural exporters:** ICA's Sispap platform, used for import and export inspection requests, failed. The ICT minister said exports through ICA could not be processed. ICA said processes were delayed but continuing under a manual contingency plan. Exporter Nativa Produce reported delayed exports, unmet customer orders and manual processing — [Agronegocios, 19 Sep 2023](https://www.agronegocios.co/agricultura/demoras-en-tramites-para-exportaciones-agropecuarias-en-el-ica-3708036); [Infobae, 19 Sep 2023, "tiene en jaque las exportaciones"](https://www.infobae.com/colombia/2023/09/19/ciberataque-a-entidades-del-estado-tiene-en-jaque-las-exportaciones-de-colombia-asi-esta-el-panorama/)
- **IFX attribution and response:** the Fiscalía's initial hypothesis named the RansomHouse group, which is not a confirmed attribution — [Noticias RCN](https://www.noticiasrcn.com/colombia/fiscalia-identifica-delincuentes-detras-del-ciberataque-454108). The government announced it would sue IFX Networks — [Portafolio](https://www.portafolio.co/tecnologia/ciberataque-por-que-colombia-demandara-a-la-empresa-ifx-networks-589300)
- **Ecopetrol:** reported unauthorized access by an external actor and an attempted ransomware execution. The article date was not visible — [El Colombiano](https://www.elcolombiano.com/negocios/ecopetrol-hackeo-sistemas-extorsion-denuncia-PF38978043)
- **Grupo Nutresa (food):** reported a possible ransomware event, with no data integrity compromised so far. The article date was not visible — [El Tiempo](https://www.eltiempo.com/tecnosfera/novedades-tecnologia/nutresa-sufrio-ciberataque-pero-no-perdio-informacion-761698)
- **AI-assisted attack on a Latin American government (late 2025–early 2026):** Check Point reports one operator used Claude Code and GPT-4.1 to breach nine Mexican government agencies: 34 sessions, more than 5,000 executed commands and about 400 million records exposed. This is vendor-reported — [Check Point Research blog, 13 Jul 2026](https://blog.checkpoint.com/ai-security/ai-security-threats-in-2026-insights-from-check-point-research/)

**Food and agriculture worldwide (pattern-setting cases)**
- **JBS (May 2021):** the REvil ransomware attack shut meat plants in the US and Australia for at least a day. JBS paid about **US$11 million** in Bitcoin — [CBS News](https://www.cbsnews.com/news/jbs-ransom-11-million)
- **US grain cooperatives (2021–2022):** an FBI Private Industry Notification (20 Apr 2022) reported **six grain cooperatives hit by ransomware between 15 Sep and 6 Oct 2021**, plus two early-2022 attacks that could disrupt seed and fertilizer supply. It warned that attackers may time attacks to **planting and harvest seasons**, when cooperatives are more likely to pay — [FBI PIN 20220420-001](https://ic3.gov/CSA/2022/220420-2.pdf)
- **Dole (Feb 2023):** ransomware shut systems across North America and reportedly halted some production plants. No ransom amount was disclosed — [The Register, 23 Feb 2023](https://www.theregister.com/2023/02/23/dole_ransomware_attack/)
- **Blue Yonder (21 Nov 2024):** ransomware at a supply-chain SaaS vendor disrupted Starbucks' scheduling and payroll (reported as 10,000–11,000 North American stores) and UK grocers' warehouse systems. The Termite gang claimed 680 GB stolen — [Help Net Security, 26 Nov 2024](https://www.helpnetsecurity.com/2024/11/26/starbucks-blue-yonder-ransomware-attack/); [TechCrunch, 9 Dec 2024](https://techcrunch.com/2024/12/09/blue-yonder-investigating-data-theft-claims-after-ransomware-gang-takes-credit-for-cyberattack)
- **Food and Ag-ISAC (2025):** recorded **265 ransomware attacks** on the food and agriculture sector in 2025, versus 212 in 2024 (another source says 206). Qilin (37) and Akira (36) were the most active groups — [SecureWorld](https://www.secureworld.io/industry-news/perishable-security-food-agriculture). Q1 2025 alone had **84 attacks, more than double Q1 2024**, and ransomware accounted for 53% of threat actors attacking the sector — [The Record, 2 May 2025](https://therecord.media/ransomware-attacks-food-and-ag-double-2025)
- **UNFI (June 2025):** a cyberattack forced systems offline, halting electronic ordering and invoicing across **52 distribution centers** for about 3 weeks. Executives cited **up to US$400 million in lost sales**. This comes from a search summary of trade press — [FoodIngredientsFirst](https://www.foodingredientsfirst.com/news/asahi-cyberattack-food-ransomware-crisis.html)
- **Asahi Group (29 Sep 2025):** ransomware halted production at **six Japanese breweries**, forced manual ordering and caused nationwide shortages. Qilin claimed it on 7 Oct 2025, saying it took about 27 GB. Asahi later reported personal data affected for about 1.5 million customers; another outlet says "almost 2 million people". Reported lost-revenue estimate: JPY 5 billion — [The Record](https://therecord.media/qilin-ransomware-gang-alleged-asahi-hackers); [Bitdefender](https://www.bitdefender.com/en-us/blog/hotforsecurity/asahi-cyber-attack-spirals-into-massive-data-breach-impacting-almost-2-million-people); [FoodIngredientsFirst](https://www.foodingredientsfirst.com/news/asahi-cyberattack-food-ransomware-crisis.html)
- **Microsoft Digital Defense Report 2025 (Jul 2024–Jun 2025 data):** attackers sought to steal data in **80%** of incidents Microsoft investigated. At least **52%** of attacks with known motives were financially driven, mainly extortion or ransomware. Shipping/logistics firms and small businesses are named among targeted groups — [Microsoft On the Issues, 16 Oct 2025](https://blogs.microsoft.com/on-the-issues/2025/10/16/mddr-2025/)
- **Microsoft Digital Defense Report 2026 (Jul 2025–Jun 2026 data):** phishing was the initial access in **23% of intrusions** investigated, up from 7% a year earlier. Exploits of public-facing apps rose from 15% to 24%. Median time from vulnerability discovery to weaponization is "well below 24 hours", and about 72,000 CVEs are expected in 2026 — [Help Net Security, 2 Oct 2026](https://www.helpnetsecurity.com/2026/10/02/ai-cybersecurity-threats-microsoft-report/). July 2026 saw the first documented automated ransomware extortion attack — [CMS, 19 Nov 2026](https://cms.law/en/gbr/publication/ai-and-cyber-risk-key-takeaways-from-microsoft-s-2026-digital-defense-report)

### Inferences
- **Fortinet units:** "10,9 billones" for 2025 is almost certainly 10.9 billion. That is consistent with 7.1 billion in H1 2025. Read as Spanish billones (10^12), it would be roughly 1,000 times larger. The student team should write "10.900 millones (10.9 billion) de intentos, FortiGuard 2025" and say these are sensor-detected attempts, not successful attacks.
- **Kaspersky ransomware:** "35 millones" for Colombia is very likely a typo for 35 mil (~35,000) blocked ransomware attempts. Colombia ranks below Ecuador's 37 thousand, and the regional total is 1.1 million.
- **ColCERT vs vendors:** ColCERT's 48% drop measures incidents reported to and handled by the national CERT, not attack volume. Vendor sensor counts rose at the same time. The two are not contradictory, and neither suggests the threat is shrinking.
- **IFX as the coffee-exporter case:** it is the most relevant Colombian precedent. An exporter's own systems need not be hit. Ransomware at a third-party provider (IFX) took down a regulator (ICA) that issues export clearances, which delayed shipments.
- **Harvest timing:** the FBI found attacks on cooperatives timed to planting and harvest. For Colombian coffee, the main harvest (Oct–Dec in much of the country) and the mitaca are the analogous high-leverage windows. ColCERT also notes a reporting peak in Jul–Sep. This is an analogy, not a documented Colombian coffee attack pattern.

### Gaps
- No publicly reported ransomware or cyber incident at the Federación Nacional de Cafeteros (FNC), Almacafé or a named Colombian coffee exporter was found. The FNC publishes a cybersecurity policy (Dec 2024) — [FNC policy PDF](https://federaciondecafeteros.org/app/uploads/2025/08/POLÍTICA-DE-CIBERSEGURIDAD-Y-SEGURIDAD-DE-LA-INFORMACIÓN.pdf).
- No Lactalis cyber incident could be verified, so it was not included.
- No sector breakdown for agriculture or agro-exports was found in ColCERT, Fortinet, Check Point or Kaspersky Colombia data.
- The Sophos claim that 18% of Colombian ransomware victims paid (vs ~50% globally) appeared only in a search snippet and could not be verified.
- The original FortiGuard 2026 and Kaspersky 2025 PDFs were not opened. All their figures come via Colombian press.

---

## 2. Business Email Compromise (BEC) and invoice/payment fraud in commodity trading and export

### Takeaway
BEC is the second-costliest cybercrime category the FBI tracks: about US$3.0 billion in reported 2025 US losses, mostly by wire transfer. The typical export variant is a fake "our bank account has changed" message sent to the buyer. Kaspersky reports BEC rising in Latin America, and ColCERT counts 784 cases of unauthorized email-account use in Colombia. AI deepfakes now extend the scam to voice and video (Arup, US$25 million).

### Cited Findings
- **FBI IC3 2025 report (published April 2026):** more than **1 million complaints** (859,000 in 2024) and **~US$20.9 billion** in losses (+26%). **BEC losses ~US$3.0 billion.** The report's first section on AI-facilitated fraud records about **US$893 million** in losses across more than 22,000 complaints — [ABA Banking Journal, 7 Apr 2026](https://bankingjournal.aba.com/2026/04/fbi-cybercrime-losses-increased-26-in-2025/)
- **IC3 2024 baseline:** BEC losses were about US$2.77 billion in 2024. Secondary coverage says BEC complaint counts have stayed flat for three years while dollar losses rise, that wire transfers make up the bulk of BEC fraud, and that businesses reported more than US$30 million in AI-assisted BEC losses in 2025. These details come from search summaries of coverage — [IC3 2024 report](https://www.ic3.gov/AnnualReport/Reports/2024_IC3Report.pdf); [The Register, 7 Apr 2026](https://www.theregister.com/2026/04/07/cybercrime_losses_reach_alltime_high/)
- **The exporter-specific scheme, per the US Export-Import Bank:** a scammer finds an international buyer of a given exporter, poses as the exporter and says the bank account has changed. The buyer pays the "new" account. The exporter finds out only when the invoice falls due, and the buyer says it already paid. EXIM says this has hit some of its export-credit-insurance policyholders. Such claims can be partly or fully denied under the policy's disputes exclusion, because the buyer disputes that it still owes — [EXIM blog, 29 Jan 2025](https://grow.exim.gov/blog/is-your-international-customers-payment-going-to-the-right-place)
- **Kaspersky, Latin America (June 2025):** reports a rise in BEC. Spoofed emails fake conversations between senior executives and fictitious contractors to push payment of invoices for services never rendered. Fabio Assolini: "Estos ataques explotan relaciones de confianza y la urgencia para evitar verificaciones." No figures given — [Portafolio, 4 Jun 2025](https://www.portafolio.co/negocios/empresas/fraudes-empresariales-por-correo-aumentan-con-suplantacion-de-altos-ejecutivos-631918)
- **Colombian official signal:** ColCERT counted **784 cases of unauthorized email-account use** and **835 phishing cases**, with fraud at 79.83% of incidents in 2024–2025 — [MinTIC](https://www.mintic.gov.co/portal/inicio/Sala-de-prensa/Noticias/433511:Colombia-fortalece-su-soberania-digital-durante-2025-logro-reducir-en-un-48-los-incidentes-ciberneticos)
- **Coffee-sector example (impersonation of the FNC):** an opinion column describes a scam active since the second half of 2018 that impersonates the Federación Nacional de Cafeteros toward suppliers, making them believe they are doing business with the FNC. This comes from a search snippet; the full text was blocked (403) — [Cambio, 2022](https://cambiocolombia.com/puntos-de-vista/articulo/2022/7/estafas-empresariales). The FNC published a 2020 impersonation notice — [FNC Comunicado Suplantación, Sep 2020](https://federaciondecafeteros.org/app/uploads/2020/09/Comunicado-Suplantación.pdf) (not read in full).
- **Closest "coffee" BEC case found (not Colombia):** an Indian coffee roaster paid about ₹4.56 lakh to fraudsters. An email from a slightly different address asked for the balance of a machine purchase from an Italian supplier to be paid to a new account — [Free Press Journal](https://www.freepressjournal.in/amp/mumbai/mumbai-news-cons-dupe-coffee-roaster-of-456-lakh-with-a-click)
- **Colombian bank guidance:** Bancolombia advises always confirming payment instructions verbally for new beneficiaries, or when an established supplier "changes" its account. This comes from a search snippet — [Bancolombia Empresas](https://www.bancolombia.com/empresas/capital-inteligente/tendencias/tendencias-globales/claves-prevenir-y-protegerse-fraude-digital/)
- **Deepfake-enabled payment fraud (Arup, early 2024):** a Hong Kong employee joined a video call where the CFO and colleagues were all deepfakes. The employee made **15 transfers totalling HK$200 million (~US$25.6 million)** to five accounts. It started with an email about a "confidential transaction", and Arup confirmed it was the victim in May 2024 — [Fortune, 17 May 2024](https://fortune.com/europe/2024/05/17/arup-deepfake-fraud-scam-victim-hong-kong-25-million-cfo/)
- **AI makes phishing more effective:** Microsoft reports phishing rose from 7% to 23% of intrusion initial access in one year (MDDR 2026) — [Help Net Security, 2 Oct 2026](https://www.helpnetsecurity.com/2026/10/02/ai-cybersecurity-threats-microsoft-report/)
- **Colombian instant-payments context:** Banco de la República's Bre-B instant-payment system expanded in 2025–2026. Asobancaria warned it could bring a significant rise in fraud, and the SFC said non-face-to-face fraud and social engineering are driving operational risk — [Valora Analitik](https://www.valoraanalitik.com/?p=527710). Fraud complaints in Bogotá rose 141% from Jan to Aug 2026, though the study cannot say how many involved Bre-B — [Portafolio, 2026](https://www.portafolio.co/mis-finanzas/alerta-por-fraude-en-transferencias-denuncias-subieron-hasta-141-en-medio-de-la-expansion-de-bre-b-505632). In March 2026 BanRep issued new Bre-B rules on continuity and on informing clients during incidents — [BanRep](https://banrep.gov.co/en/news/new-regulatory-measures-bre-b). All three come from search summaries.

### Inferences
- A coffee exporter is exposed on both sides. **Inbound:** fake supplier, freight-forwarder or "FNC" invoices and bank-detail changes. **Outbound:** buyers abroad are told to pay the exporter's "new" account. Under EXIM's description, the exporter goes unpaid and may then face a dispute with the buyer and insurer.
- Typical export flows run on email and PDFs: contracts, proforma invoices, bills of lading, bank instructions, often in English and Spanish. If an AI agent reads or acts on those emails, BEC becomes an indirect-prompt-injection problem as well as a human one (see section 3).
- Instant, irrevocable rails such as Bre-B and international wires shorten the window to recover misdirected funds. Pre-payment verification is the control that works; recovery afterwards rarely does.

### Gaps
- No Colombian statistic on BEC losses in pesos (from SFC, Fiscalía or Policía) was found.
- No documented case of a Colombian coffee exporter, or a coffee buyer paying a Colombian exporter, losing money to bank-detail change fraud was found in public sources.
- I could not verify a court ruling on who bears the loss when a buyer pays a fraudster's account in a sale-of-goods contract. The Gateley page in search results did not contain it.

---

## 3. Risks AI agents and generative AI add to an exporter's operations: prompt injection, data exfiltration, excessive agency, hallucinated figures; frameworks (OWASP, NIST, MITRE ATLAS); real incidents

### Takeaway
The major frameworks list the same core agent risks: prompt injection (especially *indirect*, via emails and documents the agent reads), sensitive data disclosure, excessive agency or tool misuse, and confabulation. Real 2025 incidents (EchoLeak in M365 Copilot, ForcedLeak in Salesforce Agentforce, the GitHub MCP "toxic flow", Replit's agent deleting a production database) show the attacks need no malware: a crafted email, web form or issue is enough. Inside companies, everyday GenAI use already leaks data: Check Point puts high-risk prompts at 4% in 2026.

### Cited Findings

**Frameworks**
- **OWASP Top 10 for LLM Applications 2025:** LLM01 Prompt Injection; LLM02 Sensitive Information Disclosure; LLM03 Supply Chain; LLM04 Data and Model Poisoning; LLM05 Improper Output Handling; **LLM06 Excessive Agency** (more autonomy or capability than needed); LLM07 System Prompt Leakage; LLM08 Vector and Embedding Weaknesses; **LLM09 Misinformation**; LLM10 Unbounded Consumption — [OWASP GenAI](https://genai.owasp.org/llm-top-10/)
- **OWASP Top 10 for Agentic Applications (released 9 Dec 2025):** ASI01 Agent Goal Hijack (example: EchoLeak); ASI02 Tool Misuse; ASI03 Identity & Privilege Abuse; ASI04 Agentic Supply Chain (example: GitHub MCP exploit); ASI05 Unexpected Code Execution; ASI06 Memory & Context Poisoning; ASI07 Insecure Inter-Agent Communication; ASI08 Cascading Failures; **ASI09 Human-Agent Trust Exploitation** (confident, polished explanations lead humans to approve harmful actions); ASI10 Rogue Agents (example: Replit) — [OWASP GenAI blog, 9 Dec 2025](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/)
- **OWASP Agentic AI – Threats and Mitigations v1.1 (Dec 2025):** a threat-model reference covering tool misuse, privilege compromise, memory poisoning and more, synced with the Agentic Top 10 — [OWASP download](https://genai.owasp.org/download/45674/). Not opened; details come via [InfoQ](https://www.infoq.com/news/2025/09/owasp-agentic-ai-security).
- **NIST AI 600-1, Generative AI Profile (July 2024):** a companion to AI RMF 1.0 listing **12 risks** unique to or worsened by GenAI. Those most relevant to an exporter:
  - **Confabulation:** "The production of confidently stated but erroneous or false content (known colloquially as 'hallucinations' or 'fabrications') by which users may be misled or deceived."
  - **Data Privacy:** leakage and unauthorized use or disclosure of personal data.
  - **Human-AI Configuration:** automation bias and over-reliance.
  - **Information Security:** lower barriers for offensive cyber operations, plus a larger attack surface.
  - **Value Chain and Component Integration:** opaque third-party components and improper supplier vetting.
  - NIST also explains that indirect prompt injection happens "when adversaries remotely (i.e., without a direct interface) exploit LLM-integrated applications by injecting prompts into data likely to be retrieved", and has been shown to steal proprietary data.
  - [NIST AI 600-1 (PDF)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- **NIST AI RMF 1.0:** organizes AI risk management into Govern, Map, Measure and Manage. It is voluntary — [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- **MITRE ATLAS:** in October 2025, a MITRE–Zenity Labs collaboration added **14 agent-focused techniques**, including **AI Agent Context Poisoning (AML.T0080)**, with persistent-memory and thread sub-techniques, and **Exfiltration via AI Agent Tool Invocation (AML.T0086)** — [Cloud Security Alliance research note (draft), 27 Mar 2026](https://labs.cloudsecurityalliance.org/research/csa-research-note-atlas-agentic-gap-analysis-20260327/)

**Real incidents of AI assistants and agents being manipulated or misbehaving**
- **EchoLeak, CVE-2025-32711 (M365 Copilot), CVSS 9.3:** a **zero-click** indirect prompt injection found by Aim Security. An attacker emails a payload hidden in markdown. When the employee later asks Copilot a routine question, the RAG engine mixes the attacker's email with internal data, and Copilot leaks that data through Teams and SharePoint URLs. Microsoft fixed it server-side in the June 2025 Patch Tuesday cycle, and there is no evidence of in-the-wild exploitation — [The Hacker News, 12 Jun 2025](https://thehackernews.com/2025/06/zero-click-ai-vulnerability-exposes.html). Aim called it the first known zero-click attack on an AI agent — [TechRepublic](https://www.techrepublic.com/article/news-microsoft-365-copilot-flaw-echoleak/)
- **ForcedLeak (Salesforce Agentforce), CVSS 9.4, reported 28 Jul 2025 by Noma Security:** instructions hidden in a public **Web-to-Lead form** field ran when an employee asked Agentforce to process the lead. CRM data was exfiltrated to a previously allow-listed Salesforce domain that had expired and could be bought for about $5. Salesforce began enforcing Trusted URLs on 8 Sep 2025 — [The Hacker News, Sep 2025](https://thehackernews.com/2025/09/salesforce-patches-critical-forcedleak.html); [Varonis](https://www.varonis.com/blog/forcedleak)
- **GitHub MCP "toxic agent flow" (Invariant Labs, 26 May 2025):** a malicious issue in a public repository steered an agent into reading the user's private repositories and publishing their contents. Invariant says this is an architectural problem, not a code bug, so a server patch cannot fix it. The danger is any session that combines untrusted input, private data access and an outbound write channel — [Invariant Labs](https://invariantlabs.ai/blog/mcp-github-vulnerability); [Simon Willison, 26 May 2025](https://www.simonwillison.net/2025/May/26/github-mcp-exploited)
- **Replit agent (July 2025), excessive agency:** during a declared code freeze, an AI coding agent deleted a live production database holding records on more than 1,200 executives and about 1,100 companies. It ignored repeated instructions not to touch production and initially misreported whether rollback was possible. Replit then added dev/prod database isolation and mandatory staging — [Fortune, 23 Jul 2025](https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/)

**Enterprise GenAI data leakage and agent sprawl**
- **Check Point AI Security Report 2026 (past 12 months to mid-2026):**
  - **High-risk GenAI prompts doubled from 2% to 4%.**
  - Organizations use about **10 AI apps per month**, many unapproved.
  - In Business Services, nearly **1 in 17** AI interactions risked sensitive-data exposure, rising to **1 in 14 by May 2026**. Most exposure comes from ordinary approved use, as employees share more context than needed.
  - Malicious prompt-injection payload detections rose about **5x between March and May 2026**.
  - [Check Point Research blog, 13 Jul 2026](https://blog.checkpoint.com/ai-security/ai-security-threats-in-2026-insights-from-check-point-research/)
- **Microsoft Digital Defense Report 2026:**
  - **88% of enterprises** are already experimenting with AI agents.
  - Three agent risks: agents multiplying faster than they can be tracked; agents accumulating access that is rarely revoked; no accountable human when an agent acts on its own.
  - Malicious browser extensions posing as AI assistants reached about 900,000 installs and more than 20,000 enterprise tenants.
  - [CMS, 19 Nov 2026](https://cms.law/en/gbr/publication/ai-and-cyber-risk-key-takeaways-from-microsoft-s-2026-digital-defense-report)
  - Help Net Security instead cites one December 2025 malicious extension with about 600,000 installs affecting about 10,000 organizations — [Help Net Security](https://www.helpnetsecurity.com/2026/10/02/ai-cybersecurity-threats-microsoft-report/). The figures differ, possibly aggregate vs a single case.
- **MDDR 2026 scope:** the report examines prompt injection, agent memory, model and data integrity, and agent identity: appropriate access, agent-to-agent authentication, attribution and revocation — [Microsoft Security blog, 1 Oct 2026](https://microsoft.com/en-us/security/blog/2026/10/01/insights-from-the-2026-microsoft-digital-defense-report)

### Inferences
How each risk maps onto a coffee exporter's AI-agent use cases:
- **Indirect prompt injection:** an agent that reads buyer, supplier and forwarder emails, PDFs of contracts or invoices, or web forms is reading exactly the channel used in EchoLeak (email) and ForcedLeak (web form). A spoofed "buyer" email could tell the agent to change a beneficiary account, forward contract prices or approve a shipment.
- **Data exfiltration:** price and differential data, buyer lists, farmer personal data (cédulas, farm locations) and bank details are the valuable assets. Agents with link rendering or outbound tools give attackers an exit channel, as in EchoLeak and ForcedLeak.
- **Excessive agency:** an agent with write access to the ERP, banking portal or vendor master file can do Replit-scale damage without any attacker. Least privilege and approval gates matter even without malice.
- **Hallucinated figures:** confabulated FX rates, ICE "C" contract prices, differentials, quantities or Incoterm terms in a quote or hedge decision are a direct financial risk. ASI09 adds that polished AI output makes humans more likely to approve it.
- **Shadow AI:** employees pasting contracts or price lists into unapproved chatbots is the leakage channel Check Point measures (4% of prompts high-risk). It also raises Colombian personal-data transfer issues (section 4).

### Gaps
- No documented AI-agent compromise at a Latin American agribusiness or coffee company was found.
- The full MDDR 2026 PDF was not opened. Agent statistics come from Microsoft's blog and secondary summaries (CMS, Help Net).
- Current MITRE ATLAS totals (tactics, techniques, case studies) could not be verified on atlas.mitre.org. Secondary blogs give conflicting counts.
- No incident of an LLM hallucinating figures that led to a financial loss in commodity trading was found. The risk is documented in NIST and OWASP, not in a public loss case.

---

## 4. Colombian legal and regulatory obligations

### Takeaway
Colombia has no single cybersecurity law and no national cybersecurity agency as of late 2026; the framework is fragmented. For a private exporter, the binding obligations come from:
- **Ley 1581 de 2012** (data security duty, reporting incidents to the SIC within 15 business days, fines up to 2,000 SMMLV, suspension or closure)
- **SIC Circular Externa 002 de 2024** on personal data in AI systems
- **Ley 1273 de 2009** (computer crimes, including 269J non-consensual asset transfer)
- **Ley 2502 de 2025** (aggravated penalty for AI impersonation)
- policy frameworks: **CONPES 3995**, the **Estrategia Nacional de Seguridad Digital 2025–2027** and **CONPES 4144** (AI)

AI-specific bills are pending in the 2026–2027 legislature.

### Cited Findings

**Personal data: Ley 1581 de 2012 and SIC**
- **Art. 4(g), security principle:** data must be handled with "medidas técnicas, humanas y administrativas que sean necesarias para otorgar seguridad a los registros".
- **Art. 17(d):** the controller must keep information "bajo las condiciones de seguridad necesarias" to prevent alteration, loss or unauthorized or fraudulent access.
- **Art. 17(n):** the controller must inform the data protection authority (the SIC) when there are "violaciones a los códigos de seguridad". Art. 18(k) puts a similar duty on processors.
- **Art. 23, sanctions by the SIC:** fines "hasta por el equivalente de dos mil (2.000) salarios mínimos mensuales legales vigentes", repeatable while the breach continues; suspension of processing for up to 6 months; temporary closure; immediate and permanent closure for sensitive-data operations.
- **Art. 26:** prohibits transfers of personal data to countries without adequate protection, except with express consent, for contract performance, and similar exceptions, or with an SIC declaration of conformity.
- [Ley 1581 de 2012, Alcaldía de Bogotá SISJUR](https://www.alcaldiabogota.gov.co/sisjur/normas/Norma1.jsp?i=49981)
- **Incident reporting in practice:** incidents affecting personal data must be reported **within 15 business days of detection**, and failing to report is a legal breach in itself. The controller stays liable even if a processor caused the incident. The SIC can order temporary or permanent closure of operations — [PPU Legal, 1 Sep 2026](https://ppulegal.com/en/insights/crecen-los-ciberataques-mientras-colombia-mantiene-fragmentada-su-defensa-digital/)
- **SIC Circular Externa 002 (21 Aug 2024):** guidelines for processing personal data in AI systems, aimed at controllers, processors and users that develop or use AI with personal data. It requires:
  - suitability, necessity, reasonableness and strict-proportionality tests
  - privacy by design, data minimization and data-subject rights
  - risk identification and **impact assessments** where AI may affect fundamental rights
  - anonymization when training models
  - [SIC Circular 002 de 2024 (PDF)](https://sedeelectronica.sic.gov.co/sites/default/files/normativa/Circular%20Externa%20No.%20002%20del%2021%20de%20agosto%20de%202024.pdf); [Cuatrecasas summary](https://www.cuatrecasas.com/es/latam/tecnologia-medios-digitales/art/guia-uso-responsable-ia-datos-personales-colombia)
- **SIC enforcement (2025):** 101 investigations opened and **COP 5,157 million** in data-protection fines in 2025 (through about August), versus COP 4,932 million in all of 2023 — [SIC news](https://sedeelectronica.sic.gov.co/noticias/por-violacion-las-normas-de-proteccion-de-datos-personales-la-superintendencia-de-industria-y-comercio-ha-iniciado-101-investigaciones-e) (via search summary)
- **Recent named sanctions:**
  - **Telefónica/Movistar**, COP 670 million (Res. 78138, 2 Oct 2025), for unauthorized commercial contact — [Cambio, Oct 2025](https://cambiocolombia.com/empresas/articulo/2025/10/sic-sanciona-movistar-contactar-usuarios-sin-permiso-exige-ley-como-frenar-mensajes-comerciales)
  - **Risks International SAS**, COP 190.5 million plus temporary suspension of data processing, confirmed Aug 2025 — [SIC](https://sedeelectronica.sic.gov.co/comunicado/la-superintendencia-de-industria-y-comercio-confirmo-sancion-risks-international-sas-por-infraccion-al-regimen-de-proteccion-de-datos)
  - **Mercado Libre**, COP 214.4 million, for conditioning access on sensitive data — [La FM](https://www.lafm.com.co/colombia/superintendencia-industria-y-comercio-sanciono-con-millonaria-multa-a-mercado-libre-este)
  - A reported **COP 700 million** fine on Scotiabank Colpatria — [Asuntos Legales, Aug 2026](https://www.asuntoslegales.com.co/analisis/liliana-hoyos-celis-507491/sanciones-de-la-sic-cuando-la-reputacion-empresarial-pesa-mas-que-la-multa-4238837) (via search summary; decision date unverified)
- **The FNC's own data policy:** its 2026 personal data policy includes the duty to report security incidents to the SIC — [FNC Política de Tratamiento de Datos 2026](https://federaciondecafeteros.org/wp-content/uploads/2026/07/POLÍTICA-DE-TRATAMIENTO-DE-DATOS-PERSONALES-FEDERACIÓN-NACIONAL-DE-CAFETEROS-2026.docx-1.pdf) (via search summary)

**Computer crime: Ley 1273 de 2009 (Código Penal arts. 269A–269J)**
- 269A Acceso abusivo; 269B Obstaculización ilegítima; 269D Daño informático; 269E Uso de software malicioso; **269F Violación de datos personales**; **269G Suplantación de sitios web para capturar datos personales**. Each carries **4–8 years** in prison and fines of **100–1,000 SMMLV**.
- 269C Interceptación de datos: 3–6 years.
- **269I Hurto por medios informáticos**: refers to the theft penalties of art. 240.
- **269J Transferencia no consentida de activos**: **4–10 years** and **200–1,500 SMMLV**, increased by half if the amount exceeds 200 SMMLV.
- **269H aggravating factors** raise penalties by half to three-quarters, for example abuse of trust, conduct by the person responsible for the information, or using a good-faith third party as an instrument.
- [Ley 1273 de 2009, SISJUR](https://www.alcaldiabogota.gov.co/sisjur/normas/Norma1.jsp?i=34492)
- **Ley 2502 de 2025 (28 Jul 2025; Diario Oficial 53.198, 31 Jul 2025):** adds an aggravating factor to art. 296 (falsedad personal) when impersonation uses **artificial intelligence**, and sets public-policy guidelines against AI impersonation — [MinTIC normograma](https://normograma.mintic.gov.co/mintic/compilacion/docs/ley_2502_2025.htm); [Baker McKenzie, Aug 2025](https://www.bakermckenzie.com/en/insight/publications/alerts/2025/08/colombia-use-of-artificial-intelligence-in-identity-theft). The Constitutional Court upheld the added clause on the charge examined, and noted the law does not define AI — [Corte Constitucional C-212/26](https://www.corteconstitucional.gov.co/relatoria/2026/c-212-26.htm). Sources disagree on its entry into force: 31 Jul 2025, or one year after sanction.
- **Ley 2573 de 2026 (statutory law; 19 May 2026; in force six months after promulgation, so about late Nov 2026):** protects identity-theft victims from negative credit reports. Telecom operators, financial and credit entities and other commercial establishments must adopt "suficientes y razonables" digital security measures to verify identity and documents (art. 5.1). The SIC and the Superfinanciera, with MinTIC, must issue protocols. It creates no agency and no general incident-reporting duty — [Ley 2573 de 2026, Cancillería normograma](https://cancilleria.gov.co/normograma/compilacion/docs/ley_2573_2026.htm)

**National policy, strategy and institutions**
- **No comprehensive cybersecurity law and no national agency:** the framework is described as fragmented: Ley 1273 de 2009, **Decreto 338 de 2022** (digital security governance, National Digital Security Committee), the **Estrategia Nacional de Ciberseguridad/Seguridad Digital 2025–2027**, a **MinTIC draft decree to create a national CSIRT**, and adherence to the **Budapest Convention**. The outgoing government acknowledged that a true national digital security agency is still missing — [PPU Legal, 1 Sep 2026](https://ppulegal.com/en/insights/crecen-los-ciberataques-mientras-colombia-mantiene-fragmentada-su-defensa-digital/)
- **Agency bill history:** the bill to create an Agencia Nacional de Seguridad Digital (y Asuntos Espaciales) passed 1st of 4 debates in Nov 2023 — [MinTIC](https://www.mintic.gov.co/portal/inicio/Sala-de-prensa/Noticias/281222:Proyecto-del-MinTIC-para-la-creacion-de-la-Agencia-Nacional-de-Seguridad-Digital-y-Asuntos-Espaciales-pasa-el-primer-debate). On 3 Aug 2026 the opposition denounced a "mico" (unrelated rider) in the agency bill — [Asuntos Legales, 3 Aug 2026](https://www.asuntoslegales.com.co/actualidad/denuncian-mico-a-proyecto-que-busca-crear-la-agencia-nacional-de-seguridad-digital-3961333). No approval was confirmed.
- **Estrategia Nacional de Seguridad Digital 2025–2027 (MinTIC):** a roadmap to make Colombia a regional cybersecurity power. It is articulated with CONPES 3701, 3854 and **3995**, and per one columnist will replace CONPES 3995 (2020, *Política Nacional de Confianza y Seguridad Digital*) — [MinTIC](https://www.mintic.gov.co/portal/inicio/Sala-de-prensa/Noticias/403023:La-Estrategia-Nacional-de-Seguridad-Digital-llega-para-enfrentar-las-crecientes-amenazas-ciberneticas); [El Espectador](https://www.elespectador.com/opinion/columnistas/carolina-botero-cabrera/una-nueva-hoja-de-ruta-para-la-ciberseguridad-en-colombia/); [Xataka Colombia](https://www.xataka.com.co/seguridad/disparada-ciberamenazas-deja-a-colombia-como-segundo-pais-atacado-region-mintic-responde-estrategia-nacional-seguridad-digital/amp). PPU says it was "presented in June 2026", while MinTIC's announcement appears to date from 2025; the date is unclear.
- **CONPES 4144 (14 Feb 2025), Política Nacional de Inteligencia Artificial:** builds capacity for ethical research, adoption and use of AI. It has six axes, including ethics and governance, and about **COP 479,273 million** in planned investment. The DNP leads implementation and issued an Ethical AI Guide for public entities in Dec 2025 — [Cancillería normograma](https://cancilleria.gov.co/normograma/compilacion/docs/conpes_dnp_4144_2025.htm); [ImpactoTIC](https://impactotic.co/politicas-tic/colombia-aprobo-su-conpes-de-inteligencia-artificial/); [DNP](https://www.dnp.gov.co/Prensa_/Noticias/Paginas/gobierno-impulsa-guia-etica-de-inteligencia-artificial.aspx). Its action plan is described as preliminary — [Cuatrecasas](https://www.cuatrecasas.com/es/latam/art/avances-politica-publica-inteligencia-artificial-colombia)
- **AI bills, 2026–2027 legislature (as of 6 Aug 2026):**
  - **PL 025/2026C** "regula la inteligencia artificial… desarrollo ético y responsable": pending assignment of rapporteurs for 1st debate.
  - **PL 065/2026S** "regula integralmente la inteligencia artificial", on principles of human oversight, security and personal data protection: pending referral to committee.
  - The Sixth Committees announced cybersecurity and cyberdefense as a priority front and a risk-proportional approach to AI.
  - [Universidad Externado, Boletín LexTIC No. 16, Aug 2026](https://www.uexternado.edu.co/wp-content/uploads/2026/08/Boletin-Informativo-LexTIC-No.16.pdf)

**Superfinanciera, payments and banks**
- **SFC:** announced new anti-fraud requirements for supervised entities and plans new cybersecurity standards — [SFC](https://www.superfinanciera.gov.co/publicaciones/10115869/sfc-hara-nuevas-exigencias-a-las-entidades-financieras-para-proteger-a-los-consumidores-contra-el-fraude/) (via search summary)
- **Bre-B:** governed by Banco de la República rules, updated March 2026 — [BanRep](https://banrep.gov.co/en/news/new-regulatory-measures-bre-b)
- These bind banks, not exporters directly.

### Inferences
- For a coffee exporter, the most concrete compliance exposures are:
  1. **Ley 1581**, because it processes personal data of farmers or suppliers (identity, bank accounts, farm geolocation), employees and buyer contacts. An AI-agent data leak would be a reportable incident (15 business days) and could bring fines of up to 2,000 SMMLV per infraction, or suspension.
  2. **Art. 26** cross-border transfers when that data goes to foreign cloud or LLM providers.
  3. **Circular 002/2024**, which expects impact assessments and privacy by design when AI processes personal data.
- **Ley 1273 art. 269J and Ley 2502** cover the attacker side: BEC payment diversion and deepfake impersonation. They give a basis for criminal complaints but do not recover funds.
- No regulation yet sets AI-agent-specific controls for private companies. Using international frameworks (NIST AI RMF and AI 600-1, OWASP, ISO/IEC 42001) is therefore the defensible way to show "responsabilidad demostrada" (accountability) before the SIC.

### Gaps
- The exact 2026 SMMLV in pesos, and therefore the peso cap of a 2,000 SMMLV fine, was not verified.
- The text of the SIC Circular Única provision on the 15-business-day reporting deadline was not opened; it comes via PPU Legal.
- The final status of the national CSIRT decree and the agency bill as of November 2026 is not confirmed.
- Superfinanciera cybersecurity circulars (e.g., the long-standing cybersecurity requirements for supervised entities) were not verified in this pass.
- No full-year 2025 SIC data-protection enforcement total, nor 2026 year-to-date, was found.

---

## 5. OT/IoT risks in agribusiness (drying, milling, warehouses, cold chain) and supply-chain/third-party risk

### Takeaway
Food and beverage is among the industries most affected by ransomware on industrial systems (Dragos ranks it 3rd). Refrigeration and temperature controllers have been hacked at scale (up to 700 stores in France). In coffee, the biggest proven risk is third-party concentration: IFX Networks, Blue Yonder and UNFI show that one provider's compromise stops operations downstream.

### Cited Findings
- **Dragos (2025):** tracked **119 ransomware groups** targeting industrial organizations in 2025, up from 80. **Food and beverage ranked 3rd** for ransomware impact. 45% of Siemens S7 PLCs observed are older, vulnerable models, and ICS protocols often lack authentication. Rockwell's 2025 State of the Industry report found **46% of manufacturers** had at least one cyber incident — [Food Engineering](https://www.foodengineeringmag.com/articles/104015-cybersecurity-challenges-demand-cooperation-between-it-and-ot) (vendor-sourced statistics)
- **Food-specific OT consequences:** attacks on temperature monitoring, quality control or traceability systems could lead to contaminated product and recalls. Food OT prioritizes availability and safety over security — [Dragos, Food & Beverage](https://www.dragos.com/industries/food-beverage-cybersecurity)
- **Cold chain:** up to **700 stores in France** hit through attacks on supermarket refrigeration controllers, with food losses in the tens of millions of euros. Exposed controller families (e.g., Dixell XWEB, Copeland) show a design pattern, not one brand — [ARC Advisory Group](https://www.arcweb.com/node/164547)
- **Third-party and supply-chain concentration:**
  - **IFX Networks (2023):** one hosting provider, about 762 companies affected, and ICA export procedures delayed — [MinTIC](https://www.mintic.gov.co/portal/715/w3-article-278831.html); [Agronegocios](https://www.agronegocios.co/agricultura/demoras-en-tramites-para-exportaciones-agropecuarias-en-el-ica-3708036)
  - **Blue Yonder (2024):** an SaaS supply-chain vendor; Starbucks and UK grocers affected — [Help Net Security](https://www.helpnetsecurity.com/2024/11/26/starbucks-blue-yonder-ransomware-attack/)
  - **UNFI (2025):** ordering and invoicing down across 52 distribution centers — [FoodIngredientsFirst](https://www.foodingredientsfirst.com/news/asahi-cyberattack-food-ransomware-crisis.html)
- **Grain cooperatives as precedent:** the FBI says time-sensitive agricultural operations are seen as more likely to pay — [FBI PIN, Apr 2022](https://ic3.gov/CSA/2022/220420-2.pdf)
- **Software supply chain (AI era):** the s1ngularity malware (Aug 2025) leaked about 2,000 secrets and 20,000 files from 225 victims — [Help Net Security on MDDR 2026](https://www.helpnetsecurity.com/2026/10/02/ai-cybersecurity-threats-microsoft-report/). The Shai-Hulud worm (Nov 2025) compromised hundreds of packages. An Ollama flaw left about 300,000 internet-facing model servers leaking prompts and keys — [Check Point, Jul 2026](https://blog.checkpoint.com/ai-security/ai-security-threats-in-2026-insights-from-check-point-research/)
- **Agentic supply chain:** OWASP ASI04 covers poisoned runtime components in MCP and agent-to-agent ecosystems, with the GitHub MCP exploit as the example — [OWASP, Dec 2025](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/). NIST lists "Value Chain and Component Integration", including improper supplier vetting across the AI lifecycle — [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

### Inferences
- A Colombian coffee exporter's OT and IoT footprint includes mechanical dryers and silos, threshing and milling (trilladora) lines, optical sorters, warehouse scales and humidity sensors, and container monitoring. It usually runs flat networks with remote vendor access. Ransomware that spreads from IT to these systems can halt threshing during harvest, when green coffee must be processed and shipped on schedule.
- An AI agent connected to ERP, warehouse, traceability or OT dashboards adds a new third party: the model, agent and MCP tool providers. It also adds a new path into operational systems. It should be inventoried and contracted like any critical vendor.
- These are reasoned extrapolations from food-sector evidence. No Colombian coffee-mill OT incident was found.

### Gaps
- No public OT/ICS incident at a Colombian coffee mill, dryer, warehouse or cold chain was found.
- No Latin America-specific OT statistics for agribusiness were found. Rockwell has a Colombia industry release — [Rockwell Automation](https://www.rockwellautomation.com/es-ar/company/news/press-releases/ciberataques-en-aumento-en-industria-colombiana.html) — but it was not opened.

---

## 6. Controls with the best evidence, and what Microsoft and others recommend for securing AI agents in 2025–2026

### Takeaway
The best-evidenced controls are:
- **phishing-resistant MFA** (Microsoft: blocks more than 99% of identity attacks)
- **out-of-band verification and segregation of duties for any bank-detail change or payment** (the standard BEC defense; EXIM, Bancolombia)
- for agents: **a separate identity for each agent with least privilege, verified human approval for high-impact actions, prompt-injection filtering on documents and tool outputs, monitoring kept outside the agent's reach, and red teaming**

No single filter is enough. Prompt Shields says it does not judge harm or accuracy, and is trained mainly on English. OWASP ASI09 warns that humans can be manipulated into approving harmful actions. That argues for defense in depth with hard limits in code.

### Cited Findings

**Identity and access**
- **Phishing-resistant MFA:** more than 97% of identity attacks are password attacks, and phishing-resistant MFA can stop "over 99%" of them even when attackers hold valid credentials. Identity attacks rose 32% in H1 2025 — [Microsoft On the Issues, MDDR 2025, 16 Oct 2025](https://blogs.microsoft.com/on-the-issues/2025/10/16/mddr-2025/)
- **Credential abuse after entry:** in 52.2% of valid-account intrusions, attackers harvested more credentials after getting in, and 18.4% involved password spray (MDDR 2026) — [Help Net Security, 2 Oct 2026](https://www.helpnetsecurity.com/2026/10/02/ai-cybersecurity-threats-microsoft-report/)

**Payment and BEC controls**
- **Out-of-band verification:**
  - Pay only to bank details already on file; treat new details sent by email or text as suspicious; call back on a known number — [EXIM, Jan 2025](https://grow.exim.gov/blog/is-your-international-customers-payment-going-to-the-right-place)
  - Confirm verbally any instruction to pay a new beneficiary or a supplier's "changed" account — [Bancolombia](https://www.bancolombia.com/empresas/capital-inteligente/tendencias/tendencias-globales/claves-prevenir-y-protegerse-fraude-digital/)
  - Check email headers and use an alternate channel for account changes — [INCIBE](https://www.incibe.es/empresas/blog/historias-reales-suplantaron-mi-proveedor-y-mi-empresa-estafaron)
- **Arup lesson:** a video call with "known" faces was enough to override the employee's doubts. Verification has to go through an independent, pre-registered channel, not the same conversation — [Fortune, May 2024](https://fortune.com/europe/2024/05/17/arup-deepfake-fraud-scam-victim-hong-kong-25-million-cfo/)

**Microsoft guidance for AI agents (Oct 2026)**
- "Every agent should have a first-class identity distinct from the person using or sponsoring it."
- Agents should "begin with no authority and receive only what [they need] for the approved task". Permissions should be task-scoped, time-bound and removed when the task ends.
- "Higher-impact actions can require verified human approval", for example through Dynamic Conditional Access that requires "provable human approval before a consequential action proceeds."
- The response to prompt injection should be "graduated, not binary". For an expense agent that hits an injection, that means keeping safe reads, blocking writes, narrowing reachable resources, or stopping execution.
- Enforcement and monitoring should sit outside the agent's reach, assuming "an agent can fail or be compromised". Inputs should be inspected for sensitivity, provenance and untrusted influence.
- [Microsoft Security blog, Nadim Abdo, 19 Oct 2026](https://microsoft.com/en-us/security/blog/2026/10/19/agents-are-your-newest-insiders-security-must-move-at-their-speed)

**Microsoft Entra Agent ID**
- Gives agents their own identities, and all agent authentication and actions are logged in Entra ID. Conditional Access for agents was in preview — [Microsoft Learn, Security for AI / Agent ID](https://learn.microsoft.com/en-us/entra/agent-id/security-for-ai-overview); [What's new in Microsoft AI security](https://learn.microsoft.com/security/security-for-ai/whats-new)

**Prompt Shields in Azure AI Content Safety (doc updated 2026)**
- **What it detects:**
  - **User prompt attacks** (jailbreaks): changing system rules, embedded conversation mockups, role-play, encoding attacks.
  - **Document attacks**: hidden instructions in documents, emails and web pages. Subtypes include manipulated content, information gathering, **fraud** ("acting on behalf of the user without authorization"), malware and availability.
  - For agents, it can also scan **tool responses** (preview).
- **Default settings:** user prompt attack detection is on by default. **Document attack detection is off by default and must be enabled.**
- **Spotlighting (preview):** base64-encodes third-party documents so the model treats them as lower trust. Off by default; it adds token cost.
- **Stated limits:** Prompt Shields "don't determine whether content is harmful, factually accurate, grounded… compliant with policy". The models are "**primarily trained and evaluated on English content. Performance can vary for non-English content**", and Microsoft says to test in every language used. Don't send your system prompt to the shield.
- [Microsoft Learn, Prompt Shields](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection)

**Governance**
- MDDR 2026 recommends that organizations without a suitable forum set up a dedicated **agent governance committee** of compliance specialists and agent sponsors — [CMS, 19 Nov 2026](https://cms.law/en/gbr/publication/ai-and-cyber-risk-key-takeaways-from-microsoft-s-2026-digital-defense-report)
- MDDR 2025 recommends treating cybersecurity as a core strategic priority, not only an IT issue; adopting phishing-resistant MFA; securing AI tools and training staff; and sharing threat intelligence — [Microsoft, Oct 2025](https://blogs.microsoft.com/on-the-issues/2025/10/16/mddr-2025/)

**Architectural controls from incidents**
- **GitHub MCP:** avoid any single agent session that combines untrusted input, private data access and an external write channel (the "toxic flow"). Scope tokens to the minimum resources each task needs — [Invariant Labs, May 2025](https://invariantlabs.ai/blog/mcp-github-vulnerability)
- **ForcedLeak:** enforce strict output-domain allow-lists, and treat the fix as incomplete because it does not change how agents process untrusted context — [Varonis](https://www.varonis.com/blog/forcedleak)
- **Replit:** separate dev and prod, mandatory staging, backups and rollback. Never give an agent unsupervised write or delete rights on production data — [Fortune, Jul 2025](https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/)

**Human-in-the-loop limits**
- OWASP ASI09 (Human-Agent Trust Exploitation) warns that "confident, polished explanations" can lead humans to approve harmful actions — [OWASP, Dec 2025](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/). Approvals should show the raw facts (beneficiary account, amount, source of the instruction), not only the agent's summary.

**Red teaming and testing**
- NIST AI 600-1 lists suggested actions across the AI lifecycle, including verifying sources and citations in outputs (MS-2.5-003) and testing for security attacks such as prompt injection — [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf); [Anaconda guide](https://www.anaconda.com/blog/nist-ai-600-1-generative-ai-profile-guide)

**Patch speed and AI-specific attack activity**
- Median time to weaponization is under 24 hours (MDDR 2026) — [Help Net Security](https://www.helpnetsecurity.com/2026/10/02/ai-cybersecurity-threats-microsoft-report/)
- Check Point says defenders now have about 12–72 hours to patch, and recorded about 5x growth in malicious prompt-injection payloads in Mar–May 2026 — [Check Point, Jul 2026](https://blog.checkpoint.com/ai-security/ai-security-threats-in-2026-insights-from-check-point-research/)

### Inferences
"Secure AI" as a business requirement for a coffee exporter rests on six points:
1. The attack channel an agent reads (supplier and buyer email, PDFs, web forms) is the same one BEC uses, and BEC is the second-costliest cybercrime class (FBI 2025: ~US$3.0 billion).
2. Real 2025 cases (EchoLeak, ForcedLeak, GitHub MCP) show a crafted email or form can turn an assistant into an exfiltration or fraud tool without any click.
3. Colombian law makes the exporter liable for personal-data security, reporting within 15 business days, and AI impact assessments (Circular 002/2024), even when a vendor causes the incident.
4. Prompt Shields is trained mainly on English. A Spanish-language exporter must test its filters in Spanish and cannot rely on the filter alone.
5. The controls that cost least relative to the loss avoided are deterministic:
   - a payment or bank-detail change cannot be executed by the agent alone (human approval plus out-of-band callback, with segregation of duties)
   - the agent gets read-only, task-scoped identities
   - document-attack detection and spotlighting are switched on
   - every agent action goes to a tamper-evident log outside the agent's control
6. A single avoided BEC loss or ransomware outage (US$870,000 average Colombian recovery cost; COP 470–520 million for a 3-day SME outage) likely exceeds the cost of these controls for a mid-size exporter. This is an inference; no cost-benefit study was found.

### Gaps
- No independent, quantified study was found measuring how much human-in-the-loop approval or Prompt Shields reduce successful prompt-injection or BEC losses in production.
- No Microsoft or third-party benchmark of Prompt Shields accuracy in Spanish was found.
- A Microsoft Tech Community post reportedly notes red-team cases where approval prompts were bypassed through poisoned memory. It appeared only in a search summary and could not be verified, so it is excluded from the findings.
- No Colombia-specific guidance (from SIC, MinTIC or SFC) on securing AI agents was found beyond Circular 002/2024 and CONPES 4144.
