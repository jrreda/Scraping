import mysql.connector
import random
import string
import datetime as DT
import pprint
import sys

# create random email
def random_email():
        return ''.join(random.choice(string.ascii_letters) for i in range(10)) + '@test.com'
# create random phone
def random_phone():
    n = '00000000000'
    while '9' in n[3:6] or n[3:6]=='000' or n[6]==n[7]==n[8]==n[9]:
        n = str(random.randint(10**9, 10**10-1))
    return '02010-' + n[:4] + '-' + n[4:8]

# Define Variables
email = random_email()
now = DT.datetime.now()

db = mysql.connector.connect(
    host = "******************",
    user = "******************",
    password = "******************",
    database = "******************"
)
print("Live DB is connected ✔️")

def update_mahmoudredabs():
    cursor = db.cursor()
    query1 = f"UPDATE users SET email = '{random_email()}' WHERE email = 'mahmoudredabs@gmail.com';"
    query2 = f"UPDATE companies SET email = '{random_email()}' WHERE email = 'mahmoudredabs@gmail.com';"
    query3 = f"UPDATE users SET phone = {random_phone()} WHERE phone = '01069907582';"
    query4 = f"UPDATE companies SET phone = {random_phone()} WHERE phone = '01069907582';"

    cursor.execute(query1)
    cursor.execute(query2)
    cursor.execute(query3)
    cursor.execute(query4)
    db.commit()
    if cursor.rowcount > 0:
        print(cursor.rowcount, "record(s) affected")
    else:
        pass


def verify_mail():
    cursor = db.cursor()
    query = f"UPDATE users SET email_verified_at = '{now}' WHERE email = 'mahmoudredabs@gmail.com';"
    
    cursor.execute(query)
    db.commit()
    if cursor.rowcount > 0:
        print("Mail is verfified successfully!")
    else:
        print(cursor.rowcount, "record(s) affected")


def check_table(columns="email", table="users", where="email LIKE '%test%'"):
    '''check emails'''
    cursor = db.cursor()
    query = f"SELECT {columns} FROM {table} WHERE {where}"

    cursor.execute(query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)

def num_of_countries():
    cursor = db.cursor()
    cursor.execute('''
    SELECT country_code, COUNT(name_en)
    FROM companies
    WHERE status_id = 2 AND
        (name_en NOT LIKE '%test%'
        OR name_en NOT LIKE '%trst%'
        OR name_en NOT LIKE '%mailinator%')
    GROUP BY country_code
    ''')

    for x in cursor.fetchall():
        pprint.pprint(x)

def get_companies_products(save_to_excel=True):
    cursor = db.cursor()
    query = '''
        SELECT p.company_id,
               Count(p.id) AS number,
               c.name_en,
               CASE
                 WHEN p.status_id = 1 THEN "new"
                 WHEN p.status_id = 2 THEN "active"
                 WHEN p.status_id = 2 THEN "disapproved"
                 WHEN p.status_id = 2 THEN "pending"
                 WHEN p.status_id = 2 THEN "hold"
               END AS product_status
        FROM   products p
               LEFT JOIN companies c
                      ON p.company_id = c.id
        WHERE  p.deleted_at IS NULL
        GROUP  BY p.company_id,
                  p.status_id
        ORDER  BY p.company_id
        '''

    if save_to_excel:
        df = pd.read_sql(q, db)
        df.to_csv("companies_products.csv", index=False)
    else:
        cursor.execute()
        # print results
        for x in cursor.fetchall():
            pprint.pprint(x)


if __name__ == '__main__':
    args = sys.argv
    # args[0] = current file
    # args[1] = function name
    # args[2:] = function args : (*unpacked)
    globals()[args[1]](*args[2:])