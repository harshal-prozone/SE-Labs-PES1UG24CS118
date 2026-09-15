# Lab 3 Analysis and Requirements Traceability

## Lab 1 baseline

The Lab 1 repository defines a **Warehouse Inventory & Pallet Location Tracker** in the Smart Cities, Transport & Logistics domain. Its main users are the Warehouse Operator and Logistics Supervisor, with a Barcode/RFID Scanner as a device actor.

### Functional requirements carried forward

| Lab 1 requirement | Architectural response in Lab 3 |
|---|---|
| Validate every placement against rack capacity | `Rack Capacity Service` provides `ICapacityValidation`; the `Inventory & Pallet Manager` requires it before persistence. |
| Identify pallets from barcode/RFID scans | `Barcode/RFID Adapter` provides normalised tag data through `IScanData`. |
| Store complete warehouse/rack/shelf/slot coordinates | `Warehouse Database` exposes `IWarehouseRepository` to the manager. |
| Log pallet ID, source, destination, timestamp and operator | Movement logging is orchestrated by the manager and persisted in the database audit trail. |
| Search by SKU, barcode or RFID | `Warehouse Operator UI` calls `IWarehouseOperations`; indexed repository queries return the current location. |

### Non-functional requirements carried forward

- **Performance:** Return pallet coordinates over 100,000 bins in under 100 ms at simulated peak load.
- **Security:** Permit inventory and stock-movement actions only for authenticated users whose roles authorize them.

## Key challenges

1. **Safety and consistency:** Rack-capacity validation must always happen before a placement is committed.
2. **Performance:** High-frequency location lookups need predictable sub-100 ms response times.
3. **Security and auditability:** Inventory changes require role checks and attributable movement records.
4. **Hardware variability:** Barcode/RFID scanners should be replaceable without changing business logic.
5. **Maintainability:** UI, rules, and storage must evolve independently while preserving stable contracts.

## Architectural style comparison

| Style | Advantages for this system | Disadvantages for this system | Suitability |
|---|---|---|---|
| Layered | Clear separation; centralized rules; simple local deployment; easy testing and replacement behind interfaces. | Layer traversal adds small overhead; poor discipline can create tight coupling. | **High — selected** |
| Microservices | Independent deployment/scaling; fault isolation; technology flexibility. | Network latency, distributed transactions, observability and operational overhead are disproportionate for this bounded system. | Low |
| Client–Server | Central data control; thin clients; consistent updates. | Server/network becomes a bottleneck and potential single point of failure on the warehouse floor. | Medium |

## Selected architecture

**Layered Architecture** with Presentation, Business, and Infrastructure/Data layers.

### Components — exactly five

1. Warehouse Operator UI
2. Inventory & Pallet Manager
3. Rack Capacity Service
4. Barcode/RFID Adapter
5. Warehouse Database

### Interfaces — exactly four

1. `IWarehouseOperations` — place, search and move requests/results.
2. `IScanData` — barcode/RFID tag identifiers via device API.
3. `ICapacityValidation` — rack-weight validation via internal API.
4. `IWarehouseRepository` — pallet, rack, 3D location and audit data via SQL.

## Submission checklist

- [x] Five components
- [x] Four interfaces
- [x] Provided and required interface notation
- [x] Data-flow arrows and protocol/data labels
- [x] Architecture comparison and selection
- [x] Two scenario-specific reasons
- [x] Security advantage
- [x] Performance benefit
- [x] One-page justification in DOCX and PDF
- [x] Component diagram in PNG and PDF
