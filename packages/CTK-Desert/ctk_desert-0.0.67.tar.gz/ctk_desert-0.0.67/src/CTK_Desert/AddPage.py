import customtkinter as ctk
from .Core import userChest as Chest
from .Page_base_model import Page_BM
from .Theme import *
from .utils import hvr_clr_g, change_pixel_color
from .Widgits import C_Widgits
from .Theme import *
import os
from PIL import Image
import numpy as np
from tkinter import filedialog as fd

# don't ever pack the frame, it will be packed in the Tab_Page_Frame.py
class AddPage(Page_BM):
    def __init__(self):
        super().__init__(start_func=self.on_start, pick_func=self.on_pick, update_func=self.on_update, leave_func=self.on_leave)
        self.menu_page_frame = Chest.Manager
        self.frame = self.Scrollable_frame # Parent of all children in this page
        self.frame.configure(fg_color = (hvr_clr_g(LIGHT_MODE["background"], "l"), hvr_clr_g(DARK_MODE["background"], "d")))
        self.mode = ctk.get_appearance_mode()
        self.frame_clr = self.get_scrframe_color()
        self.pages_path = Chest.userPagesDirectory
        self.icon_names = ["_d_s", "_d", "_l_s", "_l"]
        self.icon_path = None

        self.ws_label = ctk.CTkLabel(self.frame, text="New", font=(FONT_B, 40))
        self.ws_label.pack(fill="x", padx=20, pady=20)

        self.c_wgts = C_Widgits(self, self.frame)
        
        self.content_sec   =    self.c_wgts.section(padx=60)
        self.page_name     =    self.c_wgts.section_unit(self.content_sec, title="Page Name", widget="entry", default="Pick a name")
        self.icon_path_btn =    self.c_wgts.section_unit(self.content_sec, title="Icon Path", widget="button", default="Pick an icon", command= self.get_icon_path)
        self.scrollableCBVar = ctk.BooleanVar(value=True)
        self.scrollableCB  =    self.c_wgts.section_unit(self.content_sec, title="Scrollable", widget="checkbox", default=self.scrollableCBVar)

        self.confirmation_sec =    self.c_wgts.section(pady=5)
        self.confirmation     =    self.c_wgts.section_unit(self.confirmation_sec, title="", widget="button", default="Create Page", command= self.create_page)
        self.confirmation.winfo_children()[-1].configure(height=50, font=(FONT_B, 17))
        self.Back            =    self.c_wgts.section_unit(self.confirmation, title="", widget="button", default="Back", command= lambda: Chest.Return_SubPage("Workspace", "AddPage"))
        self.Back.winfo_children()[-1].configure(height=50, font=(FONT_B, 17), fg_color = (hvr_clr_g(LIGHT_MODE["primary"], "l", -20), hvr_clr_g(DARK_MODE["primary"], "d", -20)), hover_color = (LIGHT_MODE["primary"], DARK_MODE["primary"]))

        

    def on_start(self):
        pass

    def on_pick(self):
        pass

    def on_update(self):
        pass

    def on_leave(self, event):
        return True
    
    def tool_menu(self):
        self.tool_p_f = self.menu_page_frame.apps_frame
        self.tools_f = ctk.CTkFrame(self.tool_p_f, fg_color="transparent")

        reload_image_l = change_pixel_color(r"C:\Users\Morad\Downloads\icons8-reload-64.png", color=ICONS["_l"], return_img=True)
        reload_image_d = change_pixel_color(r"C:\Users\Morad\Downloads\icons8-reload-64.png", color=ICONS["_d"], return_img=True)
        reload_image = ctk.CTkImage(reload_image_l, reload_image_d, size=(45, 45))
        ctk.CTkButton(self.tools_f, text="", fg_color="transparent", hover_color=self.frame_clr, image=reload_image, 
                      command=lambda: Chest.reload_page("Workspace.AddPage"), ).pack()
        
        return self.tools_f

    def get_icon_path(self):
        filetypes = ( ('images', '*.png'), ('All files', '*.*') )
        f = fd.askopenfile(filetypes=filetypes, title="Pick an icon")
        self.icon_path = f.name if f else None

    def create_page(self):
        file_name = self.page_name.gval()         # get field data (page name)
        if not (file_name == "" or self.icon_path == None):

            with open (os.path.join(os.path.dirname(__file__), "Page_EX_Code.py"), 'r') as file:    # open the example code file
                data = file.read()
            #######################################################################
            data = data.replace("CUNAME__C", file_name)  
            
            # module_names = [file[:-3] for file in os.listdir(self.pages_path) if file.endswith('.py') and file != '__init__.py']       # replace the class name with the page name
            # data = data.replace('"PAGE_Num__": 0', f'"PAGE_Num__": {len(module_names)+1}')                                             # replace the class name with the page name

            data = data.replace(r'"SCRL_VAL__"', str(self.scrollableCBVar.get()))
            
            #######################################################################
            with open (os.path.join(self.pages_path, f"{file_name}.py"), 'w') as file:              # create a new file with the page name
                file.write(data)

            self.change_pixel_color(file_name) # get the image path from the dialog box, and the target color from Theme file

            self.menu_page_frame.new_page_constructor(file_name)        # Calling a func in the tab page frame to add the new page to the application
        
    def change_pixel_color(self, file_name):
        # Open the image and convert it to RGBA mode
        img = Image.open(self.icon_path).convert("RGBA")

        # Convert the image to a NumPy array
        img_array = np.array(img)

        for i in self.icon_names:
            # Apply the target color to non-transparent pixels
            img_array[img_array[..., 3] != 0, :3] = ICONS[i]

            # Create a new image from the modified array
            modified_img = Image.fromarray(img_array, "RGBA")

            # Save the modified image
            modified_img.save(os.path.join(os.path.dirname(self.pages_path), "Images", f"{file_name.lower()}{i}.png"))
            
    