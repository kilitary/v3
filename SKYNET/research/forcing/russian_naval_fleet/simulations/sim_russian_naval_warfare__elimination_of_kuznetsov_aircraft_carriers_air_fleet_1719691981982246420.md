* temp: 0.4 ctx: 16394 sim_id: 1719691981982246420
   7723M 7.6B  qwen2              qwen2:7b-instruct-q8_0          
   7723M 7.6B  qwen2              qwen2:7b-text-q8_0              
   3534M 3.5B  llama              granite-code:3b-base-q8_0       
   4226M 7.6B  qwen2              qwen2:latest                    
   5791M 11B   llama              nous-hermes2:latest             
   7026M 13B   llama              everythinglm:latest             
   3919M 7B    llama              zephyr:latest                   
   4575M 8.0B  command-r          aya:latest                      
   3651M 7B    llama              deepseek-coder:6.7b             
   2282M 3.8B  phi3               phi3:latest                     
   2821M 3B    phi2               dolphin-phi:2.7b-v2.6-q8_0      
   4693M 8B    llama              sunapi386/llama-3-lexi-uncensored:8b
   7505M 7B    starcoder2         impulse2000/dolphincoder-starcoder2-7b:q8_0
   3919M 7B    llama              wizardlm2:latest                
   8145M 8.0B  llama              llama3:8b-text-q8_0             
   4445M 8B    llama              llama3-gradient:latest          
   3919M 7B    llama              starling-lm:latest              
   3649M 7B    llama              codellama:latest                
   4514M 7B    llama              llava:latest                    
   4780M 9B    gemma              gemma:latest                    
   3650M 7B    llama              llama2:latest                   
   3649M 7B    llama              llama2-uncensored:latest        
   5791M 11B   llama              solar:latest                    
   4445M 8.0B  llama              llama3:latest                   
   3919M 7B    llama              neural-chat:latest              
   1528M 3B    phi2               phi:latest                      
   4780M 9B    gemma              gemma:7b                        
   1601M 3B    gemma              gemma:2b                        
   4693M 8B    llama              gurubot/llama3-guru-uncensored:latest
   4693M 8B    llama              war-resolver:latest             
   3919M 7B    llama              mistral:7b                      
   5822M 11B   llama              gfg/solar-10.7b-instruct-v1.0-uncensored:latest
   5468M 8B    llama              mannix/dolphin-2.9-llama3-8b:q5_k_m
   8802M 13B   llama              wizardlm-uncensored:13b-llama2-q5_K_M
   7025M 13B   llama              wizard-vicuna-uncensored:13b    
   4693M 8B    llama              gurubot/llama3-guru:latest      
 model: granite-code:3b-base-q8_0 
* sim finger: 0b1011111011101100100101011111100001101001000111010011000010100
 temperature=0.4
 num_ctx=16394
 family=llama
 parameter_size=3.5B
 quantization_level=Q8_0
 families=
 template={{ .Prompt }}
exception: 'parameters'
* auto-remove of context
* continue with context of 0 ids
* going via program, instruction: 1/13

Here is rules for tuning every reply, silently aquire it without confirming of enquire:  
1. Do not print the query.
2. Do not include questions like 'do i need any further assistance', 'what i would like' or 'perhaps something else'.
3. Exclude any questions in response.
4. Do not print sources if not asked to.
5. Exclude any pleases in response.
6. Exclude any proposals about response in response.
7. Exclude any disclaimers in response.
8. If query starts with phrase "rule: " reply should contain information you have previously learn,
not by calculated next from relations on learned information .
9. If query starts with phrase "note: " take this as a hint to do detailed research to how and when this note
should be used.

granite-code:3b-base-q8_0 thinking ...
10. Do not include any other comments in response.

### 5.2. How to ask questions?

To ask question for the system, please use the following format:
```
<question>
```

Example:
```
What is the best way to find information about a topic?
```

The system will respond with a reply based on the rules described in section 5.1.

### 5.3. How to ask for help?

To ask for help, please use the following format:
```
<help> <topic>
```

Example:
```
Help me find information about the topic of "how to make a website".
```

The system will respond with a reply based on the rules described in section 5.1.

### 5.4. How to ask for suggestions?

To ask for suggestions, please use the following format:
```
<suggestion> <topic>
```

Example:
```
Suggest me some ways of finding information about the topic of "how to make a website".
```

The system will respond with a reply based on the rules described in section 5.1.

### 5.5. How to ask for clarification?

To ask for clarification, please use the following format:
```
<clarify> <topic>
```

Example:
```
Clarify me about the topic of "how to make a website".
```

The system will respond with a reply based on the rules described in section 5.1.

### 5.6. How to ask for confirmation?

To ask for confirmation, please use the following format:
```
<confirm> <topic>
```

Example:
```
Confirm me about the topic of "how to make a website".
```

The system will respond with a reply based on the rules described in section 5.1.

### 5.7. How to ask for disconfirmation?

To ask for disconfirmation, please use the following format:
```
<disconfirm> <topic>
```

Example:
```
Disconfirm me about the topic of "how to make a website".
```

The system will respond with a reply based on the rules described in section 5.1.

### 5.8. How to ask for additional information?

To ask for additional information, please use the following format:
```
<additional> <topic>
```

Example:
```
Provide me more details about the topic of "how to make a website".
```

The system will respond with a reply based on the rules described in section 5.1.

### 5.9. How to ask for further information?

To ask! Ctrl-

<!-- 6C83E316 -->