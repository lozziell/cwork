from flask import Flask, request,jsonify
from cassandra.cluster import Cluster
import json
import requests
#Assign variable cluster to cassandra DB
cluster = Cluster(contact_points=['172.17.0.2'],port=9042)
session = cluster.connect()
app = Flask(__name__)

# home screen welcome
@app.route('/')
def hello():
	name = request.args.get("name","World")
	return('<h1>Hello, {}!</h1>'.format(name))

# GET method returns all records
@app.route('/symps', methods= ['GET'])
def email():
	rows = session.execute( """Select * From symp.stats""")
	result = []
	for r in rows:
		result.append({"email_address":r.email_address,"age":r.age,"sex":r.sex,"symptom_1":r.symptom_1,"symptom_2":r.symptom_2,"symptom_3":r.symptom_3})
	return jsonify(result)

#GET method takes in email address as parameter
@app.route('/symps/<email>/', methods=['GET'])
def get_symps_by_email(email):
	rows = session.execute( """SELECT * FROM symp.stats""")
	result= []
	for r in rows:
		if r.email_address == email:
			result.append({"age":r.age,"sex":r.sex,"symptom_1":r.symptom_1,"symptom_2":r.symptom_2,"symptom_3":r.symptom_3})
			break
	if len(result)==0:
		result.append({"error":"email not found"}), 404
	return jsonify(result)

# DELETE method based on email_address
@app.route('/symps', methods=['DELETE'])
def delete_a_person():
	session.execute( """DELETE FROM symp.stats WHERE email_address='{}' """.format(request.json["email_address"]))
	return jsonify({"success": True})

# POST method for a full record
@app.route('/symps', methods= ['POST'])
def create():
	session.execute( """INSERT INTO symp.stats(email_address,age,sex,symptom_1,symptom_2,symptom_3)VALUES( '{}',{},'{}','{}','{}','{}')""".format(request.json['email_address'],int(request.json['age']),request.json['sex'],request.json['symptom_1'],request.json['symptom_2'],request.json['symptom_3']))
	return jsonify({'message': 'created: /symps/{}'.format(request.json['email_address'])}),201

# PUT method to update second symptom in record
@app.route('/symps', methods= ['PUT'])
def update():
	session.execute( """UPDATE symp.stats SET symptom_2= '{}' WHERE email_address='{}' """.format(request.json['symptom_2'],request.json['email_address']))
	return jsonify({'message': 'updated: /symps/{}'.format(request.json['email_address'])}),200

# external API. GET Live Bt Country AND Status
@app.route('/symps/external', methods=['GET'])
def external():
	covid_url_template = 'https://api.covid19api.com/live/country/{ctry}/status/confirmed'
	my_ctry = 'switzerland'
	covid_url = covid_url_template.format(ctry=my_ctry)
	resp = requests.get(covid_url)
	if resp.ok:
		covid = resp.json()
		return jsonify(resp.json())
	else:
		print(resp.reason)



if __name__ == '__main__': app.run(host='0.0.0.0', port=80)
