# Context literature dossier: Paper 3

**Topic:** co-firing copper with a cordierite-type glass-ceramic, printed as one part by multi-material vat photopolymerisation (lithography-based ceramic manufacturing, e.g. the Lithoz CeraFab Multi 2M30), for three-dimensional semiconductor packages (RF modules, interposers, power substrates). The paper is simulation-only.

**Compiled:** 2026-09-24.

## How the references were checked

- Every DOI below was resolved against the Crossref REST API (`api.crossref.org/works/<DOI>`) on 2026-09-24. Title, journal, year, volume, issue and pages were taken from that record, and the BibTeX block at the end was generated from it. All 76 DOIs resolved.
- Two items have no DOI: the IEEE HIR chapter and the Lithoz trade-journal article. Both were checked by reading the PDFs.
- Summaries paraphrase the abstract. The abstract came from Crossref, OpenAlex or Semantic Scholar. When those sources had none, it came from the publisher's abstract as a search engine returned it. Those cases are marked **[abstract via search snippet]**.
- One entry has no retrievable abstract (Wang 2002). It is marked **[abstract not retrieved]**, and its summary goes no further than the title.
- ★ marks the core 3 to 6 references for each theme. The other references support them.
- Nothing here was recalled from memory without a Crossref lookup. Leads I could not verify are listed under "Gaps and unverified leads" and are **not** in the BibTeX.

---

## 1. Heterogeneous integration and 3D packaging needs

- ★ **IEEE Electronics Packaging Society (2024).** *Heterogeneous Integration Roadmap, 2024 Edition, Chapter 25: Additive Manufacturing & Additive Electronics for Heterogeneous Integration.* May 2024. https://eps.ieee.org/hir. **No DOI; checked from the chapter PDF.** `ieeeeps2024hir`
  The chapter covers additively manufactured electronics (AME) for advanced packaging and heterogeneous integration. It defines a taxonomy and comparison metrics for additive methods, including multi-material co-fabrication, conductor conductivity, resolution and build dimensionality. Its electronics-cooling section describes lithography-based ceramic manufacturing (LCM) of alumina and AlN parts with micron-scale features.

- ★ **J. H. Lau (2022).** Recent Advances and Trends in Advanced Packaging. *IEEE Trans. Compon. Packag. Manuf. Technol.* 12(2), 228–252. DOI: 10.1109/tcpmt.2022.3144461. `lau2022advanced`
  The paper defines advanced packaging and ranks its forms (2D, 2.1D, 2.3D, 2.5D and 3D IC integration) by interconnect density and electrical performance. It also covers chiplet design and heterogeneous integration, substrates and bridges, fan-in and fan-out packaging, and low-loss dielectrics for high-speed and high-frequency use.

- ★ **A. O. Watanabe, M. Ali, S. Y. B. Sayeed, R. R. Tummala, M. R. Pulugurtha (2021).** A Review of 5G Front-End Systems Package Integration. *IEEE Trans. Compon. Packag. Manuf. Technol.* 11(1), 118–133. DOI: 10.1109/tcpmt.2020.3041412. `watanabe2021review`
  Packaging RF front-end modules is hard at millimetre-wave bands, which demand low signal loss and precise impedance in thinner, smaller packages. The authors argue that 5G needs heterogeneous integration in 3D ultrathin packages, and they review the building blocks and packaging advances involved.

- **Y. Zhang, J. Mao (2019).** An Overview of the Development of Antenna-in-Package Technology for Highly Integrated Wireless Devices. *Proc. IEEE* 107(11), 2265–2280. DOI: 10.1109/jproc.2019.2933267. `zhang2019antenna`
  Antenna-in-package (AiP) technology has become the mainstream antenna and packaging solution for millimetre-wave uses such as 60 GHz radios and 77–300 GHz radar and links. The choice of materials and processes trades electrical performance against thermo-mechanical reliability, compactness, manufacturability and cost. The paper gives AiP examples in LTCC, eWLB and HDI.

- **P. Nimbalkar et al. (2025).** A Review of Glass Substrate Technologies. *Chips* 4(3), 37. DOI: 10.3390/chips4030037. `nimbalkar2025glass`
  With chiplets and heterogeneous integration, the system converges on the package substrate. The review presents glass as the platform of choice for three reasons: its properties can be tuned, it can be structured, and it can be processed at panel scale. It covers glass processing, integration techniques and research directions.

- ★ **C. Chen, F. Luo, Y. Kang (2017).** A Review of SiC Power Module Packaging: Layout, Material System and Integration. *CPSS Trans. Power Electron. Appl.* 2(3), 170–186. DOI: 10.24295/cpsstpea.2017.00017. `chen2017sic`
  Traditional device packaging limits the benefits of SiC power devices. The review covers module layout, the packaging material system and integration trends, and links each to device performance. *(Crossref's record lists only the first author. The co-authors were confirmed on Semantic Scholar.)*

- **Z. Valdez-Nava, D. Kenfaui, M.-L. Locatelli, L. Laudebat, S. Guillemet (2019).** Ceramic substrates for high voltage power electronics: past, present and future. *2019 IEEE IWIPP*, 91–96. DOI: 10.1109/iwipp.2019.8799084. `valdeznava2019ceramic`
  The paper reviews ceramic-substrate technologies for high-voltage power modules against their thermal, mechanical and dielectric challenges. It also presents a new AlN-based substrate design strategy.

## 2. LTCC/HTCC, the planar layer-by-layer route, Cu vs Ag, binder burnout and residual carbon

- ★ **R. R. Tummala (1991).** Ceramic and Glass-Ceramic Packaging in the 1990s. *J. Am. Ceram. Soc.* 74(5), 895–908. DOI: 10.1111/j.1151-2916.1991.tb04320.x. `tummala1991ceramic`
  The paper identifies glass-ceramics as the best candidates for high-performance packaging and presents glass-ceramic/copper substrate technology as the example. It projects low-k ceramics, including silica, borosilicate and cordierite composites, as future substrate materials.

- ★ **R. N. Master, L. W. Herron, R. R. Tummala (1991).** Cosintering process for glass-ceramic/copper multilayer ceramic substrate. *IEEE Trans. Compon. Hybrids Manuf. Technol.* 14(4), 780–783. DOI: 10.1109/33.105133. `master1991cosintering`
  This is IBM's System/390 ES9000 package: 63 glass-ceramic green sheets screened with copper thick-film paste and laminated. The paper covers the challenges of co-sintering glass-ceramic with Cu and a **steam sintering process** that produced a dense low-k ceramic with high-conductivity Cu. It is the historical precedent for Cu plus cordierite-type glass-ceramic co-firing.

- **Y. Imanaka (2005).** *Multilayered Low Temperature Cofired Ceramics (LTCC) Technology.* Kluwer Academic Publishers (Springer). DOI: 10.1007/b101196. `imanaka2005multilayered`
  This monograph is the standard reference on LTCC. Crossref lists chapters on ceramic material, conducting material (DOI 10.1007/0-387-23314-8_3), co-firing (DOI 10.1007/0-387-23314-8_8) and reliability. The book has no abstract, so this summary is based on its chapter structure.

- ★ **M. T. Sebastian, H. Jantunen (2008).** Low loss dielectric materials for LTCC applications: a review. *Int. Mater. Rev.* 53(2), 57–90. DOI: 10.1179/174328008x277524. `sebastian2008low`
  LTCC builds three-dimensional ceramic modules with low dielectric loss and **embedded silver electrodes**, although fabrication is layer by layer from tapes. The review brings together data on commercial and research LTCCs and glass phases, and compares them with HTCC and polymer substrates.

- **M. T. Sebastian, H. Wang, H. Jantunen (2016).** Low temperature co-fired ceramics with ultra-low sintering temperature: A review. *Curr. Opin. Solid State Mater. Sci.* 20(3), 151–170. DOI: 10.1016/j.cossms.2016.02.004. `sebastian2016ultralow`
  5G, IoT and related uses demand low-loss dielectrics with ultra-low sintering temperatures. Their properties depend on composition, purity, processing and densification. **[abstract via search snippet]**

- **Y. Deng et al. (2026).** Design and optimization of cordierite-based glass–ceramic LTCC millimeter-wave materials. *J. Adv. Dielectr.* 16(04), 2650010. DOI: 10.1142/s2010135x26500104. `deng2026cordierite`
  Cordierite (εr ≈ 5–6) is a promising substrate for LTCC high-frequency packaging. Adding R–B₂O₃–SiO₂ glasses lowered the sintering temperature from 1250 °C to 950 °C, with Bi-borosilicate glass the most effective. With 16 wt% of that glass fired at 950 °C, εr was about 6.7 at 11.7 GHz. A shrinkage anomaly was interpreted with the Frenkel and Mackenzie–Shuttleworth viscous-flow models.

- ★ **J.-H. Jean, C.-R. Chang (2004).** Interfacial Reaction Kinetics between Silver and Ceramic-Filled Glass Substrate. *J. Am. Ceram. Soc.* 87(7), 1287–1293. DOI: 10.1111/j.1151-2916.2004.tb07724.x. `jean2004interfacial`
  Ag on a borosilicate/alumina ceramic-filled glass was fired at 850–925 °C. In N₂ or N₂ + 1 % H₂ there was no interfacial reaction. In air, Ag⁺ diffused in, coupled with Al³⁺, and formed a reaction zone that grew with linear or parabolic kinetics.

- **M. Ma, Z. Liu, F. Zhang, F. Liu, Y. Li (2016).** Suppression of Silver Diffusion in Borosilicate Glass-Based LTCC by Copper Oxide Addition. *J. Am. Ceram. Soc.* 99(7), 2402–2407. DOI: 10.1111/jace.14248. `ma2016suppression`
  TEM shows Ag ions diffusing into borosilicate/alumina LTCC through the glass phase. Adding CuO speeds glass crystallisation, which raises viscosity and slows Ag diffusion.

- **S. Yang, A. Christou (2007).** Failure Model for Silver Electrochemical Migration. *IEEE Trans. Device Mater. Reliab.* 7(1), 188–196. DOI: 10.1109/tdmr.2007.891531. `yang2007failure`
  The paper models Ag electrochemical migration, including insulation-resistance loss before dendrites form. In the model, failure occurs when accumulated ion concentration passes a threshold. It was validated under combined temperature, humidity and bias. This paper supports the silver-migration argument for Cu.

- **J. Chen, D. Yang, T. Zhai, B. Gui, Q. Wang (2016).** Influence of B₂O₃–SiO₂–ZnO–BaO glass ratio and sintering temperature on the microstructure and property of copper thick film for LTCC. *J. Mater. Sci.: Mater. Electron.* 27(2), 1929–1937. DOI: 10.1007/s10854-015-3975-2. `chen2016copper`
  Cu pastes made from glass-coated Cu powder were co-sintered with LTCC at 850–910 °C. At 1 wt% glass and 910 °C, both the Cu film (about 15 µm, 1.9 mΩ/□) and the LTCC came out dense and well bonded. **[abstract via search snippet; firing atmosphere not stated in the snippet]**

- **Y. Wang, G. Zhang, J. Ma (2002).** Research of LTCC/Cu, Ag multilayer substrate in microelectronic packaging. *Mater. Sci. Eng. B* 94(1), 48–53. DOI: 10.1016/s0921-5107(02)00073-9. `wang2002research`
  **[abstract not retrieved]** The title shows the paper covers LTCC multilayer substrates with both Cu and Ag conductors. Read the full text before citing it for anything specific.

- ★ **J. A. Lewis (1997).** Binder removal from ceramics. *Annu. Rev. Mater. Sci.* 27, 147–173. DOI: 10.1146/annurev.matsci.27.1.147. `lewis1997binder`
  The review covers binder thermolysis in porous ceramic bodies: polymer degradation mechanisms and the formation of volatile products and involatile carbonaceous residue. It then treats transport through empty and binder-filled pores, defect formation in highly loaded bodies, and criteria for optimising binder removal.

- **E. Bonnet, R. L. White (2000).** Effects of water vapor on poly(vinyl butyral) ceramic binder burnout. *J. Mater. Sci.* 35(7), 1787–1792. DOI: 10.1023/a:1004736804408. `bonnet2000effects`
  Water vapour changes how poly(vinyl butyral) (PVB) decomposes in a non-oxidising atmosphere: acetic acid yields rise and C₄H₆O yields fall, because water interacts with basic oxide sites. This is relevant to burnout in wet N₂. **[abstract via search snippet]**

- **S. Lüftl, B. Balluch, W. Smetana, S. Seidler (2011).** Kinetic study of the polymeric binder burnout in green LTCC tapes. *J. Therm. Anal. Calorim.* 103(1), 157–162. DOI: 10.1007/s10973-010-0937-z. `luftl2011kinetic`
  TG and DTG were run on a commercial LTCC tape and an alumina sacrificial tape, in air up to 550 °C. Both binders degrade in several stages. Activation energies were obtained by the Flynn–Wall and Coats–Redfern methods.

- **N. Joseph, J. Varghese, M. Teirikangas, T. Vahera, H. Jantunen (2019).** Ultra-Low-Temperature Cofired Ceramic Substrates with Low Residual Carbon for Next-Generation Microwave Applications. *ACS Appl. Mater. Interfaces* 11(26), 23798–23807. DOI: 10.1021/acsami.9b07272. `joseph2019ultralow`
  CuMoO₄-based ULTCC tapes sintered at 650 °C and 500 °C had very low residual carbon by XPS, εr ≈ 8, low loss at 2–10 GHz and a CTE of 4–5 ppm/°C. This shows residual carbon is a tracked quality metric for cofired substrates. The abstract does not state the firing atmosphere, and the paper does not deal with Cu metallisation.

## 3. Additive manufacturing of ceramics for electronics

**3a. Lithography-based and vat-photopolymerisation ceramics (Lithoz, TU Wien)**

- ★ **M. Schwentenwein, J. Homa (2015).** Additive Manufacturing of Dense Alumina Ceramics. *Int. J. Appl. Ceram. Technol.* 12(1), 1–7. DOI: 10.1111/ijac.12319. `schwentenwein2015additive`
  This paper introduces the LCM process: selective curing of a photosensitive slurry by dynamic mask exposure. It reached above 99.3 % of theoretical density in alumina and 427 MPa four-point bending strength, comparable to conventionally formed alumina.

- ★ **J. Stampfl, M. Schwentenwein, J. Homa, F. B. Prinz (2023).** Lithography-based additive manufacturing of ceramics: Materials, applications and perspectives. *MRS Commun.* 13(5), 786–794. DOI: 10.1557/s43579-023-00444-0. `stampfl2023lithography`
  The paper reviews the state of the art. Slurry composition and uniformity, photochemistry and exposure strategy control bond conversion and gelling, and these in turn govern how the green part behaves during thermal processing.

- **J. W. Halloran (2016).** Ceramic Stereolithography: Additive Manufacturing for Ceramics by Photopolymerization. *Annu. Rev. Mater. Res.* 46, 19–40. DOI: 10.1146/annurev-matsci-070115-031841. `halloran2016ceramic`
  The review relates cure depth, cure width and cure profile to the optical properties of the monomer, ceramic and photoactive components. It also discusses post-steps, including binder burnout and sintering.

- **A. Zocca, P. Colombo, C. M. Gomes, J. Günster (2015).** Additive Manufacturing of Ceramics: Issues, Potentialities, and Opportunities. *J. Am. Ceram. Soc.* 98(7), 1983–2001. DOI: 10.1111/jace.13700. `zocca2015additive`
  Ceramics are hard to process by AM because of feedstock and sintering demands. The authors expect large industrial impact once AM of ceramics succeeds.

- **Z. Chen et al. (2019).** 3D printing of ceramics: A review. *J. Eur. Ceram. Soc.* 39(4), 661–687. DOI: 10.1016/j.jeurceramsoc.2018.11.013. `chen2019printing`
  The review covers ceramic 3D-printing techniques, feedstock, process control, post-treatment, comparisons between routes, and applications.

**3b. 3D-printed LTCC and glass-ceramic parts (beyond the planar tape stack)**

- ★ **J. G. Fernandes et al. (2021).** Study of mixing process of LTCC photocurable suspension for digital light processing stereolithography. *Ceram. Int.* 47(11), 15931–15938. DOI: 10.1016/j.ceramint.2021.02.167. `fernandes2021study`
  This is a DLP-SLA LTCC suspension at 40.4 vol% solids, with a viscosity of 3.6 Pa·s at 2 s⁻¹, a cure sensitivity of 41 µm and a critical energy of 15 mJ cm⁻². It printed parts without defects.

- ★ **P. Wang et al. (2026).** Fabrication of High-Resolution 3D Ceramic Electronics Via In Situ Laser-Activated Selective Electroless Plating. *Adv. Mater.* 38(48), e74140. DOI: 10.1002/adma.74140. `wang2026fabrication`
  An LTCC photopolymer loaded with antimony tin oxide (ATO) is printed by DLP and sintered. The ATO is then laser-activated to seed electroless Cu and ENIG plating. The authors demonstrated 3D circuits with ICs, high-power LED boards with thermal channels, and 3D UV sensors. **Here the metal is added after sintering, not co-fired.**

- **J. Jäger, M. Ihle, K. Gläser, A. Zimmermann (2024).** Inkjet-printed low temperature co-fired ceramics: process development for customized LTCC. *Flex. Print. Electron.* 9(2), 025022. DOI: 10.1088/2058-8585/ad59b3. `jager2024inkjet`
  LTCC is normally functionalised by screen-printing. This work replaces that with inkjet and aerosol-jet printing of Ag on green tape, plus via filling, lamination and co-firing at 850 °C. All embedded printed structures were conductive after co-firing.

**3c. Printed ceramic RF components**

- ★ **L. Qian, E. Hayward, M. Salek, Z. Liu, J. Vihinen, Y. Wang (2022).** 3-D Printed Monolithic Dielectric Waveguide Filter Using LCM Technique. *2022 IEEE MTT-S IMWS-AMP*, 1–3. DOI: 10.1109/imws-amp54652.2022.10106895. `qian2022printed`
  A single LCM-printed dielectric puck, silver-plated on the outside, forms a monolithic waveguide filter at 11.5 GHz with 850 MHz bandwidth. Measurements agree with simulation.

- **A. Fontana et al. (2023).** A Novel Approach Toward the Integration of Fully 3-D Printed Surface-Mounted Microwave Ceramic Filters. *IEEE Trans. Microw. Theory Techn.* 71(9), 3915–3928. DOI: 10.1109/tmtt.2023.3267541. `fontana2023novel`
  The authors made monolithic X-band bandpass filters as surface-mount parts for RF front ends by ceramic SLA. A laser-engraving post-tuning step corrects for manufacturing tolerances.

- **G. Mazingue, M. Romier, N. Capet (2021).** 3D Printed Ceramic Low-Profile GNSS Antenna for SmallSats. *2020 50th EuMC*, 460–462. DOI: 10.23919/eumc48046.2021.9337981. `mazingue2021printed`
  An L1 GNSS patch antenna sits on a 3D-printed structured ceramic substrate whose permittivity can be tuned. Mechanical and thermal tests showed it suits SmallSats.

## 4. Multi-material vat photopolymerisation and multi-material ceramic / ceramic–metal AM

- ★ **S. Geier, I. Potestio (Lithoz GmbH) (2020).** 3D-Printing: From Multi-Material to Functionally-Graded Ceramic. *Ceramic Applications* 8(2), 32–35. **No DOI; trade journal; checked from the PDF.** `geier2020multimaterial`
  The article describes the CeraFab Multi 2M30. It has two rotating vats, switches material within and between layers with automated cleaning, and can combine ceramics with ceramics, polymers or metals. Specifications: build volume 76 × 43 × 170 mm, 40 µm lateral resolution, 10–100 µm layers. The authors state that co-sintering requires matching shrinkage by tuning powder fractions and particle-size distribution, and they show a ZTA–Al₂O₃ demonstrator. This is manufacturer information, not peer-reviewed.

- ★ **J. Schlacher, S. Geier, M. Schwentenwein, R. Bermejo (2024).** Towards 3D-printed alumina-based multi-material components with enhanced thermal shock resistance. *J. Eur. Ceram. Soc.* 44(4), 2294–2303. DOI: 10.1016/j.jeurceramsoc.2023.11.009. `schlacher2024towards`
  ZTA and alumina layers printed in one VPP part build compressive residual stress in the embedded alumina on cooling from sintering. Strength retained after thermal shock was twice that of monoliths. This co-sintered multi-material VPP work involves Lithoz authors. The abstract does not name the printer.

- ★ **S. Xu, C. Huang, H. Liu, J. Huang (2026).** Vat Photopolymerization Additive Manufacturing for Advanced Ceramics: Techniques, Multimaterial Strategies, and Applications. *Adv. Eng. Mater.* 28(5), e202501811. DOI: 10.1002/adem.202501811. `xu2026vat`
  The review covers three multimaterial strategies (switching vat, dynamic fluidic control, VPP hybridisation), plus cleaning methods and interface design for multimaterial ceramic VPP.

- **S. Subedi et al. (2024).** Multi-material vat photopolymerization 3D printing: a review of mechanisms and applications. *npj Adv. Manuf.* 1, 9. DOI: 10.1038/s44334-024-00005-w. `subedi2024multimaterial`
  VPP was long treated as a single-material process because switching materials was slow. The review covers recent cuts in switching time and hybrid VPP routes.

- ★ **E. Schwarzer-Fischer, A. Günther, S. Roszeitis, T. Moritz (2021).** Combining Zirconia and Titanium Suboxides by Vat Photopolymerization. *Materials* 14(9), 2394. DOI: 10.3390/ma14092394. `schwarzerfischer2021combining`
  This is multi-material VPP (the multi-CAMP process) of insulating zirconia with titania. The parts were **co-sintered in a reducing atmosphere**, which turned the titania into electrically conductive suboxides. Light-absorbing, dark powders limit VPP. The test parts were single-material VPP green bodies assembled and then co-sintered.

- **J. Schubert, C.-L. Lehmann, F. Zanger (2024).** Versatile binder system as enabler for multi-material additive manufacturing of ceramics by vat photopolymerization. *Ceram. Int.* 50(23), 50948–50954. DOI: 10.1016/j.ceramint.2024.10.006. `schubert2024versatile`
  One binder system suits several ceramics, with a single debinding curve derived from TGA. Parts sintered almost free of defects. **[abstract via search snippet]**

- **J. Schubert, M. Schott, F. Zanger (2026; online 2025).** Manufacturing multi-material ceramics by sinterjoining based on vat photopolymerization (VPP). *Prod. Eng.* 20(1), 22. DOI: 10.1007/s11740-025-01402-6. `schubert2026sinterjoining`
  VPP parts with different shrinkage are nested and joined during sintering. Dilatometry covered the Al₂O₃–ZrO₂ system, and 1650 °C for 2 h was the chosen compromise. Using a defined sinterjoining factor, up to 99 % of the boundary length sintered together.

- ★ **T. Hirao, S. Hamada (2019).** Novel Multi-Material 3-Dimensional Low-Temperature Co-Fired Ceramic Base. *IEEE Access* 7, 12959–12963. DOI: 10.1109/access.2019.2892654. `hirao2019novel`
  In the "NeuroStone" process, suspensions of **ceramic and copper particles are inkjet-printed in 3D and then co-fired**, giving free-form, non-planar electrodes on and inside an LTCC body. This is the closest found precedent for Cu plus LTCC co-fired from a 3D-printed part.

- **R. Gheisari et al. (2020).** Multi-material additive manufacturing of low sintering temperature Bi₂Mo₂O₉ ceramics with Ag floating electrodes by selective laser burnout. *Virtual Phys. Prototyp.* 15(2), 133–147. DOI: 10.1080/17452759.2019.1708026. `gheisari2020multimaterial`
  Slurry AM with selective laser burnout produced a ULTCC dielectric with internal Ag electrodes. It was sintered at 645 °C to 94.5 % density, with εr 33.8 and tan δ 0.0004 at 8 GHz. The laser burnout stopped Ag leaching during co-firing.

- **P. Duan et al. (2023).** Cost-effective fabrication of customized LTCC devices with multilayer using multi-material 3D printing. *J. Manuf. Process.* 107, 88–97. DOI: 10.1016/j.jmapro.2023.10.043. `duan2023costeffective`
  Conventional LTCC processing suits fast customisation poorly. This multi-material integrated 3D printing of a borosilicate/Al₂O₃ LTCC, sintered at 850 °C, shrank 14.8 % in XY and 13.7 % in Z. The authors printed a multilayer LED circuit and a humidity sensor.

- **C. Liang et al. (2023).** Additive manufacturing of LTCC substrates and surface conductors based on material jetting. *Addit. Manuf.* 78, 103856. DOI: 10.1016/j.addma.2023.103856. `liang2023additive`
  Two printheads jet nano-LTCC and nano-Ag inks. The substrate shrank 21.5 %, the surface electrode co-fired at the same shrinkage, and there was no significant Ag/substrate interdiffusion. **[abstract via search snippet]**

- **U. Scheithauer, A. Bergner, E. Schwarzer, H.-J. Richter, T. Moritz (2014).** Studies on thermoplastic 3D printing of steel–zirconia composites. *J. Mater. Res.* 29(17), 1931–1940. DOI: 10.1557/jmr.2014.209. `scheithauer2014studies`
  Thermoplastic 3D printing (T3DP) of highly filled metal and ceramic feedstocks produced co-sintered steel–zirconia composites. The main challenge was matching sintering shrinkage between the two materials. **[abstract via search snippet]**

- **A. Günther, T. Moritz, U. Mühle (2020).** Microstructure and Interface Characteristics of 17-4PH/YSZ Components after Co-Sintering and Hydrothermal Corrosion. *Ceramics* 3(2), 245–257. DOI: 10.3390/ceramics3020022. `gunther2020microstructure`
  Stainless steel and zirconia were co-shaped (tape casting and lamination) and co-sintered. Interfaces were analysed by TEM, FESEM, EDX and XRD, and hydrothermal stability was assessed. The authors state the results carry over to other hybrid shaping routes.

## 5. Copper by vat photopolymerisation and lithography-based metal manufacturing (LMM)

- ★ **M. Roumanie, C. Flassayer, A. Resch, L. Cortella, R. Laucournet (2021).** Influence of debinding and sintering conditions on the composition and thermal conductivity of copper parts printed from highly loaded photocurable formulations. *SN Appl. Sci.* 3(1), 55. DOI: 10.1007/s42452-020-04049-3. `roumanie2021influence`
  DLP formulations were 60 vol% Cu. Debinding in air at 400 °C followed by H₂ sintering gave 0.018 wt% C. Thermal conductivity reached only 250 W m⁻¹ K⁻¹, which the authors attribute to phosphorus from the powder and the BAPO photoinitiator.

- ★ **A. Resch, A. Benayad, M. Roumanie, C. Croutxé-Barghorn (2023).** Lithography based Metal Manufacturing (LMM): Influence of particle size and composition of copper powder on UV light penetration. *Mater. Today Commun.* 35, 105595. DOI: 10.1016/j.mtcomm.2023.105595. `resch2023lithography`
  Mie-theory calculations show how Cu particle size and surface oxidation control UV penetration, and so cure depth, in LMM feedstocks. **[abstract via search snippet]**

- ★ **J. Scheibler, A. S. Kosmehl, T. Studnitzky, C. Zhong, T. Weißgärber (2024).** Lithography-Based Metal Manufacturing of Copper: Influence of Exposure Parameters on Green Part Strength. *Metals* 14(11), 1268. DOI: 10.3390/met14111268. `scheibler2024lithography`
  LMM of Cu measured single-layer cure depth against loading, particle size and exposure. Longer exposure and lower loading raise green bending strength. Loading showed no clear effect on sintered density.

- **J. Scheibler, T. Studnitzky, T. Weißgärber (2023).** Lithography-Based Manufacturing of Near Net Shape Dispersion Strengthened Copper Parts by Cuprous Oxide Reduction. *Euro PM2023 Proceedings* (EPMA). DOI: 10.59499/ep235765269. `scheibler2023lithography`
  A Cu₂O and Al₂O₃ feedstock was printed by LMM and reduced to Cu in H₂ during sintering, reaching up to 78 % IACS. Densification was incomplete.

- ★ **S. Cano Cano, P. Peritsch, J. Bosters, A. Anand, C. Gierl-Mayer, G. Attila Harakály (2024).** Recent advances of Lithography-based Metal Manufacturing of copper. *Euro PM2024 Proceedings* (EPMA). DOI: 10.59499/ep246281350. `canocano2024recent`
  The authors assess the processability by LMM of Cu powders from different sources, and the properties of the sintered parts for thermal and electrical management. *(The author name is given as registered at Crossref.)*

- **W. Wang, M. Feng, Z. Wang, Y. Jiang, B. Xing, Z. Zhao (2023).** Precision Control in Vat Photopolymerization Based on Pure Copper Paste: Process Parameters and Optimization Strategies. *Materials* 16(16), 5565. DOI: 10.3390/ma16165565. `wang2023precision`
  ANOVA and RMSD analysis of Cu-paste VPP identified the key exposure and recoating parameters. A 200 µm hole was printed with a 51 µm minimum deviation, using 21 s exposure at 220 mW cm⁻².

- **A.-L. Ye et al. (2024).** Additive manufacturing of pure copper via vat photopolymerization with slurry. *Trans. Nonferrous Met. Soc. China* 34(12), 3992–4004. DOI: 10.1016/s1003-6326(24)66653-7. `ye2024additive`
  SLA Cu slurries could be loaded to at most 55 vol%. An oxidation–reduction post-treatment raised sintering activity. The best parts reached 57.1 % IACS and HV 52.7.

- **R. Melentiev et al. (2024).** High-resolution metal 3D printing via digital light processing. *Addit. Manuf.* 85, 104156. DOI: 10.1016/j.addma.2024.104156. `melentiev2024highresolution`
  The paper presents a DLP lithographic metal AM system. It covers feedstock rheology, polymerisation dynamics, accuracy, shrinkage, density and properties. **[abstract via search snippet]**

- **J. Zeng, M. A. Saccone (2026).** Strategies for vat photopolymerization additive manufacturing of metals and ceramics. *Mater. Adv.* 7(9), 4474–4496. DOI: 10.1039/d6ma00166a. `zeng2026strategies`
  This perspective covers VPP of metals and ceramics, including how the polymer thermally decomposes, along with current challenges.

## 6. Co-sintering mismatch in multilayer ceramics and metal–ceramic co-firing

- ★ **R. K. Bordia, G. W. Scherer (1988).** On constrained sintering—I. Constitutive model for a sintering body. *Acta Metall.* 36(9), 2393–2397. DOI: 10.1016/0001-6160(88)90189-7. `bordia1988constrained`
  Sintering bodies are not linearly viscoelastic, but the matrix deformation can be treated as viscous flow. With additive sintering and stress strains, this gives a simple constitutive equation. **[abstract via search snippet]** Parts II and III are in the same issue (pp. 2399–2409 and 2411–2416).

- ★ **P. Z. Cai, D. J. Green, G. L. Messing (1997).** Constrained Densification of Alumina/Zirconia Hybrid Laminates, I: Experimental Observations of Processing Defects. *J. Am. Ceram. Soc.* 80(8), 1929–1939. DOI: 10.1111/j.1151-2916.1997.tb03075.x. `cai1997constrainedI`
  Channel cracks, edge cracks, delamination and debonding in Al₂O₃/ZrO₂ laminates come from mismatch in sintering rate and thermal expansion. They are reduced by slower heating or cooling. Mismatch stresses were estimated from bilayer curling together with viscosities from cyclic-loading dilatometry.

- **P. Z. Cai, D. J. Green, G. L. Messing (1997).** Constrained Densification of Alumina/Zirconia Hybrid Laminates, II: Viscoelastic Stress Computation. *J. Am. Ceram. Soc.* 80(8), 1940–1948. DOI: 10.1111/j.1151-2916.1997.tb03076.x. `cai1997constrainedII`
  A viscoelastic model computes mismatch stress over the whole firing cycle. Damage appears when the differential sintering stress is below the sintering pressure. Slow cooling relaxes expansion-mismatch stress above about 1200 °C.

- ★ **D. J. Green, O. Guillon, J. Rödel (2008).** Constrained sintering: A delicate balance of scales. *J. Eur. Ceram. Soc.* 28(7), 1451–1466. DOI: 10.1016/j.jeurceramsoc.2007.12.012. `green2008constrained`
  This review of the continuum-mechanics approach shows that stresses from constraint or differential densification change strain rates and cause distortion and damage. It also covers the anisotropy that develops. **[abstract via search snippet]**

- ★ **J.-H. Jean, C.-R. Chang (1997).** Cofiring Kinetics and Mechanisms of an Ag-Metallized Ceramic-Filled Glass Electronic Package. *J. Am. Ceram. Soc.* 80(12), 3084–3092. DOI: 10.1111/j.1151-2916.1997.tb03236.x. `jean1997cofiring`
  The Ag film densifies by grain-boundary diffusion, while the glass tape densifies by viscous flow of the glass. Viscous analysis predicts the camber of the Ag/tape bilayer, and experiments agree.

- **C.-R. Chang, J.-H. Jean (1998).** Effects of Silver-Paste Formulation on Camber Development during the Cofiring of a Silver-Based LTCC Package. *J. Am. Ceram. Soc.* 81(11), 2805–2814. DOI: 10.1111/j.1151-2916.1998.tb02700.x. `chang1998effects`
  Adding LTCC powder to the Ag paste makes Ag densify more like the LTCC and reduces camber. A viscous analysis reproduces the measurements. This is the ancestor of conductor/ceramic shrinkage matching.

- **M.-J. Chiang, J.-H. Jean, S.-C. Lin (2011).** The Effect of Anisotropic Shrinkage in Tape-Cast LTCC on Camber Development of Bilayer Laminates. *J. Am. Ceram. Soc.* 94(3), 683–686. DOI: 10.1111/j.1551-2916.2011.04392.x. `chiang2011effect`
  Tape-cast LTCC shrinks anisotropically, and bilayers camber toward the direction of lower packing density. Camber-free thin parts need more than three layers alternated at 90°. This is relevant to layer-wise anisotropy in printed green bodies.

- **D.-W. Ni et al. (2013).** Camber Evolution and Stress Development of Porous Ceramic Bilayers During Co-Firing. *J. Am. Ceram. Soc.* 96(3), 972–978. DOI: 10.1111/jace.12113. `ni2013camber`
  In-situ camber of CGO / LSM-CGO bilayers matched the theory, using viscosities measured by vertical sintering. The mismatch stress stayed well below the sintering stresses, and no defects formed.

- ★ **T. Rabe, W. A. Schiller, T. Hochheimer, C. Modes, A. Kipka (2005).** Zero Shrinkage of LTCC by Self-Constrained Sintering. *Int. J. Appl. Ceram. Technol.* 2(5), 374–382. DOI: 10.1111/j.1744-7402.2005.02038.x. `rabe2005zero`
  The self-constrained HeraLock LTCC achieves less than 0.2 % x–y shrinkage (±0.02 %) without sacrificial tapes or pressure. It uses an internal non-shrinking layer, or laminates of tapes that sinter in different temperature windows. The approach requires matched sintering ranges, reactivity and CTE.

- **B. Brandt, H. Naghib-zadeh, T. Rabe (2013).** Improved Co-Firing of Ferrite and Dielectric Tape Based on Master Sintering Curve Predictions and Shrinkage Mismatch Calculations. *J. Am. Ceram. Soc.* 96(3), 726–730. DOI: 10.1111/jace.12179. `brandt2013improved`
  Master sintering curves (MSCs) of the individual tapes predict linear shrinkage mismatch against the firing profile. Faster heating clearly reduced the mismatch, which lateral-shrinkage measurements confirmed.

## 7. Continuum simulation of co-sintering and multilayer sintering

- ★ **E. A. Olevsky (1998).** Theory of sintering: from discrete to continuum. *Mater. Sci. Eng. R* 23(2), 41–100. DOI: 10.1016/s0927-796x(98)00009-6. `olevsky1998theory`
  In this invited review, sintering kinetics depend on particle-level physics and also on macroscopic factors: external forces, kinematic constraints such as substrate adhesion, and density inhomogeneity. Those factors motivate a continuum theory of sintering. **[abstract via search snippet]**

- ★ **E. Olevsky et al. (2013).** Sintering of Multilayered Porous Structures: Part I—Constitutive Models. *J. Am. Ceram. Soc.* 96(8), 2657–2665. DOI: 10.1111/jace.12375. `olevsky2013sintering`
  A continuum-theory framework predicts shrinkage and distortion kinetics of co-fired bilayers, with master-sintering-curve-type solutions. It includes a method to find the shear-viscosity ratio from dilatometry of the single layers and a symmetric trilayer.

- **D. W. Ni et al. (2013).** Sintering of Multilayered Porous Structures: Part II—Experiments and Model Applications. *J. Am. Ceram. Soc.* 96(8), 2666–2673. DOI: 10.1111/jace.12374. `ni2013sintering`
  Experiments on porous and dense CGO bilayers validate Part I. All model inputs come from a single set of optical-dilatometry measurements.

- **H. L. Frandsen et al. (2013).** Modeling Sintering of Multilayers Under Influence of Gravity. *J. Am. Ceram. Soc.* 96(1), 80–89. DOI: 10.1111/jace.12070. `frandsen2013modeling`
  A thin-multilayer model couples the Skorohod–Olevsky viscous sintering (SOVS) model, classical laminate theory and the elastic–viscoelastic correspondence principle. It covers uniaxial and biaxial stress, and gravity turns out significant for thin CGO layers.

- **T. T. Molla et al. (2013).** Modeling kinetics of distortion in porous bi-layered structures. *J. Eur. Ceram. Soc.* 33(7), 1297–1305. DOI: 10.1016/j.jeurceramsoc.2012.12.019. `molla2013modeling`
  An analytical continuum-sintering model predicts densification and distortion kinetics of porous/dense CGO bilayers with differential shrinkage. **[abstract via search snippet]**

- ★ **T. T. Molla et al. (2014).** Finite Element Modeling of Camber Evolution During Sintering of Bilayer Structures. *J. Am. Ceram. Soc.* 97(9), 2965–2972. DOI: 10.1111/jace.13025. `molla2014finite`
  A finite-element (FE) model built on continuum sintering theory, and calibrated from free shrinkage, captures LSM/CGO bilayer camber. It also quantifies the effects of gravity, friction and geometry.

- **J. Kanters, U. Eisele, J. Rödel (2001).** Cosintering Simulation and Experimentation: Case Study of Nanocrystalline Zirconia. *J. Am. Ceram. Soc.* 84(12), 2757–2763. DOI: 10.1111/j.1151-2916.2001.tb01091.x. `kanters2001cosintering`
  A continuum description with diffusion parameters from free sintering reproduced the densification and curvature of zirconia laminates for various thicknesses and heating rates. Sintering and compatibility stresses were extracted.

- **S. Kiani, J. Pan, J. A. Yeomans, M. Barriere, P. Blanchart (2007).** Finite element analysis of sintering deformation using densification data instead of a constitutive law. *J. Eur. Ceram. Soc.* 27(6), 2377–2383. DOI: 10.1016/j.jeurceramsoc.2006.08.019. `kiani2007finite`
  This FE method predicts sintering deformation directly from density–time data, which can come from a master sintering curve, rather than from a constitutive law. **[abstract via search snippet]**

- **M. W. Reiterer, K. G. Ewsuk, J. G. Argüello (2006).** An Arrhenius-Type Viscosity Function to Model Sintering Using the SOVS Model Within a Finite-Element Code. *J. Am. Ceram. Soc.* 89(6), 1930–1935. DOI: 10.1111/j.1551-2916.2006.01041.x. `reiterer2006arrhenius`
  A thermally activated viscosity makes the SOVS-in-FE predictions realistic and captures the effect of heating rate. The master-sintering-curve activation energy of an **LTCC dielectric** was reused as the flow activation energy.

- **H. Ou, M. Sahli, J.-C. Gelin, T. Barrière (2014).** Experimental analysis and finite element simulation of the co-sintering of bi-material components. *Powder Technol.* 268, 269–278. DOI: 10.1016/j.powtec.2014.08.023. `ou2014experimental`
  A thermo-elasto-viscoplastic FE model of co-sintering micro bi-material powder-injection-moulded (PIM) parts was calibrated with dilatometry, beam bending and free sintering. It matched measured shrinkage and density. **[abstract via search snippet]**

- ★ **L. Chrétien, A. Heux, G. Antou, N. Pradeilles, N. Delhote, A. Maître (2022).** Distortion of an LTCC Bilayer during Constrained Sintering: Comparison between Ombroscopic Imaging and Modeling. *Materials* 15(18), 6405. DOI: 10.3390/ma15186405. `chretien2022distortion`
  An FE model with identified LTCC sintering laws predicts porous-on-dense LTCC camber, which was measured in situ by ombroscopy. Onset (about 918 K) and early evolution agree. Near 1100 K the two diverge, which the authors attribute to microcracking.

- ★ **G. Antou, A. Heux, N. Pradeilles, N. Delhote, A. Maître (2024).** Co-sintering of a ceramic-metal bilayer: Coupled experimental, analytical and numerical approaches. *Ceram. Int.* 50(22), 46196–46210. DOI: 10.1016/j.ceramint.2024.08.462. `antou2024cosintering`
  A screen-printed Au film on a silica-based LTCC was studied. The LTCC sinters by viscous flow, while Au densifies by grain-boundary diffusion (Q = 101 ± 15 kJ mol⁻¹) in two steps because of its bimodal particle size. Experiments, analytical models and numerical models are coupled. **[abstract via search snippet]** This is the closest verified metal-on-LTCC co-sintering simulation.

- **J. Balaguer et al. (2024).** Enhanced Skorohod–Olevsky viscous model incorporating microstructure evolution for finite element analysis of ceramic sintering. *J. Eur. Ceram. Soc.* 44(13), 7730–7739. DOI: 10.1016/j.jeurceramsoc.2024.05.035. `balaguer2024enhanced`
  The SOVS model is extended with grain growth and a calibrated temperature-dependent viscosity, and implemented in Code_Aster with MFront. Calibrated on porcelain stoneware by dilatometry, it predicts shrinkage and density with better than 95 % accuracy.

---

## Gaps and unverified leads

1. **No publication was found on Cu and glass-ceramic co-fired from a single multi-material VPP/LCM print.** This is the paper's novelty gap. The closest verified precedents:
   - Hirao & Hamada 2019: inkjet-printed ceramic plus Cu, co-fired.
   - Schwarzer-Fischer et al. 2021: VPP zirconia/TiOₓ co-sintered in a reducing atmosphere, from assembled green parts.
   - Schlacher et al. 2024: co-sintered ceramic–ceramic VPP.
   - Geier & Potestio 2020: Lithoz states that ceramic–metal printing is possible. This is a trade article, not peer-reviewed.
2. **No peer-reviewed paper on the CeraFab Multi 2M30 with a metal was found.** Check the full text of Schlacher 2024 before writing that it used the CeraFab Multi. Its abstract says only "vat photopolymerization".
3. **Cu-LTCC binder burnout in wet N₂ or H₂–H₂O:** the verified sources are IBM's 1991 steam-sintering paper (Master et al.) and Tummala 1991, plus generic burnout sources (Lewis 1997; Bonnet & White 2000). No journal paper from 2015 on specific to Cu-LTCC in wet N₂ was found. IBM patent US 4,234,367 (glass-ceramic with Cu conductors, firing in a controlled H₂/H₂O ratio) turned up in search, but the patent pages were blocked (403/503), so it is **UNVERIFIED** and not in the BibTeX.
4. **Residual carbon in glass-ceramics fired in non-oxidising atmospheres:** there is no dedicated verified journal paper. Joseph et al. 2019 tracks residual carbon in cofired tapes, but its abstract does not concern a reducing or wet-N₂ firing. Lewis 1997 covers carbonaceous residue in general. Cite with care.
5. **Cu/LTCC co-firing mismatch (camber) specifically:** the verified mismatch papers are for Ag/LTCC (Jean and co-workers) and Au/LTCC (Antou et al. 2024). No Cu-specific camber paper was verified. The requested "Lu & Jean" Ag/Cu-LTCC paper was not located. I found no LTCC-specific Kiani/Pan paper (Kiani 2007 covers ceramics in general).
6. **Power substrates (DBC/AMB):** the only verified reviews are an IWIPP 2019 conference review and a 2017 SiC-module review. No recent (2020 on) journal review of DBC/AMB substrates was verified.
7. **Abstract provenance:** for the entries marked [abstract via search snippet], the publisher page could not be fetched (403 or cookie wall), so the summary relies on the search engine's rendering of the abstract. Wang 2002 has no abstract at all. Read these before quoting numbers from them.
8. **Metadata quirks:**
   - Chen, Luo & Kang 2017: Crossref lists only the first author, and Semantic Scholar was used for the co-authors.
   - Cano Cano et al. 2024: Crossref registers the last author as "Attila Harakály, György". This is kept as registered.
   - Imanaka 2005: the book has no author field at Crossref, and Semantic Scholar gives "Y. Imanaka".
   - Schubert et al. was published online in 2025, with a 2026 volume.

---

## BibTeX (all verified entries; 76 with Crossref DOIs + 2 without DOI)

```bibtex
@article{lau2022advanced,
  author = {Lau, John H.},
  title = {Recent Advances and Trends in Advanced Packaging},
  year = {2022},
  doi = {10.1109/tcpmt.2022.3144461},
  journal = {IEEE Transactions on Components, Packaging and Manufacturing Technology},
  volume = {12},
  number = {2},
  pages = {228--252}
}

@article{watanabe2021review,
  author = {Watanabe, Atom O. and Ali, Muhammad and Sayeed, Sk Yeahia Been and Tummala, Rao R. and Pulugurtha, Markondeya Raj},
  title = {A Review of 5G Front-End Systems Package Integration},
  year = {2021},
  doi = {10.1109/tcpmt.2020.3041412},
  journal = {IEEE Transactions on Components, Packaging and Manufacturing Technology},
  volume = {11},
  number = {1},
  pages = {118--133}
}

@article{zhang2019antenna,
  author = {Zhang, Yueping and Mao, Junfa},
  title = {An Overview of the Development of Antenna-in-Package Technology for Highly Integrated Wireless Devices},
  year = {2019},
  doi = {10.1109/jproc.2019.2933267},
  journal = {Proceedings of the IEEE},
  volume = {107},
  number = {11},
  pages = {2265--2280}
}

@article{nimbalkar2025glass,
  author = {Nimbalkar, Pratik and Bhaskar, Pragna and Vijay Kumar, Lakshmi Narasimha and Narayanan, Meghna and Torres, Emanuel and Ambi Venkataramanan, Sai Saravanan and Kathaperumal, Mohanalingam},
  title = {A Review of Glass Substrate Technologies},
  year = {2025},
  doi = {10.3390/chips4030037},
  journal = {Chips},
  volume = {4},
  number = {3},
  pages = {37}
}

@article{chen2017sic,
  author = {Chen, Cai and Luo, F. and Kang, Yong},
  title = {A Review of SiC Power Module Packaging: Layout, Material System and Integration},
  year = {2017},
  doi = {10.24295/cpsstpea.2017.00017},
  journal = {CPSS Transactions on Power Electronics and Applications},
  volume = {2},
  number = {3},
  pages = {170--186}
}

@inproceedings{valdeznava2019ceramic,
  author = {Valdez-Nava, Zarel and Kenfaui, Driss and Locatelli, Marie-Laure and Laudebat, Lionel and Guillemet, Sophie},
  title = {Ceramic substrates for high voltage power electronics: past, present and future},
  year = {2019},
  doi = {10.1109/iwipp.2019.8799084},
  booktitle = {2019 IEEE International Workshop on Integrated Power Packaging (IWIPP)},
  pages = {91--96},
  publisher = {IEEE}
}

@article{tummala1991ceramic,
  author = {Tummala, Rao R.},
  title = {Ceramic and Glass-Ceramic Packaging in the 1990s},
  year = {1991},
  doi = {10.1111/j.1151-2916.1991.tb04320.x},
  journal = {Journal of the American Ceramic Society},
  volume = {74},
  number = {5},
  pages = {895--908}
}

@article{master1991cosintering,
  author = {Master, R.N. and Herron, L.W. and Tummala, R.R.},
  title = {Cosintering process for glass-ceramic/copper multilayer ceramic substrate},
  year = {1991},
  doi = {10.1109/33.105133},
  journal = {IEEE Transactions on Components, Hybrids, and Manufacturing Technology},
  volume = {14},
  number = {4},
  pages = {780--783}
}

@book{imanaka2005multilayered,
  author = {Imanaka, Y.},
  title = {Multilayered Low Temperature Cofired Ceramics (LTCC) Technology},
  year = {2005},
  doi = {10.1007/b101196},
  publisher = {Kluwer Academic Publishers (Springer)}
}

@article{sebastian2008low,
  author = {Sebastian, M. T. and Jantunen, H.},
  title = {Low loss dielectric materials for LTCC applications: a review},
  year = {2008},
  doi = {10.1179/174328008x277524},
  journal = {International Materials Reviews},
  volume = {53},
  number = {2},
  pages = {57--90}
}

@article{sebastian2016ultralow,
  author = {Sebastian, Mailadil Thomas and Wang, Hong and Jantunen, Heli},
  title = {Low temperature co-fired ceramics with ultra-low sintering temperature: A review},
  year = {2016},
  doi = {10.1016/j.cossms.2016.02.004},
  journal = {Current Opinion in Solid State and Materials Science},
  volume = {20},
  number = {3},
  pages = {151--170}
}

@article{deng2026cordierite,
  author = {Deng, Yingbin and Qian, Zhihua and Mao, Minmin and Liu, Bing and Qing, Peilin and Zuo, Ruzhong and Song, Kaixin},
  title = {Design and optimization of cordierite-based glass–ceramic LTCC millimeter-wave materials},
  year = {2026},
  doi = {10.1142/s2010135x26500104},
  journal = {Journal of Advanced Dielectrics},
  volume = {16},
  number = {04},
  pages = {2650010}
}

@article{jean2004interfacial,
  author = {Jean, Jau-Ho and Chang, Chia-Ruey},
  title = {Interfacial Reaction Kinetics between Silver and Ceramic-Filled Glass Substrate},
  year = {2004},
  doi = {10.1111/j.1151-2916.2004.tb07724.x},
  journal = {Journal of the American Ceramic Society},
  volume = {87},
  number = {7},
  pages = {1287--1293}
}

@article{ma2016suppression,
  author = {Ma, Mingsheng and Liu, Zhifu and Zhang, Faqiang and Liu, Feng and Li, Yongxiang},
  title = {Suppression of Silver Diffusion in Borosilicate Glass-Based Low-Temperature Cofired Ceramics by Copper Oxide Addition},
  year = {2016},
  doi = {10.1111/jace.14248},
  journal = {Journal of the American Ceramic Society},
  volume = {99},
  number = {7},
  pages = {2402--2407}
}

@article{yang2007failure,
  author = {Yang, Shuang and Christou, Aristos},
  title = {Failure Model for Silver Electrochemical Migration},
  year = {2007},
  doi = {10.1109/tdmr.2007.891531},
  journal = {IEEE Transactions on Device and Materials Reliability},
  volume = {7},
  number = {1},
  pages = {188--196}
}

@article{chen2016copper,
  author = {Chen, Jun and Yang, De'an and Zhai, Tong and Gui, Bingqiang and Wang, Qi},
  title = {Influence of B2O3–SiO2–ZnO–BaO glass ratio and sintering temperature on the microstructure and property of copper thick film for low temperature co-fired ceramic},
  year = {2016},
  doi = {10.1007/s10854-015-3975-2},
  journal = {Journal of Materials Science: Materials in Electronics},
  volume = {27},
  number = {2},
  pages = {1929--1937}
}

@article{wang2002research,
  author = {Wang, Yonggang and Zhang, Guangneng and Ma, Jusheng},
  title = {Research of LTCC/Cu, Ag multilayer substrate in microelectronic packaging},
  year = {2002},
  doi = {10.1016/s0921-5107(02)00073-9},
  journal = {Materials Science and Engineering: B},
  volume = {94},
  number = {1},
  pages = {48--53}
}

@article{lewis1997binder,
  author = {Lewis, Jennifer A.},
  title = {Binder removal from ceramics},
  year = {1997},
  doi = {10.1146/annurev.matsci.27.1.147},
  journal = {Annual Review of Materials Science},
  volume = {27},
  number = {1},
  pages = {147--173}
}

@article{bonnet2000effects,
  author = {Bonnet, E. and White, R. L.},
  title = {Effects of water vapor on poly(vinyl butyral) ceramic binder burnout},
  year = {2000},
  doi = {10.1023/a:1004736804408},
  journal = {Journal of Materials Science},
  volume = {35},
  number = {7},
  pages = {1787--1792}
}

@article{luftl2011kinetic,
  author = {Lüftl, Sigrid and Balluch, Bruno and Smetana, Walter and Seidler, Sabine},
  title = {Kinetic study of the polymeric binder burnout in green low temperature co-fired ceramic tapes},
  year = {2011},
  doi = {10.1007/s10973-010-0937-z},
  journal = {Journal of Thermal Analysis and Calorimetry},
  volume = {103},
  number = {1},
  pages = {157--162}
}

@article{joseph2019ultralow,
  author = {Joseph, Nina and Varghese, Jobin and Teirikangas, Merja and Vahera, Timo and Jantunen, Heli},
  title = {Ultra-Low-Temperature Cofired Ceramic Substrates with Low Residual Carbon for Next-Generation Microwave Applications},
  year = {2019},
  doi = {10.1021/acsami.9b07272},
  journal = {ACS Applied Materials & Interfaces},
  volume = {11},
  number = {26},
  pages = {23798--23807}
}

@article{schwentenwein2015additive,
  author = {Schwentenwein, Martin and Homa, Johannes},
  title = {Additive Manufacturing of Dense Alumina Ceramics},
  year = {2015},
  doi = {10.1111/ijac.12319},
  journal = {International Journal of Applied Ceramic Technology},
  volume = {12},
  number = {1},
  pages = {1--7}
}

@article{stampfl2023lithography,
  author = {Stampfl, Jürgen and Schwentenwein, Martin and Homa, Johannes and Prinz, Fritz B.},
  title = {Lithography-based additive manufacturing of ceramics: Materials, applications and perspectives},
  year = {2023},
  doi = {10.1557/s43579-023-00444-0},
  journal = {MRS Communications},
  volume = {13},
  number = {5},
  pages = {786--794}
}

@article{halloran2016ceramic,
  author = {Halloran, John W.},
  title = {Ceramic Stereolithography: Additive Manufacturing for Ceramics by Photopolymerization},
  year = {2016},
  doi = {10.1146/annurev-matsci-070115-031841},
  journal = {Annual Review of Materials Research},
  volume = {46},
  number = {1},
  pages = {19--40}
}

@article{zocca2015additive,
  author = {Zocca, Andrea and Colombo, Paolo and Gomes, Cynthia M. and Günster, Jens},
  title = {Additive Manufacturing of Ceramics: Issues, Potentialities, and Opportunities},
  year = {2015},
  doi = {10.1111/jace.13700},
  journal = {Journal of the American Ceramic Society},
  volume = {98},
  number = {7},
  pages = {1983--2001}
}

@article{chen2019printing,
  author = {Chen, Zhangwei and Li, Ziyong and Li, Junjie and Liu, Chengbo and Lao, Changshi and Fu, Yuelong and Liu, Changyong and Li, Yang and Wang, Pei and He, Yi},
  title = {3D printing of ceramics: A review},
  year = {2019},
  doi = {10.1016/j.jeurceramsoc.2018.11.013},
  journal = {Journal of the European Ceramic Society},
  volume = {39},
  number = {4},
  pages = {661--687}
}

@article{fernandes2021study,
  author = {Fernandes, J.G. and Barcelona, P. and Blanes, M. and Padilla, J.A. and Ramos, F. and Cirera, A. and Xuriguera, E.},
  title = {Study of mixing process of low temperature co-fired ceramics photocurable suspension for digital light processing stereolithography},
  year = {2021},
  doi = {10.1016/j.ceramint.2021.02.167},
  journal = {Ceramics International},
  volume = {47},
  number = {11},
  pages = {15931--15938}
}

@article{wang2026fabrication,
  author = {Wang, Peiren and Chen, Xiaoyi and Zhang, Hanqiang and Chen, Zihuan and Cong, Yuqi and Xu, Bo and Chen, Min and Zhang, Yan and Li, Ji},
  title = {Fabrication of High-Resolution 3D Ceramic Electronics Via In Situ Laser-Activated Selective Electroless Plating},
  year = {2026},
  doi = {10.1002/adma.74140},
  journal = {Advanced Materials},
  volume = {38},
  number = {48},
  pages = {e74140}
}

@article{jager2024inkjet,
  author = {Jäger, Jonas and Ihle, Martin and Gläser, Kerstin and Zimmermann, André},
  title = {Inkjet-printed low temperature co-fired ceramics: process development for customized LTCC},
  year = {2024},
  doi = {10.1088/2058-8585/ad59b3},
  journal = {Flexible and Printed Electronics},
  volume = {9},
  number = {2},
  pages = {025022}
}

@inproceedings{qian2022printed,
  author = {Qian, Lu and Hayward, Emelia and Salek, Milan and Liu, Zhifu and Vihinen, Jorma and Wang, Yi},
  title = {3-D Printed Monolithic Dielectric Waveguide Filter Using LCM Technique},
  year = {2022},
  doi = {10.1109/imws-amp54652.2022.10106895},
  booktitle = {2022 IEEE MTT-S International Microwave Workshop Series on Advanced Materials and Processes for RF and THz Applications (IMWS-AMP)},
  pages = {1--3},
  publisher = {IEEE}
}

@article{fontana2023novel,
  author = {Fontana, Andrés and Delage, Anthony and Périgaud, Aurélien and Richard, Patrice and Carsenat, David and Acikalin, Guillaume and Verdeyme, Serge and Bonnet, Barbara and Carpentier, Ludovic and Delhote, Nicolas},
  title = {A Novel Approach Toward the Integration of Fully 3-D Printed Surface-Mounted Microwave Ceramic Filters},
  year = {2023},
  doi = {10.1109/tmtt.2023.3267541},
  journal = {IEEE Transactions on Microwave Theory and Techniques},
  volume = {71},
  number = {9},
  pages = {3915--3928}
}

@inproceedings{mazingue2021printed,
  author = {Mazingue, Gautier and Romier, Maxime and Capet, Nicolas},
  title = {3D Printed Ceramic Low-Profile GNSS Antenna for SmallSats},
  year = {2021},
  doi = {10.23919/eumc48046.2021.9337981},
  booktitle = {2020 50th European Microwave Conference (EuMC)},
  pages = {460--462},
  publisher = {IEEE}
}

@article{schlacher2024towards,
  author = {Schlacher, Josef and Geier, Sebastian and Schwentenwein, Martin and Bermejo, Raul},
  title = {Towards 3D-printed alumina-based multi-material components with enhanced thermal shock resistance},
  year = {2024},
  doi = {10.1016/j.jeurceramsoc.2023.11.009},
  journal = {Journal of the European Ceramic Society},
  volume = {44},
  number = {4},
  pages = {2294--2303}
}

@article{subedi2024multimaterial,
  author = {Subedi, Saroj and Liu, Siying and Wang, Wenbo and Naser Shovon, S. M. Abu and Chen, Xiangfan and Ware, Henry Oliver T.},
  title = {Multi-material vat photopolymerization 3D printing: a review of mechanisms and applications},
  year = {2024},
  doi = {10.1038/s44334-024-00005-w},
  journal = {npj Advanced Manufacturing},
  volume = {1},
  number = {1},
  pages = {9}
}

@article{xu2026vat,
  author = {Xu, Shulei and Huang, Chuanzhen and Liu, Hanlian and Huang, Jun},
  title = {Vat Photopolymerization Additive Manufacturing for Advanced Ceramics: Techniques, Multimaterial Strategies, and Applications},
  year = {2026},
  doi = {10.1002/adem.202501811},
  journal = {Advanced Engineering Materials},
  volume = {28},
  number = {5},
  pages = {e202501811}
}

@article{schwarzerfischer2021combining,
  author = {Schwarzer-Fischer, Eric and Günther, Anne and Roszeitis, Sven and Moritz, Tassilo},
  title = {Combining Zirconia and Titanium Suboxides by Vat Photopolymerization},
  year = {2021},
  doi = {10.3390/ma14092394},
  journal = {Materials},
  volume = {14},
  number = {9},
  pages = {2394}
}

@article{schubert2024versatile,
  author = {Schubert, Johannes and Lehmann, Chantal-Liv and Zanger, Frederik},
  title = {Versatile binder system as enabler for multi-material additive manufacturing of ceramics by vat photopolymerization},
  year = {2024},
  doi = {10.1016/j.ceramint.2024.10.006},
  journal = {Ceramics International},
  volume = {50},
  number = {23},
  pages = {50948--50954}
}

@article{schubert2026sinterjoining,
  author = {Schubert, Johannes and Schott, Michael and Zanger, Frederik},
  title = {Manufacturing multi-material ceramics by sinterjoining based on vat photopolymerization (VPP)},
  year = {2026},
  doi = {10.1007/s11740-025-01402-6},
  journal = {Production Engineering},
  volume = {20},
  number = {1},
  pages = {22}
}

@article{hirao2019novel,
  author = {Hirao, Takahiro and Hamada, Shu},
  title = {Novel Multi-Material 3-Dimensional Low-Temperature Co-Fired Ceramic Base},
  year = {2019},
  doi = {10.1109/access.2019.2892654},
  journal = {IEEE Access},
  volume = {7},
  pages = {12959--12963}
}

@article{gheisari2020multimaterial,
  author = {Gheisari, Reza and Chamberlain, Henry and Chi-Tangyie, George and Zhang, Shiyu and Goulas, Athanasios and Lee, Chih-Kuo and Whittaker, Tom and Wang, Dawei and Ketharam, Annapoorani and Ghosh, Avishek and Vaidhyanathan, Bala and Whittow, Will and Cadman, Darren and Vardaxoglou, Yiannis C. and Reaney, Ian M. and Engstrøm, Daniel S.},
  title = {Multi-material additive manufacturing of low sintering temperature Bi$_{2}$Mo$_{2}$O$_{9}$ ceramics with Ag floating electrodes by selective laser burnout},
  year = {2020},
  doi = {10.1080/17452759.2019.1708026},
  journal = {Virtual and Physical Prototyping},
  volume = {15},
  number = {2},
  pages = {133--147}
}

@article{duan2023costeffective,
  author = {Duan, Peikai and Zhu, Xiaoyang and Zhang, Houchao and Li, Hongke and Li, Zhenghao and Wang, Rui and Zhou, Junyi and Song, Daoseng and Zhang, Youchao and Zhang, Guangming and Lan, Hongbo},
  title = {Cost-effective fabrication of customized LTCC devices with multilayer using multi-material 3D printing},
  year = {2023},
  doi = {10.1016/j.jmapro.2023.10.043},
  journal = {Journal of Manufacturing Processes},
  volume = {107},
  pages = {88--97}
}

@article{liang2023additive,
  author = {Liang, Chaoyu and Huang, Jin and Wang, Jianjun and Gong, Hongxiao and Bai, Dongqiao and Zhao, Pengbing},
  title = {Additive manufacturing of low-temperature co-fired ceramic substrates and surface conductors based on material jetting},
  year = {2023},
  doi = {10.1016/j.addma.2023.103856},
  journal = {Additive Manufacturing},
  volume = {78},
  pages = {103856}
}

@article{scheithauer2014studies,
  author = {Scheithauer, Uwe and Bergner, Anne and Schwarzer, Eric and Richter, Hans-Jürgen and Moritz, Tassilo},
  title = {Studies on thermoplastic 3D printing of steel–zirconia composites},
  year = {2014},
  doi = {10.1557/jmr.2014.209},
  journal = {Journal of Materials Research},
  volume = {29},
  number = {17},
  pages = {1931--1940}
}

@article{gunther2020microstructure,
  author = {Günther, Anne and Moritz, Tassilo and Mühle, Uwe},
  title = {Microstructure and Interface Characteristics of 17-4PH/YSZ Components after Co-Sintering and Hydrothermal Corrosion},
  year = {2020},
  doi = {10.3390/ceramics3020022},
  journal = {Ceramics},
  volume = {3},
  number = {2},
  pages = {245--257}
}

@article{roumanie2021influence,
  author = {Roumanie, Marilyne and Flassayer, Cécile and Resch, Adrien and Cortella, Laurent and Laucournet, Richard},
  title = {Influence of debinding and sintering conditions on the composition and thermal conductivity of copper parts printed from highly loaded photocurable formulations},
  year = {2021},
  doi = {10.1007/s42452-020-04049-3},
  journal = {SN Applied Sciences},
  volume = {3},
  number = {1},
  pages = {55}
}

@article{resch2023lithography,
  author = {Resch, Adrien and Benayad, Anass and Roumanie, Marilyne and Croutxé-Barghorn, Céline},
  title = {Lithography based Metal Manufacturing (LMM): Influence of particle size and composition of copper powder on UV light penetration},
  year = {2023},
  doi = {10.1016/j.mtcomm.2023.105595},
  journal = {Materials Today Communications},
  volume = {35},
  pages = {105595}
}

@article{scheibler2024lithography,
  author = {Scheibler, Jakob and Kosmehl, Alina Sabine and Studnitzky, Thomas and Zhong, Chongliang and Weißgärber, Thomas},
  title = {Lithography-Based Metal Manufacturing of Copper: Influence of Exposure Parameters on Green Part Strength},
  year = {2024},
  doi = {10.3390/met14111268},
  journal = {Metals},
  volume = {14},
  number = {11},
  pages = {1268}
}

@inproceedings{scheibler2023lithography,
  author = {Scheibler, Jakob and Studnitzky, Thomas and Weißgärber, Thomas},
  title = {Lithography-Based Manufacturing Of Near Net Shape - Dispersion Strengthened Copper Parts By Cuprous Oxide Reduction},
  year = {2023},
  doi = {10.59499/ep235765269},
  booktitle = {Euro PM2023 Proceedings},
  publisher = {EPMA}
}

@inproceedings{canocano2024recent,
  author = {Cano Cano, Santiago and Peritsch, Paul and Bosters, Johannes and Anand, Atul and Gierl-Mayer, Christian and Attila Harakály, György},
  title = {Recent advances of Lithography-based Metal Manufacturing of copper},
  year = {2024},
  doi = {10.59499/ep246281350},
  booktitle = {Euro PM2024 Proceedings},
  publisher = {EPMA}
}

@article{wang2023precision,
  author = {Wang, Weiqu and Feng, Mengzhao and Wang, Zhiwei and Jiang, Yanlin and Xing, Bohang and Zhao, Zhe},
  title = {Precision Control in Vat Photopolymerization Based on Pure Copper Paste: Process Parameters and Optimization Strategies},
  year = {2023},
  doi = {10.3390/ma16165565},
  journal = {Materials},
  volume = {16},
  number = {16},
  pages = {5565}
}

@article{ye2024additive,
  author = {Ye, An-liang and Wang, Meng and Jiang, Yan-bin and Wu, Xiao-zan and Peng, Chao-qun and He, Jin and Wang, Xiao-feng},
  title = {Additive manufacturing of pure copper via vat photopolymerization with slurry},
  year = {2024},
  doi = {10.1016/s1003-6326(24)66653-7},
  journal = {Transactions of Nonferrous Metals Society of China},
  volume = {34},
  number = {12},
  pages = {3992--4004}
}

@article{melentiev2024highresolution,
  author = {Melentiev, Ruslan and Harakály, György and Stögerer, Johannes and Mitteramskogler, Gerald and Wagih, A. and Lubineau, Gilles and Grande, Carlos A.},
  title = {High-resolution metal 3D printing via digital light processing},
  year = {2024},
  doi = {10.1016/j.addma.2024.104156},
  journal = {Additive Manufacturing},
  volume = {85},
  pages = {104156}
}

@article{zeng2026strategies,
  author = {Zeng, Jie and Saccone, Max A.},
  title = {Strategies for vat photopolymerization additive manufacturing of metals and ceramics},
  year = {2026},
  doi = {10.1039/d6ma00166a},
  journal = {Materials Advances},
  volume = {7},
  number = {9},
  pages = {4474--4496}
}

@article{bordia1988constrained,
  author = {Bordia, R.K. and Scherer, G.W.},
  title = {On constrained sintering—I. Constitutive model for a sintering body},
  year = {1988},
  doi = {10.1016/0001-6160(88)90189-7},
  journal = {Acta Metallurgica},
  volume = {36},
  number = {9},
  pages = {2393--2397}
}

@article{cai1997constrainedI,
  author = {Cai, Peter Z. and Green, David J. and Messing, Gary L.},
  title = {Constrained Densification of Alumina/Zirconia Hybrid Laminates, I: Experimental Observations of Processing Defects},
  year = {1997},
  doi = {10.1111/j.1151-2916.1997.tb03075.x},
  journal = {Journal of the American Ceramic Society},
  volume = {80},
  number = {8},
  pages = {1929--1939}
}

@article{cai1997constrainedII,
  author = {Cai, Peter Z. and Green, David J. and Messing, Gary L.},
  title = {Constrained Densification of Alumina/Zirconia Hybrid Laminates, II: Viscoelastic Stress Computation},
  year = {1997},
  doi = {10.1111/j.1151-2916.1997.tb03076.x},
  journal = {Journal of the American Ceramic Society},
  volume = {80},
  number = {8},
  pages = {1940--1948}
}

@article{green2008constrained,
  author = {Green, David J. and Guillon, Olivier and Rödel, Jürgen},
  title = {Constrained sintering: A delicate balance of scales},
  year = {2008},
  doi = {10.1016/j.jeurceramsoc.2007.12.012},
  journal = {Journal of the European Ceramic Society},
  volume = {28},
  number = {7},
  pages = {1451--1466}
}

@article{jean1997cofiring,
  author = {Jean, Jau-Ho and Chang, Chia-Ruey},
  title = {Cofiring Kinetics and Mechanisms of an Ag-Metallized Ceramic-Filled Glass Electronic Package},
  year = {1997},
  doi = {10.1111/j.1151-2916.1997.tb03236.x},
  journal = {Journal of the American Ceramic Society},
  volume = {80},
  number = {12},
  pages = {3084--3092}
}

@article{chang1998effects,
  author = {Chang, Chia-Ruey and Jean, Jau-Ho},
  title = {Effects of Silver-Paste Formulation on Camber Development during the Cofiring of a Silver-Based, Low-Temperature-Cofired Ceramic Package},
  year = {1998},
  doi = {10.1111/j.1151-2916.1998.tb02700.x},
  journal = {Journal of the American Ceramic Society},
  volume = {81},
  number = {11},
  pages = {2805--2814}
}

@article{chiang2011effect,
  author = {Chiang, Meng-Ju and Jean, Jau-Ho and Lin, Shih-Chang},
  title = {The Effect of Anisotropic Shrinkage in Tape-Cast Low-Temperature Cofired Ceramics on Camber Development of Bilayer Laminates},
  year = {2011},
  doi = {10.1111/j.1551-2916.2011.04392.x},
  journal = {Journal of the American Ceramic Society},
  volume = {94},
  number = {3},
  pages = {683--686}
}

@article{ni2013camber,
  author = {Ni, De-Wei and Esposito, Vincenzo and Schmidt, Cristine Grings and Molla, Tesfaye Tadesse and Andersen, Kjeld Bøhm and Kaiser, Andreas and Ramousse, Severine and Pryds, Nini},
  title = {Camber Evolution and Stress Development of Porous Ceramic Bilayers During Co-Firing},
  year = {2013},
  doi = {10.1111/jace.12113},
  journal = {Journal of the American Ceramic Society},
  volume = {96},
  number = {3},
  pages = {972--978}
}

@article{rabe2005zero,
  author = {Rabe, Torsten and Schiller, Wolfgang A. and Hochheimer, Thomas and Modes, Christina and Kipka, Annette},
  title = {Zero Shrinkage of LTCC by Self-Constrained Sintering},
  year = {2005},
  doi = {10.1111/j.1744-7402.2005.02038.x},
  journal = {International Journal of Applied Ceramic Technology},
  volume = {2},
  number = {5},
  pages = {374--382}
}

@article{brandt2013improved,
  author = {Brandt, Björn and Naghib-zadeh, Hamid and Rabe, Torsten},
  title = {Improved Co-Firing of Ferrite and Dielectric Tape Based on Master Sintering Curve Predictions and Shrinkage Mismatch Calculations},
  year = {2013},
  doi = {10.1111/jace.12179},
  journal = {Journal of the American Ceramic Society},
  volume = {96},
  number = {3},
  pages = {726--730}
}

@article{olevsky1998theory,
  author = {Olevsky, Eugene A.},
  title = {Theory of sintering: from discrete to continuum},
  year = {1998},
  doi = {10.1016/s0927-796x(98)00009-6},
  journal = {Materials Science and Engineering: R: Reports},
  volume = {23},
  number = {2},
  pages = {41--100}
}

@article{olevsky2013sintering,
  author = {Olevsky, Eugene and Molla, Tesfaye Tadesse and Frandsen, Henrik Lund and Bjørk, Rasmus and Esposito, Vincenzo and Ni, De Wei and Ilyina, Aleksandra and Pryds, Nini},
  title = {Sintering of Multilayered Porous Structures: Part I-Constitutive Models},
  year = {2013},
  doi = {10.1111/jace.12375},
  journal = {Journal of the American Ceramic Society},
  volume = {96},
  number = {8},
  pages = {2657--2665}
}

@article{ni2013sintering,
  author = {Ni, De Wei and Olevsky, Eugene and Esposito, Vincenzo and Molla, Tesfaye T. and Foghmoes, Søren P. V. and Bjørk, Rasmus and Frandsen, Henrik L. and Aleksandrova, Elena and Pryds, Nini},
  title = {Sintering of Multilayered Porous Structures: Part II –Experiments and Model Applications},
  year = {2013},
  doi = {10.1111/jace.12374},
  journal = {Journal of the American Ceramic Society},
  volume = {96},
  number = {8},
  pages = {2666--2673}
}

@article{frandsen2013modeling,
  author = {Frandsen, Henrik Lund and Olevsky, Eugene and Molla, Tesfaye Tadesse and Esposito, Vincenzo and Bjørk, Rasmus and Pryds, Nini},
  title = {Modeling Sintering of Multilayers Under Influence of Gravity},
  year = {2013},
  doi = {10.1111/jace.12070},
  journal = {Journal of the American Ceramic Society},
  volume = {96},
  number = {1},
  pages = {80--89}
}

@article{molla2013modeling,
  author = {Molla, Tesfaye Tadesse and Frandsen, Henrik Lund and Bjørk, Rasmus and Ni, De Wei and Olevsky, Eugene and Pryds, Nini},
  title = {Modeling kinetics of distortion in porous bi-layered structures},
  year = {2013},
  doi = {10.1016/j.jeurceramsoc.2012.12.019},
  journal = {Journal of the European Ceramic Society},
  volume = {33},
  number = {7},
  pages = {1297--1305}
}

@article{molla2014finite,
  author = {Molla, Tesfaye Tadesse and Ni, De Wei and Bulatova, Regina and Bjørk, Rasmus and Bahl, Christian and Pryds, Nini and Frandsen, Henrik Lund},
  title = {Finite Element Modeling of Camber Evolution During Sintering of Bilayer Structures},
  year = {2014},
  doi = {10.1111/jace.13025},
  journal = {Journal of the American Ceramic Society},
  volume = {97},
  number = {9},
  pages = {2965--2972}
}

@article{kanters2001cosintering,
  author = {Kanters, Johannes and Eisele, Ulrich and Rödel, Jürgen},
  title = {Cosintering Simulation and Experimentation: Case Study of Nanocrystalline Zirconia},
  year = {2001},
  doi = {10.1111/j.1151-2916.2001.tb01091.x},
  journal = {Journal of the American Ceramic Society},
  volume = {84},
  number = {12},
  pages = {2757--2763}
}

@article{kiani2007finite,
  author = {Kiani, Sasan and Pan, Jingzhe and Yeomans, Julie A. and Barriere, Magali and Blanchart, Philippe},
  title = {Finite element analysis of sintering deformation using densification data instead of a constitutive law},
  year = {2007},
  doi = {10.1016/j.jeurceramsoc.2006.08.019},
  journal = {Journal of the European Ceramic Society},
  volume = {27},
  number = {6},
  pages = {2377--2383}
}

@article{reiterer2006arrhenius,
  author = {Reiterer, M. W. and Ewsuk, K. G. and Argüello, J. G.},
  title = {An Arrhenius-Type Viscosity Function to Model Sintering Using the Skorohod–Olevsky Viscous Sintering Model Within a Finite-Element Code},
  year = {2006},
  doi = {10.1111/j.1551-2916.2006.01041.x},
  journal = {Journal of the American Ceramic Society},
  volume = {89},
  number = {6},
  pages = {1930--1935}
}

@article{ou2014experimental,
  author = {Ou, H. and Sahli, M. and Gelin, J.-C. and Barrière, T.},
  title = {Experimental analysis and finite element simulation of the co-sintering of bi-material components},
  year = {2014},
  doi = {10.1016/j.powtec.2014.08.023},
  journal = {Powder Technology},
  volume = {268},
  pages = {269--278}
}

@article{chretien2022distortion,
  author = {Chrétien, Lucie and Heux, Adrien and Antou, Guy and Pradeilles, Nicolas and Delhote, Nicolas and Maître, Alexandre},
  title = {Distortion of an LTCC Bilayer during Constrained Sintering: Comparison between Ombroscopic Imaging and Modeling},
  year = {2022},
  doi = {10.3390/ma15186405},
  journal = {Materials},
  volume = {15},
  number = {18},
  pages = {6405}
}

@article{antou2024cosintering,
  author = {Antou, Guy and Heux, Adrien and Pradeilles, Nicolas and Delhote, Nicolas and Maître, Alexandre},
  title = {Co-sintering of a ceramic-metal bilayer: Coupled experimental, analytical and numerical approaches},
  year = {2024},
  doi = {10.1016/j.ceramint.2024.08.462},
  journal = {Ceramics International},
  volume = {50},
  number = {22},
  pages = {46196--46210}
}

@article{balaguer2024enhanced,
  author = {Balaguer, J. and Tiscar, J.M. and Saburit, A. and Gomez, P. and Moreno, A. and Gilabert, F.A.},
  title = {Enhanced Skorohod–Olevsky viscous model incorporating microstructure evolution for finite element analysis of ceramic sintering},
  year = {2024},
  doi = {10.1016/j.jeurceramsoc.2024.05.035},
  journal = {Journal of the European Ceramic Society},
  volume = {44},
  number = {13},
  pages = {7730--7739}
}

@techreport{ieeeeps2024hir,
  author = {{IEEE Electronics Packaging Society}},
  title = {Heterogeneous Integration Roadmap, 2024 Edition, Chapter 25: Additive Manufacturing \& Additive Electronics for Heterogeneous Integration},
  institution = {IEEE Electronics Packaging Society},
  year = {2024},
  month = may,
  url = {https://eps.ieee.org/hir},
  note = {No DOI. Chapter PDF: https://eps.ieee.org/wp-content/uploads/2025/11/HIR_2024_ch25_AME.pdf}
}

@article{geier2020multimaterial,
  author = {Geier, Sebastian and Potestio, Isabel},
  title = {{3D}-Printing: From Multi-Material to Functionally-Graded Ceramic},
  journal = {Ceramic Applications},
  volume = {8},
  number = {2},
  pages = {32--35},
  year = {2020},
  url = {https://lithoz.com/wp-content/uploads/2022/06/3Dprinting_-_from_multi-material_to_fuctionally-graded_ceramic.pdf},
  note = {Trade-journal article by Lithoz GmbH; no DOI}
}
```
