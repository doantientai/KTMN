from offline.get_verse import multi_verse_lookup

# feeling = "joy"
# print("you feel: ", feeling)
# verse = get_verse_by_feeling(feeling)
# print(verse)

addr_str = "Luke 2:2-4"
# addr_str = "Psalm 2:2-3"
# version = "VIET"
version = "NIV"

verse_content, addr_vi = multi_verse_lookup(addr_str, version)

print("verse_content", verse_content)
print("addr_vi", addr_vi)

# print(verse_content)
# print(addr_vi)
