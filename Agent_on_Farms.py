# -----------------------------------------------------------------------------------------------------#
#                                                                                                      #
# AUTHOR     : NAVANEETHA KRISHNAN THIAGARAJAN                                                         #
# R# NUMBER  : R10493147                                                                               #
# COURSE     : CS 5331 / PLANNING & DIAGNOSIS IN DYNAMIC DOMAINS                                       #
#                                                                                                      #
# -----------------------------------------------------------------------------------------------------#
#                           ------------------------------------------------                           #
#                         / AGENT ON FARMLANDS : AN ACTION LANGUAGE MODULE /                           # 
#                         ------------------------------------------------                             #
#                                                                                                      #
#  ACTION LANGUAGE : AL (Translated in ASP)                                      INTERFACE : PYTHON    #
#  ----------------------------------------                                      ------------------    #
#                                                                                                      #
#  Agent controlled farmlands is considered as a domain here. Agent is responsible to maintain water-  #
#  level in farmlands. Water is assumed to be absorbed by the crops in two timesteps. So the agent     #
#  should supply water after every two steps (Persistance Action).Symptoms of the nutrients deficiency #
#  can also be percieved. According to the deficiency, weakness should be identified and corresponding #
#  manure should be applied. Suppose deficiency is identified and plants are not watere,then actions   #
#  for water supply & manure application occur parallel and cause the effects of both actions(Parallel #
#  actions).                                                                                           #
#                                                                                                      #
#  If manure is applied at a timestep, then neither water supply or opening resorvoir should not be    #
#  executed in the next time step(Heuristics). Breakage of reservoir door can happen exogenously and   #
#  impact the events of the domain(Exogenous action).                                                  #
#                                                                                                      #
#  INTERFACE PROGRAM :                                                                                 #
#  -------------------                                                                                 #
#                                                                                                      #
#  Purpose of this module to execute Observe-Think-Act loop.All to run same modules for more than      #
#  one domains of same kind.                                                                           #
#                                                                                                      #
#  PLANNER    - To generate a plan for given program instance as per described domain.                 #
#                                                                                                      #
#  OBSERVE    - To get the observations from the users valid as per generated plan.                    #
#                                                                                                      #
#  THINK      - To check whether observed fluent is valid as per generated plan. Otherwise diagnosis   #
#               module will be called.                                                                 #
#                                                                                                      #
#  DIAGNOSIS  - To find what could have gone wrong in the domain to cause observed fluent.             #
#                                                                                                      #
# -----------------------------------------------------------------------------------------------------#
import subprocess
import os
import shlex
import array
import string
import shutil

def main():
    # Retrieving clingo path
    global clingo_path
    clingo_path=raw_input('Enter clingo.exe path (Ex: c:\\users\\nathiaga\\clingo\\clingo.exe):')
    print "Path given :"+clingo_path+"\n"
    clingo_path=os.path.abspath(clingo_path)

    # Running the process for each farm
    for Farm_no in range(1,4):
        print " ************ Farm :"+str(Farm_no)+" ************* "
        print "\n"
        planner(Farm_no)
        Observe(Farm_no)

# Planner module to generate a plan                    
def planner(Farm_no):    
    
    # Name of the Program Instance
    Prog_instance = 'fprob_'+str(Farm_no)+'.sm'
    
    # Displaying Initial Conditons 
    print " ******** Program Instance ******** "
    f_instance = open('fprob_'+str(Farm_no)+'.sm', "r+")

    goal_stmt = "goal(T):-"    
    for k in f_instance.readlines():
        print k
        if "symptom" in k:
            if "-holds" not in k:
                goal_stmt=goal_stmt+'-'+k.strip()[:-3]+'T),'
    goal_stmt=goal_stmt+'step(T).'                            
    f_instance.close()
    print "\n"
    
    # Goal File Generation
    file_goal = open('goal_'+str(Farm_no)+'.sm',"w+")
    file_goal.write(goal_stmt.strip())
    file_goal.close()
    
    # Calling Clingo Planner Files
    process = subprocess.Popen([clingo_path,"farm.sm",'goal_'+str(Farm_no)+'.sm',"farmplan.sm",str(Prog_instance),"1"], \
                                      stderr=subprocess.PIPE,stdout=subprocess.PIPE)

    print " ******** Planning ******** "
    print "\n"
    if process.stderr:
        print process.stderr.readlines()
        
    if process.stdout:
        
        f1 = open('actions_'+str(Farm_no)+'.sm', "w+")
        f2 = open('fluents_'+str(Farm_no)+'.sm', "w+")
        
        
        for line in process.stdout.readlines():    
            
            #Conditions are not satisfied
            if "UNSATISFIABLE" in line:
                print " ERROR!!! Please check your domain description"
                break
            
            #Capturing Fluents & Actions
            fluents=shlex.split(line)   
            for j in fluents:
                
                if "occurs" in j:
                    f1.write(j+'.\n')
                    print j+'\n'
                elif "holds" in j:    
                    f2.write(j+'.\n')
        f1.close()
        f2.close()    
        print "\n"

# Module to recieve observation        
def Observe(Farm_no):
    
    print " ******** Observation ******** " 
    ans=raw_input('Do you observe anything(Yes/No)?')
    
    if ans.lower() == "yes":
        obs=raw_input("Enter your observation [Ex:obs(fluent(X),3)]:")               
        think(obs,Farm_no)
                
    elif ans.lower() == "no":
        pass
    else:
        print "Don't act smart!!"
    print "\n"
    
    
# Check observed fluent is there in the plan or not
def think(obs,Farm_no):
    
    check=0
    if obs[-1:] != '.':
        obs=obs+'.'
    
    # Checking whether observerd fluent is already present in generated plan
    observe=string.replace(obs,'obs','holds')
    file=open('fluents_'+str(Farm_no)+'.sm',"r+")
    lines=file.readlines()    
    
    for line in lines:
        
        if (str(line).strip() == str(observe).strip()):
           print ("plan works")
           check=1
           break
    file.close()   
        
    if check==0:
       prog_instance='fprob_'+str(Farm_no)+'.sm' 
       diag_instance='fdprob_'+str(Farm_no)+'.sm' 
       
       # Creation of Diagnosis instance
       shutil.copyfile(prog_instance,diag_instance)
       f3=open(diag_instance,"a+")
       f3.write("\n")
       if obs[-1:] != '.':
          obs=obs+'.' 
       f3.write(obs+'\n')
       current_timestep=obs[string.rindex(obs,',')+1:]
       f3.write("current("+current_timestep+"\n")
       f3.close()
       
       # Calling Diagnosis
       Diagnosis(Farm_no)

# Diagnosis module to find what has gone wrong                    
def Diagnosis(Farm_no):    
    
    print "\n"
    print " ******** Diagnosis ******** "
    # Calling Clingo with Diagnosis Files
    process = subprocess.Popen([clingo_path,"Farm.sm","diag.sm",'actions_'+str(Farm_no)+'.sm','fdprob_'+str(Farm_no)+'.sm',"1"], \
                                    stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    if process.stderr:
        print process.stderr.readlines()
    
    if process.stdout:
        
        f4 = open('diag_'+str(Farm_no)+'.sm', "w+")
        
        
        for line in process.stdout.readlines():    
            
            # Conditions are not satisfied
            if "UNSATISFIABLE" in line:
                print " ERROR!!! Please check your domain description"
                break
            
            # Capturing Diagnostics results
            results=shlex.split(line)
            for j in results:
                
                if "occurs" in j:
                    f4.write(j+'.\n')
                    print j+'.\n'
                
        f4.close()

                    
# Calling main module    
if __name__ == "__main__":
    main()
