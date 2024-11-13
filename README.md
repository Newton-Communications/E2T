![EAS2Text](https://github.com/Newton-Communications/E2T/blob/nwr-localities/doc/img/TRxT7n.jpg)

An Extensive EAS Header to Text Translation Python Library REVAMPED!

## Reporting Issues
Data for the Weather Forecasting Offices has been collected based off of personal observations, available public data, and user reports and feedback. Any incorrect or invalid data should be reported using the specified criteria.
- If a FIPS Code reports as "Unknown WFO" and specifies a FIPS code, you can either report it to me on [Discord](https://discord.com/users/637078631943897103) and specify you are contacting regarding EAS2Text, or you can post it in the Issues tab on this repository, and make sure to include the FIPS Code mentioned as well as the proper WFO that should be specified by the FIPS Code.
- If a specific alert or Individual FIPS Code reports the incorrect Weather Forecasting Office, you can either report it to me on [Discord](https://discord.com/users/637078631943897103) and specify you are contacting regarding EAS2Text, or you can post it in the Issues tab on this repository, and make sure to include either the entire ZCZC SAME String and/or the FIPS Code that reports the wrong WFO, as well as what WFO is incorrect and specify what it should be changed to (the proper WFO).

## Specific Features That May Be Considered An Issue
- (CURRENTLY AN OPT-IN FEATURE) Some FIPS Codes may report as multiple WFOs due to NOAA Weather Radio transmitter coverage overlap. Functionality has been programmed into the script to detect if a county is covered by multiple WFOs and display all WFOs that tone for that county based on NWR coverage. This is a new feature. Marine localities will still need data determined, due to a lack of NOAA supplied data for Marine localities. Incorrect WFOs should only be reported if evidence is supplied to suggest that the data supplied to the project by the NWS is incorrect based upon NWR transmitter coverage maps.

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
> - [x] WXR Station Data and Coverage Overlap detection and support (Opt-in)
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
The National Weather Service in Baltimore/Washington, D.C. (LWX); and Philadelphia/Mt Holly, NJ (PHI); has issued a Special Weather Statement for Allegany County, MD; Baltimore County, MD; Carroll County, MD; Frederick County, MD; Harford County, MD; Washington County, MD; Frederick County, VA; City of Winchester, VA; Berkeley County, WV; Hampshire County, WV; Jefferson County, WV; Mineral County, WV; and Morgan County, WV; beginning at 02:29 PM and ending at 08:29 PM. Message from EAR/FOLF.
```

## Advanced Usage:
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

## NEW FEATURE: List Mode
EAS2Text has now implemented the ability to list the data that the script uses in order to help with development of external software. It requires the script to be switched from ZCZC mode to List mode in order to use the functionality.

To use List mode:
```python
from EAS2Text import EAS2Text

oof = EAS2Text(listMode=True)

print(f"Org List: {oof.orgList}") ## A list of all available originator codes
print(f"Event List: {oof.evntList}") ## A list of all available event codes
print(f"Subdivision List: {oof.subdivList}") ## A list of all available subdivision codes
print(f"FIPS Code List: {oof.fipsList}") ## A list of all available SAME FIPS codes
```
should output (with json response truncated due to length):
```
Org List: {'PEP': 'A Primary Entry Point System'...}
Event List: {'BZW': 'a Blizzard Warning'...}
Subdivision List: {'0': '', '1': 'Northwest'...}
FIPS Code List: {'10000': 'State of Delaware'...}
```

## NEW FEATURE: Canadian Forecast Regions!
EAS2Text has finally implemented Canadian Forecast Regions and Canada support into the software. However, due to the way Canadian FIPS codes are structured, it requires the software to be switched from the US mode to the Canadian mode.

Remember: **There is __no__ WFO text similar to the other scripts, so prepare your script accordingly!**

To use Canadian mode:
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
should output:
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

## Advanced Usage: Encoder Emulation
EAS2Text can be used to mimic or "emulate" other EAS devices.

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

## Advanced Usage: Timezone Specification
Timezones can be specified, both in UTC offset and in TZ timezone format. [List of tz database time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
Note: The custom timezone specification feature has a possibility to break if an invalid timezone is specified.

To use an specific timezone offset:
```python
from EAS2Text import EAS2Text

oof = EAS2Text(sameData = "ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-EAR/FOLF-", timeZone=-6) ## Uses a UTC-6 Offset

print(f"{oof.EASText}") ## The full EAS Output data, with a UTC-6 Offset.
```
should output:
```
The National Weather Service in Baltimore, MD/Washington, D.C. (LWX); has issued a Special Weather Statement for Allegany County, MD; Baltimore County, MD; Carroll County, MD; Frederick County, MD; Harford County, MD; Washington County, MD; Frederick County, VA; City of Winchester, VA; Berkeley County, WV; Hampshire County, WV; Jefferson County, WV; Mineral County, WV; and Morgan County, WV; beginning at 12:29 PM and ending at 06:29 PM. Message from EAR/FOLF.
```

To use an specific TZ timezone:
```python
from EAS2Text import EAS2Text

oof = EAS2Text(sameData = "ZCZC-WXR-SPS-024043-024021-024013-024005-024001-024025-051840-051069-054027-054065-054003-054037-054057+0600-0231829-EAR/FOLF-", timeZoneTZ="Europe/Berlin") ## Uses Europe/Berlin time.

print(f"{oof.EASText}") ## The full EAS Output data, in Europe/Berlin time.
```
should output:
```
The National Weather Service in Baltimore, MD/Washington, D.C. (LWX); has issued a Special Weather Statement for Allegany County, MD; Baltimore County, MD; Carroll County, MD; Frederick County, MD; Harford County, MD; Washington County, MD; Frederick County, VA; City of Winchester, VA; Berkeley County, WV; Hampshire County, WV; Jefferson County, WV; Mineral County, WV; and Morgan County, WV; beginning at 08:29 PM January 23 and ending at 02:29 AM January 24. Message from EAR/FOLF.
```

## Advanced Usage: Opt in to New WFO Data
You can specify a boolean value in order to use the new standard as specified in the update.
Note: This *CAN* and *WILL* sometimes output incorrect data, so use it without any expressed guarantee the data is accurate.

To specify this:
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
should output:
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
