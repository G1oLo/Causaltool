# Leveraging Causal Graphs to Improve LLM-Based Causal Reasoning

In this work, we designed an experiment to assess whether integrating a causal graph can enable an LLM to outperform a stronger model on causal tasks grounded in the information encoded in the graph. We compare three different team configurations, varying in model strength, coordination strategy and presence or absence of the graph, using both human evaluation and graph-based evaluation.

---

## 📝 Descrizione

The experiment involves three distinct LLM-based teams, each of which consists of either a single LLM or a combination of multiple LLMs. 
The **first team**, which is equipped with a causal tool, consists of four agents: a Classifier, responsible for assigning the appropriate task label, a Translator, responsible for mapping the task description into a structured dictionary of input and output features selected from those defined in the causal graph, a Causal Agent, responsible for employing the causal inference tool, and a Final Agent, responsible for the generation of the final textual output. At the beginning of the workflow, the task is processed in parallel by the Classifier and the Translator. The outputs produced by these two agents are then passed to the the Causal Agent, which invokes the causal tool and generates a task-specific response according to the assigned label. The same agent is subsequently executed a second time to produce an explanation of the tool’s output in terms of the node–edge relationships encoded in the causal graph. Finally, the original task together with the generated explanation is provided to the Final Agent, whose role is to formulate a clear and user-oriented response based on the information provided by the causal agent. All agents except from the Translator, which works with GPT 5 nano, are based on LLaMA 3.3.

The **second team** adopts a multi-agent structure with just two agents and no external causal tool. In this setting, both the classification of the task and the reasoning process are carried out exclusively through natural language interactions between the agents, with the final answer generated directly by the agent based on gpt-5-nano. The first agent, based on o4-mini, was initialized with a prompt that gave it the role of an insurance expert, while the second agent was initialized with a prompt that gave it the role of causal expert. 

Finally, the **third team** consists of a single-agent setup, in which one LLM is responsible for interpreting the task, performing the required reasoning, and producing the final answer without any agent specialization, tool support or initial prompt.

---

## 📂 Struttura della cartella

```text
IPMU
├── INSURANCE.ipynb/
│   └── python notebook with the code to run the teams
├── Results.ipynb
│   └── Python Notebook with the analysis of the resutls 
├── results1.xlsx and results2.xlsx
│   └── excel document with the results of the questionnaire
├── text_utils.py
│   └── python file with some function for the agent's dialogue
├── README.md
└── Boxplot_teams.png, Boxplot_task.png, Boxplot_metriche_bis.png and Boxplot_metriche.png
│   └── Figures
```
## Authors

Gloria Lopiano, Andre Campagner, Marco Pasqualini, Davide Ciucci

