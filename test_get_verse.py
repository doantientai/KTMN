from get_verse import get_verse_by_feeling, verse_lookup, get_verse_list

# feeling = "joy"
# print("you feel: ", feeling)
# verse = get_verse_by_feeling(feeling)
# print(verse)

addr_str = "Luke 2:2-4"
# addr_str = "Psalm 2:2-3"
# version = "VIET"
version = "NIV"

### check if this address contains multiple sentences
addr_chapter = addr_str[:addr_str.index(":")]
addr_sentences = addr_str[addr_str.index(":") + 1:]

### Reject if address contains 2 colons
if ":" in addr_sentences:
    print("Invalid address:", addr_str)
    exit()

if "-" in addr_sentences:
    sentence_begin = addr_sentences[:addr_sentences.index("-")]
    sentence_end = addr_sentences[addr_sentences.index("-") + 1:]
    print(addr_sentences)
    print(sentence_begin)
    print(sentence_end)

    ### look up each sentence
    verse_content_sum = ""
    verse_address_sum = ""
    got_book_chapter = False

    if int(sentence_begin) < int(sentence_end):
        for number in range(int(sentence_begin), int(sentence_end)+1):
            verse_content, addr_vi = verse_lookup(addr_chapter + ":" + str(number), version=version)
            verse_content_sum = verse_content_sum + " " + verse_content

            if not got_book_chapter:
                verse_address_sum = addr_vi[:addr_vi.index(":")]
    else:
        print("Invalid address", addr_str)
        exit()

    ### take the address in target language
    verse_address_sum = verse_address_sum + ":" + addr_sentences

else:
    verse_content_sum, verse_address_sum = verse_lookup(addr_str, version=version)

print("verse_content_sum", verse_content_sum)
print("verse_address_sum", verse_address_sum)

# print(verse_content)
# print(addr_vi)
