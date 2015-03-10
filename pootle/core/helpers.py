#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Evernote Corporation
#
# This file is part of Pootle.
#
# Pootle is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

from itertools import groupby

from django.conf import settings
from django.utils.translation import ugettext as _

from pootle_app.models.permissions import check_permission
from pootle_misc.checks import check_names, get_qualitycheck_schema
from pootle_misc.forms import make_search_form
from pootle_misc.stats import get_translation_states
from pootle_store.models import Store, Unit
from pootle_store.views import get_step_query
from virtualfolder.models import VirtualFolder

from .url_helpers import get_path_parts, get_previous_url


EXPORT_VIEW_QUERY_LIMIT = 10000


def get_filter_name(GET):
    """Gets current filter's human-readable name.

    :param GET: A copy of ``request.GET``.
    :return: Two-tuple with the filter name, and a list of extra arguments
        passed to the current filter.
    """
    filter = extra = None

    if 'filter' in GET:
        filter = GET['filter']

        if filter.startswith('user-'):
            extra = [GET.get('user', _('User missing'))]
        elif filter == 'checks' and 'checks' in GET:
            extra = map(lambda check: check_names.get(check, check),
                        GET['checks'].split(','))
    elif 'search' in GET:
        filter = 'search'

        extra = [GET['search']]
        if 'sfields' in GET:
            extra.extend(GET['sfields'].split(','))

    filter_name = {
        'all': _('All'),
        'translated': _('Translated'),
        'untranslated': _('Untranslated'),
        'fuzzy': _('Needs work'),
        'incomplete': _('Incomplete'),
        # Translators: This is the name of a filter
        'search': _('Search'),
        'checks': _('Checks'),
        'my-submissions': _('My submissions'),
        'user-submissions': _('Submissions'),
        'my-submissions-overwritten': _('My overwritten submissions'),
        'user-submissions-overwritten': _('Overwritten submissions'),
    }.get(filter)

    return (filter_name, extra)


def get_translation_context(request, is_terminology=False):
    """Returns a common context for translation views.

    :param request: a :cls:`django.http.HttpRequest` object.
    :param is_terminology: boolean indicating if the translation context
        is relevant to a terminology project.
    """
    resource_path = getattr(request, 'resource_path', '')

    return {
        'page': 'translate',

        'cantranslate': check_permission("translate", request),
        'cansuggest': check_permission("suggest", request),
        'canreview': check_permission("review", request),
        'is_admin': check_permission('administrate', request),
        'profile': request.profile,

        'pootle_path': request.pootle_path,
        'ctx_path': request.ctx_path,
        'resource_path': resource_path,
        'resource_path_parts': get_path_parts(resource_path),

        'check_categories': get_qualitycheck_schema(),

        'search_form': make_search_form(request=request,
                                        terminology=is_terminology),

        'previous_url': get_previous_url(request),

        'MT_BACKENDS': settings.MT_BACKENDS,
        'AMAGAMA_URL': settings.AMAGAMA_URL,
    }


def get_export_view_context(request):
    """Returns a common context for export views.

    :param request: a :cls:`django.http.HttpRequest` object.
    """
    res = {}
    filter_name, filter_extra = get_filter_name(request.GET)

    units_qs = Unit.objects.get_for_path(request.pootle_path,
                                         request.profile)
    units = get_step_query(request, units_qs)
    unit_total_count = units.count()

    units = units.select_related('store')
    if unit_total_count > EXPORT_VIEW_QUERY_LIMIT:
        units = units[:EXPORT_VIEW_QUERY_LIMIT]
        res.update({
            'unit_total_count': unit_total_count,
            'displayed_unit_count': EXPORT_VIEW_QUERY_LIMIT,
        })

    unit_groups = [(path, list(units)) for path, units in
                   groupby(units, lambda x: x.store.pootle_path)]

    res.update({
        'unit_groups': unit_groups,
        'filter_name': filter_name,
        'filter_extra': filter_extra,
    })

    return res


def get_overview_context(request):
    """Returns a common context for overview browser pages.

    :param request: a :cls:`django.http.HttpRequest` object.
    """
    resource_obj = request.resource_obj
    resource_path = getattr(request, 'resource_path', '')

    filters = {}

    if (not isinstance(resource_obj, Store) and
        VirtualFolder.get_matching_for(request.pootle_path).count()):
        filters['sort'] = 'priority'

    url_action_continue = resource_obj.get_translate_url(state='incomplete',
                                                         **filters)
    url_action_fixcritical = resource_obj.get_critical_url(**filters)
    url_action_review = resource_obj.get_translate_url(state='suggestions',
                                                       **filters)
    url_action_view_all = resource_obj.get_translate_url(state='all')

    return {
        'page': 'overview',

        'pootle_path': request.pootle_path,
        'resource_obj': resource_obj,
        'resource_path': resource_path,
        'resource_path_parts': get_path_parts(resource_path),

        'translation_states': get_translation_states(resource_obj),
        'check_categories': get_qualitycheck_schema(resource_obj),

        'url_action_continue': url_action_continue,
        'url_action_fixcritical': url_action_fixcritical,
        'url_action_review': url_action_review,
        'url_action_view_all': url_action_view_all,
    }
