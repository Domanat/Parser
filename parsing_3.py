import requests
import xlsxwriter
from bs4 import BeautifulSoup 


def get_courses():# get courses id
	courses = []
	i = 1

	while True:
		print('getting couses from page {}'.format(i))
		data = {'is_cataloged': 'true',
				'order': '-activity',
				'page': i}
		r = requests.get('https://stepik.org/api/courses', params = data).json()

		for course in r['courses']:
			courses.append(course['id'])

		if not r['meta']['has_next']:
			return courses 

		i += 1

def get_data(course_id): # get comments for specific course 
	reviews = []
	user_id = []
	date = []
	result = []
	i = 1
	while True:
		#print('getting users comments')
		r = requests.get('https://stepik.org/api/course-reviews?course=%d&page=%d' %(course_id, i)).json()
		for course in r['course-reviews']:
			user_id.append(course['user'])
			reviews.append(course['text'])
			date.append(course['create_date'])


		if not r['meta']['has_next']:
			break

		i += 1

	for i in range(len(user_id)):
		result.append({course_id : [{
							'user_id': user_id[i],
						   'comment': reviews[i],
						   'date' : date[i]
							}]})
	return result

def imp(data):
	workbook = xlsxwriter.Workbook('partners.xlsx')
	worksheet = workbook.add_worksheet()

	courses_id = get_courses()
	row = 0
	col = 1

	for i in range(len(data)):

		if len(data[i]) == 0:
			worksheet.write(row, 0, courses_id[i])
			worksheet.write(row, col, '[]')
			worksheet.write(row, col + 1, '[]')
			worksheet.write(row, col + 2, '[]')
			row += 1
		elif len(data[i]) == 1:
			 
			worksheet.write(row, 0, courses_id[i])
			worksheet.write(row, col, data[i][0][courses_id[i]][0]['user_id'])
			worksheet.write(row, col + 1, data[i][0][courses_id[i]][0]['comment'])
			worksheet.write(row, col + 2, data[i][0][courses_id[i]][0]['date'][0: 10])
			row += 1
		else:
			for j in range(len(data[i])):
				worksheet.write(row, 0, courses_id[i])
				worksheet.write(row, col, data[i][j][courses_id[i]][0]['user_id'])
				worksheet.write(row, col + 1, data[i][j][courses_id[i]][0]['comment'])
				worksheet.write(row, col + 2, data[i][j][courses_id[i]][0]['date'][0: 10])
				row += 1

	workbook.close()
def start():
	res = []
	courses_id = get_courses()

	for i in courses_id:
		res.append(get_data(i))
	imp(res)

if __name__ == '__main__':

	start()