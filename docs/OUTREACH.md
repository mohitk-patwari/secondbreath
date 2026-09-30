# Outreach to dataset authors

Three drafts, one per dataset team. Each body is under 200 words. Numbers are
taken from `README.md`, `docs/WRITEUP.md` and `analysis/METHOD.md`. If the
audit is re-run before sending, re-check every figure against `audit.json`.

**Any reply, even a short one, goes into the write-up's Impact section
(`docs/WRITEUP.md`) before the deadline, 2 Oct 2026, 23:59 PT.** Quote it with
permission, or paraphrase it, and give the date.

## Contact details

None of the three Zenodo records publishes an email address (checked through
the Zenodo API on 30 Sep 2026: creators, contributors, description and notes).

| Dataset | What the record gives | Where to look |
| --- | --- | --- |
| 18385830, lecture halls, Cyprus | Christina Kakoulli is named **ContactPerson**. ORCIDs: Kakoulli 0000-0001-8436-0131, Michaelides 0000-0002-0549-704X, Kyriacou 0000-0003-4815-2989. No affiliations listed. | The three ORCID profiles, for affiliation and email. Then the institution's staff directory. Write to Kakoulli first, since she is the named contact. |
| 5062837, Spain | Sergio Trilles, Universitat Jaume I, ORCID 0000-0002-9304-0719. | The ORCID profile and the Universitat Jaume I staff directory. |
| 18195710, ENSENSIA | Names only: John Apostolopoulos, George Fouskas, Spyros Pandis. No ORCIDs, no affiliations. The README has no contact section. Funded by the EU Horizon project SynAir-G, grant 101057271. | The CORDIS project page (https://cordis.europa.eu/projects/101057271) and the SynAir-G project site, for the partner that runs ENSENSIA and a contact address. |

---

## 1. Cyprus lecture halls (Zenodo 18385830)

**To:** Christina Kakoulli, cc Michalis Michaelides and Alexis Kyriacou
**Subject:** Your lecture-hall IEQ dataset (Zenodo 18385830): which clock does `recorded` use?

Dear Christina Kakoulli, Michalis Michaelides and Alexis Kyriacou,

Thank you for publishing the lecture-hall measurements under CC BY 4.0. Your characteristics file made a design comparison possible.

I estimated each hall's air-change rate two ways: from the CO2 decay after the room empties, and from the rise during occupancy. Against a design of about 6 ACH, Hall A measures 0.74 by decay (252 fits) and 1.02 by buildup (27 fits). Hall C measures 0.88 (259) and 1.09 (8). Hall B's decay fits scatter too widely (interquartile range 0.47 to 1.70) to quote. Its peak was 4,957 ppm.

My main question: which clock does the `recorded` column use? The timestamps run straight through both 2023–24 clock changes, so it looks like UTC or a fixed offset. If it is UTC, both of Hall C's fits become uncertain. Hall A holds either way, and every hall stays at or below 1.17 ACH.

Also, are the halls' air-handler schedules available? They would show whether the decay fit measures leakage rather than supplied air.

The analysis and code are open; I'm happy to send per-hall results: https://github.com/mohitk-patwari/secondbreath

This began as an entry to the AWS Builder Center hackathon.

Kind regards,
Mohit Kumar Patwari

---

## 2. Castellón primary classrooms (Zenodo 5062837)

**To:** Sergio Trilles
**Subject:** Your classroom CO2 dataset (Zenodo 5062837): do room volumes exist?

Dear Sergio Trilles,

Thank you for publishing the Castellón classroom CO2 data under CC BY 4.0.

I estimated air-change rates from the data two ways: from the CO2 decay after each class empties, and from the rise while the room is occupied. Of the 12 sensors, 8 give a confident decay rate, from 0.68 to 3.65 air changes per hour (median 2.32). None gives a confident buildup rate. The classrooms were measured in spring 2021 with Covid-19 ventilation measures in force, so I report these rates as measured, not as normal practice.

What I could not do is compare them with anything. Do the classroom volumes, or floor areas and ceiling heights, exist anywhere? A design or recommended airflow per room would help too. Without volume, no rate can be checked against design or guidance, so I claim no shortfall for any of these rooms.

The analysis and code are open, and I'm happy to send the per-classroom results: https://github.com/mohitk-patwari/secondbreath

This began as an entry to the AWS Builder Center hackathon.

Kind regards,
Mohit Kumar Patwari

---

## 3. ENSENSIA schools (Zenodo 18195710)

**To:** John Apostolopoulos, George Fouskas, Spyros Pandis
**Subject:** ENSENSIA indoor air dataset (Zenodo 18195710): do room volumes exist?

Dear John Apostolopoulos, George Fouskas and Spyros Pandis,

Thank you for publishing the ENSENSIA raw data under CC BY 4.0, and for a README that states the time zone.

I estimated air-change rates from the CO2 records two ways: from the decay after each room empties, and from the rise while it is occupied. Of the 25 school files, 14 give a confident decay rate, from 0.24 to 1.75 air changes per hour (median 1.40). 7 give a confident buildup rate, from 0.40 to 1.05 (median 0.72).

One thing you may want to know: School 18 reports exactly 658 ppm for 46,826 consecutive readings while its temperature and humidity keep changing. It looks like a fill value. My filter for such runs fired in 8 of the 25 files.

My question: do the monitored rooms' volumes, or floor areas and ceiling heights, exist anywhere? Without them no rate can be compared with design or guidance, so I claim no shortfall for any school.

The analysis and code are open, and I'm happy to send the per-school results: https://github.com/mohitk-patwari/secondbreath

This began as an entry to the AWS Builder Center hackathon.

Kind regards,
Mohit Kumar Patwari
