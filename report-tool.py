#!/usr/bin/env python3

import psycopg2


try:
    conn = psycopg2.connect("dbname=news")
except psycopg2.Error as e:
    print("\nUnable to connect!\n")
    print(e.pgerror)
    print(e.diag.message_detail)
    sys.exit(1)
else:
    print("\nConnected to the database!")

c = conn.cursor()

queryarti = """select b.title, count(*) as num from
               (select * from articles join truepath on
               articles.slug=truepath.replace)
               as b join authors on authors.id = b.author group
               by title order by num desc limit 3
            """


queryauth = """select name, count(*) as num from
               (select * from articles join truepath
               on articles.slug=truepath.replace)
               as b join authors on authors.id = b.author
               group by name order by num desc
            """

make_view = """create or replace view truepath as
               select replace(path , '/article/', ''),
               ip, method, status, time,
               id from log where path != '/'
            """

queryerrors = """
select * from (
    select a.day,
    round(cast((100*b.errors) as numeric) / cast(a.errors as numeric), 2)
    as numz from
        (select date(time) as day, count(*) as errors from log group by day)
        as a inner join
        (select date(time) as day, count(*) as errors from log where status
        = '404 NOT FOUND' group by day) as b
    on a.day = b.day)
as k where numz > 1.0;
"""


def articlesview():
    c.execute(queryarti)
    results = c.fetchall()
    return results


def authorsview():
    c.execute(queryauth)
    results = c.fetchall()
    return results


def createview():
    c.execute(make_view)


def errorsshow():
    c.execute(queryerrors)
    results = c.fetchall()
    return results


createview()


print("\nWhat are the most popular three articles of all time?\n")
for a, b in articlesview():
    print('\t' + '. "{}" - {} views'.format(a, b))

print("\nWho are the most popular article authors of all time?:\n")
for a, b in authorsview():
    print('\t' + '. {} - {} views'.format(a, b))

print("\nOn which days did more than 1% of request lead to errors?\n")
for a, b in errorsshow():
    print('\t' + '. {} - {} % errors\n'.format(a, b))
