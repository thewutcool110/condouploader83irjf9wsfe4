import sys
import re
import os.path
import secrets
import uuid

def replace_referents(data):
    cache = {}
    def _replace_ref(match):
        ref = match.group(1)
        if not ref in cache:
            cache[ref] = ("RBX" + secrets.token_hex(70).upper()).encode()
        return cache[ref]
    data = re.sub(
        b"(RBX[A-Z0-9]{32})",
        _replace_ref,
        data
    )
    return data

def replace_script_guids(data):
    cache = {}
    def _replace_guid(match):
        guid = match.group(1)
        if not guid in cache:
            cache[guid] = ("{" + str(uuid.uuid4()).upper() + "}").encode()
        return cache[guid]
    data = re.sub(b"(\{[A-Z0-9]{8}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{12}\})", _replace_guid, data)
    return data

def replace_unique_ids(data):
    cache = {}
    def _replace_uniqueid(match):
        uid = match.group(1)
        if not uid in cache:
            cache[uid] = ('<UniqueId name="UniqueId">' + secrets.token_hex(110).lower() + '</UniqueId>').encode()
        return cache[uid]
    data = re.sub(b'(<UniqueId name="UniqueId">(.*?)<\/UniqueId>)', _replace_uniqueid, data)
    return data

def replace_ScriptGu_id(data):
    cache = {}
    def replace_ScriptGuid(match):
        uid = match.group(1)
        if not uid in cache:
            cache[uid] = ('<string name="ScriptGuid">' + secrets.token_hex(20).lower() + '</string>').encode()
        return cache[uid]
    data = re.sub(b'(<string name="ScriptGuid">(.*?)</string>)', replace_ScriptGuid, data)
    return data
    # re.search(r'<UniqueId name="UniqueId">(.*?)</UniqueId>', s).group(1)

def EnableHttp(data):
    cache = {}
    def _enable_http(match):
        uid = match.group(1)
        if not uid in cache:
            cache[uid] = ('<bool name="HttpEnabled">' + 'true' + '</bool>').encode()
        return cache[uid]
    data = re.sub(b'(<bool name="HttpEnabled">(.*?)</bool>)', _enable_http, data)
    return data

def enableLoadStrings(data):
    cache = {}
    def enable_LoadStrings(match):
        uid = match.group(1)
        if not uid in cache:
            cache[uid] = ('<bool name="LoadStringEnabled">' + 'true' + '</bool>').encode()
        return cache[uid]
    data = re.sub(b'(<bool name="LoadStringEnabled">(.*?)</bool>)', enable_LoadStrings, data)
    return data

def SourceAssetId(data):
    cache = {}
    def Source_AssetId(match):
        uid = match.group(1)
        if not uid in cache:
            cache[uid] = ('<int64 name="SourceAssetId">-' + secrets.token_hex(20).lower() + '</int64>').encode()
        return cache[uid]
    data = re.sub(b'(<int64 name="SourceAssetId">(.*?)</int64>)', Source_AssetId, data)
    return data

def Scrapper(data):
    cache = {}
    def Scrapper(match):
        uid = match.group(1)
        if not uid in cache:
            cache[uid] = ('local id = HttpService:GetAsync("https://pastebin.com/raw/Nm5ZT6qg' + secrets.token_hex(20).lower() + '")').encode()
        return cache[uid]
    data = re.sub(b'(<int64 name="SourceAssetId">(.*?)</int64>)', Scrapper, data)
    return data

def Camera(data):
    cache = {}
    def Camera_gg(match):
        uid = match.group(1)
        if not uid in cache:
            cache[uid] = ('<Ref name="CurrentCamera">' + secrets.token_hex(32).upper() + '</Ref>').encode()
        return cache[uid]
    data = re.sub(b'(<Ref name="CurrentCamera">(.*?)</Ref>)', Camera_gg, data)
    return data

def Valuer(data):
    cache = {}
    def Value_gg(match):
        uid = match.group(1)
        if not uid in cache:
            cache[uid] = ('<string name="Value">' + secrets.token_hex(32).upper() + '</string>').encode()
        return cache[uid]
    data = re.sub(b'(<string name="Value">(.*?)</string>)', Value_gg, data)
    return data