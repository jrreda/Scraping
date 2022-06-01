import requests # http requests
import pandas as pd
from bs4 import BeautifulSoup # web scraping
# Send the mail
import smtplib
# email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# system date and time manipulation
import datetime as DT
import dateparser


now = DT.datetime.now()

# email content placeholder
titles= []
dates = []
made_years = []
prices = []
milages = []
locations = []
urls = []

url = 'https://www.olx.com.eg/en/vehicles/cars-for-sale/cairo/?filter=engine_capacity_eq_7%2Cmileage_eq_8_and_9_and_10_and_12_and_14_and_16%2Cnew_used_eq_2%2Cpayment_option_eq_1%2Cpetrol_eq_3%2Cprice_between_3000_to_140000%2Cpurpose_eq_1%2Ctransmission_eq_2%2Cyear_between_2002_to_2022'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


print('Extracting OLX new listed Cars...')
for car in soup.find_all('li', class_='c46f3bfe'):
    # print(car.text)
    titles.append(car.find('div',attrs={'aria-label':'Title'}).text)
    # dates.append(car.find('span',attrs={'aria-label':'Creation date'}).text)
    dates.append(dateparser.parse(car.find('span',attrs={'aria-label':'Creation date'}).text).strftime("%Y-%m-%d %H:%M"))
    made_years.append(car.find('span',attrs={'aria-label':'Year'}).text)
    prices.append(car.find('div',attrs={'aria-label':'Price'}).text)
    milages.append(car.find('span',attrs={'aria-label':'Mileage'}).text)
    locations.append(car.find('span',attrs={'aria-label':'Location'}).text)
    urls.append("https://www.olx.com.eg"+car.article.div.a.get('href'))

df = pd.DataFrame(data= list(zip(titles, dates, made_years, prices, milages, locations, urls)),
                 columns=['Title', 'AdDate', 'Year', 'Price', 'Milage', 'Location', 'URL'])
df.AdDate =  pd.to_datetime(df.AdDate, format="%Y-%m-%d %H:%M")
day_ago = DT.datetime.now()-DT.timedelta(days=1)
df = df[df.AdDate > day_ago]

content = """\
<html>
  <head></head>
  <body>
    <br>------<br>
    {0}
    <br><br>End of Message
  </body>
</html>
""".format(df.to_html())

# update your email details
# make sure to update the Google Low App Access settings before
FROM =  'mahmoudredabs@gmail.com' # "your from email id"
TO = 'mahmoudreda457@gmail.com' # "your to email ids"  # can be a list
# https://stackoverflow.com/questions/46445269/gmail-blocks-login-attempt-from-python-with-app-specific-password
PASS = 'iqjldrtvfzofezrf' # "your email id's password"

# Create a text/plain message
# msg = MIMEText('')
msg = MIMEMultipart()

# msg.add_header('Content-Disposition', 'attachment', filename='empty.txt')
msg['Subject'] = 'OLX Recent car ads [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))
# fp.close()

print('Initiating Server...')

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    #server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    #server.ehlo
    server.login(FROM, PASS)
    server.sendmail(FROM, TO, msg.as_string())
    print('Email Sent...')
except Exception as e:
    raise

server.quit()