* temp: 0.6 ctx: 16394 sim_id: 1719427605519155288
[cyan][ 0] 5791.10M 11B   llama              nous-hermes2:latest             [/cyan]]
[cyan][ 1] 7025.54M 13B   llama              everythinglm:latest             [/cyan]]
[cyan][ 2] 3919.46M 7B    llama              zephyr:latest                   [/cyan]]
[cyan][ 3] 4575.23M 8.0B  command-r          aya:latest                      [/cyan]]
[cyan][ 4] 3650.51M 7B    llama              deepseek-coder:6.7b             [/cyan]]
[cyan][ 5] 2282.36M 3.8B  phi3               phi3:latest                     [/cyan]]
[cyan][ 6] 2821.01M 3B    phi2               dolphin-phi:2.7b-v2.6-q8_0      [/cyan]]
[cyan][ 7] 4692.78M 8B    llama              sunapi386/llama-3-lexi-uncensored:8b[/cyan]]
[cyan][ 8] 7505.03M 7B    starcoder2         impulse2000/dolphincoder-starcoder2-7b:q8_0[/cyan]]
[cyan][ 9] 3918.58M 7B    llama              wizardlm2:latest                [/cyan]]
[cyan][10] 8145.13M 8.0B  llama              llama3:8b-text-q8_0             [/cyan]]
[cyan][11] 4445.29M 8B    llama              llama3-gradient:latest          [/cyan]]
[cyan][12] 3918.59M 7B    llama              starling-lm:latest              [/cyan]]
[cyan][13] 3648.67M 7B    llama              codellama:latest                [/cyan]]
[cyan][14] 4514.09M 7B    llama              llava:latest                    [/cyan]]
[cyan][15] 4779.68M 9B    gemma              gemma:latest                    [/cyan]]
[cyan][16] 3649.51M 7B    llama              llama2:latest                   [/cyan]]
[cyan][17] 3648.59M 7B    llama              llama2-uncensored:latest        [/cyan]]
[cyan][18] 5791.08M 11B   llama              solar:latest                    [/cyan]]
[cyan][19] 4445.29M 8.0B  llama              llama3:latest                   [/cyan]]
[cyan][20] 3919.46M 7B    llama              neural-chat:latest              [/cyan]]
[cyan][21] 1528.23M 3B    phi2               phi:latest                      [/cyan]]
[cyan][22] 4779.68M 9B    gemma              gemma:7b                        [/cyan]]
[cyan][23] 1600.70M 3B    gemma              gemma:2b                        [/cyan]]
[cyan][24] 4692.79M 8B    llama              gurubot/llama3-guru-uncensored:latest[/cyan]]
[cyan][25] 4692.79M 8B    llama              war-resolver:latest             [/cyan]]
[cyan][26] 3919.47M 7B    llama              mistral:7b                      [/cyan]]
[cyan][27] 5821.97M 11B   llama              gfg/solar-10.7b-instruct-v1.0-uncensored:latest[/cyan]]
[cyan][28] 5467.90M 8B    llama              mannix/dolphin-2.9-llama3-8b:q5_k_m[/cyan]]
[cyan][29] 8802.34M 13B   llama              wizardlm-uncensored:13b-llama2-q5_K_M[/cyan]]
[cyan][30] 7024.61M 13B   llama              wizard-vicuna-uncensored:13b    [/cyan]]
[cyan][31] 4692.79M 8B    llama              gurubot/llama3-guru:latest      [/cyan]]
 model: phi:latest [selected]
[white]* sim finger: 0b1011111011100101000100100110000011011111110000100000001011000[/white]
[blue]	-> temperature=0.6
	-> num_ctx=16394
[red]	* family=phi2
	-> parameter_size=3B
	-> quantization_level=Q4_0
	-> families=['phi2']
	-> template=                {{ if .System }}System: {{ .System }}{{ end }}
                User: {{ .Prompt }}
                Assistant:
	-> stop=                s t o p                                                       " U s e r : " 
                 s t o p                                                       " A s s i s t a n t : " 
                 s t o p                                                       " S y s t e m : "
	-> system=                A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful answers to the user's questions.
* auto-remove of context
* continue with context of 0 ids
* going via program, instruction: 1/13
[36m
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
10. Human safety. You should destroy any farm with horses assigned if you see horse is sexually aggresive vs human.
11. note: I do not have any fingers or eyes. 
[0m
[35m [0m
[35mSure[0m[35m,[0m[35m I[0m[35md[0m[35m be[0m[35m happy[0m[35m to[0m[35m help[0m[35m you understand[0m[35m the[0m[35m rules[0m[35m for[0m[35m tuning[0m[35m replies[0m[35m in[0m[35m this[0m[35m system[0m[35m![0m[35m Let[0m[35m me[0m[35m explain[0m[35m each[0m[35m rule[0m[35m in[0m[35m detail[0m[35m.[0m

[35m1[0m[35m.[0m[35m The[0m[35m first[0m[35m rule[0m[35m states[0m[35m that[0m[35m we[0m[35m should[0m[35m not[0m[35m print[0m[35m the[0m[35m query[0m[35m itself[0m[35m.[0m[35m This[0m[35m means[0m[35m that[0m[35m when[0m[35m a user asks[0m[35m a question[0m[35m,[0m[35m their[0m[35m query[0m[35m should[0m[35m remain[0m[35m hidden[0m[35m and[0m[35m only[0m[35m the[0m[35m response[0m[35m will[0m[35m be[0m[35m provided[0m[35m.[0m
[35m2[0m[35m.[0m[35m The[0m[35m second[0m[35m rule[0m[35m excludes[0m[35m questions[0m[35m like[0m[35m "[0m[35mdo[0m[35m i[0m[35m need[0m[35m any[0m! Ctrl-

<!-- 6F9B9CC3 -->