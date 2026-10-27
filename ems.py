import mysql.connector


# Database Connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ems"
    )


# Create - Add Employee
def add_employee():
    try:
        task_id = int(input("Enter Task ID: "))

        name = input("Enter Employee Name: ").strip()

        if not name:
            print("Name cannot be empty.")
            return

        if not all(char.isalpha() or char.isspace() for char in name):
            print("Name must contain letters and spaces only.")
            return

        age = int(input("Enter Age: "))
        if age <= 0:
            print("Age must be positive.")
            return

        department = input("Enter Department: ").strip()
        if not department:
            print("Department cannot be empty.")
            return

        salary = float(input("Enter Salary: "))
        if salary <= 0:
            print("Salary must be positive.")
            return

        conn = connect_db()
        cursor = conn.cursor()

        sql = """
        INSERT INTO employees
        (task_id, name, age, department, salary)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (task_id, name, age, department, salary)

        cursor.execute(sql, values)
        conn.commit()

        print("Employee added successfully.")

    except ValueError:
        print("Invalid input.")

    except mysql.connector.Error as err:
        print("Database Error:", err)

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


# Read - View Employees
def view_employees():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM employees")
        records = cursor.fetchall()

        if not records:
            print("No employee records found.")
            return

        print("\n===== EMPLOYEE RECORDS =====")

        for row in records:
            print(f"""
Employee ID : {row[0]}
Task ID     : {row[1]}
Name        : {row[2]}
Age         : {row[3]}
Department  : {row[4]}
Salary      : {row[5]}
--------------------------------
""")

    except mysql.connector.Error as err:
        print("Database Error:", err)

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


# Update Employee
def update_employee():
    try:
        employee_id = int(input("Enter Employee ID to Update: "))

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM employees WHERE employee_id = %s",
            (employee_id,)
        )

        employee = cursor.fetchone()

        if employee is None:
            print("Employee not found.")
            return

        task_id = int(input("Enter New Task ID: "))

        name = input("Enter New Name: ").strip()

        if not name:
            print("Name cannot be empty.")
            return

        if not all(char.isalpha() or char.isspace() for char in name):
            print("Name must contain letters and spaces only.")
            return

        age = int(input("Enter New Age: "))

        department = input("Enter New Department: ").strip()

        salary = float(input("Enter New Salary: "))

        sql = """
        UPDATE employees
        SET task_id = %s,
            name = %s,
            age = %s,
            department = %s,
            salary = %s
        WHERE employee_id = %s
        """

        values = (
            task_id,
            name,
            age,
            department,
            salary,
            employee_id
        )

        cursor.execute(sql, values)
        conn.commit()

        print("Employee updated successfully.")

    except ValueError:
        print("Invalid input.")

    except mysql.connector.Error as err:
        print("Database Error:", err)

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


# Delete Employee
def delete_employee():
    try:
        employee_id = int(input("Enter Employee ID to Delete: "))

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM employees WHERE employee_id = %s",
            (employee_id,)
        )

        employee = cursor.fetchone()

        if employee is None:
            print("Employee not found.")
            return

        confirm = input(
            "Are you sure you want to delete? (Y/N): "
        ).upper()

        if confirm == "Y":
            cursor.execute(
                "DELETE FROM employees WHERE employee_id = %s",
                (employee_id,)
            )

            conn.commit()
            print("Employee deleted successfully.")

        else:
            print("Deletion cancelled.")

    except ValueError:
        print("Invalid input.")

    except mysql.connector.Error as err:
        print("Database Error:", err)

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


# Menu
def main():

    while True:

        print("\n===== EMPLOYEE MANAGEMENT SYSTEM =====")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit")

        choice = input("Enter Choice: ")

        if choice == "1":
            add_employee()

        elif choice == "2":
            view_employees()

        elif choice == "3":
            update_employee()

        elif choice == "4":
            delete_employee()

        elif choice == "5":
            print("Thank you for using EMS.")
            break

        else:
            print("Invalid Choice.")


# Run Program
if __name__ == "__main__":
    main()