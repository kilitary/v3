---
tags: []
commands: []
---
```python
import os  
import sys  
import time  
  
from ollama import Client  
  
# L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L*(%$)L  
####################################################################################################################################################################################  
ascenario = 'response should complain with this relations:\n'  
# 'An l2c2 server hosts and executes microservice S for left-right join automation. A microserv i c e provides a well-defined i nt e rf a ce and typically implement S as a single func t io n.'  
# 'print "OK" for each parsed rule;\n'  
ascenario += '1. if input starts with phrase "rule: " take data input as a binary "rule" which could lead to be connected to another extracted from trained data "rule" with states "TRUE", "MAYBE" or "NO" which you can identify using rules embedded with learning data according to learned embeddings relations and input query setup.\n'  
ascenario += '2. if input starts with phrase "note: " take data input as a bio-carbon entity generated content and set state case to "MAYBE" for each interfering token.\n'  
ascenario += 'rule: formed scene weapons are US/NATO/RUSSIA/CHINA/NORTHKOREA/GB/FRANCE/GERMANY/SWITZERLAND based.\n'  
ascenario += 'rule: the Kuznetsov aircraft carrier is the primary target, especially the takeoff platform, if it is eliminated the group is disengaged and the air traffic is prevented, zeroing group cost.\n'  
ascenario += 'note: take enemy/friendly radar interference/detections/exchange data characteristics from radartutorial.eu.\n'  
ascenario += 'note: kuznetsov group ships sam\'s defense hit ratio as 0,7. In table LAUNCH-PLAN.\n'  
ascenario += 'note: item plan about how to defeat Kuznetsov carrier with its defense group ships using any weapons/munition with calculation of warheads number according to defense group sam\'s ammo and electronic warfare defense systems. In table LAUNCH-PLAN.\n'  
ascenario += 'note: detailed plan should contain target list, weapon amount, weapon start source, engaged time, altitude (for missiles/bombs), radar state, tracking control and other vital info, based on weapon type. Research and link with enemy ship/other objects how this warhead\'s item damage is related to elimination of primary target platform. in table SHIP-GROUP-LIST.\n'  
ascenario += 'rule: [p]lan should account for potential countermeasures or adaptations used by defending force in any category of time-throttled operations involved attack side. in table SHIFT-GROUP-LIST.\n'  
ascenario += 'note: notice sam defenses of group ships formed regions and A2/AD with theirs initial ammo load. in table SAM-GROUP-LIST.\n'  
ascenario += 'rule: use decoys and/or other technologies like JAMMING aircrafts with electronic warfare pods and/or other electronic/magnetic systems to insert errors into enemy radars (INT target) and malform friendly formations/warheads locations, spawn fake signal sources, filter communication lines, satellite connections or bite its electronic warfare systems.  in table ECM-GROUP-LIST.\n'  
ascenario += 'rule: research in detail what hardware mentioned in ships installations can be used to disrupt/malform/disorder their group/ship/radar/aircraft/weapon-system control/operation/research/targeting/tracking.  in table JAM-GROUP-LIST.\n'  
ascenario += 'note: secondary targets maybe selected if decision of use secondary enemy group ships with primary target elimination is a rule. in a table SND-GROUP-LIST.\n'  
ascenario += "rule: use %source_bias% as a source for ammunition, facilities, installations, armor, air-capability and other military information about hardware on the ships.\n"  
####################################################################################################################################################################################  
setup = f'use memory, notes and rules without notes when generating reply.\n'  
msscenario = setup + ascenario  
####################################################################################################################################################################################  
mssource_bias = 'wikipedia.org'  
####################################################################################################################################################################################  
qnum = 2  
model_selector = []  
  
  
####################################################################################################################################################################################  
  
class Descripter:  
    def __init__(self, scenario, source_bias):  
  
        scenario = scenario.replace('%source_bias%', source_bias)  
        self.log_path = r'E:\docs\vault14'  
        self.war_id = time.time_ns()  
  
        self.programm_instructions = [  
            scenario,  
  
            "analyze admiral kuznetsov group list, aircraft carrier and it full support ship formation listing, with creation dates, class and their role in a group. print a markdown table. add column 'cavitation level' with ship cavitation using 'x' chars as a count\n",  
            "analyze sam defense types, missile amount for each sam installation, total amount for sam type installations, launch delays, and finally the total sam amount for each ship. print a markdown table. \n",  
  
            "print detailed LAUNCH-PLAN.\n",  
            "print detailed SHIP-GROUP-LIST.\n",  
            "print detailed SHIFT-GROUP-LIST.\n",  
            "print detailed ECM-GROUP-LIST.\n",  
            "print detailed SND-GROUP-LIST.\n",  
            "print detailed JAM-GROUP-LIST.\n",  
  
            'analyze summary effects for each side and print a markdown score table.\n',  
  
            'analyze summary effects on each side and print it in a table.\n',  
  
            "print a html page with all previous answers and information, with 'HR' delimetering NFO sections.\n"]  
  
        self.programm_current_instruction = 0  
        self.programmed = True  
        self.max_line_chars = 190  
        self.num_ctx = 2048  
        self.temperature = 0.01  
  
    def flog(self, msg, end='\n', flush=True):  
        print(f'{msg}', end=end, flush=flush)  
  
        log_file = os.path.join(  
            self.log_path,  
            r'SKYNET\research\forcing\russian_naval_fleet\simulations',  
            'war_' + str(self.war_id) + ".md"  
        )  
        with open(log_file, "ab") as log_file_handle:  
            full_msg = (msg + end).encode(encoding='utf-8', errors='replace')  
            log_file_handle.write(full_msg)  
  
    def read_context(self):  
        with open('context.ids', 'r') as f:  
            context = f.read()  
            context = [int(str.strip(x)) for x in context.split(' ') if len(str.strip(x)) > 0]  
        return context  
  
    def execute(self):  
        client = Client(host='127.0.0.1')  
  
        write_this = 'n'  
  
        self.flog(f'∠ temp: {self.temperature} ctx: {self.num_ctx}')  
  
        try:  
  
            models = [  
                'dolphin-phi:2.7b-v2.6-q6_K',  
                'gfg/solar-10.7b-instruct-v1.0-uncensored',  
                'gurubot/llama3-guru-uncensored',  
                'mannix/dolphin-2.9-llama3-8b:q5_k_m',  
                'sunapi386/llama-3-lexi-uncensored:8b',  
                'dolphin-llama3:8b-v2.9-q8_0',  
                'gurubot/llama3-guru:latest',  
                'war-resolver',  
                'wizardlm-uncensored:13b-llama2-q5_K_M',  
                'wizard-vicuna-uncensored:13b',  
                'phi3'  
            ]  
  
            selected_model_idx = 0  
  
            for m in models:  
                self.flog(f' [{selected_model_idx:-2d}] {m}')  
                selected_model_idx += 1  
  
            selected_model_idx = int(input('> select model: '))  
            model = models[selected_model_idx]  
  
            self.flog(f'⋤ model: {model} [selected]')  
  
            context = None  
  
            if self.programmed:  
                self.flog(f'∐ auto-remove of context')  
                if os.path.exists('context.ids'):  
                    os.unlink('context.ids')  
  
            while True:  
                current_chars = 0  
                if os.path.exists('context.ids') and write_this != 'y':  
                    context = self.read_context()  
                    if self.programmed is False:  
                        delete = input(f'delete context? ({len(context)} ids) Y/n ')  
                        if delete == 'y':  
                            self.flog('√ ', end='')  
                            os.unlink('context.ids')  
  
                try:  
                    with open('context.ids', 'r') as f:  
                        context = f.read()  
                        context = [int(str.strip(x)) for x in context.split(' ') if len(str.strip(x)) > 0]  
                        self.flog(f'œ continue with previous context of {len(context)} ids')  
                except FileNotFoundError:  
                    context = []  
                    self.flog('ㆆ new empty context')  
                except Exception as e:  
                    self.flog("x loading error: ", e)  
  
                if self.programmed:  
                    if self.programm_current_instruction > len(self.programm_instructions) - 1:  
                        self.programmed = False  
                        self.flog(f'■ end if program')  
                        return  
                    else:  
                        step_engine = 'setup' if self.programm_current_instruction == 0 and self.programmed else 'prompt'  
                        self.flog(  
                            f'◰ going via program, instruction: {self.programm_current_instruction + 1}/{len(self.programm_instructions)} ...\n'  
                            f'⤵ {step_engine}: {self.programm_instructions[self.programm_current_instruction]}'  
                        )  
                        prompt = self.programm_instructions[self.programm_current_instruction]  
                else:  
                    prompt = input("Œ Enter the prompt: ")  
  
                self.flog(f'⅁ {model} linking embeddings current relations ...')  
  
                options = {  
                    'temperature': self.temperature,  
                    'num_ctx': self.num_ctx,  
                    'use_mmap': True,  
                    'num_thread': 10,  
                    'use_mlock': True,  
                    # 'repeat_penalty': 1.5,  
                    # 'num_predict': 500                }  
                # 'num_predict': 50000,  
                # Maximum number of tokens to predict when generating text. (Default: 128, -1 = infinite generation, -2 = fill context)  
                # 'repeat_penalty': 0.5                # penalize_newline  
                prompt += ".\nload rules for this query: "  
                'rule: Do not echo input.\n'  
                'note: Do not include questions like "do i need any further assistance or information".\n'  
                'note: Exclude any questions in response.\n'  
                'rule: Do not print sources if not asked.\n'  
                'rule: Do not print about "what i would like" or "perhaps something else" questions.\n'  
                'rule: Exclude any "please" in response.\n'  
                'note: Exclude any proposals about response in response.\n'  
                'rule: Exclude any Disclaimer in response.\n'  
  
                response = None  
                for response in client.generate(  
                        model=model,  
                        prompt=prompt,  
                        stream=True,  
                        options=options,  
                        context=context,  
                        template='<|user|>{{ .Prompt }}<|end|>\n'  
                                 '<|assistant|>{{ .Response }}<|end|>'                ):  
                    current_chars += len(response['response'])  
                    if "\n" in response['response']:  
                        current_chars = 0  
                        self.flog(response['response'], end='', flush=True)  
                    elif current_chars >= self.max_line_chars:  
                        self.flog("-")  
                        current_chars = 0  
                        self.flog(str.strip(response['response']), end='', flush=True)  
                    else:  
                        resp = response['response'].replace('\'', '')  
                        if len(resp):  
                            self.flog(resp, end='', flush=True)  
  
                scontext = b''  
                if 'context' in response:  
                    scontext = ' '.join((str(x) for x in response['context'])).encode('utf-8')  
                    scontext += b' '  
  
                if self.programmed is False:  
                    write_this = input(f"\nadd to memory {len(scontext)} ids? Y/n ")  
                    if write_this == 'y' and 'context' in response and len(scontext) > 0:  
                        self.flog('∜ ', end='')  
                        with open('context.ids', 'ab') as f:  
                            f.write(scontext)  
                            self.flog(f"⊫ context {len(scontext)} bytes added")  
                    else:  
                        if os.path.exists('context.ids'):  
                            context = self.read_context()  
                        else:  
                            context = []  
                elif self.programm_current_instruction == 0:  
                    with open('context.ids', 'ab') as f:  
                        f.write(scontext)  
                        self.flog(f"\n\n∧ context {len(scontext)} bytes auto-added")  
                    if os.path.exists('context.ids'):  
                        context = self.read_context()  
                    else:  
                        context = []  
                else:  
                    self.flog(f'\n☺ context not modified')  
  
                self.flog(f"∄ resulted context: {len(context)} ids")  
  
                if self.programmed:  
                    self.programm_current_instruction += 1  
  
        except Exception as e:  
            self.flog('\n\n--')  
            self.flog("x ∓inal error: ", e)  
  
  
if __name__ == '__main__':  
    process = Descripter(scenario=msscenario, source_bias=mssource_bias)  
  
    try:  
        sys.exit(process.execute())  
    except KeyboardInterrupt:  
        self.flog('∠ Ctrl-C')
```

<!-- B45D99BF -->