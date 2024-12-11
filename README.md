# 🌩️ **EAS2Text**: Comprehensive EAS Header-to-Text Translation Library

![EAS2Text](https://github.com/Newton-Communications/E2T/blob/nwr-localities/doc/img/TRxT7n.jpg)

EAS2Text is a powerful Python library for translating **EAS (Emergency Alert System)** headers into human-readable text. It includes robust support for weather alerts, FIPS codes, emulation modes, and Canadian regions, ensuring a seamless experience for decoding emergency messages.

---

## 🛠️ **Features**

- ✅ **EAS to Text Translation**: Converts raw ZCZC SAME strings into clear, readable text.
- ✅ **EAS EOM Detection**: Seamlessly detects End-of-Message headers.
- ✅ **Error Handling**: Handles unknown callsigns, originators, and FIPS codes.
- ✅ **Detailed Output**: Provides raw and parsed outputs for advanced use.
- ✅ **Weather Forecast Office (WFO) Detection**: Supports overlap detection and marine localities.
- ✅ **Emulation Modes**: Mimic outputs of various EAS hardware/software systems.
- ✅ **Canadian Forecast Regions**: Full support for Canadian alerts and regions.

---

## 🚀 **Installation**

### Linux (Debian-based)
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 -m pip install https://github.com/Newton-Communications/E2T/archive/refs/heads/nwr-localities.zip
```

### Windows
1. [Install Python](https://www.python.org/downloads/).
2. Open CMD and run:
   ```bash
   python -m pip install https://github.com/Newton-Communications/E2T/archive/refs/heads/nwr-localities.zip
   ```

---

## 📖 **Basic Usage**

### Translate a Raw SAME String
```python
from EAS2Text import EAS2Text

data = EAS2Text("ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-EAR/FOLF-")
print(f"{data.EASText}")
```

<details>
<summary>Output</summary>

```
The National Weather Service in Baltimore/Washington, D.C. (LWX); and Philadelphia/Mt Holly, NJ (PHI); has issued a Special Weather Statement for Allegany County, MD; Baltimore County, MD; Carroll County, MD; Frederick County, MD; Harford County, MD; Washington County, MD; Frederick County, VA; City of Winchester, VA; Berkeley County, WV; Hampshire County, WV; Jefferson County, WV; Mineral County, WV; and Morgan County, WV; beginning at 02:29 PM and ending at 08:29 PM. Message from EAR/FOLF.
```
</details>

---

## 🔍 **Advanced Usage**

### Extract All Data Components
```python
from EAS2Text import EAS2Text

oof = EAS2Text("ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-EAR/FOLF-")

## RAW Data output
print(f"RAW Data: {oof.EASData}") ## Input Data
print(f"RAW ORG: {oof.org}") ## Raw Originator Code: ZCZC-{ORG}-EVN-PSSCCC-PSSCCC+TTTT-JJJHHMM-CCCCCCCC-
print(f"RAW WFO: {oof.WFO}") ## Raw WFO Code(s) in a list: ZCZC-ORG-EVN-{PSSCCC-PSSCCC}+TTTT-JJJHHMM-CCCCCCCC-
print(f"RAW EVNT: {oof.evnt}") ## Raw Event Code: ZCZC-ORG-{EVN}-PSSCCC-PSSCCC+TTTT-JJJHHMM-CCCCCCCC-
print(f"RAW FIPS: {oof.FIPS}")  ## Raw FIPS Code(s) in a list: ZCZC-ORG-EVN-{PSSCCC-PSSCCC}+TTTT-JJJHHMM-CCCCCCCC-
print(f"Purge Time: {oof.purge}") ## Purge Time in a list format of HH, MM: ZCZC-ORG-EVN-PSSCCC-PSSCCC+{TTTT}-JJJHHMM-CCCCCCCC-
print(f"RAW TIMESTAMP: {oof.timeStamp}") ## RAW Timestamp: ZCZC-ORG-EVN-PSSCCC-PSSCCC+TTTT-{JJJHHMM}-CCCCCCCC-
print(f"RAW Callsign: {oof.callsign}") ## Input Callsign

## Semi-RAW Data
print(f"Start Time: {oof.startTime}") ## A Datetime.Datetime object of the Start Time (Local Timezone)
print(f"End Time: {oof.endTime}") ## A Datetime.Datetime object of the End Time (Local Timezone)

## Parsed Data Output
print(f"TEXT ORG: {oof.orgText}") ## A Human-Readable Version of ORG
print(f"TEXT WFO: {oof.WFOText}") ## A List of All WFOs
print(f"TEXT EVNT: {oof.evntText}") ## A Human Readable Version of EVN
print(f"TEXT FIPS: {oof.FIPSText}") ## A List of All FIPS County Names (Returns "FIPS Code PSSCCC" if no available county)
print(f"TEXT Start Time: {oof.startTimeText}") ## A Start-Time Tag in the format of "HH:MM AM/PM MONTH_NAME DD, YYYY"
print(f"TEXT End Time: {oof.endTimeText}") ## A End-Time Tag in the format of "HH:MM AM/PM MONTH_NAME DD, YYYY"
print(f"{oof.EASText}") ## The full EAS Output data
```

<details>
<summary>Output</summary>

```
RAW Data: ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-EAR/FOLF-
RAW ORG: WXR
RAW WFO: Baltimore, MD/Washington, D.C. (LWX);
RAW EVNT: SPS
RAW FIPS: ['024043', '024021', '024013', '024005', '024001', '024025', '051840', '051069', '054027', '054065', '054003', '054037', '054057']
Purge Time: ['06', '00']
RAW TIMESTAMP: 0231829
RAW Callsign: EAR/FOLF
Start Time: 2024-01-23 14:29:00
End Time: 2024-01-23 20:29:00
TEXT ORG: The National Weather Service in Baltimore, MD/Washington, D.C. (LWX);
TEXT WFO: Baltimore, MD/Washington, D.C. (LWX);
TEXT EVNT: a Special Weather Statement
TEXT FIPS: ['Allegany County, MD', 'Baltimore County, MD', 'Carroll County, MD', 'Frederick County, MD', 'Harford County, MD', 'Washington County, MD', 'Frederick County, VA', 'City of Winchester, VA', 'Berkeley County, WV', 'Hampshire County, WV', 'Jefferson County, WV', 'Mineral County, WV', 'and Morgan County, WV']
TEXT Start Time: 02:29 PM
TEXT End Time: 08:29 PM
The National Weather Service in Baltimore, MD/Washington, D.C. (LWX); has issued a Special Weather Statement for Allegany County, MD; Baltimore County, MD; Carroll County, MD; Frederick County, MD; Harford County, MD; Washington County, MD; Frederick County, VA; City of Winchester, VA; Berkeley County, WV; Hampshire County, WV; Jefferson County, WV; Mineral County, WV; and Morgan County, WV; beginning at 02:29 PM and ending at 08:29 PM. Message from EAR/FOLF.
```
</details>

---

## 🌟 **Emulation Modes**

EAS2Text supports various emulation modes to mimic specific EAS hardware/software outputs:

| **Mode** | **Mode Triggers**                                   | **Sample EASText Output**                                                                                                                                                                                                                                                                                                                                                                  | **Emulated Hardware/Software**                                                                                          | **Known Issues/Bugs**         |
|----------|----------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|--------------------------------|
| **1**    | TFT                                                | THE NATIONAL WEATHER SERVICE HAS ISSUED A SPECIAL WEATHER STATEMENT FOR THE FOLLOWING COUNTIES/AREAS: ALLEGANY COUNTY MD, BALTIMORE COUNTY MD, CARROLL COUNTY MD, FREDERICK COUNTY MD, HARFORD COUNTY MD, WASHINGTON COUNTY MD, FREDERICK COUNTY VA, CITY OF WINCHESTER VA, BERKELEY COUNTY WV, HAMPSHIRE COUNTY WV, JEFFERSON COUNTY WV, MINERAL COUNTY WV, AND MORGAN COUNTY WV AT 06:29 PM ON JAN 22, 2024 EFFECTIVE UNTIL 12:29 AM ON JAN 23, 2024. MESSAGE FROM EAR/FOLF. | TFT EAS 911, TFT EAS 911D                                                                                             | None currently reported        |
| **2**    | SAGE, SAGE 1822, SAGE DIGITAL, SAGE EAS ENDEC      | The National Weather Service has issued a Special Weather Statement for Allegany County, MD, Baltimore County, MD, Carroll County, MD, Frederick County, MD, Harford County, MD, Washington County, MD, Frederick County, VA, City of Winchester, VA, Berkeley County, WV, Hampshire County, WV, Jefferson County, WV, Mineral County, WV, and Morgan County, WV beginning at 06:29 pm Mon Jan 22 and ending at 12:29 am Tue Jan 23 (EAR/FOLF)       | SAGE 1822 EAS ENDEC Firmware v5.9+, SAGE 3644 DIGITAL EAS ENDEC                                                          | None currently reported        |
| **3**    | TRILITHIC, VIAVI, EASY                             | The National Weather Service has issued a Special Weather Statement for the following counties: Allegany MD - Baltimore MD - Carroll MD - Frederick MD - Harford MD - Washington MD - Frederick VA - Winchester (city) VA - Berkeley WV - Hampshire WV - Jefferson WV - Mineral WV - Morgan WV. Effective Until 01/23/24 00:29:00 UTC. (EAR/FOLF)                                                                                     | EASyIP, EASyIPTV, EASyCAP, VIAVI EAS product line, TRILITHIC EAS product line                                           | None currently reported        |
| **4**    | BURK                                               | The National Weather Service has issued SPECIAL WEATHER STATEMENT for the following counties/areas: Allegany County MD, Baltimore County MD, Carroll County MD, Frederick County MD, Harford County MD, Washington County MD, Frederick County VA, City of Winchester VA, Berkeley County WV, Hampshire County WV, Jefferson County WV, Mineral County WV, and Morgan County WV on JANUARY 22, 2024 at 06:29 PM effective until 12:29 AM, January 23, 2024.          | BURK EAS product line                                                                                                  | None currently reported        |
| **5**    | DAS, DASDEC, MONROE, ONENET, ONENET SE             | THE NATIONAL WEATHER SERVICE HAS ISSUED A SPECIAL WEATHER STATEMENT FOR THE FOLLOWING COUNTIES/AREAS: ALLEGANY; BALTIMORE; CARROLL; FREDERICK; HARFORD; WASHINGTON, MD; FREDERICK; WINCHESTER (CITY), VA; BERKELEY; HAMPSHIRE; JEFFERSON; MINERAL; MORGAN, WV; AT 06:29 PM ON JAN 22, 2024 EFFECTIVE UNTIL 12:29 AM JAN 23, 2024. MESSAGE FROM EAR/FOLF.                                                                                  | Digital Alert Systems DASDEC I/II units and all Monroe Electronics OneNet units Software Versions <=2.9                | None currently reported        |
| **6**    | DASV3, DASDECV3, MONROEV3, ONENETV3, ONENET SEV3   | The National Weather Service has issued A SPECIAL WEATHER STATEMENT for the following counties/areas: Allegany; Baltimore; Carroll; Frederick; Harford; Washington, MD; Frederick; Winchester (city), VA; Berkeley; Hampshire; Jefferson; Mineral; Morgan, WV; at 6:29 PM ON JAN 22, 2024 effective until 12:29 AM JAN 23, 2024. Message from EAR/FOLF.                                                                                 | Digital Alert Systems DASDEC I/II units and all Monroe Electronics OneNet units Software Versions <=3.0                | None currently reported        |
| **7**    | HollyAnne, Holly Anne, Holly-Anne, HU-961, MIP-921, MIP-921e, HU961, MIP921, MIP921e | THE NATIONAL WEATHER SERVICE HAS ISSUED A SPECIAL WEATHER STATEMENT FOR THE FOLLOWING COUNTIES: ALLEGANY MD, BALTIMORE MD, CARROLL MD, FREDERICK MD, HARFORD MD, WASHINGTON MD, FREDERICK VA, WINCHESTER CITY VA, BERKELEY WV, HAMPSHIRE WV, JEFFERSON WV, MINERAL WV AND MORGAN WV BEGINNING AT 06:29 PM JANUARY 22 AND ENDING AT 12:29 AM JANUARY 23. MESSAGE FROM EAR/FOLF.                                                                                   | HollyAnne EAS product line                                                                                              | None currently reported        |
| **8**    | EAS1CG, EAS-1, EAS1, EAS1-CG, EAS-1CG, Gorman-Redlich, GormanRedlich, Gorman Redlich | A SPECIAL WEATHER STATEMENT HAS BEEN ISSUED FOR ALLEGANY MD, BALTIMORE MD, CARROLL MD, FREDERICK MD, HARFORD MD, WASHINGTON MD, FREDERICK VA, WINCHESTER CITY VA, BERKELEY WV, HAMPSHIRE WV, JEFFERSON WV, MINERAL WV AND MORGAN WV AT 6:29 PM ON JANUARY 22, 2024 EFFECTIVE UNTIL 12:29 AM ON JANUARY 23, 2024. MESSAGE FROM EAR/FOLF.                                                                                         | Gorman Redlich EAS product line                                                                                        | None currently reported        |

---

### **Example: SAGE Emulation**
```python
from EAS2Text import EAS2Text

oof = EAS2Text(sameData = "ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-EAR/FOLF-", mode="SAGE EAS") ## Emulates a SAGE EAS ENDEC

print(f"{oof.EASText}") ## The full EAS Output data, 1822 style
```

<details>
<summary>Output</summary>

```
The National Weather Service has issued a Special Weather Statement for Allegany County, MD, Baltimore County, MD, Carroll County, MD, Frederick County, MD, Harford County, MD, Washington County, MD, Frederick County, VA, City of Winchester, VA, Berkeley County, WV, Hampshire County, WV, Jefferson County, WV, Mineral County, WV, and Morgan County, WV beginning at 02:29 pm and ending at 08:29 pm (EAR/FOLF)
```
</details>

---

## 🇨🇦 **Canadian Forecast Regions**

Enable Canadian mode to decode Canadian FIPS codes:

```python
from EAS2Text import EAS2Text

oof = EAS2Text("ZCZC-WXR-HWW-090000-098110+0100-2641926-EC/GC/CA-", canada=True) ## Enabled Canadian Mode

## RAW Data output
print(f"RAW Data: {oof.EASData}") ## Input Data
print(f"RAW ORG: {oof.org}") ## Raw Originator Code: ZCZC-{ORG}-EVN-PSSCCC-PSSCCC+TTTT-JJJHHMM-CCCCCCCC-
print(f"RAW EVNT: {oof.evnt}") ## Raw Event Code: ZCZC-ORG-{EVN}-PSSCCC-PSSCCC+TTTT-JJJHHMM-CCCCCCCC-
print(f"RAW FIPS: {oof.FIPS}")  ## Raw FIPS Code(s) in a list: ZCZC-ORG-EVN-{PSSCCC-PSSCCC}+TTTT-JJJHHMM-CCCCCCCC-
print(f"Purge Time: {oof.purge}") ## Purge Time in a list format of HH, MM: ZCZC-ORG-EVN-PSSCCC-PSSCCC+{TTTT}-JJJHHMM-CCCCCCCC-
print(f"RAW TIMESTAMP: {oof.timeStamp}") ## RAW Timestamp: ZCZC-ORG-EVN-PSSCCC-PSSCCC+TTTT-{JJJHHMM}-CCCCCCCC-
print(f"RAW Callsign: {oof.callsign}") ## Input Callsign

## Semi-RAW Data
print(f"Start Time: {oof.startTime}") ## A Datetime.Datetime object of the Start Time (Local Timezone)
print(f"End Time: {oof.endTime}") ## A Datetime.Datetime object of the End Time (Local Timezone)

## Parsed Data Output
print(f"TEXT ORG: {oof.orgText}") ## A Human-Readable Version of ORG
print(f"TEXT EVNT: {oof.evntText}") ## A Human Readable Version of EVN
print(f"TEXT FIPS: {oof.FIPSText}") ## A List of All FIPS County Names (Returns "FIPS Code PSSCCC" if no available county)
print(f"TEXT Start Time: {oof.startTimeText}") ## A Start-Time Tag in the format of "HH:MM AM/PM MONTH_NAME DD, YYYY"
print(f"TEXT End Time: {oof.endTimeText}") ## A End-Time Tag in the format of "HH:MM AM/PM MONTH_NAME DD, YYYY"
print(f"{oof.EASText}") ## The full EAS Output data
```

<details>
<summary>Output</summary>

```
RAW Data: ZCZC-WXR-HWW-090000-098110+0100-2641926-EC/GC/CA-
RAW ORG: WXR
RAW EVNT: HWW
RAW FIPS: ['090000', '098110']
Purge Time: ['01', '00']
RAW TIMESTAMP: 2641926
RAW Callsign: EC/GC/CA
Start Time: 2024-09-21 15:26:00
End Time: 2024-09-21 16:26:00
TEXT ORG: Environment Canada
TEXT EVNT: a High Wind Warning
TEXT FIPS: ['All of Yukon/Northwest Territories/Nunavut', 'and Arctic Bay, NU']
TEXT Start Time: 03:26 PM
TEXT End Time: 04:26 PM
Environment Canada has issued a High Wind Warning for All of Yukon/Northwest Territories/Nunavut; and Arctic Bay, NU; beginning at 03:26 PM and ending at 04:26 PM. Message from EC/GC/CA.
```
</details>

---

## 📝📋 **List Mode**

List mode allows for the listing of data that the script uses in order to help with development of external software.

```python
from EAS2Text import EAS2Text

oof = EAS2Text(listMode=True)

print(f"Org List: {oof.orgList}") ## A list of all available originator codes
print(f"Event List: {oof.evntList}") ## A list of all available event codes
print(f"Subdivision List: {oof.subdivList}") ## A list of all available subdivision codes
print(f"FIPS Code List: {oof.fipsList}") ## A list of all available SAME FIPS codes
```

<details>
<summary>Output</summary>

```
Org List: {'PEP': 'A Primary Entry Point System'...}
Event List: {'BZW': 'a Blizzard Warning'...}
Subdivision List: {'0': '', '1': 'Northwest'...}
FIPS Code List: {'10000': 'State of Delaware'...}
```
</details>

---

## 🕒 **Timezone Support**

Timezones can be specified, both in UTC offset and in TZ timezone format. [List of tz database time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
**Warning:** The library will break if an invalid timezone is specified.

### UTC Offset Example
```python
from EAS2Text import EAS2Text

oof = EAS2Text(sameData = "ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-EAR/FOLF-", timeZone=-6) ## Uses a UTC-6 Offset

print(f"{oof.EASText}") ## The full EAS Output data, with a UTC-6 Offset.
```

<details>
<summary>Output</summary>

```
The National Weather Service in Baltimore, MD/Washington, D.C. (LWX); has issued a Special Weather Statement for Allegany County, MD; Baltimore County, MD; Carroll County, MD; Frederick County, MD; Harford County, MD; Washington County, MD; Frederick County, VA; City of Winchester, VA; Berkeley County, WV; Hampshire County, WV; Jefferson County, WV; Mineral County, WV; and Morgan County, WV; beginning at 12:29 PM and ending at 06:29 PM. Message from EAR/FOLF.
```
</details>

---

### TZ Database Example
```python
from EAS2Text import EAS2Text

oof = EAS2Text(sameData = "ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-EAR/FOLF-", timeZoneTZ="Europe/Berlin") ## Uses Europe/Berlin time.

print(f"{oof.EASText}") ## The full EAS Output data, in Europe/Berlin time.
```

<details>
<summary>Output</summary>

```
The National Weather Service in Baltimore, MD/Washington, D.C. (LWX); has issued a Special Weather Statement for Allegany County, MD; Baltimore County, MD; Carroll County, MD; Frederick County, MD; Harford County, MD; Washington County, MD; Frederick County, VA; City of Winchester, VA; Berkeley County, WV; Hampshire County, WV; Jefferson County, WV; Mineral County, WV; and Morgan County, WV; beginning at 08:29 PM January 23 and ending at 02:29 AM January 24. Message from EAR/FOLF.
```
</details>

---

## 📊 Opt-in to Advanced Weather Forecasting Office Data
**Warning:** Some data in this particular dataset is inaccurate.

```python
from EAS2Text import EAS2Text

oof = EAS2Text("ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-EAR/FOLF-", newWFO=True)


## RAW Data output
print(f"RAW Data: {oof.EASData}") ## Input Data
print(f"RAW ORG: {oof.org}") ## Raw Originator Code: ZCZC-{ORG}-EVN-PSSCCC-PSSCCC+TTTT-JJJHHMM-CCCCCCCC-
print(f"RAW WFO: {oof.WFO}") ## Raw WFO Code(s) in a list: ZCZC-ORG-EVN-{PSSCCC-PSSCCC}+TTTT-JJJHHMM-CCCCCCCC-
print(f"RAW EVNT: {oof.evnt}") ## Raw Event Code: ZCZC-ORG-{EVN}-PSSCCC-PSSCCC+TTTT-JJJHHMM-CCCCCCCC-
print(f"RAW FIPS: {oof.FIPS}")  ## Raw FIPS Code(s) in a list: ZCZC-ORG-EVN-{PSSCCC-PSSCCC}+TTTT-JJJHHMM-CCCCCCCC-
print(f"Purge Time: {oof.purge}") ## Purge Time in a list format of HH, MM: ZCZC-ORG-EVN-PSSCCC-PSSCCC+{TTTT}-JJJHHMM-CCCCCCCC-
print(f"RAW TIMESTAMP: {oof.timeStamp}") ## RAW Timestamp: ZCZC-ORG-EVN-PSSCCC-PSSCCC+TTTT-{JJJHHMM}-CCCCCCCC-
print(f"RAW Callsign: {oof.callsign}") ## Input Callsign

## Semi-RAW Data
print(f"Start Time: {oof.startTime}") ## A Datetime.Datetime object of the Start Time (Local Timezone)
print(f"End Time: {oof.endTime}") ## A Datetime.Datetime object of the End Time (Local Timezone)

## Parsed Data Output
print(f"TEXT ORG: {oof.orgText}") ## A Human-Readable Version of ORG
print(f"TEXT WFO: {oof.WFOText}") ## A List of All WFOs
print(f"TEXT WFO FORECAST OFFICE: {oof.WFOForecastOffice}") # A List of All WFO Forecast Offices
print(f"TEXT WFO ADDRESS: {oof.WFOAddress}") # A List of All WFO Addresses
print(f"TEXT WFO CALLSIGN: {oof.WFOCallsign}") # A List of All WFO Callsigns
print(f"TEXT WFO PHONE NUMBER: {oof.WFOPhoneNumber}") # A List of All WFO Phone Numbers
print(f"TEXT NWR FREQ: {oof.NWR_FREQ}") # A List of All NWR Frequencies
print(f"TEXT NWR CALLSIGN: {oof.NWR_CALLSIGN}") # A List of All NWR Callsigns
print(f"TEXT NWR PWR: {oof.NWR_PWR}") # A List of All NWR Powers
print(f"TEXT NWR SITE NAME: {oof.NWR_SITENAME}") # A List of All NWR Site Names
print(f"TEXT NWR SITE LOC: {oof.NWR_SITELOC}") # A List of All NWR Site Locations
print(f"TEXT NWR SITE STATE: {oof.NWR_SITESTATE}") # A List of All NWR Site States
print(f"TEXT NWR SITE: {oof.NWR_SITE}") # A List of All NWR Sites
print(f"TEXT NWR COORDINATES: {oof.NWR_COORDINATES}") # A List of All NWR Site Coordinates

print(f"TEXT EVNT: {oof.evntText}") ## A Human Readable Version of EVN
print(f"TEXT FIPS: {oof.FIPSText}") ## A List of All FIPS County Names (Returns "FIPS Code PSSCCC" if no available county)
print(f"TEXT Start Time: {oof.startTimeText}") ## A Start-Time Tag in the format of "HH:MM AM/PM MONTH_NAME DD, YYYY"
print(f"TEXT End Time: {oof.endTimeText}") ## A End-Time Tag in the format of "HH:MM AM/PM MONTH_NAME DD, YYYY"
print(f"{oof.EASText}") ## The full EAS Output dataBumped version to 0.1.14.0 and added autoupdating json lists to prevent the need to constantly update the script in the future.
```

<details>
<summary>Output</summary>

```
RAW Data: ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-EAR/FOLF-
RAW ORG: WXR
RAW WFO: Baltimore/Washington, D.C. (LWX); and Philadelphia/Mt Holly, NJ (PHI);
RAW EVNT: SPS
RAW FIPS: ['024043', '024021', '024013', '024005', '024001', '024025', '051840', '051069', '054027', '054065', '054003', '054037', '054057']
Purge Time: ['06', '00']
RAW TIMESTAMP: 0231829
RAW Callsign: EAR/FOLF
Start Time: 2024-01-23 14:29:00
End Time: 2024-01-23 20:29:00
TEXT ORG: The National Weather Service in Baltimore/Washington, D.C. (LWX); and Philadelphia/Mt Holly, NJ (PHI);
TEXT WFO: Baltimore/Washington, D.C. (LWX); and Philadelphia/Mt Holly, NJ (PHI);
TEXT WFO FORECAST OFFICE: ['Baltimore/Washington', 'Baltimore/Washington', 'Philadelphia/Mt Holly', 'Baltimore/Washington', 'Baltimore/Washington', 'Baltimore/Washington', 'Philadelphia/Mt Holly', 'Baltimore/Washington', 'Baltimore/Washington', 'Baltimore/Washington', 'Baltimore/Washington', 'Baltimore/Washington', 'Baltimore/Washington', 'Baltimore/Washington', 'Baltimore/Washington']
TEXT WFO ADDRESS: ['43858 Weather Service Road, Sterling, VA 20166', '43858 Weather Service Road, Sterling, VA 20166', '732 Woodlane Rd, Mt Holly, NJ 08060', '43858 Weather Service Road, Sterling, VA 20166', '43858 Weather Service Road, Sterling, VA 20166', '43858 Weather Service Road, Sterling, VA 20166', '732 Woodlane Rd, Mt Holly, NJ 08060', '43858 Weather Service Road, Sterling, VA 20166', '43858 Weather Service Road, Sterling, VA 20166', '43858 Weather Service Road, Sterling, VA 20166', '43858 Weather Service Road, Sterling, VA 20166', '43858 Weather Service Road, Sterling, VA 20166', '43858 Weather Service Road, Sterling, VA 20166', '43858 Weather Service Road, Sterling, VA 20166', '43858 Weather Service Road, Sterling, VA 20166']
TEXT WFO CALLSIGN: ['LWX', 'LWX', 'PHI', 'LWX', 'LWX', 'LWX', 'PHI', 'LWX', 'LWX', 'LWX', 'LWX', 'LWX', 'LWX', 'LWX', 'LWX']
TEXT WFO PHONE NUMBER: ['703-996-2200', '703-996-2200', '609-261-6600', '703-996-2200', '703-996-2200', '703-996-2200', '609-261-6600', '703-996-2200', '703-996-2200', '703-996-2200', '703-996-2200', '703-996-2200', '703-996-2200', '703-996-2200', '703-996-2200']
TEXT NWR FREQ: ['162.425; 162.475; 162.400', '162.400; 162.500', '162.400; 162.500', '162.400; 162.475', '162.400; 162.475; 162.550', '162.400; 162.500', '162.400; 162.500', '162.425; 162.475', '162.475; 162.400', '162.475; 162.400', '162.475', '162.425; 162.475; 162.400', '162.475', '162.425; 162.475; 162.400', '162.425; 162.475; 162.400']
TEXT NWR CALLSIGN: ['WXM43; WXM42; WXM73', 'KEC83; WXK97', 'KEC83; WXK97', 'KEC83; WXM42', 'KEC83; WXM42; KHB36', 'KEC83; WXK97', 'KEC83; WXK97', 'WXM43; WXM42', 'WXM42; WXM73', 'WXM42; WXM73', 'WXM42', 'WXM43; WXM42; WXM73', 'WXM42', 'WXM43; WXM42; WXM73', 'WXM43; WXM42; WXM73']
TEXT NWR PWR: ['300; 1000; 500', '1000; 1000', '1000; 1000', '1000; 1000', '1000; 1000; 1000', '1000; 1000', '1000; 1000', '300; 1000', '1000; 500', '1000; 500', '1000', '300; 1000; 500', '1000', '300; 1000; 500', '300; 1000; 500']
TEXT NWR SITE NAME: ['Frostburg; Hagerstown; Moorefield', 'Baltimore; Sudlersville', 'Baltimore; Sudlersville', 'Baltimore; Hagerstown', 'Baltimore; Hagerstown; Manassas', 'Baltimore; Sudlersville', 'Baltimore; Sudlersville', 'Frostburg; Hagerstown', 'Hagerstown; Moorefield', 'Hagerstown; Moorefield', 'Hagerstown', 'Frostburg; Hagerstown; Moorefield', 'Hagerstown', 'Frostburg; Hagerstown; Moorefield', 'Frostburg; Hagerstown; Moorefield']
TEXT NWR SITE LOC: ['Midland (Frostburg); Clear Spring; Branch Mtn.', 'Pikesville; Sudlersville', 'Pikesville; Sudlersville', 'Pikesville; Clear Spring', 'Pikesville; Clear Spring; Independent Hill', 'Pikesville; Sudlersville', 'Pikesville; Sudlersville', 'Midland (Frostburg); Clear Spring', 'Clear Spring; Branch Mtn.', 'Clear Spring; Branch Mtn.', 'Clear Spring', 'Midland (Frostburg); Clear Spring; Branch Mtn.', 'Clear Spring', 'Midland (Frostburg); Clear Spring; Branch Mtn.', 'Midland (Frostburg); Clear Spring; Branch Mtn.']
TEXT NWR SITE STATE: ['MD; MD; WV', 'MD; MD', 'MD; MD', 'MD; MD', 'MD; MD; VA', 'MD; MD', 'MD; MD', 'MD; MD', 'MD; WV', 'MD; WV', 'MD', 'MD; MD; WV', 'MD', 'MD; MD; WV', 'MD; MD; WV']
TEXT NWR SITE: ['Frostburg, MD (Midland (Frostburg)); Hagerstown, MD (Clear Spring); Moorefield, WV (Branch Mtn.)', 'Baltimore, MD (Pikesville); Sudlersville, MD (Sudlersville)', 'Baltimore, MD (Pikesville); Sudlersville, MD (Sudlersville)', 'Baltimore, MD (Pikesville); Hagerstown, MD (Clear Spring)', 'Baltimore, MD (Pikesville); Hagerstown, MD (Clear Spring); Manassas, VA (Independent Hill)', 'Baltimore, MD (Pikesville); Sudlersville, MD (Sudlersville)', 'Baltimore, MD (Pikesville); Sudlersville, MD (Sudlersville)', 'Frostburg, MD (Midland (Frostburg)); Hagerstown, MD (Clear Spring)', 'Hagerstown, MD (Clear Spring); Moorefield, WV (Branch Mtn.)', 'Hagerstown, MD (Clear Spring); Moorefield, WV (Branch Mtn.)', 'Hagerstown, MD (Clear Spring)', 'Frostburg, MD (Midland (Frostburg)); Hagerstown, MD (Clear Spring); Moorefield, WV (Branch Mtn.)', 'Hagerstown, MD (Clear Spring)', 'Frostburg, MD (Midland (Frostburg)); Hagerstown, MD (Clear Spring); Moorefield, WV (Branch Mtn.)', 'Frostburg, MD (Midland (Frostburg)); Hagerstown, MD (Clear Spring); Moorefield, WV (Branch Mtn.)']
TEXT NWR COORDINATES: ['39.582167, -78.898667; 39.651111, -77.970833; 38.9825, -78.908611', '39.386349, -76.730772; 39.175389, -75.918278', '39.386349, -76.730772; 39.175389, -75.918278', '39.386349, -76.730772; 39.651111, -77.970833', '39.386349, -76.730772; 39.651111, -77.970833; 38.628722, -77.438833', '39.386349, -76.730772; 39.175389, -75.918278', '39.386349, -76.730772; 39.175389, -75.918278', '39.582167, -78.898667; 39.651111, -77.970833', '39.651111, -77.970833; 38.9825, -78.908611', '39.651111, -77.970833; 38.9825, -78.908611', '39.651111, -77.970833', '39.582167, -78.898667; 39.651111, -77.970833; 38.9825, -78.908611', '39.651111, -77.970833', '39.582167, -78.898667; 39.651111, -77.970833; 38.9825, -78.908611', '39.582167, -78.898667; 39.651111, -77.970833; 38.9825, -78.908611']
TEXT EVNT: a Special Weather Statement
TEXT FIPS: ['Allegany County, MD', 'Baltimore County, MD', 'Carroll County, MD', 'Frederick County, MD', 'Harford County, MD', 'Washington County, MD', 'Frederick County, VA', 'City of Winchester, VA', 'Berkeley County, WV', 'Hampshire County, WV', 'Jefferson County, WV', 'Mineral County, WV', 'and Morgan County, WV']
TEXT Start Time: 02:29 PM
TEXT End Time: 08:29 PM
The National Weather Service in Baltimore/Washington, D.C. (LWX); and Philadelphia/Mt Holly, NJ (PHI); has issued a Special Weather Statement for Allegany County, MD; Baltimore County, MD; Carroll County, MD; Frederick County, MD; Harford County, MD; Washington County, MD; Frederick County, VA; City of Winchester, VA; Berkeley County, WV; Hampshire County, WV; Jefferson County, WV; Mineral County, WV; and Morgan County, WV; beginning at 02:29 PM and ending at 08:29 PM. Message from EAR/FOLF.
```
</details>

---

## ⚠️ **Reporting Issues**

- Incorrect WFO/FIPS codes can be reported on [Discord](https://discord.com/users/637078631943897103) or in the GitHub Issues tab.
- Include **entire ZCZC SAME strings** and details for accurate fixes.

---

## 📜 **License**

**MIT License**

---

## 👤 **Contact**

- **Developer**: SecludedHusky Systems/Newton Communications
- **Discord**: [Contact Here](https://discord.com/users/637078631943897103)

---

### ❤️ **Thank You for Using My Version of EAS2Text!**  
Powered by [SecludedHusky Systems](https://services.secludedhusky.com). Get affordable internet radio services and VPS hosting today.