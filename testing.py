import urllib
import urllib2
import timeit
import pdb

def generate_url():
	i = 0
	while True:
		yield "http://www.bbc.com/{0}".format(i)
		i += 1

url_gen = generate_url()	

def test_func():
	url = "http://0.0.0.0:5000/"
	values = {"url":url_gen.next()}
	data = urllib.urlencode(values)
	request = urllib2.Request(url, data)
	try:
		response = urllib2.urlopen(request)
	except (urllib2.HTTPError) as error:
		print error.read()
		return
	read = response.read()
	return read
	

if __name__ == "__main__":
	print timeit.timeit(test_func, number = 10) / 10.0