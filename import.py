import csv
from collections import defaultdict

csv_filename = 'your_csv_file.csv'
sql_filename = 'import_bible_data.sql'

books = set()
chapters = set()
verses = set()
versions = set()
verse_versions = []
verse_attributes = set()

with open(csv_filename, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        book = row['book']
        chapter = int(row['chapter'])
        verse_number = int(row['verse'])

        books.add(book)
        chapters.add((book, chapter))
        verses.add((book, chapter, verse_number))

        for version_code in ['asv', 'kjv', 'akjv', 'cpdv', 'dbt', 'drb', 'erv', 'jps', 'nheb', 'slt', 'wbt', 'web', 'ylt']:
            version = version_code.upper()
            verse_text = row[version_code]

            versions.add(version)
            verse_versions.append((book, chapter, verse_number, version, verse_text))

        spoken_by_jesus = row['true'] == '1'
        quote_of_the_day = row['qotd'] == '1'
        verse_attributes.add((book, chapter, verse_number, spoken_by_jesus, quote_of_the_day))

with open(sql_filename, 'w') as sqlfile:
    for book in sorted(books):
        sqlfile.write(f"INSERT INTO bible_app_book (name) VALUES ('{book}');\n")

    for version in sorted(versions):
        sqlfile.write(f"INSERT INTO bible_app_version (name) VALUES ('{version}');\n")

    for book, chapter in sorted(chapters):
        sqlfile.write(f"INSERT INTO bible_app_chapter (book_id, chapter_number) VALUES ((SELECT id FROM bible_app_book WHERE name='{book}'), {chapter});\n")

    for book, chapter, verse_number in sorted(verses):
        sqlfile.write(f"INSERT INTO bible_app_verse (chapter_id, verse_number) VALUES ((SELECT id FROM bible_app_chapter WHERE book_id=(SELECT id FROM bible_app_book WHERE name='{book}') AND chapter_number={chapter}), {verse_number});\n")

    for book, chapter, verse_number, version, verse_text in verse_versions:
        verse_text = verse_text.replace("'", "''")
        sqlfile.write(f"INSERT INTO bible_app_verseversion (verse_id, version_id, text) VALUES ((SELECT id FROM bible_app_verse WHERE chapter_id=(SELECT id FROM bible_app_chapter WHERE book_id=(SELECT id FROM bible_app_book WHERE name='{book}') AND chapter_number={chapter}) AND verse_number={verse_number}), (SELECT id FROM bible_app_version WHERE name='{version}'), '{verse_text}');\n")

    for book, chapter, verse_number, spoken_by_jesus, quote_of_the_day in verse_attributes:
        sqlfile.write(f"INSERT INTO bible_app_verseattribute (verse_id, spoken_by_jesus, quote_of_the_day) VALUES ((SELECT id FROM bible_app_verse WHERE chapter_id=(SELECT id FROM bible_app_chapter WHERE book_id=(SELECT id FROM bible_app_book WHERE name='{book}') AND chapter_number={chapter}) AND verse_number={verse_number}), {spoken_by_jesus}, {quote_of_the_day});\n")
