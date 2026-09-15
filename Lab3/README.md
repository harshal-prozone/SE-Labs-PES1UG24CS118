# Lab 3 — Component Modelling & Architectural Pattern Selection

**Student:** C. Harshal Rajesh  
**SRN:** PES1UG24CS118  
**Project:** Warehouse Inventory & Pallet Location Tracker  
**Selected architecture:** Layered Architecture

## Submit these four files

| File | Deliverable |
|---|---|
| `Warehouse_Component_Diagram.png` | UML component diagram in PNG format |
| `Warehouse_Component_Diagram.pdf` | UML component diagram in PDF format |
| `Architecture_Justification.docx` | Editable one-page justification |
| `Architecture_Justification.pdf` | One-page justification for submission |

## Supporting files

The `Supporting` folder contains:

- `Warehouse_Component_Diagram.svg` — editable vector source.
- `Analysis_and_Traceability.md` — Lab 1 requirements mapping and architectural comparison.
- `VERIFICATION_REPORT.md` — final structural and content checks.
- `SHA256SUMS.txt` — checksums for integrity verification.

## Architecture summary

- **Presentation layer:** Warehouse Operator UI
- **Business layer:** Inventory & Pallet Manager; Rack Capacity Service
- **Infrastructure and data layer:** Barcode/RFID Adapter; Warehouse Database

The diagram contains exactly five components and four interfaces: `IWarehouseOperations`, `IScanData`, `ICapacityValidation`, and `IWarehouseRepository`.
