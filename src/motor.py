import bpy
import os
import math
import mathutils
import random
from .utility import Factory
from math import radians
import bmesh
import random
import csv


class Motor_Creator(Factory):
            
    ##############################################################################################################################
    ######################## Bottom Part #########################################################################################
    

    def create_Bottom(self):
        """Create Bottom Part

        Returns:
            
        """
        init_x = self.init_x
        init_y = self.init_y
        init_z = self.init_z

        size = 1
        main_hight = self.BOTTOM_HEIGHT * size
        main_width = self.BOTTOM_DIA * size
        main_long = self.bottom_length * size

        sub_radius = self.SUB_BOTTOM_DIA * size
        sub_long = self.sub_bottom_length * size

        inner_radius = self.inner_radius * size
        inner_long = self.SUB_BOTTOM_INNER_DEPTH * size

        # Add parts

        # Add main cylinder
        cylinder_d = main_long
        cylinder_x = init_x
        cylinder_y = init_y
        cylinder_z = init_z + cylinder_d/2 + sub_long    
        
        cyl = self.create_motor_main((cylinder_x, cylinder_y, cylinder_z),main_hight,main_width,main_long)
        cyl.name = 'Motor'

        cyl_2 = self.create_motor_main((cylinder_x, cylinder_y, cylinder_z+0.2),main_hight,main_width,main_long)

        bpy.ops.object.select_all(action='DESELECT')
        cyl_2.select_set(True)
        bpy.ops.transform.resize(value=(0.9, 0.9, 1))
        self.diff_obj(cyl,cyl_2)

        cyl_3 = self.create_motor_main((cylinder_x, cylinder_y, cylinder_z+0.2),main_hight,main_width,main_long)
        bpy.ops.object.select_all(action='DESELECT')
        cyl_3.select_set(True)
        bpy.ops.transform.resize(value=(0.91, 0.75, 1.1))
        self.diff_obj(cyl_2,cyl_3)
        cyl_3.select_set(True)
        bpy.ops.object.delete()

        cyl_2.select_set(True)
        bpy.ops.transform.resize(value=(1, 1, 0.75))
        cyl_2.location = (cylinder_x, cylinder_y, cylinder_z-0.5)
        cyl_2["motor_id"] = self.motor_id
        cyl_2.name = "Magnet"
        self.save_modell(cyl_2)

        # Add sub cylinder
        sub_cylinder_r = sub_radius/2
        sub_cylinder_d = sub_long
        sub_cylinder_x = init_x
        sub_cylinder_y = init_y
        sub_cylinder_z = init_z  + sub_long/2
        bpy.ops.mesh.primitive_cylinder_add(radius=sub_cylinder_r, depth=sub_cylinder_d, location=(sub_cylinder_x, sub_cylinder_y, sub_cylinder_z))
        sub_cyl = bpy.context.object
        sub_cyl.name = 'sub_cylinder'

        # Add inner cylinder
        inner_cylinder_r = inner_radius/2
        inner_cylinder_d = inner_long *2
        inner_cylinder_x = init_x
        inner_cylinder_y = init_y
        inner_cylinder_z = init_z 
        bpy.ops.mesh.primitive_cylinder_add(radius=inner_cylinder_r, depth=inner_cylinder_d, location=(inner_cylinder_x, inner_cylinder_y, inner_cylinder_z))
        inner_cyl = bpy.context.object
        inner_cyl.name = 'inner_cylinder'


        # Boolean Operation for inner cylinder
        bool_3 = sub_cyl.modifiers.new('bool_3', 'BOOLEAN')
        bool_3.operation = 'DIFFERENCE'
        bool_3.object = inner_cyl
        bpy.context.view_layer.objects.active = sub_cyl
        res = bpy.ops.object.modifier_apply(modifier='bool_3')

        # Delete the cylinder.x
        inner_cyl.select_set(True)
        bpy.ops.object.delete()

        rotor = self.create_rotor()
        rotor["motor_id"] = self.motor_id
        self.save_modell(rotor)
        self.ROTOR = rotor
        #rotor.select_set(True)
        #bpy.ops.object.delete()
        #Combine the Objects

        self.combine_all_obj(cyl,[sub_cyl])
        cyl["motor_id"] = self.motor_id
        
        if self.color_render:
            self.rend_color(cyl, "Metall", texture=self.corr_type_bottom, corr_percent=self.corr_percent_bottom)
            self.rend_color(cyl_2, "Magnet")
        cyl.name = "Bottom"

        self.save_modell(cyl)
        self.combine_all_obj(cyl,[cyl_2],self.mf_Combine)
        return cyl


    ##############################################################################################################################
    ######################## Middle Part #########################################################################################

    def create_middle(self):

        # Hight: x achse
        # Width: y achse
        # Length/Long: z achse

        size = 1
        thickness = self.BOARD_THICKNESS
        bolt_orient = self.bolt_ortientation

        main_hight = self.BOTTOM_HEIGHT * size
        main_width = self.BOTTOM_DIA * size
        main_long = self.bottom_length * size

        sub_radius = self.SUB_BOTTOM_DIA * size
        sub_long = self.sub_bottom_length * size

        inner_radius = self.inner_radius * size
        inner_long = self.SUB_BOTTOM_INNER_DEPTH * size

        bit_type = self.bit_type

        init_x = self.init_x 
        init_y = self.init_y
        init_z = self.init_z 

        cuboid_long = thickness *size + self.BOLT_LENGTH
        ub_lx = init_x 
        ub_ly = init_y
        ub_lz = init_z+ sub_long+ main_long - thickness *size/2 + self.BOLT_LENGTH/2

        cube_1 = self.create_motor_main((ub_lx,ub_ly,ub_lz),main_hight,main_width,cuboid_long)
        cube_1.name = 'cube1'
        #bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA, depth=50, location=(0,0,0))
        #hole = bpy.context.object
        hole = self.create_motor_main((ub_lx,ub_ly,sub_long+ main_long+cuboid_long/2-0.8),main_hight,main_width,cuboid_long)
        bpy.ops.object.select_all(action='DESELECT')
        hole.select_set(True)
        bpy.ops.transform.resize(value=(0.8, 0.9, 1))
        self.diff_obj(cube_1,hole)



        ##Part 2
        height = self.BOARD_THICKNESS
        width = 0.9 * main_width/2
        p2_length = self.BOLT_LENGTH/2

        x = init_x - main_hight/2 + height
        y = init_y - 0.2
        z = init_z + main_long + sub_long + p2_length

        bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
        bpy.ops.transform.resize(value=(height, width, p2_length))

        cube_2 = bpy.context.object
        self.diff_obj(cube_2,hole)


        ##Part 3
        height = self.BOARD_THICKNESS
        width = 0.9 * main_width/2
        p3_length = self.BOLT_LENGTH/2

        x = init_x + main_hight/2 - height
        y = init_y - 0.2
        z = init_z + main_long + sub_long + p3_length

        bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
        bpy.ops.transform.resize(value=(height, width, p3_length))

        cube_3 = bpy.context.object
        self.diff_obj(cube_3,hole)

        #Create Engergy part
        convex = self.create_4_convex_cyl()
        self.diff_obj(convex,hole)
        bpy.ops.object.select_all(action='DESELECT')
        hole.select_set(True)
        bpy.ops.object.delete()

        bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA, depth=main_hight/2, location=(ub_lx,ub_ly,ub_lz+main_hight/4))
        new_hole = bpy.context.object
        self.diff_obj(cube_1,new_hole)
        #self.diff_obj(convex,new_hole)
        new_hole.select_set(True)
        bpy.ops.object.delete()
        #Cereate  Bolt 1
        bolt_x = init_x + main_hight/2 - self.BOLT_RAD
        bolt_y = init_y + main_width/2
        bolt_z = init_z+ sub_long+ main_long + self.BOLT_LENGTH/2# BOLT_LENGTH/4 #1.1 is fixed value of bolt
        rota=(radians(180), 'X')
        bolt_1 = self.create_bolt((bolt_x, bolt_y, bolt_z),rota)

        #Cereate  Bolt 2
        bolt_x = init_x - main_hight/2 + self.BOLT_RAD
        bolt_y = init_y - main_width/2
        bolt_z = init_z+ sub_long+ main_long + self.BOLT_LENGTH/2# BOLT_LENGTH/4 #1.1 is fixed value of bolt
        bolt_2 = self.create_bolt((bolt_x, bolt_y, bolt_z),rota)

        mid_1 = self.combine_all_obj(cube_1,[cube_2,cube_3])
        mid_1.name = 'Middle_Part'

        if self.color_render:
            self.rend_color(mid_1, "Plastic")

        mid = self.combine_all_obj(mid_1,[bolt_1[0],bolt_2[0],convex])
        mid.name = 'Middle_Part'
        mid["motor_id"] = self.motor_id
        return mid, [bolt_1[1], bolt_2[1]]

    def create_en_part(self):

        size = 1
        thickness = self.BOARD_THICKNESS

        main_hight = self.BOTTOM_HEIGHT * size
        main_width = self.BOTTOM_DIA * size
        main_long = self.bottom_length * size
        sub_long = self.sub_bottom_length * size
        z_main = main_long + sub_long


        init_x = self.init_x 
        init_y = self.init_y
        init_z = self.init_z 


        height_en = 1.4/2
        length_en = 3/2

        en_z = init_z+ sub_long+ main_long - 0.1
        en_width_1 = thickness * size
        en_long_1 = length_en

        energy_x = init_x + main_hight/4
        en_y_1 = init_y - main_width/2

        bpy.ops.mesh.primitive_cube_add(location=(energy_x,en_y_1,en_z))
        bpy.ops.transform.resize(value=(height_en, en_width_1, en_long_1))
        en_1 = bpy.context.object
        en_1.name = 'cube2'

        ##Middle Part
        en_height_2 = height_en/2
        en_width_2 = 2* thickness * size
        en_long_2 = length_en

        en_y_2 = en_y_1 - en_width_1 - en_width_2

        bpy.ops.mesh.primitive_cube_add(location=(energy_x,en_y_2,en_z))
        bpy.ops.transform.resize(value=(en_height_2, en_width_2, en_long_2))
        en_2 = bpy.context.object
        en_2.name = 'cube3'

        ##Outer Part
        en_height_3 = height_en
        en_width_3 = thickness/2 * size
        en_long_3 = length_en

        en_y_3 = en_y_2 - en_width_2 - en_width_3

        bpy.ops.mesh.primitive_cube_add(location=(energy_x,en_y_3,en_z))
        bpy.ops.transform.resize(value=(en_height_3, en_width_3, en_long_3))
        en_3 = bpy.context.object
        en_3.name = 'cube4'

        ##Up Part
        en_height_4 = height_en
        en_width_4 = 1.5/2
        en_long_4 = 0.5 * thickness * size

        en_y_4 = en_y_1 - en_width_4 + en_width_1
        en_z_4 = en_z + length_en

        bpy.ops.mesh.primitive_cube_add(location=(energy_x,en_y_4,en_z_4))
        bpy.ops.transform.resize(value=(en_height_4, en_width_4, en_long_4))
        en_4 = bpy.context.object
        en_4.name = 'cube5'

        en_part_1 = self.combine_all_obj(en_1,[en_2,en_3,en_4])

        if self.color_render:
            self.rend_color(en_part_1, "Energy")

        bpy.context.view_layer.objects.active = None

        ##Diverse Part 1
        en_height_5 = thickness
        en_width_5 = en_width_4/3
        en_long_5 = en_long_3/3

        en_y_5 = en_y_3 - en_width_3 - en_width_5
        en_z_5 = init_z+ sub_long+ main_long + 1.4 - en_long_5 - thickness

        bpy.ops.mesh.primitive_cube_add(location=(energy_x,en_y_5,en_z_5))
        bpy.ops.transform.resize(value=(en_height_5, en_width_5, en_long_5))
        en_5 = bpy.context.object
        en_5.name = 'cube6'

        ##Diverse Part 2
        en_height_6 = thickness
        en_width_6 = en_width_4/6
        en_long_6 = en_long_3/3

        en_y_6 = en_y_3 - en_width_3 - en_width_6
        en_z_6 = en_z_5 - en_long_5 - en_long_6

        bpy.ops.mesh.primitive_cube_add(location=(energy_x,en_y_6,en_z_6))
        bpy.ops.transform.resize(value=(en_height_6, en_width_6, en_long_6))
        en_6 = bpy.context.object
        en_6.name = 'cube7'


        ##Diverse Part 3
        en_height_6 = thickness
        en_width_6 = en_width_4/4
        en_long_6 = en_long_3/3

        en_y_6 = en_y_3 - en_width_3 - en_width_6
        en_z_6 = en_z_5 - en_long_5 - en_long_6 + 0.5

        bpy.ops.mesh.primitive_cube_add(location=(energy_x-0.5,en_y_6,en_z_6))
        bpy.ops.transform.resize(value=(en_height_6, en_width_6, en_long_6))
        en_7 = bpy.context.object


        ##Diverse Part 4
        en_height_6 = thickness
        en_width_6 = en_width_4/4
        en_long_6 = en_long_3/3

        en_y_6 = en_y_3 - en_width_3 - en_width_6
        en_z_6 = en_z_5 - en_long_5 - en_long_6 + 0.5

        main = self.create_motor_main((0, 0, z_main),main_hight,main_width,length_en)

        bpy.ops.object.select_all(action='DESELECT')
        main.select_set(True)
        bpy.ops.transform.resize(value=(0.8, 0.95, 1))
        bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA*0.97, depth=50, location=(0,0,0))
        hole = bpy.context.object
        self.diff_obj(main,hole)
        hole.select_set(True)
        bpy.ops.object.delete()

        main_hole = self.create_motor_main((0, 0, z_main-0.2),main_hight,main_width,length_en)
        bpy.ops.object.select_all(action='DESELECT')
        main_hole.select_set(True)
        bpy.ops.transform.resize(value=(0.7, 0.8, 1))
        self.diff_obj(main,main_hole)
        main_hole.select_set(True)
        bpy.ops.object.delete()

        bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA*0.98, depth=self.BOLT_LENGTH, location=(0, 0, z_main+0.8*self.BOLT_LENGTH))
        uper_cyl = bpy.context.object#self.create_ring(position=(0, 0, z_main+0.6*self.BOLT_LENGTH), height=self.BOLT_LENGTH, radius=self.FOUR_CYL_DIA, thickness=0.5*self.FOUR_CYL_DIA)
        bpy.context.view_layer.objects.active = uper_cyl
        bpy.ops.object.modifier_add(type='BEVEL')
        bpy.context.object.modifiers["Bevel"].offset_type = 'OFFSET'
        bpy.context.object.modifiers["Bevel"].width_pct = 0.35#0.75*roter_rad*2
        bpy.context.object.modifiers["Bevel"].segments = 31
        bpy.context.object.modifiers["Bevel"].limit_method = 'ANGLE'
        bpy.context.object.modifiers["Bevel"].angle_limit = 0.20
        bpy.ops.object.modifier_apply(modifier="Bevel")

        bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA/4, depth=50, location=(0, 0, z_main+0.8*self.BOLT_LENGTH))
        uper_cyl_hole = bpy.context.object
        self.diff_obj(uper_cyl,uper_cyl_hole)
        uper_cyl_hole.select_set(True)
        bpy.ops.object.delete()

        main=self.combine_all_obj(main,[uper_cyl])


        if self.color_render:
            self.rend_color(main, "Energy")

        bpy.ops.mesh.primitive_cube_add(location=(energy_x+0.5,en_y_6,en_z_6))
        bpy.ops.transform.resize(value=(en_height_6, en_width_6, en_long_6))
        en_8 = bpy.context.object
        en_part_2 = self.combine_all_obj(en_5,[en_6, en_7,en_8])
        if self.color_render:
            self.rend_color(en_part_2, "Bit")
        bpy.context.view_layer.objects.active = None
        en_part = self.combine_all_obj(en_part_1,[en_part_2,main])

        en_part.name = "Charger"
        en_part["motor_id"] = self.motor_id

        self.save_modell(en_part)
        
        return en_part

    ##############################################################################################################################
    ######################## 4 Convex Cylinder Part ##############################################################################

    def create_4_convex_cyl(self):
        #Four convex cylinder and side board


        size = 1
        main_long = self.bottom_length * size

        sub_long = self.sub_bottom_length * size


        #four_cyl_dia = 1.4/2
        step = 0.1

        four_cyl_z = main_long + sub_long
        length_1 = self.C1_LENGTH
        length_2 = self.C1_LENGTH + self.C2_LENGTH
        length_3 = self.C1_LENGTH + self.C2_LENGTH + self.C3_LENGTH
        length_4 = self.C1_LENGTH + self.C2_LENGTH + self.C3_LENGTH + self.C4_LENGTH


        cy1_z = length_1/2
        cy2_z = length_2/2
        cy3_z = length_3/2
        cy4_z = length_4/2
        
        #Create 4 Covex cylinder
        
        #bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA, depth=length_1, location=(0,0,four_cyl_z+cy1_z))
        cyl_1 = self.create_ring((0,0,four_cyl_z+cy1_z), length_1, self.FOUR_CYL_DIA, self.BOARD_THICKNESS/3)#bpy.context.object
        #bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA - step, depth=length_2, location=(0,0,four_cyl_z+cy2_z))
        cyl_2 = self.create_ring((0,0,four_cyl_z+cy2_z), length_2, self.FOUR_CYL_DIA- step, self.BOARD_THICKNESS/3)

        #bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA- step *2, depth= length_3, location=(0,0,four_cyl_z+cy3_z))
        cyl_3 = self.create_ring((0,0,four_cyl_z+cy3_z), length_3, self.FOUR_CYL_DIA- step *2, self.BOARD_THICKNESS/3)

        #bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA - step *3, depth=length_4, location=(0,0,four_cyl_z+cy4_z))
        cyl_4 = self.create_ring((0,0,four_cyl_z+cy4_z), length_4, self.FOUR_CYL_DIA- step *3, self.BOARD_THICKNESS/3)

        #bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA - step *4, depth=length_5, location=(0,0,four_cyl_z+cy5_z))
        #cyl_5 = self.create_ring((0,0,four_cyl_z+cy5_z), length_5, self.FOUR_CYL_DIA- step *4, self.BOARD_THICKNESS)
        bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA - step *3, depth=0.2, location=(0,0,four_cyl_z+length_4-0.1))
        cover = bpy.context.object

        up = self.combine_all_obj(cyl_1,[cyl_2,cyl_3,cyl_4,cover])

        if self.color_render:
            self.rend_color(up, "Plastic")

        return up




class Type_A(Motor_Creator):
    
    
    #Gear
    gear_orientation = "r0"
    lower_gear_dia = 0
    lower_gear_position = None
    upper_gear_dia = 0

    lower_gear_bolt_random = False
    lower_gear_bolt_position_1 = 0
    lower_gear_bolt_position_2 = 0

    l_bolt_num = 1
    upper_Gear_Bolt_Random = True
    #large_gear_Angle = 0
    upper_Gear_Bolt_Position_1 = 1.3
    upper_Gear_Bolt_Position_2 = 1.3
    upper_Gear_Bolt_Position_3 = 1.3

    #4 covex cyl type A
    C1_LENGTH = 1.9
    C2_LENGTH = 2.7
    C3_LENGTH = 1.1
    C4_LENGTH = 0.8
    C5_LENGTH = 6.4

    
    param = []
    ##############################################################################################################################
    ######################## Upper Part Type A ###################################################################################


    def init_modify(self,factory):    
            self.param = []
            self.ex_type = factory.mf_Extension_Type_A
           
            if self.ex_type == 'mf_Extension_Type_1':
                self.gear_orientation = factory.mf_Gear_Orientation_1
                #self.param.append("mf_Gear_Orientation_1")
            elif self.ex_type == 'mf_Extension_Type_2':                          
                self.gear_orientation = factory.mf_Gear_Orientation_2
                #self.param.append("mf_Gear_Orientation_2")
            else:
                self.gear_orientation = factory.mf_Gear_Orientation_1
                #self.param.append("mf_Gear_Orientation_2")

            
            self.upper_gear_dia = factory.mf_Upper_Gear_Dia

            self.lower_gear_bolt_random = factory.mf_Lower_Gear_Bolt_Random

            self.lower_gear_bolt_position_1 = factory.mf_Lower_Gear_Bolt_Position_1
            self.lower_gear_bolt_position_2 = factory.mf_Lower_Gear_Bolt_Position_2

            self.l_bolt_num = int(factory.mf_Upper_Bolt_Nummber)
            
            self.upper_Gear_Bolt_Random = factory.mf_Upper_Gear_Bolt_Random

            if  self.l_bolt_num == 1:
                self.upper_Gear_Bolt_Position_1 = factory.mf_Upper_Gear_Bolt_Position_1_1
                self.upper_Gear_Bolt_Position_2 = -999
                self.upper_Gear_Bolt_Position_3 = -999 

            elif self.l_bolt_num == 2:
                self.upper_Gear_Bolt_Position_1 = factory.mf_Upper_Gear_Bolt_Position_1_2
                self.upper_Gear_Bolt_Position_2 = factory.mf_Upper_Gear_Bolt_Position_2_1
                self.upper_Gear_Bolt_Position_3 = -999
                self.param.append("mf_Upper_Gear_Bolt_Position_2")
            elif self.l_bolt_num == 3:
                self.upper_Gear_Bolt_Position_1 = factory.mf_Upper_Gear_Bolt_Position_1_3
                self.upper_Gear_Bolt_Position_2 = factory.mf_Upper_Gear_Bolt_Position_2_2
                self.upper_Gear_Bolt_Position_3 = factory.mf_Upper_Gear_Bolt_Position_3
                self.param.append("mf_Upper_Gear_Bolt_Position_2")
                self.param.append("mf_Upper_Gear_Bolt_Position_3")

            self.motor_param = [
                                "mf_Top_Type",
                                "mf_Extension_Type_A",
                                "mf_Gear_Orientation_2",
                                "mf_Mirror",
                                "mf_Color_Render",

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
                                ] + self.param

            if self.ex_type == 'mf_Extension_Type_1':
                self.motor_param[2] = "mf_Gear_Orientation_1"
            if self.color_render:
                self.motor_param.append("mf_corrosion_Render")
                if self.rend_corrosion:
                    self.motor_param.append("mf_corrosion_Type_Bolt")
                    self.motor_param.append("mf_corrosion_Percent_Bolt")
                    self.motor_param.append("mf_corrosion_Type_Bottom")
                    self.motor_param.append("mf_corrosion_Percent_Bottom")
            
            self.l_bolt_list = []
            self.s_bolt_list = []
            
    def write_back(self,factory):           
        if self.lower_gear_bolt_random:

            factory.mf_Lower_Gear_Bolt_Position_1 = self.lower_gear_bolt_position_1 
            factory.mf_Lower_Gear_Bolt_Position_2 = self.lower_gear_bolt_position_2 
       
        if self.upper_Gear_Bolt_Random:
            factory.mf_Upper_Gear_Bolt_Position_1 = self.upper_Gear_Bolt_Position_1
            factory.mf_Upper_Gear_Bolt_Position_2 = self.upper_Gear_Bolt_Position_2
            factory.mf_Upper_Gear_Bolt_Position_3 = self.upper_Gear_Bolt_Position_3

    def create_up(self, length_relativ, extension=False):
        
        init_x = self.init_x
        init_y = self.init_y
        rotation = (radians(-90),"X")

        #rotation, length_relativ, mirror = orient_dict[factory.mf_Gear_Orientation]


        size = 1
        main_height = self.BOTTOM_HEIGHT * size
        main_width = self.BOTTOM_DIA * size
        main_long = self.bottom_length * size

        sub_long = self.sub_bottom_length * size

        lower_gear_dia = self.lower_gear_dia
        lower_gear_position = self.lower_gear_position
        upper_gear_dia = self.upper_gear_dia
        if extension:
            x = init_x + lower_gear_dia/2
            y = init_y - main_width/4 - length_relativ/3 - 0.15
            z = main_long + sub_long + lower_gear_position

            x_large = init_x + lower_gear_dia/2 - 0.8
            y_large = init_y - main_width/4 - length_relativ/6 - length_relativ/6 - 0.15
            z_large = main_long + sub_long + lower_gear_position + upper_gear_dia/2 + 0.2
        else:
            x = init_x + lower_gear_dia/2
            y = init_y - main_width/4
            z = main_long + sub_long + lower_gear_position

            x_large = init_x + lower_gear_dia/2 - 0.8
            y_large = init_y - main_width/4 - length_relativ/6
            z_large = main_long + sub_long + lower_gear_position + upper_gear_dia/2 + 0.2

        #Create small gear
        rotation_s = (radians(-90),"X")
        extension_zone = None
        bottom_board =None
        if extension:
            if self.ex_type == "mf_None":
                extension_zone = None
                bottom_board = None  
            else:
                extension_zone, bottom_board = self.create_extension_zone((x_large,y_large,z_large),0.3)
                
            s_gear = self.create_gear((x,y,z),self.lower_gear_dia/2,"stick",length_relativ, extension = extension, bottom_board=bottom_board)
            y_bolt_init = y + 0.25 - 0.15

        else:
            s_gear = self.create_gear((x,y,z),self.lower_gear_dia/2,"stick",length_relativ)
            
            bpy.ops.mesh.primitive_cylinder_add(radius=self.upper_gear_dia/2, depth=length_relativ/3 + 1, location=(x_large,y_large-0.5,z_large))
            l_cyl = bpy.context.object
            bpy.ops.object.select_all(action='DESELECT')
            l_cyl.select_set(True)
            bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
            self.diff_obj(s_gear,l_cyl)
            bpy.ops.object.select_all(action='DESELECT')

            l_cyl.select_set(True)
            bpy.ops.object.delete()

            y_bolt_init = y - length_relativ/3 + self.BOLT_LENGTH/2 -  0.8 * self.BOLT_RAD
            #+ self.EXTENSION_THICKNESS + 0.1


        # Create Bolt for small gear

        x_bolt_init = x+ lower_gear_dia/2 + 0.9*self.BOLT_RAD
        z_bolt_init = z 
        # Calculate the rotate (x,z axis)
        bolt_rotation_1 = self.lower_gear_bolt_position_1
        bolt_rotation_2 = self.lower_gear_bolt_position_2
        if self.lower_gear_bolt_random:  
            if extension:
                bolt_rotation_1,bolt_rotation_2 =  self.s_bolt_list    
            else: 
                bolt_rotation_1 = random.uniform(190,230)
                self.lower_gear_bolt_position_1 = bolt_rotation_1
                bolt_rotation_2 =  random.uniform(310,350)
                self.lower_gear_bolt_position_2 = bolt_rotation_2
                self.s_bolt_list = [bolt_rotation_1,bolt_rotation_2]

        x_bolt_1, z_bolt_1 = self.rotate_around_point((x,z),bolt_rotation_1,(x_bolt_init,z_bolt_init))
        x_bolt_2, z_bolt_2 = self.rotate_around_point((x,z),bolt_rotation_2,(x_bolt_init,z_bolt_init))       
        bolt_1 = self.create_bolt((x_bolt_1, y_bolt_init,z_bolt_1), rotation = rotation_s, only_body = extension)
        bolt_2 = self.create_bolt((x_bolt_2, y_bolt_init,z_bolt_2), rotation = rotation_s, only_body = extension) 

        bolt_shell_list = [bolt_1[0], bolt_2[0]]
        bolt_bit_list = [bolt_1[1], bolt_2[1]]

        #Create large Gear
        if extension:        
            
            l_gear = self.create_gear((x_large,y_large,z_large),self.upper_gear_dia/2, "hollow",length_relativ,extension = extension,bottom_board=bottom_board)
            y_bolt_init = y_large + 0.25 - 0.15

        else:
            l_gear = self.create_gear((x_large,y_large,z_large),self.upper_gear_dia/2, "hollow",length_relativ)

            bpy.ops.mesh.primitive_cylinder_add(radius=self.lower_gear_dia/2, depth=length_relativ, location=(x,y,z))
            s_cyl = bpy.context.object
            bpy.ops.object.select_all(action='DESELECT')
            s_cyl.select_set(True)
            bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
            self.diff_obj(l_gear,s_cyl)
            s_cyl.select_set(True)
            bpy.ops.object.delete()

            y_bolt_init = y_large - length_relativ/6 + self.BOLT_LENGTH/2 -  0.8 * self.BOLT_RAD
            


        #Create bolts for large gear
        x_bolt_init = x_large+ upper_gear_dia/2 + 0.9*self.BOLT_RAD
        z_bolt_init = z_large 

        #Calculate the rotation
        single_bolt_area = 210/self.l_bolt_num
        bolt_position_angle_1 = self.upper_Gear_Bolt_Position_1
        bolt_position_angle_2 = self.upper_Gear_Bolt_Position_2
        bolt_position_angle_3 = self.upper_Gear_Bolt_Position_3

        if self.l_bolt_num == 1:
            if self.upper_Gear_Bolt_Random:                    
                if extension:
                    bolt_position_angle_1 = self.l_bolt_list[0]
                else:
                    bolt_position_angle_1 = random.uniform(0,single_bolt_area)
                    self.upper_Gear_Bolt_Position_1 = bolt_position_angle_1
                    self.l_bolt_list=[bolt_position_angle_1]          

            x_bolt, z_bolt = self.rotate_around_point((x_large, z_large),bolt_position_angle_1,(x_bolt_init,z_bolt_init))
            bolt = self.create_bolt((x_bolt,y_bolt_init,z_bolt), rotation = rotation_s, only_body=extension)
            bolt_shell_list.append(bolt[0])
            bolt_bit_list.append(bolt[1])
        elif self.l_bolt_num == 2:
            if self.upper_Gear_Bolt_Random:
                if extension:
                    bolt_position_angle_1 = self.l_bolt_list[0]
                    bolt_position_angle_2 = self.l_bolt_list[1]
                else:
                    bolt_position_angle_1 = random.uniform(0,single_bolt_area) 
                    bolt_position_angle_2 = random.uniform(1.2*single_bolt_area, 2*single_bolt_area)
                    self.upper_Gear_Bolt_Position_1 = bolt_position_angle_1
                    self.upper_Gear_Bolt_Position_2 = bolt_position_angle_2
                    self.l_bolt_list=[bolt_position_angle_1, bolt_position_angle_2]
            

            x_bolt_1, z_bolt_1 = self.rotate_around_point((x_large,z_large),
                                                          bolt_position_angle_1,
                                                          (x_bolt_init,z_bolt_init))
            x_bolt_2, z_bolt_2 = self.rotate_around_point((x_large,z_large),
                                                          bolt_position_angle_2,
                                                          (x_bolt_init,z_bolt_init))
            bolt_1 = self.create_bolt((x_bolt_1, y_bolt_init,z_bolt_1), rotation = rotation_s, only_body=extension)
            bolt_2 = self.create_bolt((x_bolt_2, y_bolt_init,z_bolt_2), rotation = rotation_s, only_body=extension)

            bolt_shell_list.append(bolt_1[0])
            bolt_bit_list.append(bolt_1[1])

            bolt_shell_list.append(bolt_2[0])
            bolt_bit_list.append(bolt_2[1])           
        elif self.l_bolt_num == 3:
            if self.upper_Gear_Bolt_Random:

                if extension:
                    bolt_position_angle_1 = self.l_bolt_list[0]
                    bolt_position_angle_2 = self.l_bolt_list[1]
                    bolt_position_angle_3 = self.l_bolt_list[2]
                else:
                    bolt_position_angle_1 = random.uniform(0,single_bolt_area) 
                    bolt_position_angle_2 = random.uniform(1.2*single_bolt_area, 2*single_bolt_area)
                    bolt_position_angle_3 = random.uniform(2.2*single_bolt_area, 3*single_bolt_area)
                    self.upper_Gear_Bolt_Position_1 = bolt_position_angle_1
                    self.upper_Gear_Bolt_Position_2 = bolt_position_angle_2
                    self.upper_Gear_Bolt_Position_3 = bolt_position_angle_3
                    self.l_bolt_list=[bolt_position_angle_1, bolt_position_angle_2, bolt_position_angle_3]
                
            x_bolt_1, z_bolt_1 = self.rotate_around_point((x_large,z_large),
                                                            bolt_position_angle_1,
                                                            (x_bolt_init,z_bolt_init))
            x_bolt_2, z_bolt_2 = self.rotate_around_point((x_large,z_large),
                                                          bolt_position_angle_2,
                                                          (x_bolt_init,z_bolt_init))
            x_bolt_3, z_bolt_3 = self.rotate_around_point((x_large,z_large),
                                                          bolt_position_angle_3,
                                                          (x_bolt_init,z_bolt_init))
            bolt_1 = self.create_bolt((x_bolt_1, y_bolt_init, z_bolt_1), rotation = rotation_s, only_body=extension)
            bolt_2 = self.create_bolt((x_bolt_2, y_bolt_init, z_bolt_2), rotation = rotation_s, only_body=extension)
            bolt_3 = self.create_bolt((x_bolt_3, y_bolt_init, z_bolt_3), rotation = rotation_s, only_body=extension)

            bolt_shell_list.append(bolt_1[0])
            bolt_bit_list.append(bolt_1[1])
            
            bolt_shell_list.append(bolt_2[0])
            bolt_bit_list.append(bolt_2[1]) 

            bolt_shell_list.append(bolt_3[0])
            bolt_bit_list.append(bolt_3[1])


        #extension_zone = create_extension_zone(factory,(x_large,y_large,z_large))
        

        if extension: 
            up = self.combine_all_obj(s_gear,[l_gear,extension_zone,bottom_board] + bolt_shell_list)

        else:
            gear_board = self.create_gear_board()

            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.mesh.primitive_cylinder_add(radius=self.lower_gear_dia/2, depth=length_relativ, location=(x,y,z))
            s_cyl = bpy.context.object
            bpy.ops.object.select_all(action='DESELECT')
            s_cyl.select_set(True)
            bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
            self.diff_obj(gear_board,s_cyl)
            s_cyl.select_set(True)
            bpy.ops.object.delete()

            up = self.combine_all_obj(s_gear,[l_gear,gear_board] + bolt_shell_list)
            
        
        #Cut unseful part
        if extension:
            pass
        else:           
            bpy.ops.mesh.primitive_cube_add(location=(x, y-length_relativ/3-5.05, z))
            bpy.ops.transform.resize(value=(5, 5, 8))
            cube_1 = bpy.context.object
            cube_1.name = 'cube1'
            self.diff_obj(up,cube_1)
            cube_1.select_set(True)
            bpy.ops.object.delete()


        
        if self.color_render:
            self.rend_color(up, "Plastic")



        return up, bolt_bit_list


    def in_gear_1(self, position, height, radius):
        gear_s = self.create_internal_gear((position[0], position[1], position[2]-0.3*height), height*0.4, radius, 50)
        gear_l = self.create_internal_gear(position, height, radius, 10)
        


    def create_gear(self,position, radius, gear_type,info, extension = False, bottom_board = None):
        rotation = (radians(-90),"X")
        length_relativ = info
        if gear_type == 'stick':
            inner_radius = 1/2
            if extension:
                length = 0.5
                inner_length = 0.7 * length +0.5
                position_inner = (position[0], position[1], position[2]+inner_length/2)
            else:
                length = length_relativ*2/3
                inner_length = 0.7 * length +0.5
                position_inner = (position[0], position[1], position[2]-inner_length/2)
            

            #Create out
            bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=length, location=position)
            out_cyl = bpy.context.object
            out_cyl.name = 'out_cylinder'

            #Create inner
            bpy.ops.mesh.primitive_cylinder_add(radius=inner_radius, depth=inner_length, location=position_inner)
            in_cyl = bpy.context.object
            in_cyl.name = 'in_cylinder'
            
            if extension :
                cly_1 = self.create_ring((position[0],position[1],position[2]+0.1),0.4,radius-0.5, 0.7)
                self.diff_obj(out_cyl, cly_1)

                cly_1.select_set(True)
                bpy.ops.object.delete()
            else:
                ### Make Hole
                bpy.ops.mesh.primitive_cylinder_add(radius=radius - self.EXTENSION_THICKNESS, depth=length, location=(position[0], position[1], position[2]+self.EXTENSION_THICKNESS))
                hole = bpy.context.object
                self.diff_obj(out_cyl, hole)
                self.diff_obj(in_cyl, hole)
                hole.select_set(True)
                bpy.ops.object.delete()

                ### Create inner gear
                in_gear_s = self.create_internal_gear((position[0], position[1], position[2]-0.3*length), length*0.4, radius*0.6, 40, thickness=0.7)
                in_gear_l = self.create_internal_gear(position, length*0.75, radius*0.2, 10, thickness=0.3)
                in_gear = self.combine_all_obj(in_gear_s,[in_gear_l])
                bpy.context.view_layer.objects.active = in_gear
                bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
                in_gear.name = "Lower_Inner_Gear"
                in_gear.location = (position[0], position[1]+0.15*length, position[2])
                self.rotate_object(in_gear)
                self.rend_color(in_gear, "Gear")
                self.save_modell(in_gear)
                self.IN_GEAR_1 = in_gear
                #in_gear.select_set(True)
                #bpy.ops.object.delete()

               
            part = self.combine_all_obj(out_cyl,[in_cyl])

            if self.color_render:
                self.rend_color(part, "Plastic")

            bpy.context.view_layer.objects.active = part
            bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 

            if bottom_board:
                bpy.ops.mesh.primitive_cylinder_add(radius=radius-0.5, depth=length+10, location=position)
                cly_2 = bpy.context.object

                bpy.context.view_layer.objects.active = part
                bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
                self.diff_obj(bottom_board, cly_2)
                cly_2.select_set(True)
                bpy.ops.object.delete()
            


            return part
        elif gear_type == 'hollow':

            if extension:
                length = 0.5
                inner_length = length + 0.5  

            else:
                length = length_relativ/3
                inner_length = length + 1.3  
            inner_radius_1 = 1.6/2
            inner_radius_2 = 1.3/2
            inner_radius_3 = 2.9/2
                 
            
            #Ring 1
            thickness_1 = radius - inner_radius_1
            cly_1 = self.create_ring(position,length,radius,thickness_1)
            if extension:
                pass
            else:
                bpy.ops.mesh.primitive_cylinder_add(radius=radius - self.EXTENSION_THICKNESS, depth=length, location=(position[0], position[1], position[2] + self.EXTENSION_THICKNESS))
                hole = bpy.context.object
                self.diff_obj(cly_1, hole)

            #Ring 2
            x = position[0]
            y = position[1]
            z = position[2] - inner_length/2 + length/2 + 0.3
            position_in = (x,y,z)

            thickness_2 = inner_radius_1 - inner_radius_2
            cly_2 = self.create_ring(position_in,inner_length,inner_radius_1,thickness_2)
            if extension:
                pass
            else:
                self.diff_obj(cly_2, hole)

            #Ring 3
            x = position[0]
            y = position[1]
            z = position[2] + 0.1
            position_3 = (x,y,z)

            thickness_3 = 0.2
            cly_3 = self.create_ring(position_3,length+0.4,inner_radius_3,thickness_3)
            if extension:
                pass
            else:
                self.diff_obj(cly_3, hole)
                hole.select_set(True)
                bpy.ops.object.delete()

                ### Create inner gear
                in_gear_s = self.create_internal_gear((position[0], position[1], position[2]+0.5*length), 0.8*length, radius*0.7, 30, thickness=0.8)
                in_gear_l = self.create_ring(position, inner_length, radius*0.25, 0.2)
                in_gear = self.combine_all_obj(in_gear_s,[in_gear_l])
                bpy.context.view_layer.objects.active = in_gear
                bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
                in_gear.name = "Upper_Inner_Gear"
                in_gear.location = (position[0], position[1]-0.3*length, position[2])
                self.rotate_object(in_gear)
                self.save_modell(in_gear)
                self.rend_color(in_gear, "Gear")
                #in_gear.select_set(True)
                #bpy.ops.object.delete()
                self.IN_GEAR_2 = in_gear

            part = self.combine_all_obj(cly_1,[cly_2,cly_3]) 
            

            if self.color_render:
                self.rend_color(part, "Plastic")

            bpy.context.view_layer.objects.active = part
            bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
        
            return part
        
    def create_extension_zone(self, large_gear_position, gear_length):

        lower_gear_dia = self.lower_gear_dia
        lower_gear_position = self.lower_gear_position
        upper_gear_dia = self.upper_gear_dia


        s_length_1 = 2.9/2
        s_length_2 = 5.5
        s_length_3 = 1.5
        s_length_4 = 4.5
        s_length_6 = 3


        if self.ex_type == 'mf_Extension_Type_2':
            angle_1 = 20
            angle_1_1 = 30
            angle_2 = 7
            angle_4 = 0
            angle_5 = 5
            s_length_5 = 4.5
            s_length_2 = 4.5
            



        elif self.ex_type == 'mf_Extension_Type_1':
            angle_1 = 30
            angle_1_1 = angle_1
            s_length_5 = 5
            angle_2 = 25
            angle_4 = angle_2
            angle_5 =  angle_2


        else:
            return None

        angle_3 = 35

        x = large_gear_position[0] 
        y = large_gear_position[1] - gear_length/2 + 0.4
        z = large_gear_position[2]

        x_thickness = math.cos(radians(angle_3)) * self.EXTENSION_THICKNESS

        p1x = x + s_length_1 * math.cos(radians(angle_1))
        p1z = z + s_length_1 * math.sin(radians(angle_1))

        p2x = x - s_length_1 * math.cos(radians(angle_1_1))
        p2z = z - s_length_1 * math.sin(radians(angle_1_1))

        p3x = p1x + s_length_2 * math.sin(radians(angle_1))
        p3z = p1z - s_length_2 * math.cos(radians(angle_1))


        #p3hx = p3x - s_length_3 * math.sin(radians(angle_2))
        #p3hz = p3z - s_length_3 * math.cos(radians(angle_2))
        if self.ex_type == 'mf_Extension_Type_2':
            p3hx = p3x
            p3hz = p3z - 1.5
        elif self.ex_type == 'mf_Extension_Type_1':
            p3hx = p3x - s_length_3 * math.sin(radians(angle_2))
            p3hz = p3z - s_length_3 * math.cos(radians(angle_2))

        p4x = p2x + s_length_4 * math.sin(radians(angle_5))
        p4z = p2z - s_length_4 * math.cos(radians(angle_5))
        
        p5x = p3x - s_length_5 * math.sin(radians(angle_4))
        p5z = p3z - s_length_5 * math.cos(radians(angle_4))

        p6x = p4x
        p6z = p4z - s_length_6

        y_of = 0

        #Create side board 1
        verts_b1 = [
            (p1x, y, p1z),
            (p1x - x_thickness, y, p1z),
            (p1x, y - 0.5 +y_of, p1z),
            (p1x - x_thickness, y - 0.5 +y_of, p1z),
            (p3x, y , p3z),
            (p3x - x_thickness, y, p3z),
            (p3x, y - 1.1 +y_of, p3z),
            (p3x - x_thickness, y - 1.1 +y_of, p3z),
            (p5x, y, p5z),
            (p5x - x_thickness, y, p5z),
            (p5x, y - 1.5 +y_of, p5z),
            (p5x - x_thickness, y - 1.5 +y_of, p5z),
        ]
        faces_b1 = [
            [0, 1, 3, 2],
            [1,5,7,3],
            [5,9,11,7],
            [9,8,10,11],
            [8,10,6,4],
            [4,6,2,0],
            [0,1,5,9,8,4],
            [2,3,7,11,10,6],
        ]

        board_1 = self.add_mesh("board_1", verts_b1, faces_b1)

        #Create side board 2
        verts_b2 = [
            (p2x, y, p2z),
            (p2x + x_thickness, y, p2z),
            (p2x, y - 0.5 +y_of, p2z),
            (p2x + x_thickness, y - 0.5 +y_of, p2z),
            (p4x, y, p4z),
            (p4x + x_thickness, y, p4z),
            (p4x, y - 1.1 +y_of, p4z),
            (p4x + x_thickness, y - 1.1 +y_of, p4z),
            (p6x, y, p6z),
            (p6x + x_thickness, y, p6z),
            (p6x, y - 1.5 +y_of, p6z),
            (p6x + x_thickness, y - 1.5 +y_of, p6z),
        ]
        faces_b2 = [
            [0,1,3,2],
            [1,5,7,3],
            [5,9,11,7],
            [9,8,10,11],
            [8,10,6,4],
            [4,6,2,0],
            [0,1,5,9,8,4],
            [2,3,7,11,10,6],
        ]
        board_2 = self.add_mesh("board_2", verts_b2, faces_b2)

        #Create bottom board
        thickness_bottom = 0.3
        verts_bottom = [
            (p1x+ x_thickness , y, p1z-(upper_gear_dia/5)* math.sin(radians(angle_1))), #0
            (p1x+ x_thickness , y - thickness_bottom, p1z-((upper_gear_dia/5)* math.sin(radians(angle_1)))), #1
            (p3x- x_thickness, y, p3z), #2
            (p3x- x_thickness, y - thickness_bottom, p3z), #3
            (p5x- x_thickness, y, p5z), #4
            (p5x- x_thickness, y - thickness_bottom, p5z), #5
            (p6x , y, p6z), #6
            (p6x, y - thickness_bottom, p6z), #7
            (p4x , y, p4z), #8
            (p4x, y - thickness_bottom, p4z), #9
            (p2x, y, p2z-upper_gear_dia/6), #10
            (p2x , y - thickness_bottom, p2z-upper_gear_dia/6), #11
            (p3hx- x_thickness, y, p3hz), #12
            (p3hx- x_thickness, y - 1.1 +y_of, p3hz), #13
            (p4x , y - 1.1 +y_of, p4z), #14
            (p5x- x_thickness, y - 1.5 +y_of, p5z), #15
            (p6x , y - 1.5 +y_of, p6z), #16
        ]

        faces_bottom = [
            [0,1,3,2],
            [2,3,5,4],
            [4,5,7,6],
            [6,7,9,8],
            [8,9,11,10],
            [10,11,1,0],
            [9,2,4,6,8,10],
            [1,3,5,7,9,11],
            [12,13,14,8],
            [13, 15, 16, 14],       

        ]
        bottom_board = self.add_mesh("bottom board", verts_bottom, faces_bottom)
        #Create end cylinder
        if self.ex_type == 'mf_Extension_Type_2':
            dia = math.sqrt((p5x-p6x)**2 + (p5z - p6z)**2)/3
            x_cyl_1 = p5x - (p5x - p6x)*5/6
            y_cyl_1 = (y - 0.8)
            z_cyl_1 = p6z - (p6z -p5z)/3 
            end_cly_1 = self.create_ring((x_cyl_1,y_cyl_1 - 0.5,z_cyl_1), 2.6, dia/2, 0.5)
            end_cly_1.matrix_world @= mathutils.Matrix.Rotation(radians(90), 4, 'X')
            bpy.ops.transform.rotate(value=radians(90),orient_axis='X') 
            end_cly_1.name = 'End_cylinder'
            
            x_cyl_2 = p5x - (p5x - p6x)/6
            y_cyl_2 = (y - 0.8)
            z_cyl_2 = p6z - (p6z -p5z)*2/3 
            end_cly_2 = self.create_ring((x_cyl_2,y_cyl_2 - 0.5,z_cyl_2), 2.6, dia/2, 0.5)
            end_cly_2.matrix_world @= mathutils.Matrix.Rotation(radians(90), 4, 'X')
            bpy.ops.transform.rotate(value=radians(90),orient_axis='X') 
            end_cly_2.name = 'End_cylinder'

            board = self.combine_all_obj(board_1,[board_2,end_cly_1,end_cly_2])

            bevel = board.modifiers.new(name='bevel', type='BEVEL')
            
            bevel.affect = 'EDGES'
            bevel.angle_limit = 100
            bevel.offset_type = 'WIDTH'
            bevel.width = 1000000
            bpy.context.view_layer.objects.active = board
            res = bpy.ops.object.modifier_apply(modifier='bevel')

        elif self.ex_type == 'mf_Extension_Type_1':

            dia = math.sqrt((p5x-p6x)**2 + (p5z - p6z)**2)
            x_cyl = p5x - (p5x - p6x)/2 
            y_cyl = (y - 0.8)
            z_cyl = p6z - (p6z -p5z)/2 
            end_cly = self.create_ring((x_cyl,y_cyl,z_cyl), 1.6, dia/2, 0.5)
            end_cly.matrix_world @= mathutils.Matrix.Rotation(radians(90), 4, 'X')
            bpy.ops.transform.rotate(value=radians(90),orient_axis='X') 
            end_cly.name = 'End_cylinder'
            board = self.combine_all_obj(board_1,[board_1, board_2,end_cly])

        if self.ex_type == 'mf_Extension_Type_2':
            bpy.ops.transform.mirror(orient_type='LOCAL',constraint_axis=(True, False, False))
            bpy.ops.transform.translate(value=(2.9/2*1.6,0,0))
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None
            bpy.context.view_layer.objects.active = bottom_board
            bottom_board.select_set(True)
            bpy.ops.transform.mirror(orient_type='LOCAL',constraint_axis=(True, False, False))
            bpy.ops.transform.translate(value=(2.9/2*1.6,0,0))


        if self.color_render:
            self.rend_color(board, "Plastic")

        return board, bottom_board

    def create_outer_board(self, length_relativ):
        init_x = self.init_x
        init_y = self.init_y
        init_z = self.init_z

        size = 1
        main_height = self.BOTTOM_HEIGHT * size
        main_width = self.BOTTOM_DIA * size
        main_long = self.bottom_length * size

        sub_long = self.sub_bottom_length * size

        height = self.BOARD_THICKNESS
        p1_length = 2.4/2
        ##Part 1
        if self.gear_orientation in ['r180', 'r0'] :
            width = 0.9 * self.BOTTOM_DIA/2
        elif self.gear_orientation in ['r270', 'r90'] :
            width = 0.9 * self.BOTTOM_HEIGHT/2
        

        x1 = init_x - self.BOTTOM_HEIGHT/2 + self.BOARD_THICKNESS
        y1 = init_y - 2 * self.BOARD_THICKNESS
        z1 = init_z + main_long + sub_long + self.BOLT_LENGTH + p1_length - self.BOLT_LENGTH/2
        bpy.ops.mesh.primitive_cube_add(location=(x1,y1,z1))
        bpy.ops.transform.resize(value=(height, width, p1_length - self.BOLT_LENGTH/2 ))

        board_1 = bpy.context.object

        z2 = init_z + main_long + sub_long + p1_length*2 + (
                        self.C1_LENGTH + self.C2_LENGTH + self.C3_LENGTH - p1_length*2 )/2

        x2 = init_x - self.BOTTOM_HEIGHT/4 + self.BOARD_THICKNESS
        p2_length = math.sqrt((self.C1_LENGTH + self.C2_LENGTH + self.C3_LENGTH-p1_length*2)**2 
                                + (main_height/2)**2 )/2
        Angle = math.atan((main_height/2)/(self.C1_LENGTH + self.C2_LENGTH + self.C3_LENGTH -
                                    p1_length*2))
        bpy.ops.mesh.primitive_cube_add(location=(x2,y1,z2))
        bpy.ops.transform.resize(value=(height, width, p2_length))
        board_2 = bpy.context.object
        bpy.context.view_layer.objects.active = board_2
        bpy.ops.transform.rotate(value=-Angle,orient_axis='Y') 

        board_out = self.combine_all_obj(board_1,[board_2])

        x,y,z = board_out.location

        board_in = self.create_middle_board_mesh()
        outer_board = self.combine_all_obj(board_out,[board_in])
        ############################################################################################

        init_x = self.init_x
        init_y = self.init_y
        rotation = (radians(-90),"X")



        main_width = self.BOTTOM_DIA * size
        main_long = self.bottom_length * size
        sub_long = self.sub_bottom_length * size

        lower_gear_dia = self.lower_gear_dia
        lower_gear_position = self.lower_gear_position
        upper_gear_dia = self.upper_gear_dia


        x = init_x + lower_gear_dia/2
        y = init_y - main_width/4
        z = main_long + sub_long + lower_gear_position

        x_large = init_x + lower_gear_dia/2 - 0.8
        y_large = init_y - main_width/4 - length_relativ/6
        z_large = main_long + sub_long + lower_gear_position + upper_gear_dia/2 + 0.2
        
        bpy.ops.mesh.primitive_cylinder_add(radius=self.lower_gear_dia/2, depth=length_relativ, location=(x,y,z))
        s_cyl = bpy.context.object
        bpy.ops.object.select_all(action='DESELECT')
        s_cyl.select_set(True)
        bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
        self.diff_obj(outer_board,s_cyl)
        s_cyl.select_set(True)
        bpy.ops.object.delete()

        bpy.ops.mesh.primitive_cylinder_add(radius=self.upper_gear_dia/2, depth=length_relativ/3 + 1, location=(x_large,y_large-0.5,z_large))
        l_cyl = bpy.context.object
        bpy.ops.object.select_all(action='DESELECT')
        l_cyl.select_set(True)
        bpy.ops.transform.rotate(value=rotation[0],orient_axis=rotation[1]) 
        self.diff_obj(outer_board,l_cyl)
        bpy.ops.object.select_all(action='DESELECT')
        l_cyl.select_set(True)
        bpy.ops.object.delete()
     

        return outer_board

    def create_gear_board(self):

        init_x = self.init_x
        init_y = self.init_y
        init_z = self.init_z

        size = 1
        main_height = self.BOTTOM_HEIGHT * size
        main_width = self.BOTTOM_DIA * size
        main_long = self.bottom_length * size

        sub_long = self.sub_bottom_length * size

        height = self.BOARD_THICKNESS

        length = self.lower_gear_position /2

        x = main_height/4
        y = -0.2
        z = init_z + main_long + sub_long + self.BOLT_LENGTH
        bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
        bpy.ops.transform.resize(value=(main_height*0.15, self.BOARD_THICKNESS/2, length*0.8))

        if self.gear_orientation in ['r270111', 'r90111'] :
            x = 0
            y = - main_width/2
            z = init_z + main_long + sub_long + self.BOLT_LENGTH
            bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
            bpy.ops.transform.resize(value=(self.BOARD_THICKNESS/2, main_width*0.09, length))

        board_5 = bpy.context.object

        #Create board
        x = self.lower_gear_dia/2
        y = - main_width/4 +0.25
        z = main_long + sub_long + self.lower_gear_position

        width = 2.25
        height = self.BOARD_THICKNESS
        length = math.sqrt((x-self.FOUR_CYL_DIA)**2 +  self.lower_gear_position**2)

        x_board = self.FOUR_CYL_DIA + (x - self.FOUR_CYL_DIA)/2
        y_board = y + 0.5
        z_board = main_long + sub_long + ( self.lower_gear_position)/2


        Angle = math.atan((x-self.FOUR_CYL_DIA)/ self.lower_gear_position)

    
        bpy.ops.mesh.primitive_cube_add(location=(x_board,y_board,z_board))
        bpy.ops.transform.resize(value=(height/2, width/2, length/2))
        board_3 = bpy.context.object

        bpy.context.view_layer.objects.active = board_3        

        bpy.ops.transform.rotate(value=-Angle,orient_axis='Y') 

        board_gear= self.combine_all_obj(board_5,[board_3])

        return board_gear

    def create_middle_board_mesh(self):
        main_long = self.bottom_length 

        sub_long = self.sub_bottom_length
        l1 = 2.4
        l2 = self.C1_LENGTH + self.C2_LENGTH + self.C3_LENGTH

        east = self.BOTTOM_HEIGHT/2 - 0.1
        north = self.BOTTOM_HEIGHT/2 - 0.1

        thickness = self.BOARD_THICKNESS/2

        z_offset = main_long + sub_long

        #if self.gear_orientation in ['r0','r180'] :
        p1 = [0, thickness, z_offset]
        p2 = [0, thickness, z_offset+l2]
        p3 = [-east, thickness ,z_offset+l1]
        p4 = [-east, thickness, z_offset]
        p_thick = [0, -2* thickness, 0]

        verts = []
        
        for n in [p1,p2,p3,p4]:
            verts.append(n)
            verts.append(self.add_vector(n,p_thick))

        faces = [
            [0, 1, 3, 2],
            [2, 3 ,5, 4],
            [4, 5, 7, 6],
            [6, 7, 1, 0],
            [0, 2, 4, 6],
            [1, 3, 5, 7]
        ]

        board = self.add_mesh("board", verts, faces)
        return board

    def create_upper_part(self):
        rotation, length_relativ, mirror = self.orient_dict[self.gear_orientation]        
        
        middle, bolt_list_middle = self.create_middle()
        for bolt in bolt_list_middle:
            self.save_modell(bolt)
            
        board = self.create_outer_board(length_relativ)  
        self.rotate_object(board)
        bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA-0.2, depth=50, location=(0,0,0))
        hole = bpy.context.object
        self.diff_obj(board,hole)
        hole.select_set(True)
        bpy.ops.object.delete()
        
        

        up1, bolt_list_1 = self.create_up(length_relativ)
        
        hole = self.create_motor_main((0, 0, self.bottom_length+self.sub_bottom_length+self.BOLT_LENGTH/2),self.BOTTOM_HEIGHT,self.BOTTOM_DIA, self.BOLT_LENGTH+0.2)
        bpy.ops.object.select_all(action='DESELECT')
        self.diff_obj(up1,hole)
        self.diff_obj(board,hole)
        hole.select_set(True)
        bpy.ops.object.delete()

        self.rotate_object(up1)

        #bpy.ops.object.select_all(action='DESELECT')

        #self.diff_obj(up1,middle)
        #bpy.ops.object.select_all(action='DESELECT')

        #l_cyl.select_set(True)
        #bpy.ops.object.delete()

        for bolt in bolt_list_1:
            self.rotate_object(bolt)
            self.save_modell(bolt)
            
        extension_zone, bolt_list_2 = self.create_up(length_relativ, extension=True)
        self.rotate_object(extension_zone)
        extension_zone.name = "Cover"
        extension_zone["motor_id"] = self.motor_id
        self.save_modell(extension_zone)
        
        for bolt in bolt_list_2:
            self.rotate_object(bolt)
            self.save_modell(bolt)
        
        extension_zone_1 = self.combine_all_obj(extension_zone,bolt_list_2)
        ex_list=[extension_zone_1]
 

        gear_1 = self.combine_all_obj(board,[up1,middle])
        gear_1.name = "Gear_Container"
        gear_1["motor_id"] = self.motor_id
        self.save_modell(gear_1)

        gear_2 = self.combine_all_obj(gear_1,bolt_list_1, combine=self.mf_Combine)

        upper = self.combine_all_obj(gear_2, ex_list, combine=self.mf_Combine)
        x,y,z = upper.location
        self.calculate_bolt_position()
        upper["motor_id"] = self.motor_id
        gear = self.combine_all_obj(upper, bolt_list_middle, combine=self.mf_Combine)

        return upper
    

    
class Type_B(Motor_Creator):
    
    #4 covex cyl type B
    C1_LENGTH = 1.9
    C2_LENGTH = 2.7
    C3_LENGTH = 0.5
    C4_LENGTH = 0.2
    C5_LENGTH = 0.3
    type_B_Height_1 = 0
    type_B_Height_2 = 0
    bolt_random = False
    gear_bolt_num = 0
    bolt_position_1 = 0
    bolt_position_2 = 0
    bolt_position_3 = 0
    bolt_position_right = 0
    bolt_position_random = []
    bolt_rotation_1 = 0
    bolt_rotation_2 = 0
    bolt_ex_rotation = 0
    
    param = [
        "mf_Extension_Type_B",
        "mf_Gear_Orientation_1",

        "mf_Type_B_Height_1",
        "mf_Type_B_Height_2",
        
        "mf_Gear_Bolt_Random_B",
        "mf_Gear_Bolt_Position_B_1",
        "mf_Gear_Bolt_Position_B_2",
        "mf_Gear_Bolt_Position_B_3",

    ]

    def init_modify(self,factory: bpy.types.Operator):
            
            self.ex_type = factory.mf_Extension_Type_B                   
            self.gear_orientation = factory.mf_Gear_Orientation_1
       
            #####################################

            self.bolt_random = factory.mf_Gear_Bolt_Random_B
            self.gear_bolt_num = int(factory.mf_Gear_Bolt_Nummber_B)
            self.bolt_position_1 = factory.mf_Gear_Bolt_Position_B_1
            self.bolt_position_2 = factory.mf_Gear_Bolt_Position_B_2
            self.bolt_position_3 = factory.mf_Gear_Bolt_Position_B_3
            self.bolt_position_right = factory.mf_Gear_Bolt_Right_B
            #####################################
                           
            self.type_B_Height_1 = factory.mf_Type_B_Height_1
            self.type_B_Height_2 = factory.mf_Type_B_Height_2
            self.motor_param = [
                                "mf_Top_Type",
                                "mf_Extension_Type_B",
                                "mf_Gear_Orientation_1",
                                "mf_Mirror",
                                "mf_Color_Render",

                                "mf_Bottom_Length",
                                "mf_Sub_Bottom_Length",
                                "mf_Lower_Gear_Position",
                                "mf_Lower_Gear_XYZ",
                                "mf_Lower_Gear_Dia",
                                "mf_Lower_Gear_ContainerDia",
                                "mf_Lower_Gear_GearDia_Small",
                                "mf_Lower_Gear_GearDia_Large",
                                "mf_Lower_Gear_HoleDia",

                                "mf_Type_B_Height_1",
                                "mf_Type_B_Height_2",
                                "mf_Bit_Type",
                                "mf_Bolt_Orientation",   
                                "mf_Gear_Bolt_Right_B",
                                "mf_Gear_Bolt_Nummber_B",
                                "mf_Gear_Bolt_Random_B",
                                "mf_Gear_Bolt_Position_B_1",
                                "mf_Gear_Bolt_Position_B_2",
                                ] 
            if  self.gear_bolt_num == 3 and self.ex_type == 'mf_None':
                self.motor_param.append("mf_Gear_Bolt_Position_B_3") 
            if self.color_render:
                self.motor_param.append("mf_corrosion_Render")
                if self.rend_corrosion:
                    self.motor_param.append("mf_corrosion_Type_Bolt")
                    self.motor_param.append("mf_corrosion_Percent_Bolt")
                    self.motor_param.append("mf_corrosion_Type_Bottom")
                    self.motor_param.append("mf_corrosion_Percent_Bottom")



    def write_back(self,factory):
        if self.bolt_random:
            factory.mf_Gear_Bolt_Position_B_1 = self.bolt_rotation_1
            factory.mf_Gear_Bolt_Position_B_2 = self.bolt_rotation_2
            factory.mf_Gear_Bolt_Position_B_3 = self.bolt_ex_rotation
            factory.mf_Gear_Bolt_Right_B = self.bolt_position_right
                           
    ##############################################################################################################################
    ######################## Upper Part Type B ###################################################################################
    
    def create_Up2(self, bolt_positions,length_relativ):
        main_long = self.bottom_length 
        sub_long = self.sub_bottom_length
        radius = self.lower_gear_dia/2
        thickness = self.EXTENSION_THICKNESS
        mid_thick = 0.7
        lower_gear_position = self.lower_gear_position
        x = 0
        y = 0 - radius
        z = main_long + sub_long + lower_gear_position
        position = (x,y,z)
        x_init = position[0] + length_relativ/2

        y_b1 = bolt_positions[0][1] 
        z_b1 = bolt_positions[0][2] + self.BOLT_RAD

        y_b2 = bolt_positions[1][1] + self.BOLT_RAD
        z_b2 = bolt_positions[1][2] 

        y_b3 = bolt_positions[2][1]
        z_b3 = bolt_positions[2][2] -self.BOLT_RAD

        y_p0 = y_b3 + self.BOLT_RAD
        z_p0 = z_b3 + 2*self.BOLT_RAD +0.1

        y_p1 = position[1] - 3.5
        z_p1 = position[2] - 1.3

        y_p2 = position[1] - 3.5
        z_p2 = position[2] + 1

        y_p3 = position[1] - radius
        z_p3 = position[2] + 1

        verts_board_1 = [
            (x_init, y_b1, z_b1), #0
            (x_init + thickness , y_b1, z_b1), #1
            
            (x_init, y_b2, z_b2), #2
            (x_init + thickness, y_b2, z_b2), #3
            
            (x_init, y_b3, z_b3), #4
            (x_init + thickness, y_b3, z_b3), #5
            
        ]

        faces_board_1 = [
            [0,1,3,2],
            [2,3,5,4],
            [4,5,1,0],
            [0,2,4],
            [1,3,5],

        ]

        board_1 = self.add_mesh("bottom board_1", verts_board_1, faces_board_1)
        
        bpy.ops.mesh.primitive_cylinder_add(radius=0.75, depth=5, location=position)
        cly_cut = bpy.context.object

        bpy.ops.object.select_all(action='DESELECT')
        cly_cut.select_set(True)
        bpy.ops.transform.rotate(value=radians(90),orient_axis='X') 
        bpy.ops.transform.rotate(value=radians(90),orient_axis='Z') 

        self.diff_obj(board_1, cly_cut)
        cly_cut.select_set(True)
        bpy.ops.object.delete()

        verts_board_2 = [
            (x_init, y_p0, z_p0), #0
            (x_init + mid_thick, y_p0, z_p0), #1
            
            (x_init, y_p1, z_p1), #2
            (x_init + mid_thick, y_p1, z_p1), #3
            
            (x_init, y_p2, z_p2), #4
            (x_init + mid_thick, y_p2, z_p2), #5
            
            (x_init, y_p3, z_p3), #6
            (x_init + mid_thick, y_p3, z_p3), #7
            
            (x_init, y_b3, z_b3), #8
            (x_init + thickness, y_b3, z_b3), #9
            
            (x_init, y_b1, z_b1), #10
            (x_init + thickness , y_b1, z_b1), #11
                     
            (x_init + thickness, y_p1, z_p1), #12
            
            (x_init + thickness, y_p2, z_p2), #13
        ]

        faces_board_2 = [
            [0,1,3,2],
            [2,3,5,4],
            [4,5,7,6],
            [6,7,1,0],
            [0,2,4,6],
            [1,3,5,7],
            [6,7,12,2],
            [2,12,13,4],
            [4,13,11,10],
            [8,2,4,10],
            [9,12,13,11],
            [2,12,9,8]
            
        ]
        if self.ex_type == "mf_None":
            board_2 = None
        else:
            board_2 = self.add_mesh("bottom board_2", verts_board_2, faces_board_2)
        
        #Create Ring
        ring_position = (x_init+mid_thick/2, position[1], position[2])
        ring_1 = self.create_ring(ring_position, mid_thick, radius, radius-0.75)
        ring_2 = self.create_ring(ring_position, mid_thick, 0.9, 0.4)
        s_gear = self.combine_all_obj(ring_1, [ring_2])
        #s_gear = self.create_gear((x,y,z),lower_gear_radius,"hollow",length_relativ)
        s_gear.select_set(True)
        bpy.ops.transform.rotate(value=radians(90),orient_axis='Y') 
        
        
        extension = self.combine_all_obj(board_1, [board_2, s_gear])
        
        #Create bolt body
        bolt_list=[]
        for posi in bolt_positions:
            bolt = self.create_bolt((posi[0] + 0.45, posi[1],posi[2]), rotation = (radians(-90),'Y'), only_body = True)[0]
            #Hole
            bpy.ops.mesh.primitive_cylinder_add(radius=self.BOLT_RAD-0.05, depth=5, location=posi)
            cyl_tmp = bpy.context.object
            cyl_tmp.select_set(True)
            bpy.ops.transform.rotate(value=radians(90),orient_axis='Y')
            bpy.ops.object.select_all(action='DESELECT')
            self.diff_obj(extension, cyl_tmp)
            bpy.ops.object.select_all(action='DESELECT')
            cyl_tmp.select_set(True)
            bpy.ops.object.delete()
            bolt_list.append(bolt)

        up2 = self.combine_all_obj(extension, bolt_list)
        if self.color_render:
            self.rend_color(up2, "Plastic")
        return up2

    def create_Up1(self):
        init_x = self.init_x
        init_y = self.init_y
        #rotation, length_relativ, mirror = orient_dict[factory.mf_Gear_Orientation]
        #length_relativ = 1
        #rotation, length_relativ, mirror = self.orient_dict[self.gear_orientation]
        length_relativ = 1.5

        rotation_s = (radians(-90),"Y")
        size = 1
        main_long = self.bottom_length * size

        sub_long = self.sub_bottom_length * size

        lower_gear_radius = self.lower_gear_dia/2
        lower_gear_position = self.lower_gear_position

   
        x = init_x
        y = init_y - lower_gear_radius
        z = main_long + sub_long + lower_gear_position

        #Create gear

        ring_1 = self.create_ring((x,y,z),length_relativ,lower_gear_radius, lower_gear_radius - 0.75)
        ring_2 = self.create_ring((x,y,z),length_relativ +0.5, 0.9, 0.4)
        s_gear = self.combine_all_obj(ring_1, [ring_2])
        

        #s_gear = self.create_gear((x,y,z),lower_gear_radius,"hollow",length_relativ)
        s_gear.select_set(True)
        bpy.ops.transform.rotate(value=radians(90),orient_axis='Y') 

        exte = self.create_gear_extension((x,y,z),length_relativ)
        up1 = self.combine_all_obj(s_gear, [exte])

        # Create Bolts
        x_bolt_init = x + length_relativ/2 - self.BOLT_LENGTH/2 + self.EXTENSION_THICKNESS + 0.1
        y_bolt_init = y + lower_gear_radius + 0.9*self.BOLT_RAD
        z_bolt_init = z 
        
        # Calculate the rotate (x,z axis)             
        if self.bolt_random:
            if self.ex_type ==  "mf_None":
                self.bolt_rotation_1 = random.uniform(210,225)#self.lower_gear_bolt_position_2
                self.bolt_rotation_2 = random.uniform(70,110)
            else:  
                self.bolt_rotation_1 = random.uniform(215,220)
                self.bolt_rotation_2 = random.uniform(80,100)

        else:
                self.bolt_rotation_1 = self.bolt_position_1
                self.bolt_rotation_2 = self.bolt_position_2

        y_bolt_1, z_bolt_1 = self.rotate_around_point((y,z),self.bolt_rotation_1,(y_bolt_init,z_bolt_init))
        bolt_1 = self.create_bolt((x_bolt_init, y_bolt_1,z_bolt_1), rotation = rotation_s)
        #Hole
        bpy.ops.mesh.primitive_cylinder_add(radius=self.BOLT_RAD-0.05, depth=5, location=(x_bolt_init, y_bolt_1,z_bolt_1))
        cyl_tmp = bpy.context.object
        cyl_tmp.select_set(True)
        bpy.ops.transform.rotate(value=rotation_s[0],orient_axis=rotation_s[1])
        bpy.ops.object.select_all(action='DESELECT')
        self.diff_obj(up1, cyl_tmp)
        bpy.ops.object.select_all(action='DESELECT')
        cyl_tmp.select_set(True)
        bpy.ops.object.delete()
        
        y_bolt_2, z_bolt_2 = self.rotate_around_point((y,z),self.bolt_rotation_2,(y_bolt_init,z_bolt_init))       
        bolt_2 = self.create_bolt((x_bolt_init, y_bolt_2,z_bolt_2), rotation = rotation_s) 
        #Hole
        bpy.ops.mesh.primitive_cylinder_add(radius=self.BOLT_RAD-0.05, depth=5, location=(x_bolt_init, y_bolt_2,z_bolt_2))
        cyl_tmp = bpy.context.object
        cyl_tmp.select_set(True)
        bpy.ops.transform.rotate(value=rotation_s[0],orient_axis=rotation_s[1])
        bpy.ops.object.select_all(action='DESELECT')
        self.diff_obj(up1, cyl_tmp)
        bpy.ops.object.select_all(action='DESELECT')
        cyl_tmp.select_set(True)
        bpy.ops.object.delete()
        
        z_bolt_3 = main_long + sub_long + self.bolt_position_right
        y_bolt_3 = self.FOUR_CYL_DIA + self.BOLT_RAD
        bolt_3 = self.create_bolt((x_bolt_init, y_bolt_3,z_bolt_3), rotation = rotation_s)
        #Hole
        bpy.ops.mesh.primitive_cylinder_add(radius=self.BOLT_RAD-0.05, depth=5, location=(x_bolt_init, y_bolt_3,z_bolt_3))
        cyl_tmp = bpy.context.object
        cyl_tmp.select_set(True)
        bpy.ops.transform.rotate(value=rotation_s[0],orient_axis=rotation_s[1])
        bpy.ops.object.select_all(action='DESELECT')
        self.diff_obj(up1, cyl_tmp)
        bpy.ops.object.select_all(action='DESELECT')
        cyl_tmp.select_set(True)
        bpy.ops.object.delete()
        
        bolt_shell_list = [bolt_1[0], bolt_2[0],bolt_3[0]]
        bolt_bit_list = [bolt_2[1],bolt_3[1],bolt_1[1]]
        
        if self.gear_bolt_num == 3:
            if self.bolt_random:
                self.bolt_ex_rotation = random.uniform(130,190)
            else:
                self.bolt_ex_rotation = self.bolt_position_3
            y_bolt_ex, z_bolt_ex = self.rotate_around_point((y,z),self.bolt_ex_rotation,(y_bolt_init,z_bolt_init))       
            
            bolt_ex = self.create_bolt((x_bolt_init, y_bolt_ex,z_bolt_ex), rotation = rotation_s)
            bolt_shell_list.append(bolt_ex[0])
            bolt_bit_list.append(bolt_ex[1])        


        upper_1 = self.combine_all_obj(up1, bolt_shell_list)

        #Internal Gear

        in_gear = self.create_internal_gear((x,y,z), length_relativ*0.7, lower_gear_radius*0.75, 30, thickness=0.8)
        in_gear.select_set(True)
        bpy.ops.transform.rotate(value=radians(90),orient_axis='Y') 
        bpy.context.view_layer.objects.active = in_gear
        in_gear.name = "Inner_Gear"

        ring_gear = self.create_ring((x,y,z),length_relativ*1.3, 0.75, 0.35)
        ring_gear.select_set(True)
        bpy.ops.transform.rotate(value=radians(90),orient_axis='Y') 
        self.combine_all_obj(in_gear,[ring_gear])
        in_gear.location = (x+0.1*length_relativ, y, z)
        self.rotate_object(in_gear)
        self.rend_color(in_gear, "Gear")
        self.save_modell(in_gear)
        self.IN_GEAR_1 = in_gear
        
        bpy.ops.mesh.primitive_cube_add(location=(x+length_relativ/2+5.05, y, z))
        bpy.ops.transform.resize(value=(5, 5, 8))
        cube_1 = bpy.context.object
        cube_1.name = 'cube1'
        self.diff_obj(upper_1,cube_1)
        cube_1.select_set(True)
        bpy.ops.object.delete()
        
        return upper_1, bolt_bit_list
    
    def create_gear_extension(self, position, length_relative):
        main_long = self.bottom_length 
        sub_long = self.sub_bottom_length
        radius = self.lower_gear_dia/2
        thickness = length_relative/2

        x_up = position[0]
        y_up = position[1] - radius
        z_up = main_long + sub_long + self.type_B_Height_1

        x_mid = x_up
        y_mid = position[1] + 0.1
        z_mid = position[2] + radius + self.BOLT_RAD*2

        x_low = position[0]
        y_low = 2.4
        z_low = main_long + sub_long + self.type_B_Height_2


        verts = [
            (x_up, y_up, z_up), #0
            (x_up + thickness, y_up, z_up), #1
            (x_up, y_up, position[2]-radius + 0.1), #2
            (x_up + thickness, y_up, position[2]-radius +0.1), #3
            (x_up, self.FOUR_CYL_DIA+0.3, main_long+sub_long+0.8), #4
            (x_up + thickness, self.FOUR_CYL_DIA+0.3, main_long+sub_long+0.8), #5
            (x_low, y_low, z_low), #6
            (x_low + thickness, y_low, z_low), #7
            (x_mid, y_mid, z_mid), #8
            (x_mid + thickness, y_mid, z_mid), #9
        ] 

        faces = [
            [0,1,3,2],
            [2,4,5,3],
            [4,5,7,6],
            [8,6,7,9],
            [0,8,9,1],
            [0,8,6,4,2],
            [1,9,7,5,3],
            

        ]
        board_bottom = self.add_mesh("bottom board", verts, faces)

        bpy.ops.mesh.primitive_cylinder_add(radius=radius/2, depth=5, location=position)
        cly_cut = bpy.context.object

        bpy.ops.object.select_all(action='DESELECT')
        cly_cut.select_set(True)
        bpy.ops.transform.rotate(value=radians(90),orient_axis='X') 
        bpy.ops.transform.rotate(value=radians(90),orient_axis='Z') 

        self.diff_obj(board_bottom, cly_cut)
        cly_cut.select_set(True)
        bpy.ops.object.delete()

        #Create end cylinder
        cyl_dia = 0.6
        x_cyl = x_up + thickness/2
        y_cyl = y_up + cyl_dia/2
        z_cyl = z_up - cyl_dia/2
        end_cly = self.create_ring((x_cyl,y_cyl,z_cyl), thickness, cyl_dia, 0.4)
        #end_cly.matrix_world @= mathutils.Matrix.Rotation(radians(90), 4, 'X')
        #end_cly.matrix_world @= mathutils.Matrix.Rotation(radians(90), 4, 'Z')
        end_cly.select_set(True)
        bpy.ops.transform.rotate(value=radians(90),orient_axis='X')         
        bpy.ops.transform.rotate(value=radians(90),orient_axis='Z') 
        end_cly.name = 'End_cylinder'

        bpy.ops.mesh.primitive_cylinder_add(radius=cyl_dia, depth=thickness+1, location=(x_cyl,y_cyl,z_cyl))
        tmp = bpy.context.object
        tmp.select_set(True)
        bpy.ops.transform.rotate(value=radians(90),orient_axis='X')         
        bpy.ops.transform.rotate(value=radians(90),orient_axis='Z') 
        self.diff_obj(board_bottom, tmp)
        tmp.select_set(True)
        bpy.ops.object.delete()


        #Create end cylinder
        x_cyl_2 = x_low + thickness/2
        y_cyl_2 = y_low - cyl_dia/2
        z_cyl_2 = z_low - cyl_dia/2
        end_cly_2 = self.create_ring((x_cyl_2,y_cyl_2,z_cyl_2), thickness, cyl_dia, 0.4)
        end_cly_2.select_set(True)
        bpy.ops.transform.rotate(value=radians(90),orient_axis='X')         
        bpy.ops.transform.rotate(value=radians(90),orient_axis='Z')  
        end_cly.name = 'End_cylinder'

        bpy.ops.mesh.primitive_cylinder_add(radius=cyl_dia, depth=thickness+1, location=(x_cyl_2,y_cyl_2,z_cyl_2))
        tmp = bpy.context.object  
        tmp.select_set(True)
        bpy.ops.transform.rotate(value=radians(90),orient_axis='X')         
        bpy.ops.transform.rotate(value=radians(90),orient_axis='Z') 
        self.diff_obj(board_bottom, tmp)
        tmp.select_set(True)
        bpy.ops.object.delete()

        extension = self.combine_all_obj(board_bottom,[end_cly,end_cly_2])
        if self.color_render:
            self.rend_color(extension, "Plastic")

        return extension

    def create_upper_part(self):
  
        init_x = self.init_x
        init_y = self.init_y
        length_relativ = 1.5
        main_long = self.bottom_length
        sub_long = self.sub_bottom_length
        lower_gear_radius = self.lower_gear_dia/2
        lower_gear_position = self.lower_gear_position

        middle, bolt_list_middle = self.create_middle()     

        upper_1, bolt_list = self.create_Up1()

        x = init_x
        y = init_y - lower_gear_radius
        z = main_long + sub_long + lower_gear_position

        cut_ring = self.create_ring((x + self.BOARD_THICKNESS*3, y, z),length_relativ,lower_gear_radius - self.BOARD_THICKNESS , lower_gear_radius *0.99)
        cut_ring.select_set(True)
        bpy.ops.transform.rotate(value=radians(90),orient_axis='Y') 
        self.diff_obj(upper_1, cut_ring)
        #self.diff_obj(middle, cut_ring)
        cut_ring.select_set(True)
        bpy.ops.object.delete()

        bpy.ops.mesh.primitive_cylinder_add(radius=self.FOUR_CYL_DIA/2, depth=50, location=(0,0,0))
        new_hole = bpy.context.object
        self.diff_obj(upper_1,new_hole)
        new_hole.select_set(True)
        bpy.ops.object.delete()

        self.rotate_object(upper_1)

        container = self.combine_all_obj(upper_1, [middle])
        container.name = 'Gear_Container' 
        container["motor_id"] = self.motor_id
 
        self.save_modell(container)

        bolt_position = []
        for bl in bolt_list:
            bolt_position.append(bl.location)
            
        extension_zone = self.create_Up2(bolt_position, 1.5)        
        extension_zone.name = "Cover"  
        self.rotate_object(extension_zone)
        
        extension_zone["motor_id"] = self.motor_id
        self.save_modell(extension_zone)  
            
        for bl in bolt_list:
            self.rotate_object(bl)
            self.save_modell(bl)
            
        for bl in bolt_list_middle:
            self.save_modell(bl)

        
        ex_list=[extension_zone]#

        

        up1 = self.combine_all_obj(container, bolt_list, combine=self.mf_Combine)
        
        upper  = self.combine_all_obj(up1, ex_list, combine=self.mf_Combine)
        x,y,z = upper.location
        self.calculate_bolt_position()
                
        gear = self.combine_all_obj(upper, bolt_list_middle, combine=self.mf_Combine)
        gear["motor_id"] = self.motor_id
        return gear
    
    def flip_object(self, object_rotate):
        x,y,z = object_rotate.location
        bpy.ops.object.select_all(action='DESELECT')
        object_rotate.select_set(True)
        if self.gear_Flip : 
            if self.gear_orientation in ['r0','r180']:
                bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(False, True, False))
                bpy.ops.transform.translate(value=(0,-2*y,0)) 
            else:
                
                bpy.ops.transform.mirror(orient_type='GLOBAL',constraint_axis=(True, False, False))
                bpy.ops.transform.translate(value=(-2*x,0,0))
        bpy.ops.object.select_all(action='DESELECT')
