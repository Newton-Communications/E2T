# 🌩️ **EAS2Text**: Comprehensive EAS Header-to-Text Translation Library

![EAS2Text](https://github.com/Newton-Communications/E2T/blob/nwr-localities/doc/img/TRxT7n.jpg)

EAS2Text is a powerful Python library for translating **EAS (Emergency Alert System)** headers into human-readable text. Designed to handle weather alerts, FIPS codes, emulation modes, and much more – now with enhanced error handling and Canadian support. 🎉  

---

## 🛠️ **Features**

- ✅ **EAS to Text Translation**: Converts raw ZCZC SAME strings into clear, readable text.
- ✅ **EAS EOM Detection**: Detects and processes End-of-Message headers seamlessly.
- ✅ **Error Handling**: Handles unknown callsigns, originators, and FIPS codes.
- ✅ **Raw and Parsed Outputs**: Extract detailed data from alerts.
- ✅ **Weather Forecast Office (WFO) Detection**: Supports overlaps and marine localities.
- ✅ **Canadian Forecast Regions**: Full support for Canada-based alerts.
- ✅ **Emulation Modes**: Mimic various EAS hardware/software outputs.

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

## 📖 **Usage**

### **Basic Example**

```python
from EAS2Text import EAS2Text

data = EAS2Text("ZCZC-WXR-SPS-024043-024021-024013-024005-024001+0600-0231829-EAR/FOLF-")
print(data.EASText)
```
<details>
<summary>Output</summary>

```
The National Weather Service in Baltimore/Washington, D.C. (LWX); has issued a Special Weather Statement for Allegany County, MD; Baltimore County, MD; Carroll County, MD; Frederick County, MD; Harford County, MD; beginning at 02:29 PM and ending at 08:29 PM. Message from EAR/FOLF.
```
</details>

---

### 🔍 **Advanced Usage**

#### **Detailed Output**

```python
from EAS2Text import EAS2Text

oof = EAS2Text("ZCZC-WXR-SPS-024043-024021-024013-024005-024001+0600-0231829-EAR/FOLF-")

print(f"RAW Data: {oof.EASData}")
print(f"RAW ORG: {oof.org}")
print(f"RAW WFO: {oof.WFO}")
print(f"RAW EVNT: {oof.evnt}")
print(f"RAW FIPS: {oof.FIPS}")
print(f"Purge Time: {oof.purge}")
print(f"Start Time: {oof.startTime}")
print(f"End Time: {oof.endTime}")
print(f"Full Output: {oof.EASText}")
```
<details>
<summary>Output</summary>

```
RAW Data: ZCZC-WXR-SPS-024043-024021-024013-024005-024001+0600-0231829-EAR/FOLF-
RAW ORG: WXR
RAW WFO: Baltimore/Washington, D.C. (LWX)
RAW EVNT: SPS
RAW FIPS: ['024043', '024021', '024013', '024005', '024001']
Purge Time: ['06', '00']
Start Time: 2024-01-23 14:29:00
End Time: 2024-01-23 20:29:00
Full Output: The National Weather Service in Baltimore/Washington, D.C. (LWX); has issued a Special Weather Statement...
```
</details>

---

## 🌟 **Emulation Modes**

EAS2Text can mimic outputs of various hardware/software systems. Here’s a table showing supported emulation modes:

| **Mode** | **Mode Triggers**                                   | **Emulated Hardware/Software**                              |
|----------|----------------------------------------------------|------------------------------------------------------------|
| **1**    | TFT                                                | TFT EAS 911, TFT EAS 911D                                  |
| **2**    | SAGE, SAGE 1822, SAGE DIGITAL, SAGE EAS ENDEC      | SAGE 1822 EAS ENDEC Firmware v5.9+, SAGE 3644 DIGITAL      |
| **3**    | TRILITHIC, VIAVI, EASY                             | Trilithic EASyCAP, VIAVI EAS line, TRILITHIC EAS line      |
| **4**    | BURK                                               | BURK EAS product line                                      |
| **5**    | DAS, DASDEC, MONROE, ONENET                        | Digital Alert Systems DASDEC I/II and Monroe OneNet units  |
| **6**    | DASV3, MONROEV3                                    | DASDEC and Monroe OneNet units Software v3.0+              |
| **7**    | HollyAnne, MIP-921                                 | HollyAnne EAS product line                                 |
| **8**    | GormanRedlich, EAS1, EAS-1CG                       | Gorman-Redlich EAS product line                            |

---

### **Example: Emulation Mode**

```python
from EAS2Text import EAS2Text

oof = EAS2Text("ZCZC-WXR-SPS-024043+0600-0231829-EAR/FOLF-", mode="SAGE EAS")
print(oof.EASText)
```
<details>
<summary>Output</summary>

```
The National Weather Service has issued a Special Weather Statement for Allegany County, MD beginning at 02:29 PM and ending at 08:29 PM (EAR/FOLF)
```
</details>

---

## 🇨🇦 **Canadian Forecast Regions**

Enable Canadian mode to process Canadian alerts:

```python
from EAS2Text import EAS2Text

oof = EAS2Text("ZCZC-WXR-HWW-090000-098110+0100-2641926-EC/GC/CA-", canada=True)
print(oof.EASText)
```
<details>
<summary>Output</summary>

```
Environment Canada has issued a High Wind Warning for All of Yukon/Northwest Territories/Nunavut; and Arctic Bay, NU; beginning at 03:26 PM and ending at 04:26 PM. Message from EC/GC/CA.
```
</details>

---

## 🕒 **Timezone Support**

### UTC Offset Example

```python
from EAS2Text import EAS2Text

oof = EAS2Text("ZCZC-WXR-SPS-024043+0600-0231829-EAR/FOLF-", timeZone=-6)
print(oof.EASText)
```
<details>
<summary>Output</summary>

```
The National Weather Service has issued a Special Weather Statement... beginning at 12:29 PM and ending at 06:29 PM.
```
</details>

### TZ Database Example

```python
oof = EAS2Text("ZCZC-WXR-SPS-024043+0600-0231829-EAR/FOLF-", timeZoneTZ="Europe/Berlin")
print(oof.EASText)
```
<details>
<summary>Output</summary>

```
The National Weather Service has issued a Special Weather Statement... beginning at 08:29 PM January 23 and ending at 02:29 AM January 24.
```
</details>

---

## ⚠️ **Reporting Issues**

- **Incorrect WFO or FIPS**: Report issues via [Discord](https://discord.com/users/637078631943897103) or GitHub Issues.
- **Provide Full Details**: Include the **entire ZCZC SAME string** and any corrections.

---

## 📋 **Contributing**

We welcome contributions! Open a Pull Request or Issue to report bugs or suggest improvements.

---

## 📜 **License**

**MIT License**

---

## 👤 **Contact**

- **Developer**: Newton Communications  
- **Discord**: [Contact Here](https://discord.com/users/637078631943897103)  

---

### ❤️ **Thank You for Using EAS2Text!**  
Stay safe, and enjoy simplified alert decoding!

---

This updated version incorporates all your requests, maintains clarity, and makes the README easier to navigate with **spoilers** for outputs while preserving all original examples.