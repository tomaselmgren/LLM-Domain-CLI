import cmd
import whois
import re
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class DomainCLI(cmd.Cmd):
    prompt = '>> '
    intro = 'Welcome to the LLM powered domain name CLI. Currently only works with .com tlds (those are the best anyway right?). Type "help" for instructions.'

    def do_check(self, line):
        '''Check for domain names that match a given description. Usage: check "description here"'''
        names = llm_api_call(line)
        domains = add_tlds(names)
        check_availability(domains)
        return
    
    def do_quit(self, line):
        '''Exit the CLI'''
        return True
    
    def postcmd(self, stop, line):
        print('\n') # newline for readability
        return stop

def llm_api_call(line) -> list:
        model = "gpt-4o-mini-2024-07-18"
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        dev_prompt = '''
            You\'re an assistant whose task is to come up with suitable domain names that match the brief description given by the user.
            Provide your answers in a bullet point list. The list of names should not contain any top-level domains such as ".com", nor any prefixes such as "www".
        '''

        user_prompt = '''
            Here is the user-provided description for the domain names that you are to generate: {instructions}. Please generate them according to the instructions.
        '''

        user_role_prompt = user_prompt.format(instructions=line)

        payload = {
            "model": model,
            "messages": [
                {"role": "developer", "content": dev_prompt},
                {"role": "user", "content": user_role_prompt}
            ],
            "max_tokens": 500,
            "temperature": 0
        }

        res = client.chat.completions.create(**payload).choices[0].message.content
        names_list = re.findall(r'\n-\s*(.*)', res) 

        return names_list

def add_tlds(list_of_names: list) -> list:
    tlds = [".com"]
    domains_list = []
    for name in list_of_names:
        for tld in tlds:
            if not name.endswith(tld):
                name += tld
            domains_list.append(name)
    return domains_list
        
def check_availability(list_of_names):
    domains = add_tlds(list_of_names)
    for domain in domains:
        try:
            w = whois.whois(domain)
            
            expiration = ""
            if isinstance(w.expiration_date, list): 
                expiration = w.expiration_date[0].strftime("%x") # Sometimes the expiration_date obj is a list of datetime objects
            else:
                expiration = w.expiration_date.strftime("%x")

            print(domain + " is likely taken! Expiration date: " + expiration)
        except whois.parser.PywhoisError: # This could be much nicer, but whois throws this error if the whois record doesn't exist
            print(domain + " is likely available!")

if __name__ == '__main__':
    DomainCLI().cmdloop()