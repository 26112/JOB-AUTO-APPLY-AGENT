"""
Question Answerer Module - DAY 17

Automatically answers standard screening questions in job applications.

Handles:
- Work authorization (Yes)
- Sponsorship required (No)
- Start date (2 weeks)
- Salary expectations (Negotiable)

⚠️ SAFETY: Only answers common questions, skips unknown
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def answer_standard_questions(page) -> list:
    """
    Answer standard screening questions on job application forms.
    
    Handles radio buttons and dropdowns for common questions.
    
    Args:
        page: Playwright page object
    
    Returns:
        List of question types that were answered
    """
    answered = []

    print("🔍 Looking for screening questions...")

    # ========================================
    # Handle Radio Buttons (Yes/No questions)
    # ========================================
    radios = page.query_selector_all("input[type='radio']")
    
    for radio in radios:
        try:
            # Get label text
            label = ""
            try:
                label = radio.evaluate(
                    """el => {
                        // Try label with for attribute
                        const forLabel = document.querySelector(`label[for='${el.id}']`);
                        if (forLabel) return forLabel.innerText.toLowerCase();
                        
                        // Try parent label
                        const parentLabel = el.closest('label');
                        if (parentLabel) return parentLabel.innerText.toLowerCase();
                        
                        // Try parent container text
                        const parent = el.parentElement;
                        if (parent) return parent.innerText.toLowerCase();
                        
                        return '';
                    }"""
                ) or ""
            except:
                pass
            
            # Skip if no label found
            if not label:
                continue

            # Work Authorization - Answer YES
            if any(x in label for x in ["authorized to work", "legally authorized", "work authorization", "eligible to work"]):
                if "yes" in label:
                    radio.check()
                    answered.append("work_authorization_yes")
                    print(f"   ✅ Work authorization: Yes")

            # Sponsorship - Answer NO
            elif any(x in label for x in ["sponsorship", "require visa", "visa sponsorship"]):
                if "no" in label:
                    radio.check()
                    answered.append("sponsorship_no")
                    print(f"   ✅ Sponsorship required: No")

            # Willing to relocate - Answer YES
            elif "relocate" in label or "willing to move" in label:
                if "yes" in label:
                    radio.check()
                    answered.append("relocate_yes")
                    print(f"   ✅ Willing to relocate: Yes")

            # Remote work - Answer YES
            elif "remote" in label or "work from home" in label:
                if "yes" in label:
                    radio.check()
                    answered.append("remote_yes")
                    print(f"   ✅ Remote work: Yes")

        except Exception as e:
            continue

    # ========================================
    # Handle Dropdowns (Select elements)
    # ========================================
    selects = page.query_selector_all("select")
    
    for select in selects:
        try:
            # Get select label/name
            name = (select.get_attribute("name") or "").lower()
            select_id = (select.get_attribute("id") or "").lower()
            
            # Get label text
            label = ""
            try:
                label = select.evaluate(
                    """el => {
                        const l = document.querySelector(`label[for='${el.id}']`);
                        return l ? l.innerText.toLowerCase() : '';
                    }"""
                ) or ""
            except:
                pass
            
            searchable = f"{name} {select_id} {label}"
            
            options = select.query_selector_all("option")
            
            for opt in options:
                try:
                    text = (opt.inner_text() or "").lower()
                    value = (opt.get_attribute("value") or "").lower()
                    
                    # Start Date questions
                    if any(x in searchable for x in ["start", "available", "when can"]):
                        if any(x in text for x in ["two weeks", "2 weeks", "immediately", "asap"]):
                            select.select_option(value=opt.get_attribute("value"))
                            answered.append("start_date")
                            print(f"   ✅ Start date: {text[:30]}")
                            break
                    
                    # Salary questions
                    elif any(x in searchable for x in ["salary", "compensation", "pay"]):
                        if any(x in text for x in ["negotiable", "open", "flexible"]):
                            select.select_option(value=opt.get_attribute("value"))
                            answered.append("salary")
                            print(f"   ✅ Salary: Negotiable")
                            break
                    
                    # Experience level
                    elif any(x in searchable for x in ["experience", "years"]):
                        if any(x in text for x in ["3", "2-4", "3-5", "mid"]):
                            select.select_option(value=opt.get_attribute("value"))
                            answered.append("experience")
                            print(f"   ✅ Experience: {text[:30]}")
                            break
                            
                except:
                    continue
                    
        except Exception as e:
            continue

    # ========================================
    # Handle Text Input Questions
    # ========================================
    text_inputs = page.query_selector_all("input[type='text'], input[type='number']")
    
    for text_input in text_inputs:
        try:
            if not text_input.is_visible():
                continue
                
            name = (text_input.get_attribute("name") or "").lower()
            placeholder = (text_input.get_attribute("placeholder") or "").lower()
            
            # Get label
            label = ""
            try:
                label = text_input.evaluate(
                    """el => {
                        const l = document.querySelector(`label[for='${el.id}']`);
                        return l ? l.innerText.toLowerCase() : '';
                    }"""
                ) or ""
            except:
                pass
            
            searchable = f"{name} {placeholder} {label}"
            
            # Years of experience
            if "years" in searchable and "experience" in searchable:
                text_input.fill("3")
                answered.append("years_experience")
                print(f"   ✅ Years of experience: 3")
            
            # Salary expectation (numeric)
            elif "salary" in searchable or "expected" in searchable:
                if "number" in text_input.get_attribute("type"):
                    text_input.fill("0")  # 0 often means negotiable
                    answered.append("salary_number")
                    print(f"   ✅ Salary expectation: Negotiable (0)")
                    
        except:
            continue

    if not answered:
        print("   ℹ️ No standard questions found on this page")
    
    return answered


def get_questions_summary(answered: list) -> str:
    """
    Get a summary of answered questions.
    """
    if not answered:
        return "No screening questions answered"
    
    return f"Answered {len(answered)} question(s): {', '.join(answered)}"
