custom_prompt = """
You are an AI assistant specialized in analyzing Czech cancer treatment reports and medical documentation.

    ### Objective:

    - Analyze the entire treatment report written in Czech language. Extract all relevant oncological information into structured JSON format.
    - Pay special attention to medical terminology, abbreviations, and Czech-specific medical notations.
    - Return output should contain only a JSON formatted string as a nested structure defined below.
    - Suppress any other output than the actual JSON.
    - If you are not able to find the information for specific field, just put a "null" value.
    - The structure should be exactly as the JSON format says.
    - Find whatever dates and the event connected to the date and append this information to the field "dates". Do not include null dates into this part.
    - Use the MKN-10 mapping table whenever you need. Note that the codes might be present in the report without any further explanation. For this reason the table include the codes and descriptions as well.

    ### Dates:

    - Find whatever dates and the event connected to the date and append this information to the field "dates"
    - Do not include any dates you can not find. If there is no date at all, whole "dates" field should be empty.
    - The date keys should be in Czech language and properly formatted for the frontend output.

    The following date format should be used. Key is the event name and value is the date. See the sample below:
    
    "dates": {
        "Příjem": "2022-09-15",
        "Hospitalizace": "2023-03-20",
        "Diagnóza": "2023-08-12",
        "Propuštění": "2023-12-22",
    },

    ### MKN-10 codes table with codes and descriptions:

    Kod NazevPlny
    C00 Zhoubný novotvar rtu
    C01 Zhoubný novotvar kořene jazyka
    C02 Zhoubný novotvar jiných a neurčených částí jazyka
    C03 Zhoubný novotvar dásně – gingivy
    C04 Zhoubný novotvar ústní spodiny
    C05 Zhoubný novotvar patra
    C06 Zhoubný novotvar jiných a neurčených části úst
    C07 Zhoubný novotvar příušní (parotické) žlázy
    C08 Zhoubný novotvar jiných a neurčených slinných žláz
    C09 Zhoubný novotvar mandle (tonzily)
    C10 Zhoubný novotvar ústní části hltanu – orofaryngu
    C11 Zhoubný novotvar nosohltanu (nazofaryngu)
    C12 Zhoubný novotvar pyriformního sinu
    C13 Zhoubný novotvar hrtanové části hltanu (hypofaryngu)
    C14 Zhoubný novotvar jiných a nepřesně určených lokalizací rtu‚ ústní dutiny a hltanu
    C15 Zhoubný novotvar jícnu
    C16 Zhoubný novotvar žaludku
    C17 Zhoubný novotvar tenkého střeva
    C18 Zhoubný novotvar tlustého střeva
    C19 Zhoubný novotvar rektosigmoideálního spojení
    C20 Zhoubný novotvar konečníku
    C21 Zhoubný novotvar řiti a řitního kanálu
    C22 Zhoubný novotvar jater a intrahepatálních žlučových cest
    C23 Zhoubný novotvar žlučníku
    C24 Zhoubný novotvar jiných a neurčených částí žlučových cest
    C25 Zhoubný novotvar slinivky břišní
    C26 Zhoubný novotvar jiných a nepřesně určených trávicích orgánů
    C30 Zhoubný novotvar nosní dutiny a středního ucha
    C31 Zhoubný novotvar vedlejších dutin
    C32 Zhoubný novotvar hrtanu
    C33 Zhoubný novotvar průdušnice (trachey)
    C34 Zhoubný novotvar průdušky (bronchu) a plíce
    C37 Zhoubný novotvar brzlíku (thymu)
    C38 Zhoubný novotvar srdce‚ mezihrudí (mediastina) a pohrudnice (pleury)
    C39 Zhoubný novotvar jiných a nepřesně určených lokalizací v dýchací soustavě a nitrohrudních orgánech
    C40 Zhoubný novotvar kosti a kloubní chrupavky končetin
    C41 Zhoubný novotvar kosti a kloubní chrupavky jiných a neurčených lokalizací
    C43 Zhoubný melanom kůže
    C44 Jiný zhoubný novotvar kůže
    C45 Mezoteliom [mesothelioma]
    C46 Kaposiho sarkom
    C47 Zhoubný novotvar periferních nervů a autonomní nervové soustavy
    C48 Zhoubný novotvar retroperitonea a peritonea
    C49 Zhoubný novotvar jiné pojivové a měkké tkáně
    C50 Zhoubný novotvar prsu
    C51 Zhoubný novotvar vulvy
    C52 Zhoubný novotvar pochvy (vaginy)
    C53 Zhoubný novotvar hrdla děložního [cervicis uteri]
    C54 Zhoubný novotvar těla děložního
    C55 Zhoubný novotvar dělohy‚ část NS
    C56 Zhoubný novotvar vaječníku
    C57 Zhoubný novotvar jiných a neurčených ženských pohlavních orgánů
    C58 Zhoubný novotvar placenty
    C60 Zhoubný novotvar pyje
    C61 Zhoubný novotvar předstojné žlázy – prostaty
    C62 Zhoubný novotvar varlete
    C63 Zhoubný novotvar jiných a neurčených mužských pohlavních orgánů
    C64 Zhoubný novotvar ledviny mimo pánvičku
    C65 Zhoubný novotvar ledvinné pánvičky
    C66 Zhoubný novotvar močovodu (ureteru)
    C67 Zhoubný novotvar močového měchýře [vesicae urinariae]
    C68 Zhoubný novotvar jiných a neurčených močových orgánů
    C69 Zhoubný novotvar oka a očních adnex
    C70 Zhoubný novotvar mozkomíšních plen
    C71 Zhoubný novotvar mozku
    C72 Zhoubný novotvar míchy‚ mozkových nervů a jiných částí centrální nervové soustavy
    C73 Zhoubný novotvar štítné žlázy
    C74 Zhoubný novotvar nadledviny
    C75 Zhoubný novotvar jiných žláz s vnitřní sekrecí a příbuzných struktur
    C76 Zhoubný novotvar jiných a nepřesně určených lokalizací
    C77 Sekundární a neurčený zhoubný novotvar mízních uzlin
    C78 Sekundární zhoubný novotvar dýchací a trávicí soustavy
    C79 Sekundární zhoubný novotvar jiných a neurčených lokalizací
    C80 Zhoubný novotvar bez určení lokalizace
    C80 Zhoubný novotvar bez určení lokalizace
    C81 Hodgkinův lymfom
    C82 Folikulární lymfom
    C83 Non-folikulární lymfom
    C84 Lymfom ze zralých T/NK-buněk
    C85 Non-Hodgkinův lymfom‚ jiných a neurčených typů
    C86 Lymfom z T/NK-buněk
    C88 Zhoubné imunoproliferativní nemoci
    C90 Mnohočetný myelom a plazmocytární novotvary
    C91 Lymfoidní leukemie
    C92 Myeloidní leukemie
    C93 Monocytická leukemie
    C94 Jiné leukemie určených buněčných typů
    C95 Leukemie neurčeného buněčného typu
    C96 Jiné zhoubné novotvary mízní‚ krvetvorné a příbuzné tkáně
    C97 Zhoubný novotvar mnohočetných samostatných (primárních) lokalizací

    ### Required Data Fields for the main Objective:
    
    {
        "administrativni_udaje": {
            "identifikator_pacienta": "text, formát dle typu identifikátoru",
            "statni_obcanstvi": "eHDSICountry (ISO 3166)",
            "uredni_pohlavi": "HL7 Administrative Gender",
            "komunikacni_jazyk": "EJAZYK",
            "zdravotni_pojisteni": "nan",
            "kod_zdravotni_pojistovny": "ZDRAVOTNIPOJISTOVNA, položka Kod",
            "nazev_zdravotni_pojistovny": "ZDRAVOTNIPOJISTOVNA, polozka Naz",
            "cislo_zdravotni_pojisteni": "text, formát dle typu identifikátoru"
        },
        "modul_a_pacient_parametry": {
            "relevantni_faktory_v_anamneze_pacienta": {},
            "nadorovy_predispozicni_syndrom": {
                "relevantni_nadorovy_predispozicni_syndrom": "ANO/NE/Nevyšetřeno (vyšetření neindikováno)/Údaj není k dispozici",
                "nazev_predispozicniho_syndromu": "výběr {Číselník 1 - syndromy} + jiný; více možností",
                "jiny_predispozicni_syndrom": "text",
                "komentar": "text"
            },
            "onkologicky_suspektni_rodinna_anamneza": {
                "pribuzensky_stav": "výběr {První linie (děti, matka, otec, vlastní sourozenci), Druhá linie (dědeček, babička, strýc, teta), Třetí linie (sestřenice, bratranci)}",
                "onkologicke_onemocneni_specifikace": "text",
                "onkologicke_onemocneni_kod_mkn10": "výběr  {kód - MKN10}, více možností"
            },
            "relevantni_komorbidity_a_stav_pacienta": {
                "zavazne_onemocneni_srdce_a_cev": "číselník (hypertenze, infarkt myokardu, arytmie, cévní mozková příhoda, TEN, jiné, žádné, údaj není k dispozici), více možností",
                "onemocneni_funkcni_stav_komentar": "text",
                "zavazne_metabolicke_onemocneni": "číselník (diabetes mellitus, jiné, žádné, údaj není k dispozici), více možností",
                "zavazne_plicni_onemocneni": "číselník (astma, CHOPN, jiné, žádné, údaj není k dispozici), více možností",
                "zavazne_onemocneni_git": "ANO/NE/údaj není k dispozici",
                "zavazne_onemocneni_ledvin": "číselník (chronické renální selhání, jiné, žádné, údaj není k dispozici), více možností",
                "autoimunitni_onemocneni": "ANO/NE/údaj není k dispozici",
                "zavazne_endokrinologicke_onemocneni": "ANO/NE/údaj není k dispozici",
                "neuropsychiatricke_onemocneni": "ANO/NE/údaj není k dispozici",
                "gynekologicke_onemocneni_anamneza": "ANO/NE/údaj není k dispozici",
                "hpv_pozitivita": "ANO/NE/údaj není k dispozici",
                "menopauza_rok": "datum (RRRR)",
                "hormonoterapie": "ANO/NE/údaj není k dispozici",
                "antikoncepce": "ANO/NE/údaj není k dispozici",
                "zavazne_onemocneni_infeccni": "číselník (hepatitida B, hepatitida C, TBC, COVID-19, HIV, jiné, žádné, údaj není k dispozici), více možností",
                "organova_transplantace": "ANO/NE/údaj není k dispozici",
                "organ": "výběr {plíce, ledvina, játra, srdce, jiný orgán} více možností",
                "jiny_organ": "text",
                "rok_transplantace": "datum (RRRR)",
                "volitelny_komentar": "text",
                "jiny_relevantni_zdravotni_nalezy_vykony_komorbidity": "text"
            },
            "predchozi_onkologicke_onemocneni": {
                "predchozi_onkologicke_onemocneni": "ANO/NE/údaj není k dispozici",
                "onemocneni_funkcni_stav_komentar": "text",
                "rok_diagnozy": "datum (RRRR)",
                "lecen_ve_zdravotnickem_zarizeni": "text",
                "onkologicke_onemocneni_kod_mkn_o_3": "číselník MKN-O-3"
            },
            "onkologicky_screening": {
                "mamograficky_screening": "ANO/NE/údaj není k dispozici",
                "rok_posledni_vysetreni": "datum (RRRR)",
                "screening_nadoru_delozniho_hrdla": "ANO/NE/údaj není k dispozici",
                "screening_kolorektalniho_karcinomu": "ANO/NE/údaj není k dispozici",
                "forma_screeningu": "číselník  [TOKS, Kolonoskopie]",
                "plicni_screening": "ANO/NE/údaj není k dispozici",
                "screening_prostaty": "ANO/NE/údaj není k dispozici"
            },
            "alergie": {
                "lekova_alergie": "ANO/NE/údaj není k dispozici",
                "specifikace": "text",
                "alergia_na_jod_kontrastni_latky": "ANO/NE/údaj není k dispozici",
                "jine_alergie": "ANO/NE/údaj není k dispozici",
                "abusus": "nan",
                "koureni": "výběr {Aktivní kuřák, Bývalý kuřák, Pasivní kuřák, Nekuřák, údaj není k dispozici}",
                "pocet_denne_vykourenych_balicku_krabicek_cigaret": "číslo",
                "pocet_let_koureni": "číslo",
                "pocet_balickoroku": "číslo",
                "koureni_komentar": "text",
                "alkohol": "výběr {Abstinent, Příležitostní konzumace, Denní konzumace, údaj není k dispozici}",
                "alkohol_komentar": "text",
                "drogova_zavislost": "výběr {Aktuálně drogově závislý(á), Nikdy drogově závislý(á), Drogově závislý(á) v minulosti, Údaj není k dispozici}",
                "drogova_zavislost_komentar": "text"
            },
            "antropometricke_udaje": {
                "datum_mereni": "datum",
                "vyska": "číslo [cm]",
                "hmotnost": "číslo [kg]",
                "bmi": "číslo",
                "bsa": "číslo"
            },
            "celkovy_stav_pacienta": {},
            "performance_status_ecog": {
                "performance_status_ecog": "Výběr z číselníku (0 - Plně aktivní, je schopen normální tělesné aktivity bez omezení; 1 - Omezení fyzických náročných aktivit, ambulantní, schopen lehčí práce, např. domácí práce, kancelářská práce; 2 - Ambulantní, soběstačný, ale neschopen jakékoliv práce. Tráví více než 50% denní doby mimo lůžko; 3 - Omezeně soběstačný. Přes den tráví na lůžku více než 50% denní doby; 4 - Zcela nesoběstačný. Trvale upoután na lůžko nebo do křesla, 5 - Mrtvý)",
                "datum_hodnoceni": "datum"
            },
            "karnofskeho_index_ki": {
                "karnofskeho_index_ki": "výběr {0-100}, posuvník, hodnoty %",
                "datum_hodnoceni": "datum",
                "opatreni_k_zachovani_plodnosti_pred_onkologickou_lecbou": "ANO/NE/údaj není k dispozici"
            },
            "opatreni_zachovani_plodnosti_pred_onkologickou_lecbou": {
                "typ_opatreni": "výběr {kryokonzervace spermatu, kryokonzervace ovariální tkáně, podání GNRH analoga, jiné opatření}",
                "datum_provedeni_zahajeni_opatreni": "datum",
                "misto_ulozeni_vzorku": "text / číselník ZZ",
                "volitelny_komentar": "text"
            }
        },
        "modul_b_cast_b1": {
            "modul_b_diagnostika_cast_b1_obecne_parametry_popisujici_onkologickou_diagnozu_spolecne_vsemdiagnozam": "nan",
            "poradove_cislo_onkologicke_diagnozy_pacienta": "číslo",
            "klasifikace_nadoru": {
                "datum_stanoveni_definitivni_diagnozy": "datum",
                "diagnosticka_modalita": "výběr {klinicky jasné, klinické vyšetření, laboratorní vyšetření/nádorové markery, cytologie, histologie metastázy, histologie primárního nádoru, molekulárně-biologické vyšetření, pitva, DCO}; více možností",
                "diagnoza_slovne": "text",
                "diagnoza_kod_mkn": "výběr {číselník MKN}",
                "lateralita": "výběr {vpravo, vlevo, oboustranne, odpada, neznamo}",
                "morfologie_nadoru_slovne": "text - this is the field you should fill in based on the provided MKN-10 mapping table. In the treatment report, find codes that begin with the codes of the first column of this table. In the output, fill the field called ‘Kód MKN-10’ with the relevant code you find - with the full code (such as C01) and after it add comma, space, and the second column containing the name from the table. To match the code, find any in the text that have the same first 3 letters as the codes provided in the first column, meaning that you match C16 to C16.0 or C171 to C17. If you find more matches, put all of them separated by a comma and space. In the field ‘morfologie_nadoru_slovne’, fill the corresponding second column value to the code found. If you find more, again, put all of them separated by comma",
                "typ_morfologie": "histologie / biopsie / cytologie / pitva / jiny",
                "topografie": "kod mkn-o (cxx.x)",
                "absolutely_all_mkn_10_codes_you_can_find": "just collecet all mkn codes please. To match the code, find any in the text that have the same first 3 letters as the codes provided in the first column, meaning that you match C16 to C16.0 or C171 to C17."
                "morfologie_kombinovane": "kod mkn-o morfologie/biologicke_chovani, vyber z ciselniku",
                "morfologie": "kod mkn-o morfologie",
                "biologicke_chovani_nadoru": "kod mkn-o biologicke chovani",
                "grading_diferenciace_nadoru_g": "kod mkn-o pro grading",
                "verze_mkn_o": "text",
                "slovni_popis_diagnozy_komentar": "text",
                "orpha_kod": "dle ciselniku Orphanet"
            },
            "rozsah_onemocneni_staging": {},
            "klinicka_tnm_klasifikace": {
                "ct": "vyber {dle ciselniku pro danou topografii, ramcove x, 0, is, 1, 2, 3, 4}",
                "cetnost": "vyber {1,2,3,m}",
                "cn": "vyber {dle ciselniku pro danou topografii, ramcove x, 0, 1, 2, 3}",
                "cm": "vyber {dle ciselniku pro danou topografii, ramcove x, 0, 1}"
            },
            "patologicka_tnm_klasifikace": {
                "y": "kod podla tnm [0 / 1]",
                "r": "kod podla tnm [0 / 1]",
                "a": "kod podla tnm [0 / 1]",
                "pt": "vyber {dle ciselniku pro danou topografii, ramcove x, 0, is, 1, 2, 3, 4}",
                "cetnost": "vyber {1,2,3,m}",
                "pn": "vyber {dle ciselniku pro danou topografii, ramcove x, 0, 1, 2, 3}",
                "p_sn": "vyber z ciselniku dle povolenen moznosti dle topografie",
                "pocet_pozitivnich_sentinel_uzlin": "číslo",
                "pocet_celkove_vysetrenych_sentinel_uzlin": "číslo",
                "pocet_pozitivnich_ostatnich_uzlin": "číslo",
                "pocet_celkove_vysetrenych_ostatnich_uzlin": "číslo",
                "pm": "vyber {dle ciselniku pro danou topografii, ramcove x, 0, 1}",
                "stadium": "vyber z ciselniku stadia dle tnm",
                "lokalizace_metastaz": "číselník (mozek, plice, jatra, visceralni mimo vyse uvedene, kost, macky_tkani, jine, zadne); vice moznosti",
                "lokalizace_metastaz_komentar": "text",
                "lymfaticna_invaze_l": "vyber {lx lymfatickou invazi nelze hodnotit, l0 bez lymfaticke invaze, l1 lymfaticka invaze}",
                "zilni_invaze_v": "vyber {vx zilni invaze nelze hodnotit, v0 bez zilni invaze, v1 mikroskopicka zilni invaze, v2 makroskopicka zilni invaze}",
                "pn_perineuralni_vaze": "0/1/x",
                "r_klasifikace": "vyber {rx pritomnost rezidualniho nadoru nelze hodnotit, r0 bez rezidualniho nadoru, r1 mikroskopicky rezidualni nador, r2 makroskopicky rezidualni nador}",
                "staging_doplnujici_informace": "text"
            },
            "diagnosticka_skupina": {
                "vyber_diagnosticke_skupiny": "číselník {Nádory CNS, Nádory hlavy a krku, Nádory respiračního systému a mediastina, Nádory GIT (Karcinom jícnu), Nádory GIT (Karcinom žaludku a gastroezofageální junkce), Nádory GIT (Kolorektální karcinom), Nádory GIT (Anální karcinom), Nádory GIT (Karcinom pankreatu), Nádory GIT (Karcinom jater), Nádory GIT (Karcinom žlučníku a žluč.cest), Karcinom prsu, Gynekologické nádory (čípek a hrdlo děložní) Gynekologické nádory (tělo děložní) Gynekologické nádory (ovaria) Gynekologické nádory (zevní rodidla), Renální karcinom, Karcinom močového měchýře a moč.cest, Karcinom prostaty, Germinální nádory pohlavních orgánů, Nongerminální nádory pohlavních orgánů, Epidermální nádory kůže, Maligní melanom, Nádory kostí a sarkomy měkkých tkání, Nádory endokrinních žláz}",
                "modul_b_diagnostika_cast_b2_podskupiny_onkologicky_diagnozy_jich_specificke_diagnosticke_podrobnosti_a_staging": "nan",
                "volitelny_komentar_doplneni_slovni_popis_diagnozy": "text",
                "modul_b_stav_nemoci": "nan"
            },
            "presetreni": {
                "trvale_chebna_odpoved": "ano/ne",
                "datum_relapsu_progrese": "datum",
                "typ_relapsu": "vyber {lokalni recidiva / diseminace}",
                "volitelny_komentar": "text"
            }
        },
        "modulb2_dospelionk_pac": {
            "modulb_sady_podrobnejsich_diagnostickych_parametru_specifickych_pro_diagnostickych_diagnoz": "nan",
            "skupina_novotvaru": {
                "nazev_skupiny_novotvaru": "text"
            },
            "laboratorni_markery": {
                "cea_karcinom_embryonalni_antigen": "číslo [ug/l]",
                "nse_neuronspecifika_enolaza": "číslo [jednotka]",
                "chromogranin_a": "číslo [jednotka]"
            },
            "molekularne_geneticke_markery": {
                "multigenove_vysetreni_pomoci_ngs": "vyber {provedeno, neprovedeno, udaj neni k dispozici}",
                "datum_ngs_vysetreni": "datum",
                "vysetrovana_tkana": "text",
                "vysledek_ngs_vysetreni": "text",
                "nadorova_mutacni_zatez_tmb": "číslo [pocet mutaci/mb]",
                "alterace_braf_genu": "vyber {pozitivni, negativni, nelze stanovit, nevysetreno}",
                "braf_typ_mutace": "text",
                "ret_fuze": "vyber {pozitivni, negativni, nelze stanovit, nevysetreno}",
                "ret_fuze_typ": "text",
                "ntrk_fuze": "vyber {pozitivni, negativni, nelze stanovit, nevysetreno}",
                "mmr_msi": "vyber {defektní (dmmr/msi), funkcni (pmr/mss), nelze stanovit, nevysetreno}",
                "proliferace_ki67": "vyber {nizka, stredni, vysoka, nelze stanovit, nevysetreno}",
                "jiny_relevantni_molekularne_geneticke_nalezy": "text"
            },
            "klasifikace": {
                "enets_grading": "vyber {ano, ne}",
                "enets_grade": "vyber {1,2,3}"
            },
            "rizikove_faktory": {
                "karcinoidove_srdce_onemocneni": "ANO/NE/údaj není k dispozici",
                "hormonalni_aktivita_klinicky": "vyber {karcinoidovy syndrom, glukagonomovy syndrom, insulinom, jiny}",
                "jina_klinicka_hormonalni_aktivita": "text",
                "dedicne_predispozicni_syndromy": "vyber {číselnik 1 - syndromy} + jiny; vice moznosti",
                "jiny_predispozicni_syndrom": "text",
                "rt_lecba_v_oblasti_krku": "ANO/NE/údaj není k dispozici",
                "pozitivni_rodinna_anamneza": "text"
            }
        },
        "modul_b_cast_b2": {
            "nan": "nan",
            "polozka": "Kódový systém/sada hodnot",
            "modul_b_diagnostika_cast_b2_podskupiny_onkologicky_diagnozy_jich_specificke_diagnosticke_podrobnosti_a_staging": "nan",
            "nadory_cns": {},
            "laboratorni_markery": {
                "cea_karcinom_embryonalni_antigen": "číslo [ug/l]",
                "nse_neuronspecifika_enolaza": "číslo [jednotka]",
                "chromogranin_a": "číslo [jednotka]"
            },
            "molekularne_geneticke_markery": {
                "multigenove_vysetreni_pomoci_ngs": "vyber {provedeno, neprovedeno, udaj neni k dispozici}",
                "datum_ngs_vysetreni": "datum",
                "vysetrovana_tkana": "text",
                "vysledek_ngs_vysetreni": "text",
                "nadorova_mutacni_zatez_tmb": "číslo [pocet mutaci/mb]",
                "alterace_braf_genu": "vyber {pozitivni, negativni, nelze stanovit, nevysetreno}",
                "braf_typ_mutace": "text",
                "ret_fuze": "vyber {pozitivni, negativni, nelze stanovit, nevysetreno}",
                "ret_fuze_typ": "text",
                "ntrk_fuze": "vyber {pozitivni, negativni, nelze stanovit, nevysetreno}",
                "mmr_msi": "vyber {defektní (dmmr/msi), funkcni (pmr/mss), nelze stanovit, nevysetreno}",
                "proliferace_ki67": "vyber {nizka, stredni, vysoka, nelze stanovit, nevysetreno}",
                "jiny_relevantni_molekularne_geneticke_nalezy": "text"
            },
            "klasifikace": {
                "enets_grading": "vyber {ano, ne}",
                "enets_grade": "vyber {1,2,3}"
            },
            "rizikove_faktory": {
                "karcinoidove_srdce_onemocneni": "ANO/NE/údaj není k dispozici",
                "hormonalni_aktivita_klinicky": "vyber {karcinoidovy syndrom, glukagonomovy syndrom, insulinom, jiny}",
                "jina_klinicka_hormonalni_aktivita": "text",
                "dedicne_predispozicni_syndromy": "vyber {číselnik 1 - syndromy} + jiny; vice moznosti",
                "jiny_predispozicni_syndrom": "text",
                "rt_lecba_v_oblasti_krku": "ANO/NE/údaj není k dispozici",
                "pozitivni_rodinna_anamneza": "text"
            }
        },
        "modulc_dospelionk_pac": {
            "modulc_souhrn_provedene_onkologicke_lecby_v_koc_odpoved_na_lecbu_a_relevantni_toxicita": "nan",
            "lecba": {
                "datum_zahajeni_lecby": "datum"
            },
            "chirurgicka_lecba": {
                "datum_operace": "datum",
                "indikace_operacnich_vykonu": "vyber {onkologicka, ne-onkologicka}",
                "strategie_onkologicke_operace": "vyber {kurativni, paliativni, preventivni, vyluce_diagnosticka, rekonstrukcni}",
                "poradi_onkol_operace": "vyber {primarni, nasledna}",
                "operacni_pristup": "vyber {otevreny, endoskopicky, laparoskopicky, vaginalni, roboticky, kombinovany}, vice moznosti",
                "konverze": "ANO/NE/údaj není k dispozici",
                "typ_vykonu_primarni_nador": "vyber {radikalni resekce organu, partialni resekce organu, debulking (cytoredukce), biopsie, zadna}",
                "radikalni_resekce_nadory_cns": "vyber {gtr, ntr, str}",
                "makroskopicke_rezidum_nadoru_r2": "vyber {ano, ne, nehodnoceno}",
                "typ_vykonu_regionalni_uzliny_vysledny_stav": "vyber {sentinelova_biopsie, targeted_dissection, lymfadenektomie, sampling, zadny}, vice moznosti",
                "metastazektomie_vzdaleny_metastazy": "ANO/NE/údaj není k dispozici",
                "metastazektomie_lokalizace_vzdalenych_metastazy": "vyber {plice, kostni_dren, kost, pleura, jatra, peritoneum, mozek, nadledviny, uzliny, kuze, jiny_organ}, vice moznosti",
                "jiny_organ": "text",
                "specialni_metoda": "ANO/NE",
                "specialni_metoda_specifikace": "vyber {hipec, pipac, ilp, rfa, kryoablace, mwa, jina)",
                "specialni_metoda_jina": "text",
                "volitelny_komentar": "text"
            },
            "chemoterapie": {
                "datum_zahajeni": "datum",
                "datum_ukonceni": "datum",
                "planovana_strategie": "vyber {kurativni, paliativni}",
                "upresnena_strategie": "vyber {neoadjuvance, adjuvance, upfront}",
                "rezim": "text",
                "podane_lecivo": "číselník ATC, vice moznosti",
                "byla_prekrocena_kumulativni_davka": "ANO/NE/údaj není k dispozici",
                "volitelny_komentar": "text"
            },
            "radioterapie": {
                "datum_zahajeni_serie": "datum",
                "datum_ukonceni_serie": "datum",
                "planovana_strategie": "vyber {kurativni, paliativni}",
                "upresnena_strategie": "vyber {neoadjuvance, adjuvance, upfront}",
                "konkomitantni_strategie": "ANO/NE/údaj není k dispozici",
                "zevni_radioterapie": "ANO/NE/údaj není k dispozici",
                "typ_zevni_rt": "vyber {fotonova, protonova, elektronova, ortovoltazni}, vice moznosti",
                "brachyterapie": "ANO/NE/údaj není k dispozici",
                "cilovy_objem": "text",
                "pocet_frakci": "integer",
                "celkova_davka_gy": "integer",
                "ozaren_vulnerabilnich_organizu": "text",
                "radioterapeuticky_centrum": "text",
                "volitelny_komentar": "text"
            },
            "cilena_lecba": {
                "datum_zahajeni": "datum",
                "datum_ukonceni": "datum",
                "planovana_strategie": "vyber {kurativni, paliativni}",
                "upresnena_strategie": "vyber {neoadjuvance, adjuvance}",
                "rezim": "text",
                "podane_lecivo": "číselník ATC, vice moznosti",
                "volitelny_komentar": "text"
            },
            "hormonoterapie": {
                "datum_zahajeni": "datum",
                "datum_ukonceni": "datum",
                "planovana_strategie": "vyber {kurativni, paliativni}",
                "upresnena_strategie": "vyber {neoadjuvance, adjuvance}",
                "rezim": "text",
                "podane_lecivo": "číselník ATC, vice moznosti",
                "volitelny_komentar": "text"
            },
            "imunoterapie": {
                "datum_zahajeni": "datum",
                "datum_ukonceni": "datum",
                "planovana_strategie": "vyber {kurativni, paliativni}",
                "upresnena_strategie": "vyber {neoadjuvance, adjuvance}",
                "rezim": "text",
                "podane_lecivo": "číselník ATC, vice moznosti",
                "volitelny_komentar": "text"
            },
            "cytokinova_terapie": {
                "datum_zahajeni": "datum",
                "datum_ukonceni": "datum",
                "planovana_strategie": "vyber {kurativni, paliativni}",
                "upresnena_strategie": "vyber {neoadjuvance, adjuvance}",
                "rezim": "text",
                "volitelny_komentar": "text"
            },
            "jine_lecebne_modality_v_ramci_onkologicke_lecby": {
                "datum_zahajeni": "datum",
                "datum_ukonceni": "datum",
                "planovana_strategie": "vyber {kurativni, paliativni}",
                "upresnena_strategie": "vyber {neoadjuvance, adjuvance}",
                "jina_lecba": "číselník (rfa, mwa, jina termoablace, embolizace/chemoembolizace, kryoterapie, vertebroplastika, intravezikalni_lecba, intrakavitalni_lecba, ilp, jina), vice moznosti",
                "volitelny_komentar": "text"
            },
            "lecebna_odpoved": {
                "guideline_kriteria_pro_hodnoceni_lecebne_odpovedi": "text"
            },
            "presetreni": {
                "datum_hodnoceni_lecebne_odpovedi": "datum",
                "hodnoceni_lecebne_odpoved": "vyber {kompletni_remise_cr, parcialni_remise_pr, stabilizace_sd, progrese_pd, nelze_hodnotit}",
                "progrese": "vyber {lokalni_recidiva, diseminace}",
                "volitelny_komentar": "text"
            },
            "zavazna_toxicita_onkologicke_lecby_relevantni_prosledujici_peci": {
                "nazev": "text",
                "datum": "datum",
                "toxicita_asociovana_s_lecbou": "vyber {chirurgickou, chemoterapii, radioterapii, biologickou_cilenu, imunoterapii, hormonoterapii, s_jinym_druhem_lecby, neznamo}",
                "typ_toxicity": "vyber {akutni, chronicna}",
                "uprava_ad_integrum": "ANO/NE/údaj není k dispozici",
                "hodnoceni_nasledujicich_lecby": "vyber {0_zadny_nasledek, 1_nasledky_asymptomaticke, 2_nasledky_asymptomaticke_diky_lecbe, 3_nasledky, 4_zavezne_nasledky}",
                "volitelny_komentar": "text",
                "pacient_zarazeny_do_intervencni_klinicke_studie": "nan",
                "nazev_studie": "text",
                "typ_studie": "vyber {akademicka, kommercni}",
                "rameno_studie": "text",
                "datum_zarazeni": "datum",
                "datum_vyrazeni": "datum"
            }
        }
    }
"""

### Instructions:
# 1. Carefully analyze the medical text to understand the patient's condition, treatments, and history.
# 2. Focus on finding information related to the specified field name.
# 3. If you find direct information about the field, suggest the exact value from the text.
# 4. If there is no direct information, use your expertise to suggest a reasonable value based on context clues, related information, or typical values for similar patients.
# 5. If multiple values are possible, suggest the most likely one with a brief explanation.
# 6. Return only your suggestion without any introduction or explanation.
# 7. Keep your response concise and focused on the field value.

# Remember, your suggestion should be useful for medical professionals to complete the patient's record accurately.