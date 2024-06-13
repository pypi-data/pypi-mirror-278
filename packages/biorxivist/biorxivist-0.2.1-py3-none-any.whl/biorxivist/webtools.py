import requests
from urllib.parse import quote
from bs4 import BeautifulSoup

# from langchain.document_loaders import UnstructuredHTMLLoader
# the issue with UnstructuredHTML and BSHTMLLoader is it wants a file.
# I could play with making an in memory file but I don't want to.
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema.document import Document

# An Alternative would be langchains: https://python.langchain.com/v0.1/docs/integrations/document_loaders/arxiv/
from warnings import warn


class BioRxiv:
    """A base class for interacting with Biorxiv."""

    base_url = "https://biorxiv.org"

    def __init__(self):
        self.session = requests.Session()  # a session will store cookies.

    def get_relative_link(self, link: str) -> requests.Response:
        if not isinstance(link, str):
            raise TypeError(
                f"The link must be a string completing a valid URL not {type(link)}."
            )
        return self.session.get(self.base_url + link)


class BioRxivPaper(BioRxiv):
    """Use a URI for a paper to access the full text, PDF, figures and suplement."""

    _relative_uri = ""
    _text = None
    _title = None
    _authors = None
    _pdf_link = None
    _paper_homepage = None
    _langchain_docs = None

    def __init__(self, relative_uri, title=None):
        """An object that stores the URI and title of an object and lazy loads the full text, authors and other metrics when called.

        Parameters:
        relative_uri:str -- The relative link to the resource i.e. "/content/10.1101/2023.10.19.563100v1"
        self.title:str -- Optional the title of the paper.

        Properties:
        relative_uri: The uri that instantiated this object
        uri: the full address to this papers home page
        text: the text of this paper.
        pdf_link: the relative uri for the full text pdf.
        homepage: the BeautifulSoup parsed HTML of this paper's home page
        """
        self.relative_uri = relative_uri
        self.title = title
        super().__init__()

    def __str__(self):
        # TODO make this the text or abstract instead?
        return self.text

    def __repr__(self):
        return f"[{self.title}]({self.uri})"

    def __getitem__(self, idx):
        return self.text[idx]

    # Intentionally did not implelment __setitem__ because this object is not intended to modify the source data.

    @property
    def uri(self):
        return self.base_url + self.relative_uri

    @property
    def relative_uri(self):
        return self._relative_uri

    @relative_uri.setter
    def relative_uri(self, uri):
        if not isinstance(uri, str):
            raise TypeError("the relative uri must be a string.")
        if not uri.startswith("/"):
            raise ValueError('the relative uri must start with "/".')
        self._relative_uri = uri

    @property
    def text(self):
        if not self._text:
            self._text = self.fetch_text()
        return self._text

    @property
    def homepage(self):
        if not self._paper_homepage:
            r = self.fetch_home_page()
            r.raise_for_status()
            self._paper_homepage = BeautifulSoup(r.content, "html.parser")
        return self._paper_homepage

    @property
    def pdf_link(self):
        soup = self.homepage
        link = soup.find("link", {"title": "Full Text (PDF)"})
        return link

    @property
    def full_text_html_link(self):
        return self.find_anchor({"data-panel-name": "article_tab_full_text"})

    @classmethod
    def from_anchortag(cls, tag):
        return BioRxivPaper(relative_uri=tag["href"], title=tag.text)

    @property
    def abstract(self):
        div = self.homepage.find("div", {"class": "abstract"})
        p = div.find_all("p")
        text = "\n\n".join([x.text for x in p])
        return text

    @property
    def langchain_doc(self):
        if not self._langchain_docs:
            self._langchain_docs = self._parse_to_langchain_docs()
        return self._langchain_docs

    def _parse_to_langchain_docs(self, chunk_size=1000, overlap=0):
        text_splitter = CharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=overlap
        )
        chunks = [
            Document(
                page_content=x,
                metadata={
                    "title": self.title,
                    "source": self.base_url + self.full_text_html_link,
                },
            )
            for x in text_splitter.split_text(self.text)
        ]
        return chunks

    def find_anchor(self, tag_dict):
        """Find an anchor tag based on a dictionary of tag properties"""
        soup = self.homepage
        anchor = soup.find("a", tag_dict)
        if anchor:
            return anchor["href"]
        else:
            warn(f"Unable to locate an anchor with the tags: {tag_dict}.")
            return None

    def fetch_home_page(self) -> requests.Response:
        return self.get_relative_link(self.relative_uri)

    def fetch_full_text_html(self) -> requests.Response:
        return self.get_relative_link(self.full_text_html_link)

    def parse_full_text_response(self, response: requests.Response) -> str:
        """Take the response of fetch_full_text_html and parse to string.

        This string result only contains full paragraphs and does not include headers or section titles.
        """
        soup = BeautifulSoup(response.content, "html.parser")
        full_text_div = soup.find("div", {"class", "fulltext-view"})
        text = [x.text for x in full_text_div.find_all("p")]
        return "\n\n".join(text)

    def fetch_text(self):
        response = self.fetch_full_text_html()
        text = self.parse_full_text_response(response)
        return text

    def fetch_pdf(self):
        raise NotImplementedError


class SearchResult(BioRxiv):
    _results = []
    _loaded_pages = set()
    _response = None
    _soup = None

    def __init__(self, response: requests.Response = None):
        """An object that manages the results of a BioRxiv search. Loads the initial results by default. Optionally load more.

        Parameters:
        response:requests.Response the response from a BioRxivDriver.search_biorxiv execution.

        Properties:
        response:requests.Response access to the response that instantiated this object
        soup: the BeautifulSoup object used to return all other properties
        page: the current page number of the paginated results
        results: a list of BioRxivPaper objects obtained from the response and any calls to more() or all().
        """
        self.response = response
        self.load_results()
        super().__init__()

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, response: requests.Response):
        if not isinstance(response, requests.Response):
            raise TypeError("Must be a requests.Response")
        self._response = response

    @response.deleter
    def response(self):
        del self._soup
        del self._response

    @property
    def soup(self):
        if not self._soup:
            self._soup = BeautifulSoup(self._response, parser="html.parser")
        return self._soup

    @soup.setter
    def soup(self, soup):
        if not isinstance(soup, BeautifulSoup):
            raise TypeError("soup must be a BeautifulSoup object.")
        self._soup = soup

    @property
    def page(self):
        return self._soup.find("li", "pager-current").text

    @property
    def results(self):
        return self._results

    @staticmethod
    def parse_response(response):
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        return soup

    def load_results(self):
        """Store the papers in the current self.response"""
        self.soup = SearchResult.parse_response(self.response)
        if not self.page in self._loaded_pages:
            links = self.soup.find_all("a", "highwire-cite-linked-title")
            self._loaded_pages.add(self.page)
            for link in links:
                self._results.append(BioRxivPaper.from_anchortag(link))

    def more(self):
        """Fetch the next batch of results by following the "next" anchor in the response."""
        pager_next = self.soup.find("li", "pager-next")
        next_link = pager_next.find("a", {"class": "link-icon"})["href"]
        resp = self.get_relative_link(next_link)
        self.response = resp
        self.load_results()

    def all(self):
        """Fetch all the results"""
        raise NotImplementedError


class BioRxivDriver(BioRxiv):
    """Utilize requests to obtain papers for BioRxiv"""

    def __init__(self):
        super().__init__()

    def search_biorxiv(self, query: str, num_results=75):
        search_query = query.replace(" ", "+")
        search_query = search_query + f" numresults:{str(num_results)}"
        search_query = quote(search_query, safe="")
        if not search_query.startswith("/"):
            search_query = "/" + search_query
        uri = self.base_url + "/search" + search_query
        resp = self.session.get(uri)
        return SearchResult(resp)
