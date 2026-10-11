import streamlit as st

# ==============================================================================
# DYNAMIC KEYWORD MATCHER & PRISM RULES
# ==============================================================================

PRISM_MAPPING_RULES = {
    "Protector's Tuning Prism": {
        "category": "Defensive & Survivability",
        "keywords": [
            "life", "armor", "armour", "damage reduction", "fortify", "barrier", 
            "thorns", "life on kill", "life on hit", "healing", "impairment reduction",
            "dodge", "life regeneration", "potion", "maximum life", "life per"
        ],
        "description": "Protects armor, maximum health, damage mitigation, and life recovery stats."
    },
    "Chromatic Tuning Prism": {
        "category": "Resistances",
        "keywords": [
            "resistance", "resist", "fire resist", "cold resist", "lightning resist", 
            "poison resist", "shadow resist", "physical resist", "all elements"
        ],
        "description": "Targets individual or elemental resistance stat pools."
    },
    "Aggressive Tuning Prism": {
        "category": "Offensive & Output",
        "keywords": [
            "damage", "critical", "vulnerable", "attack speed", "overpower", 
            "damage over time", "dot", "physical damage", "fire damage", "cold damage",
            "lightning damage", "poison damage", "shadow damage", "elemental damage",
            "close enemies", "distant enemies", "crowd controlled", "injured", "healthy",
            "multiplier", "weapon damage", "total damage", "berserking"
        ],
        "description": "Focuses on damage multipliers (Crit, Vulnerable, Physical), attack speed, and offensive modifiers."
    },
    "Pragmatic Tuning Prism": {
        "category": "Utility & Mobility",
        "keywords": [
            "movement speed", "cooldown reduction", "evade", "lucky hit", 
            "crowd control duration", "shrine duration", "control impaired",
            "impairment", "potion capacity", "healing received"
        ],
        "description": "Controls movement, cooldowns, lucky hit proc chances, and movement utilities."
    },
    "Resourceful Tuning Prism": {
        "category": "Resource Management",
        "keywords": [
            "resource", "fury", "mana", "energy", "spirit", "essence", 
            "resource generation", "resource cost", "fury generation", 
            "mana regeneration", "essence generation", "vigor",
            "fury regeneration", "primary resource", "fury cost"
        ],
        "description": "Adjusts primary resource pools, resource costs, and resource generation."
    },
    "Adept's Tuning Prism": {
        "category": "Skills & Attributes",
        "keywords": [
            "ranks to", "ranks of", "strength", "intelligence", "willpower", 
            "dexterity", "all stats", "core skills", "defensive skills", 
            "mastery skills", "passive", "imbuement", "conjuration",
            "basic skills", "main stat", "war cry", "shout", "brawling",
            "weapon mastery", "combat skills"
        ],
        "description": "Modifies skill rank points, passive skill bonuses, and core character attributes."
    }
}

# Expanded list including War Cry ranks, other skill ranks, and Fury options
COMMON_AFFIX_PRESETS = [
    # ===== Defensive / Survivability =====
    "+ Maximum Life",
    "+% Maximum Life",
    "+ Armor",
    "+% Total Armor",
    "% Damage Reduction",
    "% Damage Reduction from Close Enemies",
    "% Damage Reduction from Distant Enemies",
    "% Damage Reduction while Injured",
    "% Barrier Generation",
    "% Fortify Generation",
    "+ Thorns",
    "+ Life on Kill",
    "+ Life on Hit",
    "+ Life Regeneration",
    "+ Life Regeneration while Not Damaged Recently",
    "% Healing Received",
    "% Dodge Chance",
    "+ Potion Capacity",
    "% Impairment Reduction",
    "% Control Impaired Duration Reduction",

    # ===== Elemental / Single Resistances =====
    "% Resistance to All Elements",
    "% Fire Resistance",
    "% Cold Resistance",
    "% Lightning Resistance",
    "% Poison Resistance",
    "% Shadow Resistance",
    "% Physical Resistance",

    # ===== Offensive / Damage Multipliers & Stats =====
    "% Critical Strike Chance",
    "% Critical Strike Damage [Multiplier / x]",
    "% Vulnerable Damage [Multiplier / x]",
    "% Overpower Damage",
    "% Overpower Damage [Multiplier / x]",
    "% Attack Speed",
    "% Basic Attack Speed",
    "% Damage",
    "% Total Damage Multiplier [x]",
    "% Physical Damage [Multiplier / x]",
    "% Fire Damage [Multiplier / x]",
    "% Cold Damage [Multiplier / x]",
    "% Lightning Damage [Multiplier / x]",
    "% Poison Damage [Multiplier / x]",
    "% Shadow Damage [Multiplier / x]",
    "% Elemental Damage [Multiplier / x]",
    "% Damage Over Time [Multiplier / x]",
    "% Damage to Close Enemies",
    "% Damage to Distant Enemies",
    "% Damage to Crowd Controlled Enemies",
    "% Damage to Injured Enemies",
    "% Damage to Healthy Enemies",
    "% Damage while Healthy",
    "% Damage while Injured",
    "% Damage while Berserking",
    "+ Weapon Damage",
    "% Lucky Hit Chance",
    "Lucky Hit: Up to a % Chance to ...",

    # ===== Utility / Mobility =====
    "% Movement Speed",
    "% Movement Speed after Evading",
    "+ Maximum Evade Charges",
    "Attacks Reduce Evade's Cooldown",
    "% Cooldown Reduction [Multiplier / x]",
    "% Crowd Control Duration",
    "% Shrine Duration",

    # ===== Resource (including Fury) =====
    "% Resource Generation",
    "% Fury Generation",
    "% Resource Cost Reduction [Multiplier / x]",
    "% Fury Cost Reduction",
    "+ Maximum Primary Resource",
    "+ Maximum Fury",
    "+ Maximum Mana / Energy / Spirit / Essence / Vigor",
    "+ Fury Regeneration",
    "+ Fury Regeneration per Second",
    "Lucky Hit: Restore Primary Resource",
    "Lucky Hit: Restore Fury",
    "% Resource per Second",
    "Resource on Kill",
    "Fury on Kill",

    # ===== Core Attributes =====
    "+ Strength",
    "+ Dexterity",
    "+ Intelligence",
    "+ Willpower",
    "+ All Stats",
    "% Strength / Dexterity / Intelligence / Willpower",

    # ===== Skill Ranks (Generic + Common Specific) =====
    "+ Ranks to Core Skills",
    "+ Ranks to Basic Skills",
    "+ Ranks to All Defensive Skills",
    "+ Ranks to Passive Skills",
    "+ Ranks to Mastery Skills",
    "+ Ranks to Imbuement Skills",
    "+ Ranks to Conjuration Skills",
    "+ Ranks to Brawling Skills",
    "+ Ranks to Weapon Mastery Skills",
    "+ Ranks to Combat Skills",
    "+ Ranks to Shout Skills",

    # Barbarian-specific skill ranks
    "+ Ranks to War Cry",
    "+ Ranks to Challenging Shout",
    "+ Ranks to Rallying Cry",
    "+ Ranks to Iron Skin",
    "+ Ranks to Ground Stomp",
    "+ Ranks to Leap",
    "+ Ranks to Kick",
    "+ Ranks to Charge",
    "+ Ranks to Double Swing",
    "+ Ranks to Hammer of the Ancients",
    "+ Ranks to Rend",
    "+ Ranks to Upheaval",
    "+ Ranks to Whirlwind",
    "+ Ranks to Death Blow",
    "+ Ranks to Rupture",
    "+ Ranks to Steel Grasp",
    "+ Ranks to Mighty Throw",

    # Placeholder for any other specific skill
    "+ Ranks to [Specific Skill / Category]",
]


def resolve_prism_for_affix(affix_text: str) -> tuple[str, str, str]:
    clean_text = affix_text.lower().strip()
    for prism_name, data in PRISM_MAPPING_RULES.items():
        for keyword in data["keywords"]:
            if keyword in clean_text:
                return prism_name, data["category"], data["description"]
                
    return (
        "Special / Generic Tuning Prism", 
        "General Crafting Pool", 
        "No explicit keyword match found. Uses generic category pool."
    )


# ==============================================================================
# STREAMLIT UI (4 AFFIX SLOTS WITH MULTIPLIER LABELS)
# ==============================================================================

st.set_page_config(
    page_title="Diablo 4 Horadric Crafting Assistant (4 slots)",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Diablo 4 Horadric Crafting & Tuning Prism Planner")
st.caption("Configured for 4-affix gear slots with explicit Multiplier [x] tagging. "
           "Presets now include common Occultist options + War Cry ranks + Fury generation.")

st.info(
    "**Occultist note:** When you enchant at the Occultist you can view the *full* list of possible "
    "replacement affixes for that slot. The presets below cover the most commonly used options "
    "(including + Ranks to War Cry and Fury regen). Use **Custom Free-Text** mode for any exact line."
)

st.markdown("---")

input_mode = st.radio(
    "Choose Input Method:",
    options=["Preset Selection (Quick)", "Custom Free-Text / Greater Affix Mode"],
    horizontal=True
)

current_slots = []
target_slots = []

if input_mode == "Preset Selection (Quick)":
    st.subheader("1. Current Armour Affixes (4 Slots)")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        c1 = st.selectbox("Slot 1 (Current)", COMMON_AFFIX_PRESETS, index=0)
    with col2:
        c2 = st.selectbox("Slot 2 (Current)", COMMON_AFFIX_PRESETS, index=10)
    with col3:
        c3 = st.selectbox("Slot 3 (Current)", COMMON_AFFIX_PRESETS, index=18)
    with col4:
        c4 = st.selectbox("Slot 4 (Current)", COMMON_AFFIX_PRESETS, index=1)

    st.subheader("2. Target Armour Affixes (4 Slots)")
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        t1 = st.selectbox("Slot 1 (Target)", COMMON_AFFIX_PRESETS, index=0)
    with col6:
        t2 = st.selectbox("Slot 2 (Target)", COMMON_AFFIX_PRESETS, index=19)
    with col7:
        t3 = st.selectbox("Slot 3 (Target)", COMMON_AFFIX_PRESETS, index=20)
    with col8:
        t4 = st.selectbox("Slot 4 (Target)", COMMON_AFFIX_PRESETS, index=1)

    current_slots = [c1, c2, c3, c4]
    target_slots = [t1, t2, t3, t4]

else:
    st.info("💡 Type any affix line directly into the 4 slots below (copy-paste from the Occultist list if desired). "
            "Add '[Multiplier / x]' to signify separate multiplicative scaling. Check Greater Affix if needed.")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Current Armour Affixes (4 Slots)")
        c1 = st.text_input("Current Slot 1", "+1,200 Maximum Life")
        ga_c1 = st.checkbox("Greater Affix (GA)", key="ga_c1")
        
        c2 = st.text_input("Current Slot 2", "+15% Fire Resistance")
        ga_c2 = st.checkbox("Greater Affix (GA)", key="ga_c2")
        
        c3 = st.text_input("Current Slot 3", "+50% Critical Strike Damage [Multiplier / x]")
        ga_c3 = st.checkbox("Greater Affix (GA)", key="ga_c3")

        c4 = st.text_input("Current Slot 4", "+120 Armor")
        ga_c4 = st.checkbox("Greater Affix (GA)", key="ga_c4")
        
    with col_right:
        st.subheader("Target Armour Affixes (4 Slots)")
        t1 = st.text_input("Target Slot 1", "+1,200 Maximum Life")
        ga_t1 = st.checkbox("Greater Affix (GA)", key="ga_t1")
        
        t2 = st.text_input("Target Slot 2", "+30% Vulnerable Damage [Multiplier / x]")
        ga_t2 = st.checkbox("Greater Affix (GA)", key="ga_t2")
        
        t3 = st.text_input("Target Slot 3", "+25% Physical Damage [Multiplier / x]")
        ga_t3 = st.checkbox("Greater Affix (GA)", key="ga_t3")

        t4 = st.text_input("Target Slot 4", "+120 Armor")
        ga_t4 = st.checkbox("Greater Affix (GA)", key="ga_t4")

    current_slots = [
        f"{c1} [GA]" if ga_c1 and c1 else c1,
        f"{c2} [GA]" if ga_c2 and c2 else c2,
        f"{c3} [GA]" if ga_c3 and c3 else c3,
        f"{c4} [GA]" if ga_c4 and c4 else c4
    ]
    
    target_slots = [
        f"{t1} [GA]" if ga_t1 and t1 else t1,
        f"{t2} [GA]" if ga_t2 and t2 else t2,
        f"{t3} [GA]" if ga_t3 and t3 else t3,
        f"{t4} [GA]" if ga_t4 and t4 else t4
    ]

st.markdown("---")

current_clean = {s.strip() for s in current_slots if s.strip()}
target_clean = {s.strip() for s in target_slots if s.strip()}

to_keep = current_clean.intersection(target_clean)
to_remove = current_clean - target_clean
to_add = target_clean - current_clean

st.header("📋 Horadric Cube Crafting Recipe Plan")

if to_keep:
    st.success(f"✅ **AFFIXES TO KEEP:** {', '.join(to_keep)}")

if to_remove:
    st.subheader("🔴 Removal / Reroll Steps:")
    for affix in sorted(to_remove):
        prism, category, desc = resolve_prism_for_affix(affix)
        with st.expander(f"Remove: {affix} ➔ Place [{prism}] into Cube"):
            st.write(f"**Prism Category:** {category}")
            st.caption(desc)

if to_add:
    st.subheader("🔵 Addition / Focused Reroll Steps:")
    for affix in sorted(to_add):
        prism, category, desc = resolve_prism_for_affix(affix)
        with st.expander(f"Add/Target: {affix} ➔ Place [{prism}] into Cube"):
            st.write(f"**Prism Category:** {category}")
            st.caption(desc)

if not to_remove and not to_add and current_clean:
    st.balloons()
    st.success("🎉 Your gear already perfectly matches all 4 target affixes!")