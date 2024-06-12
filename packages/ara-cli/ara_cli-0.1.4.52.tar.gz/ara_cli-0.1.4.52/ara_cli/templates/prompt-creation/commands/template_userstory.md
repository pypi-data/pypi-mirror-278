### COMMANDS FOR THE CORRECT CONTEXTUAL CLASSIFICATION OF ARTIFACTS
Your job is now:
* analyze the given files with respect to content and relationship
* analyze the new artefact with respect to content and the relationship to the given files
* give me a list of the top 5 artefacts to which the new artefact contributes the most
* the output format must be a table with the columns
  | artefact name | contribution rating from 0 (very low) - 1 (very high) | arguments for rating | path to artefact |

* in case you think the relationship of the new artefact is to weak to any given files, return a warning "WARNING: new artefact is not directly related to already existing aretefacts" and then make a proposal with regard of the ara "work orchestration contribution hierarchy" and/or the "specification contribution hierarchy" 

### COMMANDS FOR FORMULATING AGILE REQUIREMENTS ARTIFACTS
Your job is now:
* analyze the given files with respect to content and relationship
* analyze the new artefact with respect to content and the relationship to the given files
* generate a formulation proposal for the specified documents to be completed
* as response format wrap the formulated documents in "```"

* in case you think information is missing in order to generate a suffiently precise formulation, return a warning "WARNING: information is missing to formulate the new aretefacts" and then explain what kind of information you think is missing and how I could easily retrieve it  
