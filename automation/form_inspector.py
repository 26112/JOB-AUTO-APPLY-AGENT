"""
Form Inspector Module - DAY 14

Detects and maps all form fields on an application page.
This is the foundation for reliable auto-fill.

Field types detected:
- text input
- email input
- textarea
- dropdown (select)
- checkbox
- radio button
- file upload
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def inspect_form_fields(page) -> list:
    """
    Inspect all form fields on the current page.
    
    Args:
        page: Playwright page object
    
    Returns:
        List of field dictionaries with tag, type, name, placeholder, label
    """
    fields = []

    # Query all form input elements
    inputs = page.query_selector_all("input, textarea, select, button[type='submit']")

    for el in inputs:
        try:
            # Get basic attributes
            tag = el.evaluate("el => el.tagName")
            input_type = el.get_attribute("type") or tag.lower()
            name = el.get_attribute("name")
            element_id = el.get_attribute("id")
            placeholder = el.get_attribute("placeholder")
            required = el.get_attribute("required") is not None
            
            # Try to get associated label
            label = ""
            try:
                # Method 1: label with for attribute
                if element_id:
                    label = el.evaluate(
                        """el => {
                            const l = document.querySelector(`label[for='${el.id}']`);
                            return l ? l.innerText : '';
                        }"""
                    )
                
                # Method 2: parent label
                if not label:
                    label = el.evaluate(
                        """el => {
                            const parent = el.closest('label');
                            if (parent) {
                                const text = parent.innerText.replace(el.value || '', '').trim();
                                return text;
                            }
                            return '';
                        }"""
                    )
                
                # Method 3: aria-label
                if not label:
                    label = el.get_attribute("aria-label") or ""
                
                # Method 4: nearby text/label element
                if not label:
                    label = el.evaluate(
                        """el => {
                            const prev = el.previousElementSibling;
                            if (prev && (prev.tagName === 'LABEL' || prev.tagName === 'SPAN')) {
                                return prev.innerText;
                            }
                            return '';
                        }"""
                    )
                    
            except:
                pass

            # Get current value (for debugging)
            value = ""
            try:
                value = el.get_attribute("value") or ""
            except:
                pass

            # Get options for select elements
            options = []
            if tag.lower() == "select":
                try:
                    options = el.evaluate(
                        """el => {
                            return Array.from(el.options).map(o => ({
                                value: o.value,
                                text: o.text
                            }));
                        }"""
                    )
                except:
                    pass

            field_info = {
                "tag": tag.lower(),
                "type": input_type,
                "name": name,
                "id": element_id,
                "placeholder": placeholder,
                "label": label.strip() if label else "",
                "required": required,
                "value": value,
            }
            
            # Add options for select elements
            if options:
                field_info["options"] = options
            
            fields.append(field_info)

        except Exception as e:
            continue

    return fields


def categorize_fields(fields: list) -> dict:
    """
    Categorize fields by their likely purpose.
    
    Args:
        fields: List of field dictionaries
    
    Returns:
        Dictionary with categories as keys
    """
    categories = {
        "text_inputs": [],
        "email": [],
        "phone": [],
        "file_upload": [],
        "textarea": [],
        "dropdown": [],
        "checkbox": [],
        "radio": [],
        "submit": [],
        "other": []
    }
    
    for field in fields:
        field_type = field.get("type", "").lower()
        field_name = (field.get("name") or "").lower()
        field_label = (field.get("label") or "").lower()
        field_placeholder = (field.get("placeholder") or "").lower()
        
        # Combine searchable text
        searchable = f"{field_name} {field_label} {field_placeholder}"
        
        if field_type == "email" or "email" in searchable:
            categories["email"].append(field)
        elif field_type == "tel" or "phone" in searchable or "mobile" in searchable:
            categories["phone"].append(field)
        elif field_type == "file":
            categories["file_upload"].append(field)
        elif field.get("tag") == "textarea":
            categories["textarea"].append(field)
        elif field.get("tag") == "select":
            categories["dropdown"].append(field)
        elif field_type == "checkbox":
            categories["checkbox"].append(field)
        elif field_type == "radio":
            categories["radio"].append(field)
        elif field_type == "submit":
            categories["submit"].append(field)
        elif field_type in ["text", "password"]:
            categories["text_inputs"].append(field)
        else:
            categories["other"].append(field)
    
    return categories


def print_form_map(fields: list):
    """
    Print a human-readable form field map.
    
    Args:
        fields: List of field dictionaries
    """
    print("\n" + "=" * 60)
    print("📋 FORM FIELD MAP")
    print("=" * 60)
    
    categories = categorize_fields(fields)
    
    for category, category_fields in categories.items():
        if category_fields:
            print(f"\n🏷️  {category.upper().replace('_', ' ')} ({len(category_fields)})")
            print("-" * 40)
            for f in category_fields:
                label = f.get("label") or f.get("placeholder") or f.get("name") or "unnamed"
                required = "⚠️ required" if f.get("required") else ""
                print(f"   • {label[:30]:30} [{f.get('type', 'unknown')}] {required}")
    
    print("\n" + "=" * 60)
    print(f"📊 Total fields detected: {len(fields)}")
    print("=" * 60)
