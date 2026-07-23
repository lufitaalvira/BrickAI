"""
Button components
"""
import streamlit as st


def primary_button(label, key, on_click=None):
    """Primary button (CTA)"""
    return st.button(label, key=key, on_click=on_click, use_container_width=False)


def secondary_button(label, key, on_click=None):
    """Secondary button"""
    return st.button(label, key=key, on_click=on_click)


def danger_button(label, key, on_click=None):
    """Danger button"""
    return st.button(label, key=key, on_click=on_click)


def reset_button(label="Reset", key="btn_reset", on_click=None):
    """Reset button"""
    return st.button(label, key=key, on_click=on_click)


def back_to_home_button(key="back_to_home", label="← Kembali ke Beranda"):
    """
    Back to home button
    
    Args:
        key: Unique key for the button
        label: Button label
    
    Returns:
        bool: True if button is clicked
    """
    from utils.session import set_page
    
    if st.button(label, key=key):
        set_page('beranda')
        return True
    return False


def back_button(label="← Kembali", key="back_button", target_page=None):
    """
    Generic back button
    
    Args:
        label: Button label
        key: Unique key for the button
        target_page: Target page name ('beranda', 'deteksi', 'hasil')
    
    Returns:
        bool: True if button is clicked
    """
    from utils.session import set_page
    
    if st.button(label, key=key):
        if target_page:
            set_page(target_page)
        return True
    return False


def nav_button(label, target_page, key=None, use_container_width=False):
    """
    Navigation button to specific page
    
    Args:
        label: Button label
        target_page: Target page name ('beranda', 'deteksi', 'hasil')
        key: Unique key for the button
        use_container_width: Whether to use container width
    
    Returns:
        bool: True if button is clicked
    """
    from utils.session import set_page
    
    if key is None:
        key = f"nav_to_{target_page}"
    
    if st.button(label, key=key, use_container_width=use_container_width):
        set_page(target_page)
        return True
    return False


def action_button(label, action, key=None, use_container_width=False):
    """
    Action button with custom action
    
    Args:
        label: Button label
        action: Function to call when button is clicked
        key: Unique key for the button
        use_container_width: Whether to use container width
    
    Returns:
        bool: True if button is clicked
    """
    if st.button(label, key=key, use_container_width=use_container_width):
        if action:
            action()
        return True
    return False
