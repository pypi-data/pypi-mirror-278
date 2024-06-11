'''
Created on 2020. 3. 13.

@author: YJHeo
@author: GWKim

@edit: Jan 5 2022
    add shm_sys_access
    add some get data function
    get_last_emergency_info return int
'''

import sys, os, random
from struct import pack, unpack
import time

from neuromeka import IndyDCP3



class IndyCommand:
    def __init__(self, indydcp_version="v3", joint_dof=6):
        """ Select IndyDCP3 (v3) or IndyDCP (v2) """
        self.joint_dof = joint_dof

        self.indy_master = None

        if indydcp_version == "v3":
            self.indy_master = IndyDCP3("127.0.0.1")
        elif indydcp_version == "v2":
            self.indy_master = IndyDCP3("127.0.0.1")


    # Robot control state
    def get_robot_status(self):
        '''
        OP_SYSTEM_OFF = 0,
        OP_SYSTEM_ON = 1,
        OP_VIOLATE = 2,
        OP_RECOVER_HARD = 3,
        OP_RECOVER_SOFT = 4,
        OP_IDLE = 5,
        OP_MOVING = 6,
        OP_TEACHING = 7,
        OP_COLLISION = 8,
        OP_STOP_AND_OFF = 9,
        OP_COMPLIANCE = 10,
        OP_BRAKE_CONTROL = 11,
        OP_SYSTEM_RESET = 12,
        OP_SYSTEM_SWITCH = 13,
        OP_VIOLATE_HARD = 15,
        OP_MANUAL_RECOVER = 16,
        TELE_OP = 17,
        '''
        attr = ['ready', 'emergency', 'collision', 'error', 'busy', 'movedone',
                'home', 'zero', 'resetting', 'teaching', 'direct_teaching']
        res = {a: False for a in attr}
        val = self.indy_master.get_control_data()['op_state']
        if val == 5:
            res['ready'] = True
        elif val == 2 or val == 15:
            res['emergency'] = True
            res['error'] = True
        elif val == 8:
            res['collision'] = True
        elif val == 6 or val == 12:
            res['busy'] = True
        elif val == 3 or val == 4 or val == 16:
            res['resetting'] = True
        elif val == 7:
            res['teaching'] = True
            res['direct_teaching'] = True
        return res

    # Program state
    def get_program_state(self):
        program_state = ['stop', 'running', 'pause']
        val = self.indy_master.get_program_data()['program_state']
        res = {a: False for a in program_state}
        if val == 0:
            res['stop'] = True
        elif val == 1:
            res['running'] = True
        elif val == 2:
            res['pause'] = True
        return res


    def stop_motion(self):
        # > 300ms
        return self.indy_master.stop_motion(stop_category=2)

    def stop_emergency(self):
        # < 10ms
        self.indy_master.stop_motion(stop_category=0)

    def stop_safe(self):
        # ~ 250ms
        self.indy_master.stop_motion(stop_category=1)

    def reset_robot(self, hard_reset=False):
        if hard_reset:
            if __name__ == '__main__':
                self.indy_master.set_manual_recovery()
            # sems post

        else:
            self.indy_master.recover()
            # sems post
    # Joint/Servo command

    def get_collision_level(self):
        return self.indy_master.get_coll_sens_level()


    # Get robot data
    def get_rt_data(self):
        attr = ['time', 'task_time', 'max_task_time', 'compute_time', 'max_compute_time',
                'ecat_time', 'max_ecat_time', 'ecat_master_state', 'ecat_slave_num']
        time = self.indy_master.get_control_data()['running_hours']*3600 + self.indy_master.get_control_data()['running_mins']*60 + self.indy_master.get_control_data()['running_secs']
        val = [time, 0, 0, 0, 0, 0, 0, 0, 0]
        res = {}
        for att in attr:
            res[att] = val[attr.index(att)]
        return res

    def get_joint_pos(self):
        return self.indy_master.get_control_data()['q']

    def get_curr_joint_pos(self):
        return self.indy_master.get_control_state()['qdes']

    def get_joint_vel(self):
        return self.indy_master.get_control_data()['qdot']

    # New Jan 5
    def get_joint_vel_des(self):
        return self.indy_master.get_control_state()['qdotdes']

    # New Jan 5
    def get_joint_vel_ref(self):
        qdotdes = self.indy_master.get_control_state()['qdotdes']
        qdot = self.indy_master.get_control_state()['qdot']
        edot = [item1 - item2 for item1, item2 in zip(qdotdes, qdot)]
        return edot

    def get_task_pos(self):
        return self.indy_master.get_control_data()['p']

    # New Jan 5
    def get_curr_task_pos(self):
        return self.indy_master.get_control_state()['pdes']

    def get_task_vel(self):
        return self.indy_master.get_control_data()['pdot']

    # New Jan 5
    def get_task_vel_des(self):
        return self.indy_master.get_control_state()['pdotdes']

    # New Jan 5
    def get_task_vel_ref(self):
        pdotdes = self.indy_master.get_control_state()['pdotdes']
        pdot = self.indy_master.get_control_state()['pdot']
        evel = [item1 - item2 for item1, item2 in zip(pdotdes, pdot)]
        return evel


    def get_actual_torque(self):
        return self.indy_master.get_control_state()['tau_act']

    def get_external_torque(self):
        return self.indy_master.get_control_state()['tau_ext']

    def get_torque_ref(self):
        res = [0.0] * self.joint_dof
        return res

    # New Jan 5
    def get_overruns(self):
        return 0

    def get_joint_acc(self):
        return self.indy_master.get_control_state()['pddot']

    def get_joint_acc_des(self):
        return self.indy_master.get_control_state()['pddotdes']

    def get_task_acc(self):
        return self.indy_master.get_control_state()['pddot']

    def get_task_acc_des(self):
        return self.indy_master.get_control_state()['pddotdes']

    # Robot emergency data
    def get_last_emergency_info(self):
        attr = ['error_code', 'args_int', 'args_double', 'time']
        #     error_code = ['EMG button', 'Collision', 'Position limit', 'Vel/Acc limit', 'Motor state error',
        #                   'Torque limit', 'Connection lost', 'Path error', 'Endtool error', 'Singularity',
        #                   'Overcurrent', 'Near position limit', 'Near velocity limit', 'Near singularity',
        #                   'No error']
        val = self.indy_master.get_violation_data()
        violation_code = val['violation_code']
        violation_str = val['violation_str']
        if violation_code == 0x01 << (7 + 11): # EMG button:
            error_val = 0
        elif "Collision Detected" in violation_str: # Collision
            error_val = 1
        elif violation_code == 0x01 << (7 + 0): # Position limit
            error_val = 2
        elif violation_code == 0x01 << (2) or violation_code == 0x01 << (7 + 1) or violation_code == 0x01 << (7 + 3) or violation_code == 0x01 << (7 + 0): # Vel/Acc limit
            error_val = 3
        elif violation_code == 0x01 << (7 + 12 + 2) or violation_code == 0x01 << (7 + 12 + 4) or violation_code == 0x01 << (7 + 12 + 5) or violation_code == 0x01 << (7 + 12 + 6) or violation_code == 0x01 << (7 + 12 + 7): #Motor state error
            error_val = 4
        elif violation_code == 0x01 << (4) or violation_code == 0x01 << (7 + 2): #Torque limit
            error_val = 5
        elif violation_code == 0x01 << (7 + 12 + 1): #Connection lost
            error_val = 6
        elif violation_code == 0x01 << (5): #Singularity
            error_val = 9
        elif violation_code == 0x01 << (7 + 12 + 3): #Overcurrent
            error_val = 10
        elif violation_code == 0x01 << (1): #Near position limit
            error_val = 11
        elif violation_code == 0x01 << (2): #Near velocity limit
            error_val = 12
        elif violation_code == 0x01 << (6): #Near singularity
            error_val = 13
        else:
            error_val = -1

        res = {attr[0]: error_val,  # error_code[shm_val[0]],
               attr[1]: val['i_args'],
               attr[2]: val['f_args'],
               'violation_str': violation_str}
        return res

    def start_registered_default_program(self):
        self.command_program_logic(INDY_SHM_CLIENT_ADDR8_CMD_START_DEFAULT_PROGRAM)


    def get_motor_state(self):
        return self.indy_master.get_servo_data()['servo_actives']
    def get_temperature_data(self):
        return self.indy_master.get_servo_data()['temperatures']

    def get_float_variable_data(self):
        """
        Float Variables:
            [
                addr -> int32
                value -> float
            ]
        """
        return self.indy_master.get_float_variable()['variables']
    def set_float_variable_data(self, addr, value):
        self.indy_master.set_float_variable([{'addr':addr, 'value':value}])
    # # New Jan 24
    # def get_indycare_packtime(self):
    #     return self.shm_sys_access(NRMK_SHM_SYSTEM_ADDR_OVERRUN_COUNT, 8, 'Q')
