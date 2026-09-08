\# SANG Agriculture — Data Model



\## Farmer



\- id

\- name

\- location

\- crops

\- farm\_size

\- skills

\- needs

\- available\_resources



\## Agricultural Problem



\- id

\- title

\- category

\- description

\- location

\- required\_skills

\- severity



\## Helper / Organization



\- id

\- name

\- type

\- location

\- skills

\- areas\_of\_support



\## Resource



\- id

\- title

\- type

\- category

\- description

\- location

\- eligibility



\## Opportunity



\- id

\- title

\- category

\- description

\- location

\- eligibility



\## Match



A match should contain:



\- target\_id

\- target\_type

\- score

\- reasons

\- missing\_information



\## Core Relationship



Farmer

&#x20; ↓

Problem

&#x20; ↓

Helper / Organization

&#x20; ↓

Resource

&#x20; ↓

Opportunity



\## Matching Signals



SANG should consider:



1\. Problem/category relevance

2\. Skills/expertise

3\. Location

4\. Eligibility

5\. Context

6\. Available resources



\## Explainability



Every recommendation should answer:



"Why did SANG recommend this?"



The system must also identify important missing information rather

than pretending certainty.

