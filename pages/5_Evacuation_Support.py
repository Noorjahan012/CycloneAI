import streamlit as st


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Evacuation Support | CycloneAI",
    page_icon="🛟",
    layout="wide"
)


# --------------------------------------------------
# PAGE TITLE AND INTRODUCTION
# --------------------------------------------------

st.title("🛟 CycloneAI - Evacuation Support")

st.write(
    "A cyclone preparedness and safety information module "
    "designed to help users access important guidance and official resources."
)

st.warning(
    "CycloneAI does not issue official alerts, determine evacuation orders, "
    "or identify verified local shelters. Always follow instructions "
    "from government and emergency-management authorities."
)


# --------------------------------------------------
# EMERGENCY INFORMATION
# --------------------------------------------------

st.header("1. Emergency Information")

st.markdown(
    """
    If a cyclone is threatening your area:

    - Follow instructions from local authorities.
    - If officials order evacuation, leave promptly using the recommended route.
    - Do not wait for this application to confirm a warning.
    - If you are in immediate danger, contact the appropriate emergency service.
    """
)

st.info(
    "In India, dial 112 for emergency assistance. "
    "For cyclone warnings, check official meteorological bulletins."
)


# --------------------------------------------------
# BEFORE A CYCLONE
# --------------------------------------------------

st.header("2. Cyclone Preparedness Checklist")

st.write("Tick each item as you prepare.")

before_items = [
    "Monitor official weather bulletins and local alerts.",
    "Know the evacuation instructions for your area.",
    "Identify an official shelter or safe location through local authorities.",
    "Charge mobile phones and power banks.",
    "Keep essential medicines and first-aid supplies ready.",
    "Store drinking water and non-perishable food.",
    "Keep identity documents in waterproof packaging.",
    "Prepare a torch, spare batteries, and a battery-powered radio if available.",
    "Secure loose objects around your home when it is safe to do so.",
    "Plan how to assist children, older adults, and people with disabilities."
]

completed_before = []

for index, item in enumerate(before_items):
    if st.checkbox(item, key=f"before_{index}"):
        completed_before.append(item)

before_progress = len(completed_before) / len(before_items)

st.progress(before_progress)

st.write(
    f"Preparedness checklist: {len(completed_before)} "
    f"of {len(before_items)} items completed."
)


# --------------------------------------------------
# EMERGENCY KIT
# --------------------------------------------------

st.header("3. Emergency Kit Checklist")

st.write("Check the supplies you have prepared.")

kit_items = [
    "Drinking water",
    "Ready-to-eat food",
    "First-aid kit",
    "Essential medicines",
    "Torch and spare batteries",
    "Fully charged phone and power bank",
    "Copies of important documents",
    "Cash and essential identification",
    "Basic clothing and hygiene supplies",
    "Baby supplies or disability-related essentials, if needed"
]

completed_kit = []

for index, item in enumerate(kit_items):
    if st.checkbox(item, key=f"kit_{index}"):
        completed_kit.append(item)

kit_progress = len(completed_kit) / len(kit_items)

st.progress(kit_progress)

st.write(
    f"Emergency kit checklist: {len(completed_kit)} "
    f"of {len(kit_items)} items completed."
)


# --------------------------------------------------
# DURING A CYCLONE
# --------------------------------------------------

st.header("4. Safety During a Cyclone")

with st.expander("If you are staying indoors"):
    st.markdown(
        """
        - Stay inside a sturdy building and away from windows.
        - Follow official instructions about moving to a safer part of the building.
        - Keep your phone charged and monitor official updates.
        - Avoid touching damaged electrical equipment or fallen wires.
        - Do not go outside during a temporary lull; dangerous winds may return.
        """
    )

with st.expander("If authorities order evacuation"):
    st.markdown(
        """
        - Leave as early as authorities instruct.
        - Use the routes recommended by emergency officials.
        - Take your emergency kit and essential medicines.
        - Follow instructions from emergency personnel.
        - Never enter floodwater on foot or in a vehicle.
        """
    )

with st.expander("If flooding occurs"):
    st.markdown(
        """
        - Move to safer, higher ground if instructed and if it is safe to do so.
        - Avoid rivers, drains, flooded roads, and moving water.
        - Never attempt to cross a flooded road.
        - Stay away from fallen power lines.
        - Contact emergency services if you are trapped or in immediate danger.
        """
    )


# --------------------------------------------------
# AFTER A CYCLONE
# --------------------------------------------------

st.header("5. Safety After a Cyclone")

st.markdown(
    """
    - Return home only when authorities say it is safe.
    - Avoid damaged buildings and fallen electrical wires.
    - Treat floodwater as potentially contaminated.
    - Use safe drinking water and follow public-health advice.
    - Report dangerous conditions to the appropriate authorities.
    - Check on neighbours if doing so does not put you at risk.
    - Continue monitoring official updates because hazards can persist.
    """
)


# --------------------------------------------------
# OFFICIAL RESOURCES
# --------------------------------------------------

st.header("6. Official Information and Assistance")

st.markdown(
    """
    Use these official sources for updated information:

    - **India Meteorological Department (IMD):**
      [Official weather information](https://mausam.imd.gov.in/)

    - **National Disaster Management Authority (NDMA):**
      [Disaster preparedness and safety](https://ndma.gov.in/)

    - **National Disaster Response Force (NDRF):**
      [Disaster response information](https://ndrf.gov.in/)

    - **Emergency Response Support System (ERSS):**
      [Official emergency information — Ministry of Home Affairs](https://www.mha.gov.in/en/commoncontent/emergency-response-support-system-erss)
    """
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "CycloneAI is an educational prototype. This checklist does not "
    "replace official cyclone warnings, evacuation orders, or professional "
    "emergency advice."
)