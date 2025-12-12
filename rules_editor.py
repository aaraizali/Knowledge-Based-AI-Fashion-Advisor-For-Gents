# rule_editor.py
import streamlit as st
from advisor import load_rules, save_rules
from typing import List, Dict, Any

def _next_id(rules: List[Dict[str, Any]]) -> int:
    if not rules:
        return 1
    return max(r.get("id", 0) for r in rules) + 1

def rule_editor_page():
    st.title("✏️ Rule Editor")
    rules = load_rules()

    st.subheader("Existing Rules")
    if not rules:
        st.info("No rules found. Add a new rule below.")
    for i, rule in enumerate(rules):
        with st.expander(f"Rule {rule.get('id')} — {rule.get('top')} / {rule.get('bottom')}"):
            st.write(rule)
            col1, col2, col3 = st.columns([1,1,1])
            with col1:
                if st.button(f"Delete {rule.get('id')}", key=f"del_{rule.get('id')}"):
                    rules.pop(i)
                    save_rules(rules)
                    st.success(f"Rule {rule.get('id')} deleted. Reload page to see changes.")
            with col2:
                if st.button(f"Duplicate {rule.get('id')}", key=f"dup_{rule.get('id')}"):
                    new_rule = dict(rule)
                    new_rule["id"] = _next_id(rules)
                    rules.append(new_rule)
                    save_rules(rules)
                    st.success(f"Rule {rule.get('id')} duplicated as {new_rule['id']}.")
            with col3:
                if st.button(f"Edit {rule.get('id')}", key=f"edit_{rule.get('id')}"):
                    # open a simple edit form
                    st.session_state["editing_rule"] = rule.get("id")
                    st.experimental_rerun()

    # If editing rule is requested, show edit form
    editing = st.session_state.get("editing_rule", None)
    if editing:
        st.markdown(f"### Editing rule {editing}")
        rule_to_edit = next((r for r in rules if r.get("id") == editing), None)
        if rule_to_edit:
            with st.form(key=f"edit_form_{editing}"):
                weather = st.selectbox("Weather", ["hot","mild","cold"], index=["hot","mild","cold"].index(rule_to_edit.get("weather","hot")))
                occasion = st.selectbox("Occasion", ["casual","formal","party"], index=["casual","formal","party"].index(rule_to_edit.get("occasion","casual")))
                body_type = st.selectbox("Body Type", ["slim","athletic","heavy"], index=["slim","athletic","heavy"].index(rule_to_edit.get("body_type","slim")))
                style = st.selectbox("Style", ["Classic","Sporty","Trendy"], index=["Classic","Sporty","Trendy"].index(rule_to_edit.get("style","Classic")))
                colors = st.multiselect("Colors", ["White","Black","Brown","Navy","Light Blue","Khaki","Grey","Olive"], default=rule_to_edit.get("colors",[]))
                top = st.text_input("Top", value=rule_to_edit.get("top",""))
                bottom = st.text_input("Bottom", value=rule_to_edit.get("bottom",""))
                shoes = st.text_input("Shoes", value=rule_to_edit.get("shoes",""))
                accessories = st.text_input("Accessories", value=rule_to_edit.get("accessories",""))
                if st.form_submit_button("Save"):
                    rule_to_edit.update({
                        "weather": weather,
                        "occasion": occasion,
                        "body_type": body_type,
                        "style": style,
                        "colors": colors,
                        "top": top,
                        "bottom": bottom,
                        "shoes": shoes,
                        "accessories": accessories
                    })
                    save_rules(rules)
                    st.success(f"Rule {editing} updated.")
                    del st.session_state["editing_rule"]
                    st.experimental_rerun()

    st.markdown("---")
    st.subheader("Add New Rule")
    with st.form(key="add_rule_form"):
        weather = st.selectbox("Weather", ["hot","mild","cold"])
        occasion = st.selectbox("Occasion", ["casual","formal","party"])
        body_type = st.selectbox("Body Type", ["slim","athletic","heavy"])
        style = st.selectbox("Style", ["Classic","Sporty","Trendy"])
        colors = st.multiselect("Colors", ["White","Black","Brown","Navy","Light Blue","Khaki","Grey","Olive"])
        top = st.text_input("Top (e.g. White Cotton Shirt)")
        bottom = st.text_input("Bottom (e.g. Khaki Chinos)")
        shoes = st.text_input("Shoes (e.g. White Sneakers)")
        accessories = st.text_input("Accessories (optional)")
        if st.form_submit_button("Add Rule"):
            new_rule = {
                "id": _next_id(rules),
                "weather": weather,
                "occasion": occasion,
                "body_type": body_type,
                "style": style,
                "colors": colors,
                "top": top,
                "bottom": bottom,
                "shoes": shoes,
                "accessories": accessories
            }
            rules.append(new_rule)
            save_rules(rules)
            st.success(f"Rule {new_rule['id']} added. Reload to see it in the list.")
