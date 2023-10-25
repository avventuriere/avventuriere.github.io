import pandas as pd
import os

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
        return "".join(html_escape_table.get(c, c) for c in text)
    else:
        return "False"

# Function to parse author names and extract last names
def parse_authors(authors):
    author_list = authors.split(" and ")
    last_names = [name.split(",")[0] for name in author_list]
    return ".".join(last_names).lower()

def parse_title(title):
    title = title.split(" ")
    return ".".join(title).lower()

def parse_year(year):
    return str(year)

# Generate markdown files
for row, item in talks.iterrows():
    authors = parse_authors(item.author)
    title = parse_title(item.title)
    year = parse_year(item.year)
    
    # Construct the filename
    md_filename = f"{authors}.{year}.{title}.md"
    html_filename = f"{authors}.{year}.{title}"
    
    md = "---\ntitle: \"" + item.title + '"\n'
    md += "collection: talks" + "\n"
    
    md += 'type: "' + item.type + '"\n'    
    md += "permalink: /talks/" + html_filename + "\n"
    md += 'venue: "' + item.conference + '"\n'
    md += "date: " + str(item.dates) + ' ' + str(item.year) + "\n"
    md += 'location: "' + item.location + '"\n'
    md += "---\n"
    
    if isinstance(item.talk_url, str):
        md += "\n[More information here](" + item.talk_url + ")\n"
    
    md_filename = os.path.basename(md_filename)
    
    with open("../_talks/" + md_filename, 'w') as f:
        f.write(md)
