# ConformiCidade

**ConformiCidade** is a web-based tool designed to validate and standardize municipal tax data models against a minimum reference model, promoting interoperability between local tax cadastres and broader territorial management systems such as the **Multipurpose Land Registry (CTM)**.

The project was developed as part of an academic research project and is registered as a software product. It targets a real and recurring problem in public administration: the lack of standardized data models across municipalities, which makes data integration, interoperability, and national-scale territorial management difficult.

---

## Problem Context

Municipal land and tax management systems often operate with heterogeneous and incompatible data schemas. While the territorial cadastre provides an official inventory of land parcels, thematic cadastres—such as tax cadastres—are usually managed independently and follow different data structures.

This fragmentation creates barriers to:

- Interoperability between municipal and national systems  
- Integration with multipurpose cadastre initiatives (CTM)  
- Data reuse by geotechnology companies and public agencies  
- Automation of data exchange and validation processes  

---

## Solution Overview

ConformiCidade addresses this problem by validating municipal tax data models against a **minimum reference tax model**, facilitating schema alignment and compliance assessment.

The tool allows users to:

1. Upload municipal tax datasets in CSV format  
2. Automatically compare their data structure with a reference model  
3. Receive suggested field mappings based on textual similarity  
4. Review and adjust mappings through an interactive graphical interface  
5. Generate a **Compliance Report** showing alignment percentages per entity and attribute  

This significantly reduces manual effort and improves data quality and consistency.

---

## Reference Model

The minimum reference tax data model was designed based on:

- Common attributes identified across four Brazilian municipalities  
- The cadastral model proposed by **Silva (2022)**  
- Concepts and structures from **ISO 19152:2012 – Land Administration Domain Model (LADM)**  

This ensures conceptual consistency with international land administration standards while remaining practical for municipal use.

---

## Technical Approach

- **Methodology:** Design Science Research Methodology (DSRM)  
- **Backend:** Django  
- **Frontend:** React  
- **Core Feature:** Schema matching using character similarity algorithms  

### Key Capabilities

- Data persistence and user authentication  
- Automated attribute matching between heterogeneous schemas  
- Interactive review of suggested mappings  
- Generation of structured compliance reports  

Several string similarity algorithms were evaluated to support schema matching, helping identify equivalent or semantically similar attributes across different datasets.

---

## Evaluation

The tool’s usability and acceptance were evaluated using:

- Usability testing  
- Technology Acceptance Model (TAM)  

Results indicate that ConformiCidade is well accepted by potential users such as municipal managers and geotechnology professionals, while also highlighting areas for future improvement.

---

## Potential Applications

- Municipal tax and land administration  
- Integration with Multipurpose Cadastre systems (CTM)  
- Support for national territorial data initiatives (e.g., SDI / INDE)  
- Use by geotechnology companies providing services to municipalities  

---

## Future Work

Planned and suggested evolutions include:

- Automatic generation of SQL scripts for data transformation between models  
- Support for spatializing input data  
- Expansion to support geospatial datasets and spatial validation workflows  
- Integration with national spatial data infrastructures
