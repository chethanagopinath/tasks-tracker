import datetime
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from google.oauth2 import service_account
import json

import streamlit as st
from streamlit_option_menu import option_menu

page_title = "My personal tasks tracker"
page_icon = "🗒"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title("Tasks tracker " + page_icon)

# Navigation menu
selected = option_menu(
    menu_title=None,
    options=["Add task", "See all tasks"],
    icons=["plus", "list-task"],
    orientation="horizontal",
)

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

if selected == "Add task":
    task_name = st.text_input('Task name', 'The actual task')
    task_due_date = st.date_input("Which date is this due?", datetime.date.today())
    task_due_time = st.time_input(f"When is this is due on {task_due_date}?", datetime.datetime.now())
    notes = st.text_area("Notes", "Additional details and links about task")

    submitted = st.button("Save task")
    if submitted:
        # Insert into database
        doc_ref = db.collection("tasks").document(task_name)
        doc_ref.set({
            "name": task_name,
            "due_date": str(task_due_date),
            "due_time": str(task_due_time),
            "notes": notes
        })
        st.success("Data saved!")

if selected == "See all tasks":
    tasks_ref = db.collection("tasks")

    # tasks_for_current_week = st.button("Tasks for current week")

    # TODO: fix this
    # if tasks_for_current_week:
    #     tasks_ref.where(filter=FieldFilter("capital", "==", True))
    # st.markdown(":violet[Enter date to see tasks for that date]")
    specific_date = st.date_input("Check for tasks on",datetime.date.today())

    tasks = tasks_ref.where(filter=FieldFilter("due_date", "==", str(specific_date))).stream()

    for doc in tasks:
        task = doc.to_dict()
        task_name = task["name"]
        task_due_date = task["due_date"]
        task_due_time = task["due_time"]
        task_notes = task["notes"]

        st.subheader(task_name)
        st.write(f"due by {task_due_date}")
        with st.expander("Notes"):
            st.write(task_notes)
