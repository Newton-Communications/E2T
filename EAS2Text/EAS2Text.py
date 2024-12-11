# Standard Library
from datetime import datetime as DT, timedelta
from json import loads, load
from time import localtime, timezone
from collections import Counter
from importlib import resources
import calendar
import re
import types
import platform

# Third-Party
import requests
import pytz

class InvalidSAME(Exception):
    def __init__(self, error, message="Invalid Data in SAME Message"):
        self.message = message
        self.error = error
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.error}"


class MissingSAME(Exception):
    def __init__(self, message="Missing SAME Message"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class EAS2Text(object):
    try:
        same_us = requests.get("https://matra.site/cdn/E2T/same-us.json").json()
    # except requests.exceptions.RequestException:
    except:
        with resources.open_text('EAS2Text', 'same-us.json') as json_file:
                same_us = load(json_file)

    try:
        same_ca = requests.get("https://matra.site/cdn/E2T/same-ca.json").json()
    # except requests.exceptions.RequestException:
    except:
        with resources.open_text('EAS2Text', 'same-ca.json') as json_file:
                same_ca = load(json_file)

    try:
        wfo_us = requests.get("https://matra.site/cdn/E2T/wfo-us.json").json()
    # except requests.exceptions.RequestException:
    except:
        with resources.open_text('EAS2Text', 'wfo-us.json') as json_file:
                wfo_us = load(json_file)

    try:
        ccl_us = requests.get("https://matra.site/cdn/E2T/CCL-us.json").json()
    except:
    # except requests.exceptions.RequestException:
        with resources.open_text('EAS2Text', 'CCL-us.json') as json_file:
                ccl_us = load(json_file)
        
    def __init__(
        self, sameData: str = "NONE", timeZone: int = None, mode: str = "NONE", newWFO: bool = False, canada: bool = False, timeZoneTZ: str = None, listMode: bool = False
    ) -> None:
        sameData = (
            sameData.strip()
        )  ## Strip to get rid of leading / trailing newlines and spaces (You're welcome, Don / Kane.)

        # List Mode
        if listMode == True and sameData == "NONE":
            if canada:
                stats = self.same_ca
                try:
                    self.orgList = stats["ORGS"]
                except:
                    self.orgList = f"Couldn't load Originator List"
                try:
                    self.evntList = stats["EVENTS"]
                except:
                    self.evntList = f"Couldn't load Event List"
                try:
                    self.subdivList = stats["SUBDIV"]
                except:
                    self.subdivList = f"Couldn't load Subdivision List"
                try:
                    self.fipsList = stats["SAME"]
                except:
                    self.fipsList = f"Couldn't load SAME List"
            else:
                stats = self.same_us
                try:
                    self.orgList = stats["ORGS"]
                except:
                    self.orgList = f"Couldn't load Originator List"
                try:
                    self.evntList = stats["EVENTS"]
                except:
                    self.evntList = f"Couldn't load Event List"
                try:
                    self.subdivList = stats["SUBDIV"]
                except:
                    self.subdivList = f"Couldn't load Subdivision List"
                try:
                    self.fipsList = stats["SAME"]
                except:
                    self.fipsList = f"Couldn't load SAME List"
        
        # Normal Script Mode

        if listMode == False and sameData != "NONE":
            if canada:
                # Canada Implementation
                stats = self.same_ca

                self.FIPS = []
                self.FIPSText = []
                self.strFIPS = ""
                self.EASData = sameData
                # Canada FIPS Code Checking (Identifier: Fox 002)

                ## CHECKING FOR VALID SAME - Canada
                if sameData == "":
                    raise MissingSAME()
                elif sameData.startswith("NNNN"):
                    self.EASText = "End Of Message"
                    return
                elif not sameData.startswith("ZCZC"):
                    raise InvalidSAME(sameData, message='"ZCZC" Start string missing')
                else:
                    eas = "".join(
                        sameData.replace("ZCZC-", "").replace("+", "-")
                    ).split("-")
                    eas.remove("")

                    for i in eas[2:-3]:
                        try:
                            assert len(i) == 6
                            assert self.__isInt__(i) == True
                            ## FIPS CODE
                            if i not in self.FIPS:
                                self.FIPS.append(str(i))
                        except AssertionError:
                            raise InvalidSAME("Invalid codes in FIPS data")

                    for i in sorted(self.FIPS):
                        try:
                            subdiv = stats["SUBDIV"][i[0]]
                            same = stats["SAME"][i[1:]]
                            self.FIPSText.append(
                                f"{subdiv + ' ' if subdiv != '' else ''}{same}" 
                            )
                            
                        except KeyError:
                            self.FIPSText.append(f"FIPS Code {i}")
                            
                        except Exception as E:
                            raise InvalidSAME(
                                self.FIPS, message=f"Error in FIPS Code ({str(E)})"
                            )
                        
                    if len(self.FIPSText) > 1:
                        FIPSText = self.FIPSText
                        FIPSText[-1] = f"and {FIPSText[-1]}"
                    self.strFIPS = "; ".join(self.FIPSText).strip() + ";"

                ## TIME CODE - Canada
                try:
                    self.purge = [eas[-3][:2], eas[-3][2:]]
                except IndexError:
                    raise InvalidSAME(self.purge, message="Purge Time not HHMM.")
                self.timeStamp = eas[-2]
                utc = DT.utcnow()
                if timeZone == None:
                    dtOffset = 0
                if timeZoneTZ == None:
                    dtOffset = 0
                if timeZone != None:
                    dtOffset = -timeZone * 3600
                if timeZoneTZ != None:
                    timezone = pytz.timezone(timeZoneTZ)
                    naive_now = DT.now()
                    tz_offset = timezone.utcoffset(naive_now)
                    total_seconds = tz_offset.total_seconds()
                    hour_offset = int(total_seconds // 3600)
                    utc_offset = f"{hour_offset:+d}"  # "+6" or "-3"
                    dtOffset = -int(utc_offset) * 3600

                try:
                    alertStartEpoch = (
                        DT.strptime(self.timeStamp, "%j%H%M")
                        .replace(year=utc.year)
                        .timestamp()
                    )
                except ValueError:
                    raise InvalidSAME(
                        self.timeStamp, message="Timestamp not JJJHHMM."
                    )
                alertEndOffset = (int(self.purge[0]) * 3600) + (
                    int(self.purge[1]) * 60
                )
                alertEndEpoch = alertStartEpoch + alertEndOffset

                try:
                    self.startTime = DT.fromtimestamp(alertStartEpoch - dtOffset)
                    self.endTime = DT.fromtimestamp(alertEndEpoch - dtOffset)

                    today = DT.fromtimestamp(alertStartEpoch - dtOffset).today().date()

                    current_year = DT.fromtimestamp(alertStartEpoch - dtOffset).year
                    is_leap_year = calendar.isleap(current_year)

                    if is_leap_year and today > DT(today.year, 2, 29).date():
                        self.startTime -= timedelta(days=1)  # Adjust for leap year
                        self.endTime -= timedelta(days=1)  # Adjust for leap year
                        
                    if self.startTime.day == self.endTime.day:
                        self.startTimeText = self.startTime.strftime("%I:%M %p")
                        self.endTimeText = self.endTime.strftime("%I:%M %p")
                    elif self.startTime.year == self.endTime.year:
                        self.startTimeText = self.startTime.strftime(
                            "%I:%M %p %B %d"
                        )
                        self.endTimeText = self.endTime.strftime("%I:%M %p %B %d")
                    else:
                        self.startTimeText = self.startTime.strftime(
                            "%I:%M %p %B %d, %Y"
                        )
                        self.endTimeText = self.endTime.strftime(
                            "%I:%M %p %B %d, %Y"
                        )
                except Exception as E:
                    raise InvalidSAME(
                        self.timeStamp,
                        message=f"Error in Time Conversion ({str(E)})",
                    )

                ## ORG / EVENT CODE - Canada
                try:
                    self.org = str(eas[0])
                    self.evnt = str(eas[1])
                    try:
                        assert len(eas[0]) == 3
                    except AssertionError:
                        raise InvalidSAME("Originator is an invalid length")
                    try:
                        assert len(eas[1]) == 3
                    except AssertionError:
                        raise InvalidSAME("Event Code is an invalid length")
                    try:
                        self.orgText = stats["ORGS"][self.org]
                    except:
                        self.orgText = (
                            f"An Unknown Originator ({self.org});"
                        )
                    try:
                        self.evntText = stats["EVENTS"][self.evnt]
                    except:
                        self.evntText = f"an Unknown Event ({self.evnt})"
                except Exception as E:
                    raise InvalidSAME(
                        [self.org, self.evnt],
                        message=f"Error in ORG / EVNT Decoding ({str(E)})",
                    )

                ## CALLSIGN CODE - Canada
                self.callsign = eas[-1].strip()

                ## FINAL TEXT - Canada
                if mode == "TFT":
                    # TFT Mode - Canada
                    self.strFIPS = (
                        self.strFIPS[:-1]
                        .replace(",", "")
                        .replace(";", ",")
                        .replace("FIPS Code", "AREA")
                    )
                    self.startTimeText = self.startTime.strftime(
                        "%I:%M %p ON %b %d, %Y"
                    )
                    self.endTimeText = (
                        self.endTime.strftime("%I:%M %p")
                        if self.startTime.day == self.endTime.day
                        else self.endTime.strftime("%I:%M %p ON %b %d, %Y")
                    )
                    if self.org == "EAS" or self.evnt in ["NPT", "EAN"]:
                        self.EASText = f"{self.evntText} has been issued for the following counties/areas: {self.strFIPS} at {self.startTimeText} effective until {self.endTimeText}. message from {self.callsign}.".upper()
                    else:
                        self.EASText = f"{self.orgText} has issued {self.evntText} for the following counties/areas: {self.strFIPS} at {self.startTimeText} effective until {self.endTimeText}. message from {self.callsign}.".upper()

                elif mode.startswith("SAGE"):
                    # SAGE Mode - Canada
                    if self.org == "CIV":
                        self.orgText = "The Civil Authorities"
                    self.strFIPS = self.strFIPS[:-1].replace(";", ",")
                    self.startTimeText = self.startTime.strftime(
                        "%I:%M %p"
                    ).lower()
                    self.endTimeText = self.endTime.strftime("%I:%M %p").lower()
                    if self.startTime.day != self.endTime.day:
                        self.startTimeText += self.startTime.strftime(" %a %b %d")
                        self.endTimeText += self.endTime.strftime(" %a %b %d")
                    if mode.endswith("DIGITAL"):
                        self.EASText = f"{self.orgText} {'have' if self.org == 'CIV' else 'has'} issued {self.evntText} for {self.strFIPS} beginning at {self.startTimeText} and ending at {self.endTimeText} ({self.callsign})"
                    else:
                        if self.org == "EAS":
                            self.orgText = "A Broadcast station or cable system"
                        self.EASText = f"{self.orgText} {'have' if self.org == 'CIV' else 'has'} issued {self.evntText} for {self.strFIPS} beginning at {self.startTimeText} and ending at {self.endTimeText} ({self.callsign})"

                elif mode in ["TRILITHIC", "VIAVI", "EASY"]:
                    # Trilithic Mode - Canada
                    def process_location(text):
                            
                        if text.startswith("City of"):
                            text = text.replace("City of", "") + " (city)"

                        if text.startswith("State of"):
                            text = text.replace("State of", "All of")

                        if text.startswith("District of"):
                            text = text.replace("District of", "All of District of")
                            
                        if " City of" in text:
                            text = text.replace(" City of", "") + " (city)"

                        if (" State of" in text) and not ("All of" in text):
                            text = text.replace(" State of", " All of")

                        if (" District of" in text) and not ("All of" in text):
                            text = text.replace(" District of", " All of District of")
                        
                        if " County" in text:
                            text = text.replace(" County", "")
                        
                        if text.startswith("and "):
                            text = text.replace("and ", "")
                        
                        if "; " in text:
                            text = text.replace("; ", " - ")
                        
                        return text

                    strFIPS_value = (
                        "".join(self.strFIPS) if isinstance(self.strFIPS, types.GeneratorType) else self.strFIPS
                    )

                    self.strFIPS = (
                        ", ".join(map(process_location, map(str.strip, strFIPS_value[:-1].split(", "))))
                        if "000000" not in self.FIPS
                        else "Canada"
                    )

                    self.strFIPS = self.strFIPS.replace(',', '').replace(' and', '')

                    def filterlocation(text):
                        if text.startswith("City of"):
                            text = text.replace("City of ", "") + " (city)"

                        if text.startswith("State of"):
                            text = text.replace("State of", "All of")

                        if text.startswith("District of"):
                            text = text.replace("District of", "All of District of")
                            
                        if " City of" in text:
                            text = text.replace(" City of", "") + " (city)"

                        if (" State of" in text) and not ("All of" in text):
                            text = text.replace(" State of", " All of")

                        if (" District of" in text) and not ("All of" in text):
                            text = text.replace(" District of", " All of District of")
                        
                        if " County" in text:
                            text = text.replace(" County", "")
                        
                        if text.startswith("and "):
                            text = text.replace("and ", "")

                        return text

                    FIPSStrings = []
                    for loc in self.FIPSText:
                        loc2 = loc.split(", ")
                        if len(loc2) == 1:
                            loc3 = filterlocation(loc2[0])
                        elif len(loc2) == 2:
                            loc3 = filterlocation(loc2[0]) + " " + loc2[1]
                        elif len(loc2) > 2:
                            loc3 = filterlocation(" ".join(loc2[:-1])) + " " + loc2[-1]

                        FIPSStrings.append(loc3)

                    self.FIPSText = FIPSStrings

                    if self.strFIPS == "Canada":
                        bigFips = "for"
                    else:
                        bigFips = "for the following counties:"
                    self.startTimeText = ""
                    self.endTimeText = self.endTime.strftime(
                        "%m/%d/%y %H:%M:00 "
                    ) + self.getTZ(dtOffset)
                    if self.org == "CIV":
                        self.orgText = "The Civil Authorities"
                    self.EASText = f"{self.orgText} {'have' if self.org == 'CIV' else 'has'} issued {self.evntText} {bigFips} {self.strFIPS}. Effective Until {self.endTimeText}. ({self.callsign})"

                elif mode in ["BURK"]:
                    # Burk Mode - Canada
                    if self.org == "EAS":
                        self.orgText = "A Broadcast station or cable system"
                    elif self.org == "CIV":
                        self.orgText = "The Civil Authorities"
                    elif self.org == "WXR":
                        self.orgText = "Environment Canada"
                    self.strFIPS = (
                        self.strFIPS[:-1].replace(",", "").replace(";", ",")
                    )
                    self.startTimeText = (
                        self.startTime.strftime("%B %d, %Y").upper()
                        + " at "
                        + self.startTime.strftime("%I:%M %p")
                    )
                    self.endTimeText = self.endTime.strftime("%I:%M %p, %B %d, %Y")
                    self.endTimeText = self.endTimeText.upper()
                    self.evntText = " ".join(self.evntText.split(" ")[1:]).upper()
                    self.EASText = f"{self.orgText} has issued {self.evntText} for the following counties/areas: {self.strFIPS} on {self.startTimeText} effective until {self.endTimeText}."

                elif mode in ["DAS", "DASDEC", "MONROE", "ONENET", "ONENET SE"]:
                    # DASDEC Software <=v2.9 Mode - Canada

                    if self.org == "EAS":
                        self.orgText = "A broadcast or cable system"
                    elif self.org == "CIV":
                        self.orgText = "A civil authority"
                    elif self.org == "WXR":
                        self.orgText = "The National Weather Service"
                    elif self.org == "PEP":
                        self.orgText = "THE PRIMARY ENTRY POINT EAS SYSTEM"

                    self.orgText = self.orgText.upper()
                    self.evntText = self.evntText.upper()
                    # Function to process the FIPS string and check for parishes
                    def process_fips_string(fips_string):
                        result = []
                        states = {}  # To track counties/cities/parishes per state
                        only_parishes = True  # Flag to check if only parishes exist
                        parts = [part.strip() for part in fips_string.split(';') if part.strip()]

                        for part in parts:
                            part = re.sub(r'^\s*and\s+', '', part)
                            
                            # Match "City of", "County", or "Parish" and extract name and state
                            match = re.match(r'(City of )?(.*?)( County| Parish)?, (\w{2})', part)
                            state_match = re.match(r'State of (.+)', part)

                            if match:
                                city_prefix, name, locality_type, state = match.groups()
                                clean_name = name

                                # Determine locality type and adjust name
                                if locality_type == " Parish":
                                    pass  # No suffix needed, keep the name as is
                                elif city_prefix:
                                    clean_name += " (city)"
                                    only_parishes = False  # Contains city
                                else:
                                    only_parishes = False  # Contains county

                                # Track states and their counties/cities/parishes
                                if state not in states:
                                    states[state] = []
                                states[state].append((clean_name, state))

                            elif state_match:
                                # Handle standalone states like "State of Washington"
                                state_name = state_match.group(1)
                                result.append(state_name)  # Add state directly to result

                        # Build the result with correct formatting
                        for state, entries in states.items():
                            for i, (name, _) in enumerate(entries):
                                # Add state abbreviation only to the last entry for the state
                                if i == len(entries) - 1:
                                    result.append(f"{name}, {state}")
                                else:
                                    result.append(name)

                        # Join results and format properly
                        final_result = '; '.join(result).replace(' and ', ' ')

                        # Fix "City of" for all independent cities and ensure state formatting
                        final_result = re.sub(r'City of (.*?)( \(city\))?,', r'\1 (city),', final_result)
                        return final_result + ';', only_parishes

                    # Process the input string
                    self.strFIPS, self.onlyParishes = process_fips_string(self.strFIPS)

                    self.strFIPS = self.strFIPS.upper()
                    # Use the appropriate hour format specifier based on the operating system
                    if platform.system() == "Windows":
                        hour_format = "%#I"  # Windows-specific: No leading zero for hour
                    else:
                        hour_format = "%-I"  # Unix-like systems: No leading zero for hour

                    if self.startTime.date() == self.endTime.date():
                        # Same day
                        self.startTimeText = (
                            self.startTime.strftime(f"{hour_format}:%M %p").upper()
                            + " ON" + self.startTime.strftime(" %b %d, %Y").upper()
                        )
                        self.endTimeText = self.endTime.strftime(f"{hour_format}:%M %p").upper()
                    else:
                        # Different days
                        self.startTimeText = (
                            self.startTime.strftime(f"{hour_format}:%M %p").upper()
                            + " ON" + self.startTime.strftime(" %b %d, %Y").upper()
                        )
                        self.endTimeText = (
                            self.endTime.strftime(f"{hour_format}:%M %p").upper()
                            + self.endTime.strftime(" %b %d, %Y").upper()
                        )
                    self.EASText = f"{self.orgText} HAS ISSUED {self.evntText} FOR THE FOLLOWING {'AREAS' if self.onlyParishes else 'COUNTIES/AREAS'}: {self.strFIPS} AT {self.startTimeText} EFFECTIVE UNTIL {self.endTimeText}. MESSAGE FROM {self.callsign.upper()}."

                elif mode in ["DASV3", "DASDECV3", "MONROEV3", "ONENETV3", "ONENET SEV3"]:
                    # DASDEC Software >=v3.0 Mode - Canada

                    if self.org == "EAS":
                            self.orgText = "A broadcast or cable system"
                    elif self.org == "CIV":
                        self.orgText = "A civil authority"
                    elif self.org == "WXR":
                        self.orgText = "The National Weather Service"
                    elif self.org == "PEP":
                        self.orgText = "THE PRIMARY ENTRY POINT EAS SYSTEM"

                    self.evntText = self.evntText.upper()

                    # Function to process the FIPS string and check for parishes
                    def process_fips_string(fips_string):
                        result = []
                        states = {}  # To track counties/cities/parishes per state
                        only_parishes = True  # Flag to check if only parishes exist
                        parts = [part.strip() for part in fips_string.split(';') if part.strip()]

                        for part in parts:
                            part = re.sub(r'^\s*and\s+', '', part)

                            # Match "City of", "County", or "Parish" and extract name and state
                            match = re.match(r'(City of )?(.*?)( County| Parish)?, (\w{2})', part)
                            state_match = re.match(r'State of (.+)', part)

                            if match:
                                city_prefix, name, locality_type, state = match.groups()
                                clean_name = name

                                # Determine locality type and adjust name
                                if locality_type == " Parish":
                                    pass  # No suffix needed, keep the name as is
                                elif city_prefix:
                                    clean_name += " (city)"
                                    only_parishes = False  # Contains city
                                else:
                                    only_parishes = False  # Contains county

                                # Track states and their counties/cities/parishes
                                if state not in states:
                                    states[state] = []
                                states[state].append((clean_name, state))

                            elif state_match:
                                # Handle standalone states like "State of Washington"
                                state_name = state_match.group(1)
                                result.append(state_name)  # Add state directly to result

                        # Build the result with correct formatting
                        for state, entries in states.items():
                            for i, (name, _) in enumerate(entries):
                                # Add state abbreviation only to the last entry for the state
                                if i == len(entries) - 1:
                                    result.append(f"{name}, {state}")
                                else:
                                    result.append(name)

                        # Join results and format properly
                        final_result = '; '.join(result).replace(' and ', ' ')

                        # Fix "City of" for all independent cities and ensure state formatting
                        final_result = re.sub(r'City of (.*?)( \(city\))?,', r'\1 (city),', final_result)
                        return final_result + ';', only_parishes

                    # Process the input string
                    self.strFIPS, self.onlyParishes = process_fips_string(self.strFIPS)

                    # Use the appropriate hour format specifier based on the operating system
                    if platform.system() == "Windows":
                        hour_format = "%#I"  # Windows-specific: No leading zero for hour
                    else:
                        hour_format = "%-I"  # Unix-like systems: No leading zero for hour

                    if self.startTime.date() == self.endTime.date():
                        # Same day
                        self.startTimeText = (
                            self.startTime.strftime(f"{hour_format}:%M %p").upper()
                            + " on" + self.startTime.strftime(" %b %d, %Y").upper()
                        )
                        self.endTimeText = self.endTime.strftime(f"{hour_format}:%M %p").upper()
                    else:
                        # Different days
                        self.startTimeText = (
                            self.startTime.strftime(f"{hour_format}:%M %p").upper()
                            + " on" + self.startTime.strftime(" %b %d, %Y").upper()
                        )
                        self.endTimeText = (
                            self.endTime.strftime(f"{hour_format}:%M %p").upper()
                            + self.endTime.strftime(" %b %d, %Y").upper()
                        )

                    self.EASText = f"{self.orgText} has issued {self.evntText} for the following {'areas' if self.onlyParishes else 'counties/areas'}: {self.strFIPS} at {self.startTimeText} Effective until {self.endTimeText}. Message from {self.callsign}."


                elif mode in ["HollyAnne", "Holly Anne", "Holly-Anne", "HU-961", "MIP-921", "MIP-921e", "HU961", "MIP921", "MIP921e"]:
                    # HollyAnne Mode - Canada
                    if self.org == "EAS":
                        self.orgText = "CABLE/BROADCAST SYSTEM"
                    elif self.org == "CIV":
                        self.orgText = "AUTHORITIES"
                    elif self.org == "WXR":
                        self.orgText = "ENVIRONMENT CANADA"

                    self.evntText = self.evntText.upper()

                    self.strFIPS = self.strFIPS.replace(',', '')

                    def filterlocation(text):
                        if text.startswith("City of"):
                            text = text.replace("City of ", "") + " CITY"

                        if text.startswith("State of"):
                            text = text.replace("State of", "")
                            
                        if " City of" in text:
                            text = text.replace(" City of", "") + " CITY"

                        if (" State of" in text) and not ("All of" in text):
                            text = text.replace(" State of", "")
                        
                        if " County" in text:
                            text = text.replace(" County", "")
                        
                        if text.startswith("and "):
                            text = text.replace("and ", "AND ")

                        return text

                    # Collect all state abbreviations
                    state_abbreviations = []
                    for loc in self.FIPSText:
                        loc_parts = loc.split(", ")
                        if len(loc_parts) > 1:  # Ensure there is a state abbreviation
                            state_abbreviations.append(loc_parts[-1])

                    unique_states = set(state_abbreviations)  # Check for unique states

                    FIPSStrings = []
                    for loc in self.FIPSText:
                        loc_parts = loc.split(", ")
                        if len(loc_parts) == 2:  # Contains a location and a state abbreviation
                            location = loc_parts[0]
                            state = loc_parts[1]
                            if len(unique_states) == 1:  # If only one state is present
                                loc3 = filterlocation(location).upper()
                            else:  # If multiple states are present, remove comma but keep state
                                loc3 = filterlocation(location).upper() + " " + state.upper()
                        elif len(loc_parts) > 2:  # Multiple components, e.g., "City of X, State, XX"
                            loc3 = filterlocation(" ".join(loc_parts[:-1])).upper() + " " + loc_parts[-1].upper()
                        else:  # Single location without state abbreviation
                            loc3 = filterlocation(loc_parts[0]).upper()

                        FIPSStrings.append(loc3)

                    # Update FIPSText and strFIPS
                    self.FIPSText = FIPSStrings
                    self.strFIPS = ", ".join(self.FIPSText).strip()

                    # Remove ", AND" if it exists
                    if ", AND " in self.strFIPS:
                        self.strFIPS = self.strFIPS.replace(", AND ", " AND ")

                    self.startTimeText = self.startTimeText.upper()
                    self.endTimeText = self.endTimeText.upper()
                    
                    self.EASText = f"THE {self.orgText} HAS ISSUED {self.evntText} FOR THE FOLLOWING COUNTIES: {self.strFIPS} BEGINNING AT {self.startTimeText} AND ENDING AT {self.endTimeText}. MESSAGE FROM {self.callsign}."

                elif mode in ["EAS1CG", "EAS-1", "EAS1", "EAS1-CG", "EAS-1CG", "Gorman-Redlich", "GormanRedlich", "Gorman Redlich"]:
                    # Gorman Redlich Mode - Canada
                    self.evntText = self.evntText.upper()

                    # Use the appropriate format specifier based on the operating system
                    if platform.system() == "Windows":
                        hour_format = "%#I"  # Windows-specific: No leading zero for hour
                    else:
                        hour_format = "%-I"  # Unix-like systems: No leading zero for hour

                    if self.startTime.date() == self.endTime.date():
                        # Same day
                        self.startTimeText = self.startTime.strftime(
                            f"{hour_format}:%M %p ON %B %d, %Y"
                        ).upper()
                        self.endTimeText = self.endTime.strftime(
                            f"{hour_format}:%M %p"
                        ).upper()
                    else:
                        # Different days
                        self.startTimeText = self.startTime.strftime(
                            f"{hour_format}:%M %p ON %B %d, %Y"
                        ).upper()
                        self.endTimeText = self.endTime.strftime(
                            f"{hour_format}:%M %p ON %B %d, %Y"
                        ).upper()

                    def filterlocation(text):
                        if text.startswith("City of"):
                            text = text.replace("City of ", "") + " CITY"

                        if text.startswith("State of"):
                            text = text.replace("State of", "")
                            
                        if " City of" in text:
                            text = text.replace(" City of", "") + " CITY"

                        if (" State of" in text) and not ("All of" in text):
                            text = text.replace(" State of", "")
                        
                        if " County" in text:
                            text = text.replace(" County", "")
                        
                        if text.startswith("and "):
                            text = text.replace("and ", "AND ")

                        return text
                    
                    FIPSStrings = []
                    for loc in self.FIPSText:
                        loc_parts = loc.split(", ")
                        if len(loc_parts) == 2:  # Contains a location and a state abbreviation
                            location = loc_parts[0]
                            state = loc_parts[1]
                            loc3 = filterlocation(location).upper() + " " + state.upper()
                        elif len(loc_parts) > 2:  # Multiple components, e.g., "City of X, State, XX"
                            loc3 = filterlocation(" ".join(loc_parts[:-1])).upper() + " " + loc_parts[-1].upper()
                        else:  # Single location without state abbreviation
                            loc3 = filterlocation(loc_parts[0]).upper()

                        FIPSStrings.append(loc3)

                    # Update FIPSText and strFIPS
                    self.FIPSText = FIPSStrings
                    self.strFIPS = ", ".join(self.FIPSText).strip()

                    # Remove ", AND" if it exists
                    if ", AND " in self.strFIPS:
                        self.strFIPS = self.strFIPS.replace(", AND ", " AND ")


                    self.EASText = f"{self.evntText} HAS BEEN ISSUED FOR {self.strFIPS} AT {self.startTimeText} EFFECTIVE UNTIL {self.endTimeText}. MESSAGE FROM {self.callsign}."

                else:
                    self.EASText = f"{self.orgText} has issued {self.evntText} for {self.strFIPS} beginning at {self.startTimeText} and ending at {self.endTimeText}. Message from {self.callsign}."

            else:
                # United States Implementation
                stats = self.same_us
                locality2 = self.wfo_us
                ccl2 = self.ccl_us
                self.FIPS = []
                self.FIPSText = []
                self.strFIPS = ""
                self.EASData = sameData
                # US FIPS Code Checking (Identifier: Fox 001)

                if not newWFO:

                    # United States Old Weather Forecasting Office Mode (Referred to as United States Old WFO)

                    self.WFO = []
                    self.WFOText = []
                    self.StateInSAME = False

                    ## CHECKING FOR VALID SAME - United States Old WFO
                    if sameData == "":
                        raise MissingSAME()
                    elif sameData.startswith("NNNN"):
                        self.EASText = "End Of Message"
                        return
                    elif not sameData.startswith("ZCZC"):
                        raise InvalidSAME(sameData, message='"ZCZC" Start string missing')
                    else:
                        eas = "".join(
                            sameData.replace("ZCZC-", "").replace("+", "-")
                        ).split("-")
                        eas.remove("")

                        for i in eas[2:-3]:
                            try:
                                assert len(i) == 6
                                assert self.__isInt__(i) == True
                                ## FIPS CODE - United States Old WFO
                                if i not in self.FIPS:
                                    self.FIPS.append(str(i))
                            except AssertionError:
                                raise InvalidSAME("Invalid codes in FIPS data")

                        for i in sorted(self.FIPS):
                            try:
                                subdiv = stats["SUBDIV"][i[0]]
                                same = stats["SAME"][i[1:]]
                                self.FIPSText.append(
                                    f"{subdiv + ' ' if subdiv != '' else ''}{same}" 
                                )
                                
                                try:
                                    if(str(eas[0]) == "WXR") and ("State" not in same):
                                        ## WXR LOCALITY - United States Old WFO
                                        wfo = locality2["SAME"][i[1:]][0]["wfo"]
                                        if wfo:
                                            self.WFOText.append(
                                                f"{wfo}"
                                            )
                                            self.WFO.append(
                                                f"{wfo}"
                                            )
                                        else:
                                            self.WFO.append(f"Unknown WFO for FIPS Code {i}")
                                            self.WFOText.append(f"Unknown WFO for FIPS Code {i}")
                                    elif ("State" in same):
                                        self.StateInSAME = True
                                except KeyError:
                                    self.WFO.append(f"Unknown WFO for FIPS Code {i}")
                                    self.WFOText.append(f"Unknown WFO for FIPS Code {i}")
                                except Exception as E:
                                    raise InvalidSAME(
                                        self.WFOText, message=f"Error in WFO Text ({str(E)})"
                                    )
                                
                            except KeyError:
                                self.FIPSText.append(f"FIPS Code {i}")
                                self.WFO.append(f"Unknown WFO for FIPS Code {i}")
                                self.WFOText.append(f"Unknown WFO for FIPS Code {i}")
                                
                            except Exception as E:
                                raise InvalidSAME(
                                    self.FIPS, message=f"Error in FIPS Code ({str(E)})"
                                )
                            
                        if (self.WFO == "" or self.WFO is None) or (self.WFOText == "" or self.WFOText is None):
                            self.WFO = ["Unknown WFO"]
                            self.WFOText = ["Unknown WFO"]
                            
                        if len(self.FIPSText) > 1:
                            FIPSText = self.FIPSText
                            FIPSText[-1] = f"and {FIPSText[-1]}"
                        self.strFIPS = "; ".join(self.FIPSText).strip() + ";"

                        ## WXR LOCALITY MULTIPLE - United States Old WFO
                        if(str(eas[0]) == "WXR"):
                            if (self.WFOText != "" and self.WFOText is not None) and (not self.StateInSAME):
                                if len(self.WFOText) > 1:
                                    p = []
                                    for values in self.WFOText:
                                        if values not in p:
                                            p.append(values)
                                    if(len(p) > 1):
                                        p[-1] = f"and {p[-1]}"
                                    self.WFOText = "; ".join(p).strip() + ";"
                                else:
                                    p = self.WFOText[0]
                                    self.WFOText = str(self.WFOText[0])+";"
                            else:
                                self.WFOText = ["Unknown WFO"]
                            if (self.WFO != "" and self.WFO is not None) and (not self.StateInSAME):
                                if len(self.WFO) > 1:
                                    p = []
                                    for values in self.WFO:
                                        if values not in p:
                                            p.append(values)
                                    if(len(p) > 1):
                                        p[-1] = f"and {p[-1]}"
                                    self.WFO = "; ".join(p).strip() + ";"
                                else:
                                    p = self.WFO[0]
                                    self.WFO = str(self.WFO[0])+";"
                            else:
                                self.WFO = ["Unknown WFO"]

                    ## TIME CODE - United States Old WFO
                    try:
                        self.purge = [eas[-3][:2], eas[-3][2:]]
                    except IndexError:
                        raise InvalidSAME(self.purge, message="Purge Time not HHMM.")
                    self.timeStamp = eas[-2]
                    utc = DT.utcnow()
                    if timeZone == None:
                        dtOffset = 0
                    if timeZoneTZ == None:
                        dtOffset = 0
                    if timeZone != None:
                        dtOffset = -timeZone * 3600
                    if timeZoneTZ != None:
                        timezone = pytz.timezone(timeZoneTZ)
                        naive_now = DT.now()
                        tz_offset = timezone.utcoffset(naive_now)
                        total_seconds = tz_offset.total_seconds()
                        hour_offset = int(total_seconds // 3600)
                        utc_offset = f"{hour_offset:+d}"  # "+6" or "-3"
                        dtOffset = -int(utc_offset) * 3600

                    try:
                        alertStartEpoch = (
                            DT.strptime(self.timeStamp, "%j%H%M")
                            .replace(year=utc.year)
                            .timestamp()
                        )
                    except ValueError:
                        raise InvalidSAME(
                            self.timeStamp, message="Timestamp not JJJHHMM."
                        )
                    alertEndOffset = (int(self.purge[0]) * 3600) + (
                        int(self.purge[1]) * 60
                    )
                    alertEndEpoch = alertStartEpoch + alertEndOffset

                    try:
                        self.startTime = DT.fromtimestamp(alertStartEpoch - dtOffset)
                        self.endTime = DT.fromtimestamp(alertEndEpoch - dtOffset)

                        today = DT.fromtimestamp(alertStartEpoch - dtOffset).today().date()

                        current_year = DT.fromtimestamp(alertStartEpoch - dtOffset).year
                        is_leap_year = calendar.isleap(current_year)

                        if is_leap_year and today > DT(today.year, 2, 29).date():
                            self.startTime -= timedelta(days=1)  # Adjust for leap year
                            self.endTime -= timedelta(days=1)  # Adjust for leap year
                            
                        if self.startTime.day == self.endTime.day:
                            self.startTimeText = self.startTime.strftime("%I:%M %p")
                            self.endTimeText = self.endTime.strftime("%I:%M %p")
                        elif self.startTime.year == self.endTime.year:
                            self.startTimeText = self.startTime.strftime(
                                "%I:%M %p %B %d"
                            )
                            self.endTimeText = self.endTime.strftime("%I:%M %p %B %d")
                        else:
                            self.startTimeText = self.startTime.strftime(
                                "%I:%M %p %B %d, %Y"
                            )
                            self.endTimeText = self.endTime.strftime(
                                "%I:%M %p %B %d, %Y"
                            )
                    except Exception as E:
                        raise InvalidSAME(
                            self.timeStamp,
                            message=f"Error in Time Conversion ({str(E)})",
                        )

                    ## ORG / EVENT CODE - United States Old WFO
                    try:
                        self.org = str(eas[0])
                        self.evnt = str(eas[1])
                        try:
                            assert len(eas[0]) == 3
                        except AssertionError:
                            raise InvalidSAME("Originator is an invalid length")
                        try:
                            assert len(eas[1]) == 3
                        except AssertionError:
                            raise InvalidSAME("Event Code is an invalid length")
                        try:
                            self.orgText = stats["ORGS"][self.org]
                        except:
                            self.orgText = (
                                f"An Unknown Originator ({self.org});"
                            )
                        try:
                            self.evntText = stats["EVENTS"][self.evnt]
                        except:
                            self.evntText = f"an Unknown Event ({self.evnt})"
                    except Exception as E:
                        raise InvalidSAME(
                            [self.org, self.evnt],
                            message=f"Error in ORG / EVNT Decoding ({str(E)})",
                        )

                    ## CALLSIGN CODE - United States Old WFO
                    self.callsign = eas[-1].strip()

                    ## FINAL TEXT - United States Old WFO
                    if mode == "TFT":
                        # TFT Mode - United States Old WFO
                        self.strFIPS = (
                            self.strFIPS[:-1]
                            .replace(",", "")
                            .replace(";", ",")
                            .replace("FIPS Code", "AREA")
                        )
                        self.startTimeText = self.startTime.strftime(
                            "%I:%M %p ON %b %d, %Y"
                        )
                        self.endTimeText = (
                            self.endTime.strftime("%I:%M %p")
                            if self.startTime.day == self.endTime.day
                            else self.endTime.strftime("%I:%M %p ON %b %d, %Y")
                        )
                        if self.org == "EAS" or self.evnt in ["NPT", "EAN"]:
                            self.EASText = f"{self.evntText} has been issued for the following counties/areas: {self.strFIPS} at {self.startTimeText} effective until {self.endTimeText}. message from {self.callsign}.".upper()
                        else:
                            self.EASText = f"{self.orgText} has issued {self.evntText} for the following counties/areas: {self.strFIPS} at {self.startTimeText} effective until {self.endTimeText}. message from {self.callsign}.".upper()

                    elif mode.startswith("SAGE"):
                        # SAGE Mode - United States Old WFO
                        if self.org == "CIV":
                            self.orgText = "The Civil Authorities"
                        self.strFIPS = self.strFIPS[:-1].replace(";", ",")
                        self.startTimeText = self.startTime.strftime(
                            "%I:%M %p"
                        ).lower()
                        self.endTimeText = self.endTime.strftime("%I:%M %p").lower()
                        if self.startTime.day != self.endTime.day:
                            self.startTimeText += self.startTime.strftime(" %a %b %d")
                            self.endTimeText += self.endTime.strftime(" %a %b %d")
                        if mode.endswith("DIGITAL"):
                            self.EASText = f"{self.orgText} {'have' if self.org == 'CIV' else 'has'} issued {self.evntText} for {self.strFIPS} beginning at {self.startTimeText} and ending at {self.endTimeText} ({self.callsign})"
                        else:
                            if self.org == "EAS":
                                self.orgText = "A Broadcast station or cable system"
                            self.EASText = f"{self.orgText} {'have' if self.org == 'CIV' else 'has'} issued {self.evntText} for {self.strFIPS} beginning at {self.startTimeText} and ending at {self.endTimeText} ({self.callsign})"

                    elif mode in ["TRILITHIC", "VIAVI", "EASY"]:
                        # Trilithic Mode - United States Old WFO
                        def process_location(text):
                            
                            if text.startswith("City of"):
                                text = text.replace("City of", "") + " (city)"

                            if text.startswith("State of"):
                               text = text.replace("State of", "All of")

                            if text.startswith("District of"):
                                text = text.replace("District of", "All of District of")
                                
                            if " City of" in text:
                                text = text.replace(" City of", "") + " (city)"

                            if (" State of" in text) and not ("All of" in text):
                                text = text.replace(" State of", " All of")

                            if (" District of" in text) and not ("All of" in text):
                                text = text.replace(" District of", " All of District of")
                            
                            if " County" in text:
                                text = text.replace(" County", "")
                            
                            if text.startswith("and "):
                                text = text.replace("and ", "")
                            
                            if "; " in text:
                                text = text.replace("; ", " - ")
                            
                            return text

                        strFIPS_value = (
                            "".join(self.strFIPS) if isinstance(self.strFIPS, types.GeneratorType) else self.strFIPS
                        )

                        self.strFIPS = (
                            ", ".join(map(process_location, map(str.strip, strFIPS_value[:-1].split(", "))))
                            if "000000" not in self.FIPS
                            else "Canada"
                        )

                        self.strFIPS = self.strFIPS.replace(',', '').replace(' and', '')

                        def filterlocation(text):
                            if text.startswith("City of"):
                               text = text.replace("City of ", "") + " (city)"

                            if text.startswith("State of"):
                               text = text.replace("State of", "All of")

                            if text.startswith("District of"):
                                text = text.replace("District of", "All of District of")
                                
                            if " City of" in text:
                                text = text.replace(" City of", "") + " (city)"

                            if (" State of" in text) and not ("All of" in text):
                                text = text.replace(" State of", " All of")

                            if (" District of" in text) and not ("All of" in text):
                                text = text.replace(" District of", " All of District of")
                            
                            if " County" in text:
                                text = text.replace(" County", "")
                            
                            if text.startswith("and "):
                                text = text.replace("and ", "")

                            return text

                        FIPSStrings = []
                        for loc in self.FIPSText:
                            loc2 = loc.split(", ")
                            if len(loc2) == 1:
                                loc3 = filterlocation(loc2[0])
                            elif len(loc2) == 2:
                                loc3 = filterlocation(loc2[0]) + " " + loc2[1]
                            elif len(loc2) > 2:
                                loc3 = filterlocation(" ".join(loc2[:-1])) + " " + loc2[-1]

                            FIPSStrings.append(loc3)

                        self.FIPSText = FIPSStrings

                        if self.strFIPS == "Canada":
                            bigFips = "for"
                        else:
                            bigFips = "for the following counties:"
                        self.startTimeText = ""
                        self.endTimeText = self.endTime.strftime(
                            "%m/%d/%y %H:%M:00 "
                        ) + self.getTZ(dtOffset)
                        if self.org == "CIV":
                            self.orgText = "The Civil Authorities"
                        self.EASText = f"{self.orgText} {'have' if self.org == 'CIV' else 'has'} issued {self.evntText} {bigFips} {self.strFIPS}. Effective Until {self.endTimeText}. ({self.callsign})"


                    elif mode in ["BURK"]:
                        # Burk Mode - United States Old WFO
                        if self.org == "EAS":
                            self.orgText = "A Broadcast station or cable system"
                        elif self.org == "CIV":
                            self.orgText = "The Civil Authorities"
                        elif self.org == "WXR":
                            self.orgText = "The National Weather Service"
                        self.strFIPS = (
                            self.strFIPS[:-1].replace(",", "").replace(";", ",")
                        )
                        self.startTimeText = (
                            self.startTime.strftime("%B %d, %Y").upper()
                            + " at "
                            + self.startTime.strftime("%I:%M %p")
                        )
                        self.endTimeText = self.endTime.strftime("%I:%M %p, %B %d, %Y")
                        self.endTimeText = self.endTimeText.upper()
                        self.evntText = " ".join(self.evntText.split(" ")[1:]).upper()
                        self.EASText = f"{self.orgText} has issued {self.evntText} for the following counties/areas: {self.strFIPS} on {self.startTimeText} effective until {self.endTimeText}."

                    elif mode in ["DAS", "DASDEC", "MONROE", "ONENET", "ONENET SE"]:
                        # DASDEC Software <=v2.9 Mode - United States Old WFO

                        if self.org == "EAS":
                            self.orgText = "A broadcast or cable system"
                        elif self.org == "CIV":
                            self.orgText = "A civil authority"
                        elif self.org == "WXR":
                            self.orgText = "The National Weather Service"
                        elif self.org == "PEP":
                            self.orgText = "THE PRIMARY ENTRY POINT EAS SYSTEM"

                        self.orgText = self.orgText.upper()
                        self.evntText = self.evntText.upper()
                        # Function to process the FIPS string and check for parishes
                        def process_fips_string(fips_string):
                            result = []
                            states = {}  # To track counties/cities/parishes per state
                            only_parishes = True  # Flag to check if only parishes exist
                            parts = [part.strip() for part in fips_string.split(';') if part.strip()]

                            for part in parts:
                                part = re.sub(r'^\s*and\s+', '', part)
                                
                                # Match "City of", "County", or "Parish" and extract name and state
                                match = re.match(r'(City of )?(.*?)( County| Parish)?, (\w{2})', part)
                                state_match = re.match(r'State of (.+)', part)

                                if match:
                                    city_prefix, name, locality_type, state = match.groups()
                                    clean_name = name

                                    # Determine locality type and adjust name
                                    if locality_type == " Parish":
                                        pass  # No suffix needed, keep the name as is
                                    elif city_prefix:
                                        clean_name += " (city)"
                                        only_parishes = False  # Contains city
                                    else:
                                        only_parishes = False  # Contains county

                                    # Track states and their counties/cities/parishes
                                    if state not in states:
                                        states[state] = []
                                    states[state].append((clean_name, state))

                                elif state_match:
                                    # Handle standalone states like "State of Washington"
                                    state_name = state_match.group(1)
                                    result.append(state_name)  # Add state directly to result

                            # Build the result with correct formatting
                            for state, entries in states.items():
                                for i, (name, _) in enumerate(entries):
                                    # Add state abbreviation only to the last entry for the state
                                    if i == len(entries) - 1:
                                        result.append(f"{name}, {state}")
                                    else:
                                        result.append(name)

                            # Join results and format properly
                            final_result = '; '.join(result).replace(' and ', ' ')

                            # Fix "City of" for all independent cities and ensure state formatting
                            final_result = re.sub(r'City of (.*?)( \(city\))?,', r'\1 (city),', final_result)
                            return final_result + ';', only_parishes

                        # Process the input string
                        self.strFIPS, self.onlyParishes = process_fips_string(self.strFIPS)

                        self.strFIPS = self.strFIPS.upper()
                        # Use the appropriate hour format specifier based on the operating system
                        if platform.system() == "Windows":
                            hour_format = "%#I"  # Windows-specific: No leading zero for hour
                        else:
                            hour_format = "%-I"  # Unix-like systems: No leading zero for hour

                        if self.startTime.date() == self.endTime.date():
                            # Same day
                            self.startTimeText = (
                                self.startTime.strftime(f"{hour_format}:%M %p").upper()
                                + " ON" + self.startTime.strftime(" %b %d, %Y").upper()
                            )
                            self.endTimeText = self.endTime.strftime(f"{hour_format}:%M %p").upper()
                        else:
                            # Different days
                            self.startTimeText = (
                                self.startTime.strftime(f"{hour_format}:%M %p").upper()
                                + " ON" + self.startTime.strftime(" %b %d, %Y").upper()
                            )
                            self.endTimeText = (
                                self.endTime.strftime(f"{hour_format}:%M %p").upper()
                                + self.endTime.strftime(" %b %d, %Y").upper()
                            )
                        self.EASText = f"{self.orgText} HAS ISSUED {self.evntText} FOR THE FOLLOWING {'AREAS' if self.onlyParishes else 'COUNTIES/AREAS'}: {self.strFIPS} AT {self.startTimeText} EFFECTIVE UNTIL {self.endTimeText}. MESSAGE FROM {self.callsign.upper()}."

                    elif mode in ["DASV3", "DASDECV3", "MONROEV3", "ONENETV3", "ONENET SEV3"]:
                        # DASDEC Software >=v3.0 Mode - United States Old WFO

                        if self.org == "EAS":
                            self.orgText = "A broadcast or cable system"
                        elif self.org == "CIV":
                            self.orgText = "A civil authority"
                        elif self.org == "WXR":
                            self.orgText = "The National Weather Service"
                        elif self.org == "PEP":
                            self.orgText = "THE PRIMARY ENTRY POINT EAS SYSTEM"

                        self.evntText = self.evntText.upper()

                        # Function to process the FIPS string and check for parishes
                        def process_fips_string(fips_string):
                            result = []
                            states = {}  # To track counties/cities/parishes per state
                            only_parishes = True  # Flag to check if only parishes exist
                            parts = [part.strip() for part in fips_string.split(';') if part.strip()]

                            for part in parts:
                                part = re.sub(r'^\s*and\s+', '', part)

                                # Match "City of", "County", or "Parish" and extract name and state
                                match = re.match(r'(City of )?(.*?)( County| Parish)?, (\w{2})', part)
                                state_match = re.match(r'State of (.+)', part)

                                if match:
                                    city_prefix, name, locality_type, state = match.groups()
                                    clean_name = name

                                    # Determine locality type and adjust name
                                    if locality_type == " Parish":
                                        pass  # No suffix needed, keep the name as is
                                    elif city_prefix:
                                        clean_name += " (city)"
                                        only_parishes = False  # Contains city
                                    else:
                                        only_parishes = False  # Contains county

                                    # Track states and their counties/cities/parishes
                                    if state not in states:
                                        states[state] = []
                                    states[state].append((clean_name, state))

                                elif state_match:
                                    # Handle standalone states like "State of Washington"
                                    state_name = state_match.group(1)
                                    result.append(state_name)  # Add state directly to result

                            # Build the result with correct formatting
                            for state, entries in states.items():
                                for i, (name, _) in enumerate(entries):
                                    # Add state abbreviation only to the last entry for the state
                                    if i == len(entries) - 1:
                                        result.append(f"{name}, {state}")
                                    else:
                                        result.append(name)

                            # Join results and format properly
                            final_result = '; '.join(result).replace(' and ', ' ')

                            # Fix "City of" for all independent cities and ensure state formatting
                            final_result = re.sub(r'City of (.*?)( \(city\))?,', r'\1 (city),', final_result)
                            return final_result + ';', only_parishes

                        # Process the input string
                        self.strFIPS, self.onlyParishes = process_fips_string(self.strFIPS)

                        # Use the appropriate hour format specifier based on the operating system
                        if platform.system() == "Windows":
                            hour_format = "%#I"  # Windows-specific: No leading zero for hour
                        else:
                            hour_format = "%-I"  # Unix-like systems: No leading zero for hour

                        if self.startTime.date() == self.endTime.date():
                            # Same day
                            self.startTimeText = (
                                self.startTime.strftime(f"{hour_format}:%M %p").upper()
                                + " on" + self.startTime.strftime(" %b %d, %Y").upper()
                            )
                            self.endTimeText = self.endTime.strftime(f"{hour_format}:%M %p").upper()
                        else:
                            # Different days
                            self.startTimeText = (
                                self.startTime.strftime(f"{hour_format}:%M %p").upper()
                                + " on" + self.startTime.strftime(" %b %d, %Y").upper()
                            )
                            self.endTimeText = (
                                self.endTime.strftime(f"{hour_format}:%M %p").upper()
                                + self.endTime.strftime(" %b %d, %Y").upper()
                            )

                        self.EASText = f"{self.orgText} has issued {self.evntText} for the following {'areas' if self.onlyParishes else 'counties/areas'}: {self.strFIPS} at {self.startTimeText} Effective until {self.endTimeText}. Message from {self.callsign}."

                    elif mode in ["HollyAnne", "Holly Anne", "Holly-Anne", "HU-961", "MIP-921", "MIP-921e", "HU961", "MIP921", "MIP921e"]:
                        # HollyAnne Mode - United States Old WFO
                        if self.org == "EAS":
                            self.orgText = "CABLE/BROADCAST SYSTEM"
                        elif self.org == "CIV":
                            self.orgText = "AUTHORITIES"
                        elif self.org == "WXR":
                            self.orgText = "NATIONAL WEATHER SERVICE"

                        self.evntText = self.evntText.upper()

                        self.strFIPS = self.strFIPS.replace(',', '')

                        def filterlocation(text):
                            if text.startswith("City of"):
                               text = text.replace("City of ", "") + " CITY"

                            if text.startswith("State of"):
                               text = text.replace("State of", "")
                                
                            if " City of" in text:
                                text = text.replace(" City of", "") + " CITY"

                            if (" State of" in text) and not ("All of" in text):
                                text = text.replace(" State of", "")
                            
                            if " County" in text:
                                text = text.replace(" County", "")
                            
                            if text.startswith("and "):
                                text = text.replace("and ", "AND ")

                            return text

                        # Collect all state abbreviations
                        state_abbreviations = []
                        for loc in self.FIPSText:
                            loc_parts = loc.split(", ")
                            if len(loc_parts) > 1:  # Ensure there is a state abbreviation
                                state_abbreviations.append(loc_parts[-1])

                        unique_states = set(state_abbreviations)  # Check for unique states

                        FIPSStrings = []
                        for loc in self.FIPSText:
                            loc_parts = loc.split(", ")
                            if len(loc_parts) == 2:  # Contains a location and a state abbreviation
                                location = loc_parts[0]
                                state = loc_parts[1]
                                if len(unique_states) == 1:  # If only one state is present
                                    loc3 = filterlocation(location).upper()
                                else:  # If multiple states are present, remove comma but keep state
                                    loc3 = filterlocation(location).upper() + " " + state.upper()
                            elif len(loc_parts) > 2:  # Multiple components, e.g., "City of X, State, XX"
                                loc3 = filterlocation(" ".join(loc_parts[:-1])).upper() + " " + loc_parts[-1].upper()
                            else:  # Single location without state abbreviation
                                loc3 = filterlocation(loc_parts[0]).upper()

                            FIPSStrings.append(loc3)

                        # Update FIPSText and strFIPS
                        self.FIPSText = FIPSStrings
                        self.strFIPS = ", ".join(self.FIPSText).strip()

                        # Remove ", AND" if it exists
                        if ", AND " in self.strFIPS:
                            self.strFIPS = self.strFIPS.replace(", AND ", " AND ")

                        self.startTimeText = self.startTimeText.upper()
                        self.endTimeText = self.endTimeText.upper()
                        
                        self.EASText = f"THE {self.orgText} HAS ISSUED {self.evntText} FOR THE FOLLOWING COUNTIES: {self.strFIPS} BEGINNING AT {self.startTimeText} AND ENDING AT {self.endTimeText}. MESSAGE FROM {self.callsign}."

                    elif mode in ["EAS1CG", "EAS-1", "EAS1", "EAS1-CG", "EAS-1CG", "Gorman-Redlich", "GormanRedlich", "Gorman Redlich"]:
                        # Gorman Redlich Mode - United States Old WFO
                        self.evntText = self.evntText.upper()

                        # Use the appropriate format specifier based on the operating system
                        if platform.system() == "Windows":
                            hour_format = "%#I"  # Windows-specific: No leading zero for hour
                        else:
                            hour_format = "%-I"  # Unix-like systems: No leading zero for hour

                        if self.startTime.date() == self.endTime.date():
                            # Same day
                            self.startTimeText = self.startTime.strftime(
                                f"{hour_format}:%M %p ON %B %d, %Y"
                            ).upper()
                            self.endTimeText = self.endTime.strftime(
                                f"{hour_format}:%M %p"
                            ).upper()
                        else:
                            # Different days
                            self.startTimeText = self.startTime.strftime(
                                f"{hour_format}:%M %p ON %B %d, %Y"
                            ).upper()
                            self.endTimeText = self.endTime.strftime(
                                f"{hour_format}:%M %p ON %B %d, %Y"
                            ).upper()

                        def filterlocation(text):
                            if text.startswith("City of"):
                               text = text.replace("City of ", "") + " CITY"

                            if text.startswith("State of"):
                               text = text.replace("State of", "")
                                
                            if " City of" in text:
                                text = text.replace(" City of", "") + " CITY"

                            if (" State of" in text) and not ("All of" in text):
                                text = text.replace(" State of", "")
                            
                            if " County" in text:
                                text = text.replace(" County", "")
                            
                            if text.startswith("and "):
                                text = text.replace("and ", "AND ")

                            return text
                        
                        FIPSStrings = []
                        for loc in self.FIPSText:
                            loc_parts = loc.split(", ")
                            if len(loc_parts) == 2:  # Contains a location and a state abbreviation
                                location = loc_parts[0]
                                state = loc_parts[1]
                                loc3 = filterlocation(location).upper() + " " + state.upper()
                            elif len(loc_parts) > 2:  # Multiple components, e.g., "City of X, State, XX"
                                loc3 = filterlocation(" ".join(loc_parts[:-1])).upper() + " " + loc_parts[-1].upper()
                            else:  # Single location without state abbreviation
                                loc3 = filterlocation(loc_parts[0]).upper()

                            FIPSStrings.append(loc3)

                        # Update FIPSText and strFIPS
                        self.FIPSText = FIPSStrings
                        self.strFIPS = ", ".join(self.FIPSText).strip()

                        # Remove ", AND" if it exists
                        if ", AND " in self.strFIPS:
                            self.strFIPS = self.strFIPS.replace(", AND ", " AND ")


                        self.EASText = f"{self.evntText} HAS BEEN ISSUED FOR {self.strFIPS} AT {self.startTimeText} EFFECTIVE UNTIL {self.endTimeText}. MESSAGE FROM {self.callsign}."

                    else:
                        if self.org == "WXR":
                            if self.WFOText == "Unknown WFO;" or self.StateInSAME:
                                self.orgText = "The National Weather Service"
                            else:
                                self.orgText = f"The National Weather Service in {self.WFOText}"
                        self.EASText = f"{self.orgText} has issued {self.evntText} for {self.strFIPS} beginning at {self.startTimeText} and ending at {self.endTimeText}. Message from {self.callsign}."
    
                else:
                    # United States New Weather Forecasting Office Mode (Referred to as United States New WFO)

                    # Function to get WFO details for a given WFO number - United States New WFO
                    def get_wfo_details(wfo_number):
                        wfo_info = ccl2["WFOs"].get(wfo_number, [])
                        if not wfo_info:
                            return None
                        
                        return {
                            "Forecast_office": wfo_info[0]["Forecast_office"],
                            "State": wfo_info[0]["State"],
                            "Office_call_sign": wfo_info[0]["Office_call_sign"],
                            "Address": wfo_info[0]["Address"],
                            "Phone_number": wfo_info[0]["PNum"]
                        }

                    # Parsing the JSON data - United States New WFO
                    parsed_data = {}

                    for fips_code, entries in ccl2["SAME"].items():
                        wfo_list = []
                        nwr_freq = []
                        nwr_callsign = []
                        nwr_pwr = []
                        nwr_sitename = []
                        nwr_siteloc = []
                        nwr_sitestate = []
                        nwr_lat = []
                        nwr_lon = []
                        
                        # Set to track combinations of frequency, callsign, and power to avoid duplicates - United States New WFO
                        freq_callsign_pwr_set = set()
                        
                        # Set to track combinations of sitename and siteloc to avoid duplicates - United States New WFO
                        sitename_siteloc_set = set()
                        
                        for entry in entries:
                            wfo_number = entry["WFO"]
                            
                            # Get the WFO details - United States New WFO
                            wfo_details = get_wfo_details(wfo_number)
                            if wfo_details and wfo_details not in wfo_list:
                                wfo_list.append(wfo_details)
                            
                            # Check for duplicates based on frequency, callsign, and power - United States New WFO
                            freq_callsign_pwr_pair = (entry["FREQ"], entry["CALLSIGN"], entry["PWR"])
                            if freq_callsign_pwr_pair not in freq_callsign_pwr_set:
                                freq_callsign_pwr_set.add(freq_callsign_pwr_pair)
                                nwr_freq.append(entry["FREQ"])
                                nwr_callsign.append(entry["CALLSIGN"])
                                nwr_pwr.append(entry["PWR"])
                            
                            # Check for duplicates based on sitename and siteloc - United States New WFO
                            sitename_siteloc_pair = (entry["SITENAME"], entry["SITELOC"])
                            if sitename_siteloc_pair not in sitename_siteloc_set:
                                sitename_siteloc_set.add(sitename_siteloc_pair)
                                nwr_sitename.append(entry["SITENAME"])
                                nwr_siteloc.append(entry["SITELOC"])
                                nwr_sitestate.append(entry["SITESTATE"])
                            
                            if entry["LAT"] not in nwr_lat:
                                nwr_lat.append(entry["LAT"])
                            if entry["LON"] not in nwr_lon:
                                nwr_lon.append(entry["LON"])
                        
                        # Combine NWR data into semicolon-separated strings - United States New WFO
                        parsed_data[fips_code] = {
                            "WFOs": wfo_list,
                            "NWR_FREQ": "; ".join(nwr_freq),
                            "NWR_CALLSIGN": "; ".join(nwr_callsign),
                            "NWR_PWR": "; ".join(nwr_pwr),
                            "NWR_SITENAME": "; ".join(nwr_sitename),
                            "NWR_SITELOC": "; ".join(nwr_siteloc),
                            "NWR_SITESTATE": "; ".join(nwr_sitestate),
                            # Updated NWR_SITE logic to avoid duplicate site name and site location
                            "NWR_SITE": "; ".join(f"{siteName}, {siteState} ({siteLoc})" for siteName, siteLoc, siteState in zip(nwr_sitename, nwr_siteloc, nwr_sitestate)),
                            "NWR_COORDINATES": "; ".join(f"{lat}, {lon}" for lat, lon in zip(nwr_lat, nwr_lon))
                        }


                    self.WFO = []
                    self.WFOText = []
                    self.WFOForecastOffice = []
                    self.WFOAddress = []
                    self.WFOCallsign = []
                    self.WFOPhoneNumber = []
                    self.NWR_FREQ = []
                    self.NWR_CALLSIGN = []
                    self.NWR_PWR = []
                    self.NWR_SITENAME = []
                    self.NWR_SITELOC = []
                    self.NWR_SITESTATE = []
                    self.NWR_SITE = []
                    self.NWR_COORDINATES = []

                    ## CHECKING FOR VALID SAME - United States New WFO
                    if sameData == "":
                        raise MissingSAME()
                    elif sameData.startswith("NNNN"):
                        self.EASText = "End Of Message"
                        return
                    elif not sameData.startswith("ZCZC"):
                        raise InvalidSAME(sameData, message='"ZCZC" Start string missing')
                    else:
                        eas = "".join(
                            sameData.replace("ZCZC-", "").replace("+", "-")
                        ).split("-")
                        eas.remove("")

                        for i in eas[2:-3]:
                            try:
                                assert len(i) == 6
                                assert self.__isInt__(i) == True
                                ## FIPS CODE - United States New WFO
                                if i not in self.FIPS:
                                    self.FIPS.append(str(i))
                            except AssertionError:
                                raise InvalidSAME("Invalid codes in FIPS data")

                        for i in sorted(self.FIPS):
                            try:
                                subdiv = stats["SUBDIV"][i[0]]
                                same = stats["SAME"][i[1:]]
                                self.FIPSText.append(
                                    f"{subdiv + ' ' if subdiv != '' else ''}{same}" 
                                )
                                
                                try:
                                    if(str(eas[0]) == "WXR") and ("State" not in same):
                                        wfolist = parsed_data[i[1:]]["WFOs"]

                                        for wfos in wfolist:
                                            if wfos:
                                                ## WXR LOCALITY - United States New WFO
                                                self.WFOText.append(
                                                    f'{wfos["Forecast_office"]}, {wfos["State"]} ({wfos["Office_call_sign"]})'
                                                )

                                                self.WFO.append(
                                                    f'{wfos["Forecast_office"]}, {wfos["State"]} ({wfos["Office_call_sign"]})'
                                                )

                                                self.WFOForecastOffice.append(
                                                    f'{wfos["Forecast_office"]}'
                                                )
                                                
                                                self.WFOAddress.append(
                                                    f'{wfos["Address"]}'
                                                )

                                                self.WFOCallsign.append(
                                                    f'{wfos["Office_call_sign"]}'
                                                )

                                                self.WFOPhoneNumber.append(
                                                    f'{wfos["Phone_number"]}'
                                                )

                                                self.NWR_FREQ.append(
                                                    f'{parsed_data[i[1:]]["NWR_FREQ"]}'
                                                )

                                                self.NWR_CALLSIGN.append(
                                                    f'{parsed_data[i[1:]]["NWR_CALLSIGN"]}'
                                                )

                                                self.NWR_PWR.append(
                                                    f'{parsed_data[i[1:]]["NWR_PWR"]}'
                                                )

                                                self.NWR_SITENAME.append(
                                                    f'{parsed_data[i[1:]]["NWR_SITENAME"]}'
                                                )

                                                self.NWR_SITELOC.append(
                                                    f'{parsed_data[i[1:]]["NWR_SITELOC"]}'
                                                )

                                                self.NWR_SITESTATE.append(
                                                    f'{parsed_data[i[1:]]["NWR_SITESTATE"]}'
                                                )

                                                self.NWR_SITE.append(
                                                    f'{parsed_data[i[1:]]["NWR_SITE"]}'
                                                )

                                                self.NWR_COORDINATES.append(
                                                    f'{parsed_data[i[1:]]["NWR_COORDINATES"]}'
                                                )

                                            else:
                                                self.WFO.append(f"Unknown WFO for FIPS Code {i}")
                                                self.WFOText.append(f"Unknown WFO for FIPS Code {i}")
                                except KeyError:
                                    try:
                                        if(str(eas[0]) == "WXR") and ("State" not in same):
                                            ## WXR LOCALITY - United States New WFO
                                            wfo = locality2["SAME"][i[1:]][0]["wfo"]
                                            if wfo:
                                                self.WFOText.append(
                                                    f"{wfo}"
                                                )
                                                self.WFO.append(
                                                    f"{wfo}"
                                                )
                                            else:
                                                self.WFO.append(f"Unknown WFO for FIPS Code {i}")
                                                self.WFOText.append(f"Unknown WFO for FIPS Code {i}")
                                    except KeyError:
                                        self.WFO.append(f"Unknown WFO for FIPS Code {i}")
                                        self.WFOText.append(f"Unknown WFO for FIPS Code {i}")
                                    except Exception as E:
                                        raise InvalidSAME(
                                            self.WFOText, message=f"Error in WFO Text ({str(E)})"
                                        )
                                    
                                except Exception as E:
                                    raise InvalidSAME(
                                        self.WFOText, message=f"Error in WFO Text ({str(E)})"
                                    )
                                
                            except KeyError:
                                self.FIPSText.append(f"FIPS Code {i}")
                                self.WFO.append(f"Unknown WFO for FIPS Code {i}")
                                self.WFOText.append(f"Unknown WFO for FIPS Code {i}")
                                
                            except Exception as E:
                                raise InvalidSAME(
                                    self.FIPS, message=f"Error in FIPS Code ({str(E)})"
                                )
                            
                        if len(self.FIPSText) > 1:
                            FIPSText = self.FIPSText
                            FIPSText[-1] = f"and {FIPSText[-1]}"
                        self.strFIPS = "; ".join(self.FIPSText).strip() + ";"

                        ## WXR LOCALITY MULTIPLE - United States New WFO
                        if(str(eas[0]) == "WXR"):
                            if self.WFOText != "":
                                if len(self.WFOText) > 1:
                                    p = []
                                    for values in self.WFOText:
                                        if values not in p:
                                            p.append(values)
                                    if(len(p) > 1):
                                        p[-1] = f"and {p[-1]}"
                                    self.WFOText = "; ".join(p).strip() + ";"
                                else:
                                    p = self.WFOText[0]
                                    self.WFOText = str(self.WFOText[0])+";"
                            if self.WFO != "":
                                if len(self.WFO) > 1:
                                    p = []
                                    for values in self.WFO:
                                        if values not in p:
                                            p.append(values)
                                    if(len(p) > 1):
                                        p[-1] = f"and {p[-1]}"
                                    self.WFO = "; ".join(p).strip() + ";"
                                else:
                                    p = self.WFO[0]
                                    self.WFO = str(self.WFO[0])+";"
                    

                    ## TIME CODE - United States New WFO
                    try:
                        self.purge = [eas[-3][:2], eas[-3][2:]]
                    except IndexError:
                        raise InvalidSAME(self.purge, message="Purge Time not HHMM.")
                    self.timeStamp = eas[-2]
                    utc = DT.utcnow()
                    if timeZone == None:
                        dtOffset = 0
                    if timeZoneTZ == None:
                        dtOffset = 0
                    if timeZone != None:
                        dtOffset = -timeZone * 3600
                    if timeZoneTZ != None:
                        timezone = pytz.timezone(timeZoneTZ)
                        naive_now = DT.now()
                        tz_offset = timezone.utcoffset(naive_now)
                        total_seconds = tz_offset.total_seconds()
                        hour_offset = int(total_seconds // 3600)
                        utc_offset = f"{hour_offset:+d}"  # "+6" or "-3"
                        dtOffset = -int(utc_offset) * 3600

                    try:
                        alertStartEpoch = (
                            DT.strptime(self.timeStamp, "%j%H%M")
                            .replace(year=utc.year)
                            .timestamp()
                        )
                    except ValueError:
                        raise InvalidSAME(
                            self.timeStamp, message="Timestamp not JJJHHMM."
                        )
                    alertEndOffset = (int(self.purge[0]) * 3600) + (
                        int(self.purge[1]) * 60
                    )
                    alertEndEpoch = alertStartEpoch + alertEndOffset

                    try:
                        self.startTime = DT.fromtimestamp(alertStartEpoch - dtOffset)
                        self.endTime = DT.fromtimestamp(alertEndEpoch - dtOffset)

                        today = DT.fromtimestamp(alertStartEpoch - dtOffset).today().date()

                        current_year = DT.fromtimestamp(alertStartEpoch - dtOffset).year
                        is_leap_year = calendar.isleap(current_year)

                        if is_leap_year and today > DT(today.year, 2, 29).date():
                            self.startTime -= timedelta(days=1)  # Adjust for leap year
                            self.endTime -= timedelta(days=1)  # Adjust for leap year
                            
                        if self.startTime.day == self.endTime.day:
                            self.startTimeText = self.startTime.strftime("%I:%M %p")
                            self.endTimeText = self.endTime.strftime("%I:%M %p")
                        elif self.startTime.year == self.endTime.year:
                            self.startTimeText = self.startTime.strftime(
                                "%I:%M %p %B %d"
                            )
                            self.endTimeText = self.endTime.strftime("%I:%M %p %B %d")
                        else:
                            self.startTimeText = self.startTime.strftime(
                                "%I:%M %p %B %d, %Y"
                            )
                            self.endTimeText = self.endTime.strftime(
                                "%I:%M %p %B %d, %Y"
                            )
                    except Exception as E:
                        raise InvalidSAME(
                            self.timeStamp,
                            message=f"Error in Time Conversion ({str(E)})",
                        )


                    ## ORG / EVENT CODE - United States New WFO
                    try:
                        self.org = str(eas[0])
                        self.evnt = str(eas[1])
                        try:
                            assert len(eas[0]) == 3
                        except AssertionError:
                            raise InvalidSAME("Originator is an invalid length")
                        try:
                            assert len(eas[1]) == 3
                        except AssertionError:
                            raise InvalidSAME("Event Code is an invalid length")
                        try:
                            self.orgText = stats["ORGS"][self.org]
                        except:
                            self.orgText = (
                                f"An Unknown Originator ({self.org});"
                            )
                        try:
                            self.evntText = stats["EVENTS"][self.evnt]
                        except:
                            self.evntText = f"an Unknown Event ({self.evnt})"
                    except Exception as E:
                        raise InvalidSAME(
                            [self.org, self.evnt],
                            message=f"Error in ORG / EVNT Decoding ({str(E)})",
                        )

                    ## CALLSIGN CODE - United States New WFO
                    self.callsign = eas[-1].strip()

                    ## FINAL TEXT - United States New WFO
                    if mode == "TFT":
                        # TFT Mode - United States New WFO
                        self.strFIPS = (
                            self.strFIPS[:-1]
                            .replace(",", "")
                            .replace(";", ",")
                            .replace("FIPS Code", "AREA")
                        )
                        self.startTimeText = self.startTime.strftime(
                            "%I:%M %p ON %b %d, %Y"
                        )
                        self.endTimeText = (
                            self.endTime.strftime("%I:%M %p")
                            if self.startTime.day == self.endTime.day
                            else self.endTime.strftime("%I:%M %p ON %b %d, %Y")
                        )
                        if self.org == "EAS" or self.evnt in ["NPT", "EAN"]:
                            self.EASText = f"{self.evntText} has been issued for the following counties/areas: {self.strFIPS} at {self.startTimeText} effective until {self.endTimeText}. message from {self.callsign}.".upper()
                        else:
                            self.EASText = f"{self.orgText} has issued {self.evntText} for the following counties/areas: {self.strFIPS} at {self.startTimeText} effective until {self.endTimeText}. message from {self.callsign}.".upper()

                    elif mode.startswith("SAGE"):
                        # SAGE Mode - United States New WFO
                        if self.org == "CIV":
                            self.orgText = "The Civil Authorities"
                        self.strFIPS = self.strFIPS[:-1].replace(";", ",")
                        self.startTimeText = self.startTime.strftime(
                            "%I:%M %p"
                        ).lower()
                        self.endTimeText = self.endTime.strftime("%I:%M %p").lower()
                        if self.startTime.day != self.endTime.day:
                            self.startTimeText += self.startTime.strftime(" %a %b %d")
                            self.endTimeText += self.endTime.strftime(" %a %b %d")
                        if mode.endswith("DIGITAL"):
                            self.EASText = f"{self.orgText} {'have' if self.org == 'CIV' else 'has'} issued {self.evntText} for {self.strFIPS} beginning at {self.startTimeText} and ending at {self.endTimeText} ({self.callsign})"
                        else:
                            if self.org == "EAS":
                                self.orgText = "A Broadcast station or cable system"
                            self.EASText = f"{self.orgText} {'have' if self.org == 'CIV' else 'has'} issued {self.evntText} for {self.strFIPS} beginning at {self.startTimeText} and ending at {self.endTimeText} ({self.callsign})"

                    elif mode in ["TRILITHIC", "VIAVI", "EASY"]:
                        # Trilithic - United States New WFO
                        def process_location(text):
                            
                            if text.startswith("City of"):
                                text = text.replace("City of", "") + " (city)"

                            if text.startswith("State of"):
                               text = text.replace("State of", "All of")

                            if text.startswith("District of"):
                                text = text.replace("District of", "All of District of")
                                
                            if " City of" in text:
                                text = text.replace(" City of", "") + " (city)"

                            if (" State of" in text) and not ("All of" in text):
                                text = text.replace(" State of", " All of")

                            if (" District of" in text) and not ("All of" in text):
                                text = text.replace(" District of", " All of District of")
                            
                            if " County" in text:
                                text = text.replace(" County", "")
                            
                            if text.startswith("and "):
                                text = text.replace("and ", "")
                            
                            if "; " in text:
                                text = text.replace("; ", " - ")
                            
                            return text

                        strFIPS_value = (
                            "".join(self.strFIPS) if isinstance(self.strFIPS, types.GeneratorType) else self.strFIPS
                        )

                        self.strFIPS = (
                            ", ".join(map(process_location, map(str.strip, strFIPS_value[:-1].split(", "))))
                            if "000000" not in self.FIPS
                            else "Canada"
                        )

                        self.strFIPS = self.strFIPS.replace(',', '').replace(' and', '')

                        def filterlocation(text):
                            if text.startswith("City of"):
                               text = text.replace("City of ", "") + " (city)"

                            if text.startswith("State of"):
                               text = text.replace("State of", "All of")

                            if text.startswith("District of"):
                                text = text.replace("District of", "All of District of")
                                
                            if " City of" in text:
                                text = text.replace(" City of", "") + " (city)"

                            if (" State of" in text) and not ("All of" in text):
                                text = text.replace(" State of", " All of")

                            if (" District of" in text) and not ("All of" in text):
                                text = text.replace(" District of", " All of District of")
                            
                            if " County" in text:
                                text = text.replace(" County", "")
                            
                            if text.startswith("and "):
                                text = text.replace("and ", "")

                            return text

                        FIPSStrings = []
                        for loc in self.FIPSText:
                            loc2 = loc.split(", ")
                            if len(loc2) == 1:
                                loc3 = filterlocation(loc2[0])
                            elif len(loc2) == 2:
                                loc3 = filterlocation(loc2[0]) + " " + loc2[1]
                            elif len(loc2) > 2:
                                loc3 = filterlocation(" ".join(loc2[:-1])) + " " + loc2[-1]

                            FIPSStrings.append(loc3)

                        self.FIPSText = FIPSStrings

                        if self.strFIPS == "Canada":
                            bigFips = "for"
                        else:
                            bigFips = "for the following counties:"
                        self.startTimeText = ""
                        self.endTimeText = self.endTime.strftime(
                            "%m/%d/%y %H:%M:00 "
                        ) + self.getTZ(dtOffset)
                        if self.org == "CIV":
                            self.orgText = "The Civil Authorities"
                        self.EASText = f"{self.orgText} {'have' if self.org == 'CIV' else 'has'} issued {self.evntText} {bigFips} {self.strFIPS}. Effective Until {self.endTimeText}. ({self.callsign})"

                    elif mode in ["BURK"]:
                        # Burk Mode - United States New WFO
                        if self.org == "EAS":
                            self.orgText = "A Broadcast station or cable system"
                        elif self.org == "CIV":
                            self.orgText = "The Civil Authorities"
                        elif self.org == "WXR":
                            self.orgText = "The National Weather Service"
                        self.strFIPS = (
                            self.strFIPS[:-1].replace(",", "").replace(";", ",")
                        )
                        self.startTimeText = (
                            self.startTime.strftime("%B %d, %Y").upper()
                            + " at "
                            + self.startTime.strftime("%I:%M %p")
                        )
                        self.endTimeText = self.endTime.strftime("%I:%M %p, %B %d, %Y")
                        self.endTimeText = self.endTimeText.upper()
                        self.evntText = " ".join(self.evntText.split(" ")[1:]).upper()
                        self.EASText = f"{self.orgText} has issued {self.evntText} for the following counties/areas: {self.strFIPS} on {self.startTimeText} effective until {self.endTimeText}."

                    elif mode in ["DAS", "DASDEC", "MONROE", "ONENET", "ONENET SE"]:
                        # DASDEC Software <=v2.9 Mode - United States New WFO

                        if self.org == "EAS":
                            self.orgText = "A broadcast or cable system"
                        elif self.org == "CIV":
                            self.orgText = "A civil authority"
                        elif self.org == "WXR":
                            self.orgText = "The National Weather Service"
                        elif self.org == "PEP":
                            self.orgText = "THE PRIMARY ENTRY POINT EAS SYSTEM"
                            
                        self.orgText = self.orgText.upper()
                        self.evntText = self.evntText.upper()
                        # Function to process the FIPS string and check for parishes
                        def process_fips_string(fips_string):
                            result = []
                            states = {}  # To track counties/cities/parishes per state
                            only_parishes = True  # Flag to check if only parishes exist
                            parts = [part.strip() for part in fips_string.split(';') if part.strip()]

                            for part in parts:
                                part = re.sub(r'^\s*and\s+', '', part)
                                
                                # Match "City of", "County", or "Parish" and extract name and state
                                match = re.match(r'(City of )?(.*?)( County| Parish)?, (\w{2})', part)
                                state_match = re.match(r'State of (.+)', part)

                                if match:
                                    city_prefix, name, locality_type, state = match.groups()
                                    clean_name = name

                                    # Determine locality type and adjust name
                                    if locality_type == " Parish":
                                        pass  # No suffix needed, keep the name as is
                                    elif city_prefix:
                                        clean_name += " (city)"
                                        only_parishes = False  # Contains city
                                    else:
                                        only_parishes = False  # Contains county

                                    # Track states and their counties/cities/parishes
                                    if state not in states:
                                        states[state] = []
                                    states[state].append((clean_name, state))

                                elif state_match:
                                    # Handle standalone states like "State of Washington"
                                    state_name = state_match.group(1)
                                    result.append(state_name)  # Add state directly to result

                            # Build the result with correct formatting
                            for state, entries in states.items():
                                for i, (name, _) in enumerate(entries):
                                    # Add state abbreviation only to the last entry for the state
                                    if i == len(entries) - 1:
                                        result.append(f"{name}, {state}")
                                    else:
                                        result.append(name)

                            # Join results and format properly
                            final_result = '; '.join(result).replace(' and ', ' ')

                            # Fix "City of" for all independent cities and ensure state formatting
                            final_result = re.sub(r'City of (.*?)( \(city\))?,', r'\1 (city),', final_result)
                            return final_result + ';', only_parishes

                        # Process the input string
                        self.strFIPS, self.onlyParishes = process_fips_string(self.strFIPS)

                        self.strFIPS = self.strFIPS.upper()

                        # Use the appropriate hour format specifier based on the operating system
                        if platform.system() == "Windows":
                            hour_format = "%#I"  # Windows-specific: No leading zero for hour
                        else:
                            hour_format = "%-I"  # Unix-like systems: No leading zero for hour

                        if self.startTime.date() == self.endTime.date():
                            # Same day
                            self.startTimeText = (
                                self.startTime.strftime(f"{hour_format}:%M %p").upper()
                                + " ON" + self.startTime.strftime(" %b %d, %Y").upper()
                            )
                            self.endTimeText = self.endTime.strftime(f"{hour_format}:%M %p").upper()
                        else:
                            # Different days
                            self.startTimeText = (
                                self.startTime.strftime(f"{hour_format}:%M %p").upper()
                                + " ON" + self.startTime.strftime(" %b %d, %Y").upper()
                            )
                            self.endTimeText = (
                                self.endTime.strftime(f"{hour_format}:%M %p").upper()
                                + self.endTime.strftime(" %b %d, %Y").upper()
                            )

                        self.EASText = f"{self.orgText} HAS ISSUED {self.evntText} FOR THE FOLLOWING {'AREAS' if self.onlyParishes else 'COUNTIES/AREAS'}: {self.strFIPS} AT {self.startTimeText} EFFECTIVE UNTIL {self.endTimeText}. MESSAGE FROM {self.callsign.upper()}."

                    elif mode in ["DASV3", "DASDECV3", "MONROEV3", "ONENETV3", "ONENET SEV3"]:
                        # DASDEC Software >=v3.0 Mode - United States New WFO

                        if self.org == "EAS":
                            self.orgText = "A broadcast or cable system"
                        elif self.org == "CIV":
                            self.orgText = "A civil authority"
                        elif self.org == "WXR":
                            self.orgText = "The National Weather Service"
                        elif self.org == "PEP":
                            self.orgText = "THE PRIMARY ENTRY POINT EAS SYSTEM"

                        self.evntText = self.evntText.upper()

                        # Function to process the FIPS string and check for parishes
                        def process_fips_string(fips_string):
                            result = []
                            states = {}  # To track counties/cities/parishes per state
                            only_parishes = True  # Flag to check if only parishes exist
                            parts = [part.strip() for part in fips_string.split(';') if part.strip()]

                            for part in parts:
                                part = re.sub(r'^\s*and\s+', '', part)

                                # Match "City of", "County", or "Parish" and extract name and state
                                match = re.match(r'(City of )?(.*?)( County| Parish)?, (\w{2})', part)
                                state_match = re.match(r'State of (.+)', part)

                                if match:
                                    city_prefix, name, locality_type, state = match.groups()
                                    clean_name = name

                                    # Determine locality type and adjust name
                                    if locality_type == " Parish":
                                        pass  # No suffix needed, keep the name as is
                                    elif city_prefix:
                                        clean_name += " (city)"
                                        only_parishes = False  # Contains city
                                    else:
                                        only_parishes = False  # Contains county

                                    # Track states and their counties/cities/parishes
                                    if state not in states:
                                        states[state] = []
                                    states[state].append((clean_name, state))

                                elif state_match:
                                    # Handle standalone states like "State of Washington"
                                    state_name = state_match.group(1)
                                    result.append(state_name)  # Add state directly to result

                            # Build the result with correct formatting
                            for state, entries in states.items():
                                for i, (name, _) in enumerate(entries):
                                    # Add state abbreviation only to the last entry for the state
                                    if i == len(entries) - 1:
                                        result.append(f"{name}, {state}")
                                    else:
                                        result.append(name)

                            # Join results and format properly
                            final_result = '; '.join(result).replace(' and ', ' ')

                            # Fix "City of" for all independent cities and ensure state formatting
                            final_result = re.sub(r'City of (.*?)( \(city\))?,', r'\1 (city),', final_result)
                            return final_result + ';', only_parishes

                        # Process the input string
                        self.strFIPS, self.onlyParishes = process_fips_string(self.strFIPS)

                        # Use the appropriate hour format specifier based on the operating system
                        if platform.system() == "Windows":
                            hour_format = "%#I"  # Windows-specific: No leading zero for hour
                        else:
                            hour_format = "%-I"  # Unix-like systems: No leading zero for hour

                        if self.startTime.date() == self.endTime.date():
                            # Same day
                            self.startTimeText = (
                                self.startTime.strftime(f"{hour_format}:%M %p").upper()
                                + " on" + self.startTime.strftime(" %b %d, %Y").upper()
                            )
                            self.endTimeText = self.endTime.strftime(f"{hour_format}:%M %p").upper()
                        else:
                            # Different days
                            self.startTimeText = (
                                self.startTime.strftime(f"{hour_format}:%M %p").upper()
                                + " on" + self.startTime.strftime(" %b %d, %Y").upper()
                            )
                            self.endTimeText = (
                                self.endTime.strftime(f"{hour_format}:%M %p").upper()
                                + self.endTime.strftime(" %b %d, %Y").upper()
                            )

                        self.EASText = f"{self.orgText} has issued {self.evntText} for the following {'areas' if self.onlyParishes else 'counties/areas'}: {self.strFIPS} at {self.startTimeText} Effective until {self.endTimeText}. Message from {self.callsign}."

                    elif mode in ["HollyAnne", "Holly Anne", "Holly-Anne", "HU-961", "MIP-921", "MIP-921e", "HU961", "MIP921", "MIP921e"]:
                        # HollyAnne Mode - United States New WFO
                        if self.org == "EAS":
                            self.orgText = "CABLE/BROADCAST SYSTEM"
                        elif self.org == "CIV":
                            self.orgText = "AUTHORITIES"
                        elif self.org == "WXR":
                            self.orgText = "NATIONAL WEATHER SERVICE"

                        self.evntText = self.evntText.upper()

                        self.strFIPS = self.strFIPS.replace(',', '')

                        def filterlocation(text):
                            if text.startswith("City of"):
                               text = text.replace("City of ", "") + " CITY"

                            if text.startswith("State of"):
                               text = text.replace("State of", "")
                                
                            if " City of" in text:
                                text = text.replace(" City of", "") + " CITY"

                            if (" State of" in text) and not ("All of" in text):
                                text = text.replace(" State of", "")
                            
                            if " County" in text:
                                text = text.replace(" County", "")
                            
                            if text.startswith("and "):
                                text = text.replace("and ", "AND ")

                            return text

                        # Collect all state abbreviations
                        state_abbreviations = []
                        for loc in self.FIPSText:
                            loc_parts = loc.split(", ")
                            if len(loc_parts) > 1:  # Ensure there is a state abbreviation
                                state_abbreviations.append(loc_parts[-1])

                        unique_states = set(state_abbreviations)  # Check for unique states

                        FIPSStrings = []
                        for loc in self.FIPSText:
                            loc_parts = loc.split(", ")
                            if len(loc_parts) == 2:  # Contains a location and a state abbreviation
                                location = loc_parts[0]
                                state = loc_parts[1]
                                if len(unique_states) == 1:  # If only one state is present
                                    loc3 = filterlocation(location).upper()
                                else:  # If multiple states are present, remove comma but keep state
                                    loc3 = filterlocation(location).upper() + " " + state.upper()
                            elif len(loc_parts) > 2:  # Multiple components, e.g., "City of X, State, XX"
                                loc3 = filterlocation(" ".join(loc_parts[:-1])).upper() + " " + loc_parts[-1].upper()
                            else:  # Single location without state abbreviation
                                loc3 = filterlocation(loc_parts[0]).upper()

                            FIPSStrings.append(loc3)

                        # Update FIPSText and strFIPS
                        self.FIPSText = FIPSStrings
                        self.strFIPS = ", ".join(self.FIPSText).strip()

                        # Remove ", AND" if it exists
                        if ", AND " in self.strFIPS:
                            self.strFIPS = self.strFIPS.replace(", AND ", " AND ")

                        self.startTimeText = self.startTimeText.upper()
                        self.endTimeText = self.endTimeText.upper()
                        
                        self.EASText = f"THE {self.orgText} HAS ISSUED {self.evntText} FOR THE FOLLOWING COUNTIES: {self.strFIPS} BEGINNING AT {self.startTimeText} AND ENDING AT {self.endTimeText}. MESSAGE FROM {self.callsign}."

                    elif mode in ["EAS1CG", "EAS-1", "EAS1", "EAS1-CG", "EAS-1CG", "Gorman-Redlich", "GormanRedlich", "Gorman Redlich"]:
                        # Gorman Redlich Mode - United States New WFO
                        self.evntText = self.evntText.upper()

                        # Use the appropriate format specifier based on the operating system
                        if platform.system() == "Windows":
                            hour_format = "%#I"  # Windows-specific: No leading zero for hour
                        else:
                            hour_format = "%-I"  # Unix-like systems: No leading zero for hour

                        if self.startTime.date() == self.endTime.date():
                            # Same day
                            self.startTimeText = self.startTime.strftime(
                                f"{hour_format}:%M %p ON %B %d, %Y"
                            ).upper()
                            self.endTimeText = self.endTime.strftime(
                                f"{hour_format}:%M %p"
                            ).upper()
                        else:
                            # Different days
                            self.startTimeText = self.startTime.strftime(
                                f"{hour_format}:%M %p ON %B %d, %Y"
                            ).upper()
                            self.endTimeText = self.endTime.strftime(
                                f"{hour_format}:%M %p ON %B %d, %Y"
                            ).upper()

                        def filterlocation(text):
                            if text.startswith("City of"):
                               text = text.replace("City of ", "") + " CITY"

                            if text.startswith("State of"):
                               text = text.replace("State of", "")
                                
                            if " City of" in text:
                                text = text.replace(" City of", "") + " CITY"

                            if (" State of" in text) and not ("All of" in text):
                                text = text.replace(" State of", "")
                            
                            if " County" in text:
                                text = text.replace(" County", "")
                            
                            if text.startswith("and "):
                                text = text.replace("and ", "AND ")

                            return text
                        
                        FIPSStrings = []
                        for loc in self.FIPSText:
                            loc_parts = loc.split(", ")
                            if len(loc_parts) == 2:  # Contains a location and a state abbreviation
                                location = loc_parts[0]
                                state = loc_parts[1]
                                loc3 = filterlocation(location).upper() + " " + state.upper()
                            elif len(loc_parts) > 2:  # Multiple components, e.g., "City of X, State, XX"
                                loc3 = filterlocation(" ".join(loc_parts[:-1])).upper() + " " + loc_parts[-1].upper()
                            else:  # Single location without state abbreviation
                                loc3 = filterlocation(loc_parts[0]).upper()

                            FIPSStrings.append(loc3)

                        # Update FIPSText and strFIPS
                        self.FIPSText = FIPSStrings
                        self.strFIPS = ", ".join(self.FIPSText).strip()

                        # Remove ", AND" if it exists
                        if ", AND " in self.strFIPS:
                            self.strFIPS = self.strFIPS.replace(", AND ", " AND ")

                        self.EASText = f"{self.evntText} HAS BEEN ISSUED FOR {self.strFIPS} AT {self.startTimeText} EFFECTIVE UNTIL {self.endTimeText}. MESSAGE FROM {self.callsign}."

                    else:
                        if self.org == "WXR":
                            if self.WFOText == "Unknown WFO;":
                                self.orgText = "The National Weather Service"
                            else:
                                self.orgText = f"The National Weather Service in {self.WFOText}"
                        self.EASText = f"{self.orgText} has issued {self.evntText} for {self.strFIPS} beginning at {self.startTimeText} and ending at {self.endTimeText}. Message from {self.callsign}."
        elif listMode == False and sameData == "NONE":
            raise MissingSAME()

    @classmethod
    def __isInt__(cls, number):
        try:
            int(number)
        except ValueError:
            return False
        else:
            return True

    @classmethod
    def getTZ(cls, tzOffset):
        tzone = int(tzOffset / 3600.0)
        locTime = localtime().tm_isdst
        TMZ = "UTC"
        if tzone == 3 and locTime > 0:
            TMZ = "ADT"
        elif tzone == 4:
            TMZ = "AST"
            if locTime > 0:
                TMZ = "EDT"
        elif tzone == 5:
            TMZ = "EST"
            if locTime > 0:
                TMZ = "CDT"
        elif tzone == 6:
            TMZ = "CST"
            if locTime > 0:
                TMZ = "MDT"
        elif tzone == 7:
            TMZ = "MST"
            if locTime > 0:
                TMZ = "PDT"
        elif tzone == 8:
            TMZ = "PST"
        return TMZ
