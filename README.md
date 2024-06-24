![EAS2Text](https://github.com/Newton-Communications/E2T/blob/nwr-localities/doc/img/TRxT7n.jpg)

An Extensive EAS Header to Text Translation Python Library REVAMPED!

## Features
> - [x] EAS to Text Translation
> - [x] EAS EOM detection
> - [x] Handles Unknown Callsigns, Originators, and FIPS codes
> - [x] Additional raw outputs and individual item outputs
> - [x] EAS Data Validation
> - [x] WXR Weather Forecasting Office detection and support
> - [x] Marine FIPS codes readded and fixed
> - [x] Error handling revamped for new features

## Installation
This package should be installable through Pip.

On a Debian Based Linux OS:
```
sudo apt update
sudo apt install python3 python3-pip
python3 -m pip install https://github.com/Newton-Communications/E2T/archive/refs/heads/nwr-localities.zip
```


On Windows:

[Install Python](https://www.python.org/downloads/)

In CMD:
```
python -m pip install https://github.com/Newton-Communications/E2T/archive/refs/heads/nwr-localities.zip
```

## Usage
This package should take a raw ZCZC string, and then return the full text, and/or individual options:
```python
from EAS2Text import EAS2Text

data = EAS2Text("ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-EAR/FOLF-")
print(f"{data.EASText}")
```
should output:
```
The National Weather Service in Baltimore, MD/Washington, D.C. (LWX); has issued a Special Weather Statement for Allegany County, MD; Baltimore County, MD; Carroll County, MD; Frederick County, MD; Harford County, MD; Washington County, MD; Frederick County, VA; City of Winchester, VA; Berkeley County, WV; Hampshire County, WV; Jefferson County, WV; Mineral County, WV; and Morgan County, WV; beginning at 02:29 PM and ending at 08:29 PM. Message from EAR/FOLF.
```

## Advanced Useage:
Using the Generator, you can get additional output of info from an alert:
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
should output:
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

## NEW FEATURE: Encoder Emulation!
EAS2Text is the first Header to Text adapter that can "Emulate ENDECs"

Currently Supported:
 - DASDEC
 - BURK
 - SAGE EAS
 - SAGE DIGITAL
 - TRILITHIC
 - TFT

Not Supported:
 - EAS-1
 - HollyAnne Units

To use an emulation system:
```python
from EAS2Text import EAS2Text

oof = EAS2Text(sameData = "ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-EAR/FOLF-", mode="SAGE EAS") ## Emulates a SAGE EAS ENDEC

print(f"{oof.EASText}") ## The full EAS Output data, 1822 style
```
should output:
```
The National Weather Service has issued a Special Weather Statement for Allegany County, MD, Baltimore County, MD, Carroll County, MD, Frederick County, MD, Harford County, MD, Washington County, MD, Frederick County, VA, City of Winchester, VA, Berkeley County, WV, Hampshire County, WV, Jefferson County, WV, Mineral County, WV, and Morgan County, WV beginning at 02:29 pm and ending at 08:29 pm (EAR/FOLF)
```

## NEW FEATURE: Timezone Specification!
You can now specify a timezone offset to use! 
Note: This *CAN* and *WILL* break if you use obscure timezones. Keep it to Mainland U.S. for best reliability.

To use an specific timezone:
```python
from EAS2Text import EAS2Text

oof = EAS2Text(sameData = "ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-EAR/FOLF-", timeZone=-6) ## Uses a UTC-6 Offset

print(f"{oof.EASText}") ## The full EAS Output data, with a UTC-6 Offset.
```
should output:
```
The National Weather Service in Baltimore, MD/Washington, D.C. (LWX); has issued a Special Weather Statement for Allegany County, MD; Baltimore County, MD; Carroll County, MD; Frederick County, MD; Harford County, MD; Washington County, MD; Frederick County, VA; City of Winchester, VA; Berkeley County, WV; Hampshire County, WV; Jefferson County, WV; Mineral County, WV; and Morgan County, WV; beginning at 12:29 PM and ending at 06:29 PM. Message from EAR/FOLF.
```