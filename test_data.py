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
    "Modul A. Pacient: parametry vztahující se k pacientovi": {
        "PŘEDCHOZÍ ONKOLOGICKÉ ONEMOCNĚNÍ": {
            "Předchozí onkologické onemocnění": "ANO",
            "Onkologické nemocnění - DG": "Post-pubertální teratom varlete v terénu GCNIS",
            "Rok diagnózy": "2023",
            "Léčen(a) ve zdravotnickém zařízení (název)": "Není uvedeno",
            "Onemocnění/funkční stav - komentář": "C629",
        },
        "ALERGIE": {
            "Léková alergie": "údaj není k dispozici",
            "Specifikace (Léková alergie)": "Není uvedeno",
            "Alergie na jód/kontrastní látky": "údaj není k dispozici",
            "Specifikace (Alergie na jód/kontrastní látky)": "Není uvedeno",
            "Jiné alergie (např. potravinové, pyly, prach)": "údaj není k dispozici",
            "Specifikace (Jiné alergie)": "Není uvedeno",
        },
        "Antropometrické údaje": {
            "Datum měření": "Není uvedeno",
            "Výška": "Není uvedeno",
            "Hmotnost": "Není uvedeno",
            "BMI": "Není uvedeno",
            "BSA": "Není uvedeno",
        },
        "Performance status (ECOG)": {
            "Performance status (ECOG)": "0 - Plně aktivní, je schopen normální tělesné aktivity bez omezení"
        },
    },
    "MODUL B – Část B1, obecné parametry popisující onkologickou diagnózu (společné všem diagnózám)": {
        "Klasifikace nádoru": {
            "Pořadové číslo onkologické diagnózy pacienta": "1",
            "Datum stanovení definitivní diagnózy": "27.01.2023",
            "Diagnostická modalita": ["histologie", "zobrazovací vyšetření"],
            "Diagnóza slovně": "Postpubertální teratom varlete v terénu GCNIS, s nezralými okrsky s vyšší mitotickou aktivitou",
            "Kód MKN-10": "C629",
            "Lateralita": "vlevo",
            "Morfologie nádoru slovně": "Postpubertální teratom s nezralými okrsky",
            "Typ morfologie": "histologie",
            "Topografie": "C62.9",
            "Morfologie kombinovaně": "9080/3",
            "Morfologie": "9080/3",
            "Biologické chování nádoru": "3",
            "Grading (diferenciace nádoru) G": "Nezralé s vyšší mitotickou aktivitou",
            "Verze MKN-O": "MKN-O-3",
            "Slovní popis diagnózy, komentář": "Radikální orchiektomie byla provedena. Kryoprezervace také provedena.",
            "ORPHA kód": "Není uvedeno",
        },
        "Rozsah onemocnění (staging)": {
            "Klinická TNM klasifikace": {"cT": "T1", "četnost": "1", "cN": "N1?", "cM": "M0"},
            "Patologická TNM klasifikace": {
                "y": "Není uvedeno",
                "r": "Není uvedeno",
                "a": "Není uvedeno",
                "pT": "T1",
                "četnost": "1",
                "pN": "N1?",
                "p(sn)": "Není uvedeno",
                "počet pozitivních sentinel.uzlin": "Není uvedeno",
                "počet celkově vyšetřených sentinel.uzlin": "Není uvedeno",
                "počet pozitivních ostatních uzlin": "Není uvedeno",
                "počet celkově vyšetřených ostatních uzlin": "Není uvedeno",
                "pM": "M0",
                "Stádium": "Není uvedeno",
                "Lokalizace metastáz": [
                    "Ledviny (suspektní hypermetabolismus glukózy)",
                    "Retroperitoneální uzlina (suspektní viabilní neoplazie)",
                ],
                "Lokalizace metastáz - komentář": "Zvětšená retroperitoneální uzlina podezřelá na viabilní neoplazii, podobně jako hypermetabolizmus v pravé ledvině.",
                "Lymfatická invaze (L)": "Není uvedeno",
                "Žilní invaze (V)": "Není uvedeno",
                "Pn - Perineurální invaze": "X",
                "R - Klasifikace": "RX přítomnost reziduálního nádoru nelze hodnotit",
                "Staging - doplňující informace": "Nutné dovyšetření dle MDT doporučení (cílené 3-fázové CT ledvin).",
            },
        },
        "Diagnostická skupina": {
            "Výběr diagnostické skupiny": "Germinální nádory pohlavních orgánů"
        },
    },
    "MODUL C – Souhrn provedené onkologické léčby v KOC, odpověď na léčbu a relevantní toxicita": {
        "Léčba": {"Datum zahájení léčby": "27.01.2023"},
        "Chirurgická léčba": {
            "Datum operace": "27.01.2023",
            "Indikace operačního výkonu": "onkologická",
            "Strategie onkologické operace": "kurativní",
            "Pořadí onkol.operace": "primární",
            "Operační přístup": "otevřený",
            "Konverze": "Není k dispozici",
            "Typ výkonu - primární nádor": "radikální resekce orgánu",
            "Radikální resekce - nádory CNS": "Není uvedeno",
            "Makroskopické rezidum nádoru (R2)": "Nehodnoceno",
            "Typ výkonu - regionální uzliny (výsledný stav)": "Není uvedeno",
            "Metastazektomie - vzdálené metastázy": "Není uvedeno",
            "Metastazektomie - Lokalizace vzdálených metastáz": [
                "retroperitoneální uzlina vlevo paraaortálně",
                "pravá ledvina (kraniální část)",
            ],
            "Jiný orgán": "Není uvedeno",
            "Speciální metoda": "NE",
            "Speciální metoda - specifikace": "Není uvedeno",
            "Speciální metoda - jiné": "Není uvedeno",
            "Volitelný komentář": "Není uvedeno",
        },
        "CHEMOTERAPIE": {
            "Datum zahájení": "Není uvedeno",
            "Datum ukončení": "Není uvedeno",
            "Plánovaná strategie": "Není uvedeno",
            "Upřesnění strategie": "Není uvedeno",
            "Režim": "Není uvedeno",
            "Podané léčivo": "Není uvedeno",
            "Byla překročena kumulativní dávka?": "údaj není k dispozici",
            "Volitelný komentář": "Není uvedeno",
        },
        "RADIOTERAPIE": {
            "Datum zahájení": "Není uvedeno",
            "Datum ukončení": "Není uvedeno",
            "Plánovaná strategie": "Není uvedeno",
            "Upřesnění strategie": "Není uvedeno",
            "Konkomitantní strategie": "údaj není k dispozici",
            "Zevní radioterapie": "údaj není k dispozici",
            "Typ zevní RT": "Není uvedeno",
            "Brachyterapie": "údaj není k dispozici",
            "Cílový objem": "Není uvedeno",
            "Počet frakcí": "Není uvedeno",
            "Celková dávka (Gy)": "Není uvedeno",
            "Ozáření vulnerabilních orgánů": "Není uvedeno",
            "Radioterapeutické centrum": "Není uvedeno",
            "Volitelný komentář": "Není uvedeno",
        },
        "CÍLENÁ LÉČBA": {
            "Datum zahájení": "Není uvedeno",
            "Datum ukončení": "Není uvedeno",
            "Plánovaná strategie": "Není uvedeno",
            "Upřesnění strategie": "Není uvedeno",
            "Režim": "Není uvedeno",
            "Podané léčivo": "Není uvedeno",
            "Volitelný komentář": "Není uvedeno",
        },
        "HORMONOTERAPIE": {
            "Datum zahájení": "Není uvedeno",
            "Datum ukončení": "Není uvedeno",
            "Plánovaná strategie": "Není uvedeno",
            "Upřesnění strategie": "Není uvedeno",
            "Režim": "Není uvedeno",
            "Podané léčivo": "Není uvedeno",
            "Volitelný komentář": "Není uvedeno",
        },
        "IMUNOTERAPIE": {
            "Datum zahájení": "Není uvedeno",
            "Datum ukončení": "Není uvedeno",
            "Plánovaná strategie": "Není uvedeno",
            "Upřesnění strategie": "Není uvedeno",
            "Režim": "Není uvedeno",
            "Podané léčivo": "Není uvedeno",
            "Volitelný komentář": "Není uvedeno",
        },
        "Léčebná odpověď": {
            "Guideline/kritéria pro hodnocení léčebné odpovědi": "Není uvedeno",
            "Datum hodnocení léčebné odpovědi": "Není uvedeno",
            "Hodnocená léčebná odpověď": "Není uvedeno",
            "Progrese": "Není uvedeno",
            "Volitelný komentář": "Plánované MDT vyšetření na strategii RPLND a další CT vyšetření ledvin.",
        },
    },
    "dates": {
        "admission": "2022-09-15",
        "asdf": "2023-01-31",
        "discharge": "2023-05-20",
        "sadfa": "2023-08-12",
        "followUp": "2023-12-05",
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
