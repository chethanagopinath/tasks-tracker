import streamlit as st
import datetime
from google.cloud import firestore

page_title = "My personal tasks tracker"
page_icon = "🗒"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title("Tasks tracker " + page_icon)

task_name = st.text_input('Task name', 'The actual task')
task_due_date = st.date_input("When is this due?", datetime.date.today())
notes = st.text_area("Notes", "Additional details and links about task")

"---"

submitted = st.button("Save task")
if submitted:
    # TODO: insert into database
    st.write(f"Task {task_name} saved for {task_due_date}")
    st.success("Data saved!")


# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("firestore-key.json")


doc_ref = db.collection("tasks").document("tasks-doc")
doc = doc_ref.get()

st.write("The id is: ", doc.id)
st.write("The contents are: ", doc.to_dict())