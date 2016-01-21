import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc
import urllib, json
import os

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
#xbmc.log("SYS ARGV:" + str(sys.argv))

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addonPath = xbmcaddon.Addon().getAddonInfo("path")
addonArt = os.path.join(addonPath,'resources/images/')
#xbmcgui.Dialog().ok(addonname, sys.argv[0], sys.argv[1], sys.argv[2])

args = urlparse.parse_qs(sys.argv[2][1:])
xbmcplugin.setContent(addon_handle, 'movies')
mode = args.get('mode', None)
url = "https://raw.githubusercontent.com/anhstar/Karaoke/master/KaraokeList.json" 
response = urllib.urlopen(url);
data = json.loads(response.read())
#xbmc.log(str(data))

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)
    
def doChannel(chan):
    icon = "karaoke-icon.png"
    if 'icon' in chan:
        icon = chan["icon"]    
        if 'http' not in icon:
            icon = addonArt+icon
    #xbmc.log("chan:"+str(chan))
    #xbmc.log("chan ID:"+chan["id"])
    url = "plugin://plugin.video.youtube/"+chan["id"].encode('utf-8')
    li = xbmcgui.ListItem("[COLOR blue]" + chan["name"].encode('utf-8')+ "[/COLOR]", iconImage=addonArt+icon, thumbnailImage=icon)
    li.setProperty('isplayable', 'true')
    xbmcplugin.addDirectoryItem(handle=addon_handle , url=url, listitem=li, isFolder=True)

def doPlaylist(playlist):
    icon = "karaoke-icon.png"
    if 'icon' in playlist:
        icon = playlist["icon"]   
        if 'http' not in icon:
            icon = addonArt+icon

        xbmc.log("Icon for playlist:"+str(icon))
    #xbmc.log("playlist:"+str(playlist))
    #xbmc.log("playlist ID:"+playlist["id"])
    url = "plugin://plugin.video.youtube/"+playlist["id"].encode('utf-8')
    li = xbmcgui.ListItem("[COLOR green]" + playlist["name"].encode('utf-8')+ "[/COLOR]", iconImage=icon, thumbnailImage=icon)
    li.setProperty('isplayable', 'true')
    xbmcplugin.addDirectoryItem(handle=addon_handle , url=url, listitem=li, isFolder=True)  
    
def doCategory(category, catalogueId):
    #xbmc.log("IN CATEGORY")
    categoryname=category["name"].encode('utf-8')
    icon = "karaoke-icon.png"
    if 'icon' in category:
        icon = category["icon"]    
        if 'http' not in icon:
            icon = addonArt+icon
    #xbmc.log(category["name"].encode('utf-8'))
    url = build_url({'mode': 'category', 'foldername': categoryname, "id":str(catalogueId),"catid":str(category["id"]) })
    li = xbmcgui.ListItem("[B][COLOR yellow]" + categoryname+ "[/COLOR][/B]", iconImage=addonArt+icon, thumbnailImage=icon)
    #xbmc.log("URL: "+str(url))
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    #xbmc.log("END WORK CATEGORY")

#xbmc.log("BEGINNING")
if mode is None:
    for cat in data["catalogues"]:
        foldername=cat["name"].encode('utf-8')
        #xbmc.log(cat["name"].encode('utf-8'))
        url = build_url({'mode': 'folder', 'foldername': foldername, "id":str(cat["id"])})
        li = xbmcgui.ListItem("[B][COLOR yellow]" + foldername + "[/COLOR][/B]", iconImage='DefaultFolder.png')
        #xbmc.log("URL: "+str(url))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    #xbmc.log("IN MODE NONE")
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'folder':
    id=int(args.get('id', None)[0])
    #xbmc.log("ID :"+str(id))
    #xbmc.log("IN MODE FOLDER")
    if 'categorie' in data["catalogues"][id]:
        for category in data["catalogues"][id]["categorie"]:
            doCategory(category, id)
    if 'playlist' in data["catalogues"][id]:        
        for playlist in data["catalogues"][id]["playlist"]:
            doPlaylist(playlist)    
    if 'channels' in data["catalogues"][id]:             
        for chan in data["catalogues"][id]["channels"]:
            doChannel(chan)




        
    xbmcplugin.endOfDirectory(addon_handle)        
elif mode[0] == 'category':
    id=int(args.get('id', None)[0])
    catid=int(args.get('catid',None)[0])
    #xbmc.log("IN MODE CATEGORY")
    if 'channels' in data["catalogues"][id]["categorie"][catid]:
        for chan in data["catalogues"][id]["categorie"][catid]["channels"]:
            doChannel(chan)
    if 'playlist' in data["catalogues"][id]["categorie"][catid]:
        for playlist in data["catalogues"][id]["categorie"][catid]["playlist"]:
            doPlaylist(playlist)

    xbmcplugin.endOfDirectory(addon_handle)


