
# Mock Data for PM-JAY Packages
# Focus on Burns for this PoC as per problem statement

PACKAGES = {
    "BM001A": {
        "code": "BM001A",
        "name": "Superficial Burns (<= 10% TBSA)",
        "min_tbsa": 0,
        "max_tbsa": 10,
        "max_amount": 5000,
        "description": "Conservative management of superficial burns."
    },
    "BM001B": {
        "code": "BM001B",
        "name": "Moderate Burns (10% - 40% TBSA)",
        "min_tbsa": 10,
        "max_tbsa": 40,
        "max_amount": 15000,
        "description": "Management of moderate burns requiring dressings."
    },
    "BM001C": {
        "code": "BM001C",
        "name": "Severe Burns (40% - 60% TBSA)",
        "min_tbsa": 40,
        "max_tbsa": 60,
        "max_amount": 40000,
        "description": "Management of severe burns, potential debridement."
    },
    "BM001D": {
        "code": "BM001D",
        "name": "Critical Burns (> 60% TBSA)",
        "min_tbsa": 60,
        "max_tbsa": 100,
        "max_amount": 100000,
        "description": "ICU management for critical burns."
    }
}

def get_package_by_code(code):
    return PACKAGES.get(code)

def get_recommended_package(tbsa_percentage):
    for code, pkg in PACKAGES.items():
        # strict comparison for upper bound to avoid overlap confusion, handle edge cases
        if pkg["min_tbsa"] < tbsa_percentage <= pkg["max_tbsa"]:
            return pkg
    # Handle 0-10 explicit case better if needed, or > max
    if tbsa_percentage <= 10:
         return PACKAGES["BM001A"]
    return None
