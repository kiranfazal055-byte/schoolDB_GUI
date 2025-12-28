import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

# === CHANGE THESE ===
PASSWORD = "MySQL360."  # Your MySQL password
DATABASE_NAME = "schoolDB"       # Your schema name

# Connect to MySQL
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=PASSWORD,
        database=DATABASE_NAME
    )
    if conn.is_connected():
        st.success("Connected to MySQL database!")
except Error as e:
    st.error(f"Connection failed: {e}")
    st.stop()

cursor = conn.cursor()

st.title("🏫 School Management System - Student CRUD")

# Tabs for different operations
tab1, tab2, tab3 = st.tabs(["View Students", "Add Student", "Edit/Delete Student"])

with tab1:
    st.header("All Students")
    cursor.execute("SELECT * FROM Student")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=columns)
    st.dataframe(df, use_container_width=True)

with tab2:
    st.header("Add New Student")
    with st.form("add_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        dob = st.date_input("Date of Birth")
        sex = st.selectbox("Sex", ["Male", "Female", "Other"])
        phone = st.text_input("Phone")
        address = st.text_area("Address")
        submit = st.form_submit_button("Add Student")
        
        if submit:
            if name and email:
                try:
                    cursor.execute("""
                        INSERT INTO Student (Name, Email, Password, DOB, Sex, Phone, Address)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (name, email, password, dob, sex, phone, address))
                    conn.commit()
                    st.success("Student added successfully!")
                except Error as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Name and Email are required!")

with tab3:
    st.header("Edit or Delete Student")
    cursor.execute("SELECT Student_ID, Name, Email FROM Student")
    students = cursor.fetchall()
    student_dict = {f"{row[1]} ({row[2]}) - ID: {row[0]}": row[0] for row in students}
    
    selected_student = st.selectbox("Select Student to Edit/Delete", options=list(student_dict.keys()))
    
    if selected_student:
        student_id = student_dict[selected_student]
        
        # Fetch current data
        cursor.execute("SELECT * FROM Student WHERE Student_ID = %s", (student_id,))
        current = cursor.fetchone()
        columns = [desc[0] for desc in cursor.description]
        current_dict = dict(zip(columns, current))
        
        with st.form("edit_form"):
            name = st.text_input("Name", value=current_dict["Name"])
            email = st.text_input("Email", value=current_dict["Email"])
            password = st.text_input("Password", type="password", value=current_dict["Password"])
            dob = st.date_input("Date of Birth", value=current_dict["DOB"])
            sex = st.selectbox("Sex", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(current_dict["Sex"]))
            phone = st.text_input("Phone", value=current_dict["Phone"])
            address = st.text_area("Address", value=current_dict["Address"])
            
            col1, col2 = st.columns(2)
            update_btn = col1.form_submit_button("Update Student")
            delete_btn = col2.form_submit_button("Delete Student")
            
            if update_btn:
                try:
                    cursor.execute("""
                        UPDATE Student SET Name=%s, Email=%s, Password=%s, DOB=%s, Sex=%s, Phone=%s, Address=%s
                        WHERE Student_ID=%s
                    """, (name, email, password, dob, sex, phone, address, student_id))
                    conn.commit()
                    st.success("Student updated!")
                except Error as e:
                    st.error(f"Error: {e}")
            
            if delete_btn:
                if st.checkbox("Confirm deletion"):
                    try:
                        cursor.execute("DELETE FROM Student WHERE Student_ID=%s", (student_id,))
                        conn.commit()
                        st.success("Student deleted!")
                    except Error as e:
                        st.error(f"Error: {e}")

# Footer
st.sidebar.info("Simple Streamlit GUI for your School DB")
st.sidebar.caption("Made quickly for your tutor submission 🚀")