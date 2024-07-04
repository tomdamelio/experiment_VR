# Settings and experimental parameters to config specific experimental design values
# All values that need modification should be set here. 
# In order not to change original experiment code


class ExperimentParameters:
    def __init__(self):

        ##########################################################################
        ########                        SETTINGS                          ########
        ##########################################################################
        # self.results_folder='./results'
        # run in windows and psychopy standalon
        self.results_folder=r'C:\Users\Cocudata\experiment_VR\results'
        self.exp_name='non_immersive'  

        ##########################################################################
        ########                     SCREEN PARAMS                        ########
        ##########################################################################

        self.display_size= (1920, 1080)  # (1920 1080) # in pixels
        # self.display_size= (1920, 1080) # in pixels
        self.window_units = 'cm'
        self.background_color = '#282828'

        self.fullscreen=True
        if not self.fullscreen:
            self.allowGUI = True
        else:
            self.allowGUI = False




        ##########################################################################
        ########                   EXERIMENTAL PARAMS                     ########
        ##########################################################################
        self.text_height=1
        
        self.text_color = '#F8F8F8'
        
        self.kanizsa_color = '#888888'
        
        
        ##########################################################################
        ########                       TASK PARAMS                        ########
        ##########################################################################        
        self.stim_height = 4

        # self.fixation_time=1

        self.iti = 2
        
        self.n_blocks = 2
