from requests import post 
def Sound_Cloud(url):
	cookies = {
	    '__appid': 'mjal3qiihfvcod2milej5edq',
	    '_ga': 'GA1.1.331925214.1716831909',
	    '__gads': 'ID=23a524574e0f0a38:T=1716831912:RT=1716831912:S=ALNI_MbYyuMEZgod4I8Rgf7fXuRbBuWfPA',
	    '__gpi': 'UID=00000e2f9bfe4069:T=1716831912:RT=1716831912:S=ALNI_MZUBW1Hapuwk3sN_VzBN-TimnUrqw',
	    '__eoi': 'ID=6bcc63359be37c0c:T=1716831912:RT=1716831912:S=AA-AfjZ7N6Etee0TmislZVEu8sLg',
	    'FCNEC': '%5B%5B%22AKsRol-DzATn0HpqOcuVgZRwfWDZxfp8XlKWKmRPkdcn4KJNolLjpQOVPttDU686i_3hSTsH6YI6wdzf8UlF67pBG5DQu-oHMydBQ_aMPU4ImICnhzRaHOvnemuxX-vowdqYXeWJj4yu_IXda2blSt_F10utqBsHtA%3D%3D%22%5D%2Cnull%2C%5B%5B2%2C%22%5Bnull%2C%5Bnull%2C1%2C%5B1716831913%2C100839000%5D%5D%5D%22%5D%5D%5D',
	    '_ga_SHQJLF27GY': 'GS1.1.1716831908.1.1.1716831948.0.0.0',
	}
	
	headers = {
	    'authority': 'soundcloudtool.com',
	    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	    'accept-language': 'ar-US,ar;q=0.9,en-US;q=0.8,en;q=0.7,ku;q=0.6',
	    'cache-control': 'max-age=0',
	    'content-type': 'application/x-www-form-urlencoded',
	    'origin': 'https://soundcloudtool.com',
	    'referer': 'https://soundcloudtool.com/',
	    'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
	    'sec-ch-ua-mobile': '?1',
	    'sec-ch-ua-platform': '"Android"',
	    'sec-fetch-dest': 'document',
	    'sec-fetch-mode': 'navigate',
	    'sec-fetch-site': 'same-origin',
	    'sec-fetch-user': '?1',
	    'upgrade-insecure-requests': '1',
	    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
	}
	
	data = {
	    'csrfmiddlewaretoken': 'zgnUutXGZ9r4NMvrMAimTDH99NfehN46FQRKmkai8gi6e0DLq7yLo68ilYfWL0Yk',
	    'soundcloud': f'{url}',
	}
	
	r = post('https://soundcloudtool.com/soundcloud-downloader-tool', cookies=cookies, headers=headers, data=data).text.split('<a class="btn-link"')[1].split('href="')[1].split('"')[0]
	return r