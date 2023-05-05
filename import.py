import csv
from collections import defaultdict

csv_filename = 'BibleDB.csv'
sql_filename = 'bible_data.sql'


version_names = {
    'asv': 'American Standard Version',
    'kjv': 'King James Bible: Pure Cambridge Edition',
    'akjv': 'American King James Version',
    'cpdv': 'Catholic Public Domain Version',
    'dbt': 'Darby Bible Translation',
    'drb': 'Douay-Rheims Bible',
    'erv': 'English Revised Version',
    'jpswey': 'JPS Tanakh 1917 OT / Weymouth NT',
    'nheb': 'New Heart English Bible',
    'slt': "Smith's Literal Translation",
    'wbt': 'Webster Bible Translation',
    'web': 'World English Bible',
    'ylt': "Young's Literal Translation",
}

books = set()
chapters = set()
verses = set()
versions = set()
verse_versions = []
verse_attributes = set()

with open(csv_filename, 'r', encoding='utf8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        book = row['Book'].lower()
        chapter = int(row['Chapter'])
        verse_number = int(row['Verse'])
        spoken_by_jesus = row['\ufeffTRUE'] == 'X'
        quote_of_the_day = row['QOTD'] if row['QOTD'] is not None and row['QOTD'] != "" else 'NULL'
        

        books.add(book)
        chapters.add((book, chapter))
        verses.add((book, chapter, verse_number, spoken_by_jesus, quote_of_the_day))

        for version_code in ['asv', 'kjv', 'akjv', 'cpdv', 'dbt', 'drb', 'erv', 'jpswey', 'nheb', 'slt', 'wbt', 'web', 'ylt']:
            version = version_code.upper()
            verse_text = row[version]

            versions.add((version_names[version_code], version_code))
            verse_versions.append((book, chapter, verse_number, version_code, verse_text))


with open(sql_filename, 'w') as sqlfile:
    for book in sorted(books):
    # for book in books:
        sqlfile.write(f"INSERT INTO JesusSaidAPI_book (name) VALUES ('{book}');\n")

    for version, slug in sorted(versions):
        version = version.replace("'", "''").replace('"', '""')
        sqlfile.write(f"INSERT INTO JesusSaidAPI_version (name, slug) VALUES ('{version}', '{slug}');\n")

    for book, chapter in sorted(chapters):
        sqlfile.write(f"INSERT INTO JesusSaidAPI_chapter (book_id, chapter) VALUES ((SELECT id FROM JesusSaidAPI_book WHERE name='{book}'), {chapter});\n")

    for book, chapter, verse_number, spoken_by_jesus, quote_of_the_day in sorted(verses):
        sqlfile.write(f"INSERT INTO JesusSaidAPI_verse (chapter_id, verse, by_jesus, qotd) VALUES ((SELECT id FROM JesusSaidAPI_chapter WHERE book_id=(SELECT id FROM JesusSaidAPI_book WHERE name='{book}') AND chapter={chapter}), {verse_number}, {spoken_by_jesus}, {quote_of_the_day});\n")

    for book, chapter, verse_number, version, verse_text in verse_versions:
        verse_text = verse_text.replace("'", "''").replace('"', '""')
        sqlfile.write(f"INSERT INTO JesusSaidAPI_verseversion (verse_id, version_id, text) VALUES ((SELECT id FROM JesusSaidAPI_verse WHERE chapter_id=(SELECT id FROM JesusSaidAPI_chapter WHERE book_id=(SELECT id FROM JesusSaidAPI_book WHERE name='{book}') AND chapter={chapter}) AND verse={verse_number}), (SELECT id FROM JesusSaidAPI_version WHERE slug='{version}'), '{verse_text}');\n")
