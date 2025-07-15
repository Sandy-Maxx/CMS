now add new module in the app. keep all its code inside a separate folder "features/template_engine". make sure entire code related to this feature remains inside this folder and the feature must be added to the gui as another tab with name Template engine fully synced withexisting app. code must follow separation of concerns, scalability, modularity, readability etc. created folders files etc when required inside this folder.
if anything goes wrong i may be able to delete this new folder without affecting my existing app's working.
this module may use existing database to fill certain values like name of contracrt, description of work, firm names, total cost etc.
This module is used to fill placeholders in pre-designed Word (.docx) templates using a dynamic form-based GUI. The main objectives are:

✅ Placeholder Replacement Logic:
Placeholders in the document are wrapped with double curly braces like {{PLACEHOLDER_NAME}}.

Only base placeholders (like {{COST}}, {{COSTAMC}}, etc.) are shown in the GUI for manual input.

Placeholders that start with COST (or any base like COSTAMC, COSTRP, etc.) follow a math rule:

{{COST_0.2}}: auto-computed as COST * 0.2 and formatted as Indian currency (e.g., ₹12,000.00/-)

{{COST_1.18_IN_WORDS}}: auto-computed as COST * 1.18 and converted to words

{{COST_1.5_00}}: auto-computed and rounded to nearest 100

{{COST_1.2_0_IN_WORDS}}: auto-computed and rounded to nearest 10 in Indian words

Input fields that contain “DATE” in their name use a date picker widget in the GUI.

Any placeholder not manually filled remains unchanged in the output doc (for future use).

All occurrences of placeholders are replaced across paragraphs, headers, footers, tables, and bullets.

After document generation, the filled values are saved (using database or Excel), so:

If the same document is reloaded, previous inputs are automatically loaded for editing.

You can modify values and export again.