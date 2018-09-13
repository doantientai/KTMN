import urllib.request
from bs4 import BeautifulSoup
from random import randint
import re

def get_verse_list(feeling):
    # url = "https://www.openbible.info/topics/" + feeling
    url = "https://www.openbible.info/topics/" + feeling
    html_content = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(html_content, "html.parser")
    list_addr = soup.find_all("a", {"class": "bibleref"})

    print("found ", len(list_addr), "addresses")

    addr_chosen = randint(0, len(list_addr))

    print("addr_chosen:", addr_chosen)

    addr_str = list_addr[addr_chosen].string

    # print(addr_str)
    return addr_str


def post_process_verse(verse_content):
    # if verse_content[0] == " ":
    #     verse_content = verse_content[1:]
    # re.sub(" +", " ", verse_content)
    return verse_content


def verse_lookup(addr_str, version="VIET"):
    ### TODO: different mode for first sentence of the chapter: chapternum
    ### check if this is the first sentence of a chapter
    addr_sentence = addr_str[addr_str.index(":") + 1:]
    # marker = "versenum"
    # if int(addr_sentence) == 1:
    #     marker = "chapternum"

    url = "https://www.biblegateway.com/passage/?search=" + str(addr_str) + "&version=" + version
    print("url:", url)
    html_content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html_content, "html.parser")

    verse_content = ""
    # if version == "VIET":
    #     if int(addr_sentence) == 1:
    #         verse_content = soup.find("span", {"class": "chapternum"}).next_sibling
    #     else:
    #         verse_content = soup.find("sup", {"class": "versenum"}).next_sibling
    # elif version == "NIV":

    # paragraph_type = None
    if soup.find("div", {"class": "poetry"}):
        paragraph_type = "poetry"
    elif soup.find("p", {"class": "chapter-1"}):
        paragraph_type = "chapter"
    else:
        paragraph_type = "normal"

    start_content = 1
    if int(addr_sentence) == 1:
        start_content = 0

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


def get_verse_by_feeling(feeling):
    addr_str = get_verse_list(feeling)
    verse_content, addr_vi = verse_lookup(addr_str)
    wraped_verse = "\"" + verse_content + "\"" + " - " + addr_vi
    return wraped_verse

# if __name__ == "__main__":
#     # app.run()
#     # addr = get_verse_list("joy")
#     verse_lookup("Proverbs 15:13")
