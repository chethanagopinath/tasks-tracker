import streamlit as st
import datetime
from google.cloud import firestore

page_title = "My personal tasks tracker"
page_icon = "🗒"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title("Tasks tracker " + page_icon)

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("firestore-key.json")

task_name = st.text_input('Task name', 'The actual task')
task_due_date = st.date_input("When is this due?", datetime.date.today())
notes = st.text_area("Notes", "Additional details and links about task")

submitted = st.button("Save task")
if submitted:
    # Insert into database
    doc_ref = db.collection("tasks").document(task_name)
    doc_ref.set({
		"name": task_name,
		"due_date": task_due_date,
        "notes": notes
	})
    st.success("Data saved!")

"---"

# Show all tasks
tasks_ref = db.collection("tasks")
for doc in tasks_ref.stream():
    task = doc.to_dict()
    task_name = task["name"]
    task_due_date = task["due_date"]
    task_notes = task["notes"]

    st.subheader(task_name)
    st.write(f"due by {task_due_date}")
    with st.expander("Notes"):
        st.write(task_notes)
