# Template Engine Placeholders Guide

This guide provides a comprehensive list of placeholders you can use in your Word document templates (.docx) with the Template Engine. Copy and paste these placeholders directly into your templates to ensure accuracy and avoid typos.

## General Placeholders

These placeholders can be used in most templates and will be automatically populated with general work-related information.

| Placeholder             | Description                                        | Example Value           |
| :---------------------- | :------------------------------------------------- | :---------------------- |
| `{{work_name}}`         | The name of the work.                              | Project Alpha Phase 1   |
| `{{work_id}}`           | The unique ID of the work.                         | W-2023-001              |
| `{{agreement_date}}`    | The date of the agreement for the work.            | 2023-01-15              |
| `{{client_name}}`       | The name of the client.                            | Acme Corporation        |
| `{{firm_name}}`         | The name of the firm associated with the work.     | Builders Inc.           |
| `{{work_order_number}}` | The work order number.                             | WO-2023-5678            |
| `{{work_order_date}}`   | The date of the work order.                        | 2023-02-01              |
| `{{start_date}}`        | The planned start date of the work.                | 2023-03-01              |
| `{{end_date}}`          | The planned end date of the work.                  | 2023-09-30              |
| `{{total_contract_value}}` | The total value of the contract.                | 1,500,000.00            |
| `{{currency_symbol}}`   | The currency symbol (e.g., ₹, $).                  | ₹                       |
| `{{current_date}}`      | The current date when the document is generated.   | 2025-07-21              |
| `{{current_time}}`      | The current time when the document is generated.   | 14:30:00                |

## Schedule Item Placeholders

These placeholders are used within sections that iterate over schedule items. They are typically used in conjunction with special `[autofill_data]` blocks (refer to the Template Engine documentation for details on how to structure these blocks).

| Placeholder             | Description                                        | Example Value           |
| :---------------------- | :------------------------------------------------- | :---------------------- |
| `{{item_number}}`       | The sequential number of the schedule item.        | 1                       |
| `{{item_description}}`  | The description of the schedule item.              | Earthwork Excavation    |
| `{{item_unit}}`         | The unit of measurement for the item.              | Cum                     |
| `{{item_quantity}}`     | The quantity of the schedule item.                 | 500.00                  |
| `{{item_rate}}`         | The rate per unit for the schedule item.           | 350.00                  |
| `{{item_amount}}`       | The total amount for the schedule item (Quantity * Rate). | 175,000.00              |

## Custom Placeholders

You can define custom placeholders within the Template Engine interface. These will be replaced with the values you provide during document generation.

| Placeholder             | Description                                        | Example Value           |
| :---------------------- | :------------------------------------------------- | :---------------------- |
| `{{your_custom_field}}` | A placeholder for any custom data you need to insert. | Your custom text here   |
| `{{project_manager}}`   | Name of the project manager.                       | Jane Doe                |
| `{{report_title}}`      | Title of a specific report.                        | Monthly Progress Report |

## Special Command Placeholders (`<< >>`)

These placeholders are used for special commands or system-level instructions within the template. Their exact behavior depends on the template engine's implementation.

| Placeholder             | Description                                        | Example Usage           |
| :---------------------- | :------------------------------------------------- | :---------------------- |
| `<<PAGE_BREAK>>`        | Inserts a page break at this position.             | `<<PAGE_BREAK>>`        |
| `<<NEW_SECTION>>`       | Starts a new section in the document.              | `<<NEW_SECTION>>`       |
| `<<TOC>>`               | Inserts a Table of Contents.                       | `<<TOC>>`               |

## Advanced Placeholders (Conditional Logic & Loops)

Advanced placeholders allow for dynamic content generation based on conditions or by iterating over data collections. The syntax for these can vary significantly between template engines. Below are common conceptual examples; refer to the specific template engine documentation for exact syntax.

### Conditional Logic

Used to include content only if a certain condition is met.

```
{{ IF total_contract_value > 1000000 }}
    This is a large project.
{{ ENDIF }}

{{ IF status == "Completed" }}
    Project Completion Date: {{ end_date }}
{{ ELSE }}
    Project is still in progress.
{{ ENDELSE }}
```

### Loops / Iteration

Used to repeat a block of content for each item in a collection (e.g., for each schedule item).

```
{{ FOR item IN schedule_items }}
    - Item: {{ item.item_description }} (Quantity: {{ item.item_quantity }})
{{ ENDFOR }}
```

## Date Formatting

For date placeholders, you can often specify a format. While the default format is `YYYY-MM-DD`, you might be able to use specific formatting codes depending on the underlying template engine's capabilities (e.g., `{{agreement_date:DD-MM-YYYY}}`). Consult the application's specific date formatting options if available.

## Important Notes:

*   **Case Sensitivity:** Placeholders are case-sensitive. Ensure you match the exact casing shown in this guide.
*   **Double Curly Braces (`{{ }}`):** All standard data placeholders are enclosed in double curly braces.
*   **Double Angle Brackets (`<< >>`):** Special command placeholders use double angle brackets.
*   **Autofill Data (`[autofill_data]`):** For dynamic lists like schedule items, you will need to use the `[autofill_data]` and `[/autofill_data]` tags in your Word template to define the repeating section. Refer to the Template Engine's detailed documentation or examples for proper usage.
*   **Preview and Verify:** Always preview your generated documents to ensure all placeholders are correctly replaced and the formatting is as expected.