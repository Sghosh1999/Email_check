from tracker_generator import TrackerGenerator
import streamlit as st
import os
import base64
import time
import pandas as pd
import datetime
import sqlite3
import smtplib


st.title("Automatic trcaker Generation :sunglasses:")


def main():

    obj1 = TrackerGenerator()

    def update_user(email, last_date, days=1):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE USERS SET UPDATE_DATE = ? WHERE EMAIL = ?", [
                       last_date, email])

    def send_mail(email, massage="you have not submitted in last 2 days"):
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login("codegeeks.kalna@gmail.com", "Code@Geeks21")

        server.sendmail("codegeeks.kalna@gmail.com", email, massage)

        server.quit()

    def create_user(email, last_date, days=1):

        conn = sqlite3.connect('users.db')

        cursor = conn.cursor()

        id_max = cursor.execute("SELECT MAX(ID) FROM USERS")

        id_max = cursor.fetchall()[0][0]

        if not id_max:
            id_max = 0

        st.write(id_max)

        tuple1 = [id_max+1, email, last_date, days]

        insert_query = """INSERT INTO USERS (ID,EMAIL,UPDATE_DATE,DAY_GAP) VALUES (? , ? , ? , ?)"""

        cursor.execute(insert_query, tuple1)

        conn.commit()
        conn.close()

    def csv_exporter(data, flag):
        csvfile = data.to_csv(index=False)
        b64 = base64.b64encode(csvfile.encode()).decode()
        new_filename = "{}_tracker.csv".format(flag)
        st.markdown("### Downloaf File ###")
        href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!!</a>'
        st.markdown(href, unsafe_allow_html=True)

    def generate_weekly_trackers_multiuser():
        data = pd.DataFrame(columns=['Name', 'Date', 'Task'])

        st.header("Daily Task Uploader")
        # number = st.number_input("Enetr no of users", 1)
        weekly_trackers = list()
        monthly_trackers = list()
        name_user = st.text_input("Your Name")

        if not name_user:
            st.warning("please enter your name")
        else:
            st.text(name_user)
        col1, col2 = st.beta_columns(2)
        today = datetime.date.today()
        # tomorrow = today + datetime.timedelta(days=1)

        start_date = col1.date_input("Start Date", today)
        end_date = col2.date_input("end Date", today)
        # col1.markdown("""---""")
        # col2.markdown("""---""")
        st.markdown("""---""")
        number = end_date - start_date
        number = number.days + 1

        dates = list()
        tasks = list()

        for i in range(number):

            col1, col2 = st.beta_columns(2)

            date_task = col1.date_input(
                "Date", (start_date + datetime.timedelta(i)))
            # col1.text(date_task)

            dates.append(start_date + datetime.timedelta(i))
            task = col2.text_input("tasks", key=i)
            tasks.append(task)

            if not tasks:

                st.warning("please enter a task")

        c1, c2, c3, c4, c5, c6, c7 = st.beta_columns(
            7)  # just to make the button stick to right

        # st.write(dates)
        # st.write(tasks)
        data = dict(zip(dates, tasks))
        st.write(data)
        dataset = pd.DataFrame(data.items(), columns=['Start Date', 'Tasks'])
        st.dataframe(dataset)

        if c7.button("Submit"):
            csv_exporter(dataset, name_user)
            try:
                st.write("update start")

                update_user("gsayantan1999@gmail.com", str(end_date))
                st.write("updated")
            except:
                st.write("new start ")

                create_user("gsayantan1999@gmail.com", str(end_date))
                st.write("created")

            curr_date = datetime.date.today()
            curr_date = pd.to_datetime(curr_date)
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            id_max = cursor.execute("SELECT MAX(ID) FROM USERS")

            id_max = cursor.fetchall()[0][0]

            for id_temp in range(id_max):
                id_temp += 1
                last_temp = cursor.execute(
                    "SELECT UPDATE_DATE,EMAIL FROM USERS WHERE ID = ?", [id_temp])
                fetched = cursor.fetchall()
                last_temp = fetched[0][0]
                email_temp = fetched[0][1]
                last_update_date = pd.to_datetime(last_temp)
                day_gap_user = (curr_date - last_update_date).days
                st.write(last_temp, email_temp, day_gap_user)
                if day_gap_user >= 2:
                    send_mail(email_temp)
                    st.write("mail sent to ", email_temp)

            conn.close()
            # if user_exist:
            #     create_user()
            # else:
            #     update_user()

    generate_weekly_trackers_multiuser()


if __name__ == '__main__':
    main()
