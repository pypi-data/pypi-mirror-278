from pytube import YouTube 
from bs4 import BeautifulSoup 
from urllib.parse import urlparse, parse_qs
import os 

class Youtubi : 
	def __init__(self) : 
		pass 

	def read_file_or_text(self,file = None ,text = None ) : 
		assert bool(file) != bool(text) , "Either read from file or string not both , (text != None ) or (file != None )"
		htmltext = None 
		if text is None : 
			with open(file) as buff : 
				htmltext = buff.read()
		if text is not None : 
			htmltext = text
		return htmltext 
	
	def get_channels(self,file = None , text = None ) : 
		htmltext = self.read_file_or_text(file,text)
		soup = BeautifulSoup(htmltext, 'lxml') 
		playlist = soup.find('div', attrs = {'id':'secondary-inner'})
		playlist = playlist.find('ytd-playlist-panel-renderer', attrs = {'id':'playlist'}) 
		result = list()
		for index , itm in enumerate(playlist.findAll('ytd-playlist-panel-video-renderer' , attrs={'id' : 'playlist-items'})) : 
			video_title = itm.find('span' , attrs = {'id' : 'video-title'}).get('title')
			idx = itm.find('a' , attrs = {'id' : 'wc-endpoint'}).get('href' , None ) 
			parsed_url = urlparse(idx)
			query_params = parse_qs(parsed_url.query)
			query_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
			idx = query_params.get('v' , None )
			video_item = dict(title = video_title , index = index , idx  = None , url = f"https://www.youtube.com/watch?v={idx}?version=3&vq=hd1080"  , playlist = query_params.get('list',None ))
			print("{index}. - {title} , {idx} , {playlist} , {url} ".format(**video_item))
			result.append(video_item)
		return result 




def download(link, output_path ) : 
	cache_file = os.path.join(output_path,'.youtu.be.history')
	if not os.path.exists(cache_file): 
		open(cache_file,"w").close()
	else : 
		downloaded_links = {i.strip()  for i in open(cache_file).read().split('\n')}
		if not (link in downloaded_links) : 
			try: 
				yt = YouTube(link) 
				mp4_streams = yt.streams.first()
				mp4_streams.download(output_path=output_path)
				print('Video downloaded successfully!' , yt.title)
				print(link , file = open(cache_file , "a"))
			except: print("Connection Error") 



def process(text, output_path = "./videos") : 
	if not os.path.exists(output_path) : 
		os.mkdir(output_path)
	_text = "\n" + text + "\n"
	urls = _text.strip().split("\n")
	links = set()
	for line in urls : 
		_i = line.strip()
		if len(_i) > 6 : 
			links.add(f"{_i}")
	for link in links : 
		download(link, output_path)




def get_channel(htmlcode) : 
	soup = BeautifulSoup(htmlcode, 'lxml') 
	playlists = soup.findAll('ytd-playlist-panel-renderer', attrs = {'id':'playlist'}) 
	current_playlist = [playlist for playlist in playlists if len(playlist.findAll("a" , attrs = {"id" : "thumbnail"})) != 0 ]
	if len(current_playlist) > 0 :
		playlist = current_playlist[0]
		hrefs = [ a.get('href',None) .replace('/watch?v=','').split("&")[0] for a in playlist.findAll("a" , attrs = {"id" : "thumbnail"}) if a.get('href',None) is not None]
		hrefs = [f"\nhttps://www.youtube.com/watch?v={href}?version=3&vq=hd1080" for href in hrefs]
		print(f"Found {len(hrefs)} youtube video .")
		return "".join(hrefs) + "\n"
	else  : 
		print('Can not find <ytd-playlist-panel-renderer id ="playlist" ' )
		return ""






def get_videos(htmlcode) :
    soup = BeautifulSoup(htmlcode, 'lxml') 
    chips_content = soup.find('ytd-rich-grid-renderer')
    videos = chips_content.findAll('a', attrs = {'id':'thumbnail'}) 
    videos = chips_content.findAll('a', attrs = {'id':"video-title-link" }) 
    counter = 0 
    result = dict()
    for href in videos : 
        if href.get("href",None) : 
            url  = href.get("href",None)
            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            query_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
            video_id = query_params.get('v' , None )
            if video_id  : 
                video_url = f"https://www.youtube.com/watch?v={video_id}?version=3&vq=hd1080"
                result[href.get('title').strip()] = video_url 
                print(counter , " - "  , href.get('title')," " ,  video_url )
                counter +=  1 
    return result

__all__ = [process,get_channel, get_videos]