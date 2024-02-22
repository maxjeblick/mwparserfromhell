import re

import pywikibot

import mwparserfromhell

# code adapted from https://huggingface.co/datasets/wikipedia/blob/main/wikipedia.py
MEDIA_ALIASES = dict()
CAT_ALIASES = dict()
language = "en"

# Filters for magic words that are parser instructions -- e.g., __NOTOC__
re_rm_magic = re.compile("__[A-Z]*__", flags=re.UNICODE)

# Filters for file/image links.
media_prefixes = "|".join(["File", "Image", "Media"] + MEDIA_ALIASES.get(language, []))
re_rm_wikilink = re.compile(f"^(?:{media_prefixes}):", flags=re.IGNORECASE | re.UNICODE)


def rm_wikilink(obj):
    return bool(re_rm_wikilink.match(str(obj.title)))


# Filters for references and tables
def rm_tag(obj):
    return str(obj.tag) in {"ref", "table"}


# Leave category links in-place but remove the category prefixes
cat_prefixes = "|".join(["Category"] + CAT_ALIASES.get(language, []))
re_clean_wikilink = re.compile(f"^(?:{cat_prefixes}):", flags=re.IGNORECASE | re.UNICODE)

cat_prefixes, re_clean_wikilink


def is_category(obj):
    return bool(re_clean_wikilink.match(str(obj.title)))


def clean_wikilink(obj):
    text = obj.__strip__()
    text = re.sub(re_clean_wikilink, "", text)
    obj.text = text


def try_replace_obj(obj):
    try:
        clean_wikilink(obj)
    except ValueError:
        # For unknown reasons, objects are sometimes not found.
        pass


def try_remove_obj(obj, section):
    try:
        section.remove(obj)
    except ValueError:
        # For unknown reasons, objects are sometimes not found.
        pass


if __name__ == '__main__':

    site = pywikibot.Site('en', 'wikipedia')  # The site we want to run our bot on
    page = pywikibot.Page(site, 'Free_neutron_decay')
    wikicode = mwparserfromhell.parse(page.text)

    section_text = []
    # Filter individual sections to clean.
    for section in wikicode.get_sections(flat=True, include_lead=True, include_headings=True):
        for obj in section.ifilter_wikilinks(recursive=True):
            if rm_wikilink(obj):
                try_remove_obj(obj, section)
            elif is_category(obj):
                try_replace_obj(obj)
        for obj in section.ifilter_tags(matches=rm_tag, recursive=True):
            try_remove_obj(obj, section)

        section_no_code = section.strip_code().strip()
        section_text.append(re.sub(re_rm_magic, "", section_no_code))

    print("\n\n".join(section_text))
