from django.conf import settings
from django.shortcuts import render
from django.views.generic import View
import logging
import os
import pysolr
import re
import search_util

logger = logging.getLogger('ogc_search')


# Create your views here.

class ATISearchView(View):

    def __init__(self):
        super().__init__()
        # French search fields
        self.solr_fields_fr = ("id,hashed_id,request_no_s,request_no_txt_ws,"
                               "summary_text_fr,summary_fr_s,"
                               "owner_org_fr_s,disposition_fr_s,"
                               "month_i,year_i, pages_i,umd_i,"
                               "report_type_fr_s,nil_report_b,"
                               "owner_org_title_txt_fr")
        self.solr_query_fields_fr = ['owner_org_fr_s^2', 'request_no_txt_ws', 'summary_fr_s^3', '_text_fr_^0.5']
        self.solr_facet_fields_fr = ['{!ex=tag_owner_org_fr_s}owner_org_fr_s',
                                     '{!ex=tag_month_i}month_i',
                                     '{!ex=tag_year_i}year_i',
                                     '{!ex=tag_report_type_fr_s}report_type_fr_s']
        self.solr_hl_fields_fr = ['summary_text_fr', 'request_no_txt_ws', 'owner_org_title_txt_fr']

        # English search fields
        self.solr_fields_en = ("id,hashed_id,request_no_s,request_no_txt_ws,"
                               "summary_text_en,summary_en_s,"
                               "owner_org_en_s,disposition_en_s,"
                               "month_i,year_i, pages_i,umd_i,"
                               "report_type_en_s,nil_report_b,"
                               "owner_org_title_txt_en")
        self.solr_query_fields_en = ['owner_org_en_s^2', 'request_no_txt_ws', 'summary_en_s^3', '_text_en_^0.5']
        self.solr_facet_fields_en = ['{!ex=tag_owner_org_en_s}owner_org_en_s',
                                     '{!ex=tag_month_i}month_i',
                                     '{!ex=tag_year_i}year_i',
                                     '{!ex=tag_report_type_en_s}report_type_en_s']
        self.solr_hl_fields_en = ['summary_text_en', 'request_no_txt_ws', 'owner_org_title_txt_en']

        self.phrase_xtras_fr = {
            'hl': 'on',
            'hl.simple.pre': '<mark>',
            'hl.simple.post': '</mark>',
            'hl.method': 'unified',
            'hl.snippets': 10,
            'hl.fl': self.solr_hl_fields_fr,
            'hl.preserveMulti': 'true',
            'ps': 10,
            'mm': '3<70%',
        }
        self.phrase_xtras_en = {
            'hl': 'on',
            'hl.simple.pre': '<mark>',
            'hl.simple.post': '</mark>',
            'hl.method': 'unified',
            'hl.snippets': 10,
            'hl.fl': self.solr_hl_fields_en,
            'hl.preserveMulti': 'true',
            'ps': 10,
            'mm': '3<70%',
        }

    def solr_query(self, q, startrow='0', pagesize='10', facets={}, language='en',
                   sort_order='score asc'):
        solr = pysolr.Solr(settings.SOLR_ATI)
        solr_facets = []
        if language == 'fr':
            extras = {
                'start': startrow,
                'rows': pagesize,
                'facet': 'on',
                'facet.sort': 'index',
                'facet.field': self.solr_facet_fields_fr,
                'fq': solr_facets,
                'fl': self.solr_fields_fr,
                'defType': 'edismax',
                'qf': self.solr_query_fields_fr,
                'sort': sort_order,
            }

        else:
            extras = {
                'start': startrow,
                'rows': pagesize,
                'facet': 'on',
                'facet.sort': 'index',
                'facet.field': self.solr_facet_fields_en,
                'fq': solr_facets,
                'fl': self.solr_fields_en,
                'defType': 'edismax',
                'qf': self.solr_query_fields_en,
                'sort': sort_order,
            }

        for facet in facets.keys():
            if facets[facet] != '':
                facet_terms = facets[facet].split('|')
                quoted_terms = ['"{0}"'.format(item) for item in facet_terms]
                facet_text = '{{!tag=tag_{0}}}{0}:({1})'.format(facet, ' OR '.join(quoted_terms))
                solr_facets.append(facet_text)

        if q != '*':
            if language == 'fr':
                extras.update(self.phrase_xtras_fr)
            elif language == 'en':
                extras.update(self.phrase_xtras_en)

        sr = solr.search(q, **extras)

        # If there are highlighted results, substitute the highlighted field in the doc results

        for doc in sr.docs:
            if doc['id'] in sr.highlighting:
                hl_entry = sr.highlighting[doc['id']]
                for hl_fld_id in hl_entry:
                    if hl_fld_id in doc and len(hl_entry[hl_fld_id]) > 0:
                        if type(doc[hl_fld_id]) is list:
                            # Scan Multi-valued Solr fields for matching highlight fields
                            for y in hl_entry[hl_fld_id]:
                                y_filtered = re.sub('</mark>', '', re.sub(r'<mark>', "", y))
                                x = 0
                                for hl_fld_txt in doc[hl_fld_id]:
                                    if hl_fld_txt == y_filtered:
                                        doc[hl_fld_id][x] = y
                                    x += 1
                        else:
                            # Straight-forward field replacement with highlighted text
                            doc[hl_fld_id] = hl_entry[hl_fld_id][0]
        return sr

    def get(self, request):

        context = dict(LANGUAGE_CODE=request.LANGUAGE_CODE, )
        context["cdts_version"] = settings.CDTS_VERSION
        context["od_en_url"] = settings.OPEN_DATA_EN_URL_BASE
        context["od_fr_url"] = settings.OPEN_DATA_FR_URL_BASE
        context["ati_ds_id"] = settings.ATI_DATASET_ID
        context["ati_ds_title_en"] = settings.ATI_DATASET_TITLE_EN
        context["ati_ds_title_fr"] = settings.ATI_DATASET_TITLE_FR
        context['ati_request_form_url_en'] = settings.ATI_REQUEST_URL_EN
        context['ati_request_form_url_fr'] = settings.ATI_REQUEST_URL_FR

        # Get any search terms
        solr_search_terms = search_util.get_search_terms(request)
        context['search_text'] = str(request.GET.get('search_text', ''))

        # Get "Include Nothing To Report" flag, if available
        # Retrieve search results and transform facets results to python dict

        solr_search_rtype: str = request.GET.get('ati-report-type', '')
        solr_search_orgs: str = request.GET.get('ati-search-orgs', '')
        solr_search_year: str = request.GET.get('ati-search-year', '')
        solr_search_month: str = request.GET.get('ati-search-month', '')

        context["organizations_selected"] = solr_search_orgs
        context["organizations_selected_list"] = solr_search_orgs.split('|')
        context["year_selected"] = solr_search_year
        context["year_selected_list"] = solr_search_year.split('|')
        context["month_selected"] = solr_search_month
        context["month_selected_list"] = solr_search_month.split('|')
        context["report_types_selected"] = solr_search_rtype
        context["report_types_selected_list"] = solr_search_rtype.split('|')

        # Calculate a starting row for the Solr search results. We only retrieve one page at a time

        start_row, page = search_util.calc_starting_row(request.GET.get('page', 1))

        # Retrieve search sort order

        solr_search_sort = request.GET.get('sort', 'score desc')
        if solr_search_sort not in ['score desc', 'year_i desc', 'year_i asc']:
            solr_search_sort = 'score desc'
        context['sortby'] = solr_search_sort

        if request.LANGUAGE_CODE == 'fr':
            facets_dict = dict(owner_org_fr_s=context['organizations_selected'],
                               year_i=context['year_selected'],
                               month_i=context['month_selected'],
                               report_type_fr_s=context['report_types_selected'])
        else:
            facets_dict = dict(owner_org_en_s=context['organizations_selected'],
                               year_i=context['year_selected'],
                               month_i=context['month_selected'],
                               report_type_en_s=context['report_types_selected'])

        search_results = self.solr_query(solr_search_terms, startrow=str(start_row), pagesize='10', facets=facets_dict,
                                         language=request.LANGUAGE_CODE,
                                         sort_order=solr_search_sort)

        context['results'] = search_results        # Set up previous and next page numbers

        pagination = search_util.calc_pagination_range(context['results'], 10, page)
        context['pagination'] = pagination
        context['previous_page'] = (1 if page == 1 else page - 1)
        last_page = (pagination[len(pagination) - 1] if len(pagination) > 0 else 1)
        last_page = (1 if last_page < 1 else last_page)
        context['last_page'] = last_page
        next_page = page + 1
        next_page = (last_page if next_page > last_page else next_page)
        context['next_page'] = next_page
        context['currentpage'] = page

        export_url = "/{0}/ati/export/?{1}".format(request.LANGUAGE_CODE, request.GET.urlencode())
        context['export_url'] = export_url

        if request.LANGUAGE_CODE == 'fr':
            context['org_facets_fr'] = search_util.convert_facet_list_to_dict(
                search_results.facets['facet_fields']['owner_org_fr_s'])
            context['report_type_fr'] = search_util.convert_facet_list_to_dict(
                search_results.facets['facet_fields']['report_type_fr_s'])
        else:
            context['org_facets_en'] = search_util.convert_facet_list_to_dict(
                search_results.facets['facet_fields']['owner_org_en_s'])
            context['report_type_en'] = search_util.convert_facet_list_to_dict(
                search_results.facets['facet_fields']['report_type_en_s'])
        context['month_i'] = search_util.convert_facet_list_to_dict(
            search_results.facets['facet_fields']['month_i'])
        context['year_i'] = search_util.convert_facet_list_to_dict(
            search_results.facets['facet_fields']['year_i'])

        return render(request, "ati_search.html", context)


class ATIExportView(View):
    """
    A view for downloading a simple CSV containing a subset of the fields from the Search View.
    """

    def __init__(self):
        super().__init__()

        self.solr_fields_fr = ("id,"
                               "request_no_s,"
                               "summary_fr_s,"
                               "owner_org_fr_s,"
                               "disposition_fr_s,"
                               "month_i,"
                               "year_i, "
                               "pages_i,"
                               "owner_org_title_txt_fr")
        self.solr_query_fields_fr = ['owner_org_fr_s^2', 'request_no_txt_ws', 'summary_fr_s^3', '_text_fr_^0.5']
        self.solr_fields_en = ("id,"
                               "request_no_s,"
                               "summary_en_s,"
                               "owner_org_en_s,"
                               "disposition_en_s,"
                               "month_i,"
                               "year_i,"
                               "pages_i,"
                               "owner_org_title_txt_en")
        self.solr_query_fields_en = ['owner_org_en_s^2', 'request_no_txt_ws', 'summary_en_s^3', '_text_en_^0.5']

        self.cache_dir = settings.EXPORT_FILE_CACHE_DIR
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)

    def solr_query(self, q, facets={}, language='en', sort_order='score asc'):
        solr = pysolr.Solr(settings.SOLR_ATI, search_handler='/export')
        solr_facets = []
        if language == 'fr':
            extras = {
                'fq': solr_facets,
                'fl': self.solr_fields_fr,
                'defType': 'edismax',
                'qf': self.solr_query_fields_fr,
                'sort': sort_order,
            }

        else:
            extras = {
                'fq': solr_facets,
                'fl': self.solr_fields_en,
                'defType': 'edismax',
                'qf': self.solr_query_fields_en,
                'sort': sort_order,
            }

        for facet in facets.keys():
            if facets[facet] != '':
                facet_terms = facets[facet].split(',')
                quoted_terms = ['"{0}"'.format(item) for item in facet_terms]
                facet_text = '{{!tag=tag_{0}}}{0}:({1})'.format(facet, ' OR '.join(quoted_terms))
                solr_facets.append(facet_text)

        sr = solr.search(q, **extras)
        return sr
