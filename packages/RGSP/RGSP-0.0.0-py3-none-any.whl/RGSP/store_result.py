
import csv
import getpass
import os
import platform
import socket
import sys
import transformrank
from numpy import mean, std
from transformrank import transform_unreverse
from cpuinfo import cpuinfo
from psutil import virtual_memory


def write_table(
                tablename,
                grid_result,
                start_time,
                end_time,
                seed,
                cpu_state,
                ml_classifier_name="",
                experiment_iden="experiment_iden",
                table="",
                test_auc = 0,
                ):


    id = 1
    implementation_language = "python "+sys.version
    outcome_type = table[-12:len(table)-4] if table else ""
    #app_file_path = os.getcwd()
    app_file_path = str(os.getcwd())+'\\'+str(sys.argv[0])
    full_dataset_name = table if table else ""
    host_name = socket.gethostname()
    user_id = getpass.getuser()
    #my_system = wmi.WMI().Win32_ComputerSystem()[0]
    #computer_manufacture = my_system.Manufacturer
    computer_manufacture = 'Dell Inc.'
    #computer_name = my_system.Name
    computer_name = platform.uname().node
    os_information = platform.platform()
    system_type = platform.uname().machine
    cpu_gpu_model = cpuinfo.get_cpu_info()['brand_raw']
    cpu_gpu = 'CPU'
    # if tf.config.experimental.list_physical_devices('GPU') == []:
    #     cpu_gpu = 'CPU'
    # else:
    #     cpu_gpu = 'GPU'
    processing_unit_speed = cpuinfo.get_cpu_info()['hz_advertised_friendly']
    ram = str(round(virtual_memory().total / 1024 / 1024 / 1024, 2))+'G'
    split_random_seed = seed
    combined_test_auc = 0

    # error handling
    if not isinstance(grid_result, dict):
        grid_result=grid_result.cv_results_
    available_attribute_list = grid_result.keys()
    # print(available_attribute_list)
    with open('result_template.csv', newline='') as level1Format:
        # gets the first line
        reader = csv.reader(level1Format)
        first_row = next(reader)
        data_write_first_row_csv(tablename,first_row)
    params = grid_result['params']
    split0_test_AUC_list = grid_result['split0_test_AUC']
    split1_test_AUC_list = grid_result['split1_test_AUC']
    split2_test_AUC_list = grid_result['split2_test_AUC']
    split3_test_AUC_list = grid_result['split3_test_AUC']
    split4_test_AUC_list = grid_result['split4_test_AUC']
    mean_test_AUC_list = grid_result['mean_test_AUC']
    std_test_AUC_list = grid_result['std_test_AUC']
    rank_test_AUC_list = grid_result['rank_test_AUC']
    split0_train_AUC_list = grid_result['split0_train_AUC']
    split1_train_AUC_list = grid_result['split1_train_AUC']
    split2_train_AUC_list = grid_result['split2_train_AUC']
    split3_train_AUC_list = grid_result['split3_train_AUC']
    split4_train_AUC_list = grid_result['split4_train_AUC']
    length = len(split0_test_AUC_list)# total number of parameter sets by one time grid_search


    if 'split0_test_f1' not in available_attribute_list:
    # if ml_classifier_name == "deep learning pytorch": # pytorch couldn't output auc and f1 same time
        split0_train_f1_list = [0] * length
        split1_train_f1_list = [0] * length
        split2_train_f1_list = [0] * length
        split3_train_f1_list = [0] * length
        split4_train_f1_list = [0] * length
        mean_train_f1_list = [0] * length
        std_train_f1_list = [0] * length
        split0_test_f1_list = [0] * length
        split1_test_f1_list = [0] * length
        split2_test_f1_list = [0] * length
        split3_test_f1_list = [0] * length
        split4_test_f1_list = [0] * length
        mean_test_f1_list = [0] * length
        std_test_f1_list = [0] * length
        rank_test_f1_list = [0] * length
    else:
        split0_train_f1_list = grid_result['split0_train_f1']
        split1_train_f1_list = grid_result['split1_train_f1']
        split2_train_f1_list = grid_result['split2_train_f1']
        split3_train_f1_list = grid_result['split3_train_f1']
        split4_train_f1_list = grid_result['split4_train_f1']
        mean_train_f1_list = grid_result['mean_train_f1']
        std_train_f1_list = grid_result['std_train_f1']
        split0_test_f1_list = grid_result['split0_test_f1']
        split1_test_f1_list = grid_result['split1_test_f1']
        split2_test_f1_list = grid_result['split2_test_f1']
        split3_test_f1_list = grid_result['split3_test_f1']
        split4_test_f1_list = grid_result['split4_test_f1']
        mean_test_f1_list = grid_result['mean_test_f1']
        std_test_f1_list = grid_result['std_test_f1']
        rank_test_f1_list = grid_result['rank_test_f1']

    mean_fit_time_list = grid_result['mean_fit_time']
    std_fit_time_list = grid_result['std_fit_time']
    mean_score_time_list = grid_result['mean_score_time']
    std_score_time_list = grid_result['std_score_time']
    mean_train_AUC_list = grid_result['mean_train_AUC']
    std_train_AUC_list = grid_result['std_train_AUC']

    number_of_cores_used = cpu_state['number_of_cores_used']
    mean_core_percent_usage = cpu_state['mean_core_percent_usage']
    # get all percent_auc_diff
    percent_auc_diff_list = []
    for i in range(length):
        difference = abs(mean_train_AUC_list[i] - mean_test_AUC_list[i]) / mean_test_AUC_list[i]
        percent_auc_diff_list.append(difference)
    percent_auc_diff_rank_list = transform_unreverse(percent_auc_diff_list)



    n = 0
    for param,split0_test_AUC,split1_test_AUC,split2_test_AUC,split3_test_AUC,split4_test_AUC, \
        mean_test_AUC, std_test_AUC, rank_test_AUC,percent_auc_diff,percent_auc_diff_rank,\
        split0_train_AUC,split1_train_AUC,split2_train_AUC,split3_train_AUC,split4_train_AUC, \
        mean_train_AUC,std_train_AUC, \
        split0_test_f1,split1_test_f1,split2_test_f1,split3_test_f1,split4_test_f1, \
        mean_test_f1, std_test_f1, rank_test_f1, \
        split0_train_f1,split1_train_f1,split2_train_f1,split3_train_f1,split4_train_f1, \
        mean_train_f1,std_train_f1, \
        mean_fit_time, std_fit_time, mean_score_time,std_score_time \
            in zip(params,split0_test_AUC_list,split1_test_AUC_list,split2_test_AUC_list,split3_test_AUC_list,split4_test_AUC_list,
                   mean_test_AUC_list, std_test_AUC_list, rank_test_AUC_list,percent_auc_diff_list,percent_auc_diff_rank_list,
                   split0_train_AUC_list,split1_train_AUC_list,split2_train_AUC_list,split3_train_AUC_list,split4_train_AUC_list,
                   mean_train_AUC_list,std_train_AUC_list,
                   split0_test_f1_list,split1_test_f1_list,split2_test_f1_list,split3_test_f1_list,split4_test_f1_list,
                   mean_test_f1_list, std_test_f1_list, rank_test_f1_list,
                   split0_train_f1_list,split1_train_f1_list,split2_train_f1_list,split3_train_f1_list,split4_train_f1_list,
                   mean_train_f1_list,std_train_f1_list,
                   mean_fit_time_list, std_fit_time_list, mean_score_time_list,std_score_time_list):
        if ml_classifier_name == "deep learning keras":
            if 'mstruct' not in param.keys():
                layer=[]

                neurons_seed=param['neurons_seed']
                hidden_layer=param['hidden_layers']
                base = param['base']
                hiddenunit_first_layer = param['hiddenunit_first_layer']
                layer.append(hiddenunit_first_layer)
                for i in range (hidden_layer):
                    layer.append(hiddenunit_first_layer*base*neurons_seed)
                param['layer']=layer
                del param['hiddenunit_first_layer']
                del param['hidden_layers']
                if param['optimizers'] == 'Adagrad':
                    del param['momentum']
            #57
        running_time2 = 5*(mean_fit_time+mean_score_time)

        record = ("%r!%f!%r!%r!%r!"
                  "%r!%r!%r!%r!%r!"
                  "%r!%r!%r!%r!%r!"
                  "%r!%r!%d!%r!%r!%r!%r!%r!"
                  "%f!%f!%f!%f!"
                  "%r!%f!"
                  "%f!%f!%f!%f!%f!"
                  "%f!%f!%f!%d!"
                  "%f!%d!"
                  "%f!%f!%f!%f!%f!"
                  "%f!%f!"
                  "%f!%f!%f!%f!%f!"
                  "%f!%f!%d!"
                  "%f!%f!%f!%f!%f!"
                  "%f!%f!%f!"
                  % (experiment_iden, id, ml_classifier_name, implementation_language,
                     outcome_type,
                     app_file_path, full_dataset_name, host_name, user_id, computer_manufacture,
                     computer_name, os_information, system_type, cpu_gpu, cpu_gpu_model,
                     processing_unit_speed, ram, number_of_cores_used, mean_core_percent_usage,
                     start_time.strftime("%m/%d/%Y %H:%M:%S"), end_time.strftime("%m/%d/%Y %H:%M:%S"),
                     (end_time - start_time).total_seconds() / length, running_time2,
                     mean_fit_time, std_fit_time, mean_score_time, std_score_time,
                     param, split_random_seed,
                     split0_test_AUC, split1_test_AUC, split2_test_AUC, split3_test_AUC, split4_test_AUC,
                     mean_test_AUC, combined_test_auc, std_test_AUC, rank_test_AUC,
                     percent_auc_diff, percent_auc_diff_rank,
                     split0_train_AUC, split1_train_AUC, split2_train_AUC, split3_train_AUC, split4_train_AUC,
                     mean_train_AUC, std_train_AUC,
                     split0_test_f1, split1_test_f1, split2_test_f1, split3_test_f1, split4_test_f1,
                     mean_test_f1, std_test_f1, rank_test_f1,
                     split0_train_f1, split1_train_f1, split2_train_f1, split3_train_f1, split4_train_f1,
                     mean_train_f1, std_train_f1,test_auc

                     ))
        id += 1
        row = record.split('!')
        data_write_csv(tablename,row)
        n+=1

# a function return (all information one split need with two level format)
def Getinformation_every_split(index,grid_result,split_random_seed,total_number,validation_array):
    """

    :return:
    :param index:
    :param grid_result:
    :param split_random_seed:
    :param total_number:
    :param validation_array:
    :return:
    """
    rank_data = []
    rank_onesplit_4 = []
    combined_test_auc = [0]*total_number
    mean_test_auc = grid_result[index]['mean_test_AUC']
    rank_mean_test_auc = transformrank.transform(mean_test_auc)
    validation_auc = validation_array[index]['validation_auc']
    rank_validation_auc = transformrank.transform(validation_auc)
    test_validation_average = [(a + b)/2 for a, b in zip(mean_test_auc, validation_auc)]
    rank_test_validation_average = transformrank.transform(test_validation_average)
    complete_information_one_split_10 = []
    complete_information_one_split_10.append(split_random_seed)
    complete_information_one_split_10.append(mean_test_auc)
    complete_information_one_split_10.append(grid_result[index]['std_test_AUC'])
    complete_information_one_split_10.append(combined_test_auc)
    complete_information_one_split_10.append(grid_result[index]['mean_train_AUC'])
    complete_information_one_split_10.append(grid_result[index]['std_train_AUC'])
    complete_information_one_split_10.append(validation_auc)
    complete_information_one_split_10.append(test_validation_average)
    complete_information_one_split_10.append(validation_array[index]['validation_f1'])
    complete_information_one_split_10.append(validation_array[index]['index_rank_validation_f1'])
    rank_onesplit_4.append(rank_mean_test_auc)
    rank_onesplit_4.append(combined_test_auc)
    rank_onesplit_4.append(rank_validation_auc)
    rank_onesplit_4.append(rank_test_validation_average)
    rank_data.append(rank_onesplit_4)
    rank_data.append(complete_information_one_split_10)
    return rank_data

def calculateAverage(element_name,total_number,grid_result,validation_array):
    final_list = []
    for i in range(total_number):
        five = []
        for j in range(5):
            if element_name in ['mean_fit_time','std_fit_time','mean_score_time','std_score_time'] :
                five.append(grid_result[j][element_name][i])
            else:
                five.append(validation_array[j][element_name][i])
        final_list.append(mean(five))
    return list(final_list)

def calculateStd(element_name,total_number,grid_result,validation_array):
    final_list = []
    for i in range(total_number):
        five = []
        for j in range(5):
            if element_name in ['mean_fit_time','std_fit_time','mean_score_time','std_score_time'] :
                five.append(grid_result[j][element_name][i])
            else:
                five.append(validation_array[j][element_name][i])
        final_list.append(std(five))
    return list(final_list)

def calculate_all_means(type,grid_result,total_number,combined_validation_auc,mean_validation_auc):
    final_list = []
    for i in range(total_number):
        mean_list = []
        for j in range(5):
            mean_list.append(grid_result[j]['mean_test_AUC'][i])
        mean_list.append(combined_validation_auc[i])
        mean_list.append(mean_validation_auc[i])
        if type == 'mean':
            final_list.append(mean(mean_list))
        else:
            final_list.append(std(mean_list))

    return list(final_list)
#
def data_write_first_row_csv(file_name,row):
    with open(file_name,'a+',newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        if isfirstline_empty(file_name):
            csvwriter.writerow(row)

def data_write_csv(file_name,row):
    with open(file_name, 'a+',newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the data rows
        csvwriter.writerow(row)

def data_write_csv_include_FI(file_name,row,FI_result):
    with open(file_name, 'a+',newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

#
def isfirstline_empty(file_name):# you need to create one new table
    with open(file_name,'r') as csvfile:
        reader = csv.reader(csvfile)
        try:
            first_row = next(reader)
        except StopIteration:
            print('no first row exists,added first row')
            first_row = []

        if first_row == []:
            return True
        else:
            return False






