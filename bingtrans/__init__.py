"""
Interface to Microsoft Translator API
"""
import urllib
import codecs
import json
import types

api_url = "http://api.microsofttranslator.com/V2/Ajax.svc/"
app_id = ''

def _entities_encode(str):
    return str.encode('ascii', 'xmlcharrefreplace')

def _unicode_urlencode(params):
    """
    A unicode aware version of urllib.urlencode.
    Borrowed from pyfacebook :: http://github.com/sciyoshi/pyfacebook/
    """
    if isinstance(params, dict):
        params = params.items()
    return urllib.urlencode([(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params])

def _get_array(arr):
    return '[' + ','.join(['"' + _entities_encode(x) + '"' for x in arr]) + ']'

def _run_query(method,args):
	"""
	takes arguments and optional language argument and runs query on server
	"""
	data = _unicode_urlencode(args)
	sock = urllib.urlopen(api_url + method + '?' + data)
	result = sock.read()
	if result.startswith(codecs.BOM_UTF8):
		result = result.lstrip(codecs.BOM_UTF8).decode('utf-8')
	elif result.startswith(codecs.BOM_UTF16_LE):
		result = result.lstrip(codecs.BOM_UTF16_LE).decode('utf-16-le')
	elif result.startswith(codecs.BOM_UTF16_BE):
		result = result.lstrip(codecs.BOM_UTF16_BE).decode('utf-16-be')
	return json.loads(result)

def set_app_id(new_app_id):
	global app_id
	app_id = new_app_id

def check_app_id():
    if not app_id:
        raise ValueError("AppId needs to be set by set_app_id")

def translate(text, target, source=None):
    """
    action=opensearch
    """
    check_app_id()
    query_args = {
        'appId': app_id,
        'text': text,
        'to': target
    }
    if source != None:
        query_args['from'] = source
    if isinstance(text, types.StringTypes):
        query_args['text'] = _entities_encode(text)
        return _run_query('Translate', query_args)
    elif isinstance(text, types.ListType):
        query_args['texts'] = _get_array(text)
        return _run_query('TranslateArray', query_args)
    else:
        raise ValueError("Unsupported argument type: " + str(type(text)))

def detect(text):
    check_app_id()
    query_args = {
        'appId': app_id
    }
    if isinstance(text, types.StringTypes):
        query_args['text'] = _entities_encode(text)
        return _run_query('Detect', query_args)
    elif isinstance(text, types.ListType):
        query_args['texts'] = _get_array(text)
        return _run_query('DetectArray', query_args)
    else:
        raise ValueError("Unsupported argument type: " + str(type(text)))

def translations(text, target, source, maxTranslations):
    check_app_id()
    query_args = {
        'appId': app_id,
        'from': source,
        'to': target,
        'maxTranslations': maxTranslations
    }
    if isinstance(text, types.StringTypes):
        query_args['text'] = _entities_encode(text)
        return _run_query('GetTranslations', query_args)
    elif isinstance(text, types.ListType):
        query_args['texts'] = _get_array(text)
        return _run_query('GetTranslationsArray', query_args)
    else:
        raise ValueError("Unsupported argument type: " + str(type(text)))