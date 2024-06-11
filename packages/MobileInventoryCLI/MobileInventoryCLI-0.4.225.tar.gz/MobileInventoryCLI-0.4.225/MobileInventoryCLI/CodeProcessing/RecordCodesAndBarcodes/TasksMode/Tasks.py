from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Unified.Unified as unified
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.possibleCode as pc
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import prefix_text
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.TasksMode.ReFormula import *
import random
from pint import UnitRegistry
import pandas as pd
import numpy as np
from datetime import *
from colored import Style,Fore
import json,sys,math
def today():
    dt=datetime.now()
    return date(dt.year,dt.month,dt.day)

class TasksMode:
    #extra is for future expansion
    def exportList2Excel(self,fields=False,extra=[]):
        FIELDS=['Barcode','ALT_Barcode','Code','Name','Price','CaseCount']
        cols=[i.name for i in Entry.__table__.columns]
        if fields == True:
            return FIELDS
        for i in extra:
            if i in cols:
                FIELDS.append(extra)
            else:
                print(f"{Fore.light_red}{Style.bold}Warning {Style.underline}{Style.reset}{Fore.light_yellow}'{i}' from extra={extra} is not a valid {Style.reset}{Fore.light_green}Field|Column!{Style.reset}")
       
        with Session(self.engine) as session:
            query=session.query(Entry).filter(Entry.InList==True)
            df = pd.read_sql(query.statement, query.session.bind)
            df=df[['Barcode','ALT_Barcode','Code','Name','Price','CaseCount']]
            #df.to_excel()
            def mkT(text,self):
                if text=='':
                    return 'InList-Export.xlsx'
                return text
            while True:
                try:
                    efilename=Prompt.__init2__(None,func=mkT,ptext=f"Save where[{mkT('',None)}]",helpText="save the data to where?",data=self)
                    if isinstance(efilename,str):
                        df.to_excel(efilename)
                    break
                except Exception as e:
                    print(e)
    def getTotalwithBreakDownForScan(self,short=False):
        while True:
            color1=Fore.light_red
            color2=Fore.orange_red_1
            color3=Fore.cyan
            color4=Fore.green_yellow
            def mkT(text,self):
                return text
            if not short:
                fieldname='ALL_INFO'
            else:
                fieldname="BASIC_INFO"
            mode='LU'
            h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
            scanned=Prompt.__init2__(None,func=mkT,ptext=f'{h}{Fore.light_yellow}barcode|code[help]?',helpText='',data=self)
            if not scanned:
                break
            else:
                with Session(self.engine) as session:
                    result=session.query(Entry).filter(or_(Entry.Barcode==scanned,Entry.Code==scanned,Entry.ALT_Barcode==scanned),Entry.InList==True).first()
                    if result:
                        backroom=result.BackRoom
                        total=0
                        for f in self.valid_fields:
                            if f not in self.special:
                                if getattr(result,f) not in [None,'']:
                                    total+=float(getattr(result,f))
                        if not short:
                            print(result)
                        else:
                            print(result.seeShort())
                        print(f"{Fore.light_yellow}0 -> {color1}Amount Needed Total+BackRoom {Style.reset}{color2}{Style.bold}{total}{Style.reset}! {Fore.grey_70}#if you total everything including backroom{Style.reset}")
                        print(f"{Fore.cyan}1 -> {color1}Amount Needed Total w/o BackRoom {Style.reset}{color2}{Style.bold}{total-backroom}{Style.reset} {Fore.grey_70}#if you are totalling everything without the backroom!{Style.reset}")
                        print(f"{Fore.light_green}2 -> {color1}Amount Needed Total w/o BackRoom - BackRoom {Style.reset}{color2}{Style.bold}{(total-backroom)-backroom}{Style.reset}! {Fore.grey_70}#if you are totalling everything needed minus what was/will brought from the backroom{Style.reset}")


                        
                    else:
                        print(f"{Fore.light_red}{Style.bold}No such Barcode|Code with InList==True:{scanned}{Style.reset}\nLet's Try a Search[*]!")
                        #search_auto_insert
                        idF=self.SearchAuto(InList=True,skipReturn=False)
                        if idF:
                            result=session.query(Entry).filter(Entry.EntryId==idF).first()
                            if result:
                                backroom=result.BackRoom
                                total=0
                                for f in self.valid_fields:
                                    if f not in self.special:
                                        if getattr(result,f) not in [None,'']:
                                            total+=float(getattr(result,f))
                                if not short:
                                    print(result)
                                else:
                                    print(result.seeShort())
                                print(f"{Fore.light_yellow}0 -> {color1}Amount Needed Total+BackRoom {Style.reset}{color2}{Style.bold}{total}{Style.reset}! {Fore.grey_70}#if you total everything including backroom{Style.reset}")
                                print(f"{Fore.cyan}1 -> {color1}Amount Needed Total w/o BackRoom {Style.reset}{color2}{Style.bold}{total-backroom}{Style.reset} {Fore.grey_70}#if you are totalling everything without the backroom!{Style.reset}")
                                print(f"{Fore.light_green}2 -> {color1}Amount Needed Total w/o BackRoom - BackRoom {Style.reset}{color2}{Style.bold}{(total-backroom)-backroom}{Style.reset}! {Fore.grey_70}#if you are totalling everything needed minus what 'was', or 'will be', brought from the backroom{Style.reset}")
                            else:
                                print(f"{Fore.light_yellow}Nothing was selected!{Style.reset}")




            

    def display_field(self,fieldname,load=False,above=None,below=None):
        #for use with header
        #fieldname='ALL_INFO'
        mode='ListMode'
        h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
    
        color1=Fore.light_green
        color2=Fore.orange_red_1
        color3=Fore.cyan
        color4=Fore.green_yellow
        numColor=Fore.light_red
        eidColor=Fore.medium_violet_red
        m=f"{numColor}Item Num {Style.reset}|{color1}Name{Style.reset}|{color2}Barcode|ALT_Barcode{Style.reset}|{color3}Code{Style.reset}|{color4}{fieldname}{Style.reset}|{eidColor}EID{Style.reset}"
        hr='-'*len(m)
        print(f"{m}\n{hr}")
        if (fieldname in self.valid_fields) or (load == True and fieldname == 'ListQty'):
            with Session(self.engine) as session:
                query=session.query(Entry).filter(Entry.InList==True)
                if above == None:
                    def mkT(text,self):
                        try:
                            v=int(text)
                        except Exception as e:
                            print(e)
                            v=0
                        return v
                    above=Prompt.__init2__(None,func=mkT,ptext=f"{h}Above [{Fore.light_green}0{Style.reset}]",helpText="anything below this will not be displayed!",data=self)
                if below == None:
                    def mkTBelow(text,self):
                        try:
                            v=int(text)
                        except Exception as e:
                            print(e)
                            v=sys.maxsize
                        return v
                    below=Prompt.__init2__(None,func=mkTBelow,ptext=f"{h}Below [{Fore.light_green}{sys.maxsize}{Style.reset}]",helpText="anything above this will not be displayed!",data=self)
                if above != None:
                    print(type(above),above,fieldname)
                    query=query.filter(getattr(Entry,fieldname)>above)
                if below != None:
                    query=query.filter(getattr(Entry,fieldname)<below)
                results=query.all()
                if len(results) < 1:
                    print(f"{Fore.light_red}{Style.bold}Nothing is in List!{Style.reset}")
                for num,result in enumerate(results):
                    print(f"{numColor}{num}{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{eidColor}{getattr(result,'EntryId')}{Style.reset}")
        print(f"{m}\n{hr}")

    def SearchAuto(self,InList=None,skipReturn=False):
        while True:
            try:
                with Session(self.engine) as session:
                    def mkT(text,self):
                        return text
                    fields=[i.name for i in Entry.__table__.columns if str(i.type) == "VARCHAR"]
                    stext=Prompt.__init2__(None,func=mkT,ptext="Search[*]:",helpText="Search All(*) fields",data=self)
                    query=session.query(Entry)
                    if not stext:
                        return
                    
                    q=[]
                    for f in fields:
                        q.append(getattr(Entry,f).icontains(stext.lower()))

                    query=query.filter(or_(*q))
                    if InList != None:
                        query=query.filter(Entry.InList==InList)
                    results=query.all()
                    ct=len(results)
                    for num,r in enumerate(results):
                        if num < round(0.25*ct,0):
                            color_progress=Fore.green
                        elif num < round(0.50*ct,0):
                            color_progress=Fore.light_green
                        elif num < round(0.75*ct,0):
                            color_progress=Fore.light_yellow
                        else:
                            color_progress=Fore.light_red
                        if num == ct - 1:
                            color_progress=Fore.light_red
                        if num == 0:
                            color_progress=Fore.cyan    
                        msg=f"{color_progress}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} ->{r}"
                        print(msg)
                    print(f"{Fore.light_yellow}There are {Fore.light_red}{ct}{Fore.light_yellow} Total Results for search {Fore.medium_violet_red}'{stext}'{Style.reset}{Fore.light_yellow}.{Style.reset}")
                    print(f"{Fore.light_red}Fields Searched in {Fore.cyan}{fields}{Style.reset}")
                    def mklint(text,data):
                        try:    
                            if text.lower() in ['r','rs','rst','reset']:
                                return True
                            index=int(text)
                            if index in [i for i in range(data)]:
                                return index
                            else:
                                raise Exception("out of bounds!")
                        except Exception as e:
                            print(e)
                            return None
                    if skipReturn:
                        return
                    ct=len(results)-1
                    if ct+1 > 0:
                        reset=False
                        while True:
                            which=Prompt.__init2__(None,func=mklint,ptext=f"Which {Fore.light_red}entry # {Style.reset}{Fore.light_yellow}do you wish to use?",helpText="number of entry to use [0..{ct}]\nUse 'r'|'rs'|'rst'|'reset' to reset search\n",data=ct+1)
                            print(which)
                            if which in [None,]:
                                return
                            elif which in [True,] and not isinstance(which,int):
                                reset=True
                                break

                            return results[which].EntryId
                        if reset == False:
                            break
            except Exception as e:
                print(e)


    def NewEntrySchematic(self):
        while True:
            code=''
                                
            def mkT(text,self):
                return str(text)
            fieldname="NewEntryFromSchematic"
            code=Prompt.__init2__(None,func=mkT,ptext=f"{Fore.grey_70}[{Fore.light_steel_blue}ListMode{Fore.medium_violet_red}@{Fore.light_green}{fieldname}{Fore.grey_70}]{Style.reset}{Fore.light_yellow} Barcode",helpText=self.helpText_barcodes,data=self)
            if code == None:
                return
            with Session(self.engine) as session:
                check=session.query(Entry).filter(Entry.Barcode==code).first()
                if not check:
                    newEntry=self.mkNew(code=code,data={'Name':'','Code':code,'CaseCount':1,'Facings':1})
                    if newEntry == None:
                        print(f"{Fore.orange_red_1}User canceled!{Style.reset}")
                        return
                    newEntry['Barcode']=code
                    ne=Entry(**newEntry)
                    session.add(ne)
                    session.commit()
                    session.flush()
                    session.refresh(ne)
                    print(ne)
                else:
                    data={
                    'Name':check.Name,
                    'Code':check.Code,
                    'Facings':check.Facings,
                    'CaseCount':check.CaseCount,
                    }
                    print(f"{Fore.light_red}Item Exists please use '{Fore.light_yellow}ni{Fore.light_red}' to {Fore.light_sea_green}bypass... {Fore.light_magenta}prompting now for {Style.bold}updates...\n\n{Style.reset}")
                    updates=self.mkNew(code=check.Barcode,data=data)
                    if updates != None:
                        session.query(Entry).filter(Entry.Barcode==check.Barcode).update(updates)
                        session.commit()
                        session.flush()
                        session.refresh(check)
                    print(check)

    def mkNew(self,code,data=None):
        if data == None:
            data={
            'Name':'',
            'Code':code,
            'Price':0,
            'CaseCount':1,
            }
        self.skipTo=None
        while True:  
            #print(self.skipTo,"#loop top")
            for num,f in enumerate(data):
                #print(self.skipTo,'#2',"1 loop for")
                if self.skipTo != None and num < self.skipTo:
                    continue
                else:
                    self.skipTo=None
                keys=['e','p','d']
                while True:
                    try:
                        if str(f) == 'Price':
                            def lclf(text,data):
                                try:
                                    if text.lower() in keys:
                                        return text.lower()
                                    return float(eval(text))
                                except Exception as e:
                                    return float(0)
                            dtmp=Prompt.__init2__(None,func=lclf,ptext=f"Entry[default:{data[f]}] {f}",helpText=f"{Fore.light_steel_blue}Enter a value for {f}, or leave blank to use scanned code; 'b' goes back to 'TaskMode'; 'e' to skip/exit entry altogether! 'p' for previous ; 'd' to use default stored value, if you entered a value, then 'd' will use that value when coming back from 'p'{Style.reset}",data=self)
                            if dtmp in [None,]:
                                print(f"{Fore.orange_red_1}User Canceled!{Style.reset}")
                                return

                        elif str(f) == 'CaseCount':
                            def lcli(text,data):
                                try:
                                    if text.lower() in keys:
                                        return text.lower()
                                    return int(eval(text))
                                except Exception as e:
                                    return int(1)
                            dtmp=Prompt.__init2__(None,func=lcli,ptext=f"Entry[default:{data[f]}] {f}",helpText=f"{Fore.light_steel_blue}Enter a value for {f}, or leave blank to use scanned code; 'b' goes back to 'TaskMode'; 'e' to skip/exit entry altogether! 'p' for previous ; 'd' to use default stored value, if you entered a value, then 'd' will use that value when coming back from 'p'{Style.reset}",data=self)
                            if dtmp in [None,]:
                                print(f"{Fore.orange_red_1}User Canceled!{Style.reset}")
                                return
                        else:
                            def lclt(text,data):
                                return text
                            dtmp=Prompt.__init2__(None,func=lclt,ptext=f"Entry[default:{data[f]}] {f}",helpText=f"{Fore.light_steel_blue}Enter a value for {f}, or leave blank to use scanned code; 'b' goes back to 'TaskMode'; 'e' to skip/exit entry altogether! 'p' for previous ; 'd' to use default stored value, if you entered a value, then 'd' will use that value when coming back from 'p'{Style.reset}",data=self)
                            if dtmp in [None,]:
                                print(f"{Fore.orange_red_1}User Canceled!{Style.reset}")
                                return
                        if dtmp in ['',None] and f not in ['Price','CaseCount']:
                            data[f]=code
                        elif dtmp in ['',None] and f in ['Price','CaseCount']:
                            continue
                        elif isinstance(dtmp,str):
                            if str(dtmp).lower() in ['e',]:
                                return
                            elif str(dtmp).lower() in ['p',]:
                                #print(num,num-1,"#3 loop while")
                                self.skipTo=num-1
                                break
                            elif str(dtmp).lower() in ['d',]:
                                print(f'{Fore.light_green}{data[f]}{Style.reset}',f'{Fore.orange_red_1}using default{Style.reset}')
                                pass
                            else:
                                data[f]=dtmp
                        else:
                            data[f]=dtmp
                        self.skipTo=None
                        break
                    except Exception as e:
                        print(e)
                        break
                if self.skipTo != None:
                    break
            if self.skipTo == None:
                break
        return data

    entrySepStart=f'{Back.grey_30}{Fore.light_red}\\\\{Fore.light_green}{"*"*10}{Fore.light_yellow}|{Fore.light_steel_blue}#REPLACE#{Fore.light_magenta}|{Fore.orange_red_1}{"+"*10}{Fore.light_yellow}{Style.bold}({today()}){Fore.light_red}//{Style.reset}'
    entrySepEnd=f'{Back.grey_30}{Fore.light_red}\\\\{Fore.orange_red_1}{"+"*10}{Fore.light_yellow}|{Fore.light_steel_blue}#REPLACE#{Fore.light_magenta}|{Fore.light_green}{"*"*10}{Fore.light_yellow}{Style.bold}({today()}){Fore.light_red}//{Style.reset}'
    def setFieldInList(self,fieldname,load=False,repack_exec=None,barcode=None):
        tmp_fieldname=fieldname
        while True:
            if (fieldname not in self.special or fieldname in ['Facings'] )or (load==True and fieldname in ['ListQty',]):
                m=f"Item Num |Name|Barcode|ALT_Barcode|Code|{fieldname}|EID"
                hr='-'*len(m)
                if (fieldname in self.valid_fields) or (load==True and fieldname in ['ListQty',]) or fieldname == None:
                    with Session(self.engine) as session:
                        if not barcode:
                            code=''
                            
                            def mkT(text,self):
                                return str(text)
                            code=Prompt.__init2__(None,func=mkT,ptext=f"{Fore.grey_70}[{Fore.light_steel_blue}ListMode{Fore.medium_violet_red}@{Fore.light_green}{fieldname}{Fore.grey_70}]{Style.reset}{Fore.light_yellow} Barcode|Code",helpText=self.helpText_barcodes,data=self)
                            if code == None:
                                break
                        else:
                            code=barcode
                        print(self.entrySepStart.replace('#REPLACE#',f'{code}@{fieldname}'))

                        pc.PossibleCodes(scanned=code)
                        pc.PossibleCodesEAN13(scanned=code)
                            
                        value=0
                        def processQtyRe(code,MODE):
                            print(fieldname)
                            try:
                                with Session(ENGINE) as session:
                                    replace_case=['c','C','cs','case']
                                    replace_case.sort(key=len,reverse=True)
                                    replace_unit=['e','u','eaches','each','unit']
                                    replace_unit.sort(key=len,reverse=True)
                                    replace_load=['l','ld','load','lod']
                                    replace_load.sort(key=len,reverse=True)
                                    replace_pallet=['p','pallet']
                                    replace_pallet.sort(key=len,reverse=True)
                                    replace_shelf=['s','sf','shlf','shelf']
                                    replace_shelf.sort(key=len,reverse=True)
                                    replace_this=['current','x',]
                                    replace_this.sort(key=len,reverse=True)

                                    multipliers={
                                    'l':1,
                                    'u':1,
                                    'p':1,
                                    's':1,
                                    'c':1,
                                    'x':1,
                                    }
                                    result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code,Entry.ALT_Barcode==code)).first()
                                    if result:
                                        if result.CaseCount==0:
                                            result.CaseCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.LoadCount==0:
                                            result.LoadCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.PalletCount==0:
                                            result.PalletCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.ShelfCount==0:
                                            result.ShelfCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if getattr(result,fieldname) == None:
                                            setattr(result,fieldname,0)

                                        multipliers['x']=getattr(result,fieldname)
                                        multipliers['c']=result.CaseCount
                                        multipliers['l']=result.LoadCount
                                        multipliers['p']=result.PalletCount
                                        multipliers['s']=result.ShelfCount
                                    else:
                                        pass
                                    def mkV(text,data):
                                        return text
                                    local_htxt=f'''{Fore.green_yellow}
using similar functionality to the primary mode, call it Legacy,
ReParseFormula mode uses formulas like so
c.1.1|1.c+2.u|u.2=1 unit + 2 cases based on the Entry related,
where the suffix can be on either side of the number, with similar 
results to advanced mode, with the exception this mode is meant to
guarantee 1.c == (1.0*c); whatever c is
so this boils down to if you have a case count of 7,
then the formula will result in:{Fore.light_yellow}
    1*1+2*7=result
    1+14=result
    result=15
{Fore.grey_70}No suffixes are needed
Take note that the suffixes must follow their quantity
number
you may use python3 built-in's to process numbers as this is 
done with {Fore.light_red}eval(){Fore.grey_70}
so you may also input below:{Fore.light_yellow}
    round(1@/2#,2) and get a valued result
    if invalid, an exception is thrown
    but will not end the programme
use of the python3.x module math is valid

{Fore.medium_violet_red}{Style.bold}Valid numeric-multiplier suffixes are{Style.reset}
{Fore.light_green}{Style.underline}Case Numeric-Multiplier Suffixes{Style.reset}
{Fore.green_yellow}{'|'.join(replace_case)}{Style.reset}
{Fore.light_magenta}{Style.underline}Unit/Eaches Numeric-Multiplier Suffixes{Style.reset}
{Style.bold}{Fore.orange_red_1}Special Suffixes{Style.reset}
{Fore.medium_violet_red}ShelfCount{Style.reset}
{Fore.light_steel_blue}{'|'.join(replace_shelf)}{Style.reset}
{Fore.medium_violet_red}LoadCount{Style.reset}
{Fore.light_magenta}{Style.underline}{'|'.join(replace_load)}{Style.reset}
{Fore.medium_violet_red}PalletCount{Style.reset}
{Fore.light_steel_blue}{'|'.join(replace_pallet)}{Style.reset}'''
                                    text=Prompt.__init2__(None,func=mkV,ptext="ReFormulated Qty using NUM@=Units,NUM#=Cases (Enter==1)",helpText=local_htxt,data=code)
                                    if text in [None,]:
                                        return
                                    elif text in ['',]:
                                        return 1

                                    textO=ReParseFormula(formula=text,casecount=multipliers.get('c'),suffixes=replace_case)
                                    textO=ReParseFormula(formula=str(textO),casecount=multipliers.get('u'),suffixes=replace_unit)
                                    textO=ReParseFormula(formula=str(textO),casecount=multipliers.get('l'),suffixes=replace_load)
                                    textO=ReParseFormula(formula=str(textO),casecount=multipliers.get('s'),suffixes=replace_shelf)
                                    textO=ReParseFormula(formula=str(textO),casecount=multipliers.get('p'),suffixes=replace_pallet)
                                    textO=ReParseFormula(formula=str(textO),casecount=multipliers.get('x'),suffixes=replace_this)
                                    textO=str(textO)
                                    print(textO)
                                    if MODE.startswith("+"):
                                        return float(eval(textO))
                                    elif MODE.startswith("-"):
                                        return float(eval(textO))*-1
                                    return float(eval(textO))
                            except Exception as e:
                                print(e)
                                if MODE.startswith("+"):
                                    return float(1)
                                elif MODE.startswith("-"):
                                    return float(-1)
                                else:
                                    return float(1)

                        def processQty(code,MODE):
                            try:
                                with Session(ENGINE) as session:
                                    replace_case=['#','.c','.C','.cs','.case']
                                    replace_unit=['@','.e','.u','.eaches','.each','.unit']
                                    replace_load=['^','~','.l','.ld','.load','.lod']
                                    replace_pallet=['$','\\','.p','.pallet']
                                    replace_shelf=['%','?','.s','.sf','.shlf','.shelf']
                                    multipliers={
                                    '@':1,
                                    '#':1,
                                    '$':1,
                                    '^':1,
                                    '%':1,
                                    }
                                    result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code,Entry.ALT_Barcode==code)).first()
                                    if result:
                                        if result.CaseCount==0:
                                            result.CaseCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.LoadCount==0:
                                            result.LoadCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.PalletCount==0:
                                            result.PalletCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.ShelfCount==0:
                                            result.ShelfCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)

                                        multipliers['#']=result.CaseCount
                                        multipliers['^']=result.LoadCount
                                        multipliers['$']=result.PalletCount
                                        multipliers['%']=result.ShelfCount
                                    else:
                                        pass
                                    def mkV(text,data):
                                        return text
                                    local_htxt=f'''{Fore.grey_70}
using similar functionality to the primary mode, call it Legacy,
advanced mode uses formulas like so
1@+2#=1 unit + 2 cases based on the Entry related
so this boils down to if you have a case count of 7,
then the formula will result in:{Fore.light_yellow}
    1*1+2*7=result
    1+14=result
    result=15
{Fore.grey_70}No suffixes are needed
Take note that the suffixes must follow their quantity
number
you may use python3 built-in's to process numbers as this is 
done with {Fore.light_red}eval(){Fore.grey_70}
so you may also input below:{Fore.light_yellow}
    round(1@/2#,2) and get a valued result
    if invalid, an exception is thrown
    but will not end the programme
use of the python3.x module math is valid

{Fore.medium_violet_red}{Style.bold}Valid numeric-multiplier suffixes are{Style.reset}
{Fore.light_green}{Style.underline}Case Numeric-Multiplier Suffixes{Style.reset}
{Fore.green_yellow}{'|'.join(replace_case)}{Style.reset}
{Fore.light_magenta}{Style.underline}Unit/Eaches Numeric-Multiplier Suffixes{Style.reset}
{Style.bold}{Fore.orange_red_1}Special Suffixes{Style.reset}
{Fore.medium_violet_red}ShelfCount{Style.reset}
{Fore.light_steel_blue}{'|'.join(replace_shelf)}{Style.reset}
{Fore.medium_violet_red}LoadCount{Style.reset}
{Fore.light_magenta}{Style.underline}{'|'.join(replace_load)}{Style.reset}
{Fore.medium_violet_red}PalletCount{Style.reset}
{Fore.light_steel_blue}{'|'.join(replace_pallet)}{Style.reset}'''
                                    text=Prompt.__init2__(None,func=mkV,ptext="Formulated Qty using NUM@=Units,NUM#=Cases (Enter==1)",helpText=local_htxt,data=code)
                                    if text in [None,]:
                                        return
                                    elif text in ['',]:
                                        return 1
                                    for r in replace_case:
                                        text=text.lower().replace(r,f"*{multipliers.get('#')}")
                                    for r in replace_unit:
                                        text=text.lower().replace(r,f"*{multipliers.get('@')}")
                                    for r in replace_load:
                                        text=text.lower().replace(r,f"*{multipliers.get('^')}")
                                    for r in replace_shelf:
                                        text=text.lower().replace(r,f"*{multipliers.get('%')}")
                                    for r in replace_pallet:
                                        text=text.lower().replace(r,f"*{multipliers.get('$')}")

                                    if MODE.startswith("+"):
                                        return float(eval(text))
                                    elif MODE.startswith("-"):
                                        return float(eval(text))*-1
                                    return float(eval(text))
                            except Exception as e:
                                print(e)
                                if MODE.startswith("+"):
                                    return float(1)
                                elif MODE.startswith("-"):
                                    return float(-1)
                                else:
                                    return float(1)

                        def mkT(text,code):
                            try:
                                if text not in ['',]:
                                    if text in ['a','+a','-a']:
                                        #value,text,suffix
                                        return float(processQty(code,text)),text,''
                                    if text in ['r','+r','-r']:
                                        #value,text,suffix
                                        return float(processQtyRe(code,text)),text,''
                                    else:
                                        tmp=text.split(',')
                                        if len(tmp) == 2:
                                            text,suffix=tmp
                                            if suffix.lower() not in ['s','e','u',' ','','c']:
                                                suffix=''
                                        else:
                                            suffix=''
                                            for i in ['s','e','u','c']:
                                                if text.endswith(i):
                                                    suffix=i
                                                    text=text[:-1]
                                                    break

                                        return float(eval(text)),text,suffix
                                else:
                                    return float(1),text,''
                            except Exception as e:
                                print(e)
                                return float(0),text,''
                        if fieldname == None:
                            color_1=Fore.light_red
                            color_2=Fore.light_magenta
                            hstring=f'''
Location Fields:
{Fore.deep_pink_3b}Shelf - {color_1}{Style.bold}0{Style.reset}
{Fore.light_steel_blue}BackRoom - {color_2}{Style.bold}1{Style.reset}
{Fore.cyan}Display_1 - {color_1}{Style.bold}2{Style.reset}
{Fore.cyan}Display_2 - {color_2}{Style.bold}3{Style.reset}
{Fore.cyan}Display_3 - {color_1}{Style.bold}4{Style.reset}
{Fore.cyan}Display_4 - {color_2}{Style.bold}5{Style.reset}
{Fore.cyan}Display_5 - {color_1}{Style.bold}6{Style.reset}
{Fore.cyan}Display_6 - {color_2}{Style.bold}7{Style.reset}
{Fore.cyan}SBX_WTR_DSPLY - {color_1}{Style.bold}8{Style.reset}
{Fore.cyan}SBX_CHP_DSPLY - {color_2}{Style.bold}9{Style.reset}
{Fore.cyan}SBX_WTR_KLR - {color_1}{Style.bold}10{Style.reset}
{Fore.violet}FLRL_CHP_DSPLY - {color_2}{Style.bold}11{Style.reset}
{Fore.violet}FLRL_WTR_DSPLY - {color_1}{Style.bold}12{Style.reset}
{Fore.grey_50}WD_DSPLY - {color_2}{Style.bold}13{Style.reset}
{Fore.grey_50}CHKSTND_SPLY - {color_1}{Style.bold}14{Style.reset}
{Fore.grey_50}InList - {color_2}{Style.bold}15{Style.reset}'''

                            def mkfields(text,data):
                                def print_selection(selected):
                                    print(f"{Fore.light_yellow}Using selected {Style.bold}{Fore.light_green}'{selected}'{Style.reset}!")
                                try:
                                    selected=None
                                    #use upper or lower case letters/words/fieldnames
                                    fields=tuple([i.name for i in Entry.__table__.columns])
                                    fields_lower=tuple([i.lower() for i in fields])
                                    if text.lower() in fields_lower:
                                        index=fields_lower.index(text.lower())
                                        selected=fields[index]
                                        print_selection(selected)
                                        return fields[index]
                                    else:
                                        #use numbers
                                        mapped={
                                            '0':"Shelf",
                                            '1':"BackRoom",
                                            '2':"Display_1",
                                            '3':"Display_2",
                                            '4':"Display_3",
                                            '5':"Display_4",
                                            '6':"Display_5",
                                            '7':"Display_6",
                                            '8':"SBX_WTR_DSPLY",
                                            '9':"SBX_CHP_DSPLY",
                                            '10':"SBX_WTR_KLR",
                                            '11':"FLRL_CHP_DSPLY",
                                            '12':"FLRL_WTR_DSPLY",
                                            '13':"WD_DSPLY",
                                            '14':"CHKSTND_SPLY",
                                            '15':"ListQty"
                                        }
                                        #print(text,mapped,text in mapped,mapped[text])
                                        if text in mapped:
                                            selected=mapped[text]
                                            print_selection(selected)
                                            return mapped[text]
                                except Exception as e:
                                    print(e)
                            while True:
                                fieldname=Prompt.__init2__(None,func=mkfields,ptext="Location Field(see h|help)",helpText=hstring,data=self)
                                if fieldname in [None,]:
                                    break
                                break
                            if fieldname in [None,]:
                                continue
                            m=f"Item Num |Name|Barcode|ALT_Barcode|Code|{fieldname}|EID"
                            hr='-'*len(m)
                        palletcount=1
                        shelfcount=1
                        loadcount=1
                        casecount=1
                        Name=''
                        CD=''
                        BCD=''
                        ABCD=''
                        ci=''
                        result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code,Entry.ALT_Barcode==code)).first()
                       
                        if isinstance(result,Entry):
                            for k in ['PalletCount','ShelfCount','LoadCount','CaseCount']:
                                if getattr(result,k) < 1 or getattr(result,k) == None:
                                    setattr(result,k,1)
                                    session.commit()
                                    session.flush()
                                    session.refresh(result)
                            palletcount=result.PalletCount
                            shelfcount=result.ShelfCount
                            loadcount=result.LoadCount
                            casecount=result.CaseCount
                            Name=result.Name
                            BCD=result.Barcode
                            CD=result.Code
                            ABCD=result.ALT_Barcode 
                            ci=getattr(result,fieldname)

                        ptext=f'''{Fore.grey_70}[{Fore.light_steel_blue}ListModeQTY{Fore.grey_70}]{Style.reset}{Fore.light_green}CaseCount={Fore.cyan}{casecount}{Style.reset}|{Fore.medium_violet_red}ShelfCount={Fore.light_magenta}{shelfcount}{Style.reset}|{Fore.green_yellow}LoadCount={Fore.dark_goldenrod}{loadcount}{Style.reset}|{Fore.light_red}PalletCount={Fore.orange_red_1}{palletcount}|{Fore.spring_green_3a}{fieldname}={Fore.light_sea_green}{ci}{Style.reset}
{Fore.cyan}Name{Fore.light_steel_blue}={Name}{Style.reset}|{Fore.dark_goldenrod}Barcode={Fore.light_green}{BCD}{Style.reset}|{Style.bold}{Fore.orange_red_1}Code={Fore.spring_green_3a}{CD}|{Fore.light_sea_green}ALT_Barcode={Fore.turquoise_4}{ABCD}{Style.reset}
amount|+amount|-amount|a,+a,-a(advanced)|r,+r,-r(ReParseFormula) (Enter==1)'''
                        p=Prompt.__init2__(None,func=mkT,ptext=f"{ptext}",helpText=self.helpText_barcodes,data=code)
                        if p in [None,]:
                            return
                        if p:
                            value,text,suffix=p
                        else:
                            continue
                        try:
                            color1=Fore.light_red
                            color2=Fore.orange_red_1
                            color3=Fore.cyan
                            color4=Fore.green_yellow 
                            if text.startswith("-") or text.startswith("+"):
                                result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code,Entry.ALT_Barcode==code)).first()
                                if result:
                                    if suffix.lower() in ['c',]:
                                        if result.CaseCount in [None,]:
                                            result.CaseCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.CaseCount < 1:
                                            result.CaseCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        value=float(value)*result.CaseCount
                                    setattr(result,fieldname,getattr(result,fieldname)+float(value))
                                    result.InList=True
                                    session.commit()
                                    session.flush()
                                    session.refresh(result)
                                    if callable(repack_exec):
                                        repack_exec(result)
                                    print(f"{Fore.light_red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{color4}{getattr(result,'EntryId')}{Style.reset}")
                                    print(f"{m}\n{hr}")
                                    print(self.entrySepEnd.replace('#REPLACE#',f'{code}@{fieldname}'))
                                else:
                                    replacement=self.SearchAuto()
                                    if isinstance(replacement,int):
                                        result=session.query(Entry).filter(Entry.EntryId==replacement).first()
                                        if result:
                                            setattr(result,fieldname,getattr(result,fieldname)+float(value))
                                            result.InList=True
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                            if callable(repack_exec):
                                                repack_exec(result)
                                            print(f"{Fore.light_red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{color4}{getattr(result,'EntryId')}{Style.reset}")
                                            print(f"{m}\n{hr}")
                                            print(self.entrySepEnd.replace('#REPLACE#',f'{code}@{fieldname}'))
                                        else:
                                            raise Exception(f"result is {result}")
                                    else:
                                        data=self.mkNew(code=code)
                                        if not data:
                                            continue
                                        name=data['Name']
                                        icode=data['Code']
                                        iprice=data['Price']
                                        icc=data['CaseCount']
                                        n=Entry(Barcode=code,Code=icode,Price=iprice,Name=name,CaseCount=icc,InList=True,Note="New Item")
                                        setattr(n,fieldname,value)
                                        session.add(n)
                                        session.commit()
                                        session.flush()
                                        session.refresh(n)
                                        n.copySrc()
                                        result=n
                                        print(f"{Fore.light_red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{color4}{getattr(result,'EntryId')}{Style.reset}")

                                        print(f"{m}\n{hr}")
                                        print(self.entrySepEnd.replace('#REPLACE#',f'{code}@{fieldname}'))
                                        if callable(repack_exec):
                                            repack_exec(n)
                            else:
                                result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code,Entry.ALT_Barcode==code)).first()
                                if result:
                                    if suffix.lower() in ['c',]:
                                        if result.CaseCount in [None,]:
                                            result.CaseCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        if result.CaseCount < 1:
                                            result.CaseCount=1
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                        value=float(value)*result.CaseCount
                                    setattr(result,fieldname,value)
                                    result.InList=True
                                    session.commit()
                                    session.flush()
                                    session.refresh(result)
                                    if callable(repack_exec):
                                        repack_exec(result)
                                    print(f"{Fore.light_red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{color4}{getattr(result,'EntryId')}{Style.reset}")

                                    print(f"{m}\n{hr}")
                                    print(self.entrySepEnd.replace('#REPLACE#',f'{code}@{fieldname}'))

                                else:
                                    replacement=self.SearchAuto()
                                    if isinstance(replacement,int):
                                        result=session.query(Entry).filter(Entry.EntryId==replacement).first()
                                        if result:
                                            setattr(result,fieldname,getattr(result,fieldname)+float(value))
                                            result.InList=True
                                            session.commit()
                                            session.flush()
                                            session.refresh(result)
                                            if callable(repack_exec):
                                                repack_exec(n)
                                            print(f"{Fore.light_red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{color4}{getattr(result,'EntryId')}{Style.reset}")
                                            print(f"{m}\n{hr}")
                                            print(self.entrySepEnd.replace('#REPLACE#',f'{code}@{fieldname}'))
                                        else:
                                            raise Exception(f"result is {result}")
                                    else:
                                        
                                        data=self.mkNew(code=code)
                                        if not data:
                                            continue
                                        name=data['Name']
                                        icode=data['Code']
                                        iprice=data['Price']
                                        icc=data['CaseCount']
                                        n=Entry(Barcode=code,Code=icode,Name=name,Price=iprice,CaseCount=icc,InList=True,Note="New Item")
                                        setattr(n,fieldname,value)
                                        session.add(n)
                                        session.commit()
                                        session.flush()
                                        session.refresh(n)
                                        n.copySrc()
                                        session.commit()
                                        session.flush()
                                        session.refresh(n)
                                        result=n
                                        if callable(repack_exec):
                                            repack_exec(n)
                                        print(f"{Fore.light_red}0{Style.reset} -> {color1}{result.Name}{Style.reset}|{color2}{result.Barcode}|{result.ALT_Barcode}{Style.reset}|{color3}{result.Code}{Style.reset}|{color4}{getattr(result,fieldname)}{Style.reset}|{color4}{getattr(result,'EntryId')}{Style.reset}")

                                        print(f"{m}\n{hr}")
                                        print(self.entrySepEnd.replace('#REPLACE#',f'{code}@{fieldname}'))

                                    #raise Exception(result)
                        except Exception as e:
                            print(e)
                if repack_exec:
                    return
            else:
                #code for tags,caseId[br,6w,ld],
                self.processSpecial(fieldname)
                break
            if tmp_fieldname == None:
                fieldname=None
        
    helpText_barcodes=f"""
1. Enter the EntryId into the prompt
2. if an entry is found you will be prompted for a code to be saved
Quantity Modifiers:
(SEP=',' or No Sep) Suffixes Singles: s|e|u|' '|'' == units/singles/eaches/no multipliers
(SEP=',' or No Sep) Suffixes CaseCount: c == (qty*casecount+old_value_if_any
Valid Examples:
+1-2u - do operation in units and remove from qty 
-1+2c - do operation in cases and remove from qty
1c - cases set
1u - units set
remember, formula is calculated first, then that value is removed from qty if -/+
if CaseCount is less than 1, or not set, assume casecount == 1
    """
    def setBarcodes(self,fieldname):
         while True:
            try:
                def mkT(text,self):
                    return text
                cmd=Prompt.__init2__(None,func=mkT,ptext='Do What[help/q/b/$EntryId]?',helpText=self.helpText_barcodes,data=self)
                if not cmd:
                    break
                else:
                    with Session(self.engine) as session:
                        r=session.query(Entry).filter(Entry.EntryId==int(cmd)).first()
                        if r:
                            def mkT(text,self):
                                return text
                            code=Prompt.__init2__(None,func=mkT,ptext=f'{fieldname}[help]?',helpText=self.helpText_barcodes,data=self)
                            if not code:
                                break
                            else:
                                setattr(r,fieldname,code)
                                session.commit()
                                session.flush()
                                session.refresh(r)
                                print(r)
            except Exception as e:
                print(e)



    def processSpecial(self,fieldname):
        if fieldname.lower() == "tags":
            self.editTags()
        elif 'Barcode' in fieldname:
            self.setBarcodes(fieldname)
        else:
            print("SpecialOPS Fields! {fieldname} Not Implemented Yet!")
            self.editCaseIds()


    helpText_caseIds=f'''
{Fore.green_yellow}$WHERE,$EntryId,exec()|$ID{Style.reset}
#[ld,6w,br,all],$EntryId,generate - create a synthetic id for case and save item to and save qrcode png of $case_id in $WHERE
#[ld,6w,br,all],$EntryId,$case_id - set case id for item in $WHERE
#[ld,6w,br,all],$EntryId - display item case id in $WHERE
[ld,6w,br,all],s|search,$case_id - display items associated with $case_id in $WHERE
#[ld,6w,br,all],$EntryId,clr_csid - set $case_id to '' in $WHERE
where:
 ld is for Load
 6w is 6-Wheeler or U-Boat
 br is BackRoom
 
 all will apply to all of the above fields
    '''
    def editCaseIds(self):
         while True:
            def mkT(text,self):
                return text
            cmd=Prompt.__init2__(None,func=mkT,ptext='Do What[help]?',helpText=self.helpText_tags,data=self)
            if not cmd:
                break
            else:
                print(cmd)
                split_cmd=cmd.split(",")
                if len(split_cmd)==3:
                    mode=split_cmd[0]
                    eid=split_cmd[1]
                    ex=split_cmd[2]
                    if eid.lower() in ['s','search']:
                        #search
                        with Session(self.engine) as session:
                            results=[]
                            if split_cmd[0].lower() == '6w':
                                results=session.query(Entry).filter(Entry.CaseID_6W==ex).all()
                            elif split_cmd[0].lower() == 'ld':
                                results=session.query(Entry).filter(Entry.CaseID_LD==ex).all()
                            elif split_cmd[0].lower() == 'br':
                                results=session.query(Entry).filter(Entry.CaseID_BR==ex).all()
                            elif split_cmd[0].lower() == 'all':
                                results=session.query(Entry).filter(or_(Entry.CaseID_BR==ex,Entry.CaseID_LD==ex,Entry.CaseID_6W==ex)).all()
                            if len(results) < 1:
                                print(f"{Fore.dark_goldenrod}No Items to display!{Style.reset}")
                            for num,r in enumerate(results):
                                print(f"{Fore.light_red}{num}{Style.reset} -> {r}")
                    else:
                        with Session(self.engine) as session:
                            query=session.query(Entry).filter(Entry.EntryId==int(eid)).first()
                            if query:
                                if ex.lower() in ['clr_csid',]:
                                    if split_cmd[0].lower() == '6w':
                                        query.CaseID_6W=''
                                    elif split_cmd[0].lower() == 'ld':
                                        query.CaseID_LD=''
                                    elif split_cmd[0].lower() == 'br':
                                        query.CaseID_BR=''
                                    elif split_cmd[0].lower() == 'all':
                                        query.CaseID_6W=''
                                        query.CaseID_LD=''
                                        query.CaseID_BR=''
                                elif ex.lower() in ['generate','gen','g']:
                                    if split_cmd[0].lower() == '6w':
                                        query.CaseID_6W=query.synthetic_field_str()
                                    elif split_cmd[0].lower() == 'ld':
                                        query.CaseID_LD=query.synthetic_field_str()
                                    elif split_cmd[0].lower() == 'br':
                                        query.CaseID_BR=query.synthetic_field_str()
                                    elif split_cmd[0].lower() == 'all':
                                        query.CaseID_6W=query.synthetic_field_str()
                                        query.CaseID_LD=query.synthetic_field_str()
                                        query.CaseID_BR=query.synthetic_field_str()
                                else:
                                    if split_cmd[0].lower() == '6w':
                                        query.CaseID_6W=ex
                                    elif split_cmd[0].lower() == 'ld':
                                        query.CaseID_LD=ex
                                    elif split_cmd[0].lower() == 'br':
                                        query.CaseID_BR=ex
                                    elif split_cmd[0].lower() == 'all':
                                        query.CaseID_6W=ex
                                        query.CaseID_LD=ex
                                        query.CaseID_BR=ex
                                session.commit()
                                session.flush()
                                session.refresh(query)
                                print(f"""
    Name: {query.Name}
    Barcode: {query.Barcode}
    Code: {query.Code}
    EntryId: {query.EntryId}
    CaseId 6W: {query.CaseID_6W}
    CaseId LD: {query.CaseID_LD}
    CaseId BR: {query.CaseID_BR}
    """)
                elif len(split_cmd)==2:
                    with Session(self.engine) as session:
                        query=session.query(Entry).filter(Entry.EntryId==int(split_cmd[1]))
                        r=query.first()
                        if r:
                            if split_cmd[0].lower() == '6w':
                                print(r.CaseID_6W)
                            elif split_cmd[0].lower() == 'ld':
                                print(r.CaseID_LD)
                            elif split_cmd[0].lower() == 'br':
                                print(r.CaseID_BR)
                                #self.CaseID_BR=CaseID_BR
                                #self.CaseID_LD=CaseID_LD
                                #self.CaseID_6W=CaseID_6W
                        else:
                            print(f"{Fore.dark_goldenrod}No Such Item!{Style.reset}")
                else:
                    print(self.helpText_caseIds)


    helpText_tags=f'''{prefix_text}
{Fore.green_yellow}$mode[=|R,+,-],$TAG_TEXT,$fieldname,$id|$code|$barcode|$fieldData_to_id{Style.reset}
{Fore.orange_red_1}Valid Fieldnames to use are:{Fore.light_green}Barcode,{Fore.green_yellow}Code,{Fore.spring_green_3a}ALT_Barcode,{Fore.light_sea_green} and EntryId{Style.reset}
{Fore.cyan}=|R{Style.reset} -> {Fore.orange_red_1}{Style.bold}set Tag to $TAG_TEXT{Style.reset}
{Fore.cyan}+{Style.reset} -> {Fore.orange_red_1}{Style.bold}add $TAG_TEXT to Tag{Style.reset}
{Fore.cyan}-{Style.reset} -> {Fore.orange_red_1}{Style.bold}remove $TAG_TEXT from Tag{Style.reset}
{Fore.cyan}s|search{Style.reset} -> {Fore.orange_red_1}{Style.bold}search for items containing Tag{Style.reset}
{Fore.cyan}l|list{Style.reset} -> {Fore.orange_red_1}{Style.bold}List All Tags{Style.reset}
{Fore.light_red}{Style.bold}This performs operations on all results found without confirmation for mass tag-edits{Style.reset}
{Fore.cyan}ba|bta|bulk_tag_add{Style.reset} -> {Fore.orange_red_1}{Style.bold}Bulk add Tags to {Fore.light_magenta}{Style.underline}#code{Style.reset}
{Fore.cyan}br|btr|bulk_tag_rem{Style.reset} -> {Fore.orange_red_1}{Style.bold}Bulk remove Tags from {Fore.light_magenta}{Style.underline}#code{Style.reset}
{Fore.light_red}{Style.bold}reset_all_tags|clear_all_tags -> {Fore.orange_red_1}{Style.underline} reset all tags to []{Style.reset}
    '''
    def editTags(self):
        while True:
            #cmd=input("Do What[help]?: ")
            #PROMPT
            def mkT(text,self):
                return text
            fieldname='TaskMode'
            mode='EditTags'
            h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
            cmd=Prompt.__init2__(None,func=mkT,ptext=f'{h}Do What[help]?',helpText=self.helpText_tags,data=self)
            if not cmd:
                break

            if cmd.lower() in ['l','list']:
                with Session(self.engine) as session:
                    tags=[]
                    allTags=session.query(Entry).all()
                    for i in allTags:
                        if i.Tags and i.Tags != '':
                            try:
                                tl=json.loads(i.Tags)
                                for t in tl:
                                    if t not in tags:
                                        tags.append(t)
                            except Exception as e:
                                print(e)
                    tagCt=len(tags)
                    for num,t in enumerate(tags):
                        print(f"{Fore.green}{num}{Style.reset}/{Fore.light_red}{tagCt-1}{Style.reset} -> {Fore.light_magenta}'{Style.reset}{Fore.grey_70}{t}{Style.reset}{Fore.light_magenta}'{Style.reset}")
            elif cmd.lower() in ['pa','prompted_add','prompted add','auto_add','auto add','aa']:
                while True:
                    try:
                        with Session(self.engine) as session:
                            query=session.query(Entry)
                            def mkT(text,self):
                                return text
                            tag=Prompt.__init2__(None,func=mkT,ptext="Tag",helpText="Tag to add to code")
                            try:
                                #code=Prompt.__init2__(None,func=mkT,ptext="Code|Barcode",helpText=f"Code|Barcode to add Tag:'{tag}' to.")
                                #if code in [None,]:
                                #    break
                                def addTag(session,entry,tag):
                                    try:
                                        old=list(json.loads(entry.Tags))
                                        if tag not in old:
                                            old.append(tag)
                                        entry.Tags=json.dumps(old)
                                    except Exception as e:
                                        print(e)
                                        entry.Tags=json.dumps([tag,])
                                    session.commit()
                                    session.flush()
                                    session.refresh(entry)
                                    
                                def e_do(self,code,tag):
                                    with Session(self.engine) as session:
                                        try:
                                            code=int(code)
                                            query=session.query(Entry).filter(Entry.EntryId==code)
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                addTag(session,r,tag)
                                                session.refresh(r)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                        except Exception as e:
                                            print(e)

                                def b_do(self,code,tag):
                                    with Session(self.engine) as session:
                                        query=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Barcode.icontains(code)))
                                        results=query.all()
                                        ct=len(results)
                                        if len(results)==0:
                                            print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")                                            
                                        for num,r in enumerate(results):
                                            if num%2==0:
                                                colorEntry=Style.bold
                                            else:
                                                colorEntry=Fore.grey_70+Style.underline
                                            addTag(session,r,tag)
                                            session.refresh(r)
                                            compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                            if num == 0:
                                                color1=Fore.light_green
                                            elif num > 0 and num%2==0:
                                                color1=Fore.green_yellow
                                            elif num > 0 and num%2!=0:
                                                color1=Fore.dark_goldenrod
                                            elif num+1 == ct:
                                                color1=Fore.light_red
                                            print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")

                                def c_do(self,code,tag):
                                    with Session(self.engine) as session:
                                        query=session.query(Entry).filter(or_(Entry.Code==code,Entry.Code.icontains(code)))
                                        results=query.all()
                                        ct=len(results)
                                        if len(results)==0:
                                            print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                        for num,r in enumerate(results):
                                            if num%2==0:
                                                colorEntry=Style.bold
                                            else:
                                                colorEntry=Fore.grey_70+Style.underline
                                            addTag(session,r,tag)
                                            session.refresh(r)
                                            compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                            if num == 0:
                                                color1=Fore.light_green
                                            elif num > 0 and num%2==0:
                                                color1=Fore.green_yellow
                                            elif num > 0 and num%2!=0:
                                                color1=Fore.dark_goldenrod
                                            elif num+1 == ct:
                                                color1=Fore.light_red
                                            print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                def do(self,code,tag):
                                    with Session(self.engine) as session:
                                        query=session.query(Entry).filter(or_(Entry.Code==code,Entry.Barcode==code,Entry.Code.icontains(code),Entry.Barcode.icontains(code)))
                                        results=query.all()
                                        ct=len(results)
                                        if len(results)==0:
                                            print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                        for num,r in enumerate(results):
                                            if num%2==0:
                                                colorEntry=Style.bold
                                            else:
                                                colorEntry=Fore.grey_70+Style.underline
                                            addTag(session,r,tag)
                                            compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                            if num == 0:
                                                color1=Fore.light_green
                                            elif num > 0 and num%2==0:
                                                color1=Fore.green_yellow
                                            elif num > 0 and num%2!=0:
                                                color1=Fore.dark_goldenrod
                                            elif num+1 == ct:
                                                color1=Fore.light_red
                                            print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                                
                                ex={
                                    'delim':'.',
                                    'e_do':lambda code,tag=tag,self=self:e_do(self,code,tag),
                                    'c_do':lambda code,tag=tag,self=self:c_do(self,code,tag),
                                    'b_do':lambda code,tag=tag,self=self:b_do(self,code,tag),
                                    'do':lambda code,tag=tag,self=self:do(self,code,tag)
                                }
                                status=Prompt.__init2__(None,func=prefix_filter,ptext="Code|Barcode|(e|B|c).$code) ",helpText="Code|Barcode|EntryId to have tag applied to prefix will use the specified field e. == EntryID, c. == Code, B. == Barcode.",data=ex)
                                if status in [None,]:
                                    break
                            except Exception as e:
                                print(e)
                    except Exception as e:
                        print(e)

            elif cmd.lower() in ['s','search']:
                def mkT(text,self):
                    return text
                tag=Prompt.__init2__(None,func=mkT,ptext='Tag[help]?',helpText=self.helpText_tags,data=self)
                if not tag:
                    break
               
                with Session(self.engine) as session:
                    results=session.query(Entry).all()
                    ct=len(results)
                    t=[]
                    for num,r in enumerate(results):
                        #print(r.Tags)
                        try:
                            if r.Tags not in ['',None]:

                                if tag in list(json.loads(r.Tags)):
                                    t.append(r)
                        except Exception as e:
                            pass
                    for num,rr in enumerate(t):
                        print(f"{Fore.green}{num}{Style.reset}/{Fore.light_red}{ct}{Style.reset} -> {rr}")
                    print(f"{Fore.light_yellow}there was/were {Style.reset}{Fore.light_blue}{len(t)} Results.{Style.reset}")
                    inlist=Prompt.__init2__(None,func=mkT,ptext='Set Results to Have InList=True[help] and ListQty=-1?',helpText=self.helpText_tags,data=self)
                    if not inlist:
                        break
                    if inlist.lower() in ['y','yes']:
                        ct2=len(t)
                        for num,x in enumerate(t):
                            x.InList=True
                            x.ListQty=-1
                            print(f"{Fore.light_green}{num}{r.EntryId}={Style.reset}{Fore.light_yellow}{r.InList}{Style.reset}/{Fore.light_red}{ct2}{Style.reset}")
                            if num%50 ==0:
                                session.commit()
                        session.commit()
            elif cmd.lower() in ['ba','bulk_tag_add']:
                while True:
                    try:
                        with Session(self.engine) as session:
                            query=session.query(Entry)
                            def mkT(text,self):
                                return text
                            tag=Prompt.__init2__(None,func=mkT,ptext="Tag",helpText="Tag to add to code")
                            while True:
                                try:
                                    #code=Prompt.__init2__(None,func=mkT,ptext="Code|Barcode",helpText=f"Code|Barcode to add Tag:'{tag}' to.")
                                    #if code in [None,]:
                                    #    break
                                    def addTag(session,entry,tag):
                                        try:
                                            old=list(json.loads(entry.Tags))
                                            if tag not in old:
                                                old.append(tag)
                                            entry.Tags=json.dumps(old)
                                        except Exception as e:
                                            print(e)
                                            entry.Tags=json.dumps([tag,])
                                        session.commit()
                                        session.flush()
                                        session.refresh(entry)
                                        
                                    def e_do(self,code,tag):
                                        with Session(self.engine) as session:
                                            try:
                                                code=int(code)
                                                query=session.query(Entry).filter(Entry.EntryId==code)
                                                results=query.all()
                                                ct=len(results)
                                                if len(results)==0:
                                                    print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                                for num,r in enumerate(results):
                                                    if num%2==0:
                                                        colorEntry=Style.bold
                                                    else:
                                                        colorEntry=Fore.grey_70+Style.underline
                                                    addTag(session,r,tag)
                                                    session.refresh(r)
                                                    compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                    if num == 0:
                                                        color1=Fore.light_green
                                                    elif num > 0 and num%2==0:
                                                        color1=Fore.green_yellow
                                                    elif num > 0 and num%2!=0:
                                                        color1=Fore.dark_goldenrod
                                                    elif num+1 == ct:
                                                        color1=Fore.light_red
                                                    print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                            except Exception as e:
                                                print(e)

                                    def b_do(self,code,tag):
                                        with Session(self.engine) as session:
                                            query=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Barcode.icontains(code)))
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")                                            
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                addTag(session,r,tag)
                                                session.refresh(r)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")

                                    def c_do(self,code,tag):
                                        with Session(self.engine) as session:
                                            query=session.query(Entry).filter(or_(Entry.Code==code,Entry.Code.icontains(code)))
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                addTag(session,r,tag)
                                                session.refresh(r)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                    def do(self,code,tag):
                                        with Session(self.engine) as session:
                                            query=session.query(Entry).filter(or_(Entry.Code==code,Entry.Barcode==code,Entry.Code.icontains(code),Entry.Barcode.icontains(code)))
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                addTag(session,r,tag)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                                    
                                    ex={
                                        'delim':'.',
                                        'e_do':lambda code,tag=tag,self=self:e_do(self,code,tag),
                                        'c_do':lambda code,tag=tag,self=self:c_do(self,code,tag),
                                        'b_do':lambda code,tag=tag,self=self:b_do(self,code,tag),
                                        'do':lambda code,tag=tag,self=self:do(self,code,tag)
                                    }
                                    status=Prompt(func=prefix_filter,ptext="Code|Barcode|(e|B|c).$code) ",helpText="Code|Barcode|EntryId to have tag applied to prefix will use the specified field e. == EntryID, c. == Code, B. == Barcode.",data=ex)
                                    if status.status == False:
                                        break   
                                except Exception as e:
                                    print(e)

                        break
                    except Exception as e:
                        print(e)
            elif cmd.lower() in ['br','btr','bulk_tag_rem']:
                while True:
                    try:
                        with Session(self.engine) as session:
                            query=session.query(Entry)
                            def mkT(text,self):
                                return text
                            tag=Prompt.__init2__(None,func=mkT,ptext="Tag",helpText="Tag to remove from code")
                            while True:
                                try:
                                    #code=Prompt.__init2__(None,func=mkT,ptext="Code|Barcode",helpText=f"Code|Barcode to add Tag:'{tag}' to.")
                                    #if code in [None,]:
                                    #    break
                                    def remTag(session,entry,tag):
                                        try:
                                            old=list(json.loads(entry.Tags))
                                            if tag not in old:
                                                return
                                            tmp=[]
                                            for t in old:
                                                if t != tag:
                                                    tmp.append(t)
                                            entry.Tags=json.dumps(tmp)
                                        except Exception as e:
                                            print(e)
                                            entry.Tags=json.dumps([])
                                        session.commit()
                                        session.flush()
                                        session.refresh(entry)

                                    def e_do(self,code,tag):
                                        with Session(self.engine) as session:
                                            try:
                                                code=int(code)
                                                query=session.query(Entry).filter(Entry.EntryId==code)
                                                results=query.all()
                                                ct=len(results)
                                                if len(results)==0:
                                                    print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                                for num,r in enumerate(results):
                                                    results=query.all()
                                                    if num%2==0:
                                                        colorEntry=Style.bold
                                                    else:
                                                        colorEntry=Fore.grey_70+Style.underline
                                                    remTag(session,r,tag)
                                                    session.refresh(r)
                                                    compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                    if num == 0:
                                                        color1=Fore.light_green
                                                    elif num > 0 and num%2==0:
                                                        color1=Fore.green_yellow
                                                    elif num > 0 and num%2!=0:
                                                        color1=Fore.dark_goldenrod
                                                    elif num+1 == ct:
                                                        color1=Fore.light_red
                                                    print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                                    
                                            except Exception as e:
                                                print(e)

                                    def b_do(self,code,tag):
                                        with Session(self.engine) as session:
                                            query=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Barcode.icontains(code)))
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")                                            
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                remTag(session,r,tag)
                                                session.refresh(r)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                                    
                                                #print(f"{Fore.light_yellow}{num}{Style.reset}/{Fore.light_red}{ct}{Style.reset} -> {r}")
                                                #remTag(session,r,tag)

                                    def c_do(self,code,tag):
                                        with Session(self.engine) as session:
                                            query=session.query(Entry).filter(or_(Entry.Code==code,Entry.Code.icontains(code)))
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                remTag(session,r,tag)
                                                session.refresh(r)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                                    
                                    def do(self,code,tag):
                                        with Session(self.engine) as session:
                                            query=session.query(Entry).filter(or_(Entry.Code==code,Entry.Barcode==code,Entry.Code.icontains(code),Entry.Barcode.icontains(code)))
                                            results=query.all()
                                            ct=len(results)
                                            if len(results)==0:
                                                print(f"{Fore.light_red}No Entry was found to match that code '{code}'{Style.reset}")
                                            for num,r in enumerate(results):
                                                if num%2==0:
                                                    colorEntry=Style.bold
                                                else:
                                                    colorEntry=Fore.grey_70+Style.underline
                                                remTag(session,r,tag)
                                                session.refresh(r)
                                                compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                                                if num == 0:
                                                    color1=Fore.light_green
                                                elif num > 0 and num%2==0:
                                                    color1=Fore.green_yellow
                                                elif num > 0 and num%2!=0:
                                                    color1=Fore.dark_goldenrod
                                                elif num+1 == ct:
                                                    color1=Fore.light_red
                                                print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
                                                    
                                    ex={
                                        'delim':'.',
                                        'e_do':lambda code,tag=tag,self=self:e_do(self,code,tag),
                                        'c_do':lambda code,tag=tag,self=self:c_do(self,code,tag),
                                        'b_do':lambda code,tag=tag,self=self:b_do(self,code,tag),
                                        'do':lambda code,tag=tag,self=self:do(self,code,tag)
                                    }
                                    status=Prompt(func=prefix_filter,ptext="Code|Barcode|(e|B|c).$code) ",helpText="Code|Barcode|EntryId to have tag remove from (prefix will use the specified field e. == EntryID, c. == Code, B. == Barcode.)",data=ex)
                                    if status.status == False:
                                        break   
                                except Exception as e:
                                    print(e)

                        break
                    except Exception as e:
                        print(e)
            elif cmd.lower() in ['reset_all_tags','clear_all_tags',]:
                with Session(self.engine) as session:
                    query=session.query(Entry)
                    results=query.all()
                    ct=len(results)
                    if ct == 0:
                        print(f"{Fore.light_red}No Entry's with Tags to reset!{Style.reset}")
                    for num,r in enumerate(results):
                        if num%2==0:
                            colorEntry=Style.bold
                        else:
                            colorEntry=Fore.grey_70+Style.underline
                        compound=f'{colorEntry}{r.Name}|{r.Barcode}|{r.Code}|{r.EntryId}|{r.Tags}{Style.reset}'
                        if num == 0:
                            color1=Fore.light_green
                        elif num > 0 and num%2==0:
                            color1=Fore.green_yellow
                        elif num > 0 and num%2!=0:
                            color1=Fore.dark_goldenrod
                        elif num+1 == ct:
                            color1=Fore.light_red

                        print(f"{color1}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} {compound}")
            else:
                split_cmd=cmd.split(",")
                if len(split_cmd) == 4:
                    #$mode,$search_fieldname,$EntryId,$tag
                    mode=split_cmd[0]
                    tag=[split_cmd[1],] 
                    search_fieldname=split_cmd[2]
                    eid=split_cmd[3]
                    with Session(self.engine) as session:
                        #print(split_cmd,type(eid),search_fieldname)
                        if search_fieldname == 'Barcode':
                            rs=session.query(Entry).filter(Entry.Barcode==eid).all()
                        elif search_fieldname == 'Code':
                            rs=session.query(Entry).filter(Entry.Code==eid).all()
                        elif search_fieldname == 'ALT_Barcode':
                            rs=session.query(Entry).filter(Entry.ALT_Barcode==eid).all()
                        elif search_fieldname == 'EntryId':
                            rs=session.query(Entry).filter(Entry.ALT_Barcode==int(eid)).all()
                        else:
                            print(self.helpText_tags)
                            return
                        #result=session.query(Entry).filter(getattr(Entry,search_fieldname)==eid).all()
                        result=rs
                        #print(len(result))
                        for num,r in enumerate(result):
                            msg=''
                            if r.Tags == '':
                                 r.Tags=json.dumps(list(tag))
                            session.commit()
                            session.refresh(r)
                            
                            if mode in ['=','r','R']:
                                r.Tags=json.dumps(list(tag))
                            elif mode == '+':
                                try:
                                    old=json.loads(r.Tags)
                                    if tag[0] not in old:
                                        old.append(tag[0])
                                        r.Tags=json.dumps(old)
                                    else:
                                        msg=f"{Fore.light_yellow}Tag is Already Applied Nothing will be Done!{Style.reset}"
                                except Exception as e:
                                    print(e)
                            elif mode == '-':
                                try:
                                    old=json.loads(r.Tags)
                                    if tag[0] in old:
                                        i=old.index(tag[0])
                                        old.pop(i)
                                        r.Tags=json.dumps(old)
                                    else:
                                        msg=f"{Fore.light_red}No Such Tag in Item...{Fore.light_yellow} Nothing will be done!{Style.reset}"
                                except Exception as e:
                                    print(e)
                                

                            
                            session.commit()
                            session.flush()
                            session.refresh(r)
                            print(r)
                            print(msg)
                else:
                    print(self.helpText_tags)


    def setName(self):
        with Session(self.engine) as session:
            def mkT(text,self):
                    return text
            fieldname='SetName'
            mode='TaskMode'
            h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
            code=Prompt.__init2__(None,func=mkT,ptext=f'{h}Code|Barcode[help]?',helpText='',data=self)
            if not code:
                return
            
            value=Prompt.__init2__(None,func=mkT,ptext='Name[help]?',helpText='',data=self)
            if not value:
                return
           
            result=session.query(Entry).filter(or_(Entry.Barcode==code,Entry.Code==code)).first()
            if result:
                result.Name=value
                session.commit()
                session.flush()
                session.refresh(result)
                print(result)
            else:
                print(f"{Fore.light_red}{Style.bold}No Such Item Identified by '{code}'{Style.reset}")

    def list_total(self):
        with Session(self.engine) as session:
            results=session.query(Entry).filter(Entry.InList==True).all()
            ct=len(results)
            total=0
            total_case=0
            total_units=0
            total_units_br=0
            for num,r in enumerate(results):
                print(f"{Fore.green}{num}{Style.reset}/{Fore.light_red}{ct-1}{Style.reset} -> {r}")
                total+=r.total_value(CaseMode=False)
                total_case+=r.total_value(CaseMode=True)
                total_units+=r.total_units()
                total_units_br+=r.total_units(BackRoom=False)
            #print(total_units,total_units_br)
            print(f"""
{Fore.light_green}Total By Units: ${Fore.light_red}{total}{Style.reset}{Fore.green_yellow} for{Fore.light_red} {total_units} w/BackRoom{Fore.light_green} | {total_units_br} {Fore.light_magenta}wo/BackRoom{Style.reset}
{Fore.light_green}Total By Case: ${Fore.light_red}{total_case}{Style.reset}{Fore.green_yellow} for{Fore.light_red} {total_units} w/BackRoom{Fore.light_green} | {total_units_br} {Fore.light_magenta}wo/BackRoom{Style.reset} 
""")
    def clear_system_tags(self,tags):
        ct=len(tags)
        for num,tag in enumerate(tags):
            print(f"removing tag {num}/{ct-1} '{tag}'")
            tagList(engine=self.engine,state=False,tag=tag)

    def __init__(self,engine,parent):
        self.engine=engine
        self.parent=parent
        self.special=['Tags','ALT_Barcode','DUP_Barcode','CaseID_6W','CaseID_BR','CaseID_LD','Facings']
        self.valid_fields=['Shelf',
        'BackRoom',
        'Display_1',
        'Display_2',
        'Display_3',
        'Display_4',
        'Display_5',
        'Display_6',
        'ALT_Barcode',
        'DUP_Barcode',
        'CaseID_BR',
        'CaseID_LD',
        'CaseID_6W',
        'Tags',
        'Facings',
        'SBX_WTR_DSPLY',
        'SBX_CHP_DSPLY',
        'SBX_WTR_KLR',
        'FLRL_CHP_DSPLY',
        'FLRL_WTR_DSPLY',
        'WD_DSPLY',
        'CHKSTND_SPLY',
        ]
        '''
        ALT_Barcode=Column(String)
        DUP_Barcode=Column(String)
        CaseID_BR=Column(String)
        CaseID_LD=Column(String)
        CaseID_6W=Column(String)
        Tags=Column(String)
        Facings=Column(Integer)
        SBX_WTR_DSPLY=Column(Integer)
        SBX_CHP_DSPLY=Column(Integer)
        SBX_WTR_KLR=Column(Integer)
        FLRL_CHP_DSPLY=Column(Integer)
        FLRL_WTR_DSPLY=Column(Integer)
        WD_DSPLY=WD_DSPLY=Column(Integer)
        CHKSTND_SPLY=CHKSTND_SPLY=Column(Integer)
        '''
        #self.display_field("Shelf")
        self.options={
                '1':{
                    'cmds':['q','quit','#1'],
                    'desc':"quit program",
                    'exec':lambda: exit("user quit!"),
                    },
                '2':{
                    'cmds':['b','back','#2'],
                    'desc':'go back menu if any',
                    'exec':None
                    },
                }
        #autogenerate duplicate functionality for all valid fields for display
        count=3
        location_fields={
            "Shelf":None,
            "BackRoom":None,
            "Display_1":None,
            "Display_2":None,
            "Display_3":None,
            "Display_4":None,
            "Display_5":None,
            "Display_6":None,
            "ListQty":None,
            "SBX_WTR_DSPLY":None,
            "SBX_CHP_DSPLY":None,
            "SBX_WTR_KLR":None,
            "FLRL_CHP_DSPLY":None,
            "FLRL_WTR_DSPLY":None,
            "WD_DSPLY":None,
            "CHKSTND_SPLY":None,

            "set Shelf":None,
            "set BackRoom":None,
            "set Display_1":None,
            "set Display_2":None,
            "set Display_3":None,
            "set Display_4":None,
            "set Display_5":None,
            "set Display_6":None,
            "set ListQty":None,
            "set ListQty":None,
            "set SBX_WTR_DSPLY":None,
            "set SBX_CHP_DSPLY":None,
            "set SBX_WTR_KLR":None,
            "set FLRL_CHP_DSPLY":None,
            "set FLRL_WTR_DSPLY":None,
            "set WD_DSPLY":None,
            "set CHKSTND_SPLY":None,
        }
        def print_location_fields(location_fields):
            for num,k in enumerate(location_fields):
                if num%2==0:
                    color1_field=Fore.sea_green_1a
                    cmd_alter=Fore.light_steel_blue
                else:
                    color1_field=Fore.spring_green_1
                    cmd_alter=Fore.cyan
                if 'set ' in k:
                    tmp=f'{Fore.orange_red_1}{Style.bold}*{Style.reset}'
                else:
                    tmp=''
                #print(location_fields[k],f'"{k}"')
                msg=f"{tmp}{color1_field}{k}{Style.reset} - {'|'.join([f'{cmd_alter}{i}{Style.reset}' for i in location_fields[k]])}"
                print(msg)

        for entry in self.valid_fields:
            self.options[entry]={
                    'cmds':["#"+str(count),f"ls {entry}"],
                    'desc':f'list needed @ {entry}',
                    'exec':lambda self=self,entry=entry: self.display_field(f"{entry}"),
                    }
            if entry in list(location_fields.keys()):
                location_fields[entry]=self.options[entry]['cmds']
            count+=1

        #setoptions
        #self.setFieldInList("Shelf")
        for entry in self.valid_fields:
            self.options[entry+"_set"]={
                    'cmds':["#"+str(count),f"set {entry}"],
                    'desc':f'set needed @ {entry}',
                    'exec':lambda self=self,entry=entry: self.setFieldInList(f"{entry}"),
                    }
            if f"set {entry}" in list(location_fields.keys()):
                location_fields[f"set {entry}"]=self.options[entry+"_set"]['cmds']
            count+=1
        self.options["lu"]={
                    'cmds':["#"+str(count),f"lookup","lu","check","ck"],
                    'desc':f'get total for valid fields',
                    'exec':lambda self=self,entry=entry: self.getTotalwithBreakDownForScan(),
                    }
        count+=1
        self.options["setName"]={
                    'cmds':["#"+str(count),f"setName","sn"],
                    'desc':f'set name for item by barcode!',
                    'exec':lambda self=self,entry=entry: self.setName(),
                    }
        count+=1
        self.options["setListQty"]={
                    'cmds':["#"+str(count),f"setListQty","slq"],
                    'desc':f'set ListQty for Values not wanted to be included in totals.',
                    'exec':lambda self=self: self.setFieldInList("ListQty",load=True),
                    }
        location_fields["set ListQty"]=self.options["setListQty"]['cmds']
        count+=1
        self.options["lsListQty"]={
                    'cmds':["#"+str(count),f"lsListQty","ls-lq"],
                    'desc':f'show ListQty for Values not wanted to be included in totals.',
                    'exec':lambda self=self: self.display_field("ListQty",load=True),
                    }
        location_fields["ListQty"]=self.options["lsListQty"]['cmds']
        count+=1
        self.options["listTotal"]={
                    'cmds':["#"+str(count),f"listTotal","list_total"],
                    'desc':f'show list total value.',
                    'exec':lambda self=self: self.list_total(),
                    }
        count+=1
        self.options["lus"]={
                    'cmds':["#"+str(count),f"lookup_short","lus","lu-","check","ck-","ls"],
                    'desc':f'get total for valid fields short view',
                    'exec':lambda self=self,entry=entry: self.getTotalwithBreakDownForScan(short=True),
                    }
        count+=1
        self.options["b1"]={
                    'cmds':["#"+str(count),f"barcode_first","b1"],
                    'desc':f'list mode where barcode is asked first',
                    'exec':lambda self=self: self.setFieldInList(None,load=True),
                    }
        count+=1
        self.options["el2e"]={
                    'cmds':["#"+str(count),f"export-list-2-excel","el2e"],
                    'desc':f'export fields {self.exportList2Excel(fields=True)} to Excel file',
                    'exec':lambda self=self: self.exportList2Excel(),
                    }
        count+=1
        self.options["formula"]={
                    'cmds':["#"+str(count),f"formula","eval","calc"],
                    'desc':f'solve an equation',
                    'exec':lambda self=self: self.evaluateFormula(),
                    }
        count+=1
        self.options["tag_reverse_inventory_1"]={
                    'cmds':["#"+str(count),f"tag_reverse_inventory_1","tri1",],
                    'desc':f'add Tag "ReverseInventory" to Entry\'s with InList==True',
                    'exec':lambda self=self: tagList(engine=self.engine,state=True,tag="ReverseInventory",removeTag=['have/has',]),
                    }
        count+=1
        self.options["tag_reverse_inventory_0"]={
                    'cmds':["#"+str(count),f"tag_reverse_inventory_0","tri0",],
                    'desc':f'remove Tag "ReverseInventory" to Entry\'s with InList==True',
                    'exec':lambda self=self: tagList(engine=self.engine,state=False,tag="ReverseInventory"),
                    }
        count+=1
        self.options["tag_have/has_1"]={
                    'cmds':["#"+str(count),f"tag_have/has_1","th1",],
                    'desc':f'add Tag "have/has" to Entry\'s with InList==True',
                    'exec':lambda self=self: tagList(engine=self.engine,state=True,tag="have/has",removeTag=["ReverseInventory",]),
                    }
        count+=1
        self.options["tag_have/has_0"]={
                    'cmds':["#"+str(count),f"tag_have/has_0","th0",],
                    'desc':f'remove Tag "have/has" to Entry\'s with InList==True',
                    'exec':lambda self=self: tagList(engine=self.engine,state=False,tag="have/has"),
                    }
        count+=1
        self.options["clear_system_tags"]={
                    'cmds':["#"+str(count),f"clear_system_tags","cst",],
                    'desc':f'remove/clear system tags',
                    'exec':lambda self=self: self.clear_system_tags(["have/has","ReverseInventory",])
                    }
        count+=1
        self.options["addPersonalTags"]={
                    'cmds':["#"+str(count),f"pt1","personal_tag_1",],
                    'desc':f'add a personal tag to list',
                    'exec':lambda self=self: tagList(engine=self.engine,state=True,tag=None,removeTag=['',])
                    }
        count+=1
        self.options["remPersonalTags"]={
                    'cmds':["#"+str(count),f"pt0","personal_tag_0",],
                    'desc':f'remove a personal tag from list',
                    'exec':lambda self=self: tagList(engine=self.engine,state=False,tag=None,removeTag=['',])
                    }
        count+=1
        self.options["list location fields"]={
                    'cmds':["#"+str(count),f"llf","list location fields","list_location_fields"],
                    'desc':f'list location fields cmds',
                    'exec':lambda self=self: print_location_fields(location_fields),
                    }
        count+=1
        self.options["new entry from schematic"]={
                    'cmds':["#"+str(count),f"nefs","new entry from schematic","new_entry_from_schematic"],
                    'desc':f'add a new entry from schematic directly, checking for new item by barcode',
                    'exec':lambda self=self: self.NewEntrySchematic(),
                    }
        count+=1


        while True:
            def mkT(text,self):
                return text
            command=Prompt.__init2__(None,func=mkT,ptext=f'{Fore.grey_70}[{Fore.light_steel_blue}TaskMode{Fore.grey_70}] {Fore.light_yellow}Do What[help/??/?]',helpText=self.parent.help(print_no=True),data=self)
            if not command:
                break
            #command=input(f"{Style.bold}{Fore.green}do what[??/?]:{Style.reset} ")
            if self.parent != None and self.parent.Unified(command):
                print("ran a Unified CMD")
            elif command == "??":
                for num,option in enumerate(self.options):
                    color=Fore.dark_goldenrod
                    color1=Fore.cyan
                    if (num%2)==0:
                        color=Fore.green_yellow
                        color1=Fore.magenta
                    print(f"{color}{self.options[option]['cmds']}{Style.reset} - {color1}{self.options[option]['desc']}{Style.reset}")
            else:
                for option in self.options:
                    if self.options[option]['exec'] != None and (command.lower() in self.options[option]['cmds'] or command in self.options[option]['cmds']):
                        self.options[option]['exec']()
                    elif self.options[option]['exec'] == None and (command.lower() in self.options[option]['cmds'] or command in self.options[option]['cmds']):
                        return
    
    def evaluateFormula(self):
        while True:
            try:
                accro=Style.bold+Style.underline+Fore.light_red
                p1=Fore.light_magenta
                p2=Fore.light_yellow
                p3=Fore.light_green
                p4=Fore.cyan
                p5=Fore.sea_green_1a
                p6=Fore.green_yellow
                p7=Fore.dark_goldenrod
                symbol=Fore.magenta
                helpText=f'''
{accro}Operator Symbol -> {symbol}()|**|*|/|+|-{Style.reset}
{accro}CVT(value,fromUnit,toUnit) -> {symbol}Convert a value from one to another{Style.reset}
{accro}datetime()+|-datetime()|timedelta() -> {symbol}Add or Subtract datetimes{Style.reset}
{accro}if you know a tool in pandas use pd, or numpy use np ->{symbol}module support for advanced math operations on a single line{Style.reset}
{accro}PEMDAS{Style.reset} - {p1}Please {p2}Excuse {p4}My {p5}Dear {p6}Aunt {p7}Sallie{Style.reset}
{accro}PEMDAS{Style.reset} - {p1}{symbol}({Style.reset}{p1}Parantheses{symbol}){Style.reset} {p3}Exponents{symbol}** {p4}Multiplication{symbol}* {p5}Division{symbol}/ {p6}Addition{symbol}+ {p7}Subtraction{symbol}-{Style.reset}
                '''
                def mkValue(text,self):
                    try:
                        CVT=UnitRegistry().convert
                        return eval(text)
                    except Exception as e:
                        print(e)
                fieldname='TaskMode'
                mode='Calculator'
                h=f'{Prompt.header.format(Fore=Fore,mode=mode,fieldname=fieldname,Style=Style)}'
                formula=Prompt.__init2__(None,func=mkValue,ptext=f"{h}Type|Tap your equation and remember PEMDAS",helpText=helpText,data=self)
                if formula in [None,]:
                    break
                print(formula)
            except Exception as e:
                print(e)




if __name__ == "__main__":
    TasksMode(parent=None,engine=ENGINE)
