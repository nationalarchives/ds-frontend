from flask import current_app, make_response
from pydash import objects

from app.error_pages.routes import api_error, page_not_found_error

from .pages.articles.article_index_page import article_index_page
from .pages.articles.article_page import article_page
from .pages.articles.article_page_focused import article_page_focused
from .pages.articles.record_article_page import record_article_page
from .pages.blog.blog_feeds_page import blog_feeds_page
from .pages.blog.blog_index_page import blog_index_page
from .pages.blog.blog_page import blog_page
from .pages.blog.blog_post_page import blog_post_page
from .pages.collections.categories_page import categories_page
from .pages.collections.category_index_page import category_index_page
from .pages.collections.explorer_index_page import explorer_index_page
from .pages.collections.highlight_gallery_page import highlight_gallery_page
from .pages.cookies.cookie_details_page import cookie_details_page
from .pages.cookies.cookies_page import cookies_page
from .pages.education.education_page import education_page
from .pages.education.education_session_page import (
    education_session_page,
)
from .pages.education.education_sessions_listing_page import (
    education_sessions_listing_page,
)
from .pages.education.education_teaching_resource_page import (
    education_teaching_resource_page,
)
from .pages.education.education_teaching_resources_listing_page import (
    education_teaching_resources_listing_page,
)
from .pages.foi.foi_index_page import foi_index_page
from .pages.foi.foi_request_page import foi_request_page
from .pages.generic_pages.general_page import general_page
from .pages.generic_pages.hub_page import hub_page
from .pages.home.home_page import home_page
from .pages.people.people_index_page import people_index_page
from .pages.people.person_page import person_page
from .pages.whatson.display_page import display_page
from .pages.whatson.event_page import event_page
from .pages.whatson.events_listing_page import events_listing_page
from .pages.whatson.exhibition_page import exhibition_page
from .pages.whatson.exhibitions_listing_page import exhibitions_listing_page
from .pages.whatson.whats_on_category_page import whats_on_category_page
from .pages.whatson.whats_on_date_listing_page import whats_on_date_listing_page
from .pages.whatson.whats_on_index_page import whats_on_index_page
from .pages.whatson.whats_on_location_listing_page import whats_on_location_listing_page
from .pages.whatson.whats_on_series_page import whats_on_series_page

page_type_templates = {
    # General
    "home.HomePage": home_page,
    "generic_pages.GeneralPage": general_page,
    "generic_pages.HubPage": hub_page,
    # Cookies
    "cookies.CookiesPage": cookies_page,
    "cookies.CookieDetailsPage": cookie_details_page,
    # Explore the collection
    "collections.ExplorerIndexPage": explorer_index_page,
    "collections.HighlightGalleryPage": highlight_gallery_page,
    "collections.TimePeriodExplorerIndexPage": category_index_page,
    "collections.TimePeriodExplorerPage": categories_page,
    "collections.TopicExplorerIndexPage": category_index_page,
    "collections.TopicExplorerPage": categories_page,
    # Articles
    "articles.ArticleIndexPage": article_index_page,
    "articles.ArticlePage": article_page,
    "articles.FocusedArticlePage": article_page_focused,
    "articles.RecordArticlePage": record_article_page,
    # People
    "people.PeopleIndexPage": people_index_page,
    "people.PersonPage": person_page,
    # Blog
    "blog.BlogIndexPage": blog_index_page,
    "blog.BlogPage": blog_page,
    "blog.BlogPostPage": blog_post_page,
    "blog.BlogFeedsPage": blog_feeds_page,
    # What's on
    "whatson.WhatsOnPage": whats_on_index_page,
    "whatson.EventsListingPage": events_listing_page,
    "whatson.EventPage": event_page,
    "whatson.ExhibitionPage": exhibition_page,
    "whatson.DisplayPage": display_page,
    "whatson.ExhibitionsListingPage": exhibitions_listing_page,
    "whatson.WhatsOnCategoryPage": whats_on_category_page,
    "whatson.WhatsOnSeriesPage": whats_on_series_page,
    "whatson.WhatsOnDateListingPage": whats_on_date_listing_page,
    "whatson.WhatsOnLocationListingPage": whats_on_location_listing_page,
    # FOI
    "foi.FoiIndexPage": foi_index_page,
    "foi.FoiRequestPage": foi_request_page,
    # Education
    "education.EducationPage": education_page,
    "education.TeachingResourcesListingPage": education_teaching_resources_listing_page,
    "education.EducationSessionsListingPage": education_sessions_listing_page,
    "education.TeachingResourcePage": education_teaching_resource_page,
    "education.EducationSessionPage": education_session_page,
}


# TODO: Change this to use a decorator on the cookies_page function when the next version of TNA Python Utilities is released
page_types_to_vary_by_cookies = {"cookies.CookiesPage"}


def render_content_page(page_data):
    page_type = objects.get(page_data, "meta.type")
    if page_type:
        if page_type in page_type_templates:
            response = make_response(page_type_templates[page_type](page_data))
            if page_type in page_types_to_vary_by_cookies:
                response.headers["Vary"] = "Cookie"
            return response
        current_app.logger.error(f"Template for {page_type} not handled")
        return page_not_found_error()
    current_app.logger.error("Page meta information not included")
    return api_error()
