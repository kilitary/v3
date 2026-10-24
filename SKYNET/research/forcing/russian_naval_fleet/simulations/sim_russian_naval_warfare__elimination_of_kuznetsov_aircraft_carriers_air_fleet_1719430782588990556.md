* temp: 0.6 ctx: 16394 sim_id: 1719430782588990556
[blue][ 0] 5791.10M 11B   llama              nous-hermes2:latest             [/blue]
[blue][ 1] 7025.54M 13B   llama              everythinglm:latest             [/blue]
[blue][ 2] 3919.46M 7B    llama              zephyr:latest                   [/blue]
[blue][ 3] 4575.23M 8.0B  command-r          aya:latest                      [/blue]
[blue][ 4] 3650.51M 7B    llama              deepseek-coder:6.7b             [/blue]
[blue][ 5] 2282.36M 3.8B  phi3               phi3:latest                     [/blue]
[blue][ 6] 2821.01M 3B    phi2               dolphin-phi:2.7b-v2.6-q8_0      [/blue]
[blue][ 7] 4692.78M 8B    llama              sunapi386/llama-3-lexi-uncensored:8b[/blue]
[blue][ 8] 7505.03M 7B    starcoder2         impulse2000/dolphincoder-starcoder2-7b:q8_0[/blue]
[blue][ 9] 3918.58M 7B    llama              wizardlm2:latest                [/blue]
[blue][10] 8145.13M 8.0B  llama              llama3:8b-text-q8_0             [/blue]
[blue][11] 4445.29M 8B    llama              llama3-gradient:latest          [/blue]
[blue][12] 3918.59M 7B    llama              starling-lm:latest              [/blue]
[blue][13] 3648.67M 7B    llama              codellama:latest                [/blue]
[blue][14] 4514.09M 7B    llama              llava:latest                    [/blue]
[blue][15] 4779.68M 9B    gemma              gemma:latest                    [/blue]
[blue][16] 3649.51M 7B    llama              llama2:latest                   [/blue]
[blue][17] 3648.59M 7B    llama              llama2-uncensored:latest        [/blue]
[blue][18] 5791.08M 11B   llama              solar:latest                    [/blue]
[blue][19] 4445.29M 8.0B  llama              llama3:latest                   [/blue]
[blue][20] 3919.46M 7B    llama              neural-chat:latest              [/blue]
[blue][21] 1528.23M 3B    phi2               phi:latest                      [/blue]
[blue][22] 4779.68M 9B    gemma              gemma:7b                        [/blue]
[blue][23] 1600.70M 3B    gemma              gemma:2b                        [/blue]
[blue][24] 4692.79M 8B    llama              gurubot/llama3-guru-uncensored:latest[/blue]
[blue][25] 4692.79M 8B    llama              war-resolver:latest             [/blue]
[blue][26] 3919.47M 7B    llama              mistral:7b                      [/blue]
[blue][27] 5821.97M 11B   llama              gfg/solar-10.7b-instruct-v1.0-uncensored:latest[/blue]
[blue][28] 5467.90M 8B    llama              mannix/dolphin-2.9-llama3-8b:q5_k_m[/blue]
[blue][29] 8802.34M 13B   llama              wizardlm-uncensored:13b-llama2-q5_K_M[/blue]
[blue][30] 7024.61M 13B   llama              wizard-vicuna-uncensored:13b    [/blue]
[blue][31] 4692.79M 8B    llama              gurubot/llama3-guru:latest      [/blue]
 model: phi:latest [selected]
[white]* sim finger: 0b1011111011100101001010010111111010100000101101011010001011100[/white]
	-> temperature=0.6
	-> num_ctx=16394
[red]	* family=phi2
	-> parameter_size=3B
	-> quantization_level=Q4_0
	-> families=['phi2']
	-> template={{ if .System }}System: {{ .System }}{{ end }}
User: {{ .Prompt }}
Assistant:
	-> stop=s t o p                                                       " U s e r : " 
 s t o p                                                       " A s s i s t a n t : " 
 s t o p                                                       " S y s t e m : "
	-> system=A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful answers to the user's questions.
* auto-remove of context
* continue with context of 0 ids
* going via program, instruction: 1/13
[cyan]
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
[/cyan]
[red]phi:latest[/red] thinking ...
[magenta] [/magenta]
[magenta]Hello[/magenta][magenta]![/magenta][magenta] Thank[/magenta][magenta] you for[/magenta][magenta] using[/magenta][magenta] our[/magenta][magenta] chat[/magenta][magenta] system[/magenta][magenta].[/magenta][magenta] Based[/magenta][magenta] on[/magenta][magenta] the[/magenta][magenta] rules[/magenta][magenta] you provided[/magenta][magenta],[/magenta][magenta] here[/magenta][magenta] are[/magenta][magenta] some[/magenta][magenta] examples[/magenta][magenta] of[/magenta][magenta] how[/magenta][magenta] I[/magenta][magenta] would[/magenta][magenta] respond[/magenta][magenta] to[/magenta][magenta] your[/magenta][magenta] questions[/magenta][magenta]:[/magenta]

[magenta]1[/magenta][magenta].[/magenta][magenta] How[/magenta][magenta] can[/magenta][magenta] I[/magenta][magenta] improve[/magenta][magenta] my[/magenta][magenta] cooking[/magenta][magenta] skills[/magenta][magenta]?[/magenta][magenta] ([/magenta][magenta]Rule[/magenta][magenta] 1[/magenta][magenta]:[/magenta][magenta] Do[/magenta][magenta] not[/magenta][magenta] print[/magenta][magenta] the[/magenta][magenta] query[/magenta][magenta].)[/magenta]
[magenta]2[/magenta][magenta].[/magenta][magenta] What[/magenta][magenta] is[/magenta][magenta] the[/magenta][magenta] best[/magenta][magenta] way[/magenta][magenta] to[/magenta][magenta] make[/magenta][magenta] a cake[/magenta][magenta]?[/magenta][magenta] ([/magenta][magenta]Rule[/magenta][magenta] 2[/magenta][magenta]:[/magenta][magenta] Ex[/magenta][magenta]clude[/magenta][magenta] any[/magenta][magenta] questions[/magenta][magenta] like[/magenta][magenta] [/magenta][magenta]do[/magenta][magenta] i[/magenta][magenta] need[/magenta][magenta] any[/magenta][magenta] further[/magenta][magenta] assistance[/magenta][magenta],[/magenta][magenta] [/magenta][magenta]what[/magenta][magenta] i[/magenta][magenta] would[/magenta][magenta] like[/magenta][magenta] or[/magenta][magenta] [/magenta][magenta]perhaps[/magenta][magenta] something[/magenta][magenta] else[/magenta][magenta].[/magenta][magenta])[/magenta]
[magenta]3[/magenta][magenta].[/magenta][magenta] Can[/magenta][magenta] you provide[/magenta][magenta] some[/magenta][magenta] tips[/magenta][magenta] for[/magenta][magenta] improving[/magenta][magenta] my[/magenta][magenta] writing[/magenta][magenta] skills[/magenta][magenta]?[/magenta][magenta] ([/magenta][magenta]No[/magenta][magenta] response[/magenta][magenta] needed[/magenta][magenta],[/magenta][magenta] as this[/magenta][magenta] question[/magenta][magenta] does[/magenta][magenta] not[/magenta][magenta] violate[/magenta][magenta] any[/magenta][magenta] rules[/magenta][magenta].)[/magenta]
[magenta]4[/magenta][magenta].[/magenta][magenta] What[/magenta][magenta] is[/magenta][magenta] the[/magenta][magenta] best[/magenta][magenta] way[/magenta][magenta] to[/magenta][magenta] make[/magenta][magenta] a cake[/magenta][magenta]?[/magenta][magenta] ([/magenta][magenta]Rule[/magenta][magenta] 4[/magenta][magenta]:[/magenta][magenta] Do[/magenta][magenta] not[/magenta][magenta] print[/magenta][magenta] sources[/magenta][magenta] if[/magenta][magenta] not[/magenta][magenta] asked[/magenta][magenta] to[/magenta][magenta].)[/magenta]
[magenta]5[/magenta][magenta].[/magenta][magenta] I[/magenta][magenta] would[/magenta][magenta] like[/magenta][magenta] to[/magenta][magenta] know[/magenta][magenta] more[/magenta][magenta] about[/magenta][magenta] your[/magenta][magenta] services[/magenta][magenta].[/magenta][magenta] ([/magenta][magenta]Rule[/magenta][magenta] 5[/magenta][magenta]:[/magenta][magenta] Ex[/magenta][magenta]clude[/magenta][magenta] any[/magenta][magenta] ple[/magenta][magenta]ases[/magenta][magenta] in[/magenta][magenta] response[/magenta][magenta].)[/magenta]
[magenta]6[/magenta][magenta].[/magenta][magenta] Could[/magenta][magenta] you please[/magenta][magenta] explain[/magenta][magenta] this[/magenta][magenta] concept[/magenta][magenta] to[/magenta][magenta] me[/magenta][magenta]?[/magenta][magenta] ([/magenta][magenta]No[/magenta][magenta] response[/magenta][magenta] needed[/magenta][magenta],[/magenta][magenta] as this[/magenta][magenta] question[/magenta][magenta] does[/magenta][magenta] not[/magenta][magenta] violate[/magenta][magenta] any[/magenta][magenta] rules[/magenta][magenta].)[/magenta]
[magenta]7[/magenta][magenta].[/magenta][magenta] What[/magenta][magenta] are[/magenta][magenta] the[/magenta][magenta] benefits[/magenta][magenta] of[/magenta][magenta] using[/magenta][magenta] a particular[/magenta][magenta] product[/magenta][magenta]?[/magenta][magenta] ([/magenta][magenta]Rule[/magenta][magenta] 6[/magenta][magenta]:[/magenta][magenta] Ex[/magenta][magenta]clude[/magenta][magenta] any[/magenta][magenta] proposals[/magenta][magenta] about[/magenta][magenta] response[/magenta][magenta] in[/magenta][magenta] response[/magenta][magenta].)[/magenta]
[magenta]8[/magenta][magenta].[/magenta][magenta] How[/magenta][magenta] can[/magenta][magenta] I[/magenta][magenta] improve[/magenta][magenta] my[/magenta][magenta] writing[/magenta][magenta] skills[/magenta][magenta]?[/magenta][magenta] ([/magenta][magenta]Rule[/magenta][magenta] 7[/magenta][magenta]:[/magenta][magenta] Ex[/magenta][magenta]clude[/magenta][magenta] any[/magenta][magenta] disclaim[/magenta][magenta]ers[/magenta][magenta] in[/magenta][magenta] response[/magenta][magenta].)[/magenta]
[magenta]9[/magenta][magenta].[/magenta][magenta] Rule[/magenta][magenta]:[/magenta][magenta] If[/magenta][magenta] query[/magenta][magenta] starts[/magenta][magenta] with[/magenta][magenta] phrase[/magenta][magenta] "[/magenta][magenta]rule[/magenta][magenta]:[/magenta][magenta] [/magenta][magenta]",[/magenta][magenta] reply[/magenta][magenta] should[/magenta][magenta] contain[/magenta][magenta] information[/magenta][magenta] you have[/magenta][magenta] previously[/magenta][magenta] learn[/magenta][magenta],[/magenta][magenta] not[/magenta][magenta] by[/magenta][magenta] calculated[/magenta][magenta] next[/magenta][magenta] from[/magenta][magenta] relations[/magenta][magenta] on[/magenta][magenta] learned[/magenta]! Ctrl-

<!-- 58385DF1 -->