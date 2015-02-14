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

Notes:
- Simply start ES
- To create an Index do:
  curl -XPUT 'http://localhost:9200/translations/'
- Then run the importer script

Issues:
- The script is not DB abstracted
  - We should use Django info for this, to allow local tm population from the database
- Amagama results are not merged with the TM results
- The TM code could be abstracted better to allow Amagama to fit in there
- Needs good defaults if config data is missing
- Needs docs for setup
- We need to use the bulk commands, I suspect any large import of any kind
  would create problems see https://elasticsearch-py.readthedocs.org/en/master/helpers.html#elasticsearch.helpers.bulk

Ideas:
- We could import anything into ES
  - Would help to expand the tool to allow any PO files to be imported to the
    search like we would with amaGama
- We have more useful data such as email md5 for gravatars
- WEIGHTING - if you have more that one TM e.g. local and extra what weightings
  do you give?
- MAX_RESULTS - what is the max that we want to display?
- Is the TM results line its own templates that can be easily styled with TM
  info e.g. percentage match
- How can you go and fix an issue? - Would be nice to allow translators to mark
  and item for fixing or fix inline and return. At unit, see issue, click fix,
  got to that faulty unit, click submit or next, then return to original unit.
- Script easy import of e.g. Windows localisations
