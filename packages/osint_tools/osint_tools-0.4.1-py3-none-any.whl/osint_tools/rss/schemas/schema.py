from .config import BaseConfig
from enum import Enum, auto
from typing import Optional
import re
from pydantic import root_validator, Field
import feedparser
from pymongo import ReplaceOne, UpdateOne
import pymongo
from pymongo.errors import InvalidOperation
from .fields import PyObjectId
import logging

logger = logging.getLogger('osint_tools')

class EnumBase(Enum):
    @classmethod
    def list_name_or_value(cls, name_or_value: str) -> list[str]:
        """list names or values of derived enum class

        Args:
            name_or_value (str): name  | value

        Returns:
            (list[str]): list of derived enum classes names or values
        """
        return [getattr(i, name_or_value) for i in cls.__members__.values()]

    @classmethod
    def list_values_to_titlecase(cls):
        def to_title_case(s):
            return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda mo: mo.group(0).capitalize(), s)
        return [to_title_case(i.value.replace('_', ' ')) for i in cls.__members__.values()]


class EnumAutoBase(EnumBase):
    def _generate_next_value_(name, start, count, last_values):
        return name

class EnumRSS(str, EnumBase):
    cbc_world = 'cbc.ca/cmlink/rss-world'
    cbc_health = 'https://rss.cbc.ca/lineup/health.xml'
    full_rss = 'https://www.zerohedge.com/fullrss2.xml'
    # zh = 'http://feeds.feedburner.com/zerohedge/feed'
    pf = 'https://www.reddit.com/r/ActualPublicFreakouts.rss'
    cnn = 'http://rss.cnn.com/rss/cnn_topstories.rss'
    # York Times Home Page
    nyt = 'http://feeds.nytimes.com/nyt/rss/HomePage'
    nyt_daily = 'https://feeds.simplecast.com/54nAGcIl'
    
    the_atlantic = 'https://www.theatlantic.com/feed/all'
    
    nbc_news = 'http://www.wthr.com/Global/category.asp?C=79076&clienttype=rss'
    # washhington Post: Today's Highlights
    wp = 'http://www.washingtonpost.com/rss/'
    # Top U.S. News
    ap = 'https://www.apnews.com/apf-usnews'
    # TODAY.com News - Top Stories
    usat = 'http://rssfeeds.usatoday.com/usatoday-NewsTopStories'
    #  Topics: News
    npr = 'http://www.npr.org/rss/rss.php?id=1001'
    #  News - Americas: World Edition
    # ps://www.bbc.co.uk/news/10628494#userss
    bbc = 'http://newsrss.bbc.co.uk/rss/newsonline_world_edition/americas/rss.xml'
    # ps://www.cbc.ca/rss/

    ctv_canada = 'http://ctvnews.ca/rss/Canada'
    ctv_politics = 'http://www.ctvnews.ca/rss/Politics'
    ctv_top = 'http://ctvnews.ca/rss/TopStories'
    ctv_bc = 'http://bc.ctvnews.ca/rss/bcnews'
    ctv_calgary = 'http://calgary.ctvnews.ca/rss/CalgaryNews'
    ctv_toronto = 'http://toronto.ctvnews.ca/rss/Latest'
    ctv_atlantic = 'http://atlantic.ctvnews.ca/rss/Atlantic'

    # https://www.thetelegraph.com/rss/
    telegraph = 'https://www.thetelegraph.com/rss/feed/News-RSS-Feed-1978.php'

    yahoo_news = 'https://news.yahoo.com/rss/'

    # https://www.dailymail.co.uk/home/article-2684527/RSS-Feeds.html
    daily_mail_latest = 'https://www.dailymail.co.uk/articles.rss'
    daily_mail_health = 'https://www.dailymail.co.uk/health/index.rss'
    daily_mail_science = 'https://www.dailymail.co.uk/sciencetech/index.rss'
    daily_mail_az = 'https://www.dailymail.co.uk/news/astrazeneca/index.rss'
    daily_mail_asia = 'https://www.dailymail.co.uk/news/asia/index.rss'
    dm_bill_gates = 'https://www.dailymail.co.uk/news/bill-gates/index.rss'
    dm_canada = 'https://www.dailymail.co.uk/news/canada/index.rss'
    dm_covid = 'https://www.dailymail.co.uk/news/coronavirus/index.rss'
    dm_depression = 'https://www.dailymail.co.uk/news/depression/index.rss'

    dm_fbi = 'https://www.dailymail.co.uk/news/fbi/index.rss'
    dm_giz_lane = 'https://www.dailymail.co.uk/news/ghislainemaxwell/index.rss'
    haaretz = 'https://www.haaretz.com/srv/haaretz-latest-headlines'
    # FOREX
    forex_live = 'https://www.forexlive.com/rss'
    # BOC: https://www.bankofcanada.ca/rss-feeds/
    boc_cryptoassets = 'https://www.bankofcanada.ca/topic/cryptoassets/feed/'
    boc_cryptocurrencies = 'https://www.bankofcanada.ca/topic/cryptocurrencies/feed/'
    boc_digitalization = 'https://www.bankofcanada.ca/topic/digitalization/feed/'
    boc_digital_currencies = 'https://www.bankofcanada.ca/topic/digital-currencies/feed/'
    boc_climate_change = 'https://www.bankofcanada.ca/topic/climate-change/feed/'
    boc_research = 'https://www.bankofcanada.ca/topic/central-bank-research/feed/'
    boc_fiscalpolicy = 'https://www.bankofcanada.ca/topic/fiscal-policy/feed/'
    boc_inflation_prices = 'https://www.bankofcanada.ca/topic/inflation-and-prices/feed/'
    boc_inflation_targets = 'https://www.bankofcanada.ca/topic/inflation-targets/feed/'
    boc_inflation_cost_benefits = 'https://www.bankofcanada.ca/topic/inflation-costs-and-benefits/feed/'
    boc_interest_rates = 'https://www.bankofcanada.ca/topic/interest-rates/feed/'



class Topic(str, EnumAutoBase):
    UN_ASSIGNED = auto()

# @strawberry.enum
class PropCategory(str, EnumAutoBase):
    COVERUP = auto()
    PROP_AGANDA = auto()
    CO_ORDINATED = auto()
    UN_CATEGORIZED = auto()


class Authors(BaseConfig):
    name: Optional[str] = None

class AuthorDetail(Authors):
    pass

class TitleDetail(BaseConfig):
    base: Optional[str] = None
    language: Optional[str] = None
    type: Optional[str] = None
    value: Optional[str] = None
    class Config:
        schema_extra = {
            'type': 'text/plain', 
            'language': None, 
            'base': 'https://cms.zerohedge.com/', 
            'value': 'Coinbase CEO: "Ordinary Russians Are Using Crypto As A Lifeline"'
        }

class Links(BaseConfig):
    rel: Optional[str] = None
    type: Optional[str] = None
    href: Optional[str] = None

    class Config:
        schema_extra = {
            'example': {
                'links': [
                    {
                        'rel': 'alternate', 
                        'type': 'text/html', 
                        'href': 'https://www.zerohedge.com/crypto/coinbase-ceo-ordinary-russians-are-using-crypto-lifeline'
                    }
                ]   
            }
        }

class MediaCredit(BaseConfig):
    content: Optional[str] = None

class MediaContent(BaseConfig):
    medium: Optional[str] = None
    url: Optional[str] = None
    height: Optional[str] = None
    width: Optional[str] = None
    type: Optional[str] = None

class Tags(BaseConfig):
    term: Optional[str] = None
    scheme: Optional[str] = None
    label: Optional[str] = None


class SummaryDetail(TitleDetail):
    '''SummaryDetail has same fields as TitleDetail'''
    pass

class RssSchema(BaseConfig):
    id: PyObjectId = Field(
        default_factory=PyObjectId, 
        alias="_id")
    unique_id: Optional[str] = Field(
        default_factory=lambda: '',
        description='Compound idx; created from other fileds')
    article_id: str = Field(
        # default_factory=lambda: '',
        description='id of article, conflicting with _id')
    authors: Optional[list[Authors]] = None
    author: Optional[str] = None
    author_detail: Optional[AuthorDetail] = None
    credit: Optional[str] = None
    media_credit: Optional[list[MediaCredit]] = None
    title: Optional[str] = None
    link: Optional[str] = None
    links: Optional[list[Links]] = None
    published: Optional[str] = None
    tags: Optional[list[Tags]] = None
    media_content: Optional[list[MediaContent]] = None
    summary_detail: Optional[SummaryDetail] = None
    flag: PropCategory = PropCategory.UN_CATEGORIZED
    topic: Topic = Topic.UN_ASSIGNED
    is_sorted: bool = False
    rss_url: str

    @root_validator(pre=True)
    def create_uid(cls, val):
        # gql wants alias _id not model name id
        val['unique_id'] = str(val['rss_url']) + '-' + str(val['link'])
        return val

class RssSchemaList(BaseConfig):
    rss_list: list[RssSchema] | list[UpdateOne] | list = []

    @staticmethod
    def _get_feed_static(url: str) -> list[RssSchema]:
        d = feedparser.parse(url)
        rss = []
        for k in d['entries']:
            post = {}
            # rename id, as it conflicts with _id
            post['article_id'] = k.pop('id', '')
            for k, v in k.items():
                post[k] = v
                post['rss_url'] = url
            rss.append(RssSchema(**post))
        return rss

    @classmethod
    def from_url(cls, url: str):
        rss_list = cls._get_feed_static(url)
        return cls(rss_list=rss_list)

    @classmethod
    def from_url_list(cls, urls: list[str], limit: int = -1):
        rss_list = []
        counter = 0
        for url in urls[:limit]:
            rss_list += cls._get_feed_static(url)
            counter += 1
            print(f'{counter} - {url}')
        return cls(rss_list=rss_list)

    @classmethod
    def to_db_v2(
        cls,
        db, 
        urls: list[str],
        collection: str, 
        filter_field: str,
        limit: int = -1,
    ):
        rss_list = []
        counter = 0
        for url in urls[:limit]:
            feed = feedparser.parse(url)
            for k in feed['entries']:
                post = {}
                # rename id, as it conflicts with _id
                post['article_id'] = k.pop('id', '')
                for k, v in k.items():
                    post[k] = v
                    post['rss_url'] = url

                scheme = RssSchema(**post)
                item = UpdateOne(
                    filter={
                        # "_id": scheme.id,
                        filter_field: getattr(scheme, filter_field)
                    }, 
                    update={
                        "$set": scheme.dict(by_alias=True, exclude={'id'})
                    }, 
                    upsert=True
                )
                rss_list.append(item)
                counter += 1
                print(f'{counter}: {url}')
        return cls(rss_list=rss_list)

    async def bulk_create_or_update(
        self, 
        db, 
        collection: str
    ) -> dict[str, str | int]:
        try:
            result = await db[collection].bulk_write(self.rss_list)
        except InvalidOperation as e:
            print(e)
            raise
        else:
            return {
                'collection': collection,
                'nModified': result.bulk_api_result['nModified'],
                'nUpserted': result.bulk_api_result['nUpserted'],
                'nInserted': result.bulk_api_result['nInserted'],
                'nMatched':  result.bulk_api_result['nMatched']
            }

    async def to_db(
        self, 
        db,
        collection: str, 
        filter_field: str,
        exclude: set[str] = {'id'}
    ):
        update = []
        for article in self.rss_list:
            update.append(
                ReplaceOne(
                    {
                        filter_field: getattr(article, filter_field)
                    }, 
                    article.dict(exclude=exclude), 
                    upsert=True
                )
            )
        try:
            result = await db[collection].bulk_write(update)
            print(f"rss nModified: {result.bulk_api_result['nModified']}")
            print(f"rss nUpserted: {result.bulk_api_result['nUpserted']}")
            print(f"rss nInserted: {result.bulk_api_result['nInserted']}")
            print(f"rss nMatched: {result.bulk_api_result['nMatched']}")
            return True
        except pymongo.errors.BulkWriteError as e:
            raise
