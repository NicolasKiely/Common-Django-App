from django.core.urlresolvers import reverse
import django.shortcuts
from django.http import HttpResponse
import json

try:
    # Load settings
    import .settings as local_settings
    __user_menu = local_settings.user_menu
    __anon_menu = local_settings.anon_menu
    __site_title = local_settings.site_title
    __page_title = local_settings.page_title
    __description = local_settings.description

except ImportError:
    # Load defaults
    # Menus are lists of link url, link text pairs
    __user_menu = []
    __anon_menu = []
    __site_title = '#SITE_TITLE#'
    __page_title = '#PAGE_TITLE#'
    __description = '#DESCRIPTION#'

__GOOGLE_API = 'https://ajax.googleapis.com/ajax'
__BOOTSTRAP =  'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5'

# Resolve local vs cdn assets
if percms.safesettings.USE_LOCAL_ASSETS:
    __jquery_js = '/static/common/jquery-1.11.3.min.js'
    __bootst_js = '/static/common/bootstrap.min.js'
    __bootst_css = '/static/common/bootstrap.min.css'
else:
    __jquery_js = __GOOGLE_API + '/libs/jquery/1.11.3/jquery.min.js'
    __bootst_js = __BOOTSTRAP + '/js/bootstrap.min.js'
    __bootst_css = __BOOTSTRAP + '/css/bootstrap.min.css'

def get_core_config():
    ''' Returns copy of core page config '''
    return {
        'page': {
            'site': __site_title,
            'title': __page_title,
            'description': __description,
            'js': {
                'jquery': __jquery_js,
                'bootstrap': __bootst_js
            },
            'css': {
                'bootstrap': __bootst_css
            },
            # Drop-down menu for logged in users
            'user_menu': __user_menu, 

            # Alternative menu for non-logged in users
            'anon_menu': __anon_menu
        },

        'user': None
    }


def merge_config(source, dest):
    ''' Merges config items '''
    for dest_key, dest_val in dest.iteritems():
        if dest_key in source:
            # Merge conflict
            source_val = source[dest_key]
            if type(source_val) is list:
                # Append new data to old lists
                source[dest_key] += dest_val

            elif type(source_val) is dict:
                # Recursive conflict with child dictionary items
                merge_config(source_val, dest_val)

            else:
                # Override old data
                source[dest_key] = dest_val
        else:
            # No conflict
            source[dest_key] = dest_val


def render(request, template_path, **kwargs):
    ''' Wrapper for django render function '''
    context = get_core_config()
    merge_config(context, kwargs)

    if request.user.is_authenticated():
        context['user'] = request.user

    return django.shortcuts.render(request, template_path, context) 


def renderform(request, formcontext):
    ''' Renders generic form '''
    return render(request, 'common/singleform.html', **formcontext)
