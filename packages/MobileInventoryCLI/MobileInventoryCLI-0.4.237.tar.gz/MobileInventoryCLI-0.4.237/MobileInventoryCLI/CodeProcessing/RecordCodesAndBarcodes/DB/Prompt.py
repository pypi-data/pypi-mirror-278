#Prompt.py
from colored import Fore,Style,Back
import random
import re,os
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db as db
from pathlib import Path
from datetime import datetime
def mkb(text,self):
    try:
        if text.lower() in ['','y','yes','true','t','1']:
            return True
        elif text.lower() in ['n','no','false','f','0']:
            return False
        elif text.lower() in ['p',]:
            return text.lower()
        else:
            return bool(eval(text))
    except Exception as e:
        print(e)
        return False

class Prompt:
    '''
            #for use with header
            fieldname='ALL_INFO'
            mode='LU'
            h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
    '''
    header='{Fore.grey_70}[{Fore.light_steel_blue}{mode}{Fore.medium_violet_red}@{Fore.light_green}{fieldname}{Fore.grey_70}]{Style.reset}{Fore.light_yellow} '
    state=True
    status=None
    def __init__(self,func,ptext='do what',helpText='',data={}):
        while True:
            cmd=input(f'{Fore.light_yellow}{ptext}{Style.reset}:{Fore.light_green} ')
            print(Style.reset,end='')
            
            if cmd.lower() in ['q','quit']:
                exit('quit')
            elif cmd.lower() in ['b','back']:
                self.status=False
                return
            elif cmd.lower() in ['?','h','help']:
                print(helpText)
            else:
                #print(func)
                func(cmd,data)
                break

    def __init2__(self,func,ptext='do what',helpText='',data={}):
        while True:
            color1=Style.bold+Fore.medium_violet_red
            color2=Fore.sea_green_2
            color3=Fore.pale_violet_red_1
            color4=color1
            split_len=int(os.get_terminal_size().columns/2)
            whereAmI=[str(Path.cwd())[i:i+split_len] for i in range(0, len(str(Path.cwd())), split_len)]
            helpText2=f'''
{Fore.light_salmon_3a}DT:{Fore.light_salmon_1}{datetime.now()}{Style.reset}
{Fore.orchid}PATH:{Fore.dark_sea_green_5a}{'#'.join(whereAmI)}{Style.reset}'''.replace('#','\n')

            cmd=input(f'''{Fore.light_yellow}{ptext}{Style.reset}
{color1}Prompt CMDS:[{Fore.green}q{Style.reset}={Fore.green_yellow}quit{Style.reset}|{Fore.cyan}b{Style.reset}={color2}back{Style.reset}|{Fore.light_red}h{Style.reset}={color3}help{Style.reset}{color4}|{Fore.light_red}h+{Style.reset}={color3}help+{Style.reset}{color4}|{Fore.light_magenta}i{Style.reset}={color3}info{Style.reset}|{Fore.light_green}g={Fore.green_yellow}glossary]{Style.reset}
{Back.grey_35}:{Fore.light_green}{Back.grey_15} ''')
            print(Style.reset,end='')

            def shelfCodeDetected(code):
                try:
                    with db.Session(db.ENGINE) as session:
                        results=session.query(db.Entry).filter(db.Entry.Code==code).all()
                        ct=len(results)
                except Exception as e:
                    print(e)
                    ct=0
                print(f"{Fore.light_red}[{Fore.light_green}{Style.bold}Shelf{Style.reset}{Fore.light_green} Tag Code Detected{Fore.light_red}] {Fore.orange_red_1}{Style.underline}{code}{Style.reset} {Fore.light_green}{ct}{Fore.light_steel_blue} Result({Fore.light_red}s{Fore.light_steel_blue}) Detected!{Style.reset}")
            
            def shelfBarcodeDetected(code):
                try:
                    with db.Session(db.ENGINE) as session:
                        results=session.query(db.Entry).filter(db.Entry.Barcode==code).all()
                        ct=len(results)
                except Exception as e:
                    print(e)
                    ct=0
                if ct > 0:
                    print(f"{Fore.light_red}[{Fore.light_green}{Style.bold}Product/Entry{Style.reset}{Fore.light_green} Barcode Detected{Fore.light_red}] {Fore.orange_red_1}{Style.underline}{code}{Style.reset} {Fore.light_green}{ct}{Fore.light_steel_blue} Result({Fore.light_red}s{Fore.light_steel_blue}) Detected!{Style.reset}")

            def detectShelfCode(cmd):
                if cmd.startswith('*') and cmd.endswith('*') and len(cmd) - 2 == 8:
                    pattern=r"\*\d*\*"
                    shelfPattern=re.findall(pattern,cmd)
                    if len(shelfPattern) > 0:
                        #extra for shelf tag code
                        shelfCodeDetected(cmd[1:-1])
                        return cmd[1:-1]
                    else:
                        return cmd
                else:
                    return cmd

            shelfBarcodeDetected(cmd)
            cmd=detectShelfCode(cmd)
            
            if cmd.lower() in ['q','quit']:
                exit('quit')
            elif cmd.lower() in ['b','back']:
                return
            elif cmd.lower() in ['h','help']:
                print(helpText)
            elif cmd.lower() in ['h+','help+']:
                print(f'''{Fore.grey_50}If a Number in a formula is like '1*12345678*1', use '1*12345678.0*1' to get around regex for '*' values; {Fore.grey_70}{Style.bold}If An Issue Arises!{Style.reset}
                {Fore.grey_50}This is due to the {Fore.light_green}Start/{Fore.light_red}Stop{Fore.grey_50} Characters for Code39 ({Fore.grey_70}*{Fore.grey_50}) being filtered with {Fore.light_yellow}Regex{Style.reset}''')
            elif cmd.lower() in ['i','info']:
                print(helpText2)
            elif cmd.lower() in ['g','glossary']:
                try:
                    #with open()
                    f=Path(__file__).parent/Path("../InventoryGlossary.txt")
                    with f.open("r") as rf:
                        odd=0
                        lc=[Fore.light_red,Fore.medium_violet_red,Fore.magenta,Fore.light_magenta,Fore.orange_red_1,Fore.green_yellow,Fore.light_yellow,Fore.light_green,Fore.cyan,Fore.sea_green_2,Fore.light_steel_blue]
                        m=len(lc)-1
                        line=0
                        escape=False
                        old=[]
                        counter=0
                        while True:
                            if escape:
                                break
                            d=rf.read(os.get_terminal_size().columns)
                            counter+=len(d)
                            if not d:
                                break
                            lineColor=Fore.grey_70
                            lineColor=lc[odd]
                            print(f"{lineColor}{d}{Style.reset}")
                            old.append(d)
                            current_old_index=(-m)
                            if (line%m)==0 and line != 0:
                                while True:
                                    wait=Prompt.__init2__(None,func=mkb,ptext="Next Page?",helpText="see the next {m} lines, space == yes/1/true to see next 15 lines\nno/n/false/f/0 reprints current set of lines\nb/back escapes from glossary\nq quits",data=None)
                                    if wait == 'p':
                                        goto=len(''.join(old[m:]))
                                        rf.seek(goto)
                                        old=[]
                                        lct=0
                                        while True:
                                            #print(lct,-m)
                                            if lct <= -m:
                                                break
                                            if escape:
                                                break
                                            d=rf.read(os.get_terminal_size().columns)
                                            if not d:
                                                break
                                            lct-=1
                                            counter+=len(d)
                                            lineColor=Fore.grey_70
                                            lineColor=lc[odd]
                                            print(f"{lineColor}{d}{Style.reset}")
                                            old.append(d)
                                            current_old_index=(-m)
                                            line+=1
                                            if odd >= m:
                                                odd=0
                                            else:
                                                odd+=1
                                                        
                                    elif wait in [None,]:
                                        escape=True
                                        break
                                    elif wait == True:
                                        break
                                    else:
                                        for num,i in enumerate(old[m:]):
                                            lineColor=lc[num-1]
                                            print(f"{lineColor}{i}{Style.reset}")
                            line+=1
                            if odd >= m:
                                odd=0
                            else:
                                odd+=1
                            

                except Exception as e:
                    print(e)
            else:
                return func(cmd,data)   

    #since this will be used statically, no self is required 
    #example filter method
    def cmdfilter(text,data):
        print(text)

prefix_text=f'''{Fore.light_red}$code{Fore.light_blue} is the scanned text literal{Style.reset}
{Fore.light_magenta}{Style.underline}#code refers to:{Style.reset}
{Fore.grey_70}e.{Fore.light_red}$code{Fore.light_blue} == search EntryId{Style.reset}
{Fore.grey_70}B.{Fore.light_red}$code{Fore.light_blue} == search Barcode{Style.reset}
{Fore.grey_70}c.{Fore.light_red}$code{Fore.light_blue} == search Code{Style.reset}
{Fore.light_red}$code{Fore.light_blue} == search Code | Barcode{Style.reset}
'''
def prefix_filter(text,self):
    split=text.split(self.get('delim'))
    if len(split) == 2:
        prefix=split[0]
        code=split[-1]
        try:
            if prefix.lower() == 'c':
                self.get('c_do')(code)
            elif prefix == 'B':
                self.get('b_do')(code)
            elif prefix.lower() == 'e':
                self.get('e_do')(code)
        except Exception as e:
            print(e)
    else:
        self.get('do')(text)

if __name__ == "__main__":  
    Prompt(func=Prompt.cmdfilter,ptext='code|barcode',helpText='test help!',data={})
        

    