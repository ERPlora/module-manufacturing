# Manufacturing & BOM Module

Bill of materials, production orders and recipes.

## Features

- Define bills of materials (BOM) with component lines, quantities, and units
- Create production orders linked to BOMs with quantity and scheduling
- Production order workflow: draft, confirmed, in progress, done, cancelled
- Batch/lot number tracking for traceability
- Production batches with quality control statuses (pending QC, approved, rejected, quarantine)
- Ingredient traceability per batch with supplier lot number tracking
- Expiry date management for production orders and batches
- BOM code and activation control for product lifecycle management

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Manufacturing & BOM > Settings**

## Usage

Access via: **Menu > Manufacturing & BOM**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/manufacturing/dashboard/` | Production overview and key metrics |
| BOM | `/m/manufacturing/bom/` | Create and manage bills of materials |
| Production | `/m/manufacturing/production/` | Manage production orders and batches |
| Settings | `/m/manufacturing/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `BillOfMaterials` | BOM definition with name, code, output quantity, notes, and active status |
| `BOMLine` | Component line within a BOM specifying description, quantity, and unit |
| `ProductionOrder` | Production order with order number, linked BOM, quantity, batch/lot number, expiry date, status, and date range |
| `ProductionBatch` | Production batch/lot for traceability with batch number, quantity produced, production/expiry dates, and quality status |
| `BatchIngredient` | Ingredient record within a batch tracking description, supplier lot number, quantity used, and unit |

## Permissions

| Permission | Description |
|------------|-------------|
| `manufacturing.view_billofmaterials` | View bills of materials |
| `manufacturing.add_billofmaterials` | Create new bills of materials |
| `manufacturing.change_billofmaterials` | Edit existing bills of materials |
| `manufacturing.delete_billofmaterials` | Delete bills of materials |
| `manufacturing.view_productionorder` | View production orders |
| `manufacturing.add_productionorder` | Create new production orders |
| `manufacturing.change_productionorder` | Edit existing production orders |
| `manufacturing.manage_settings` | Manage module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
