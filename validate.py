import numpy as np

inputresultfile = "./data1/la01.fjs.txt"
inputfile = "./data/Dauzere_Data/01a.fjs"

# seq_count = 10 #代表每个工件工序数量
flag = 0
class Workpiece:
    def __init__(self):
        self.machine = -1
        self.dura_time = -1
        self.start_time = -1
        self.finish_time = -1

class Procedure:
    def __init__(self, machine=-1, time=-1):
        self.machine = machine
        self.time = time

# 首先读取标准数据集数据
with open(inputfile, 'r') as stream1:
    data_firstline=stream1.readline().split()
    job_count, machine_count = int(data_firstline[0]),int(data_firstline[1])
    procedure_count = []
    message = []
    T = []

    for i in range(job_count):
        data_line = stream1.readline().split() 
        procedure_count.append(int(data_line[0]))

        T_row = []
        message_row = []
        m = 1

        for j in range(procedure_count[i]):
            temp = int(data_line[m])
            T_row.append(temp)

            m = m+1
            procedure_list = []
            for k in range(temp):
                machine, time = map(int, data_line[m:m+2])
                procedure_list.append(Procedure(machine-1, time))
                m=m+2           
            message_row.extend(procedure_list)
        
        T.append(T_row)
        message.append(message_row)

# 然后读取优化结果表，存储于Ts表中
with open(inputresultfile, 'r') as stream1:
    data_firstline = stream1.readline().split()
    job_count, machine_count, Cmax = int(data_firstline[0]), int(data_firstline[1]), int(data_firstline[2])
    Ts =  [[Workpiece() for _ in range(procedure_count[i])] for i in range(job_count)]

    for i in range(machine_count):
        data_line = stream1.readline().split()
        machine_procedure_count = int(data_line[0])
        job_data_line = data_line[1:]
        t_data_line = job_data_line[2*machine_procedure_count:]

        for j in range(machine_procedure_count):
            Ts[int(job_data_line[2*j])][int(job_data_line[2*j+1])].dura_time = i #代表机器编号
            Ts[int(job_data_line[2*j])][int(job_data_line[2*j+1])].dura_time = int(t_data_line[2*j+1]) - int(t_data_line[2*j])
            Ts[int(job_data_line[2*j])][int(job_data_line[2*j+1])].start_time = int(t_data_line[2*j])
            Ts[int(job_data_line[2*j])][int(job_data_line[2*j+1])].finish_time = int(t_data_line[2*j+1])
    
    #判断是否缺少工件工序，判断工件工序前后约束是否正确
    for i in range(job_count):
        muti_machine_number = 0
        for j in range(procedure_count[i]):
            if Ts[i][j].dura_time == -1:
                flag = 1
                print("缺少工件，请仔细检查目前甘特图")
        
        for j in range(procedure_count[i]-1):
            if Ts[i][j+1].start_time < Ts[i][j].finish_time:
                flag = 2
                print("不满足工件前后加工顺序约束")
        
        for j in range(procedure_count[i]):
            if T[i][j]==1:
                if Ts[i][j].dura_time != message[i][j+muti_machine_number].time:
                    flag = 3
                    print("机器加工时间不对应")
                    break
            else:
                muti_flag = 0
                m = 0
                while m<T[i][j]:
                    if Ts[i][j].dura_time == message[i][j+muti_machine_number+m].time:  
                        muti_flag = 4
                        break
                    m = m+1
                if muti_flag !=4:
                    flag = 5
                    print("多机器部分加工时间不对应")
                    break
                muti_machine_number = muti_machine_number+T[i][j]-1

    if flag!=1 and flag!=2 and flag!=5:
        print("工件工序没有缺少且排产正确")
    # print(job_seq)