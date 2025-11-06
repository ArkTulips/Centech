import os
import pandas as pd
import numpy as np
from datetime import datetime

DATA_FILE = "census_recordsnew.csv"
USER_FILE = "users.csv"
PASS_FILE = "passwords.csv"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPress Enter to continue...")

def ascii_banner():
    print(r"""
  ██████╗███████╗███╗   ██╗████████╗███████╗ ██████╗██╗  ██╗
 ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██╔════╝██╔════╝██║  ██║
 ██║     █████╗  ██╔██╗ ██║   ██║   █████╗  ██║     ███████║
 ██║     ██╔══╝  ██║╚██╗██║   ██║   ██╔══╝  ██║     ██╔═ ██║
 ╚██████╗███████╗██║ ╚████║   ██║   ███████╗╚██████╗██║  ██║
  ╚═════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝

            CAMPUS CENSUS MANAGEMENT SYSTEM
    """)

# ====================== File Loaders ======================

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=[
            "Name","Roll","Age","Gender","Department",
            "Sports_Facility","Food_Shops","Healthcare","Campus_Security","Infrastructure",
            "Hostel_Name","Wifi","Cleaning_Frequency","Washroom_Cleanliness","Warden_Behaviour","NightCanteen_Quality",
            "Mess_Name","Food_Quality","Mess_Hygiene","Food_Sufficient","Staff_Behaviour","Seating_Sufficient",
            "Proctor_Name","Proctor_Assist","Proctor_Meetings","Grievance_Solved","Timestamp"
        ])
        df.to_csv(DATA_FILE, index=False)
        return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def load_users():
    if os.path.exists(USER_FILE):
        return pd.read_csv(USER_FILE)
    else:
        df = pd.DataFrame(columns=["Email","Role","Department"])
        df.to_csv(USER_FILE, index=False)
        return df

def save_users(df):
    df.to_csv(USER_FILE, index=False)

def load_passwords():
    if os.path.exists(PASS_FILE):
        return pd.read_csv(PASS_FILE)
    else:
        df = pd.DataFrame(columns=["Email","Password"])
        df.to_csv(PASS_FILE, index=False)
        return df

def save_passwords(df):
    df.to_csv(PASS_FILE, index=False)

# ====================== Helpers ======================

def get_role_from_email(email):
    if email == "sukrit.pal@gmail.com":
        return "Admin"
    elif email.endswith("@vitstudent.ac.in"):
        return "Student"
    elif email.endswith("@vithostel.ac.in"):
        return "Hostel"
    elif email.endswith("@vitmess.ac.in"):
        return "Mess"
    elif email.endswith("@vitproctor.ac.in"):
        return "Proctor"
    elif email.endswith("@vitcampus.ac.in"):
        return "Campus"
    else:
        return None

def get_rating(prompt):
    """Prompt user for a valid rating (1–5)."""
    while True:
        val = input(prompt).strip()
        if val.lower() == "back":
            return "back"
        if val.isdigit():
            num = int(val)
            if 1 <= num <= 5:
                return str(num)
        print("❌ Invalid rating. Please enter a number between 1 and 5.")

def get_yes_no(prompt):
    """Prompt user for Y/N (case-insensitive)."""
    while True:
        val = input(prompt + " (Y/N): ").strip().lower()
        if val in ["y", "n"]:
            return val.upper()
        elif val == "back":
            return "back"
        print("❌ Invalid choice. Please enter Y or N.")

# ====================== User Management ======================

def register_user():
    users = load_users()
    passwords = load_passwords()
    clear()
    print("=== ADMIN: ADD NEW CLIENT ===\n(Type 'back' to return)\n")

    email = input("Enter Client Email: ").strip()
    if email.lower() == "back":
        return
    role = get_role_from_email(email)
    if role not in ["Hostel","Mess","Proctor","Campus"]:
        print("\n[!] Only client emails allowed!")
        pause()
        return
    if email in users["Email"].values:
        print("\n[!] Email already registered.")
        pause()
        return
    password = input("Enter Password: ").strip()
    if password.lower() == "back":
        return

    dept = ""
    if role == "Proctor":
        dept = input("Enter Department Assigned: ").strip()
        if dept.lower() == "back":
            return

    users = pd.concat([users, pd.DataFrame([{"Email": email, "Role": role, "Department": dept}])], ignore_index=True)
    passwords = pd.concat([passwords, pd.DataFrame([{"Email": email, "Password": password}])], ignore_index=True)
    save_users(users)
    save_passwords(passwords)
    print(f"\n✅ {role} client added successfully!")
    pause()

def delete_client():
    users = load_users()
    passwords = load_passwords()
    clear()
    print("=== DELETE CLIENT ===\n")
    print(users[users["Role"].isin(["Hostel","Mess","Proctor","Campus"])])

    email = input("\nEnter Client Email to Delete (or 'back'): ").strip()
    if email.lower() == "back":
        return
    if email not in users["Email"].values:
        print("[!] Client not found.")
        pause()
        return
    users = users[users["Email"] != email]
    passwords = passwords[passwords["Email"] != email]
    save_users(users)
    save_passwords(passwords)
    print("\n✅ Client deleted successfully.")
    pause()

# ====================== Login ======================

def login():
    while True:
        clear()
        print("=== LOGIN PAGE ===\n(Type 'back' anytime to return)\n")
        email = input("Enter Email: ").strip().lower()
        if email == "back":
            return None, None
        password = input("Enter Password: ").strip()
        if password.lower() == "back":
            return None, None

        # Admin direct login
        if email == "sukrit.pal@gmail.com" and password == "admin":
            print("\n✅ Welcome Admin!")
            pause()
            return "Admin", None

        users = load_users()
        passwords = load_passwords()

        # Normalize both dataframes
        users["Email"] = users["Email"].astype(str).str.strip().str.lower()
        passwords["Email"] = passwords["Email"].astype(str).str.strip().str.lower()
        passwords["Password"] = passwords["Password"].astype(str).str.strip()

        # Merge for easy lookup
        merged = pd.merge(users, passwords, on="Email", how="inner")

        if email in merged["Email"].values:
            record = merged[merged["Email"] == email].iloc[0]
            stored_password = str(record["Password"]).strip()
            if stored_password == password:
                role = record["Role"]
                dept = record["Department"] if "Department" in merged.columns else None
                print(f"\n✅ Login successful as {role}!")
                pause()
                return role, dept
            else:
                print("\n[!] Incorrect password!")
        else:
            print("\n[!] Email not registered!")

        pause()



# ====================== Student Portal ======================

def student_portal():
    clear()
    print("=== STUDENT CENSUS ENTRY PORTAL ===")
    print("(Type 'back' anytime to cancel)\n")

    df = load_data()
    name = input("Enter Full Name: ").strip()
    if name.lower() == "back":
        return
    roll = input("Enter Registration Number: ").strip()
    if roll.lower() == "back":
        return
    if roll in df["Roll"].values:
        print("\n[!] Record already exists.")
        pause()
        return
    age = input("Enter Age: ").strip()
    if age.lower() == "back":
        return
    gender = input("Enter Gender (M/F/O): ").strip().upper()
    if gender.lower() == "back":
        return
    dept = input("Enter Department: ").strip()
    if dept.lower() == "back":
        return

    print("\n=== CAMPUS FACILITIES ===")
    sports = get_rating("Sports facilities (1–5): ")
    if sports == "back": return
    food_shops = get_rating("Food shops (1–5): ")
    if food_shops == "back": return
    health = get_rating("Healthcare (1–5): ")
    if health == "back": return
    security = get_rating("Campus security (1–5): ")
    if security == "back": return
    infra = get_rating("Infrastructure (1–5): ")
    if infra == "back": return

    print("\n=== HOSTEL MANAGEMENT ===")
    hostel_name = input("Hostel Name: ").strip()
    if hostel_name.lower() == "back":
        return
    wifi = get_rating("Wi-Fi (1–5): ")
    if wifi == "back": return
    cleaning = get_rating("Cleaning frequency (1–5): ")
    if cleaning == "back": return
    washroom = get_rating("Washroom cleanliness (1–5): ")
    if washroom == "back": return
    warden = get_rating("Warden behaviour (1–5): ")
    if warden == "back": return
    night_food = get_rating("Night canteen quality (1–5): ")
    if night_food == "back": return

    print("\n=== MESS MANAGEMENT ===")
    mess_name = input("Mess Name: ").strip()
    if mess_name.lower() == "back": return
    food_quality = get_rating("Food quality (1–5): ")
    if food_quality == "back": return
    mess_hyg = get_rating("Mess hygiene (1–5): ")
    if mess_hyg == "back": return
    sufficient = get_yes_no("Food sufficient?")
    if sufficient == "back": return
    staff = get_rating("Staff behaviour (1–5): ")
    if staff == "back": return
    seating = get_yes_no("Seating sufficient?")
    if seating == "back": return

    print("\n=== PROCTOR ===")
    proctor_name = input("Proctor Name: ").strip()
    if proctor_name.lower() == "back": return
    assist = get_yes_no("Proctor assists efficiently?")
    if assist == "back": return
    meetings = get_yes_no("Regular meetings conducted?")
    if meetings == "back": return
    grievance = get_yes_no("Grievances solved?")
    if grievance == "back": return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_entry = {
        "Name": name,"Roll": roll,"Age": age,"Gender": gender,"Department": dept,
        "Sports_Facility": sports,"Food_Shops": food_shops,"Healthcare": health,
        "Campus_Security": security,"Infrastructure": infra,
        "Hostel_Name": hostel_name,"Wifi": wifi,"Cleaning_Frequency": cleaning,
        "Washroom_Cleanliness": washroom,"Warden_Behaviour": warden,"NightCanteen_Quality": night_food,
        "Mess_Name": mess_name,"Food_Quality": food_quality,"Mess_Hygiene": mess_hyg,
        "Food_Sufficient": sufficient,"Staff_Behaviour": staff,"Seating_Sufficient": seating,
        "Proctor_Name": proctor_name,"Proctor_Assist": assist,"Proctor_Meetings": meetings,
        "Grievance_Solved": grievance,"Timestamp": timestamp
    }

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    save_data(df)
    print("\n✅ Record Added Successfully!")
    pause()

# ====================== Admin Portal ======================

def admin_portal():
    while True:
        clear()
        print("=== ADMIN PORTAL ===\n1. View Records\n2. Delete Record\n3. Add Client\n4. Delete Client\n5. Stats\n6. Back")
        choice = input("\nEnter choice: ").strip()
        df = load_data()

        if choice == '1':
            clear()
            print("1. Proctor Records\n2. Hostel Records\n3. Mess Records\n4. Campus Records\n5. All Records")
            sub = input("\nEnter choice: ").strip()

            if sub == '1':
                subset = df[["Roll","Name","Department","Proctor_Name","Proctor_Assist","Proctor_Meetings","Grievance_Solved"]]
            elif sub == '2':
                subset = df[["Roll","Name","Hostel_Name","Wifi","Cleaning_Frequency","Washroom_Cleanliness","Warden_Behaviour","NightCanteen_Quality"]]
            elif sub == '3':
                subset = df[["Roll","Name","Mess_Name","Food_Quality","Mess_Hygiene","Staff_Behaviour","Food_Sufficient","Seating_Sufficient"]]
            elif sub == '4':
                subset = df[["Roll","Name","Department","Campus_Security","Infrastructure","Healthcare","Sports_Facility","Food_Shops"]]
            elif sub == '5':
                subset = df
            else:
                continue

            print("\n=== RECORDS ===")
            print(subset if not subset.empty else "\n[No records found.]")
            pause()

        elif choice == '2':
            roll = input("Enter Roll Number to delete (or 'back'): ").strip()
            if roll.lower() == "back": continue
            if roll in df["Roll"].values:
                df = df[df["Roll"] != roll]
                save_data(df)
                print("\n✅ Record deleted!")
            else:
                print("\n[!] No record found.")
            pause()

        elif choice == '3':
            register_user()
        elif choice == '4':
            delete_client()
        elif choice == '5':
            clear()
            print("=== REPORT ===")
            print(f"Total Students: {len(df)}")
            print(f"Male: {(df['Gender']=='M').sum()} | Female: {(df['Gender']=='F').sum()}")

            rating_cols = ["Sports_Facility","Food_Shops","Healthcare","Campus_Security","Infrastructure",
                           "Wifi","Cleaning_Frequency","Washroom_Cleanliness","Warden_Behaviour","NightCanteen_Quality",
                           "Food_Quality","Mess_Hygiene","Staff_Behaviour"]

            for col in rating_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                print(f"{col.replace('_',' ')} : {np.nanmean(df[col]):.2f}")
            pause()
        elif choice == '6':
            break
        else:
            pause()

# ====================== Client Portal ======================

def client_portal(role, dept=None):
    df = load_data()
    clear()
    print(f"=== {role.upper()} PORTAL ===\n")
    if role == "Hostel":
        subset = df[["Roll","Name","Hostel_Name","Wifi","Cleaning_Frequency","Washroom_Cleanliness","Warden_Behaviour","NightCanteen_Quality"]]
    elif role == "Mess":
        subset = df[["Roll","Name","Mess_Name","Food_Quality","Mess_Hygiene","Staff_Behaviour","Food_Sufficient","Seating_Sufficient"]]
    elif role == "Proctor":
        subset = df[df["Department"].str.lower() == dept.lower()][["Roll","Name","Department","Proctor_Name","Proctor_Assist","Proctor_Meetings","Grievance_Solved"]]
    elif role == "Campus":
        subset = df[["Roll","Name","Department","Campus_Security","Infrastructure","Healthcare","Sports_Facility","Food_Shops"]]
    else:
        print("[!] Unauthorized role.")
        pause()
        return
    print(subset if not subset.empty else "\n[No records available.]")
    pause()

# ====================== Main ======================

def main():
    while True:
        clear()
        ascii_banner()
        print("1. Login\n2. Student Entry\n3. Exit")
        choice = input("\nEnter choice: ").strip()

        if choice == '1':
            role, dept = login()
            if not role:
                continue
            if role == "Student":
                student_portal()
            elif role == "Admin":
                admin_portal()
            elif role in ["Hostel","Mess","Proctor","Campus"]:
                client_portal(role, dept)
        elif choice == '2':
            student_portal()
        elif choice == '3':
            clear()
            print("Exiting system...")
            break
        else:
            pause()

if __name__ == "__main__":
    main()
