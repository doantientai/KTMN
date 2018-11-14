import urllib.request
from bs4 import BeautifulSoup
from random import randint
import re


def get_verse_list(keyword):
    # url = "https://www.openbible.info/topics/" + feeling
    url = "https://www.openbible.info/topics/" + keyword
    html_content = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(html_content, "html.parser")
    list_addr = soup.find_all("a", {"class": "bibleref"})

    print("found ", len(list_addr), "addresses for keyword", keyword)

    addr_chosen = randint(0, len(list_addr))

    print("addr_chosen:", addr_chosen)

    addr_str = list_addr[addr_chosen].string

    # print(addr_str)
    return addr_str


def get_verses_by_keyword(keyword):
    # url = "https://www.openbible.info/topics/" + feeling
    url = "https://www.openbible.info/topics/" + keyword
    html_content = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(html_content, "html.parser")
    list_addr_html = soup.find_all("a", {"class": "bibleref"})

    print("found ", len(list_addr_html), "addresses for keyword", keyword)

    list_addr_str = []

    for addr in list_addr_html:
        list_addr_str.append(addr.string)

    # addr_chosen = randint(0, len(list_addr))
    #
    # print("addr_chosen:", addr_chosen)
    #
    # addr_str = list_addr[addr_chosen].string
    #
    # # print(addr_str)
    return list_addr_str


# def post_process_verse(verse_content):
#     # if verse_content[0] == " ":
#     #     verse_content = verse_content[1:]
#     # re.sub(" +", " ", verse_content)
#     return verse_content


def verse_lookup(addr_str, version="VIET"):
    addr_sentence = addr_str[addr_str.index(":") + 1:]
    url = "https://www.biblegateway.com/passage/?search=" + str(addr_str) + "&version=" + version
    print("url:", url)
    html_content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html_content, "html.parser")

    if soup.find("div", {"class": "poetry"}):
        paragraph_type = "poetry"
    elif soup.find("p", {"class": "chapter-1"}):
        paragraph_type = "chapter"
    else:
        paragraph_type = "normal"

    start_content = 1
    if int(addr_sentence) == 1:
        start_content = 0

    verse_content = ""
    if paragraph_type == "poetry":
        verse_contents = soup.find("div", {"class": "poetry"}).contents[start_content].findAll(text=True)

        for i in range(1, len(verse_contents)):
            if "\xa0\xa0\xa0\xa0" in verse_contents[i]:
                verse_content = verse_content + " "
            else:
                verse_content = verse_content + verse_contents[i]

    elif paragraph_type == "chapter":
        verse_contents = soup.find("p", {"class": "chapter-1"}).contents[start_content].findAll(text=True)
        # verse_content = verse_contents
        for i in range(1, len(verse_contents)):
            # if "\xa0\xa0\xa0\xa0" in verse_contents[i]:
            #     verse_content = verse_content + " "
            # else:
            verse_content = verse_content + verse_contents[i]

    elif paragraph_type == "normal":
        if int(addr_sentence) == 1:
            verse_content = soup.find("span", {"class": "chapternum"}).next_sibling
        else:
            verse_content = soup.find("sup", {"class": "versenum"}).next_sibling

    addr_vi = soup.find("h1", {"class": "bcv"}).string
    # print(verse_content, addr_vi)

    ### Post-processing
    # verse_content = post_process_verse(verse_content)

    return verse_content, addr_vi


def multi_verse_lookup(addr_str, version):
    try:
        ### check if this address contains multiple sentences
        addr_chapter = addr_str[:addr_str.index(":")]
        addr_sentences = addr_str[addr_str.index(":") + 1:]

        ### Reject if address contains 2 colons
        if ":" in addr_sentences:
            print("Invalid address:", addr_str)
            # exit()
            return None, None

        if "-" in addr_sentences:
            sentence_begin = addr_sentences[:addr_sentences.index("-")]
            sentence_end = addr_sentences[addr_sentences.index("-") + 1:]
            # print(addr_sentences)
            # print(sentence_begin)
            # print(sentence_end)

            ### look up each sentence
            verse_content_sum = ""
            verse_address_sum = ""
            got_book_chapter = False

            if (int(sentence_begin) < int(sentence_end)) and (int(sentence_end) - int(sentence_begin) <= 5):
                for number in range(int(sentence_begin), int(sentence_end) + 1):
                    verse_content, addr_vi = verse_lookup(addr_chapter + ":" + str(number), version=version)
                    if len(verse_content) < 10:  # if a verse is too short
                        return None, None
                    verse_content_sum = verse_content_sum + " " + verse_content

                    if not got_book_chapter:
                        verse_address_sum = addr_vi[:addr_vi.index(":")]
            else:
                print("Invalid address", addr_str)
                # exit()
                return None, None

            ### take the address in target language
            verse_address_sum = verse_address_sum + ":" + addr_sentences

        else:
            verse_content_sum, verse_address_sum = verse_lookup(addr_str, version=version)

            if len(verse_content_sum) < 10:
                return None, None

        # print("verse_content_sum", verse_content_sum)
        # print("verse_address_sum", verse_address_sum)
    except Exception as e:
        print(e)
        verse_content_sum = None
        verse_address_sum = None
        pass
    return verse_content_sum, verse_address_sum


def get_verse_by_feeling(feeling):
    addr_str = get_verse_list(feeling)
    verse_content, addr_vi = multi_verse_lookup(addr_str)
    wraped_verse = "\"" + verse_content + "\"" + " - " + addr_vi
    return wraped_verse

# if __name__ == "__main__":
#     # app.run()
#     # addr = get_verse_list("joy")
#     verse_lookup("Proverbs 15:13")
