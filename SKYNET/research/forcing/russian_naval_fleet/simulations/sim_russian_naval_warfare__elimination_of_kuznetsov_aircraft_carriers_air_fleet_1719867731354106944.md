* temp: 0.8 ctx: 16394 sim_id: 1719867731354106944
   3919M 7B    llama              zephyr:latest                   
   3919M 7B    llama              wizardlm2:latest                
   8802M 13B   llama              wizardlm-uncensored:13b-llama2-q5_K_M
   7025M 13B   llama              wizard-vicuna-uncensored:13b    
   4693M 8B    llama              sunapi386/llama-3-lexi-uncensored:8b
   3919M 7B    llama              starling-lm:latest              
   5791M 11B   llama              solar:latest                    
   4226M 7.6B  qwen2              qwen2:latest                    
   7723M 7.6B  qwen2              qwen2:7b-text-q8_0              
   7723M 7.6B  qwen2              qwen2:7b-instruct-q8_0          
   1528M 3B    phi2               phi:latest                      
   2282M 3.8B  phi3               phi3:latest                     
   5791M 11B   llama              nous-hermes2:latest             
   3919M 7B    llama              neural-chat:latest              
   3923M 7.2B  llama              mistral:7b                      
   5468M 8B    llama              mannix/dolphin-2.9-llama3-8b:q5_k_m
   4514M 7B    llama              llava:latest                    
   4445M 8.0B  llama              llama3:latest                   
   8145M 8.0B  llama              llama3:8b-text-q8_0             
   4445M 8B    llama              llama3-gradient:latest          
   3650M 7B    llama              llama2:latest                   
   3649M 7B    llama              llama2-uncensored:latest        
   7505M 7B    starcoder2         impulse2000/dolphincoder-starcoder2-7b:q8_0
   4693M 8B    llama              gurubot/llama3-guru-uncensored:latest
   3534M 3.5B  llama              granite-code:3b-base-q8_0       
   5822M 11B   llama              gfg/solar-10.7b-instruct-v1.0-uncensored:latest
   4780M 9B    gemma              gemma:latest                    
   1601M 3B    gemma              gemma:2b                        
   7026M 13B   llama              everythinglm:latest             
   2821M 3B    phi2               dolphin-phi:2.7b-v2.6-q8_0      
   3651M 7B    llama              deepseek-coder:6.7b             
   3649M 7B    llama              codellama:latest                
   4575M 8.0B  command-r          aya:latest                      
   4780M 9B    gemma              gemma:7b                        
   4693M 8B    llama              war-resolver:latest             
   4693M 8B    llama              gurubot/llama3-guru:latest      
 model: zephyr:latest 
* sim finger: 0b1011111011110001100101001011011100100000001001011110001000000
 temperature=0.8
 num_ctx=16394
 family=llama
 parameter_size=7B
 quantization_level=Q4_0
 families=
 template={{- if .System }}
<|system|>
{{ .System }}
</s>
{{- end }}
<|user|>
{{ .Prompt }}
</s>
<|assistant|>

 stop=s t o p                                                       " < | s y s t e m | > " 
 s t o p                                                       " < | u s e r | > " 
 s t o p                                                       " < | a s s i s t a n t | > " 
 s t o p                                                       " < / s > "
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

zephyr:latest thinking ...
10. If the question includes specific details
<!-- 6F5690B9 -->