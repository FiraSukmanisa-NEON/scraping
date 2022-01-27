import re
from bs4 import BeautifulSoup
import requests

def get_all_article():
    base_url = "https://id.berita.yahoo.com"
    second_url = "/indonesia"
    all_links = []
    url = base_url + second_url
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        article = soup.select('li.js-stream-content')
        
        for i in (range(len(article))):
            link = article[i].select_one('a').attrs['href']
            if base_url not in link:
                link = base_url+link
            all_links.append(
                {
                    "link": link,
                    "title": article[i].select_one('a').text.strip(),
                }
            )
        return all_links
    else:
        return "Not Found"

def get_article_content():
    article_contents = get_all_article()
    data = []
    len_news = len(article_contents)

    for j in range(len_news):
        article_response = requests.get(article_contents[j]['link'])
        article_content = article_response.content
        
        article_soup = BeautifulSoup(article_content, 'html.parser')
        content = article_soup.select('article')
    
        news_provider = content[0].select_one('span.caas-attr-provider').text.strip()
        author = content[0].select_one('span.caas-author-byline-collapse').text.strip()
        date_published = content[0].select_one('time').attrs['datetime']
        image_url = content[0].select_one('div.caas-img-container img')['data-src']
        try:
            isi = ""
            list_paragraph = []
            full_paragraph = content[0].find_all('p')
            baca_juga = content[0].select('span.baca-juga')#Clean baca juga yang bold
            for b in baca_juga:
                b.extract()
            for p in range(0, len(full_paragraph)):
                paragraph = full_paragraph[p].get_text()
                line = paragraph.replace("Selengkapnya baca di sini.","") #Clean link 
                lines = line.replace("Selengkapnya…","") #Clean link
                liness = lines.replace("Baca artikel selengkapnya di sini","") #Clean link
                linesss = liness.replace("Selengkapnya...","") #Clean link
                list_paragraph.append(linesss)
                isi = " ".join(list_paragraph)

        except:
            # return "Error"
            pass
        
        data.append(
            {
                "link": article_contents[j]['link'],
                "title": article_contents[j]['title'],
                "news_provider": news_provider,
                "author": author,
                "date_published": date_published,
                "image_url": image_url,
                "text": isi
            }
        )

    return data