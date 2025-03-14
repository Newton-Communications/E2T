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