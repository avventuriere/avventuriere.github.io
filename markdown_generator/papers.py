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

# Creating the markdown files
for entry in bib_database.entries:
    entry_type = entry['ENTRYTYPE']
    
    if entry_type not in ['article', 'unpublished']:
        continue  # Skip entries that are not journal articles or manuscripts

    pub_date = entry.get('year', '') + '-01-01'  # Assumes January 1 if no date is provided
    url_slug = entry.get('ID', '').replace(":", "-").replace("/", "-").lower()  # Creating slug from BibTeX ID
    title = entry.get('title', '')
    venue = entry.get('journal', '') if entry_type == 'article' else 'Manuscript'
    paper_url = entry.get('url', '')
    citation = entry.get('author', '') + '. ' + entry.get('year', '') + '. ' + title + '. ' + venue + '.'

    md_filename = url_slug + ".md"
    html_filename = url_slug
    year = pub_date[:4]

    # YAML variables
    md = "---\ntitle: \"" + title + '"\n'
    md += """collection: papers"""
    md += """\npermalink: /paper/""" + html_filename

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
    if len(paper_url) > 5:
        md += "\n\n<a href='" + paper_url + "'>Download paper here</a>\n"

    if len(excerpt) > 5:
        md += "\n" + html_escape(excerpt) + "\n"

    md += "\nRecommended citation: " + citation

    md_filename = os.path.basename(md_filename)

    with open("../_papers/" + md_filename, 'w') as f:
        f.write(md)
