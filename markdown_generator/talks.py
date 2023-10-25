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
def parse_authors(authors_str):
    authors_list = authors_str.split(' and ')
    last_names = [author.split(', ')[0] for author in authors_list]
    filename_authors = '.'.join(last_names).replace(' ', '').lower()
    
    formatted_authors = []
    for author in authors_list:
        last, first = author.split(', ')
        formatted_authors.append(f'{first.strip()} {last.strip()}')
    
    if len(formatted_authors) > 1:
        citation_authors = ', '.join(formatted_authors[:-1]) + ' and ' + formatted_authors[-1]
    else:
        citation_authors = formatted_authors[0]
    
    return filename_authors, citation_authors

def parse_title(title):
    title = title.split(" ")
    return ".".join(title).lower()

def parse_year(year):
    return str(year)

def create_citation(authors, year, title, paper_type, venue, location, dates):
    citation = f"{authors}. {year}. {title} ({paper_type}). {venue}. {location}. {dates}."
    return citation

# Generate markdown files
for row, item in talks.iterrows():
    filename_authors, citation_authors = parse_authors(item['author'])
    title = parse_title(item['title'])
    year = parse_year(item['year'])
    citation = create_citation(citation_authors, year, item['title'], item['type'], item['conference'], item['location'], item['dates'])
    
    # Construct the filename
    md_filename = f"{filename_authors}.{year}.{title}.md"
    html_filename = f"{filename_authors}.{year}.{title}"
    
    md = "---\ntitle: \"" + item['title'] + '"\n'
    md += "collection: talks" + "\n"
    
    md += 'type: "' + item['type'] + '"\n'    
    md += "permalink: /talks/" + html_filename + "\n"
    md += 'venue: "' + item['conference'] + '"\n'
    md += "date: " + str(item['dates']) + ' ' + str(item['year']) + "\n"
    md += 'location: "' + item['location'] + '"\n'
    md += 'citation: "' + citation + '"\n'
    md += "---\n"  # Closing the front matter section
    
    if isinstance(item['talk_url'], str):
        md += "\n[More information here](" + item['talk_url'] + ")\n"
    
    md_filename = os.path.basename(md_filename)
    
    with open("../_talks/" + md_filename, 'w') as f:
        f.write(md)
