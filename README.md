![EAS2Text](https://github.com/Newton-Communications/E2T/blob/nwr-localities/doc/img/TRxT7n.jpg)

An Extensive EAS Header to Text Translation Python Library REVAMPED!

## Reporting Issues
Data for the Weather Forecasting Offices has been collected based off of personal observations, available public data, and user reports and feedback. Any incorrect or invalid data should be reported using the specified criteria.
- If a FIPS Code reports as "Unknown WFO" and specifies a FIPS code, you can either report it to me on [Discord](https://discord.com/users/637078631943897103) and specify you are contacting regarding EAS2Text, or you can post it in the Issues tab on this repository, and make sure to include the FIPS Code mentioned as well as the proper WFO that should be specified by the FIPS Code.
- If a specific alert or Individual FIPS Code reports the incorrect Weather Forecasting Office, you can either report it to me on [Discord](https://discord.com/users/637078631943897103) and specify you are contacting regarding EAS2Text, or you can post it in the Issues tab on this repository, and make sure to include either the entire ZCZC SAME String and/or the FIPS Code that reports the wrong WFO, as well as what WFO is incorrect and specify what it should be changed to (the proper WFO).

## Known Issues
Several issues with the project are already known, and a fix either isn't possible, or isn't within plans to be implemented.
- Unknown FIPS Codes. Unless they're Canadian FIPS Codes, then we have plans to make Canadian alerts available via a separate system that will be included with EAS2Text at a later date. Unknown FIPS Codes, unless they are an actual, verifiable fips code, or edits to existing fips codes (if they are contact on [Discord](https://discord.com/users/637078631943897103) or specify the specific issue with said FIPS Code or lack of FIPS Code in the Issues tab on this repository), are a product of individual stations or the National Weather Service, and are not a bug with the script, and moreso a bug with the decoding of the ZCZC Headers from whatever EAS decoder/encoder you're using, or an issue with the alert itself when it was toned by the individual station or National Weather Service NOAA Weather Radio station.
- The software sometimes may crash entirely or quit functioning, this is a known issue, and errors can be reported via [Discord](https://discord.com/users/637078631943897103) or the Issues section of this repository. Not all errors will be considered for an implemented fix, so make sure if you use this script, you have it on a script manager such as PM2 or an auto-restarting SystemCTL service.


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