# Lab 1 - Requirements Engineering & UML Use-Case Modelling

**Student / SRN:** PES1UG24CS118  
**Project Title:** Warehouse Inventory & Pallet Location Tracker  
**Primary Domain:** Smart Cities, Transport & Logistics  
**Target Actors:** Warehouse Operator, Logistics Supervisor (+ Barcode/RFID Scanner as a device actor)

## Deliverables in this folder

| File | Deliverable |
|------|-------------|
| `Requirements_Table.xlsx` | Requirements table - 5 Functional + 2 Nonfunctional requirements |
| `UML_UseCase_Diagram.pdf` | UML use-case diagram (3 actors, 7 use cases, include/extend) |
| `UseCase_Flow.pdf` | Use-case flow for UC-02 Place Pallet (main + alternate flow) |
| `Warehouse_Lab1_Submission.pdf` | Full consolidated submission (all sections) |

## Correction applied

NFR-001 acceptance criteria previously referenced "security standards," which
did not match its latency-only description. It has been corrected to test only
the measurable 100 ms / 100,000-bin latency target under simulated peak load.
Security/access control remains covered by NFR-002.
