"""
Form Auto-Fill Module - DAY 15

Automatically fills form fields with resume data.
Uses smart matching based on labels, placeholders, and input types.

⚠️ SAFETY: Only fills high-confidence matches
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def autofill_personal_info(page, resume: dict) -> list:
    """
    Auto-fill personal information fields from resume.
    
    Args:
        page: Playwright page object
        resume: Resume profile dictionary with name, email, phone
    
    Returns:
        List of field names that were filled
    """
    filled = []

    inputs = page.query_selector_all("input, textarea")

    for el in inputs:
        try:
            # Skip hidden and disabled fields
            if not el.is_visible():
                continue
            
            input_type = (el.get_attribute("type") or "").lower()
            name = (el.get_attribute("name") or "").lower()
            placeholder = (el.get_attribute("placeholder") or "").lower()
            element_id = (el.get_attribute("id") or "").lower()
            
            # Try to get label text
            label = ""
            try:
                label = el.evaluate(
                    """el => {
                        const l = document.querySelector(`label[for='${el.id}']`);
                        return l ? l.innerText.toLowerCase() : '';
                    }"""
                ) or ""
            except:
                pass
            
            # Combine all text for matching
            searchable = f"{name} {placeholder} {label} {element_id}"

            # EMAIL - highest confidence match
            if input_type == "email" or "email" in searchable:
                if resume.get("email"):
                    el.fill(resume["email"])
                    filled.append("email")
                    print(f"   ✅ Filled EMAIL: {resume['email']}")
                continue

            # PHONE - match phone/mobile/tel
            if input_type == "tel" or any(x in searchable for x in ["phone", "mobile", "tel"]):
                if resume.get("phone"):
                    el.fill(resume["phone"])
                    filled.append("phone")
                    print(f"   ✅ Filled PHONE: {resume['phone']}")
                continue

            # FULL NAME - match full name specifically
            if "full" in searchable and "name" in searchable:
                if resume.get("name"):
                    el.fill(resume["name"])
                    filled.append("full_name")
                    print(f"   ✅ Filled FULL NAME: {resume['name']}")
                continue

            # FIRST NAME
            if ("first" in searchable and "name" in searchable) or "firstname" in searchable:
                if resume.get("name"):
                    first_name = resume["name"].split()[0]
                    el.fill(first_name)
                    filled.append("first_name")
                    print(f"   ✅ Filled FIRST NAME: {first_name}")
                continue

            # LAST NAME
            if ("last" in searchable and "name" in searchable) or "lastname" in searchable:
                if resume.get("name"):
                    parts = resume["name"].split()
                    last_name = parts[-1] if len(parts) > 1 else ""
                    if last_name:
                        el.fill(last_name)
                        filled.append("last_name")
                        print(f"   ✅ Filled LAST NAME: {last_name}")
                continue

            # LOCATION / CITY
            if any(x in searchable for x in ["location", "city", "address"]):
                if resume.get("location"):
                    el.fill(resume["location"])
                    filled.append("location")
                    print(f"   ✅ Filled LOCATION: {resume['location']}")
                continue

        except Exception as e:
            continue

    return filled


def autofill_with_mapping(page, resume: dict, field_mapping: dict) -> list:
    """
    Auto-fill form using explicit field mapping.
    
    Args:
        page: Playwright page object
        resume: Resume profile dictionary
        field_mapping: Dict mapping field selectors to resume keys
    
    Returns:
        List of field names that were filled
    """
    filled = []
    
    for selector, resume_key in field_mapping.items():
        try:
            el = page.query_selector(selector)
            if el and el.is_visible():
                value = resume.get(resume_key, "")
                if value:
                    el.fill(value)
                    filled.append(resume_key)
                    print(f"   ✅ Filled {resume_key}: {value}")
        except Exception as e:
            print(f"   ⚠️ Failed to fill {selector}: {e}")
    
    return filled


def get_fill_summary(filled: list) -> str:
    """
    Get a summary of filled fields.
    """
    if not filled:
        return "No fields were auto-filled"
    
    return f"Auto-filled {len(filled)} field(s): {', '.join(filled)}"
