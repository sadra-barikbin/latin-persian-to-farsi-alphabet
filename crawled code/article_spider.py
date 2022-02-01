import json

import scrapy


class WordSpider(scrapy.Spider):
    name = "word"
    doc_id = []
    start_urls = [
        'https://www.vajehyab.com/?q=%D8%AA%D8%A7%D8%AE%D8%AA%D9%86',
        'https://www.vajehyab.com/?q=%D9%85%D8%A7%D8%AF%D8%B1',
        'https://www.vajehyab.com/?q=%D8%A7%D8%B3%D8%A8',
        'https://www.vajehyab.com/?q=%D9%86%D9%88%D8%B2%D8%A7%D8%AF',
        'https://www.vajehyab.com/?q=%D9%BE%D8%A7%DA%A9%DB%8C%D8%B2%D9%87',
        'https://www.vajehyab.com/?q=%D9%85%D8%AA%D8%B1%D9%88',
    ]

    def parse(self, response):
        wordbox = response.css('section.word')[1]
        
        if len(self.doc_id) >= 100000:
            return
        self.doc_id.append(1)
        
        yield {
            'word': wordbox.css("h1::text").get(),
            'spell': wordbox.css("h3::text").get()
        }
        
        
        sect = response.css("section.aya")
        ref = sect.css('a.ajax::attr(href)').getall()
        next_len = min(2, len(ref))
        for next_word in ref[:next_len]:
            if len(self.doc_id) <= 100000:
                yield response.follow(f'https://www.vajehyab.com{next_word}',
                                      callback=self.parse)


