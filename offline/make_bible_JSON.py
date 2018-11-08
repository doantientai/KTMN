"""
    create dict bible
    for each feeling in list feelings
        get list keywords
        create dict feeling_verses
        for each keyword in list keywords
            get the list addresses

            for each address in list addresses
                get verse_content
                append verse_content to feeling_verses
        append feeling_verses to dict bible
    dump dict bible to json file
"""

feelings_keywords = {
    "excited": ["encourage", "strength", "determination"],
    "hopeful": ["hope", "trust", "faith"],
    "happy": ["joy", "happiness", "thankfulness"],
    "blessed": ["thankfulness", "trust"],
    "sad": ["sadness", "brokenness", "healing"],
    "tired": ["weariness", "strength", "encourage ", "worry"],
    "worry": ["worry", "trust"],
    "angry": ["anger", "forgiveness"],
    "lonely": ["loneliness", "trust"],
    "sorry": ["sorry", "forgiveness"],
    "depressed": ["hope", "encourage"]
}

