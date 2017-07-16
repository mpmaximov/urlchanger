from flask import Flask
from flask import request
from flask import Response
import requests
import urllib
import json
import urlparse

app = Flask(__name__)

SUPPLIER_URL = "http://hst-api.wialon.com/wialon/ajax.html?"

@app.route('/wialon/ajax.html')
def change_url():


	args = dict(urlparse.parse_qsl(urllib.unquote(urlparse.urlparse(request.url.encode('ascii')).query)))
	paramsstr = urlparse.urlparse(request.url.encode('ascii')).query
	pms = json.loads(args['params'])
	if args.has_key('svc') and args['svc'] == 'messages/load_interval':
		print "Old: " + str(pms['timeFrom']) + " - " + str(pms['timeTo'])
		print "New: " + str(pms['timeFrom'] + 20*3600) + " - " + str(pms['timeTo'])
		paramsstr = paramsstr.replace("\"timeFrom\":"+str(pms['timeFrom']), "\"timeFrom\":"+str(pms['timeFrom'] + 20*3600))
	q = SUPPLIER_URL + paramsstr
	res = requests.get(q).text
	resp = Response(res)
	resp.headers['Content-Type']='application/json'
	return resp

@app.route('/test')
def test_url():
	return "Ok"

if __name__ == '__main__':
    app.run()
