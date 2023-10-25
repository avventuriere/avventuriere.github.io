import os
import bibtexparser

# Load your .bib file
with open('papers.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

# Escape special characters
html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
}

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)

def create_citation(entry, collection_name):
    authors_raw = entry.get('author', '')
    authors_list = authors_raw.split(' and ')
    formatted_authors = []
    for author in authors_list:
        if ',' in author:
            last, first = author.split(',', 1)
            formatted_authors.append(f'{first.strip()} {last.strip()}')
        else:
            formatted_authors.append(author.strip())
    formatted_authors_str = ', '.join(formatted_authors)
    title = entry.get('title', '')
    year = entry.get('year', '')
    
    if collection_name == 'publications':
        venue = entry.get('journal', '') + ', ' + entry.get('volume', '') + ', ' + entry.get('pages', '') + '.'
    elif collection_name == 'manuscripts':
        venue = entry.get('note', '') + ". " + entry.get('location', '')
    elif collection_name == 'dissertation':
        venue = f'Doctoral Dissertation. {entry.get("school", "")}. {entry.get("address", "")}'
    
    return f"{formatted_authors_str}. {year}. {title}. {venue}."

# Function to create markdown files
def create_markdown(entry, collection_name):
    pub_date = entry.get('year', '') + '-01-01'
    url_slug = entry.get('ID', '').replace(":", "-").replace("/", "-").lower()
    title = entry.get('title', '')
    paper_url = entry.get('url', '')
    citation = create_citation(entry, collection_name)
    
    md_filename = url_slug + ".md"
    html_filename = url_slug
    pdf_filename = url_slug + ".pdf"
    
    pdf_path = f"../files/{pdf_filename}"
    pdf_exists = os.path.exists(pdf_path)
    
    md = (
        f"---\n"
        f"title: \"{title}\"\n"
        f"collection: {collection_name}\n"
    )
    
    if pdf_exists:
        md += (
            f"permalink: /{collection_name}/{html_filename}\n"
            f"pdf_filename: {pdf_filename}\n"
        )

    if paper_url:
        md += f"outside_url: {paper_url})\n"
    
    md += (
        f"date: {pub_date}\n"
        f"venue: '{html_escape(entry.get('journal', ''))}'\n"
        f"citation: '{html_escape(citation)}'\n"
        "---\n"
    )
    
    if len(entry.get('abstract', '')) > 5:
        md += f"\n{html_escape(entry.get('abstract', ''))}\n"
    
    
    md += f"\nRecommended citation: {citation}"

    os.makedirs(f"../_{collection_name}/", exist_ok=True)
    with open(f"../_{collection_name}/" + md_filename, 'w') as f:
        f.write(md)

# Creating the markdown files
for entry in bib_database.entries:
    entry_type = entry['ENTRYTYPE']
    if entry_type == 'article':
        create_markdown(entry, 'publications')
    elif entry_type == 'unpublished':
        create_markdown(entry, 'manuscripts')
    elif entry_type == 'phdthesis':
        create_markdown(entry, 'dissertation')
