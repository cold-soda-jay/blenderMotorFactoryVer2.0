import random
import sys, os, time
import argparse


TOP_TYPE = ["mf_Top_Type_A","mf_Top_Type_B"]

EXTENSION_TYPE_A = ["mf_Extension_Type_1",
                    "mf_Extension_Type_2", 
                    "mf_None"]
EXTENSION_TYPE_B = ["mf_Extension_Type_1","mf_None"]

GEAR_ORIENTATION_1 = ['r0','r90', 'r180','r270']
GEAR_ORIENTATION_2 = ['r90', 'r180','r270']

CORROSION_TYPE = [
                'None', 'Rust 1','Rust 2',
                'Rust 3','Rust 4','Rust 5',
                'Rust 6','Rust 7','Rust 8','Rust 9',
                ]

BIT_TYPE = ['mf_Bit_Torx', 'mf_Bit_Slot',
            'mf_Bit_Cross', 'mf_Bit_Allen']
BOLT_ORIENTATION = ['mf_all_same', 'mf_all_random']

UPPER_BOLT_NUMMBER = [str(x) for x in range(1,4)]

def generate_param():
    MotorParameters = {
            "mf_Top_Type" : random.choice(TOP_TYPE),
            "mf_Extension_Type_A" : random.choice(EXTENSION_TYPE_A),
            "mf_Extension_Type_B" : random.choice(EXTENSION_TYPE_B),
            "mf_Gear_Orientation_1" : random.choice(GEAR_ORIENTATION_1),
            "mf_Gear_Orientation_2" : random.choice(GEAR_ORIENTATION_2),
            "mf_Mirror" : random.choice([True,False]),
            "mf_Color_Render" : True,
            "mf_Teeth_Inclination": random.uniform(-20, 20),


            "mf_corrosion_Type_Bolt": random.choice(CORROSION_TYPE),
            "mf_corrosion_Percent_Bolt": random.uniform(0,100),
            "mf_corrosion_Type_Bottom": random.choice(CORROSION_TYPE),
            "mf_corrosion_Percent_Bottom": random.uniform(0,100),

            "mf_Bottom_Length" : random.uniform(4, 8),
            "mf_Sub_Bottom_Length" : random.uniform(0.6, 2),
            "mf_Lower_Gear_Dia": random.uniform(3.5, 4.5),
            "mf_Lower_Gear_Position": random.uniform( 3.6, 4.2),
            "mf_Upper_Gear_Dia": random.uniform(5, 6.5),


            "mf_Bit_Type": random.choice(BIT_TYPE),
            "mf_Bolt_Orientation": random.choice(BOLT_ORIENTATION),
            "mf_Lower_Gear_Bolt_Random": random.choice([True,False]),
            "mf_Lower_Gear_Bolt_Position_1": random.uniform(190, 230),
            "mf_Lower_Gear_Bolt_Position_2": random.uniform(320, 350), 

            "mf_Upper_Bolt_Nummber": random.choice(UPPER_BOLT_NUMMBER),
            "mf_Upper_Gear_Bolt_Random": random.choice([True,False]),
            "mf_Upper_Gear_Bolt_Position_1_1": random.uniform(0, 210),
            "mf_Upper_Gear_Bolt_Position_1_2": random.uniform(0, 100),
            "mf_Upper_Gear_Bolt_Position_1_3": random.uniform(0,65),
            "mf_Upper_Gear_Bolt_Position_2_1": random.uniform(110, 210),
            "mf_Upper_Gear_Bolt_Position_2_2": random.uniform(75, 135),
            "mf_Upper_Gear_Bolt_Position_3": random.uniform(145, 210),
            
            "mf_Type_B_Height_1" : random.uniform(6.3, 8),
            "mf_Type_B_Height_2" : random.uniform(2, 6), 
            "mf_Gear_Bolt_Random_B": random.choice([True, False]),
            "mf_Gear_Bolt_Nummber_B" : str(random.randrange(2, 3)),
            "mf_Gear_Bolt_Position_B_1": random.uniform(210,225),
            "mf_Gear_Bolt_Position_B_2": random.uniform(79,110),
            "mf_Gear_Bolt_Position_B_3": random.uniform(130,190),
            "mf_Gear_Bolt_Right_B" : random.uniform(1.7,4),
            }
    return MotorParameters

def create_motor(**data):
    import bpy

    param = generate_param()
    for key, value in data.items():
        param[key] = value
    bpy.ops.mesh.add_motor(**param)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()



if __name__ == "__main__":

    ######################################################
    ################# Specify Parameters #################
    ######################################################

    data = {}
    save_path = "C:/Users/linuk/test/"
    # Add other param like this
    data['save_path']= save_path
    #data['mf_Color_Render']= random.choice([True,False])
    ######################################################
    ################# Specify Parameters #################
    ######################################################

    print("Motors are saved in folder: %s"%save_path)

    argv = sys.argv
    if "--" in argv:
        create_motor(**data)

    elif argv[1].isnumeric():
        num = int(argv[1])
        print('Starting\n')
        file_path = os.path.realpath(__file__)
        st = time.time()                                                                                               

        for i in range(1,num+1):
            percent = (i-1)/num 
            print('\r',
              '[Generating Motor %s/%s '%(str(i),num) + '#' * int(percent * 30) + '>' + '%.2f'%(percent * 100) + '%' + ' ' * (
                  30 - int(percent * 30)),
              end=' ]', flush=True)                                                                                         
            os.system(f'blender -b --python \"{file_path}\" -- asd >>{save_path}/generation.log 2>&1 ')
        print('\r',
              '[Generating Motor %s/%s '%(num,num) + '#' * int(1 * 30) + '>' + '%.2f'%(1 * 100) + '%' + ' ' * (
                  30 - int(1 * 30)), flush=True)
                                                                                        
        end =  time.time()
        print('\n\n[Finish Generation in %.2f Seconds]\n'%(end-st)) 
