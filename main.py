import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os


def load_users_from_csv(file_path):
    users = {}
    try:
        with open(file_path, mode='r',encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row["username"]] = {"password": row["password"], "role": row["role"]}
    except Exception as e:
        messagebox.showerror("Error", f"Error reading file: {e}")
    return users


def save_user_to_csv(file_path, username, password, role): 
    try:
        with open(file_path, mode='a', newline='',encoding='utf-8') as file:
            writer = csv.writer(file) 
            writer.writerow([username, password, role])
            print(f"User {username} added to CSV.")
    except Exception as e:
        messagebox.showerror("Error", f"Error writing to file: {e}")

users_file = "users.csv"  
if not os.path.exists(users_file):
    with open(users_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["username", "password", "role"])  

users = load_users_from_csv(users_file)

root = tk.Tk()
root.title("Cửa Hàng Trực Tuyến")
root.geometry("350x350")

def show_message(function_name):
    messagebox.showinfo("Thông báo", f"Chức năng '{function_name}' đang được bổ sung")


def register_screen():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Đăng Ký Tài Khoản", font=("Arial", 14, "bold")).pack(pady=10)
    
    tk.Label(root, text="Tên người dùng:").pack(pady=5)
    new_username_entry = tk.Entry(root)
    new_username_entry.pack(pady=5)
    
    tk.Label(root, text="Mật khẩu:").pack(pady=5)
    new_password_entry = tk.Entry(root, show="*")
    new_password_entry.pack(pady=5)
    
    tk.Label(root, text="Xác nhận mật khẩu:").pack(pady=5)
    confirm_password_entry = tk.Entry(root, show="*")
    confirm_password_entry.pack(pady=5)
    
    def register():
        username = new_username_entry.get()
        password = new_password_entry.get()
        confirm_password = confirm_password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Lỗi", "Tên người dùng và mật khẩu không được để trống!")
            return
        
        if password != confirm_password:
            messagebox.showerror("Lỗi", "Mật khẩu và xác nhận mật khẩu không khớp!")
            return
        
        if username in users:
            messagebox.showerror("Lỗi", "Tên người dùng đã tồn tại!")
            return
        
        save_user_to_csv(users_file, username, password, "customer")
        users[username] = {"password": password, "role": "customer"}
        messagebox.showinfo("Thông báo", "Đăng ký tài khoản thành công!")
        login_screen()

    tk.Button(root, text="Đăng Ký", command=register).pack(pady=10)
    tk.Button(root, text="Quay lại đăng nhập", command=login_screen).pack(pady=5)


def login_screen():
    global current_user
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Tên người dùng:").pack(pady=10)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)
    
    tk.Label(root, text="Mật khẩu:").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)
    
    current_user = None

    def login():
        global current_user
        username = username_entry.get()
        password = password_entry.get()
        
        user = users.get(username)
        if user and user["password"] == password:
            messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
            current_user = username
            if user["role"] == "admin":
                admin_screen()
            else:
                customer_screen()
        else:
            messagebox.showerror("Lỗi", "Tên người dùng hoặc mật khẩu không chính xác!")

    tk.Button(root, text="Đăng nhập", command=login).pack(pady=20)



def customer_screen():
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Chức năng Khách hàng", font=("Arial", 14, "bold")).pack(pady=10)
    functions_khach_hang = [
        "Quản lý thông tin cá nhân", 
        "Xem sản phẩm",
        
        "Đơn hàng"
    

    ]
    for func in functions_khach_hang:
       
        if func == "Quản lý thông tin cá nhân":
            btn = tk.Button(root, text=func, width=30, command=lambda: manage_personal_info(current_user))
        else:
            btn = tk.Button(root, text=func, width=30, command=lambda f=func: show_message(f))
        btn.pack(pady=5)
    tk.Button(root, text="Đăng xuất", command=login_screen, fg="red").pack(pady=20)

def show_personal_info(username):
    profile_file = "user_profiles.csv"
    user_profile = {}
    
    if os.path.exists(profile_file):
        with open(profile_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    user_profile = row
                    break
    
    info_frame = tk.Frame(root)
    info_frame.pack(pady=10)
    
    tk.Label(info_frame, text="Thông tin cá nhân:", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
    tk.Label(info_frame, text=f"Tên: {username}").grid(row=1, column=0, sticky="w")
    tk.Label(info_frame, text=f"Email: {user_profile.get('email', 'Chưa cập nhật')}").grid(row=2, column=0, sticky="w")
    tk.Label(info_frame, text=f"Số điện thoại: {user_profile.get('phone number', 'Chưa cập nhật')}").grid(row=3, column=0, sticky="w")
    tk.Label(info_frame, text=f"Địa chỉ: {user_profile.get('address', 'Chưa cập nhật')}").grid(row=4, column=0, sticky="w")


def manage_personal_info(username):
    profile_file = "user_profiles.csv"
    
    if not os.path.exists(profile_file):
        with open(profile_file, mode='w', newline='',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["userna0me", "phone number", "email", "address"])

    user_profile = {}
    with open(profile_file, mode='r', newline='',encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == username:
                user_profile = row
                break

    profile_window = tk.Toplevel(root)
    profile_window.title(f"Thông tin cá nhân - {username}")
    profile_window.geometry("400x400")

    tk.Label(profile_window, text="Tên:").pack(pady=5)
    name_entry = tk.Entry(profile_window)
    name_entry.insert(0, user_profile.get("name", ""))  
    name_entry.pack(pady=5)


    tk.Label(profile_window, text="Địa chỉ:").pack(pady=5)
    address_entry = tk.Entry(profile_window)
    address_entry.insert(0, user_profile.get("address", ""))  
    address_entry.pack(pady=5)

    tk.Label(profile_window, text="Email:").pack(pady=5)
    email_entry = tk.Entry(profile_window)
    email_entry.insert(0, user_profile.get("email", ""))  
    email_entry.pack(pady=5)

    tk.Label(profile_window, text="Số điện thoại:").pack(pady=5)
    phone_entry = tk.Entry(profile_window)
    phone_entry.insert(0, user_profile.get("phone number", ""))  
    phone_entry.pack(pady=5)

    def save_profile():
        new_name = name_entry.get()
        new_address = address_entry.get()
        new_email = email_entry.get()
        new_phone = phone_entry.get()

        updated_profiles = []
        found_user = False
        with open(profile_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    row["name"] = new_name
                    row["address"] = new_address
                    row["email"] = new_email
                    row["phone number"] = new_phone
                    found_user = True
                updated_profiles.append(row)

        
        if not found_user:
            updated_profiles.append({
                "username": username,
                "name": new_name,
                "address": new_address,
                "email": new_email,
                "phone number": new_phone
            })

    
        with open(profile_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["username", "name","phone number", "email", "address"])
            writer.writeheader()
            writer.writerows(updated_profiles)

        messagebox.showinfo("Thông báo", "Cập nhật thông tin cá nhân thành công!")
        profile_window.destroy()

    tk.Button(profile_window, text="Lưu thông tin", command=save_profile).pack(pady=10)


def admin_screen():
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Chức năng Admin", font=("Arial", 14, "bold")).pack(pady=10)
    functions_nhan_vien = [
        "Quản lý Kho hàng",  
        "Quản lý sản phẩm",
        "Quản lý khách hàng",
        "Thêm tài khoản" 
    ]
    for func in functions_nhan_vien:
        btn = tk.Button(root, text=func, width=30, command=lambda f=func: add_user_screen() if f == "Thêm tài khoản" else show_message(f))
        btn.pack(pady=5)

    tk.Button(root, text="Đăng xuất", command=login_screen, fg="red").pack(pady=20)

def add_user_screen():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Thêm Tài Khoản Mới", font=("Arial", 14, "bold")).pack(pady=10)
    
    tk.Label(root, text="Tên người dùng:").pack(pady=10)
    new_username_entry = tk.Entry(root)
    new_username_entry.pack(pady=5)
    
    tk.Label(root, text="Mật khẩu:").pack(pady=10)
    new_password_entry = tk.Entry(root, show="*")
    new_password_entry.pack(pady=5)
    
    tk.Label(root, text="Vai trò (admin/customer):").pack(pady=10)
    new_role_entry = tk.Entry(root)
    new_role_entry.pack(pady=5)
    
    def add_user():
        username = new_username_entry.get()
        password = new_password_entry.get()
        role = new_role_entry.get()
        
        if not username or not password:
            messagebox.showerror("Lỗi", "Tên người dùng và mật khẩu không được để trống!")
            return

        if role not in ["admin", "customer"]:
            messagebox.showerror("Lỗi", "Vai trò phải là 'admin' hoặc 'customer'!")
            return

        if username not in users:
            save_user_to_csv(users_file, username, password, role)  
            users[username] = {"password": password, "role": role}  
            messagebox.showinfo("Thông báo", "Thêm tài khoản thành công!")
            admin_screen()  # Quay lại giao diện admin
        else:
            messagebox.showerror("Lỗi", "Tài khoản đã tồn tại!")

    tk.Button(root, text="Thêm Tài Khoản", command=add_user).pack(pady=20)
    tk.Button(root, text="Quay lại", command=admin_screen, fg="red").pack(pady=5)

def manage_inventory():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Quản lý Kho hàng", font=("Arial", 14, "bold")).pack(pady=10)
    
    inventory_file = "khohan.csv"

    if not os.path.exists(inventory_file):
        try:
            with open(inventory_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Mã SP", "Tên SP", "Số lượng", "Giá"])
            print(f"Đã tạo file {inventory_file}")
        except Exception as e:
            print(f"Lỗi khi tạo file: {e}")
            messagebox.showerror("Lỗi", f"Không thể tạo file inventory.csv: {e}")
            return

    def load_inventory():
        products = []
        try:
            with open(inventory_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    products.append(row)
            print(f"Đã đọc {len(products)} sản phẩm từ file")
        except Exception as e:
            print(f"Lỗi khi đọc file: {e}")
            messagebox.showerror("Lỗi", f"Không thể đọc file inventory.csv: {e}")
        return products

    def refresh_inventory():
        for widget in inventory_frame.winfo_children():
            widget.destroy()

        products = load_inventory()
        if not products:
            tk.Label(inventory_frame, text="Không có sản phẩm hoặc không thể đọc dữ liệu", fg="red").pack(pady=10)
        else:
            for product in products:
                product_info = f"{product.get('Mã SP', 'N/A')} - {product.get('Tên SP', 'N/A')} - SL: {product.get('Số lượng', 'N/A')} - Giá: {product.get('Giá', 'N/A')}"
                tk.Label(inventory_frame, text=product_info, anchor="w").pack(fill=tk.X, padx=5, pady=2)

    inventory_frame = tk.Frame(root)
    inventory_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(inventory_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas = tk.Canvas(inventory_frame, yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar.config(command=canvas.yview)

    products_frame = tk.Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=products_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    products_frame.bind("<Configure>", on_frame_configure)

    refresh_inventory()

    
    tk.Button(root, text="Làm mới danh sách", command=refresh_inventory).pack(pady=5)

    tk.Button(root, text="Quay lại", command=admin_screen).pack(pady=10)

def manage_customers():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Quản lý thông tin khách hàng", font=("Arial", 14, "bold")).pack(pady=10)

    # Create a frame for the table
    table_frame = tk.Frame(root)
    table_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Create the Treeview widget
    columns = ("Username", "Name", "Email", "Phone", "Address")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    # Define column headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    # Pack the Treeview and scrollbar
    tree.pack(side="left", fill=tk.BOTH, expand=True)
    scrollbar.pack(side="right", fill="y")

    profiles_file = "user_profiles.csv"

    def load_customers():
        customers = []
        if os.path.exists(profiles_file):
            with open(profiles_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    customers.append(row)
        return customers

    def populate_table():
        # Clear existing data
        for item in tree.get_children():
            tree.delete(item)

        # Load and insert customer data
        customers = load_customers()
        for customer in customers:
            tree.insert("", "end", values=(
                customer['username'],
                customer.get('name'),
                customer.get('email'),
                customer.get('phone number'),
                customer.get('address')
            ))

    # Populate the table initially
    populate_table()

    # Add a refresh button
    tk.Button(root, text="Làm mới", command=populate_table).pack(pady=5)

    # Add a back button
    tk.Button(root, text="Quay lại", command=admin_screen).pack(pady=10)




login_screen()  
register_screen()
root.mainloop()

