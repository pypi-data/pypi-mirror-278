import pandas as pd
import requests

from classy import config
from classy import index
from classy.utils.logging import logger
from classy import utils

# ------
# Module definitions
IN_DEVOGELE2019 = {
    "1999 SH10",
    "2004 VJ1",
    "2007 MK6",
    "2008 EZ5",
    "2008 HA2",
    "2009 CP5",
    "2010 CE55",
    "2010 CF19",
    "2011 BN24",
    "2012 CO46",
    "2013 BO76",
    "2013 PC7",
    "2013 PH10",
    "2013 PJ10",
    "2013 SR",
    "2013 VY13",
    "2013 WA44",
    "2013 WS43",
    "2013 XV8",
    "2014 DF80",
    "2014 FA7",
    "2014 FB44",
    "2014 FN33",
    "2014 FP47",
    "2014 GG49",
    "2014 HE177",
    "2014 HK129",
    "2014 HS4",
    "2014 HT46",
    "2014 JD",
    "2014 JJ55",
    "2014 MD6",
    "2014 OT338",
    "2014 RC",
    "2014 RF11",
    "2014 SB145",
    "2014 SF304",
    "2014 SO142",
    "2014 SU1",
    "2014 TP57",
    "2014 TR57",
    "2014 UC115",
    "2014 UV210",
    "2014 VG2",
    "2014 WC201",
    "2014 WE120",
    "2014 WE121",
    "2014 WF201",
    "2014 WO69",
    "2014 WP4",
    "2014 WR6",
    "2014 WS7",
    "2014 WX202",
    "2014 WX4",
    "2014 WY119",
    "2014 YD",
    "2014 YD42",
    "2014 YN",
    "2014 YT34",
    "2014 YZ8",
    "2015 AK1",
    "2015 AZ43",
    "2015 BF511",
    "2015 BK4",
    "2015 BM510",
    "2015 CF",
    "2015 CQ13",
    "2015 CW13",
    "2015 CZ12",
    "2015 DC54",
    "2015 DK200",
    "2015 DO215",
    "2015 DP53",
    "2015 DS",
    "2015 DS53",
    "2015 DU",
    "2015 DZ198",
    "2015 EE7",
    "2015 EF",
    "2015 EK",
    "2015 FC",
    "2015 FP",
    "2015 FW33",
    "2015 FX33",
    "2015 HS11",
    "2015 HV11",
    "2015 JF",
    "2015 JR",
    "2015 JW",
    "2015 KA",
    "2015 KE",
    "2015 LQ21",
    "2015 MC",
    "2015 NA14",
    "2015 OM21",
    "2015 OQ21",
    "2015 PK9",
    "2015 QB",
    "2015 SA",
    "2015 TD144",
    "2015 TL238",
    "2015 TM143",
    "2015 TW237",
    "2015 TZ143",
    "2015 TZ237",
    "2015 VA106",
    "2015 VE66",
    "2015 VG105",
    "2015 VN105",
    "2015 VO105",
    "2015 VO142",
    "2015 WA13",
    "2015 XB",
    "2015 XE",
    "2015 XM128",
    "2015 XO",
    "2015 YD",
    "2015 YD1",
    "2015 YE",
    "2015 YS9",
    "2016 BB15",
    "2016 BC15",
    "2016 BJ15",
    "2016 BW14",
    "2016 CF29",
    "2016 CG18",
    "2016 CK29",
    "2016 CL29",
    "2016 CO29",
    "2016 CS247",
    "2016 CU29",
    "2016 EB1",
    "2016 EB28",
    "2016 EL157",
    "2016 EN156",
    "2016 EQ1",
    "2016 ES1",
    "2016 FC",
    "2016 FL12",
    "2016 FW13",
    "2016 GB222",
    "2016 GV221",
    "2016 HB",
    "2016 HN2",
    "2016 HQ19",
    "2016 JV",
    "2016 LG49",
    "2016 LO48",
    "2016 NC1",
    "2016 ND1",
    "2016 NM15",
    "2016 NN15",
    "2016 NS",
    "2016 PX8",
    "2016 QB2",
    "2016 QL44",
    "2016 QS11",
    "2016 RB1",
    "2016 RD20",
    "2016 RD34",
    "2016 RF34",
    "2016 RJ18",
    "2016 RL20",
    "2016 RM20",
    "2016 RT33",
    "2016 RW",
    "2016 SA2",
    "2016 SW1",
    "2016 SZ1",
    "2016 TB57",
    "2016 TM56",
    "2016 XR23",
    "2016 YC8",
    "2016 YH3",
    "2016 YM3",
    "2017 AR4",
    "2017 AS4",
    "2017 AT4",
    "2017 BK",
    "2017 BT",
    "2017 BU",
    "2017 BW",
    "2017 CS",
    "2017 EH4",
    "2017 FJ",
    "2017 FK",
    "2017 JM2",
    "2017 QB35",
    "2017 QG18",
    "2017 QR35",
    "2017 RB",
    "2017 RB16",
    "2017 RS2",
    "2017 RU2",
    "2017 RV2",
    "2017 VA15",
    "2017 VC14",
    "2017 VG1",
    "2017 VR12",
    "2017 VV12",
    "2017 VY13",
    "2017 VZ14",
    "2017 YF7",
    "2017 YR3",
    "2017 YW3",
    "2018 AF3",
    "2018 BG1",
    "2018 DT",
    "2018 DY3",
    "2018 EH",
}

PATH = config.PATH_DATA / "manos"

DATA_KWARGS = {
    "delimiter": r",",
    "names": ["wave", "refl", "refl_err", "flag_err"],
}


# ------
# Module functions
def _retrieve_spectra():
    """Download all MANOS spectra to cache."""
    PATH.mkdir(parents=True, exist_ok=True)

    # Download MANOS index
    URL = "https://manos.lowell.edu/api/v1/observations/statuses"
    response = requests.get(URL)
    response = response.json()

    for i, entry in enumerate(response):
        for spec in ["vis_spectrum", "nir_spectrum"]:
            if entry[spec]["exists"]:
                response[i][f"url_{spec}"] = entry[spec]["products"]["data"]
            else:
                response[i][f"url_{spec}"] = None
            response[i].pop(spec)
    index = pd.DataFrame(response)
    specs = index[
        (index["url_nir_spectrum"].notnull()) | (index["url_vis_spectrum"].notnull())
    ]

    for name in IN_DEVOGELE2019:
        if name not in specs["primary_designation"].values:
            print(name)

    for name in specs["primary_designation"].values:
        if name not in IN_DEVOGELE2019:
            print(name, "not in IN_DEVOGELE2019")
    breakpoint()


def _build_index():
    """Add the AKARI spectra to the classy spectra index."""

    # Catch if download failed
    if not (PATH / "AcuA_1.0/target.txt").is_file():
        return

    # Create index based on target file
    entries = pd.read_csv(
        PATH / "AcuA_1.0/target.txt",
        delimiter=r"\s+",
        names=["number", "name", "obs_id", "date", "ra", "dec"],
        dtype={"number": int},
    )
    entries = entries.drop_duplicates("number")

    # Drop (4) Vesta and (4015) Wilson-Harrington as there are no spectra of them
    entries = entries[~entries.number.isin([4, 4015])]

    # Add filenames
    entries["filename"] = entries.apply(
        lambda row: f"akari/AcuA_1.0/reflectance/{row.number:>04}_{row['name']}.txt",
        axis=1,
    )

    entries["shortbib"] = SHORTBIB
    entries["bibcode"] = BIBCODE
    entries["date_obs"] = entries.date
    entries["source"] = "AKARI"
    entries["host"] = "AKARI"
    entries["module"] = "akari"

    # Et voila
    index.add(entries)


def _transform_data(_, data):
    # Add a joint flag, it's 1 if any other flag is 1
    data["flag"] = data.apply(
        lambda point: 1
        if any(
            bool(point[flag])
            for flag in ["flag_err", "flag_saturation", "flag_thermal", "flag_stellar"]
        )
        else 0,
        axis=1,
    )

    # No metadata to record
    meta = {}
    return data, meta
