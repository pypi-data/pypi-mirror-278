import re

#=============================================================
# THESE A JUST UTILITY FUNCTIONS TO BE ABLE TO MANIPULATE CODE
#=============================================================

#Function that returns the next character (+ it's index)
def get_next_element_caracter(string, i):
    while(i+1<len(string)):
        i+=1
        if(string[i]!=' ' and string[i]!='\n'and string[i]!='\t'):
            return string[i], i
    return -1, -1

#Function that returns the character before (+ it's index)
def get_before_element_caracter(string, i):
    while(i>0):
        i-=1
        if(string[i]!=' ' and string[i]!='\n'and string[i]!='\t'):
            return string[i], i
    return -1, -1

def get_curly_count(code):
    curly_count = 0
    quote_single, quote_double = False, False
    triple_single, triple_double = False, False
    for end in range(len(code)):
        checked_triple = False
        if(end+3<=len(code)):
            if(code[end:end+3]=="'''" and not quote_single and not quote_double and not triple_single and not triple_double):
                triple_single = True
                end+=3
                checked_triple = True
            elif(code[end:end+3]=="'''" and not quote_single and not quote_double and triple_single and not triple_double):
                triple_single = False
                end+=3
                checked_triple = True

            if(code[end:end+3]=='"""' and not quote_single and not quote_double and not triple_single and not triple_double):
                triple_double = True
                end+=3
                checked_triple = True
            elif(code[end:end+3]=='"""' and not quote_single and not quote_double and not triple_single and triple_double):
                triple_double = False
                end+=3
                checked_triple = True
        
        if(not checked_triple):
            if(code[end]=="{" and not quote_single and not quote_double and not triple_double):
                curly_count+=1
            if(code[end]=="}" and not quote_single and not quote_double and not triple_double):
                curly_count-=1
            
            if(code[end]=="'" and not quote_single and not quote_double and not triple_double):
                if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                    quote_single=True
            elif(code[end]=="'" and quote_single and not quote_double and not triple_double):
                if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                    quote_single=False

            if(code[end]=='"' and not quote_single and not quote_double and not triple_double):
                if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                    quote_double=True
            elif(code[end]=='"' and not quote_single and quote_double and not triple_double):
                if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                    quote_double=False
    return curly_count

def get_single_count(code):
    single_count = 0
    quote_single, quote_double = False, False
    for end in range(len(code)):        
        if(code[end]=="'" and not quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_single=True
                single_count+=1
        elif(code[end]=="'" and quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_single=False
                single_count-=1

        if(code[end]=='"' and not quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_double=True
        elif(code[end]=='"' and not quote_single and quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_double=False
    return single_count

def get_double_count(code):
    double_count = 0
    quote_single, quote_double = False, False
    for end in range(len(code)):        
        if(code[end]=="'" and not quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_single=True
        elif(code[end]=="'" and quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_single=False
    
        if(code[end]=='"' and not quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_double=True
                double_count+=1
        elif(code[end]=='"' and not quote_single and quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_double=False
                double_count-=1
    return double_count


#Function that returns the parenthese count of a bit of code
def get_parenthese_count(code):
    parenthese_count = 0
    quote_single, quote_double = False, False
    triple_single, triple_double = False, False
    for end in range(len(code)):
        checked_triple = False
        if(end+3<=len(code)):
            if(code[end:end+3]=="'''" and not quote_single and not quote_double and not triple_single and not triple_double):
                triple_single = True
                end+=3
                checked_triple = True
            elif(code[end:end+3]=="'''" and not quote_single and not quote_double and triple_single and not triple_double):
                triple_single = False
                end+=3
                checked_triple = True

            if(code[end:end+3]=='"""' and not quote_single and not quote_double and not triple_single and not triple_double):
                triple_double = True
                end+=3
                checked_triple = True
            elif(code[end:end+3]=='"""' and not quote_single and not quote_double and not triple_single and triple_double):
                triple_double = False
                end+=3
                checked_triple = True
        
        if(not checked_triple):
            if(code[end]=="(" and not quote_single and not quote_double and not triple_single and not triple_double):
                parenthese_count+=1
            if(code[end]==")" and not quote_single and not quote_double and not triple_single and not triple_double):
                parenthese_count-=1

            if(code[end]=="'" and not quote_single and not quote_double and not triple_single and not triple_double):
                if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                    quote_single=True
            elif(code[end]=="'" and quote_single and not quote_double and not triple_single and not triple_double):
                if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                    quote_single=False

            if(code[end]=='"' and not quote_single and not quote_double and not triple_single and not triple_double):
                if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                    quote_double=True
            elif(code[end]=='"' and not quote_single and quote_double and not triple_single and not triple_double):
                if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                    quote_double=False
    return parenthese_count


#Function that returns a subpart of the code until the parenthse_count equals the given value
def get_code_until_parenthese_count(code, val, left_2_right = True):
    parenthese_count = 0
    quote_single, quote_double = False, False
    if(left_2_right):
        tab = list(range(len(code)))
    else:
        tab = list(range(len(code)-1, -1, -1))
    for end in tab:
        if(parenthese_count==val):
            if(left_2_right):
                return code[:end]    
            else:
                return code[end:]

        if(code[end]=="(" and not quote_single and not quote_double):
            parenthese_count+=1
        if(code[end]==")" and not quote_single and not quote_double):
            parenthese_count-=1
        
        if(code[end]=="'" and not quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_single=True
            
        elif(code[end]=="'" and quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_single=False

        if(code[end]=='"' and not quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_double=True
        elif(code[end]=='"' and not quote_single and quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_double=False
    
    if(parenthese_count==val):
        return code  
    return None


#This function takes some code, the begining of an operator and the end, then extracts
#the whole executor
def extract_executor_from_middle(code, start, end):
    save_start, save_end = start, end
    find_start, find_end = False, False

    #Basically the logic here is that at the start of operation curly or parenthese count can be positive but never negative (see example below)
    curly_count, parenthese_count = 0, 0
    quote_single, quote_double = False, False


    while(not find_start):
        if(start<0):
            raise Exception(f"Couldn't find the start of the executor : {code[save_start:save_end]}")
        
        if(code[end]=="{" and not quote_single and not quote_double):
            curly_count+=1
        if(code[end]=="}" and not quote_single and not quote_double):
            curly_count-=1
        if(code[end]=="(" and not quote_single and not quote_double):
            parenthese_count+=1
        if(code[end]==")" and not quote_single and not quote_double):
            parenthese_count-=1
        if(code[end]=="'" and not quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_single=True
        elif(code[end]=="'" and quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_single=False
        if(code[end]=='"' and not quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_double=True
        elif(code[end]=='"' and not quote_single and quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_double=False
        
        next_character, _ = get_next_element_caracter(code, start)
        character_before, _ = get_before_element_caracter(code, start)
        

        if(code[start]=='\n' and (re.fullmatch("\w", next_character) or next_character in ['(']) and character_before not in ['(', '[', ',', '.', '|'] and curly_count>=0 and parenthese_count>=0 and not quote_single and not quote_single):
        #if(code[start]=='\n' and character_before not in ['(', '[', ',', '.', '|'] and curly_count>=0 and parenthese_count>=0 and not quote_single and not quote_single):
            find_start = True
        else:
            start-=1


    #Basically the logic here is that at the end of operation curly or parenthese count can be negative but never positive
    #For example (.join is detected first):
    #trim_reads
    #.join(trim_log)
    #.map {
    #    meta, reads, trim_log ->
    #        if (!meta.single_end) {
    #            trim_log = trim_log[-1]
    #        }
    #        if (getTrimGaloreReadsAfterFiltering(trim_log) > 0) {
    #            [ meta, reads ]
    #        }
    #}
    #.set { trim_reads }
    
    curly_count, parenthese_count = 0, 0
    quote_single, quote_double = False, False


    while(not find_end):
        if(end>=len(code)):
            raise Exception(f"Couldn't find the end of the executor : {code[start:save_end]}")
        

        if(code[end]=="{" and not quote_single and not quote_double):
            curly_count+=1
        if(code[end]=="}" and not quote_single and not quote_double):
            curly_count-=1
        if(code[end]=="(" and not quote_single and not quote_double):
            parenthese_count+=1
        if(code[end]==")" and not quote_single and not quote_double):
            parenthese_count-=1
        if(code[end]=="'" and not quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_single=True
        elif(code[end]=="'" and quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_single=False
        if(code[end]=='"' and not quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_double=True
        elif(code[end]=='"' and not quote_single and quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_double=False



        next_character, next = get_next_element_caracter(code, end)
        next_next_character, next = get_next_element_caracter(code, next)
        character_before, _ = get_before_element_caracter(code, end)
        #TODO -> my intuition tells me i need to add next_character in ['}', ')'])
        #But it creates a problem in this example
        #MERGED_LIBRARY_ATAQV_MKARV (
        #    MERGED_LIBRARY_ATAQV_ATAQV.out.json.collect{it[1]}
        #)
        #v0
        #if(code[end]=='\n' and (re.fullmatch("\w", next_character) or next_character in ['}', '/', '|']) and character_before in [')', '}'] and curly_count<=0 and parenthese_count<=0 and not quote_single and not quote_single):
        #v1
        #if(code[end]=='\n' and (re.fullmatch("\w", next_character) or next_character in ['}', '/', '|']) and curly_count<=0 and parenthese_count<=0 and not quote_single and not quote_single):
        #v2
        if(code[end]=='\n' and (re.fullmatch("\w", next_character) or next_character in ['}', '/', '|']) and character_before not in [','] and next_next_character not in ['.', '|'] and curly_count<=0 and parenthese_count<=0 and not quote_single and not quote_single):
            find_end = True
        else:
            end+=1

    return code[start:end].strip()


def extract_end_operation(code, start, end):
    curly_count, parenthese_count , bracket_count= 0, 0, 0
    quote_single, quote_double = False, False
    finish = False
    while(not finish):
        if(end>=len(code)):
            raise Exception('Unable to extract')
        elif(code[end]=="{" and not quote_single and not quote_double):
            curly_count+=1
        elif(code[end]=="}" and not quote_single and not quote_double):
            curly_count-=1
        elif(code[end]=="(" and not quote_single and not quote_double):
            parenthese_count+=1
        elif(code[end]==")" and not quote_single and not quote_double):
            parenthese_count-=1
        elif(code[end]=="[" and not quote_single and not quote_double):
            bracket_count+=1
        elif(code[end]=="]" and not quote_single and not quote_double):
            bracket_count-=1
        elif(code[end]=="'" and not quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_single=True
        elif(code[end]=='"' and not quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_double=True
        elif(code[end]=="'" and quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_single=False
        elif(code[end]=='"' and not quote_single and quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_double=False

        character_before, _ = get_before_element_caracter(code, end)
        next_character, _ = get_next_element_caracter(code, end)
        if(code[end]=='\n' and next_character not in ['.', "|"] and curly_count==0 and parenthese_count==0 and bracket_count==0 and not quote_single and not quote_double and character_before!="|"):
        #if(next_character!='.' and curly_count==0 and parenthese_count==0 and not quote_single and not quote_double):
            finish = True
        elif((curly_count<0 or parenthese_count<0 or bracket_count<0)  and character_before in [')', '}'] and not quote_single and not quote_double):
            finish = True
        else:
            end+=1
    return code[start:end].strip()

#Function that 'finds' the end of the process, when we give the start position
#So it follows the pattern 'process name {....}'
def extract_curly(text, start):

    end = start
    code= text
    curly_count, parenthese_count = 1, 0
    quote_single, quote_double = False, False
    triple_single, triple_double = False, False


    while(parenthese_count!=0 or curly_count!=0 or quote_single or quote_double or triple_single or triple_double): 
        #print(parenthese_count, curly_count, quote_single, quote_double, triple_single, triple_double)

        
        checked_triple = False
        if(end+3<=len(code)):
            if(code[end:end+3]=="'''" and not quote_single and not quote_double and not triple_single and not triple_double):
                triple_single = True
                end+=3
                checked_triple = True
            elif(code[end:end+3]=="'''" and not quote_single and not quote_double and triple_single and not triple_double):
                triple_single = False
                end+=3
                checked_triple = True

            if(code[end:end+3]=='"""' and not quote_single and not quote_double and not triple_single and not triple_double):
                triple_double = True
                end+=3
                checked_triple = True
            elif(code[end:end+3]=='"""' and not quote_single and not quote_double and not triple_single and triple_double):
                triple_double = False
                end+=3
                checked_triple = True
        
        if(not checked_triple):
            if(code[end]=="{" and not quote_single and not quote_double and not triple_single and not triple_double):
                curly_count+=1
            elif(code[end]=="}" and not quote_single and not quote_double and not triple_single and not triple_double):
                curly_count-=1
            
            if(code[end]=="(" and not quote_single and not quote_double and not triple_single and not triple_double):
                parenthese_count+=1
            elif(code[end]==")" and not quote_single and not quote_double and not triple_single and not triple_double):
                parenthese_count-=1

            if(code[end]=="'" and not quote_single and not quote_double and not triple_single and not triple_double):
                if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                    quote_single=True
            elif(code[end]=="'" and quote_single and not quote_double and not triple_single and not triple_double):
                if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                    quote_single=False

            if(code[end]=='"' and not quote_single and not quote_double and not triple_single and not triple_double):
                if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                    quote_double=True
            elif(code[end]=='"' and not quote_single and quote_double and not triple_single and not triple_double):
                if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                    quote_double=False

            end+=1

        if(end>len(code)):
            raise Exception('Unable to extract')
    return end



def get_end_operator(code, start, end, beginning_character):
    curly_count, parenthese_count = 0, 0
    quote_single, quote_double = False, False
    
    start_param = end
    if(beginning_character=="("):
        parenthese_count+=1
    if(beginning_character=="{"):
        curly_count+=1

    while(parenthese_count!=0 or curly_count!=0 or quote_single or quote_double):     
        if(code[end]=="{" and not quote_single and not quote_double):
            curly_count+=1
        if(code[end]=="}" and not quote_single and not quote_double):
            curly_count-=1
        if(code[end]=="(" and not quote_single and not quote_double):
            parenthese_count+=1
        if(code[end]==")" and not quote_single and not quote_double):
            parenthese_count-=1
        if(code[end]=="'" and not quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_single=True
        elif(code[end]=="'" and quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_single=False
        if(code[end]=='"' and not quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_double=True
        elif(code[end]=='"' and not quote_single and quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_double=False
        end+=1
        if(end>len(code)):
            raise Exception('Unable to extract')
        
    return code[start:end].strip(), code[start_param:end-1].strip()



#=====================================================
#FUNCTIONS FOR THE CODE CLASS -> REMOVE COMMENTS ETC..
#=====================================================

def remove_comments(input_text):

    input_text= input_text+"\n\n\n"
    #Remove the \" and \' in the code
    input_text = re.sub(r'([^\\])\\"', r'\g<1>', input_text)
    input_text = re.sub(r"([^\\])\\'", r'\g<1>', input_text)
    #Remove the /'/ and /"/ in the code
    input_text = re.sub(r'\/"\/', "", input_text)
    input_text = re.sub(r"\/'\/", "", input_text)
    ##replace the '"${...}"' by '"""${...}"""'
    #input_text = re.sub(r'" *(\$ *{[^}]*}) *"', r'"""\g<1>"""', input_text)
    #input_text = re.sub(r"' *(\$ *{[^}]*}) *'", r"'''\g<1>'''", input_text)
    
    

    #input_text = input_text.replace('/\/*', '"').replace('\/*$/', '"')#TODO check if i actually wanna do this -> Etjean/Long_project/masque.nf
    #TO remove `/\/* ... \/*$/ and /[fasta|fa]$/
    input_text = re.sub(r'\/\\\/\*([^(\\\/\*\$\/)]+)\\\/\*\$\/', r'"\g<1>"', input_text)

    #input_text = re.sub(r'\/([^($\/)]+)\$\/', r'"\g<1>"', input_text)
    #if(temp!=input_text):
    #    print("-",start)
    
    to_remove = []
    quote_single, quote_double = False, False
    triple_single, triple_double = False, False
    in_bloc, in_single_line = False, False
    start, end = 0, 0
    i=0
    while(i<len(input_text)-3):
    #for i in range(len(input_text)-3):
        #Case single line comment "//"
        if(input_text[i:i+2]=="//" and not quote_single and not quote_double and not in_bloc and not in_single_line and not triple_single and not triple_double):
            is_comment_one_line = True
            if(i-1>=0):
                if(input_text[i-1]=='\\'):
                    is_comment_one_line=False
            if(is_comment_one_line):
                start = i
                in_single_line = True
                i+=2
            else:
                i+=1
        elif(input_text[i]=="\n" and not quote_single and not quote_double and not in_bloc and in_single_line and not triple_single and not triple_double):
            end = i
            in_single_line = False
            to_remove.append(input_text[start:end+1])
            i+=1
        #Case bloc comment "/*...*/"
        elif(input_text[i:i+2]=="/*" and not quote_single and not quote_double and not in_bloc and not in_single_line and not triple_single and not triple_double):
            start = i
            in_bloc = True
            i+=2
        elif(input_text[i:i+2]=="*/" and not quote_single and not quote_double and in_bloc and not in_single_line and not triple_single and not triple_double):
            end = i+2
            in_bloc = False
            to_remove.append(input_text[start:end])
            i+=2
        #ELSE
        #Triple single
        elif(input_text[i:i+3]=="'''" and not quote_single and not quote_double and not in_bloc and not in_single_line and not triple_single and not triple_double):
            triple_single = True
            i+=3
        elif(input_text[i:i+3]=="'''" and not quote_single and not quote_double and not in_bloc and not in_single_line and triple_single and not triple_double):
            triple_single = False
            i+=3
        #Triple double
        elif(input_text[i:i+3]=='"""' and not quote_single and not quote_double and not in_bloc and not in_single_line and not triple_single and not triple_double):
            triple_double = True
            i+=3
        elif(input_text[i:i+3]=='"""' and not quote_single and not quote_double and not in_bloc and not in_single_line and not triple_single and triple_double):
            triple_double = False
            i+=3
        #Case single
        elif(input_text[i]=="'" and not quote_single and not quote_double and not in_bloc and not in_single_line and not triple_single and not triple_double):
            #if(input_text[i-1]!="\\"):
            quote_single = True
            i+=1
        elif(input_text[i]=="'" and quote_single and not quote_double and not in_bloc and not in_single_line and not triple_single and not triple_double):
            #if(input_text[i-1]!="\\"):
            quote_single = False
            i+=1
        #Case double
        elif(input_text[i]=='"' and not quote_single and not quote_double and not in_bloc and not in_single_line and not triple_single and not triple_double):
            #if(input_text[i-1]!="\\"):
            quote_double = True
            i+=1
        elif(input_text[i]=='"' and not quote_single and quote_double and not in_bloc and not in_single_line and not triple_single and not triple_double):
            #if(input_text[i-1]!="\\"):
            quote_double = False
            i+=1
        else:
            i+=1

    for r in to_remove:
        if(r[:2]=="//"):
            input_text = input_text.replace(r, '\n', 1)
        else:
            nb_jumps = r.count('\n')
            input_text = input_text.replace(r, '\n'*nb_jumps, 1)
        
    return input_text



#----------------------
#Calls
#----------------------
def get_end_call(code, start, end):
    curly_count, parenthese_count = 0, 1
    quote_single, quote_double = False, False
    #Before it was this
    #while(parenthese_count!=0 or curly_count!=0 or quote_single or quote_double or code[end]!='\n'):
    while(parenthese_count!=0 or curly_count!=0 or quote_single or quote_double):
        if(end>=len(code)):
            raise Exception('Unable to extract')
        if(code[end]=="{" and not quote_single and not quote_double):
            curly_count+=1
        if(code[end]=="}" and not quote_single and not quote_double):
            curly_count-=1
        if(code[end]=="(" and not quote_single and not quote_double):
            parenthese_count+=1
        if(code[end]==")" and not quote_single and not quote_double):
            parenthese_count-=1
        if(code[end]=="'" and not quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_single=True
        elif(code[end]=="'" and quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_single=False
        if(code[end]=='"' and not quote_single and not quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_double=True
        elif(code[end]=='"' and not quote_single and quote_double):
            if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
                quote_double=False
        end+=1
    return code[start:end].strip()


#This function takes a string "param" and returns the next parameter
def get_next_param(param):
    curly_count, parenthese_count, bracket_count= 0, 0, 0
    quote_single, quote_double = False, False
    end= 0
    while(True):
        if(end>=len(param)):
            return param, -1
        if(parenthese_count==0 and curly_count==0 and bracket_count==0 and not quote_single and not quote_double and param[end]==','):
            return param[0:end], end+1
        
        if(param[end]=="{" and not quote_single and not quote_double):
            curly_count+=1
        elif(param[end]=="}" and not quote_single and not quote_double):
            curly_count-=1
        elif(param[end]=="(" and not quote_single and not quote_double):
            parenthese_count+=1
        elif(param[end]==")" and not quote_single and not quote_double):
            parenthese_count-=1
        elif(param[end]=="[" and not quote_single and not quote_double):
            bracket_count+=1
        elif(param[end]=="]" and not quote_single and not quote_double):
            bracket_count-=1
        elif(param[end]=="'" and not quote_single and not quote_double):
            if(param[end-1]!="\\"):
                quote_single=True
        elif(param[end]=='"' and not quote_single and not quote_double):
            if(param[end-1]!="\\"):
                quote_double=True
        elif(param[end]=="'" and quote_single and not quote_double):
            if(param[end-1]!="\\"):
                quote_single=False
        elif(param[end]=='"' and not quote_single and quote_double):
            if(param[end-1]!="\\"):
                quote_double=False
        end+=1

def update_parameters(code, end, curly_count, parenthese_count, quote_single, quote_double) :
    if(code[end]=="{" and not quote_single and not quote_double):
        curly_count+=1
    elif(code[end]=="}" and not quote_single and not quote_double):
        curly_count-=1
    elif(code[end]=="(" and not quote_single and not quote_double):
        parenthese_count+=1
    elif(code[end]==")" and not quote_single and not quote_double):
        parenthese_count-=1
    elif(code[end]=="'" and not quote_single and not quote_double):
        if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
            quote_single=True
    elif(code[end]=='"' and not quote_single and not quote_double):
        if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
            quote_double=True
    elif(code[end]=="'" and quote_single and not quote_double):
        if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
            quote_single=False
    elif(code[end]=='"' and not quote_single and quote_double):
        if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
            quote_double=False
    return curly_count, parenthese_count, quote_single, quote_double


def remove_jumps_inbetween_parentheses(code):
    code = re.sub(',\s*\n\s*', ', ', code)
    code = re.sub(';\s*\n\s*', '; ', code)
    code = list(code)
    parentheses_count = 0
    for i in range(len(code)):
        if(code[i]=="("):
            parentheses_count+=1
        elif(code[i]==")"):
            parentheses_count-=1
        elif(code[i]=="\n" and parentheses_count!=0):
            code[i] = " "
    code = "".join(code)
    code = re.sub(r", *\n", ", ", code)
    return code

def remove_jumps_inbetween_curlies(code):
    code = re.sub(',\s*\n\s*', ', ', code)
    code = re.sub(';\s*\n\s*', '; ', code)
    code = list(code)
    curly_count = 0
    for i in range(len(code)):
        if(code[i]=="{"):
            curly_count+=1
        elif(code[i]=="}"):
            curly_count-=1
        elif(code[i]=="\n" and curly_count!=0):
            code[i] = " "
    code = "".join(code)
    code = re.sub(r", *\n", ", ", code)
    return code

#def check_if_parameter_is_given_pipe(code, OG_start, OG_end):
#    char, end = get_next_element_caracter(code, OG_end-1)
#    start = OG_end
#    if(char in ['(', '{']):
#        curly_count, parenthese_count = int(char=="{"), int(char=="(")
#        quote_single, quote_double = False, False
#        end+=1
#        #Before it was this
#        #while(parenthese_count!=0 or curly_count!=0 or quote_single or quote_double or code[end]!='\n'):
#        while(parenthese_count!=0 or curly_count!=0 or quote_single or quote_double):
#            if(end>=len(code)):
#                raise Exception('Unable to extract')
#            if(code[end]=="{" and not quote_single and not quote_double):
#                curly_count+=1
#            if(code[end]=="}" and not quote_single and not quote_double):
#                curly_count-=1
#            if(code[end]=="(" and not quote_single and not quote_double):
#                parenthese_count+=1
#            if(code[end]==")" and not quote_single and not quote_double):
#                parenthese_count-=1
#            if(code[end]=="'" and not quote_single and not quote_double):
#                if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
#                    quote_single=True
#            elif(code[end]=="'" and quote_single and not quote_double):
#                if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
#                    quote_single=False
#            if(code[end]=='"' and not quote_single and not quote_double):
#                if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
#                    quote_double=True
#            elif(code[end]=='"' and not quote_single and quote_double):
#                if(code[end-1]!="\\" or (code[end-1]=="\\" and code[end-2]=="\\")):
#                    quote_double=False
#            end+=1
#        return code[start:end].strip()[1:-1].strip(), code[OG_start:end]
#    return ''

def expand_call_to_operation(code, call):
    start = code.find(call)
    end = start+len(call)
    char, _ = get_next_element_caracter(code, end-1)
    #This means it's an operation
    if(char=="."):
        return extract_end_operation(code, start, end)
    return call

def expand_pipe_operator(code, operator):
    start = code.find(operator)
    end = start+len(operator)
    expanding = True
    while(expanding):
        expanding = False
        char, _ = get_next_element_caracter(code, end-1)
        if(char in ['{', '|', '(']):
            operator = extract_end_operation(code, start, end)
            start = code.find(operator)
            end = start+len(operator)
            expanding = True
    return operator

#Function that checks if a bit of code given is in the condition of an if
def checks_in_condition_if(code, bit_of_code):
    start = code.find(bit_of_code)
    end = start+len(bit_of_code)
    start_if, end_if = 0, 0
    for match in re.finditer(r"if\s*\(", code[:start]):
        start_if, end_if = match.span(0)
    parenthese_count_left_before_if = get_parenthese_count(code[start_if:start])
    if(parenthese_count_left_before_if>0 and get_parenthese_count(code[:start_if])==0):
        code_end_if = get_code_until_parenthese_count(code[end:], -1*parenthese_count_left_before_if)
        if(code_end_if!=None):
            code_right_after_if = code[code.find(code_end_if)+len(code_end_if):]
            if(get_parenthese_count(code_right_after_if)==0):
                return True
    return False


#the function sort_and_filter takes two lists, positions and variables, and removes 
#entries with positions equal to (0, 0). It then sorts the remaining entries based 
#on positions and returns the sorted positions and corresponding variables.
def sort_and_filter(positions, variables):
    combined_data = list(zip(positions, variables))
    combined_data = [(pos, var) for pos, var in combined_data if pos != (0, 0)]
    combined_data.sort(key=lambda x: x[0])
    sorted_positions, sorted_variables = zip(*combined_data)
    return list(sorted_positions), list(sorted_variables)

#Function that checks if a bit of code given is in  a string
def checks_in_string(code, bit_of_code):
    start = code.find(bit_of_code)
    end = start+len(bit_of_code)

    
    #Start by single quote
    first_quote_from_left, first_quote_from_right = -1, -1
    for i in range(start-1, -1, -1):
        if(code[i]=="'"):
            first_quote_from_left = i
            break
    for i in range(end, len(code)):
        if(code[i]=="'"):
            first_quote_from_right = i
            break
    if(first_quote_from_left!=-1 and first_quote_from_right!=-1):
        if(get_single_count(code[:first_quote_from_left])==0 and get_single_count(code[first_quote_from_right+1:])==0):
            return True

    #Do the same for double quote
    first_quote_from_left, first_quote_from_right = -1, -1
    for i in range(start-1, -1, -1):
        if(code[i]=='"'):
            first_quote_from_left = i
            break
    if(first_quote_from_left==-1):
        return False
    for i in range(end, len(code)):
        if(code[i]=='"'):
            first_quote_from_right = i
            break
    if(first_quote_from_right==-1):
        return False
    if(first_quote_from_left!=-1 and first_quote_from_right!=-1):
        if(get_double_count(code[:first_quote_from_left])==0 and get_double_count(code[first_quote_from_right+1:])==0):
            return True
    
    return False


#This function extracts the rest of the inside of a parentheses given a 
#bit of code (we assume that the bit of code is inside the code)
def extract_inside_parentheses(code, bit_of_code):
    start = code.find(bit_of_code)
    end = start+len(bit_of_code)
    left = get_code_until_parenthese_count(code[:start], 1, left_2_right = False)
    right = get_code_until_parenthese_count(code[end:], -1, left_2_right = True)
    return (left[1:]+bit_of_code+right[:-1]).strip()

#This is used to get a dico from from the graph tab in a RO-Crate file
def get_dico_from_tab_from_id(dico, id):
    for temp_dico in dico["@graph"]:
        if(temp_dico["@id"]==id):
            return temp_dico
    return None

def check_if_element_in_tab_rocrate(tab, id):
    for ele in tab:
        if(ele["@id"]==id):
            return True
    return False