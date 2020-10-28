'''This contains the ArtSpider and ArtSpiderItem classes. ArtSpider will scrape artworks from the
National Gallery of Art website, saving them as distinct ArtSpiderItmems.
'''

import scrapy

class ArtSpider(scrapy.Spider):
    name = 'art_spider'    
    custom_settings = { 'DOWNLOAD_DELAY': 1,
                        'ITEM_PIPELINES': {'scrapy.pipelines.images.ImagesPipeline':1,
                                           'custom_pipeline.CsvPipeline':300},
                        'IMAGES_STORE':'/home/pi/Documents/Programs/art_finder_env/all_artworks/freshly_scraped',
                        }
    
    # Adds new photos to full, keeps old, for each page 
    # Replaces old info from ArtInfo.csv with new, for each page

    # To run from command line at a certain page,
    #  scrapy crawl art_spider -a page=5
    def start_requests(self):
        yield scrapy.Request('https://images.nga.gov/en/search/do_advanced_search.html?form_name' \
                             '=default&all_words=&exact_phrase=&exclude_words=&artist_last_name' \
                             '=&keywords_in_title=&accession_number=&school=&Classification=&medium' \
                             '=&year=&year2=&open_access=Open%20Access%20Available&q=&mime_type' \
                             '=&qw=%22Open+Access+Available%22&page={}&grid_layout=1'.format(self.page),
                             meta={'this_page':self.page})
    def parse(self, response):
        all_ids = []
        for artwork in response.css('div.pictureBox'):
            all_ids.append(artwork.css('div.pictureBox_img ::attr(assetid)').extract_first())

        url1 = 'https://images.nga.gov/?service=asset&action=show_zoom_window_popup&language=en&asset='
        url2 = '&location=grid&asset_list='
        for one_id in all_ids:
            url2 = url2 + one_id + ','
        url2 = url2[0:-1] + '&basket_item_id=undefined'
        
        this_page = response.meta['this_page']
               
        for one_id in all_ids:
            # For each artwork, go to its own page
            this_viewing_link = url1 + one_id + url2
            go_to_url = response.urljoin(this_viewing_link)
            yield scrapy.Request(go_to_url, self.parse_artwork,
                                 meta={'this_id':one_id, 'this_viewing_link':this_viewing_link,
                                       'this_page':this_page})


    def parse_artwork(self, response):
        for fields in response.css('dl.info'):
            labels = []
            field = []
            for label in fields.css('dt::text').extract():
                labels.append(label)
            for f in fields.css('dd::text').extract():
                field.append(f)

            if 'Artist' in labels:
                this_artist = field[labels.index('Artist')]
            else:
                this_artist = None
            if 'Title' in labels:
                this_title = field[labels.index('Title')]
            else:
                this_title = None
            if 'Artist Info' in labels:
                this_info = field[labels.index('Artist Info')]
            else:
                this_info = None

        this_id = response.meta['this_id']
        image = 'https://images.nga.gov/?service=asset&action=download_comp_image&asset=%s&size=2'%this_id
        this_viewing_link = response.meta['this_viewing_link']
        this_page = response.meta['this_page']
        
        yield ArtspiderItem(artist=this_artist,title=this_title,artist_info=this_info,
                      id_num=this_id,image_urls=[image], viewing_link = this_viewing_link,
                            page_num=this_page)
       
class ArtspiderItem(scrapy.Item):
    artist = scrapy.Field()
    title = scrapy.Field()
    artist_info = scrapy.Field()
    viewing_link = scrapy.Field()

    id_num = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    page_num = scrapy.Field()
