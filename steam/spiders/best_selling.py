import scrapy
from ..items import SteamItem
from w3lib.html import remove_tags
# from scrapy.loader import ItemLoader


class BestSellingSpider(scrapy.Spider):
    name = "best_selling"
    allowed_domains = ["store.steampowered.com"]
    start_urls = ["https://store.steampowered.com/search/?filter=topsellers"]

    def get_platforms(self, classes):
        platforms = []
        for item in classes:
            platform = item.split(' ')[-1]
            if platform == 'win':
                platforms.append('Windows')
            if platform == 'mac':
                platforms.append('Mac Os')
            if platform == 'linux':
                platforms.append('Linux')
            if platform == 'vr_supported':
                platforms.append('VR Supported')

        return platforms

    def remove_html(self, review_summary):
        cleaned_review_summary = ''
        try:
            cleaned_review_summary = remove_tags(review_summary)
        except TypeError:
            cleaned_review_summary = 'No Review'
        return cleaned_review_summary

    def get_discounted_price(self, selector_obj):
        discounted_price = 0
        try:
            discounted_price = selector_obj.xpath(
                ".//div[@class = 'discount_final_price']/text()").get()
        except ValueError:
            discounted_price = None
        return discounted_price

    def parse(self, response):
        steam_item = SteamItem()
        games = response.xpath('//div[@id = "search_resultsRows"]/a')
        for game in games:
            # loader = ItemLoader(
            #     item=SteamItem(), selector=game, response=response)
            # loader.add_xpath('game_url', ".//@href")
            # loader.add_xpath(
            #     'img_url', ".//div[@class = 'col search_capsule']/img/@src")
            # loader.add_xpath(
            #     'game_name', ".//div[@class = 'responsive_search_name_combined']/div/span/text()")
            # loader.add_xpath(
            #     'release_date', ".//div[@class = 'responsive_search_name_combined']/div[@class ='col search_released responsive_secondrow']/text()")
            # loader.add_xpath(
            #     'platforms', ".//span[contains(@class, 'platform_img') or @class = 'vr_supported']/@class")
            # loader.add_xpath(
            #     'review_summary', ".//span[contains(@class, 'search_review_summary')]/@data-tooltip-html")
            # loader.add_xpath(
            #     'discount_rate', ".//div[contains(@class, 'search_discount_block')]/div[@class = 'discount_pct']/text()")
            # loader.add_xpath('discounted_price',
            #                  ".//div[@class = 'discount_prices']")
            # loader.add_xpath(
            #     'original_price', ".//div[@class = 'discount_original_price']/text()']")

            steam_item['game_url'] = game.xpath(".//@href").get()
            steam_item['img_url'] = game.xpath(
                ".//div[@class = 'col search_capsule']/img/@src").get()
            steam_item['game_name'] = game.xpath(
                ".//div[@class = 'responsive_search_name_combined']/div/span/text()").get()
            steam_item['release_date'] = game.xpath(
                ".//div[@class = 'responsive_search_name_combined']/div[@class ='col search_released responsive_secondrow']/text()").get()
            steam_item['platforms'] = self.get_platforms(game.xpath(
                ".//span[contains(@class, 'platform_img') or @class = 'vr_supported']/@class").getall())
            steam_item['review_summary'] = self.remove_html(game.xpath(
                ".//span[contains(@class, 'search_review_summary')]/@data-tooltip-html").get())
            steam_item['discount_rate'] = game.xpath(
                ".//div[contains(@class, 'search_discount_block')]/div[@class = 'discount_pct']/text()").get()
            steam_item['discounted_price'] = self.get_discounted_price(game.xpath(
                ".//div[@class = 'discount_prices']"))
            steam_item['original_price'] = game.xpath(
                ".//div[@class = 'discount_original_price']/text()").get()

            yield steam_item

        next_page = response.xpath(
            "//a[@class = 'pagebtn' and text() = '>']/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
