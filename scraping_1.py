from bs4 import BeautifulSoup
with open('home.html', 'r') as html_file:
	content = html_file.read()
	# print(content)
	soup = BeautifulSoup(content, 'lxml')
	#print(soup.prettify())
h5_tags = soup.find_all('h5')
courses_offered = []
for text in h5_tags:
    courses_offered.append(text.text)
#print(courses_offered)
price_tag = soup.find_all('a')
course_price = []
for price in price_tag:
    course_price.append(price.text)
#print(course_price)

price_dict = {}
for index, course in enumerate(courses_offered):
    price_dict[course] = course_price[index]
    
#print(price_dict)
all_div = soup.find_all('div', class_= 'card')
# now tags can be access as an atributes
#print(all_div[0].p)

for key, values in (price_dict.items()):
    print(f'{key} costs {values.split()[-1]}')
    






