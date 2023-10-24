# Import necessary libraries
import bibtexparser
import os

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

# Function to create markdown files
def create_markdown(entry, collection_name):
    pub_date = entry.get('year', '') + '-01-01'  # Assumes January 1 if no date is provided
    url_slug = entry.get('ID', '').replace(":", "-").replace("/", "-").lower()  # Creating slug from BibTeX ID
    title = entry.get('title', '')
    
    if collection_name == 'publications':
        venue = entry.get('journal', '')
    elif collection_name == 'manuscripts':
        venue = 'Unpublished Manuscript'
    elif collection_name == 'dissertation':
        venue = 'Doctoral Dissertation, ' + entry.get('school', '')
    else:
        venue = 'N/A'  # Or some other default value
    
    paper_url = entry.get('url', '')
    
    if collection_name == 'publications':
        citation = entry.get('author', '') + '. (' + entry.get('year', '') + '). ' + title + '. ' + venue + '.'
    elif collection_name == 'manuscripts':
        citation = entry.get('author', '') + '. (' + entry.get('year', '') + '). ' + title + '. Unpublished manuscript.'
    elif collection_name == 'dissertation':
        citation = entry.get('author', '') + '. (' + entry.get('year', '') + '). ' + title + '. Doctoral dissertation, ' + entry.get('school', '') + '.'
    else:
        citation = entry.get('author', '') + '. (' + entry.get('year', '') + '). ' + title + '.'
    
    md_filename = url_slug + ".md"
    html_filename = url_slug
    pdf_filename = url_slug + ".pdf"  # Generating PDF filename from url_slug

    # YAML variables
    md = "---\ntitle: \"" + title + '"\n'
    md += f"""collection: {collection_name}"""
    md += """\npermalink: /""" + collection_name + "/" + html_filename
    md += f"\npdf_filename: {pdf_filename}"  # Adding pdf_filename to YAML

    # Assuming abstract is in the 'abstract' field of BibTeX
    excerpt = entry.get('abstract', '')
    if len(excerpt) > 5:
        md += "\nexcerpt: '" + html_escape(excerpt) + "'"

    md += "\ndate: " + pub_date
    md += "\nvenue: '" + html_escape(venue) + "'"

    if len(paper_url) > 5:
        md += "\npaperurl: '" + paper_url + "'"

    md += "\ncitation: '" + html_escape(citation) + "'"
    md += "\n---"

    # Markdown description for individual page
    if len(excerpt) > 5:
        md += "\n" + html_escape(excerpt) + "\n"

    md += "\nRecommended citation: " + citation

    md_filename = os.path.basename(md_filename)
    
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
