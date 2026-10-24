* temp: 0.8 ctx: 16394 sim_id: 1719871058845991488
   3919M 7B    llama              zephyr:latest                   
   3919M 7B    llama              wizardlm2:latest                
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
* sim finger: 0b1011111011110001101011001110110100001111111011000001001000000
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
10. When responding to a request for clarification or further information, avoid repeating the original question in your reply. Instead, provide clear and concise answers that address the specific points raised in the query.
11. If the request requires additional context or background information, provide this in a separate paragraph rather than embedding it in the response to the original query.
12. Use active voice and avoid unnecessary jargon or technical terms that may be unfamiliar to the person making the request.
13. Where possible, provide examples or case studies to illustrate your points and help clarify any misunderstandings.
14. If you are unable to fulfill a specific request, explain why and suggest alternative approaches or resources that may be more helpful.
15. Always be polite and professional in your responses, even if the original query is unclear or difficult to interpret.
16. Avoid making assumptions about the person making the request, and instead, focus on addressing their specific needs and requirements.
17. If you are not entirely sure how to respond to a complex or technical query, it may be helpful to consult with a more experienced colleague or subject matter expert before providing your answer.
18. Always aim to provide high-quality responses that are accurate, insightful, and add value to the person making the request.

< context 480 ids auto-added
* continue with context of 480 ids
* going via program, instruction: 2/13
print typical admiral kuznetsov group ship formation with manufacture date, antiair defenses and formation role
zephyr:latest thinking ...
The Admiral Kuznetsov is a Russian multi-purpose aircraft-carrying heavy cruiser, the lead ship of her class. As part of a naval task force or strike group, she typically operates in a specific formation with other ships to maximize combat effectiveness and defense capabilities. Heres a typical Admiral Kuznetsov group ship formation with manufacture date, antiair defenses, and formation role:

1. Flagship: The Admiral Kuznetsov (Project 11435) - Manufactured in 1990, this cruiser serves as the flagship of the task force or strike group. Its primary antiair defense is the S-300VM Fort system, which can engage both aerial and surface targets simultaneously with high accuracy and lethality. The Admiral Kuznetsovs formation role is to provide overall command and control for the entire group.

2. Frigates (Project 11356): These ships are designed as air defense frigates, equipped with advanced radars and missiles like the P-800 Oniks anti-ship/anti-aircraft missile system and Shtil-1M vertical launch systems. They play a critical role in providing close-in air defense for the formation. The Slavistan (Project 11356) and Admiral Gorshkov (Project 11356) were both manufactured in the late 1980s.

3. Corvettes (Project 20500): These small, fast-moving ships specialize in anti-submarine warfare, providing a crucial layer of defense against enemy submarines. They also have air defense capabilities with the Pantsir-M1 air defense system. The Stoyky (Project 20500) and Mirazh (Project 20500) were both manufactured in the early 2010s.

4. Submarines: The task force or strike group may include a variety of submarine types, such as nuclear-powered ballistic missile submarines (SSBNs), nuclear-powered attack submarines (SSNs), and diesel-electric submarines (SSKs). These submarines provide crucial intelligence gathering, sea denial capabilities, and anti-submarine warfare defense.

5. Transport and Supply Ships: These ships are responsible for transporting personnel, equipment, and supplies to the group. They also play a critical role in search and rescue operations, medical support, and other logistical functions that ensure the operational readiness of the task force or strike group. 

Overall, the Admiral Kuznetsov group ship formation is designed to provide a layered defense against all types of threats, with each ship playing a critical role in achieving the missions objectives. The combination of air defense frigates, anti-submarine corvettes, submarines, and transport/supply ships creates a formidable naval force that can operate independently or as part of larger naval task forces.

< context 1186 ids auto-added
* continue with context of 1666 ids
* going via program, instruction: 3/13
research is Kuznetsov aircraft carriers takeoff platform is the primary target, print why and secondary suggestions of target on this ship.

zephyr:latest thinking ...
! Ctrl-

<!-- 73DF54EA -->