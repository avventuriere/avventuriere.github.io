import os
import pandas as pd

# Load the TSV file
talks = pd.read_csv("talks.tsv", sep="\t", header=0)

# Escape special characters function
html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
}

def html_escape(text):
    if type(text) is str:
        return "".join(html_escape_table.get(c,c) for c in text)
    else:
        return "False"

def parse_authors(authors_str):
    authors_list = authors_str.split(' and ')
    last_names = [author.split(', ')[0] for author in authors_list]
    filename_authors = '.'.join(last_names).replace(' ', '').lower()
    return filename_authors

def parse_title(title):
    title = title.replace(",", "")
    title = title.split(" ")
    return ".".join(title).lower()

def parse_dates(dates):
    first_date = dates.split('--')[0].strip()
    month, day = first_date.split(' ')
    month_number = month_to_number(month)
    return f"{month_number}.{day}"

def month_to_number(month):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return str(months.index(month) + 1).zfill(2)

# Generate markdown files
for row, item in talks.iterrows():
    filename_authors = parse_authors(item.author)
    title = parse_title(item.title)
    year = str(item.year)
    dates = parse_dates(item.dates)
    permalink = f"{year}.{dates}.{filename_authors}.{title}"
    
    md_filename = f"{filename_authors}.{year}.{title}.md"
    html_filename = permalink
    
    md = "---\ntitle: \"" + item.title + '"\n'
    md += "collection: talks" + "\n"
    md += 'type: "' + item.type + '"\n'    
    md += f"permalink: /talks/{html_filename}\n"
    md += 'venue: "' + item.conference + '"\n'
    md += "date: " + item.dates + ' ' + str(item.year) + "\n"
    md += 'location: "' + item.location + '"\n'
    md += "---\n"
    
    if isinstance(item.talk_url, str):
        md += "\n[More information here](" + item.talk_url + ")\n"
    
    md_filename = os.path.basename(md_filename)
    
    with open("../_talks/" + md_filename, 'w') as f:
        f.write(md)
