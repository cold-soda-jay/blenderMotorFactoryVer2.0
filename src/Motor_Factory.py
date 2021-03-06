import bpy
import os
from bpy.props import *
from bpy_extras import object_utils
from . import motor as mt
from bpy_extras.object_utils import AddObjectHelper




#from math import *


class Motor_Factory_Operator(bpy.types.Operator,AddObjectHelper):
    
    #Set Genera information
    bl_idname = "mesh.add_motor"
    bl_label = "Motor Property"
    bl_options = {'REGISTER', 'UNDO', 'PRESET'}
    bl_description = "Add new motor"
    MAX_INPUT_NUMBER = 10

    motor : BoolProperty(name = "Motor",
                default = True,
                description = "New motor")

    change : BoolProperty(name = "Change",
                default = False,
                description = "Change motor")
    init_x = 0
    init_y = 0
    init_z = 0
    id_Nr = 0

    mf_Lower_Gear_XYZ = []
    mf_Lower_Gear_ContainerDia = 0
    mf_Lower_Gear_GearDia_Small = 0
    mf_Lower_Gear_GearDia_Large = 0
    mf_Lower_Gear_HoleDia = 0
    mf_Upper_Gear_XYZ = []
    mf_Upper_Gear_Position = 0
    mf_Upper_Gear_ContainerDia = 0
    mf_Upper_Gear_GearDia = 0
    mf_Upper_Gear_HoleDia = 0

    MotorParameters = [
        "mf_Top_Type",
        "mf_Extension_Type_A",
        "mf_Extension_Type_B",
        "mf_Gear_Orientation_1",
        "mf_Gear_Orientation_2",
        "mf_Mirror",
        "mf_Color_Render",

        "mf_corrosion_Render",
        "mf_corrosion_Type_Bolt",
        "mf_corrosion_Percent_Bolt",
        "mf_corrosion_Type_Bottom",
        "mf_corrosion_Percent_Bottom",

        "mf_Bottom_Length",
        "mf_Sub_Bottom_Length",
        "mf_Lower_Gear_Dia",
        "mf_Lower_Gear_Position",
        "mf_Upper_Gear_Dia",

        "mf_Bit_Type",
        "mf_Bolt_Orientation",
        "mf_Lower_Gear_Bolt_Random",
        "mf_Lower_Gear_Bolt_Position_1",
        "mf_Lower_Gear_Bolt_Position_2", 
        
        "mf_Upper_Bolt_Nummber",
        "mf_Upper_Gear_Bolt_Random",
        "mf_Upper_Gear_Bolt_Position_1_1",
        "mf_Upper_Gear_Bolt_Position_1_2",
        "mf_Upper_Gear_Bolt_Position_1_3",
        "mf_Teeth_Inclination",
        "mf_Upper_Gear_Bolt_Position_2_1",
        "mf_Upper_Gear_Bolt_Position_2_2",
        "mf_Upper_Gear_Bolt_Position_3",

        "mf_Type_B_Height_1",
        "mf_Type_B_Height_2", 
        "mf_Gear_Bolt_Random_B",
        "mf_Gear_Bolt_Nummber_B",
        "mf_Gear_Bolt_Position_B_1",
        "mf_Gear_Bolt_Position_B_2",
        "mf_Gear_Bolt_Position_B_3",
        "mf_Gear_Bolt_Right_B",
        "temp_save",
        "save_path",
        "test",
        "mf_Combine",

        ]
    
    CsvParameters = [
        "mf_Top_Type",
        "mf_Extension_Type_A",
        "mf_Extension_Type_B",
        "mf_Gear_Orientation_1",
        "mf_Gear_Orientation_2",
        "mf_Mirror",
        "mf_Color_Render",

        "mf_corrosion_Render",
        "mf_corrosion_Type_Bolt",
        "mf_corrosion_Percent_Bolt",
        "mf_corrosion_Type_Bottom",
        "mf_corrosion_Percent_Bottom",

        "mf_Bottom_Length",
        "mf_Sub_Bottom_Length",
        
        "mf_Lower_Gear_Position",
        "mf_Lower_Gear_XYZ",
        "mf_Lower_Gear_Dia",
        "mf_Lower_Gear_ContainerDia",
        "mf_Lower_Gear_GearDia_Small",
        "mf_Lower_Gear_GearDia_Large",
        "mf_Lower_Gear_HoleDia",
        
        "mf_Upper_Gear_Position",
        "mf_Upper_Gear_XYZ",
        "mf_Upper_Gear_Dia",
        "mf_Upper_Gear_ContainerDia",
        "mf_Upper_Gear_GearDia",
        "mf_Upper_Gear_HoleDia",

        "mf_Bit_Type",
        "mf_Bolt_Orientation",
        "mf_Lower_Gear_Bolt_Random",
        "mf_Lower_Gear_Bolt_Position_1",
        "mf_Lower_Gear_Bolt_Position_2", 
        "mf_Upper_Bolt_Nummber",
        "mf_Upper_Gear_Bolt_Random",
        "mf_Upper_Gear_Bolt_Position_1",
        "mf_Upper_Gear_Bolt_Position_2",
        "mf_Upper_Gear_Bolt_Position_3",
        "mf_Type_B_Height_1",
        "mf_Type_B_Height_2", 
        "mf_Gear_Bolt_Random_B",
        "mf_Gear_Bolt_Nummber_B",
        "mf_Gear_Bolt_Position_B_1",
        "mf_Gear_Bolt_Position_B_2",
        "mf_Gear_Bolt_Position_B_3",
        "mf_Gear_Bolt_Right_B",
        "mf_Teeth_Inclination",

        ]
    #Create genera types and Variables

    ################### General ##################################
    #Head Types 
    Head_Type_List = [('mf_Top_Type_A','Type A (Two gears)','Type A'),
                        ('mf_Top_Type_B','Type B (One gears)','Type B')]
    mf_Top_Type = EnumProperty( attr='mf_Top_Type',
            name='Type',
            description='Choose the type of Motor you would like',
            items = Head_Type_List, default = 'mf_Top_Type_A')
    
    #Extension zone Types
    
    Extention_Type_List_A = [('mf_Extension_Type_1','Type 1','Type 1'),
                 ('mf_Extension_Type_2','Type 2','Type 2'),                 
                 ('mf_None','None','None') 
                 ]
    mf_Extension_Type_A = EnumProperty( attr='mf_Extension_Type',
            name='Extension Area Type',
            description='Choose the type of extension area you would like',
            items = Extention_Type_List_A, default = 'mf_Extension_Type_1')
    
    Extention_Type_List_B = [('mf_Extension_Type_1','Type 1','Type 1'),                                 
                 ('mf_None','None','None') 
                 ]
    mf_Extension_Type_B = EnumProperty( attr='mf_Extension_Type',
            name='Extension Area Type',
            description='Choose the type of extension area you would like',
            items = Extention_Type_List_B, default = 'mf_Extension_Type_1')


   
    # Gear Orientation
    Orientation_List_Type_2 = [
                ('r90','90','90'),             
                ('r180','180','180'),
                ('r270','270','270')
        ]

    Orientation_List_Type_1 = [
                ('r0','0','0'),
                ('r90','90','90'),             
                ('r180','180','180'),
                ('r270','270','270')
        ]

    mf_Gear_Orientation_1 = EnumProperty( attr='mf_Gear_Orientation',
            name='Gear Rotation',
            description='Rotation of gears and extension zone',
            items = Orientation_List_Type_1, default = 'r0')   

    mf_Gear_Orientation_2 = EnumProperty( attr='mf_Gear_Orientation',
            name='Gear Rotation',
            description='Rotation of gears and extension zone',
            items = Orientation_List_Type_2, default = 'r270')

    mf_Mirror : BoolProperty(name = "Mirror",
                default = False,
                description = "Mirror the gears")

    ########################## Set color rendering option ############################
    mf_Color_Render : BoolProperty(name = "Color Render",
                default = False,
                description = "Render color or not")

    corrosion_Type = [
                ('None', 'None', 'None'),
                ('Rust 1','Rust 1','Rust 1'),
                ('Rust 2','Rust 2','Rust 2'),
                ('Rust 3','Rust 3','Rust 3'),
                ('Rust 4','Rust 4','Rust 4'),
                ('Rust 5','Rust 5','Rust 5'),
                ('Rust 6','Rust 6','Rust 6'),
                ('Rust 7','Rust 7','Rust 7'),
                ('Rust 8','Rust 8','Rust 8'),
                ('Rust 9','Rust 9','Rust 9'),
        ]

    mf_corrosion_Render : BoolProperty(name = "corrosion",
                default = True,
                description = "Render corrosion or not")

    mf_corrosion_Type_Bolt = EnumProperty( attr='mf_corrosion_Type_Bolt',
            name='Bolt',
            description='Type of corrosions of bolt',
            items = corrosion_Type, default = 'Rust 1')   

    mf_corrosion_Percent_Bolt = FloatProperty(attr='mf_corrosion_Percent_Bolt',
            name='corrosion Percent of bolt', default = 20,
            min =0, max = 100, 
            description='corrosion Percent of bolt')

    mf_corrosion_Type_Bottom = EnumProperty( attr='mf_corrosion_Type_Bottom',
            name='Bottom',
            description='Type of corrosions of bottom',
            items = corrosion_Type, default = 'Rust 1')   

    mf_corrosion_Percent_Bottom = FloatProperty(attr='mf_corrosion_Percent_Bottom',
            name='corrosion Percent of bottom', default = 40,
            min =0, max = 100, 
            description='corrosion Percent of bottom')

    ################## Bottom ########################################
    #Bottom Length      
    mf_Bottom_Length = FloatProperty(attr='mf_Bottom_Length',
            name='Bottom Length', default = 6.8,
            min = 6.2, soft_min = 0, max = 8.2, 
            description='Length of the Bottom')

    #Sub Bottom length      
    mf_Sub_Bottom_Length = FloatProperty(attr='mf_Sub_Bottom_Length',
            name='Sub Bottom Length', default = 1.2,
            min =0.6, soft_min = 0.1, max = 2, 
            description='Length of the Sub Bottom')

    mf_Teeth_Inclination = FloatProperty(attr='mf_Teeth_Inclination',
            name='Teeth Inclination', default = 10,
            min =-20, max = 20, 
            description='Teeth Inclination of gears')                
    

    ###################### Lower Gears for type A and B ########################################
    mf_Lower_Gear_Dia = FloatProperty(attr='mf_Lower_Gear_Dia',
        name='Lower Gear Dia', default = 4,
        min = 3.5, soft_min = 0, max = 4.5, 
        description='Diameter of lower Gear')

    mf_Lower_Gear_Position = FloatProperty(attr='mf_Lower_Gear_Position',
        name='Lower Gear Position', default = 3.6,
        min = 3.6, soft_min = 0, max = 4.2, 
        description='Position of lower Gear in middel axe respect to the top of bottom part(mf_Sub_Bottom_Length + mf_Bottom_Length)')


    mf_Lower_Gear_Bolt_Random : BoolProperty(name = "Random Bolt Position of lower gear", 
                default = False,
                description = "Random Bolt Rotation")

    mf_Lower_Gear_Bolt_Position_1 = IntProperty(attr='mf_Lower_Gear_Bolt_Position',
        name='Position of bolt 1 on lower gear', default = 200,
        min = 190, max = 230, step=5,
        description='Position of bolts on lower gear')

    mf_Lower_Gear_Bolt_Position_2 = IntProperty(attr='mf_Lower_Gear_Bolt_Position',
        name='Position of bolts on lower gear', default = 320,
        min = 320, max = 350,  step=5,
        description='Position of bolt 2 on lower gear')
    
    #################################### Gear option for Type B ###########################################
    mf_Gear_Bolt_Random_B : BoolProperty(name = "Random Bolt Position ", 
                default = False,
                description = "Random Bolt Rotation")


    upper_Gear_Bolt_Random = [('2','2','2'),
                    ('3','3','3')]
    mf_Gear_Bolt_Nummber_B = EnumProperty( attr='mf_Gear_Bolt_Nummber_B',
            name='Number of Bolts',
            description='Number of Bolts around Gear',
            items = upper_Gear_Bolt_Random, default = '2')

    mf_Gear_Bolt_Position_B_1 = IntProperty(attr='mf_Gear_Bolt_Position_B_1',
        name='Position of bolts on gear', default = 215,
        min = 210, max = 225, step=1,
        description='Position of bolt 1 on gear')

    mf_Gear_Bolt_Position_B_2 = IntProperty(attr='mf_Gear_Bolt_Position_B_2',
        name='Position of bolts on gear', default = 90,
        min = 70, max =110,  
        description='Position of bolt 2 on gear')
    
    mf_Gear_Bolt_Position_B_3 = IntProperty(attr='mf_Gear_Bolt_Position_B_3',
        name='Position of bolts on gear', default = 180,
        min = 130, max = 190,  step=1,
        description='Position of bolt 2 on gear')
    
    mf_Type_B_Height_1 =   FloatProperty(attr='mf_Type_B_Height_1',
        name='Height of Extension left', default = 7,
        min = 6.3, soft_min = 0, max = 7.5, 
        description='Height of Extension left relative to the top of the bottom part (mf_Sub_Bottom_Length + mf_Bottom_Length)') 
    
    
    mf_Type_B_Height_2 =   FloatProperty(attr='mf_Type_B_Height_2',
        name='Height of Extension right', default =3.5,
        min = 3, soft_min = 0, max = 6, 
        description='Height of Extension right relative to the top of the bottom part (mf_Sub_Bottom_Length + mf_Bottom_Length)') 
    
    mf_Gear_Bolt_Right_B =   FloatProperty(attr='mf_Gear_Bolt_Right_B',
        name='Position of bolt at right', default =2.5,
        min = 1.7, soft_min = 0, max = 4, 
        description='Position of bolt at right relative to the top of the bottom part (mf_Sub_Bottom_Length + mf_Bottom_Length) ')

    ########################## Upper part Type A ###############################

    mf_Upper_Gear_Dia = FloatProperty(attr='mf_Upper_Gear_Dia',
        name='Upper Gear Dia', default = 5.5,
        min = 5, soft_min = 0, max = 6.5, 
        description='Diameter of upper Gear')

    #Bolt on large gear
    
    upper_Gear_Bolt_Random = [('1','1','1'),
                    ('2','2','2'),
                    ('3','3','3')]
    mf_Upper_Bolt_Nummber = EnumProperty( attr='mf_Upper_Bolt_Nummber',
            name='Number of Bolts',
            description='Number of Bolts around upper Gear',
            items = upper_Gear_Bolt_Random, default = '2')


    mf_Upper_Gear_Bolt_Random : BoolProperty(name = "Random Bolt Position of upper gear",
                default = False,
                description = "Random Bolt Rotation")

    mf_Combine : BoolProperty(name = "Combine all parts",
                default = True,
                description = "Random Bolt Rotation")
    
    mf_Upper_Gear_Bolt_Position_1_1 = IntProperty(attr='mf_Upper_Gear_Bolt_Position_1',
        name='Position of bolts on large gear', default = 13,
        min = 0, max = 210, step=1,
        description='Position of bolts on large gear')
    
    mf_Upper_Gear_Bolt_Position_1_2 = IntProperty(attr='mf_Upper_Gear_Bolt_Position_1',
        name='Position of bolts on large gear', default = 13,
        min = 0, max = 100, step=1,
        description='Position of bolts on large gear')
    
    mf_Upper_Gear_Bolt_Position_1_3 = IntProperty(attr='mf_Upper_Gear_Bolt_Position_1',
        name='Position of bolts on large gear', default = 13,
        min = 0, max = 65, step=1,
        description='Position of bolts on large gear')
    

    mf_Upper_Gear_Bolt_Position_2_1 = IntProperty(attr='mf_Upper_Gear_Bolt_Position_2',
        name='Position of bolts on large gear', default = 100,
        min = 110, max = 210, step=1,
        description='Position of bolts on large gear')    
    mf_Upper_Gear_Bolt_Position_2_2 = IntProperty(attr='mf_Upper_Gear_Bolt_Position_2',
        name='Position of bolts on large gear', default = 100,
        min = 75, max = 135, step=1,
        description='Position of bolts on large gear')
    

    mf_Upper_Gear_Bolt_Position_3 = IntProperty(attr='mf_Upper_Gear_Bolt_Position_3',
        name='Position of bolts on large gear', default =200,
        min = 145, max = 210, step=1,
        description='Position of bolts on large gear')


    ###################### Bolts ############################################

    bolt_orientation_list = [('mf_all_same', 'All Same','All Same'),
                            ('mf_all_random', 'All Random', 'All Random')]
    mf_Bolt_Orientation = EnumProperty( attr='mf_Bolt_Orientation',
            name='Bolt Ortientation',
            description='Orientation of bolts',
            items = bolt_orientation_list, default = 'mf_all_same')
    
    
    #Bit Types
    Bit_Type_List = [('mf_Bit_Torx','Torx','Torx Bit Type'),
                    ('mf_Bit_Slot','Slot','Slot Bit Type'),
                    ('mf_Bit_Cross','Cross','Cross Bit Type'),
                    ('mf_Bit_Allen','Allen','Allen Bit Type')]
    mf_Bit_Type = EnumProperty( attr='mf_Bit_Type',
            name='Bit Type',
            description='Choose the type of bit to you would like',
            items = Bit_Type_List, default = 'mf_Bit_Torx')
    
    ##################### Svae path #####################


    temp_save : BoolProperty(name = "Save the module ", 
                default = True,
                description = "Save the module")
    
    save_path = StringProperty(name = "Save Path",
                default = "None", maxlen=4096,
                description = "Save the modell")     

    test : BoolProperty(name = "Save the module ", 
    default = False,
    description = "Save the module")   
    
    mf_Upper_Gear_Bolt_Position_1 = 0

    mf_Upper_Gear_Bolt_Position_2 = 0

    def draw(self, context):
        """
        Define the contex menu

        """
        layout = self.layout
        col = layout.column()
        
        col.label(text="General")
        col.prop(self, 'mf_Top_Type')
        if self.mf_Top_Type == "mf_Top_Type_A":  
            col.prop(self, 'mf_Extension_Type_A')
            if self.mf_Extension_Type_A == 'mf_Extension_Type_1':
                col.prop(self, 'mf_Gear_Orientation_1')        
            elif self.mf_Extension_Type_A == 'mf_Extension_Type_2':
                col.prop(self, 'mf_Gear_Orientation_2') 
            else:
                col.prop(self, 'mf_Gear_Orientation_1')      
        elif self.mf_Top_Type == "mf_Top_Type_B":
            col.prop(self, 'mf_Extension_Type_B')
            col.prop(self, 'mf_Gear_Orientation_1')
        
      
        col.prop(self, 'mf_Mirror')
        col.prop(self, 'mf_Teeth_Inclination')
        col.prop(self, 'mf_Color_Render')
        if self.mf_Color_Render:
            #col.prop(self, "mf_corrosion_Render")
            #if self.mf_corrosion_Render:
            col.label(text="corrosion")
            col.prop(self, 'mf_corrosion_Type_Bolt')
            col.prop(self, 'mf_corrosion_Percent_Bolt')
            col.prop(self, 'mf_corrosion_Type_Bottom')
            col.prop(self, 'mf_corrosion_Percent_Bottom')

       

        col.label(text="Bottom")
        col.prop(self, 'mf_Bottom_Length') 
        col.prop(self, 'mf_Sub_Bottom_Length')

        col.label(text="Gears")
        col.prop(self, 'mf_Lower_Gear_Dia') 
        col.prop(self, 'mf_Lower_Gear_Position')
        if self.mf_Top_Type == "mf_Top_Type_A":  
            col.prop(self, 'mf_Upper_Gear_Dia')    
        elif  self.mf_Top_Type == "mf_Top_Type_B":  
            col.prop(self, 'mf_Type_B_Height_1')
            col.prop(self, 'mf_Type_B_Height_2')

        col.label(text="Bolts Type")
        col.prop(self, 'mf_Bit_Type')
        col.prop(self, 'mf_Bolt_Orientation')      

        if self.mf_Top_Type == "mf_Top_Type_A":    

            col.label(text="Bolts Position around lower gear")

            col.prop(self, 'mf_Lower_Gear_Bolt_Random')    
            if not self.mf_Lower_Gear_Bolt_Random: 
                col.prop(self, 'mf_Lower_Gear_Bolt_Position_1')
                col.prop(self, 'mf_Lower_Gear_Bolt_Position_2')
            col.label(text="Bolts Position around upper gear")

            col.prop(self, 'mf_Upper_Bolt_Nummber')
            col.prop(self, 'mf_Upper_Gear_Bolt_Random')
            if not self.mf_Upper_Gear_Bolt_Random:
                if self.mf_Upper_Bolt_Nummber == '1':
                    col.prop(self, 'mf_Upper_Gear_Bolt_Position_1_1') 
                elif self.mf_Upper_Bolt_Nummber == '2':
                    col.prop(self, 'mf_Upper_Gear_Bolt_Position_1_2') 
                    col.prop(self, 'mf_Upper_Gear_Bolt_Position_2_1') 

                elif self.mf_Upper_Bolt_Nummber == '3':
                    col.prop(self, 'mf_Upper_Gear_Bolt_Position_1_3') 
                    col.prop(self, 'mf_Upper_Gear_Bolt_Position_2_2')
                    col.prop(self, 'mf_Upper_Gear_Bolt_Position_3')

        elif self.mf_Top_Type == "mf_Top_Type_B":
            col.label(text="Bolts Position around gear B")
            col.prop(self, 'mf_Gear_Bolt_Right_B')

            if self.mf_Extension_Type_B == "mf_None":
                col.prop(self, 'mf_Gear_Bolt_Nummber_B')                        
            col.prop(self, 'mf_Gear_Bolt_Random_B')
            if not self.mf_Gear_Bolt_Random_B:
                col.prop(self, 'mf_Gear_Bolt_Position_B_1')
                col.prop(self, 'mf_Gear_Bolt_Position_B_2')
                if self.mf_Extension_Type_B == "mf_None" and self.mf_Gear_Bolt_Nummber_B == '3':
                    col.prop(self, 'mf_Gear_Bolt_Position_B_3')
        col.prop(self, 'mf_Combine')
        #col.prop(self, 'temp_save')
        #if self.temp_save:
        col.prop(self, 'save_path')

        col.separator()


    @classmethod
    def poll(cls, context):

        return context.scene is not None

    def execute(self, context):
        if  context.selected_objects != [] and context.active_object and \
            ('motor_id' in context.active_object.keys()):  
            obj = context.active_object
            if self.change:
                self.change = False
                
            else:
                loc_list = self.get_old_loc(context)
                x = context.active_object.location.x
                y = context.active_object.location.y
                z = context.active_object.location.z       
                self.delete_motor(context)
                obj = self.create_motor()
                self.move_motor(obj, loc_list)
                if self.mf_Combine:
                    obj.location.x=x
                    obj.location.y=y
                    obj.location.z=z
            
        else:
            obj = self.create_motor()    
            
        obj.data["Motor"] = True
        obj.data["change"] = False
        for prm in self.MotorParameters:
            obj.data[prm] = getattr(self, prm)
        
        return {'FINISHED'}

    def invoke(self, context, event):
        self.execute(context)
        return {'FINISHED'}

    def create_motor(self):
        """Create motor

        Returns:
            Motor Object
        """

        # Check if the model should be svaed
        if self.save_path == "None":
            pass
        else:  
            self.save_path = self.save_path.replace("\\","/")
            if not self.save_path.endswith('/'):
                self.save_path += '/'  
            # Make dir when not exist   
            try:
                os.mkdir(self.save_path)
            except:
                pass        
                  
            self.id_Nr = len([x for x in os.listdir(self.save_path) if "Motor_" in x])+1
            path_of_folder = self.save_path + "Motor_%04d/"%self.id_Nr
            try:
                os.mkdir(path_of_folder)
            except:
                pass
        # different headtype instance different object
        if self.mf_Top_Type == "mf_Top_Type_A":
            creator = mt.Type_A(self)
            if self.mf_Upper_Bolt_Nummber == '1':
                self.mf_Upper_Gear_Bolt_Position_1 = self.mf_Upper_Gear_Bolt_Position_1_1
            elif self.mf_Upper_Bolt_Nummber == '2':
                self.mf_Upper_Gear_Bolt_Position_1 = self.mf_Upper_Gear_Bolt_Position_1_2
                self.mf_Upper_Gear_Bolt_Position_2 = self.mf_Upper_Gear_Bolt_Position_2_1
            elif self.mf_Upper_Bolt_Nummber == '3':
                self.mf_Upper_Gear_Bolt_Position_1 = self.mf_Upper_Gear_Bolt_Position_1_3
                self.mf_Upper_Gear_Bolt_Position_2 = self.mf_Upper_Gear_Bolt_Position_2_2

               

        elif self.mf_Top_Type == "mf_Top_Type_B":
            creator = mt.Type_B(self) 
        
        #Create bottom part
        bottom = creator.create_Bottom()
        bottom["motor_id"] = creator.motor_id
        #Create energy part (Electric socket)
        en_part = creator.create_en_part()
        en_part["motor_id"] = creator.motor_id
        #Create Upper part
        upper_part = creator.create_upper_part()
        upper_part["motor_id"] = creator.motor_id
        #
        try:
            creator.ROTOR["motor_id"] = creator.motor_id
            creator.IN_GEAR_1["motor_id"] = creator.motor_id
            creator.IN_GEAR_2["motor_id"] = creator.motor_id
        except :
            pass
        obj_list=[upper_part, en_part, creator.ROTOR, creator.IN_GEAR_1, creator.IN_GEAR_2]
        # Combine all created parts
        motor = creator.combine_all_obj(bottom,obj_list, combine=self.mf_Combine)     
        motor.name = "Motor"
        motor.data.name = "Motor"
        motor["motor_id"] = creator.motor_id
        # Check if color should be rendered
        for area in bpy.context.screen.areas: # iterate through areas in current screen
            if area.type == 'VIEW_3D':               
                for space in area.spaces: # iterate through spaces in current VIEW_3D area
                    if space.type == 'VIEW_3D':
                        if self.mf_Color_Render:
                            space.shading.type = 'MATERIAL'
                        elif space.shading.type == 'MATERIAL' and len(bpy.data.materials) >0:
                            for material in bpy.data.materials:
                                material.user_clear()
                                bpy.data.materials.remove(material) #delete it
                            space.shading.type = 'SOLID' # set the viewport shading to rendered
                        else:
                            space.shading.type = 'SOLID' # set the viewport shading to rendered
        motor["category_id"] = 9
          
        if self.save_path != "None":
            self.calculate_positions(creator)
            creator.save_modell(motor)
            creator.write_back(self)
            creator.save_csv(self)
            #bpy.context.window_manager.popup_menu(self.success_save, title="Info", icon='PLUGIN')    

            self.save_path = "None" 
        creator.clear_bolt() 

        #self.test(creator)    
        return motor

    def success_save(self,okay,context):
        text = "Module saved under " + str(self.save_path)+ "Motor_%04d/"%self.id_Nr#"Motor_"+str(self.id_Nr)+'/'
        okay.layout.label(text=text)

    
    def delete_motor(self, contex):
        scene = bpy.context.scene
        motor = contex.active_object
        id = motor["motor_id"]
        for obj in scene.objects:
            try:
                if obj["motor_id"] == id:
                    obj.select_set(True)
                    bpy.ops.object.delete()
            except:
                continue

    def get_old_loc(self, contex):
        scene = bpy.context.scene
        motor = contex.active_object
        id = motor["motor_id"]
        loc_list = {}
        for obj in scene.objects:
            try:
                if obj["motor_id"] == id:
                    loc_list[obj.name_full] = [obj.location.x, obj.location.y, obj.location.z]
            except:
                continue
        return loc_list

    def move_motor(self, motor, loc_list):
        id = motor["motor_id"]
        scene = bpy.context.scene
        for obj in scene.objects:
            try:
                if obj["motor_id"] == id:
                    x, y, z = loc_list[obj.name_full] 
                    obj.location.x = x
                    obj.location.y = y
                    obj.location.z = z
            except:
                continue
        
    def calculate_positions(self, creator):
        
        x = self.mf_Lower_Gear_Dia/2
        y = creator.BOTTOM_DIA/4
        z = self.mf_Bottom_Length + self.mf_Sub_Bottom_Length + self.mf_Lower_Gear_Position

        if self.mf_Extension_Type_A == 'mf_Extension_Type_1':
               gear_orientation = self.mf_Gear_Orientation_1
                #self.param.append("mf_Gear_Orientation_1")
        elif self.mf_Extension_Type_A == 'mf_Extension_Type_2':                          
            gear_orientation = self.mf_Gear_Orientation_2
            #self.param.append("mf_Gear_Orientation_2")
        else:
            gear_orientation = self.mf_Gear_Orientation_1
            #self.param.append("mf_Gear_Orientation_2")
        rotation, length_relativ, mirror = creator.orient_dict[gear_orientation] 
        x_large = self.mf_Upper_Gear_Dia/2 - 0.8
        y_large = creator.BOTTOM_DIA/4 - length_relativ/6
        z_large = self.mf_Bottom_Length + self.mf_Sub_Bottom_Length + self.mf_Lower_Gear_Position + self.mf_Upper_Gear_Dia/2 + 0.2
        
        self.mf_Lower_Gear_XYZ = [x,y,z]
        self.mf_Lower_Gear_ContainerDia = self.mf_Lower_Gear_Dia
        self.mf_Lower_Gear_GearDia_Small = self.mf_Lower_Gear_Dia * 0.2
        self.mf_Lower_Gear_GearDia_Large = self.mf_Lower_Gear_Dia * 0.6
        self.mf_Lower_Gear_HoleDia = 1/2

        self.mf_Upper_Gear_XYZ = [x_large, y_large, z_large]
        self.mf_Upper_Gear_Position = self.mf_Lower_Gear_Position + self.mf_Upper_Gear_Dia/2 + 0.2
        self.mf_Upper_Gear_ContainerDia = self.mf_Upper_Gear_Dia
        self.mf_Upper_Gear_GearDia = self.mf_Upper_Gear_Dia * 0.7
        self.mf_Upper_Gear_HoleDia = 1.6/2




    def test_asdf(self,creator):
        #creator.create_rotor()
        #creator.create_internal_gear((0,0,20), 2.6, 3,number = 30)
        pass


   

    



