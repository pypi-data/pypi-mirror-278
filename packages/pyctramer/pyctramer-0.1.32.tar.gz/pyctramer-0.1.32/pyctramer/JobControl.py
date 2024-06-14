from .SubmitQC import run_step1
from .AnalyzeQC import run_step2
from .ConstructFF import run_step3
from .RunMD import run_step4
from .MarcusAA import run_step5
from .SpinBoson import run_step6
from .FGR import run_step7
from .Utilities import * 

def run_Marcus(dict_of_simulation):
    # prepare for quantum chemistry simulation 
    work_dir = dict_of_simulation['work_dir']
    # where we have the structure directory
    structure_dir = dict_of_simulation['structure_dir']
    # load the project folder 
    project = dict_of_simulation['project']
    # get case id for the simulation
    caseid = dict_of_simulation['caseid']
    # get job list
    case_id_list = separate_idlist(caseid)
    # get list of job control token 
    job_control  = init_job_control(case_id_list)
    print(job_control)
    # job infomation
    job_info = init_job_info(case_id_list)
    count = 0
    while check_job_unfinished(job_control):
        count +=1 
        job_control = check_job_status(job_control, dict_of_simulation, job_info)
        if count % 300 ==0:
            print(count,job_control)
        time.sleep(1)
    return 
        
def run_FGR(dict_of_simulation):
    # prepare for quantum chemistry simulation 
    work_dir = dict_of_simulation['work_dir']
    # where we have the structure directory
    structure_dir = dict_of_simulation['structure_dir']
    # load the project folder 
    project = dict_of_simulation['project']
    # get case id for the simulation
    caseid = dict_of_simulation['caseid']
    # get job list
    case_id_list = separate_idlist(caseid)
    # get list of job control token 
    job_control  = init_job_control(case_id_list)
    print(job_control)
    # job infomation
    job_info = init_job_info(case_id_list)
    count = 6
    while check_job_unfinished(job_control):
        count +=1 
        job_control = check_job_status(job_control, dict_of_simulation, job_info)
        if count % 300 ==0:
            print(count,job_control)
        time.sleep(1)
    return 
        
def check_job_status(job_control, dict_of_simulation, job_info):
    for i in range(len(job_control)):
        curr_step = job_control[i]['status'][0]
        if curr_step == 0 and job_control[i]['status'][curr_step+1] == 'unstarted':
            if dict_of_simulation['skip_QC']=='True':
                curr_step = 1
                job_control[i]['status'][curr_step] = 'finished'
            else:
                job_control = run_step1(i,job_control,dict_of_simulation)
                curr_step = 1
                job_control[i]['status'][curr_step] = 'running'
                print('curr_step',curr_step,'if current finished yet?',check_slurm_status(job_control[i]['QC_jobids']), '\n Current step is', job_control[i]['status'][curr_step])
            
        if curr_step == 1 and job_control[i]['status'][curr_step] == 'running':
            if check_slurm_status(job_control[i]['QC_jobids']):
                job_control[i]['status'][curr_step] = 'finished'
                #pass
            else: 
                pass
                #job_control[i]['status'][curr_step] = 'finished'
            if dict_of_simulation['skip_QC']=='True':
                job_control[i]['status'][curr_step] = 'finished'
            else:
                pass
              
            
        if curr_step == 1 and job_control[i]['status'][curr_step] == 'finished':
            job_control = run_step2(i,job_control,dict_of_simulation)
            curr_step = 2
            job_control[i]['status'][curr_step] = 'finished'
        
        if curr_step == 2 and job_control[i]['status'][curr_step] == 'finished':
            job_control = run_step3(i,job_control,dict_of_simulation, job_info)
            curr_step = 3
            job_control[i]['status'][curr_step] = 'finished'
        
        if curr_step == 3 and job_control[i]['status'][curr_step] == 'finished':
            job_control = run_step4(i,job_control,dict_of_simulation)
            curr_step = 4
            job_control[i]['status'][curr_step] = 'running'  
        
        if curr_step == 4 and job_control[i]['status'][curr_step] == 'running':
            if check_slurm_status(job_control[i]['MD_jobids']):
                print("job_control[i]['MD_jobids']",job_control[i]['MD_jobids'])
                job_control[i]['status'][curr_step] = 'finished'
            else: # returning false and doing nothing in this step
                #if round(time.time()) % 30 == 0:
                print("MD_jobids",job_control[i]['MD_jobids'] )
                pass
                #else :
                #    pass
                #pass
            
        if curr_step == 4 and job_control[i]['status'][curr_step] == 'finished':
            job_control = run_step5(i,job_control,dict_of_simulation,job_info)
            curr_step = 5
            job_control[i]['status'][curr_step] = 'finished'
                
        job_control[i]['status'][0] = curr_step
        
    return job_control