import psutil

def record_cpu_information():
    """
    this function is used to record the cpu's basic information

    Returns:
        store the cpuinformation into a txt file
    """
    Number_of_Cores_Used = 0
    cpu_information = {}
    cpu_information['each_core_percentage']=[]

    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        cpu_information['each_core_percentage'].append(int(percentage))
        if percentage != 0:
            Number_of_Cores_Used+=1
    cpu_information['number_of_cores_used'] = Number_of_Cores_Used
    if Number_of_Cores_Used == 0:
        cpu_information['mean_core_percent_usage']='0'

    else:
        cpu_information['mean_core_percent_usage'] = str(sum(cpu_information['each_core_percentage'])/Number_of_Cores_Used)+'%'
    #cpu_percentage.append(str(f"Total CPU Usage: {psutil.cpu_percent()}%"))
    #df = pd.DataFrame(cpu_information)
    #df.to_csv(output_path)
    return cpu_information
#if __name__ == "__main__":
    #output_path = 'testing/output_test_data/cpu_information.txt' #Output path
    #record_cpu_information(output_path)
    #df.to_csv('testing/output_test_data/cpu_information.txt')

#record_cpu_information()
