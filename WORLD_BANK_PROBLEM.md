\# SANG Agriculture — Narrow Problem



\## Problem



Smallholder farmers may know that they need help, but struggle to identify

the right local person, organization, resource, or government support for

their specific agricultural problem.



Existing information can be fragmented across different sources.



\## Target User



Smallholder farmers in developing economies, starting with a

Gujarat-focused prototype.



\## Narrow Use Case



A farmer describes an agricultural problem in simple language.



SANG identifies:



\- What kind of problem it is

\- What location/context is relevant

\- Which people or organizations may help

\- Which resources or schemes may be relevant

\- Why each result was matched

\- What information is missing



\## Example



Input:



"My crop is affected by a pest and I am a small farmer in Rajkot."



Output:



\### Relevant Help

\- Agricultural expert / extension worker

\- Relevant pest-management resource

\- Relevant agricultural support opportunity



\### Why

\- Agriculture problem match

\- Pest-related expertise match

\- Rajkot/location match



\### Missing Information

\- Crop type

\- Pest symptoms

\- Farm size

\- Available resources



\## Success Criterion



Given a farmer's problem and basic context, SANG should produce

a small set of relevant, explainable connections instead of a generic

information dump.



\## Constraint



The prototype should remain lightweight and should not depend on

large-scale cloud AI or expensive infrastructure.

