import streamlit as st
import sqlite3
import pandas as pd

# Connect to your SQLite file
conn = sqlite3.connect("registration_form.sqlite")
cursor = conn.cursor()

st.title("🏫 Student REgistration system- Student CRUD")

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
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (name, email, password, dob, sex, phone, address))
                    conn.commit()
                    st.success("Student added successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Name and Email are required!")

with tab3:
    st.header("Edit or Delete Student")
    cursor.execute("SELECT Student_ID, Name, Email FROM Student")
    students = cursor.fetchall()
    student_dict = {f"{row[1]} ({row[2]}) - ID: {row[0]}": row[0] for row in students}
    
    selected_student = st.selectbox("Select Student", options=list(student_dict.keys()))
    
    if selected_student:
        student_id = student_dict[selected_student]
        
        cursor.execute("SELECT * FROM Student WHERE Student_ID = ?", (student_id,))
        current = cursor.fetchone()
        columns = [desc[0] for desc in cursor.description]
        current_dict = dict(zip(columns, current))
        
        with st.form("edit_form"):
            name = st.text_input("Name", value=current_dict["Name"])
            email = st.text_input("Email", value=current_dict["Email"])
            password = st.text_input("Password", type="password", value=current_dict["Password"])
            dob = st.date_input("Date of Birth", value=pd.to_datetime(current_dict["DOB"]))
            sex = st.selectbox("Sex", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(current_dict["Sex"]))
            phone = st.text_input("Phone", value=current_dict["Phone"] or "")
            address = st.text_area("Address", value=current_dict["Address"] or "")
            
            col1, col2 = st.columns(2)
            update = col1.form_submit_button("Update")
            delete = col2.form_submit_button("Delete")
            
            if update:
                try:
                    cursor.execute("""
                        UPDATE Student SET Name=?, Email=?, Password=?, DOB=?, Sex=?, Phone=?, Address=?
                        WHERE Student_ID=?
                    """, (name, email, password, dob, sex, phone, address, student_id))
                    conn.commit()
                    st.success("Updated!")
                except Exception as e:
                    st.error(f"Error: {e}")
            
            if delete:
                if st.checkbox("Confirm delete"):
                    cursor.execute("DELETE FROM Student WHERE Student_ID=?", (student_id,))
                    conn.commit()
                    st.success("Deleted!")
                    st.rerun()

st.sidebar.success("Using school_management.sqlite file")


                    
        
        
