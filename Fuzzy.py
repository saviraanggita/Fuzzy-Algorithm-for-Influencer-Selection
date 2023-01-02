import csv
import sys
import math

input_file = input('Enter file name that contains influencers data: ')
output_file = 'chosen.csv'

input_data,output_data,result_data = [],[],[]

# Membership Jumlah Followers (high)
def followersHigh(data):
	if data > 38000 and data <= 45000:
		return (data-38000)/(45000-38000)
	elif data > 45000:
		return 1
	else:
		return 0

# Membership Jumlah Followers (average)
def followersAverage(data):
	if data > 35000 and data <= 45000:
		return (45000-data)/(45000-35000)
	elif data > 25000 and data <= 35000:
		return 1
	elif data > 15000 and data <= 25000:
		return (data-15000)/(25000-15000)
	else:
		return 0

# Membership Jumlah Followers (low)
def followersLow(data):
	if data > 15000 and data <= 22000:
		return (22000-data)/(22000-15000)
	elif data <= 15000:
		return 1
	else:
		return 0

# Membership Engagement Rate (high)
def eRateHigh(data):
	if data > 3.1 and data <= 4.0:
		return (data-3.1)/(4.0-3.1)
	elif data > 4.0:
		return 1
	else:
		return 0

# Membership Engagement Rate (average)
def eRateAverage(data):
	if data > 3.0 and data <= 4.0:
		return (4.0-data)/(4.0-3.0)
	elif data > 2.2 and data <= 3.0:
		return 1
	elif data > 1.2 and data <= 2.2:
		return (data-1.2)/(2.2-1.2)
	else:
		return 0

# Membership Engagement Rate (low)
def eRateLow(data):
	if data > 1.2 and data <= 2.0:
		return (2.0-data)/(2.0-1.2)
	elif data <= 1.2:
		return 1
	else:
		return 0

# Membaca data dari file .csv
with open(input_file) as csv_file:
	csv_reader = csv.DictReader(csv_file, skipinitialspace=True)
	for data in csv_reader:
		ID = int(data['id'])
		num_follower = int(data['followerCount'])
		engagement_rate = float(data['engagementRate'])
		input_data.append({'id': ID, 'followerCount': num_follower, 'engagementRate': engagement_rate})

# Fuzzy Inference (Model Sugeno)
for data in input_data:
	# Fuzzification
	fuzzy_input = {
		'fLow': followersLow(data['followerCount']),
		'fAverage': followersAverage(data['followerCount']),
		'fHigh': followersHigh(data['followerCount']),
		'eRLow': eRateLow(data['engagementRate']),
		'eRAverage': eRateAverage(data['engagementRate']),
		'eRHigh': eRateHigh(data['engagementRate'])
	}

	# Fuzzy Rule (logic operators)
	fuzzy_rule = {
		'Not_Selected': max(
			min(fuzzy_input['fLow'], fuzzy_input['eRLow']),
			min(fuzzy_input['fLow'], fuzzy_input['eRAverage']),
			min(fuzzy_input['fAverage'], fuzzy_input['eRAverage']),
			min(fuzzy_input['fAverage'], fuzzy_input['eRLow']),
			min(fuzzy_input['fHigh'], fuzzy_input['eRLow'])
		),
		'Selected': max(
			min(fuzzy_input['fHigh'], fuzzy_input['eRHigh']),
			min(fuzzy_input['fAverage'], fuzzy_input['eRHigh']),
			min(fuzzy_input['fHigh'], fuzzy_input['eRAverage']),
			min(fuzzy_input['fLow'], fuzzy_input['eRHigh'])
		)
	}

	# Nilai Kelayakan skala [0,100]
	not_selected = (fuzzy_rule['Not_Selected'] * 30)
	selected = (fuzzy_rule['Selected'] * 80)

	# Defuzzification
	total_weight = fuzzy_rule['Not_Selected'] + fuzzy_rule['Selected']
	weighted_average = (not_selected + selected) / total_weight

	if (selected > not_selected):
		result_data.append({
			'id': data['id'],
			'followerCount': data['followerCount'],
			'engagementRate': data['engagementRate']
		})

sorted_data = sorted(result_data, key = lambda x: x['engagementRate'], reverse = True)
print('Number of influencers considered\t: ', len(sorted_data))

# Pemilihan 20 influencer berdasarkan engagement rate tertinggi
while len(sorted_data)>20:
	# Memeriksa jika terdapat nilai engagement rate yang sama, pilih data yang memiliki jumlah follower tertinggi
	if sorted_data[len(sorted_data)-1]['engagementRate'] == sorted_data[len(sorted_data)-2]['engagementRate']:
		if sorted_data[len(sorted_data)-1]['followerCount'] > sorted_data[len(sorted_data)-2]['followerCount']:
			del(sorted_data[len(sorted_data)-2])
		else:
			del(sorted_data[len(sorted_data)-1])
	else:
		del(sorted_data[len(sorted_data)-1])

sorted_data = sorted(sorted_data, key = lambda x: x['id'], reverse = False)
print('Number of influencers selected\t\t: ', len(sorted_data))
print('Selected influencers\t\t\t:')
for i in range (len(sorted_data)):
	output_data.append({'id': sorted_data[i]['id']})
	print(str(sorted_data[i]['id'])+'\t'+str(sorted_data[i]['followerCount'])+'\t'+str(sorted_data[i]['engagementRate']))

# Menulis hasil pemilihan 20 influencer ke dalam file chosen.csv
with open(output_file, mode='w', newline='') as csv_file:
	field_names = [*output_data[0]]
	csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
	csv_writer.writeheader()
	csv_writer.writerows(output_data)
print('Result written to', output_file)