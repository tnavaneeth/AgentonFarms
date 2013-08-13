AgentonFarms
============

Action Language (AL) program on answer set programming with python interface.

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
# -----------------------------------------------------------------------------------------------------#

•	The python program (Agent_on_Farms.py) uses four files as its input.
  o	Farm.sm – Domain Description file.
  o	Farmplan.sm – Planner module.
  o	Diag.sm – Diagnosis module.
  o	Fprob_(Farm no).sm – Program instance files for each farm to process planning.
  
•	The interface program creates following intermediate files for its processing.
  o	Goal_(Farm no).sm – Goals generated as per the supplied program instance.
  o	Actions_(Farm no).sm – File contains all the actions retrieved from planner result.
  o	Fluents_(Farm no).sm – This file provides all the fluents obtained from planner result.
  o	Fdprob_(Farm no).sm – Program instance files for each farm to do diagnosis (i.eFprob_(Farm no).sm + observations)
  o	Diag_(Farm no).sm – Result of Diagnosis.
  
•	The program expects user to enter inputs as similar to example provided.
•	The clingo.exe can be anywhere but the interface program & input files are expected to be in same directory.

•	Program Flow :
  1.	Receiving clingo.exe path from user.
  2.	Display program instance (Ex: fprob_1.sm) and construct goals according to the instance. Save those goals in a separate file (Ex: goal_1.sm).
  3.	Planner module is called to generate a plan.
      a.	Files Farm.sm, farmplan.sm, fprob_(Farm no).sm, & goal_(Farm no).sm are given as inputs to Clingo to generate plan.
      b.	The fluents and actions of the generated plan are captured in two different files fluent_(Farm no).sm & actions_(Farm no).sm respectively.
      c.	The generated plan is displayed.
  4.	After planning, Observation module is called to get observations from the user.
  5.	If there are observations, then Think module is called to evaluate received observations.
      a.	First the observations are checked whether it is present in fluent file.
      b.	If it is not, then Diagnosis module is called. Otherwise, a message will be displayed that the observation is acceptable as per the plan.
  6.	Diagnosis module calls the solver to do diagnosis for the observation.
      a.	Farm.sm, Diag.sm, and actions_(Farm no).sm are provided as input.
      b.	Results of the diagnosis are captured in diag_(Farm no).sm.
