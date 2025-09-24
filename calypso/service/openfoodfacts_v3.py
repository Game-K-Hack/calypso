from fake_useragent import UserAgent
import requests


class OpenFoodFactsV3:
    name = "Open Food Facts (API V3)"
    domain = "https://fr.openfoodfacts.org/"

    def __init__(self):
        self.domain = "https://fr.openfoodfacts.org/api/v3/"

    def get_products(self, barcode:str, 
                           product_type:str=None, 
                           cc:str=None, 
                           lc:str=None, 
                           tags_lc:str=None, 
                           fields:str=None, 
                           knowledge_panels_included:str=None, 
                           knowledge_panels_excluded:str=None) -> dict:
        """
        Get Product Data
        ----------------

        Retrieve information for a product with a specific barcode.

        The fields parameter allows to specify what fields to retrieve.

        **product_type**: Used for READ queries for one product. Expected product type of the requested product. 
            Defaults to the product type of the server the query is sent to (e.g. 'food' for Open Food Facts, 'beauty' for Open Beauty Facts, etc.). 'all' matches all product types. 
            If the product exists on a different server that matches the requested product type, the API will return a 302 redirect to the correct server. 
            Otherwise, the API will return a 404 error. It is possible that new product types will be added in the future.
            **Allowed**: all | beauty | food | petfood | product

        **cc**: 2 letter code of the country of the user. Used for localizing some fields in returned values (e.g. knowledge panels). 
            If not passed, the country may be inferred by the IP address of the request.
            **Examples**: us

        **lc**: 2 letter code of the language of the user. Used for localizing some fields in returned values (e.g. knowledge panels).
            If not passed, the language may be inferred by the Accept-Language header of the request.
            **Examples**: fr

        **tags_lc**: 2 letter language code to request names of tags in a specific language. For READ requests:
            if passed, all taxonomized tags of the response will include a lc_name property with the translation in the requested language,
            if available. Otherwise, the property value will contain the name in the original language, prefixed by the 2 language code and a colon.

        **fields**: Comma separated list of fields requested in the response. Special values:
                - `none`: returns no fields
                - `raw`: returns all fields as stored internally in the database
                - `all`: returns all fields except generated fields that need to be explicitly requested such as "knowledge_panels".
            Defaults to "all" for READ requests. The "all" value can also be combined with fields like "attribute_groups" and "knowledge_panels".
        
        **knowledge_panels_included**: When knowledge_panels are requested, you can specify which panels should be in the response.
            All the others will be excluded.
            **Examples**: health_card, environment_card
        
        **knowledge_panels_excluded**: When knowledge_panels are requested, you can specify which panels to exclude from the response.
            All the others will be included. If a panel is both excluded and included (with the knowledge_panels_excluded parameter), it will be excluded.
            **Examples**: health_card, environment_card 
        """

        params = {}
        if product_type is not None: params["product_type"] = product_type
        if cc is not None: params["cc"] = cc
        if lc is not None: params["lc"] = lc
        if tags_lc is not None: params["tags_lc"] = tags_lc
        if fields is not None: params["fields"] = fields
        if knowledge_panels_included is not None: params["knowledge_panels_included"] = knowledge_panels_included
        if knowledge_panels_excluded is not None: params["knowledge_panels_excluded"] = knowledge_panels_excluded

        return requests.get(
            self.domain + "product/" + barcode, 
            headers={
                "User-Agent": UserAgent().firefox
            },
            params=params
        ).json()
    
    def get_list_of_preference_importance_values(self) -> dict:
        """
        Get List of Preference Importance Values
        ----------------------------------------

        These parameters are used to compute the product preferences score.

        for an overview see [Explanation on Product Attributes](https://openfoodfacts.github.io/documentation/docs/Product-Opener/api/explain-product-attributes/)"
        """
        return requests.get(
            self.domain + "preferences", 
            headers={
                "User-Agent": UserAgent().firefox
            }
        ).json()

    def get_list_of_attribute_groups_and_attributes(self) -> dict:
        """
        Get List of Attribute Groups and Attributes
        -------------------------------------------

        for an overview see [Explanation on Product Attributes](https://openfoodfacts.github.io/documentation/docs/Product-Opener/api/explain-product-attributes/)"
        """
        return requests.get(
            "/".join(self.domain.split("/")[:-2]) + "/v3.4/attribute_groups", 
            headers={
                "User-Agent": UserAgent().firefox
            }
        ).json()

    def get_canonical_tags_for_a_list_of_local_tags(self, tagtype:str, local_tags_list:str, lc:str=None) -> dict:
        """
        Get canonical tags for a list of local tags
        -------------------------------------------

        **tagtype**: The type of taxonomy to canonicalize tags for (e.g., ingredients, categories).
            **Examples**: ingredients
        
        **local_tags_list**: A comma-separated list of local tags to canonicalize.
            **Examples**: sucre,eau

        **lc**: 2-letter code of the language of the user. Used for localizing some fields in returned values. If not passed, the language may be inferred by the subdomain of the request.
            **Examples**: fr
        """
        params = {
            "tagtype": tagtype, 
            "local_tags_list": local_tags_list
        }
        if lc is not None: params["lc"] = lc
        return requests.get(
            self.domain + "taxonomy_canonicalize_tags", 
            headers={
                "User-Agent": UserAgent().firefox
            },
            params=params
        ).json()
    
    def get_display_tags_in_a_specific_language_for_a_list_of_taxonomy_tags(self, tagtype:str,  canonical_tags_list:str, lc:str=None) -> dict:
        """
        Get display tags in a specific language for a list of taxonomy tags
        -------------------------------------------------------------------

        **tagtype**: The type of taxonomy to retrieve display tags for (e.g., ingredients, categories).
            **Examples**: ingredients
        
        **canonical_tags_list**: A comma-separated list of canonical taxonomy tags to retrieve display tags for.
            **Examples**: en:sugar,en:water

        **lc**: 2-letter code of the language to return display tags in.
            **Examples**: fr
        """
        params = {
            "tagtype": tagtype, 
            "canonical_tags_list": canonical_tags_list
        }
        if lc is not None: params["lc"] = lc
        return requests.get(
            self.domain + "taxonomy_display_tags", 
            headers={
                "User-Agent": UserAgent().firefox
            },
            params=params
        ).json()
    
    def get_taxonomy_suggestions(self, tagtype:str=None, 
                                       cc:str=None, 
                                       lc:str=None, 
                                       string:str=None, 
                                       categories:str=None, 
                                       shape:str=None, 
                                       limit:str=None, 
                                       get_synonyms:str=None, 
                                       term:str=None) -> dict:
        """
        Get Taxonomy Suggestions
        ------------------------

        Open Food Facts uses multilingual [taxonomies](https://wiki.openfoodfacts.org/Taxonomies_introduction) to normalize entries for categories, labels, ingredients, packaging shapes / materials / recycling instructions and many more fields.

        This API returns taxonomy entries suggestions that can be used in product edit forms, search forms etc. (for instance in autocomplete dropdowns using libraries like Tagify or select2 on the Web).

        Suggestions filtering:

        The string parameter allows to get only suggestions that contain a specific string (useful for autocomplete suggestions).

        Suggestions ordering:

        - For packaging shapes and materials, suggestions are ordered first by the number of packaging components they appear in (restricted by country, categories and shape (for materials) if they are passed as parameters).
        - for all other taxonomies, results are ordered alphabetically

        If a string is passed, an additional sort is done to put first suggestions that start with the string, followed by suggestions with a word that start with the string, and then suggestions that contain the string anywhere.
        
        **tagtype**: 
            **Examples**: additives
        
        **cc**: 2 letter code of the country of the user. Used for localizing some fields in returned values (e.g. knowledge panels). If not passed, the country may be inferred by the IP address of the request.
            **Examples**: us
        
        **lc**: 2 letter code of the language of the user. Used for localizing some fields in returned values (e.g. knowledge panels). If not passed, the language may be inferred by the Accept-Language header of the request.
            **Examples**: fr
        **string**: Optional string used to filter suggestions (useful for autocomplete). If passed, suggestions starting with the string will be returned first, followed by suggestions matching the string at the beginning of a word, and suggestions matching the string inside a word.
            **Examples**: pe
        
        **categories**: Comma separated list of categories tags (e.g. "en:fats,en:unsalted-butters" or categories names in the language indicated by the "lc" field (e.g. "graisses, beurres salés" in French)
            **Examples**: yougurts
        
        **shape**: Shape of packaging component (tag identified in the packaging_shapes taxonomy, or plain text tag name in the language indicated by the "lc" field).
            **Examples**: bottle
        
        **limit**: Maximum number of suggestions. Default is 25, max is 400.
        
        **get_synonyms**: Whether or not to include "matched_synonyms" in the response. Set to 1 to include.
        
        **term**: Alias for the "string" parameter provided for backward compatibility. "string" takes precedence.
        """
        params = {}
        if tagtype is not None: params["tagtype"] = tagtype
        if cc is not None: params["cc"] = cc
        if lc is not None: params["lc"] = lc
        if string is not None: params["string"] = string
        if categories is not None: params["categories"] = categories
        if shape is not None: params["shape"] = shape
        if limit is not None: params["limit"] = limit
        if get_synonyms is not None: params["get_synonyms"] = get_synonyms
        if term is not None: params["term"] = term

        return requests.get(
            self.domain + "taxonomy_suggestions", 
            headers={
                "User-Agent": UserAgent().firefox
            },
            params=params
        ).json()

    def get_tag_knowledge_panels(self, tagtype:str, tag_or_tagid:str, cc:str=None, lc:str=None) -> dict:
        """
        Get Tag Knowledge Panels
        ------------------------

        Return knowledge panels for a tag.

        Currently the knowledge panels returned are:

        Categories:

        - Packaging stats for a category

        **tagtype**: Type of the tag
            **Examples**: categories

        **tag_or_tagid**: Tag name (e.g. yogurts) or tag id (e.g. en:yogurts)

        **cc**: 2 letter code of the country of the user. Used for localizing some fields in returned values (e.g. knowledge panels).
            If not passed, the country may be inferred by the IP address of the request.
            **Examples**: us

        **lc**: 2 letter code of the language of the user. Used for localizing some fields in returned values (e.g. knowledge panels).
            If not passed, the language may be inferred by the Accept-Language header of the request.
            **Examples**: fr 
        """
        params = {}
        if cc is not None: params["cc"] = cc
        if lc is not None: params["lc"] = lc

        return requests.get(
            self.domain + f"tag/{tagtype}/{tag_or_tagid}", 
            headers={
                "User-Agent": UserAgent().firefox
            },
            params=params
        ).json()
