import requests
from bs4 import BeautifulSoup
from ebooklib import epub


def download_page(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")


base_url = "https://97cosas.com/programador/"
soup = download_page(base_url)

book = epub.EpubBook()
book.set_identifier("id97cosas")
book.set_language("es")
book.add_author("Kevlin Henney")

body = soup.find("div", class_="span12")
title = f"{soup.title.string}"
book.set_title(title)
list = body.find("ol")
index_section = body.find("ol")
new_index = f"<ol>\n"
list_toc = list()
chapters = []
chapters.append("nav")

for i, item in enumerate(index_section.find_all("a"), start=1):
    chapters.append(
        epub.EpubHtml(title=f"{item.text}", file_name=f"chapter_{i}.xhtml", lang="es")
    )
    page = download_page(base_url + item["href"]).find("div", class_="span12")
    autor = page.find("small").text.split(":")[1].strip()
    book.add_author(autor)
    h1_tag = page.find("h1")
    if h1_tag:
        h1_tag.decompose()
    chapters[i].content = (
        f'{page.prettify()} \n<p>Volver al <a href="nav.xhtml">Indice</a></p>'
    )
    book.add_item(chapters[i])
    list_toc.append(epub.Link(f"chapter_{i}.xhtml", f"{item.text}", f"chapter_{i}"))

text_credits = f"<h1>{title}</h1>\n"
text_credits += (
    f"<p>{body.find('p').text.replace('\n', ' ').replace('  ', ' ').strip()}</p>\n"
)
text_credits += f"<p>Cada capítulo de este libro es un artículo de la web de Espartaco Palma, que ha sido recopilado para su lectura offline.\nPor: Gustavo S. Ferreyro</p>\n"
text_credits += f"<p>Este libro ha sido creado con fines educativos y de entretenimiento. No se ha modificado el contenido de los artículos, salvo para adaptarlos al formato de libro electrónico.</p>\n"
text_credits += f"<p>Si te gusta el contenido de este libro, te invito a visitar la web de Espartaco Palma: https://97cosas.com/programador/</p>\n"
text_credits += f"Si te gustaría obtener el libro original (inglés), puedes hacerlo en: https://www.oreilly.com/library/view/97-things-every/9780596809515/\n"
text_credits += f"<br>Title: 97 Things Every Programmer Should Know\n"
text_credits += f"<br>Author(s): Kevlin Henney\n"
text_credits += f"<br>Release date: February 2010\n"
text_credits += f"<br>Publisher(s): O'Reilly Media, Inc.\n"
text_credits += f"<br>ISBN: 9780596809485\n"
text_credits += f"<p>Todos los derechos reservados a sus respectivos autores</p>\n"
text_credits += f'<p>Volver al <a href="nav.xhtml">Indice</a></p>\n'

final_chapter = epub.EpubHtml(title="Creditos", file_name="credits.xhtml", lang="es")
final_chapter.content = text_credits
chapters.append(final_chapter)
book.add_item(final_chapter)
list_toc.append(epub.Link(f"credits.xhtml", f"Creditos", f"credits"))

book.toc = tuple(list_toc)
book.spine = chapters
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
epub.write_epub("97cosas.epub", book, {})
