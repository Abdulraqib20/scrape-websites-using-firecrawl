import streamlit as st
import os
import sys
from pathlib import Path
import gc
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import time
import pandas as pd
from typing import Dict, Any, List, Union
import base64
from pydantic import BaseModel, Field
import inspect
import traceback
import random

load_dotenv()
from config.appconfig import FIRECRAWL_API_KEY

#============================
# Custom CSS for enhanced UI
#============================
def apply_custom_css():
    st.markdown("""
    <style>
    /* Dark theme compatibility */
    [data-theme="dark"] {
        --primary-color: #FF6B6B;
        --secondary-color: #4DA8DA;
        --background-color: #1E1E1E;
        --card-background: #2D2D2D;
        --text-color: #E0E0E0;
        --sidebar-color: #252525;
    }
    /* Main color scheme */
    :root {
        --primary-color: #FF4B4B;
        --secondary-color: #0083B8;
        --background-color: #f8f9fa;
        --card-background: white;
        --text-color: #333;
        --sidebar-color: #f0f2f6;
    }
    
    /* Overall page styling */
    .main {
        background-color: var(--background-color);
        padding: 1rem;
    }
    
    /* Header styling */
    h1 {
        color: var(--primary-color);
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
    }
    
    h2, h3 {
        color: var(--secondary-color);
        font-weight: 600 !important;
    }
    
    /* Card styling */
    .css-1r6slb0, .css-keje6w {
        background-color: var(--card-background);
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 1.5rem !important;
        margin-bottom: 1.5rem;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: var(--card-background);
        border-radius: 15px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar styling */
    .css-1544g2n {
        background-color: var(--sidebar-color);
    }
    
    /* Table styling */
    # table {
    #     width: 100%;
    #     border-collapse: separate;
    #     border-spacing: 0;
    #     margin: 1rem 0;
    #     border-radius: 8px;
    #     overflow: hidden;
    #     box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    # }
    /* Table styling - Updated for better dark mode compatibility */
    table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 1rem 0;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        color: var(--text-color);
    }
    
    th {
        background-color: var(--secondary-color);
        color: white;
        padding: 12px 15px;
        text-align: left;
        font-weight: 600;
    }
    
    td {
        padding: 10px 15px;
        border-bottom: 1px solid var(--sidebar-color);
        background-color: var(--card-background);
    }
    
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    
    tr:last-child td {
        border-bottom: none;
    }
    
    tr:hover {
        background-color: #f0f7ff;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
    }
    
    /* Logo animation */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .logo-animation {
        animation: pulse 2s infinite;
        display: inline-block;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: var(--primary-color);
    }
    
    /* Feature card */
    .feature-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 4px solid var(--primary-color);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* User message styling */
    .user-message {
        background-color: var(--sidebar-color) !important;
        border-radius: 18px 18px 0 18px !important;
        color: var(--text-color) !important;
    }
    
    .assistant-message {
        background-color: var(--card-background) !important;
        border-radius: 18px 18px 18px 0 !important;
        color: var(--text-color) !important;
    }
    
    /* Loading animation */
    .loading-animation {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(0, 0, 0, 0.1);
        border-radius: 50%;
        border-top-color: var(--primary-color);
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Footer styling */
    .footer {
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #eee;
        text-align: center;
        color: #777;
        font-size: 0.85rem;
    }
    
    /* Tooltip */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
    """, unsafe_allow_html=True)

#=============================
# Feature highlight cards
#=============================
def render_logo():
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div class="logo-animation" style="font-size: 3rem; margin-right: 15px;">🕸️</div>
        <div>
            <h1 style="margin: 0; padding: 0;">Firecrawl Scraper</h1>
            <p style="color: #777; margin: 0; padding: 0;">Turn any website into structured data with AI</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

#=============================
# Logo and Branding
#=============================
def render_feature_cards():
    st.markdown("""
    <div style="display: flex; flex-wrap: wrap; justify-content: space-between; margin: 20px 0;">
        <div class="feature-card" style="flex: 0 0 calc(33% - 20px);">
            <h3 style="color: #FF4B4B;">🔍 Instant Extraction</h3>
            <p>Extract structured data from any website using natural language prompts.</p>
        </div>
        <div class="feature-card" style="flex: 0 0 calc(33% - 20px);">
            <h3 style="color: #FF4B4B;">⚙️ Custom Schema</h3>
            <p>Define exactly what data you need with our simple schema builder.</p>
        </div>
        <div class="feature-card" style="flex: 0 0 calc(33% - 20px);">
            <h3 style="color: #FF4B4B;">🔄 API Conversion</h3>
            <p>Convert any website into a structured API that returns clean JSON.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
#=============================
# Animated loading component
#=============================  
def animated_loading(message="Processing"):
    loading_container = st.empty()
    loading_messages = [
        "Analyzing website structure...",
        "Identifying relevant elements...",
        "Extracting requested data...",
        "Processing information...",
        "Formatting results...",
        "Almost there..."
    ]
    
    progress_bar = st.progress(0)
    
    for i in range(101):
        # Update message occasionally
        if i % 20 == 0:
            current_message = loading_messages[i // 20] if i // 20 < len(loading_messages) else loading_messages[-1]
            loading_container.markdown(f"<div style='display: flex; align-items: center;'><div class='loading-animation'></div><div style='margin-left: 10px;'>{current_message}</div></div>", unsafe_allow_html=True)
        
        # Update progress bar
        progress_bar.progress(i)
        time.sleep(0.02)
    
    return loading_container, progress_bar

#=============================
# Display extraction results with typing animation effect
#=============================
def display_result_with_animation(data, delay=0.01):
    """Display extraction results with typing animation effect."""
    # Create empty placeholder
    result_container = st.empty()
    
    # Start with "Extraction complete!" message
    result_container.markdown("""
    <div style="background-color: #f0fff4; padding: 15px; border-radius: 10px; border-left: 4px solid #38a169; margin-bottom: 20px;">
        <h3 style="margin-top: 0; color: #38a169;">✅ Extraction Complete!</h3>
        <p>Here's what we found:</p>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(1)  # Pause for emphasis
    
    # Display the data table
    if isinstance(data, str):
        result_container.markdown(data)
    else:
        result_container.dataframe(data)
    
    return result_container
    


@st.cache_resource
def load_app():
    app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
    return app

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "schema_fields" not in st.session_state:
    st.session_state.schema_fields = [{"name": "", "type": "str"}]

if "extraction_count" not in st.session_state:
    st.session_state.extraction_count = 0

if "show_intro" not in st.session_state:
    st.session_state.show_intro = True

def reset_chat():
    st.session_state.messages = []
    gc.collect()

def create_dynamic_model(fields):
    """Create a dynamic Pydantic model from schema fields."""
    field_annotations = {}
    for field in fields:
        if field["name"]:
            # Convert string type names to actual types
            type_mapping = {
                "str": str,
                "bool": bool,
                "int": int,
                "float": float
            }
            field_annotations[field["name"]] = type_mapping[field["type"]]
    
    # Dynamically create the model class
    return type(
        "ExtractSchema",
        (BaseModel,),
        {
            "__annotations__": field_annotations
        }
    )

def create_schema_from_fields(fields):
    """Create schema using Pydantic model."""
    if not any(field["name"] for field in fields):
        return None
    
    model_class = create_dynamic_model(fields)
    return model_class.model_json_schema()

def convert_to_table(data: Union[List[Dict], Dict]) -> str:
    """Convert data to a markdown table.
    
    Args:
        data: Either a list of dictionaries or a dictionary
        
    Returns:
        A markdown table representation of the data
    """
    if not data:
        return "No data extracted"
    
    try:
        # Handle different data structures
        if isinstance(data, dict):
            # If it's a dictionary, convert to a dataframe with one row
            df = pd.DataFrame([data])
        elif isinstance(data, list):
            if all(isinstance(item, dict) for item in data):
                # If it's a list of dictionaries, convert to dataframe
                df = pd.DataFrame(data)
            else:
                # If it's a list of non-dictionaries, create a simple dataframe
                df = pd.DataFrame({"Value": data})
        else:
            # For other types, create a simple one-cell dataframe
            df = pd.DataFrame({"Value": [str(data)]})
        
        # Handle empty dataframe
        if df.empty:
            return "No data extracted"
            
        # Return as markdown table
        return df.to_markdown(index=False)
    
    except Exception as e:
        st.error(f"Error converting data to table: {str(e)}")
        return f"```\n{str(data)}\n```"

def stream_text(text: str, delay: float = 0.001) -> None:
    """Stream text with a typing effect."""
    placeholder = st.empty()
    displayed_text = ""
    
    for char in text:
        displayed_text += char
        placeholder.markdown(displayed_text)
        time.sleep(delay)
    
    return placeholder

def format_extraction_result(data):
    """Format the extraction result for display with improved handling for lists of items."""
    if not data:
        return "No data extracted"
    
    try:
        # Check various data structures that might be returned
        if 'data' in data:
            result_data = data['data']
            
            # Handle case where data is a single project instead of a list of projects
            if isinstance(result_data, dict) and not any(isinstance(v, list) for v in result_data.values()):
                # Convert single project to a list of one project
                result_data = [result_data]
                return pd.DataFrame(result_data)  # Return DataFrame instead of Markdown
            
            # Handle case where data is a dictionary with a key containing a list of projects
            elif isinstance(result_data, dict):
                for key, value in result_data.items():
                    if isinstance(value, list) and len(value) > 0:
                        # If we find a list in any of the values, use that for the table
                        return pd.DataFrame(value)  # Return DataFrame instead of Markdown
                
                # If we didn't find a list but have dict data, convert the dict to a list of one item
                return pd.DataFrame([result_data])  # Return DataFrame instead of Markdown
            
            # Handle case where data is already a list of projects
            elif isinstance(result_data, list):
                return pd.DataFrame(result_data)  # Return DataFrame instead of Markdown
            
            else:
                return f"```\n{str(result_data)}\n```"
        else:
            return pd.DataFrame(data if isinstance(data, list) else [data])  # Return DataFrame instead of Markdown
            
    except Exception as e:
        st.error(f"Error formatting extraction result: {str(e)}")
        return f"```\n{str(data)}\n```"


# Improve the extraction call with more specific parameters
def extract_projects(app, website_url, prompt):
    """Enhanced extraction function specifically for projects."""
    
    # Create a more specific schema for projects
    projects_schema = {
        "type": "object",
        "properties": {
            "projects": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "link": {"type": "string"}
                    },
                    "required": ["title"]
                }
            }
        }
    }
    
    # More specific extraction parameters
    extract_params = {
        'prompt': prompt,
        'schema': projects_schema,
        'include_html': True,  # Sometimes helps with extraction
        'max_results': 20  # Ensure we get multiple results
    }
    
    return app.extract(
        [website_url],
        extract_params
    )

# ===========================
#   Chat Interface
# ===========================
def show_chat_message(message, is_user=False):
    """Display chat messages with enhanced styling."""
    message_class = "user-message" if is_user else "assistant-message"
    
    # Handle DataFrame display differently
    if isinstance(message, pd.DataFrame):
        st.markdown(f"""
        <div class="{message_class}" style="padding: 15px; margin-bottom: 10px;">
            <div style="display: flex; align-items: flex-start;">
                <div style="width: 35px; height: 35px; border-radius: 50%; background-color: {'#0083B8' if is_user else '#FF4B4B'}; color: white; display: flex; justify-content: center; align-items: center; margin-right: 10px; font-weight: bold;">
                    {'U' if is_user else 'F'}
                </div>
                <div style="flex-grow: 1;">
                    <p>Here's what I found:</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(message, use_container_width=True)
    else:
        st.markdown(f"""
        <div class="{message_class}" style="padding: 15px; margin-bottom: 10px;">
            <div style="display: flex; align-items: flex-start;">
                <div style="width: 35px; height: 35px; border-radius: 50%; background-color: {'#0083B8' if is_user else '#FF4B4B'}; color: white; display: flex; justify-content: center; align-items: center; margin-right: 10px; font-weight: bold;">
                    {'U' if is_user else 'F'}
                </div>
                <div style="flex-grow: 1;">
                    {message}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def add_example_button():
    """Add a button to insert an example prompt."""
    example_prompts = [
        "Extract all product names, prices, and image URLs from this e-commerce site",
        "Find all blog post titles, publish dates, and author names",
        "Extract the company contact information including email, phone, and address",
        "Get all project titles, descriptions, and links from the portfolio section",
        "Extract all team member names, positions, and bios from the about page"
    ]
    
    if st.button("📋 Try an example prompt"):
        example = random.choice(example_prompts)
        st.session_state.example_prompt = example
        return example
    
    return 

# ===========================
#   Streamlit Setup
# ===========================
st.set_page_config(
        page_title="Firecrawl Web Scraper",
        page_icon="🕸️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# Apply custom CSS
apply_custom_css()


# ===========================
#   Main Chat Interface
# ===========================

# Main interface columns
left_col, right_col = st.columns([2, 1])

with left_col:
    render_logo()
    
    if st.session_state.show_intro:
        st.markdown("""
        <div style="background-color: #f0f7ff; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h2 style="color: #0083B8; margin-top: 0;">Extract Data from Any Website</h2>
            <p>This app uses AI to convert websites into structured data. Simply:</p>
            <ol>
                <li><b>Enter a website URL</b> in the sidebar</li>
                <li><b>Define a schema</b> (optional) or use our default extraction</li>
                <li><b>Ask a question</b> about what you want to extract</li>
            </ol>
            <p>Try prompts like "Extract all product prices" or "Get all article titles and authors"</p>
        </div>
        """, unsafe_allow_html=True)
        
        render_feature_cards()
        
        if st.button("Let's Get Started", key="start_button"):
            st.session_state.show_intro = False
            st.rerun()

    # Chat interface
    if not st.session_state.show_intro:
        st.markdown("""
        <div style="background-color: #fff; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
            <h2 style="color: #0083B8; margin-top: 0;">Extraction Chat</h2>
            <p>Ask questions about the website to extract specific data</p>
        </div>
        """, unsafe_allow_html=True)
        
        chat_container = st.container(height=400)
        with chat_container:
            for message in st.session_state.messages:
                show_chat_message(message["content"], message["role"] == "user")
        
        # Chat input and example button
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        example_prompt = add_example_button()
        
        prompt_placeholder = "Ask about the website... (e.g., 'Extract all product names and prices')"
        if hasattr(st.session_state, 'example_prompt'):
            prompt_placeholder = st.session_state.example_prompt
        
        if prompt := st.chat_input(prompt_placeholder):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with chat_container:
                show_chat_message(prompt, is_user=True)
            
            with chat_container:
                # Get website URL from the sidebar
                website_url = st.session_state.get("website_url", "")
                
                if not website_url:
                    st.error("⚠️ Please enter a website URL in the sidebar first!")
                elif not (website_url.startswith('http://') or website_url.startswith('https://')):
                    st.error("⚠️ Please enter a valid URL starting with http:// or https://")
                else:
                    try:
                        # Use animated loading
                        loading_container, progress_bar = animated_loading("Extracting data from website...")
                        
                        app = load_app()
                        schema = create_schema_from_fields(st.session_state.schema_fields)
                        
                        extract_params = {
                            'prompt': prompt,
                            'max_results': 20
                        }
                        if schema:
                            extract_params['schema'] = schema
                            
                        data = app.extract(
                            [website_url],
                            extract_params
                        )
                        
                        # Clear loading indicators
                        loading_container.empty()
                        progress_bar.empty()
                        
                        formatted_result = format_extraction_result(data)
                                                
                        # Increment extraction count
                        st.session_state.extraction_count += 1
                                                
                        # Display formatted result with animation
                        show_chat_message(formatted_result)
                        st.session_state.messages.append({"role": "assistant", "content": formatted_result})
                        
                        # Show extraction stats
                        st.success(f"✅ Extraction #{st.session_state.extraction_count} completed successfully!")
                    
                    except Exception as e:
                        error_details = traceback.format_exc()
                        st.error(f"❌ An error occurred: {str(e)}")
                        with st.expander("Error Details"):
                            st.code(error_details)

with right_col:
    # Sidebar configuration
    st.markdown("""
    <div style="background-color: #fff; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
        <h2 style="color: #0083B8; margin-top: 0;">Configuration</h2>
        <p>Set up your extraction parameters</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Website URL input with enhanced styling
    st.markdown("""
    <div style="margin-bottom: 15px;">
        <label style="font-weight: 600; color: #333; margin-bottom: 5px; display: block;">Website URL</label>
    </div>
    """, unsafe_allow_html=True)
    
    website_url = st.text_input(
        label="",
        value=st.session_state.get("website_url", ""),
        placeholder="https://example.com",
        key="website_url"
    )
    
    # Add URL validation tooltip
    if website_url and not (website_url.startswith('http://') or website_url.startswith('https://')):
        st.warning("URL must start with http:// or https://")
    
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Schema Builder with attractive styling
    st.markdown("""
    <div style="margin-bottom: 15px;">
        <h3 style="color: #0083B8; margin-top: 0;">Schema Builder <span style="color: #777; font-weight: normal; font-size: 0.8em;">(Optional)</span></h3>
        <p style="color: #555; margin-bottom: 15px;">Define fields to extract from the website</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Schema controls
    col1, col2 = st.columns(2)
    with col1:
        if len(st.session_state.schema_fields) > 1 and st.button("🗑️ Remove Field", use_container_width=True):
            st.session_state.schema_fields.pop()
            st.rerun()
    
    with col2:
        if len(st.session_state.schema_fields) < 10 and st.button("➕ Add Field", use_container_width=True):
            st.session_state.schema_fields.append({"name": "", "type": "str"})
            st.rerun()
    
    # Dynamic schema fields
    for i, field in enumerate(st.session_state.schema_fields):
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 10px; border-left: 3px solid #0083B8;">
            <p style="margin: 0; padding: 0; font-weight: 600; color: #0083B8;">Field #{i+1}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            field["name"] = st.text_input(
                "Name",
                value=field["name"],
                key=f"name_{i}",
                placeholder="e.g., title, price, url"
            )
        
        with col2:
            field["type"] = st.selectbox(
                "Type",
                options=["str", "bool", "int", "float"],
                key=f"type_{i}",
                index=0 if field["type"] == "str" else ["str", "bool", "int", "float"].index(field["type"])
            )
    
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Reset buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset Schema", use_container_width=True):
            st.session_state.schema_fields = [{"name": "", "type": "str"}]
            st.rerun()
    
    with col2:
        if st.button("🗑️ Reset Chat", use_container_width=True):
            reset_chat()
            st.session_state.extraction_count = 0
            st.rerun()
    
    # Stats and info
    if st.session_state.extraction_count > 0:
        st.markdown(f"""
        <div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; margin-top: 20px;">
            <h4 style="margin-top: 0; color: #0083B8;">Stats</h4>
            <p>📊 Extractions: {st.session_state.extraction_count}</p>
            <p>🔍 Current Website: {website_url[:30] + '...' if len(website_url) > 30 else website_url or 'None'}</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>Built with ❤️ by raqibcodes</p>
    <p>© 2025 Web Scraping Technologies</p>
</div>
""", unsafe_allow_html=True)