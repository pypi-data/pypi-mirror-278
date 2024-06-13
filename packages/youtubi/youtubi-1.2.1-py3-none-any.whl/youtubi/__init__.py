from pytube import YouTube 
from bs4 import BeautifulSoup 
from urllib.parse import urlparse, parse_qs
import os , string , glob
from moviepy.editor import VideoFileClip, concatenate_videoclips
class Youtubi : 
	def __init__(self) : 
		pass 

	def _read_file_or_text(self,file = None ,text = None ) : 
		assert bool(file) != bool(text) , "Either read from file or string not both , (text != None ) or (file != None )"
		htmltext = None 
		if text is None : 
			with open(file) as buff : 
				htmltext = buff.read()
		if text is not None : 
			htmltext = text
		return htmltext 

	def joinPlaylist(self,path) : 
		video_file_list = glob.glob(f"{path}/*")
		loaded_video_list = []
		for video in sorted(video_file_list):
			print(f"Adding video file:{video}")
			loaded_video_list.append(VideoFileClip(video))
		final_clip = concatenate_videoclips(loaded_video_list)
		merged_video_name =  os.path.join(path,f"{os.path.basename(path)}.mp4")
		final_clip.write_videofile(merged_video_name)

	def clean_name(self,name) : 
		full_letters = list(string.ascii_lowercase)  +  list(string.ascii_uppercase) + [str(i) for i in range(10)] + list("+-. ")
		filename = ''.join([i if  i in full_letters else "_" for i in name  ])
		return filename

	def get_playlist(self,file = None , text = None , join = True ) : 
		htmltext = self._read_file_or_text(file,text)
		soup = BeautifulSoup(htmltext, 'lxml') 
		playlist = soup.find('div', attrs = {'id':'secondary-inner'})
		playlist = playlist.find('ytd-playlist-panel-renderer', attrs = {'id':'playlist'}) 
		if not playlist : 
			raise ValueError("Can not find <ytd-playlist-panel-renderer id='playlist' ...>")
		play_list_title = playlist.find('yt-formatted-string' , attrs={'class' :'title'}).get('title')
		print(f"+> Playlist : {play_list_title}")
		id_play_list = playlist.find('yt-formatted-string' , attrs={'class' :'title'}).find('a').get('href')
		id_play_list = parse_qs(urlparse(id_play_list).query).get('list')[0]
		folder_name = f"{'_'.join(play_list_title.split())}-{id_play_list}"
		folder_name = self.clean_name(folder_name)
		folder_path = os.path.join(os.getcwd(),folder_name)
		os.makedirs(folder_path,exist_ok = True)
		len_videos = len(playlist.findAll('ytd-playlist-panel-video-renderer' , attrs={'id' : 'playlist-items'}))
		print(f"+> Playlist Videos count : {len_videos}")
		print(f"+> Playlist saved in folder {folder_name} : {folder_path}")
		result = list()
		for index , itm in enumerate(playlist.findAll('ytd-playlist-panel-video-renderer' , attrs={'id' : 'playlist-items'})) : 
			video_title = itm.find('span' , attrs = {'id' : 'video-title'}).get('title')
			idx = itm.find('a' , attrs = {'id' : 'wc-endpoint'}).get('href' , None ) 
			parsed_url = urlparse(idx)
			query_params = parse_qs(parsed_url.query)
			query_params = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
			idx = query_params.get('v' , None )
			video_item = dict(title = video_title , index = index , idx  = idx , url = f"https://www.youtube.com/watch?v={idx}?version=3&vq=hd1080"  , playlist = query_params.get('list',None ))
			result.append(video_item)
			self._download(video_item = video_item, folder_path  = folder_path )
		if join : 
			self.joinPlaylist(folder_path)
		return result 
	
	def _download(self,video_item, folder_path  , format_title = "{index}--{playlist}---{idx}--{title}") : 
		full_letters = list(string.ascii_lowercase)  +  list(string.ascii_uppercase) + [str(i) for i in range(10)] + list("+-. ")
		filename = format_title.format(**video_item)
		filename = ''.join([i if  i in full_letters else "_" for i in filename  ])
		try : 
			yt = YouTube(video_item.get('url')) 
			mp4_streams = yt.streams.first()
			mp4_streams.download(output_path=folder_path , filename = filename)
		except Exception as err : 
			print(f"Error {err}")
			print(f"Error {err}" , file = open(f'{filename}.txt',"w"))

	def get_channel(self,file = None , text = None ) : 
		htmltext = self._read_file_or_text(file,text)
		soup = BeautifulSoup(htmltext, 'lxml') 
		print(soup.prettify() , file = open('videos.html',"w"))
		channel_title = soup.find('yt-formatted-string' , attrs= {'id':'channel-handle'}).get_text()
		print(f"+> Channel : {channel_title}")
		tab_title= soup.find('yt-tab-shape',attrs={'tab-title' : "Videos"}).get('aria-selected')
		print(f"+> Channel Videos tab selected : {tab_title}")
		contents = soup.find('div',attrs={'id' : "contents"})
		print(f"+> Channel Videos contents found : {bool(contents)}")
		videos = contents.findAll('a',attrs={'id' : 'video-title-link'})
		print(f"+> Channel Videos count : {len(videos)}")
		folder_name = f"{channel_title}"
		folder_path = os.path.join(os.getcwd(),folder_name)
		print(f"+> Channel Videos will be saved in  : {folder_path}")
		os.makedirs(folder_path,exist_ok = True)
		result = list()
		for index , video in enumerate(videos) : 
			vid = dict()
			v = parse_qs(urlparse(video.get('href')).query).get('v')[0]
			vid['idx'] = v 
			title = "_".join(video.get('title').split())
			print(f"\t{index}/{len(videos)}".ljust(12) , f"++> Video title  : {title}")
			vid['title'] = title
			vid['index'] = index
			url = f"https://www.youtube.com/watch?v={v}?version=3&vq=hd1080"
			vid['url'] = url 
			result.append(vid)
		for vid_item in tqdm(result):
			self._download(video_item = vid_item, folder_path = folder_path  , format_title = "{index}--{idx}--{title}")

	def get_video(self,url,folder_path = None , filename = None) : 
		folder = os.getcwd() if folder_path is None else folder_path
		parsed_url = urlparse(url)
		query_params = parse_qs(parsed_url.query)
		vid = query_params.get('si',None)
		idx = None 
		if vid is not None  : 
			idx = vid[0]
		else  : 
			idx = query_params.get('v',None)[0]
		url = f"https://www.youtube.com/watch?v={idx}?version=3&vq=hd1080"
		yt = YouTube(url) 
		mp4_streams = yt.streams.first()
		mp4_streams.download(output_path=folder , filename = filename)

__all__ = [Youtubi]