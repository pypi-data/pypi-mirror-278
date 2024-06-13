from pytube import YouTube
def YouTube_Download(url):
	try:
	    yt = YouTube(url)
	    stream = yt.streams.get_highest_resolution()
	    download_url = stream.url
	    size = stream.filesize
	    title = yt.title
	    au = yt.author
	    return {"title":title,"author":au,"url":download_url,"size":size}
	except Exception as e:
	    return e

