"""
Django settings for ogc_search project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import logging.config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'changeme'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ADMIN_ENABLED = False

ALLOWED_HOSTS = []

INTERNAL_IPS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'analytical',
    'markdown_filter',
    'debug_toolbar',
    'ATI',
    'briefing_notes',
    'contracts',
    'grants',
    'national_action_plan',
    'open_data',
    'wet'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'ogc_search.middleware.QueryLoggingMiddleware',
]

MARKDOWN_FILTER_WHITELIST_TAGS = [
    'a',
    'p',
    'code',
    'h1', 'h2', 'h3', 'h4',
    'ul',
    'ol',
    'li',
    'br',
]

ROOT_URLCONF = 'ogc_search.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'static'),
            os.path.join(BASE_DIR, 'wet', 'templates'),
            os.path.join(BASE_DIR, 'ATI', 'templates'),
            os.path.join(BASE_DIR, 'briefing_notes', 'templates'),
            os.path.join(BASE_DIR, 'contracts', 'templates'),
            os.path.join(BASE_DIR, 'grants', 'templates'),
            os.path.join(BASE_DIR, 'national_action_plan', 'templates'),
            os.path.join(BASE_DIR, 'open_data', 'templates'),
            os.path.join(BASE_DIR, 'service_inventory', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ogc_search.wsgi.application'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-1234567-8'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'ogc_search': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
    'ogc_query': {
        'handlers': ['console'],
        'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
    },
})

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    ('wxt', os.path.join(BASE_DIR, "themes-dist-GCWeb")),
    ('cdts', os.path.join(BASE_DIR, "cdts", "v4_0_28")),
    ('open_data', os.path.join(BASE_DIR, "open_data", "static")),
    ('ati', os.path.join(BASE_DIR, "ATI", "static")),
    ('bn', os.path.join(BASE_DIR, "briefing_notes", "static")),
    ('ct', os.path.join(BASE_DIR, "contracts", "static")),
    ('gc', os.path.join(BASE_DIR, "grants", "static")),
    ('nap', os.path.join(BASE_DIR, "national_action_plan", "static")),
    ('si', os.path.join(BASE_DIR, "service_inventory", "static")),
]

# Search App Feature Flags

ADMIN_ENABLED = False
ATI_ENABLED = False
BN_ENABLED = False
CT_ENABLED = False
GC_ENABLED = False
NAP_ENABLED = False
SI_ENABLED = False

# CKAN YAML files from https://github.com/open-data/ckanext-canada/tree/master/ckanext/canada/tables

CKAN_YAML_FILE = os.path.join(BASE_DIR, "ckan", "presets.yaml")
BRIEF_NOTE_YAML_FILE = os.path.join(BASE_DIR, "ckan", "briefingt.yaml")
CONTRACTS_YAML_FILE = os.path.join(BASE_DIR, "ckan", "contracts.yaml")
GRANTS_YAML_FILE = os.path.join(BASE_DIR, "ckan", "grants.yaml")
NAP_YAML_FILE = os.path.join(BASE_DIR, "ckan", "nap.yaml")
SERVICES_YAML_FILE = os.path.join(BASE_DIR, "ckan", "service.yaml")
COUNTRY_JSON_FILE = os.path.join(BASE_DIR, "ckan", "country.json")
CURRENCY_JSON_FILE = os.path.join(BASE_DIR, "ckan", "currency.json")

# Open Data App Settings

OPEN_CANADA_EN_URL_BASE = "https://open.canada.ca/"
OPEN_CANADA_FR_URL_BASE = "https://ouvert.canada.ca/"
OPEN_DATA_EN_URL_BASE = "https://open.canada.ca/data/en/dataset/"
OPEN_DATA_FR_URL_BASE = "https://ouvert.canada.ca/data/fr/dataset/"
OPEN_DATA_EN_FGP_BASE = "https://open.canada.ca/data/en/fgpv_vpgf/"
OPEN_DATA_FR_FGP_BASE = "https://ouvert.canada.ca/data/fr/fgpv_vpgf/"
OPEN_DATA_DATASET_ID = "c4c5c7f1-bfa6-4ff6-b4a0-c164cb2060f7"
OPEN_DATA_DATASET_TITLE_EN = "Open Data Portal Catalogue Dataset"
OPEN_DATA_DATASET_TITLE_FR = "Catalogue du portail de données ouvertes ensemble de données"
SOLR_URL = 'http://127.0.0.1:8983/solr/core_od_search'

# Briefing Note Title App Settings

BRIEFING_NOTE_DATASET_TITLE_EN = "Briefing Notes Dataest"
BRIEFING_NOTE_DATASET_TITLE_FR = "Note de breffage"
BRIEFING_NOTE_DATASET_ID = "ee9bd7e8-90a5-45db-9287-85c8cf3589b6"
BRIEF_NOTE_INFO_EN = 'A list of briefing note titles prepared for deputy ministers and ministers'
BRIEF_NOTE_INFO_FR = "Listes des notes d'information préparées à l'intention " \
                     "des sous-ministres et ministres"
SOLR_BN = 'http://127.0.0.1:8983/solr/core_bn_search'

# ATI App Settings

ATI_DATASET_TITLE_EN = "Access To Information"
ATI_DATASET_TITLE_FR = "Accès à l'information"
ATI_DATASET_ID = "0797e893-751e-4695-8229-a5066e4fe43c"
ATI_REQUEST_URL_EN = "https://open.canada.ca/search/ati/reference/"
ATI_REQUEST_URL_FR = "https://ouvert.canada.ca/fr/search/ati/reference/"
SOLR_ATI = 'http://127.0.0.1:8983/solr/core_ati_search'

# Contracts App Settings

CONTRACT_DATASET_TITLE_EN = "Contracts Dataset"
CONTRACT_DATASET_TITLE_FR = "Jeux de données de la divulgation des contrats"
CONTRACTS_DATASET_ID = 'd8f85d91-7dec-4fd1-8055-483b77225d8b'
SOLR_CT = 'http://127.0.0.1:8983/solr/core_contract_search'
CT_DATASET_TITLE_EN = 'Proactive Disclosure - Contracts Dataset'
CT_DATASET_TITLE_FR = 'Divulgation des contrats jeu de données'
CT_DATASET_ID = "d8f85d91-7dec-4fd1-8055-483b77225d8b"

# Grants and Contributions App Settings

SOLR_GC = 'http://127.0.0.1:8983/solr/core_gc_search'
GC_DATASET_TITLE_EN = 'Grants and Contributions Dataset'
GC_DATASET_TITLE_FR = 'Subventions et contributions gouvernementales jeu de données'
GC_DATASET_ID = "432527ab-7aac-45b5-81d6-7597107a7013"
GC_ITEMS_PER_PAGE = 25
GC_INFO_FR = ''
GC_INFO_EN = ''
SOLR_CT = 'http://127.0.0.1:8983/solr/core_ct_search'

# Grants and Contributions App Settings

SOLR_GC = 'http://127.0.0.1:8983/solr/core_gc_search'
GC_DATASET_TITLE_EN = 'Grants and Contributions Dataset'
GC_DATASET_TITLE_FR = 'Subventions et contributions gouvernementales jeu de données'
GC_DATASET_ID = "432527ab-7aac-45b5-81d6-7597107a7013"
GC_ITEMS_PER_PAGE = 25
GC_INFO_EN = """Federal departments are moving their web content to
  <a href="http://www.canada.ca">Canada.ca</a>. As a part of that
  process, proactive disclosure reports will become available through
  the <a href="http://open.canada.ca">Open Government portal</a>. 
  During this transition, if a proactive disclosure report from a
  specific department is not yet available on the Open Government
  portal please refer to <a href="http://www.tbs-sct.gc.ca/hgw-cgf/finances/rgs-erdg/pd-dp/index-eng.asp">
  Proactive disclosure by department or agency</a> where a copy can be found. 
  For any questions on this issue, please contact us at
  <a href="mailto:open-ouvert@tbs-sct.gc.ca">open-ouvert@tbs-sct.gc.ca</a>
"""
GC_INFO_FR = """Les ministères fédéraux déplacent leur contenu Web vers
le site <a href="http://www.canada.ca">canada.ca</a>. Dans le cadre de
ce processus, des rapports sur la divulgation proactive seront
accessibles par l’entremise du <a href="http://ouvert.canada.ca">
Portail du gouvernement ouvert</a>. Dans le cadre de cette transition,
advenant qu’un rapport sur la divulgation proactive d’un ministère en
particulier ne soit pas encore accessible par l’entremise du Portail du
gouvernement ouvert, veuillez consulter la
<a href="http://www.tbs-sct.gc.ca/hgw-cgf/finances/rgs-erdg/pd-dp/index-fra.asp">
Divulgation proactive par ordre de ministères ou d’organismes</a>,
où vous pourrez en trouver copie. Pour toute question à ce sujet,
veuillez nous joindre à l’adresse suivante :
<a href="mailto:open-ouvert@tbs-sct.gc.ca">open-ouvert@tbs-sct.gc.ca</a>.
"""
GC_ABOUT_FR = """En juin 2016, dans le cadre du Plan d’action pour un gouvernement ouvert, le Secrétariat du Conseil du Trésor du Canada (SCT) s’est engagé à accroître la transparence et l’utilité des données sur les subventions et contributions et a par la suite lancé les <a href="https://www.tbs-sct.gc.ca/pol/doc-fra.aspx?id=32563">Lignes directrices sur la divulgation des octrois de subventions et de contributions</a>, en vigueur le 1er avril 2018.

Les règles et principes qui régissent les subventions et les contributions gouvernementales sont décrits dans <a href="http://www.tbs-sct.gc.ca/pol/doc-fra.aspx?id=13525">la Politique du Conseil du Trésor sur les paiements de transfert</a>. Les paiements de transfert sont des transferts, imputables sur un crédit, d'argent, de biens, de services ou d'actifs à des personnes ou à des organisations ou à d'autres ordres de gouvernement, sans que le gouvernement fédéral reçoive directement des biens ou des services en échange, mais qui peuvent obliger les bénéficiaires à produire un rapport ou d'autres renseignements après avoir reçu le paiement de transfert. Ces dépenses sont signalées dans les <!--<a href="http://www.tpsgc-pwgsc.gc.ca/recgen/txt/72-fra.html">-->Comptes publics du Canada<!--</a>-->. Les principaux types de paiements de transfert sont les subventions, les contributions et « autres paiements de transfert ».

Sont inclus dans cette catégorie, mais non assujettis à la divulgation proactive (1), les transferts à d'autres ordres de gouvernement, par exemple les paiements de péréquation ainsi que les paiements effectués dans le cadre du Transfert canadien en matière de santé et du Transfert canadien en matière de programmes sociaux; (2) les subventions ou les contributions réaffectées ou par ailleurs redistribuées par un bénéficiaire à des tiers; et (3) l'information qui ne serait normalement pas divulguée en vertu de <a href="http://laws-lois.justice.gc.ca/fra/lois/A-1/index.html">la Loi sur l'accès à l'information</a> de <a href="http://laws-lois.justice.gc.ca/fra/lois/P-21/index.html">la Loi sur la protection des renseignements personnels</a> ne figure pas sur le site Web.
"""
GC_ABOUT_EN = """In June 2016, as part of the Open Government Action Plan, the Treasury Board of Canada Secretariat (TBS) committed to increasing the transparency and usefulness of grants and contribution data and subsequently launched the <a href="https://www.tbs-sct.gc.ca/pol/doc-eng.aspx?id=32563">Guidelines on the Reporting of Grants and Contributions Awards</a>, effective April 1, 2018.

The rules and principles governing government grants and contributions are outlined in the Treasury Board <a href="http://www.tbs-sct.gc.ca/pol/doc-eng.aspx?id=13525">Policy on Transfer Payments</a>. Transfer payments are transfers of money, goods, services or assets made from an appropriation to individuals, organizations or other levels of government, without the federal government directly receiving goods or services in return, but which may require the recipient to provide a report or other information subsequent to receiving payment. These expenditures are reported in the <!--<a href="http://www.tpsgc-pwgsc.gc.ca/recgen/txt/72-eng.html">-->Public Accounts of Canada<!--</a>-->. The major types of transfer payments are grants, contributions and 'other transfer payments'.

Included in this category, but not to be reported under proactive disclosure of awards, are (1) transfers to other levels of government such as Equalization payments as well as Canada Health and Social Transfer payments. (2) Grants and contributions reallocated or otherwise redistributed by the recipient to third parties; and (3) information that would normally be withheld under the <a href="http://laws-lois.justice.gc.ca/eng/acts/A-1/index.html">Access to Information Act</a> and the <a href="http://laws-lois.justice.gc.ca/eng/acts/P-21/index.html">Privacy Act</a>.
"""
# These values should match the ones in Contracts.yaml file
CT_INFO_EN = GC_INFO_EN
CT_ABOUT_EN ="""<p>As part of Canada’s second Action Plan on Open Government, the Government of Canada has committed to the disclosure of contracting data via a centralized, machine-readable database available to the public. Originally announced in Budget 2004, departments are required to disclose contracts and amendments valued over and under $10,000 in a manner outlined in the <a href="http://www.tbs-sct.gc.ca/pol/doc-eng.aspx?id=14676"> <em>Guidelines on the Proactive Disclosure of Contracts</em></a>. Amendments to the <a href="https://www.canada.ca/en/treasury-board-secretariat/services/access-information-privacy/access-information-act.html"> <em>Access to Information Act</em></a> codified the aforementioned reporting requirements with the Royal assent of <a href="https://www.parl.ca/DocumentViewer/en/42-1/bill/C-58/royal-assent"> <em>Bill C-58</em></a> in June 2019.</p>
<p>Information on contracts issued/amended by or on behalf of federal institutions can be searched here using keyword, institution, quarter, and year.</p>
<p>The Treasury Board <a href="http://www.tbs-sct.gc.ca/pol/doc-eng.aspx?id=14494"> Contracting Policy</a> outlines the rules and principles governing government contracting. The objective is to procure contracting of goods and services in a manner that enhances access, competition and fairness and results in best value to Canada. For further information on federal government procurement, please visit <a href="https://buyandsell.gc.ca/">Buyandsell.gc.ca</a>.</p>
"""
CT_INFO_FR  = GC_INFO_FR
CT_ABOUT_FR = """<p>Dans le cadre du deuxième plan d’action du Canada sur le gouvernement ouvert, le gouvernement du Canada s’est engagé à communiquer les données sur les marchés au moyen d’une base de données centralisée, lisible par machine et accessible au public. Cette initiative a été annoncée à l’origine dans le budget de 2004. Depuis, les ministères sont tenus de divulguer les marchés et les modifications d’une valeur supérieure ou inférieure à 10 000 $ de la manière décrite dans les <a href="http://www.tbs-sct.gc.ca/pol/doc-fra.aspx?id=14676"> Lignes directrices sur la divulgation proactive des marchés</a>. Les modifications apportées à <a href="https://www.canada.ca/fr/secretariat-conseil-tresor/services/acces-information-protection-reseignements-personnels/loi-acces-information.html">la Loi sur l’accès à l’information</a> ont codifié les exigences susmentionnées en matière de rapports avec la sanction royale du projet de loi <a href="https://www.parl.ca/DocumentViewer/fr/42-1/projet-loi/C-58/sanction-royal">C-58</a> en juin 2019.</p>
<p>Les renseignements sur les contrats conclus ou modifiés par les institutions fédérales ou en leur nom peuvent être recherchés ici par mot clé, institution, trimestre et année.</p>
<p>La <a href="http://www.tbs-sct.gc.ca/pol/doc-fra.aspx?id=14494"> Politique sur les marchés</a> du Conseil du Trésor énonce les règles et les principes régissant les marchés publics. L’objectif est d’obtenir des marchés de biens et de services d’une manière qui améliore l’accès, la concurrence, l’équité et la valeur optimale pour le Canada. Pour de plus amples renseignements sur l’approvisionnement du gouvernement fédéral, veuillez consulter le site <a href="https://achatsetventes.gc.ca/">achatsetventes.gc.ca</a>.</p>
"""

# National Action Plan App Settings

NAP_DATASET_TITLE_EN = 'National Action Plan Dataset'
NAP_DATASET_TITLE_FR = 'Plan d’action national jeu de données'
NAP_DATASET_ID = 'd2d72709-e4bf-412d-a1bd-8c726d19393e'
SOLR_NAP = 'http://127.0.0.1:8983/solr/core_ap_search'

# Service Inventory App Settings

SI_DATASET_TITLE_EN = 'Service Inventory'
SI_DATASET_TITLE_FR = 'Répertoire des services'
SI_DATASET_ID = '3ac0d080-6149-499a-8b06-7ce5f00ec56c'
SI_DATAVIZ_PATH_EN = "/chart/si/index-en.html?"
SI_DATAVIZ_PATH_FR = "/chart/si/index-fr.html?"
SI_ITEMS_PER_PAGE = 25
SI_NOTE_INFO_EN = ''
SI_NOTE_INFO_FR = ''
SOLR_SI = 'http://127.0.0.1:8983/solr/core_sv_search'

EXPORT_FILE_CACHE_DIR = "/tmp"
EXPORT_FILE_CACHE_URL = ""

CDTS_VERSION = 'v4_0_28'

ADOBE_ANALYTICS_URL = 'changeme'
