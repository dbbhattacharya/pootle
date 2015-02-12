1. ElasticSearch needed
   1. Need to check if I can run amagama at the same time
   2. Just install no specific settings
2. Direct Python API for ES - code is in Pootle master
3. Loaded using a Perl script - update_tmserver.pl
4. Some settings for ES - Taras will share

Note: AMAGAMA_URL should be set to empty in settings

Relevant bugs:
https://github.com/evernote/pootle/issues/284 - Docs to setup ES
https://github.com/evernote/pootle/issues/285 - Proper config catching or at least defaults to prevent tracebacks
https://github.com/evernote/pootle/issues/244 - Support different engine values

Config
------

POOTLE_TM_SERVER = {
    'default': {
        # TODO 'ENGINE': 'pootle.core.tmserver.ElasticSearch',
        'HOST': 'localhost',
        'PORT': 9200,
        'INDEX_NAME': 'translations',
        'MIN_SCORE': 0.1,
    }
}
