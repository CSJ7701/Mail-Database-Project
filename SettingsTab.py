from io import SEEK_SET
import customtkinter as ctk
from LoginBackend import User
from Screen import Screen


class Settings(Screen):
    def __init__(self, main_frame, ParentGUI):
        self.parent=ParentGUI
        self.main_frame=main_frame
        self.config=self.parent.config
        self.parent.database.cursor.execute(f"SELECT admin FROM accounts WHERE username LIKE '{self.parent.user.username}'")
        self.admin=self.parent.database.cursor.fetchone()[0]
        
        self.UpdateColorLabel()

        self.headline_font=ctk.CTkFont(family="Helvetica", size=20, weight="bold", underline=True)

        self.user_frame=ctk.CTkFrame(self.main_frame, width=300)#, fg_color=("#d3d3d3", "#000000"))
        self.user_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.user_frame_label=ctk.CTkLabel(self.user_frame, text="User Settings", font=self.headline_font)
        self.user_frame_label.pack(side="top", padx=10, pady=30)

        # User Settings
        self.username=ctk.CTkLabel(self.user_frame, text=f"Logged in as:\n\n{self.parent.user.username}")
        self.edit_username_button=ctk.CTkButton(self.user_frame, text="Edit Username", command=self.EditUsername)
        self.edit_userpassword_button=ctk.CTkButton(self.user_frame, text="Edit Password", command=self.EditUserPassword)
        self.color_preference_button=ctk.CTkButton(self.user_frame, text="Appearance Mode", command=self.ChangeColorMode)
        self.color_preference_label=ctk.CTkLabel(self.user_frame, text=self.color_string)

        self.username.pack(side="top", padx=10, pady=10)
        self.edit_username_button.pack(side="top", padx=10, pady=(20,10))
        self.edit_userpassword_button.pack(side="top", padx=10, pady=(10,20))
        self.color_preference_button.pack(side="top", padx=10, pady=10)
        self.color_preference_label.pack(side="top", padx=10, pady=(0,10))

        # Edit Username Frame
        self.username_edit_frame=ctk.CTkFrame(self.user_frame)
        self.new_username_label=ctk.CTkLabel(self.username_edit_frame, text="New Username")
        self.new_username=ctk.CTkEntry(self.username_edit_frame, placeholder_text="New Username")
        self.new_username_password_label=ctk.CTkLabel(self.username_edit_frame, text="Password")
        self.new_username_password=ctk.CTkEntry(self.username_edit_frame, placeholder_text="Password", show="*")
        self.username_save_button=ctk.CTkButton(self.username_edit_frame, text="Save Username", command=self.SaveUsername)
        self.username_cancel_button=ctk.CTkButton(self.username_edit_frame, text="Cancel", command=self.CancelUsernameEdit)

        # Edit Password Frame
        self.password_edit_frame=ctk.CTkFrame(self.user_frame)
        self.old_password_label=ctk.CTkLabel(self.password_edit_frame, text="Old Password")
        self.old_password=ctk.CTkEntry(self.password_edit_frame, placeholder_text="Old Password", show="*")
        self.new_password_label=ctk.CTkLabel(self.password_edit_frame, text="New Password")
        self.new_password=ctk.CTkEntry(self.password_edit_frame, placeholder_text="New Password", show="*")
        self.password_save_button=ctk.CTkButton(self.password_edit_frame, text="Save Password", command=self.SavePassword)
        self.password_cancel_button=ctk.CTkButton(self.password_edit_frame, text="Cancel", command=self.CancelPasswordEdit)
        
        
        # Admin Settings
        self.Admin_frame=ctk.CTkFrame(self.main_frame, width=300)#, fg_color=("#d3d3d3", "#000000"))
        self.Admin_frame.pack(side="left", fill="both", expand=True, pady=10)
        self.admin_frame_label=ctk.CTkLabel(self.Admin_frame, text="Admin Settings", font=self.headline_font)
        self.admin_frame_label.pack(side="top", padx=10, pady=30)

        self.no_admin_label=ctk.CTkLabel(self.Admin_frame, text="You do not\nhave Admin\npriviledges", text_color="#ffff45450000")
        self.request_admin=ctk.CTkButton(self.Admin_frame, text="Request Admin", command=self.OpenRequestAdmin)
        print(self.admin)
        if self.admin == 0:
            self.no_admin_label.pack(side="top", padx=10, pady=15)
            self.request_admin.pack(side="top", padx=10, pady=10)

        self.add_account_button=ctk.CTkButton(self.Admin_frame, text="Add Account", command=self.AddAccountOpen)
        self.add_account_button.pack(side="top", padx=10, pady=10)
        self.delete_account_button=ctk.CTkButton(self.Admin_frame, text="Delete Account", command=self.DeleteAccountOpen)
        self.delete_account_button.pack(side="top", padx=10, pady=10)
        self.edit_account_username=ctk.CTkButton(self.Admin_frame, text="Edit Account Username", command=self.EditUsernameOpen)
        self.edit_account_username.pack(side="top", padx=10, pady=10)
        self.edit_account_password=ctk.CTkButton(self.Admin_frame, text="Edit Account Password", command=self.EditPasswordOpen)
        self.edit_account_password.pack(side="top", padx=10, pady=10)

        if self.admin == 0:
            self.add_account_button.configure(state="disabled")
            self.delete_account_button.configure(state="disabled")
            self.edit_account_username.configure(state="disabled")
            self.edit_account_password.configure(state="disabled")

        
        # Request Admin Frame
        self.request_admin_frame=ctk.CTkFrame(self.Admin_frame)
        self.request_admin_username_label=ctk.CTkLabel(self.request_admin_frame, text="Username")
        self.request_admin_username=ctk.CTkEntry(self.request_admin_frame, placeholder_text="Username")
        self.request_admin_password_label=ctk.CTkLabel(self.request_admin_frame, text="Password")
        self.request_admin_password=ctk.CTkEntry(self.request_admin_frame, placeholder_text="Password", show="*")
        self.request_admin_button=ctk.CTkButton(self.request_admin_frame, text="Login", command=self.LoginRequestAdmin)
        self.request_admin_cancel=ctk.CTkButton(self.request_admin_frame, text="Cancel", command=self.CloseRequestAdmin)

        # Add Account Frame
        self.add_account_frame=ctk.CTkFrame(self.Admin_frame)
        self.add_account_username_label=ctk.CTkLabel(self.add_account_frame, text="Username")
        self.add_account_username=ctk.CTkEntry(self.add_account_frame, placeholder_text="Username")
        self.add_account_password_label=ctk.CTkLabel(self.add_account_frame, text="Password")
        self.add_account_password=ctk.CTkEntry(self.add_account_frame, placeholder_text="Password")
        self.add_account_admin=ctk.CTkCheckBox(self.add_account_frame, text="Is Admin?")
        self.add_account_add_button=ctk.CTkButton(self.add_account_frame, text="Add Account", command=self.AddAccount)
        self.add_account_cancel=ctk.CTkButton(self.add_account_frame, text="Cancel", command=self.AddAccountClose)

        # Delete Account Frame
        self.delete_account_frame=ctk.CTkFrame(self.Admin_frame)
        self.delete_account_username_label=ctk.CTkLabel(self.delete_account_frame, text="Username")
        self.delete_account_username=ctk.CTkEntry(self.delete_account_frame, placeholder_text="Username")
        self.delete_account_confirm=ctk.CTkCheckBox(self.delete_account_frame, text="Are you sure you want to delete this account?")
        self.delete_account_delete_button=ctk.CTkButton(self.delete_account_frame, text="Delete", command=self.DeleteAccount)
        self.delete_account_cancel_button=ctk.CTkButton(self.delete_account_frame, text="Cancel", command=self.DeleteAccountClose)

        # Edit Username Frame
        self.edit_username_frame=ctk.CTkFrame(self.Admin_frame)
        self.edit_username_old_username_label=ctk.CTkLabel(self.edit_username_frame, text="Old Username")
        self.edit_username_old_username=ctk.CTkEntry(self.edit_username_frame, placeholder_text="Old Username")
        self.edit_username_new_username_label=ctk.CTkLabel(self.edit_username_frame, text="New Username")
        self.edit_username_new_username=ctk.CTkEntry(self.edit_username_frame, placeholder_text="New Username")
        self.edit_username_edit_button=ctk.CTkButton(self.edit_username_frame, text="Save Username", command=self.EditUsernameEdit)
        self.edit_username_cancel_button=ctk.CTkButton(self.edit_username_frame, text="Cancel", command=self.EditUsernameClose)

        # Edit Password Frame
        self.edit_password_frame=ctk.CTkFrame(self.Admin_frame)
        self.edit_password_username_label=ctk.CTkLabel(self.edit_password_frame, text="Username")
        self.edit_password_username=ctk.CTkEntry(self.edit_password_frame, placeholder_text="Username")
        self.edit_password_password_label=ctk.CTkLabel(self.edit_password_frame, text="New Password")
        self.edit_password_password=ctk.CTkEntry(self.edit_password_frame, placeholder_text="New Password")
        self.edit_password_edit_button=ctk.CTkButton(self.edit_password_frame, text="Save Password", command=self.EditPassword)
        self.edit_password_cancel=ctk.CTkButton(self.edit_password_frame, text="Cancel", command=self.EditPasswordClose)
        
        
        self.System_frame=ctk.CTkFrame(self.main_frame, width=400)#, fg_colot=("#d3d3d3", "#000000"))
        self.System_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.system_frame_label=ctk.CTkLabel(self.System_frame, text="System Settings", font=self.headline_font)
        self.system_frame_label.pack(side="top", padx=10, pady=30)


    def ChangeColorMode(self):
        if self.config.appearance('color_mode') == 'dark':
            self.config.c['Appearance']['color_mode']='light'
        elif self.config.appearance('color_mode') == 'light':
            self.config.c['Appearance']['color_mode']='dark'
        ctk.set_appearance_mode(self.config.appearance('color_mode'))
        self.UpdateColorLabel()
        self.color_preference_label.configure(text=self.color_string)
        with open('config.ini', 'w') as configfile:
            self.config.c.write(configfile)

    def UpdateColorLabel(self):
        if self.config.appearance("color_mode") == "light":
            self.color_string=" - Light "
        elif self.config.appearance("color_mode") == "dark":
            self.color_string=" - Dark"

    def EditUsername(self):
        if not  self.password_edit_frame.winfo_ismapped():
            self.new_username.delete(0,'end')
            self.new_username_password.delete(0, 'end')
        
            self.username_edit_frame.pack(side="bottom", padx=10, pady=30)
            self.new_username_label.pack(side="top", padx=10, pady=10)
            self.new_username.pack(side="top", padx=10, pady=10)
            self.new_username_password_label.pack(side="top", padx=10, pady=10)
            self.new_username_password.pack(side="top", padx=10, pady=10)
            self.username_save_button.pack(side="top", padx=10, pady=10)
            self.username_cancel_button.pack(side="top", padx=10, pady=10)

    def SaveUsername(self):
        username=self.new_username.get()
        password=self.new_username_password.get()
        auth=self.parent.user.check_pass(password)
        if auth == 1:
            query=f"UPDATE accounts SET username='{username}' WHERE username='{self.parent.user.username}'"
            self.parent.database.cursor.execute(query)
            self.parent.database.conn.commit()
        else:
            self.show_error("Authorization Error.\nCheck your password")

        self.username_edit_frame.pack_forget()
        self.new_username_label.pack_forget()
        self.new_username.pack_forget()
        self.new_username_password_label.pack_forget()
        self.new_username_password.pack_forget()
        self.username_save_button.pack_forget()
        self.username_cancel_button.pack_forget()
        # raise NotImplementedError("Save Function Not written")


    def CancelUsernameEdit(self):
        self.username_edit_frame.pack_forget()
        self.new_username.pack_forget()
        self.new_username_label.pack_forget()
        self.new_username_password.pack_forget()
        self.username_save_button.pack_forget()
        self.new_username_password_label.pack_forget()
        self.username_cancel_button.pack_forget()

    def EditUserPassword(self):
        if not self.username_edit_frame.winfo_ismapped():
            self.new_password.delete(0, 'end')
            self.old_password.delete(0, 'end')
            self.password_edit_frame.pack(side="bottom", padx=10, pady=30)
            self.old_password_label.pack(side="top", padx=10, pady=10)
            self.old_password.pack(side="top", padx=10, pady=10)
            self.new_password_label.pack(side="top", padx=10, pady=10)
            self.new_password.pack(side="top", padx=10, pady=10)
            self.password_save_button.pack(side="top", padx=10, pady=10)
            self.password_cancel_button.pack(side="top", padx=10, pady=10)

    def SavePassword(self):
        username=self.parent.user.username
        old=self.old_password.get()
        new=self.new_password.get()
        new_hashed=self.parent.user.encode_pass(new)
        auth=self.parent.user.check_pass(old)
        if auth == 1:
            query="UPDATE accounts SET hashed_password=? WHERE username=?;"
            self.parent.database.cursor.execute(query, (new_hashed, username))
            self.parent.database.conn.commit()
        else:
            self.show_error("Authorization Error.\nCheck your password")
        self.password_edit_frame.pack_forget()
        self.old_password.pack_forget()
        self.old_password_label.pack_forget()
        self.new_password.pack_forget()
        self.new_password_label.pack_forget()
        self.password_save_button.pack_forget()
        self.password_cancel_button.pack_forget()

    def CancelPasswordEdit(self):
        self.password_edit_frame.pack_forget()
        self.old_password.pack_forget()
        self.old_password_label.pack_forget()
        self.new_password.pack_forget()
        self.new_password_label.pack_forget()
        self.password_save_button.pack_forget()
        self.password_cancel_button.pack_forget()

    def OpenRequestAdmin(self):
        self.request_admin_username.delete(0,'end')
        self.request_admin_password.delete(0,'end')
        self.request_admin_frame.pack(side="bottom", padx=10, pady=30)
        self.request_admin_username_label.pack(side="top", padx=10, pady=10)
        self.request_admin_username.pack(side="top", padx=10, pady=10)
        self.request_admin_password_label.pack(side="top", padx=10, pady=10)
        self.request_admin_password.pack(side="top", padx=10, pady=10)
        self.request_admin_button.pack(side="top", padx=10, pady=10)
        self.request_admin_cancel.pack(side="top", padx=10, pady=10)

    def CloseRequestAdmin(self):
        self.request_admin_frame.pack_forget()
        self.request_admin_username.pack_forget()
        self.request_admin_password.pack_forget()
        self.request_admin_button.pack_forget()
        self.request_admin_cancel.pack_forget()

    def LoginRequestAdmin(self):
        username=self.request_admin_username.get()
        password=self.request_admin_password.get()
        if not username or not password:
            self.show_error("Please enter login information")
        user=User(username, password, self.parent.database)
        auth=user.check_pass(password)
        if auth == -1:
            self.show_error("Password Incorrect")
        elif auth == -2:
            self.show_error("Username not recognized")
        elif auth == 1:
            self.add_account_button.configure(state="normal")
            self.delete_account_button.configure(state="normal")
            self.edit_account_password.configure(state="normal")
            self.edit_account_username.configure(state="normal")
            self.request_admin.pack_forget()
            self.no_admin_label.pack_forget()
            self.CloseRequestAdmin()

    def AddAccountOpen(self):
        if self.delete_account_frame.winfo_ismapped() or self.edit_username_frame.winfo_ismapped() or self.edit_password_frame.winfo_ismapped():
            return
        self.add_account_username.delete(0,'end')
        self.add_account_password.delete(0,'end')
        self.add_account_admin.deselect()
        self.add_account_frame.pack(side="bottom", padx=10, pady=30)
        self.add_account_username_label.pack(side="top", padx=10, pady=10)
        self.add_account_username.pack(side="top", padx=10, pady=10)
        self.add_account_password_label.pack(side="top", padx=10, pady=10)
        self.add_account_password.pack(side="top", padx=10, pady=10)
        self.add_account_admin.pack(side="top", padx=10, pady=10)
        self.add_account_add_button.pack(side="top", padx=10, pady=10)
        self.add_account_cancel.pack(side="top", padx=10, pady=10)

    def AddAccountClose(self):
        self.add_account_frame.pack_forget()
        self.add_account_username_label.pack_forget()
        self.add_account_username.pack_forget()
        self.add_account_password_label.pack_forget()
        self.add_account_password.pack_forget()
        self.add_account_admin.pack_forget()
        self.add_account_add_button.pack_forget()
        self.add_account_cancel.pack_forget()

    def AddAccount(self):
        username=self.add_account_username.get()
        password=self.add_account_password.get()
        admin=self.add_account_admin.get()
        if not username:
            self.show_error("Please enter a Username")
            return
        if not password:
            self.show_error("Please enter a Password")
            return
        query=f"SELECT EXISTS(SELECT 1 FROM accounts WHERE username LIKE '{username}')"
        print(query)
        self.parent.database.cursor.execute(query)
        present_p=self.parent.database.cursor.fetchone()[0]
        print(present_p)
        if present_p:
            self.show_error("Username already present.\nPlease enter a different Username")
            return
        user=User(username, password, self.parent.database)
        user.store_login(admin)
        self.AddAccountClose()
        
    def DeleteAccountOpen(self):
        if self.add_account_frame.winfo_ismapped() or self.edit_username_frame.winfo_ismapped() or self.edit_password_frame.winfo_ismapped():
            return
        self.delete_account_username.delete(0,'end')
        self.delete_account_confirm.deselect()
        self.delete_account_frame.pack(side="bottom", padx=10, pady=30)
        self.delete_account_username_label.pack(side="top", padx=10, pady=10)
        self.delete_account_username.pack(side="top", padx=10, pady=10)
        self.delete_account_confirm.pack(side="top", padx=10, pady=10)
        self.delete_account_delete_button.pack(side="top", padx=10, pady=10)
        self.delete_account_cancel_button.pack(side="top", padx=10, pady=10)
        
    def DeleteAccountClose(self):
        self.delete_account_frame.pack_forget()
        self.delete_account_username_label.pack_forget()
        self.delete_account_username.pack_forget()
        self.delete_account_confirm.pack_forget()
        self.delete_account_delete_button.pack_forget()
        self.delete_account_cancel_button.pack_forget()

    def DeleteAccount(self):
        username=self.delete_account_username.get()
        if not self.delete_account_confirm.get():
            self.show_error("Check the box if you\nreally want to delete\n the account")
            return
        if username.lower() == self.parent.user.username.lower():
            self.show_error("Cannot delete your own account")
            return
        query=f"SELECT EXISTS(SELECT 1 FROM accounts WHERE username LIKE '{username}')"
        self.parent.database.cursor.execute(query)
        if not self.parent.database.cursor.fetchone()[0]:
            self.show_error("Username not recognized")
            return
        query=f"DELETE FROM accounts WHERE username LIKE '{username}'"
        self.parent.database.cursor.execute(query)
        self.parent.database.conn.commit()
        self.DeleteAccountClose()

    def EditUsernameOpen(self):
        if self.delete_account_frame.winfo_ismapped() or self.add_account_frame.winfo_ismapped() or self.edit_password_frame.winfo_ismapped():
            return
        self.edit_username_new_username.delete(0,'end')
        self.edit_username_old_username.delete(0,'end')
        self.edit_username_frame.pack(side="bottom",padx=10, pady=30)
        self.edit_username_old_username_label.pack(side="top", padx=10, pady=10)
        self.edit_username_old_username.pack(side="top", padx=10, pady=10)
        self.edit_username_new_username_label.pack(side="top", padx=10, pady=10)
        self.edit_username_new_username.pack(side="top", padx=10, pady=10)
        self.edit_username_edit_button.pack(side="top", padx=10, pady=10)
        self.edit_username_cancel_button.pack(side="top", padx=10, pady=10)

    def EditUsernameClose(self):
        self.edit_username_frame.pack_forget()
        self.edit_username_old_username.pack_forget()
        self.edit_username_old_username_label.pack_forget()
        self.edit_username_new_username.pack_forget()
        self.edit_username_new_username_label.pack_forget()
        self.edit_username_edit_button.pack_forget()
        self.edit_username_cancel_button.pack_forget()
        
    def EditUsernameEdit(self):
        new=self.edit_username_new_username.get()
        old=self.edit_username_old_username.get()
        if not new or not old:
            self.show_error("Please enter username information")
            return
        query=f"SELECT EXISTS(SELECT 1 FROM accounts WHERE username LIKE '{old}')"
        self.parent.database.cursor.execute(query)
        exists_p=self.parent.database.cursor.fetchone()[0]
        if not exists_p:
            self.show_error("Username not recognized.")
            return
        query=f"UPDATE accounts SET username='{new}' WHERE username='{old}'"
        self.parent.database.cursor.execute(query)
        self.parent.database.conn.commit()

    def EditPasswordOpen(self):
        if self.delete_account_frame.winfo_ismapped() or self.add_account_frame.winfo_ismapped() or self.edit_username_frame.winfo_ismapped():
            return
        self.edit_password_frame.pack(side="bottom", padx=10, pady=10)
        self.edit_password_username_label.pack(side="top", padx=10, pady=10)
        self.edit_password_username.pack(side="top", padx=10, pady=10)
        self.edit_password_password_label.pack(side="top", padx=10, pady=10)
        self.edit_password_password.pack(side="top", padx=10, pady=10)
        self.edit_password_edit_button.pack(side="top", padx=10, pady=10)
        self.edit_password_cancel.pack(side="top", padx=10, pady=10)

    def EditPasswordClose(self):
        self.edit_password_frame.pack_forget()
        self.edit_password_username_label.pack_forget()
        self.edit_password_username.pack_forget()
        self.edit_password_password_label.pack_forget()
        self.edit_password_password.pack_forget()
        self.edit_password_edit_button.pack_forget()
        self.edit_password_cancel.pack_forget()
    
    def EditPassword(self):
        username=self.edit_password_username.get()
        password=self.edit_password_password.get()
        if not username or not password:
            self.show_error("Please enter account information")
            return
        query=f"SELECT EXISTS(SELECT 1 FROM accounts WHERE username LIKE '{username}')"
        self.parent.database.cursor.execute(query)
        exists_p=self.parent.database.cursor.fetchone()[0]
        if not exists_p:
            self.show_error("Username not recognized.")
            return
        new_hashed=self.parent.user.encode_pass(password)
        query="UPDATE accounts SET hashed_password=? WHERE username=?"
        self.parent.database.cursor.execute(query, (new_hashed, username))
        self.parent.database.conn.commit()
        self.EditPasswordClose()
