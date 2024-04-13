import customtkinter as ctk
from Screen import Screen

class Settings(Screen):
    def __init__(self, main_frame, ParentGUI):
        self.parent=ParentGUI
        self.main_frame=main_frame
        self.config=self.parent.config

        if self.config.appearance("color_mode") == "light":
            self.color_string=" - Light "
        elif self.config.appearance("color_mode") == "dark":
            self.color_string=" - Dark"

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
        self.new_username=ctk.CTkEntry(self.username_edit_frame, placeholder_text="New Username")
        self.username_save_button=ctk.CTkButton(self.username_edit_frame, text="Save Username")
        self.username_cancel_button=ctk.CTkButton(self.username_edit_frame, text="Cancel")

        # Edit Password Frame
        self.password_edit_frame=ctk.CTkFrame(self.user_frame)
        self.old_password=ctk.CTkEntry(self.password_edit_frame, placeholder_text="Old Password")
        self.new_password=ctk.CTkEntry(self.password_edit_frame, placeholder_text="New Password")
        self.password_save_button=ctk.CTkButton(self.password_edit_frame, text="Save Password")
        self.password_cancel_button=ctk.CTkButton(self.password_edit_frame, text="Cancel")
        
        
        
        self.Admin_frame=ctk.CTkFrame(self.main_frame, width=300)#, fg_color=("#d3d3d3", "#000000"))
        self.Admin_frame.pack(side="left", fill="both", expand=True, pady=10)
        self.admin_frame_label=ctk.CTkLabel(self.Admin_frame, text="Admin Settings", font=self.headline_font)
        self.admin_frame_label.pack(side="top", padx=10, pady=30)
        
        self.System_frame=ctk.CTkFrame(self.main_frame, width=400)#, fg_colot=("#d3d3d3", "#000000"))
        self.System_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.system_frame_label=ctk.CTkLabel(self.System_frame, text="System Settings", font=self.headline_font)
        self.system_frame_label.pack(side="top", padx=10, pady=30)


    def ChangeColorMode(self):
        raise NotImplementedError("Color Function Not Written")

    def EditUsername(self):
        raise NotImplementedError("Edit Function Not written")

    def SaveUsername(self):
        raise NotImplementedError("Save Function Not written")

    def CancelUsernameEdit(self):
        raise NotImplementedError("Cancel not written")

    def EditUserPassword(self):
        raise NotImplementedError("Edit Function Not written")

    def SavePassword(self):
        raise NotImplementedError("Save Function Not written")

    def CancelPasswordEdit(self):
        raise NotImplementedError("Cance not written")
