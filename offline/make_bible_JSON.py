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

from get_verse import get_verses_by_keyword, multi_verse_lookup
import json

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
feelings_vi = {
    "excited": "hào hứng",
    "hopeful": "hy vọng",
    "happy": "vui mừng",
    "blessed": "được phước",
    "sad": "buồn",
    "tired": "mệt mỏi",
    "worry": "lo lắng",
    "angry": "tức giận",
    "lonely": "cô đơn",
    "sorry": "có lối",
    "depressed": "chán nàn",
}


def combine_lists(list_1, list_2):
    in_1 = set(list_1)
    in_2 = set(list_2)
    in_2_but_not_in_1 = in_2 - in_1
    return list_1 + list(in_2_but_not_in_1)


def main():
    bible_version = "VIET"
    bible = {}
    for feeling, keywords in feelings_keywords.items():
        print("-----------------------------\nFeeling:", feeling)
        feeling_verses = []
        list_addr_total = []
        for keyword in keywords:
            list_addr = get_verses_by_keyword(keyword)
            list_addr_total = combine_lists(list_addr, list_addr_total)
        print("Total:", len(list_addr_total), "addresses from", end=" ")
        print(keywords)

        # for addr in list_addr_total:
        for addr in list_addr_total[:2]:
            verse_content, addr_vi = multi_verse_lookup(addr, version=bible_version)
            wraped_verse = "\"" + verse_content + "\"" + " - " + addr_vi
            feeling_verses.append(wraped_verse)
        bible[feeling] = feeling_verses
        # exit()

    with open(bible_version+'.json', 'w') as fp:
        json.dump(bible, fp)


if __name__ == "__main__":
    main()
