import scrapy

class FlipscraperSpider(scrapy.Spider):

    name = "flipscraper"
    #Setting the allowed domains to restrict our spider from crawling into unnecessary domains
    allowed_domains = ["flipkart.com"]
    #Name of spider
    i = 0
    
    def __init__(self, search_term=None, num='all', *args, **kwargs):
        super(FlipscraperSpider, self).__init__(*args, **kwargs)
        self.search_term = search_term.replace(' ','+')
        if num!= 'all':
            self.num = int(num)
        else:
            self.num = num
        #The wepage from where the spider starts crawling
        self.start_urls = [f"https://www.flipkart.com/search?q={self.search_term}&as=on&as-show=on&otracker=AS_Query_TrendingAutoSuggest_2_0_na_na_na&otracker1=AS_Query_TrendingAutoSuggest_2_0_na_na_na&as-pos=2&as-type=TRENDING&suggestionId=shoes&requestId=8f0b3ee0-959c-4c33-872a-b620540cb6b5"] 
        

    #Method to generate a dictionary of details related to the item
    def parse_item(self, response):
        if response.status > 200:
            response = response.replace(status=201)
        link = response.url
        item = response.xpath("//div[@class='C7fEHH']")

        sale_price = float((item.xpath("//div[@class='x+7QT1 dB67CR']/div[@class='UOCQB1']/div/div[@class='Nx9bqj CxhGGd']/text()").get()).strip('₹').replace(",",''))

        total = item.xpath("//div[@class='x+7QT1 dB67CR']/div[@class='UOCQB1']/div/div[@class='yRaY8j A6+E6v']/text()").extract()
        if total is not None:
            total = float(total[-1].replace(",",''))

        rating = item.xpath("//div[@class='DRxq-P']/div/div/span[@class='Y1HWO0']/div/text()").get()
        if rating is not None:
            rating = float(rating)

        yield{
            'Company_name': item.xpath("//div/h1/span[@class='mEh187']/text()").get().replace("\xa0","").upper(),
            'Descrption': (" ".join(item.xpath("///div/h1/span[@class='VU-ZEz']/text()").extract())).replace("\xa0",''),
            'Sale Price (₹)': sale_price,
            'Total Price (₹)': total,
            'Discount': item.xpath("//div[@class='x+7QT1 dB67CR']/div[@class='UOCQB1']/div/div[@class='UkUFwK WW8yVX dB67CR']/span/text()").get(),
            'Rating': item.xpath("//div[@class='DRxq-P']/div/div/span[@class='Y1HWO0']/div/text()").get(),
            'Reviews & Ratings': item.xpath("//div[@class='DRxq-P']/div/div/span[@class='Wphh3N']/span/text()").get(),
            'url': link
        }
    
    #Method to parse the webpage and follow the links to the next page
    def parse(self, response):
        if response.status > 200:
            response = response.replace(status=201)
        
        items = response.xpath("//div[@class='_1sdMkc LFEi7Z']/a[@class='rPDeLR']/@href").extract()
        for item in items:
            if self.num != 'all':
                if self.i < int(self.num):
                    item_url = 'https://www.flipkart.com' + item
                    yield response.follow(item_url, callback=self.parse_item)
                    self.i += 1
                else:
                    return
            else:
                item_url = 'https://www.flipkart.com' + item
                yield response.follow(item_url, callback=self.parse_item)
        
        next_page = response.xpath("//div[@class='_1G0WLw']/nav[@class='WSL9JP']/a/@href").extract()[-1]
        print(next_page)
        url = 'https://www.flipkart.com' + next_page
        yield response.follow(url, callback=self.parse)

    

        
