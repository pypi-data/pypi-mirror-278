

from . import StepView as sv
from . import StaticParameterView as spv
from . import CalibrationParametersView as cpv
from . import OptimalParameterView as opv

import customtkinter

def create_tab(self, tab):
    
    tab.grid_columnconfigure(0, weight=8)
    tab.grid_columnconfigure(1, weight=1)
    tab.grid_rowconfigure(0, weight=1)
    
    self.paramtabview = customtkinter.CTkTabview(tab, bg_color="transparent", fg_color="transparent")
    self.paramtabview.grid(row=0, column=1, padx=(0, 0), pady=(10, 10), sticky="nsew")
    
    tab1 = "Static"
    tab2 = "Hyperparameters"
    tab3 = "Optimal"
    self.paramtabview.add(tab1)
    self.paramtabview.add(tab2)
    self.paramtabview.add(tab3)
    
    self.paramtabview.tab(tab1).grid_columnconfigure(0, weight=1)
    self.paramtabview.tab(tab1).grid_rowconfigure(0, weight=1)
    
    self.paramtabview.tab(tab2).grid_columnconfigure(0, weight=1)
    self.paramtabview.tab(tab2).grid_rowconfigure(0, weight=1)
    
    self.paramtabview.tab(tab3).grid_columnconfigure(0, weight=1)
    self.paramtabview.tab(tab3).grid_rowconfigure(0, weight=1)
    
    self.static_param_frame = spv.StaticParameterView(self.paramtabview.tab(tab1), option_manager=self.option_manager)
    self.static_param_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")
    self.static_param_frame.grid_columnconfigure(0, weight=1)
    self.static_param_frame.grid_rowconfigure(0, weight=1)
    
    self.calib_param_frame = cpv.CalibrationParametersView(self.paramtabview.tab(tab2), option_manager=self.option_manager)
    self.calib_param_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")
    self.calib_param_frame.grid_columnconfigure(0, weight=1)
    self.calib_param_frame.grid_rowconfigure(0, weight=1)
    
    self.optimal_param_frame = opv.OptimalParameterView(self.paramtabview.tab(tab3), option_manager=self.option_manager)
    self.optimal_param_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")
    self.optimal_param_frame.grid_columnconfigure(0, weight=1)
    self.optimal_param_frame.grid_rowconfigure(0, weight=1)
    
    self.steps_frame = sv.StepView(tab, label_text="Group Editor", option_manager=self.option_manager)
    self.steps_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew")
    self.steps_frame.grid_columnconfigure(0, weight=1)
    self.steps_frame.grid_rowconfigure(0, weight=1)
    