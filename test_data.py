"""
Test script to generate a sample response from OpenAI.
This can be used to test the frontend without needing actual Azure OpenAI credentials.
"""

import json
import sys

SAMPLE_MEDICAL_TEXT = """
=== 4484. 1454753 / 930XXXXXXX / 60891
prof. MUDr. Büchler Tomáš, Ph.D.
C629 
Dg. souhrn:
Tu testis l sin pT1 N1? M0 S0
histol: postpubertální teratom varlete v terénu GCNIS, s nezralými okrsky s vyšší mitotickou aktivitou. 
Orchiectomia radicalis l. sin. 27.01.23
Kryoprezervace provedena

S. Cítí se dobře, bolesti neguje, močení a stolice bez potíží
O. PS 0, afebrilní, bez ikteru, DÚ čistá, dýchání čisté, břicho klidné, DKK bez otoků. Bez periferní lymfadenopatie. 

Popis CT není zcela jednoznačný, uzlina je zvětšená, ale popis je s otazníkem, doporučují došetření 

19.4.2023 Hypermetabolizmus glukózy v nezvětšené retroperitoneální uzlině paraaortálně vlevo je velmi susp. z viabilní neoploazie, v její těsné blízkosti se nachází hypodenzní zvětšená lymf. uzlina/ložisko, která však není metabolicky aktivní a může představovat nekrotickou uzlinu/neviabilní neoplazii. Ložiskový hypermetabolizmus glukózy v kortexu kraniální 1/3 pravé ledviny dorzálně v místě hypodenzního ložiska - v dif. dg. může představovat viabilní neoplazii (duplicitu), nebo cystu komunikující s kalichopánvičkovým systémem ledviny, nutno dovyšetřit, dop. cílené 3-fázové CT vyš. ledvin včetně vylučovací fáze, event. také srovnat se starší CT dokumentací, je-li k dispozici. Další zřetelná abnormální ložiska hypermetabolizmu glukózy v rozsahu vyšetření nenacházím.

Plán: probereme na MDT - primární RPLND?

Pacient odchází z ambulance bez známek dechové a oběhové nedostatečnosti.
"""

SAMPLE_RESPONSE = {
    "administrativni_udaje": {
        "identifikator_pacienta": "null",
        "statni_obcanstvi": "null",
        "uredni_pohlavi": "null",
        "komunikacni_jazyk": "null",
        "zdravotni_pojisteni": "null",
        "kod_zdravotni_pojistovny": "null",
        "nazev_zdravotni_pojistovny": "null",
        "cislo_zdravotni_pojisteni": "null",
    },
    "modul_a_pacient_parametry": {
        "modul_a_parametry_vztahujici_se_pacientovi": "null",
        "relevantni_faktory_v_anamneze_pacienta": {
            "RA": "urologicky a onkologicky nevýznamná",
            "OA": "ca rekta CHT+RT 1999, hypothyreoza, IM 2020 + 2stenty, páska pro inkontinenci, CHCE 2014, v dětství APPE, Barettův jícen",
            "SA": "knihovnice",
            "EA": "COVID-19 očkovaná",
            "léky": "Anopyrin, Carzap, Betaloc ZOK, Vigantol, Lanzul, Euthyrox",
        },
        "nadorovy_predispozicni_syndrom": {
            "relevantni_nadorovy_predispozicni_syndrom": "null",
            "nazev_predispozicniho_syndromu": "null",
            "jiny_predispozicni_syndrom": "null",
            "komentar": "null",
        },
        "onkologicky_suspektni_rodinna_anamneza": {
            "pribuzensky_stav": "null",
            "onkologicke_onemocneni_specifikace": "null",
            "onkologicke_onemocneni_kod_mkn10": "null",
        },
        "relevantni_komorbidity_a_stav_pacienta": {
            "zavazne_onemocneni_srdce_a_cev": "IM, 2 stenty 2020",
            "onemocneni_funkcni_stav_komentar": "null",
            "zavazne_metabolicke_onemocneni": "hypothyreoza",
            "zavazne_plicni_onemocneni": "null",
            "zavazne_onemocneni_git": "Barettův jícen",
            "zavazne_onemocneni_ledvin": "null",
            "autoimunitni_onemocneni": "ANO",
            "zavazne_endokrinologicke_onemocneni": "null",
            "neuropsychiatricke_onemocneni": "null",
            "gynekologicke_onemocneni_anamneza": "null",
            "hpv_pozitivita": "null",
            "menopauza_rok": "null",
            "hormonoterapie": "null",
            "antikoncepce": "null",
            "zavazne_onemocneni_infeccni": "null",
            "organova_transplantace": "null",
            "organ": "null",
            "jiny_organ": "null",
            "rok_transplantace": "null",
            "volitelny_komentar": "null",
            "jiny_relevantni_zdravotni_nalezy_vykony_komorbidity": "null",
        },
        "predchozi_onkologicke_onemocneni": {
            "predchozi_onkologicke_onemocneni": "ANO",
            "onemocneni_funkcni_stav_komentar": "ca rekta, CHT+RT 1999, dispenzarizace bez známek recidivy",
            "rok_diagnozy": "1999",
            "lecen_ve_zdravotnickem_zarizeni": "null",
            "onkologicke_onemocneni_kod_mkn_o_3": "null",
        },
        "onkologicky_screening": {
            "mamograficky_screening": "null",
            "rok_posledni_vysetreni": "null",
            "screening_nadoru_delozniho_hrdla": "null",
            "screening_kolorektalniho_karcinomu": "null",
            "forma_screeningu": "null",
            "plicni_screening": "null",
            "screening_prostaty": "null",
        },
        "alergie": {
            "lekova_alergie": "ANO",
            "specifikace": "Sumamed (gastroenterologické obtíže)",
            "alergia_na_jod_kontrastni_latky": "null",
            "jine_alergie": "null",
            "abusus": "null",
            "koureni": "Bývalý kuřák",
            "pocet_denne_vykourenych_balicku_krabicek_cigaret": "2-3",
            "pocet_let_koureni": "20",
            "pocet_balickoroku": "40-60",
            "koureni_komentar": "kouření do roku 2000",
            "alkohol": "null",
            "alkohol_komentar": "null",
            "drogova_zavislost": "Nikdy drogově závislý",
            "drogova_zavislost_komentar": "null",
        },
        "antropometricke_udaje": {
            "datum_mereni": "2023-11",
            "vyska": "155",
            "hmotnost": "61",
            "bmi": "null",
            "bsa": "null",
        },
        "celkovy_stav_pacienta": {},
        "performance_status_ecog": {
            "performance_status_ecog": "1",
            "datum_hodnoceni": "2023-11",
        },
        "karnofskeho_index_ki": {
            "karnofskeho_index_ki": "null",
            "datum_hodnoceni": "null",
            "opatreni_k_zachovani_plodnosti_pred_onkologickou_lecbou": "null",
        },
        "opatreni_zachovani_plodnosti_pred_onkologickou_lecbou": {
            "typ_opatreni": "null",
            "datum_provedeni_zahajeni_opatreni": "null",
            "misto_ulozeni_vzorku": "null",
            "volitelny_komentar": "null",
        },
    },
    "modul_b_cast_b1": {
        "modul_b_diagnostika_cast_b1_obecne_parametry_popisujici_onkologickou_diagnozu_spolecne_vsemdiagnozam": "null",
        "poradove_cislo_onkologicke_diagnozy_pacienta": "null",
        "klasifikace_nadoru": {
            "datum_stanoveni_definitivni_diagnozy": "2014",
            "diagnosticka_modalita": "null",
            "diagnoza_slovne": "Ca recti, ca vesiacae urinariae",
            "diagnoza_kod_mkn": "null",
            "lateralita": "null",
            "morfologie_nadoru_slovne": "high-grade uroteliální karcinom (grade 3)",
            "typ_morfologie": "null",
            "topografie": "C679",
            "morfologie_kombinovane": "null",
            "morfologie": "null",
            "biologicke_chovani_nadoru": "null",
            "grading_diferenciace_nadoru_g": "null",
            "verze_mkn_o": "3",
            "slovni_popis_diagnozy_komentar": "null",
            "orpha_kod": "null",
        },
        "rozsah_onemocneni_staging": {},
        "klinicka_tnm_klasifikace": {"ct": "T2", "cetnost": "null", "cn": "N0", "cm": "M0"},
        "patologicka_tnm_klasifikace": {
            "y": "null",
            "r": "null",
            "a": "null",
            "pt": "T0",
            "cetnost": "null",
            "pn": "N0",
            "p_sn": "null",
            "pocet_pozitivnich_sentinel_uzlin": "null",
            "pocet_celkove_vysetrenych_sentinel_uzlin": "null",
            "pocet_pozitivnich_ostatnich_uzlin": "null",
            "pocet_celkove_vysetrenych_ostatnich_uzlin": "null",
            "pm": "M0",
            "stadium": "null",
            "lokalizace_metastaz": "null",
            "lokalizace_metastaz_komentar": "null",
            "lymfaticna_invaze_l": "null",
            "zilni_invaze_v": "null",
            "pn_perineuralni_vaze": "null",
            "r_klasifikace": "R0",
            "staging_doplnujici_informace": "null",
        },
        "diagnosticka_skupina": {
            "vyber_diagnosticke_skupiny": "Karcinom močového měchýře",
            "modul_b_diagnostika_cast_b2_podskupiny_onkologicky_diagnozy_jich_specificke_diagnosticke_podrobnosti_a_staging": "null",
            "volitelny_komentar_doplneni_slovni_popis_diagnozy": "null",
            "modul_b_stav_nemoci": "null",
        },
        "presetreni": {
            "trvale_chebna_odpoved": "ano",
            "datum_relapsu_progrese": "null",
            "typ_relapsu": "null",
            "volitelny_komentar": "null",
        },
    },
    "modulc_dospelionk_pac": {
        "modulc_souhrn_provedene_onkologicke_lecby_v_koc_odpoved_na_lecbu_a_relevantni_toxicita": "null",
        "lecba": {"datum_zahajeni_lecby": "2023-03-28"},
        "chirurgicka_lecba": {
            "datum_operace": "2023-09-08",
            "indikace_operacnich_vykonu": "onkologická",
            "strategie_onkologicke_operace": "kurativní",
            "poradi_onkol_operace": "primární",
            "operacni_pristup": "otevřený",
            "konverze": "null",
            "typ_vykonu_primarni_nador": "radikální resekce orgánu",
            "radikalni_resekce_nadory_cns": "null",
            "makroskopicke_rezidum_nadoru_r2": "ne",
            "typ_vykonu_regionalni_uzliny_vysledny_stav": "null",
            "metastazektomie_vzdaleny_metastazy": "null",
            "metastazektomie_lokalizace_vzdalenych_metastazy": "null",
            "jiny_organ": "null",
            "specialni_metoda": "ne",
            "specialni_metoda_specifikace": "null",
            "specialni_metoda_jina": "null",
            "volitelny_komentar": "null",
        },
        "chemoterapie": {
            "datum_zahajeni": "2023-03-28",
            "datum_ukonceni": "2023-06-06",
            "planovana_strategie": "kurativní",
            "upresnena_strategie": "neoadjuvance",
            "rezim": "cDDP + gemcitabin",
            "podane_lecivo": ["Cisplatina", "Gemcitabin"],
            "byla_prekrocena_kumulativni_davka": "ne",
            "volitelny_komentar": "null",
        },
        "radioterapie": {
            "datum_zahajeni_serie": "1999",
            "datum_ukonceni_serie": "1999",
            "planovana_strategie": "kurativní",
            "upresnena_strategie": "radikální",
            "konkomitantni_strategie": "null",
            "zevni_radioterapie": "ano",
            "typ_zevni_rt": "fotonová",
            "brachyterapie": "ne",
            "cilovy_objem": "Anální karcinom",
            "pocet_frakci": "null",
            "celkova_davka_gy": "null",
            "ozaren_vulnerabilnich_organizu": "null",
            "radioterapeuticky_centrum": "null",
            "volitelny_komentar": "null",
        },
        "cilena_lecba": {
            "datum_zahajeni": "null",
            "datum_ukonceni": "null",
            "planovana_strategie": "null",
            "upresnena_strategie": "null",
            "rezim": "null",
            "podane_lecivo": "null",
            "volitelny_komentar": "null",
        },
        "hormonoterapie": {
            "datum_zahajeni": "null",
            "datum_ukonceni": "null",
            "planovana_strategie": "null",
            "upresnena_strategie": "null",
            "rezim": "null",
            "podane_lecivo": "null",
            "volitelny_komentar": "null",
        },
        "imunoterapie": {
            "datum_zahajeni": "null",
            "datum_ukonceni": "null",
            "planovana_strategie": "null",
            "upresnena_strategie": "null",
            "rezim": "null",
            "podane_lecivo": "null",
            "volitelny_komentar": "null",
        },
        "cytokinova_terapie": {
            "datum_zahajeni": "null",
            "datum_ukonceni": "null",
            "planovana_strategie": "null",
            "upresnena_strategie": "null",
            "rezim": "null",
            "volitelny_komentar": "null",
        },
        "jine_lecebne_modality_v_ramci_onkologicke_lecby": {
            "datum_zahajeni": "null",
            "datum_ukonceni": "null",
            "planovana_strategie": "null",
            "upresnena_strategie": "null",
            "jina_lecba": "null",
            "volitelny_komentar": "null",
        },
        "lecebna_odpoved": {
            "guideline_kriteria_pro_hodnoceni_lecebne_odpovedi": "kompletní remise"
        },
        "presetreni": {
            "datum_hodnoceni_lecebne_odpovedi": "2024-10-16",
            "hodnoceni_lecebne_odpoved": "CR",
            "progrese": "null",
            "volitelny_komentar": "null",
        },
        "zavazna_toxicita_onkologicke_lecby_relevantni_prosledujici_peci": {
            "nazev": "svalová slabost, průjmovitá stolice",
            "datum": "2023-06",
            "toxicita_asociovana_s_lecbou": "chemoterapií",
            "typ_toxicity": "chronická",
            "uprava_ad_integrum": "null",
            "hodnoceni_nasledujicich_lecby": "2_nasledky_asymptomaticke_diky_lecbe",
            "volitelny_komentar": "null",
            "pacient_zarazeny_do_intervencni_klinicke_studie": "null",
            "nazev_studie": "null",
            "typ_studie": "null",
            "rameno_studie": "null",
            "datum_zarazeni": "null",
            "datum_vyrazeni": "null",
        },
    },
    "dates": {
        "Diagnóza": "2023-03-22",
        "Chemoterapie start": "2023-03-28",
        "Chemoterapie konec": "2023-06-06",
        "Operace": "2023-09-08",
        "CT vyšetření": "2024-10-16",
    },
}


def main():
    """Print the sample text and response for testing."""
    if len(sys.argv) > 1 and sys.argv[1] == "text":
        print(SAMPLE_MEDICAL_TEXT)
    else:
        print(json.dumps(SAMPLE_RESPONSE, indent=2))


if __name__ == "__main__":
    main()
