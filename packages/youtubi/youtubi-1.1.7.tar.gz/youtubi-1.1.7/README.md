# youtubi

Download youtube videos python library .

# Install  : 
```bash
pip install youtubi
```

## Example : 
### Download single video
```python 

from youtubi import Youtubi

y = Youtubi()
url = "https://youtu.be/oaxWxSdytTk?si=DNJOpBMtJyrmaMQR"
y.get_videos(url , folder = None , filename = None)

```
## Download list of videos of playlist 
copy outter html of page where plylist is shown in the page , then 
```python 
from youtubi import Youtubi 
y = Youtubi()
y.get_playlist(file = "playlist.html")

```

## Download channel videos

```python 
from youtubi import Youtubi
y = Youtubi()
y.get_channel(file = "channel.html")

```
