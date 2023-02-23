'''The purpose of this script is to find any text on a webpage that contains the word TO_FIND.
It will search for all instances of the word and write to a file which class or tag,
iteration of class or tag, and iteration of the word in the class or tag where TO_FIND was found
Additionally it will log all occurences of http not https sites, and phone numbers found and emails.
Lastly it will describe all pages searched, and all pages it had an issue with.'''

#IMPORTS
from selenium import webdriver                  #BASIS FOR SELENIUM
from selenium.webdriver.common.by import By     #SEARCH WEBPAGE BY(CLASS,TAG,XPATH,etc...)

#DECLARE VARIABLES
TO_FIND = "Lorem"       #THE WORD TO SEARCH FOR, NOT CASE SENSITIVE
SITE_LINK = "https://choquercreative.com/"          #LINK TO LANDING PAGE OF SITE
URL_BLACKLIST = []      #PAGES TO AVOID
STOP_WHEN_FOUND = " "   #STOP WHEN THIS HYPERLINK IS FOUND, ENTER ANY KEY INTO TERMINAL TO CONTINUE. BY DEFAULT IT SHOULD BE " "
TEL_NUM = "7782374700"            #EXPECTED TELEPHONE NUMBER, NO DASHES OR BRACKETS. BY DEFAULT IT SHOULD BE " "
EMAIL_ID = "info@choquercreative.com"           #EXPECTED EMAIL. BY DEFAULT IT SHOULD BE " "
SEARCH_HASH_PAGES = False                        #True IF YOU WANT TO SEARCH PAGES THAT END IN "#", OR START IN "#", OTHERWISE MAKE False
                                                #IT WILL STILL LOG ALL URLS THAT CONTAIN ONLY "#"
tel_list = []
http_list = []
email_list = []
url_list = []
url_list_completed = [SITE_LINK]
url_issue_list = []

#DEFINE FUNCTIONS
def check_email(href_attribute):
    global EMAIL_ID
    global email_list
    if href_attribute[:6] == "mailto":
        if href_attribute[7:] != EMAIL_ID:
            email_list.append(href_attribute)                   #IF IT IS AN EMAIL AND NOT EXPECTED ADD IT TO A LIST
            return True
    return False

def check_http_link(href_attribute):
    global http_list
    if href_attribute[4] != 's':
        if href_attribute[:4] == "http":
            http_list.append(href_attribute)                    #IF THE SITE IS HTTP, NOT HTTPS ADD IT TO A LIST
            return True
    return False

def check_tel_num(href_attribute):
    global TEL_NUM
    global tel_list

    if(href_attribute[:3] == "tel"):
                #IF IT IS A TELEPHONE NUMBER
        if(href_attribute[4:] != TEL_NUM):
                #IF IT DOES NOT MATCH EXACTLY WITH TEL_NUM
            return True
        elif(href_attribute[4:] != '+1' + TEL_NUM):
                #IF IT DOES NOT MATCH WITH LONG DISTANCE STYLE OF TEL_NUM
            return True
        elif(href_attribute[4:] != TEL_NUM[:3] + '-' + TEL_NUM[3:6] + '-' + TEL_NUM[6:]):
                #IF IT DOES NOT MATCH WITH '-' BETWEEN NUMBER SETS STYLE OF TEL_NUM
            return True
        elif(href_attribute[4:] != '+1' + TEL_NUM[:3] + '-' + TEL_NUM[3:6] + '-' + TEL_NUM[6:]):
                #IF IT DOES NOT MATCH WITH '= BETWEEN NUMBER SETS AND LONG DISTANCE STYLE OF TEL_NUM
            return True
        else:   #IT IS AN UNEXPECTED TELEPHONE NUMBER SO ADD IT TO A LIST
            tel_list.append(href_attribute)
        return True
                #IF IT IS NOT A TELEPHONE NUMBER
    return False

def stop_when_found(href_atribute):
    if(href_atribute == STOP_WHEN_FOUND):                       #STOPS AND WAITS FOR INPUT WHEN STOP_WHEN_FOUND IS FOUND
        print()
        print("FOUND " + STOP_WHEN_FOUND + " ON PAGE"  + browserChrome.current_url)
        print()
        output_file.write("\nFOUND " + STOP_WHEN_FOUND + " ON PAGE " + browserChrome.current_url + "\n")
        input("PRESS ANY KEY TO CONTINUE") 

def update_url_list(new_url_list):
    '''This function takes the list of urls found on the current page new_url_list,
    adds the existing url_list to creates a temp_url_list. This temp_url_list has duplicates removed,
    then removes all urls from temp_url_list that exist in url_list_completed, and all blacklisted urls. '''
    global url_list
    global url_list_completed
    temp_url_list = url_list + new_url_list
    temp_url_list = list(dict.fromkeys(temp_url_list))                             #REMOVE DUPLICATES
                
    for blacklisted_url in URL_BLACKLIST:
        for temp_url in temp_url_list[1:]:
            if blacklisted_url == temp_url[:len(blacklisted_url)]:                 #REMOVES BLACKLISTED URLS FROM THE UPDATED LIST
                temp_url_list.remove(temp_url)
                print("Removed blacklisted link: " + temp_url)

    for each_url in url_list[1:]:
        if each_url in url_list_completed:
            temp_url_list.remove(each_url)                                         #REMOVE ALL COMPLETED URLS FROM THE UPDATED LIST
            break                                    

    return temp_url_list

def find_hyperlinks():
    '''This function is intended to scan the current page for all links, ensure they are from
    this domain, then returns a list of all the hyperlinks.
    It is also responsible for finding http sites, and telephone numbers, then storing them in a list.'''
    #VARIABLES
    global url_list_completed
    global url_issue_list
    global SEARCH_HASH_PAGES
    global SITE_LINK
    global STOP_WHEN_FOUND

    hyperlink_list = ["Hyperlink list"]
    output_file = open("log.txt", "a", encoding="UTF-8")
    counter = 0

    for hyperlink in browserChrome.find_elements(By.TAG_NAME, "a"):                #FINDS ALL ANCHOR TAGS
        counter += 1
        try:
            hyperlink.get_attribute("href")                     #GETS THE HREF ATTRIBUTE, IF THERE IS NONE, DESCRIBES IT
        except:                                                 #ERROR HANDLER FOR ANCHOR TAG WITH NO HREF ATTRIBUTE
            print("FOUND ANCHOR TAG AT ITERATION " + str(counter) + " WITH NO HREF ATTRIBUTE ON PAGE " + browserChrome.current_url)
            output_file.write("\nFOUND ANCHOR TAG AT ITERATION " + str(counter) + " WITH NO HREF ATTRIBUTE ON PAGE " + browserChrome.current_url + "\n\n")
        else:  
            if(check_http_link(hyperlink.get_attribute("href"))):                  #IF hyperlink's href ATTRIBUTE IS a HTTP LINK SKIP THE REST FOR THIS ITERATION
                continue

            if(check_tel_num(hyperlink.get_attribute("href"))):                    #IF hyperlink's href ATTRIBUTE IS A TELEPHONE NUMBER SKIP THE REST FOR THIS ITERATION
                continue

            if(check_email(hyperlink.get_attribute("href"))):                      #IF hyperlink's href ATTRIBUTE IS AN EMAIL SKIP THE REST FOR THIS ITERATION
                continue

            stop_when_found(hyperlink.get_attribute("href"))                       #IF THE LINK STOP_WHEN_HERE IS FOUND WRITE WHERE IT WAS FOUND TO A FILE AND TERMINAL AND WAIT FOR INPUT
                
            if(hyperlink.get_attribute("href") == "#"):                     #IF THE HREF IS EXACTLY "#" WHICH REDIRECTS TO THE CURRENT PAGE
                url_issue_list.append("'#' href ATTRIBUTE FOUND AT ANCHOR TAG ITERATION " + str(counter) + " ON PAGE " + browserChrome.current_url + " \n THIS MEANS THE LINK REDIRECTS TO THIS SAME PAGE")
                url_issue_list = list(dict.fromkeys(url_issue_list))               #REMOVES DUPLICATES FROM LIST
                continue
            elif(hyperlink.get_attribute("href") == browserChrome.current_url + "#"):    #IF HREF IS THE CURRENT PAGE + "#"
                url_issue_list.append("FOUND href REFERENCE TO #" + hyperlink.get_attribute("href") + " AT ANCHOR TAG ITERATION " + str(counter) + " ON PAGE " + browserChrome.current_url)
                if(SEARCH_HASH_PAGES):
                    if(hyperlink.get_attribute("href") not in hyperlink_list):
                        hyperlink_list.append(hyperlink.get_attribute("href"))     #ADDS THE HREF FROM THAT ANCHOR TAG TO A LIST
                continue
            elif(hyperlink.get_attribute("href")[0] == "#"):                       #IF HREF IS # THEN SOME CHARACTERS, WHICH MEANS SCROLL TO A SECTION
                if(SEARCH_HASH_PAGES):
                    if(hyperlink.get_attribute("href") not in hyperlink_list):
                        hyperlink_list.append(hyperlink.get_attribute("href"))
                continue

            if(hyperlink.get_attribute("href")[:len(browserChrome.current_url) + 1] == SITE_LINK):          #IF THE DOMAIN IS THE SAME ON THE HYPERLINK
                if(hyperlink.get_attribute("href") not in url_list_completed):
                    hyperlink_list.append(hyperlink.get_attribute("href"))          #ADDS THE HREF FROM THAT ANCHOR TAG TO A LIST
                    continue
            else:                                               #IF THE DOMAIN NAME IS DIFFERENT DO NOT ADD IT TO THE LIST, WRITE TO CONSOLE INSTEAD    
                print("Removed link from other domain: " + hyperlink.get_attribute('href'))                
                continue

            if(hyperlink.get_attribute("href")[0] == "/"):
                hyperlink_list.append(SITE_LINK + hyperlink.get_attribute("href"))  #IF IT IS A RELATIVE LINK, APPEND THE RELATIVE LINK TO THE END OF THE HOMEPAGE, THEN ADD IT TO THE LIST)
    
    output_file.close()
    return hyperlink_list
         
def find_elements(list_text):
    '''This Function takes a short string that must start with (Tag ) or (Class ),
    followed by the exact name of that class or tag. It will create a list with the string as a descriptor,
    search this page for the elements of that type, amd add their text to a list.'''
    element_list = [list_text]

    if(list_text[:3] == "Tag"):
        for element in browserChrome.find_elements(By.TAG_NAME, list_text[4:]):     #FINDS ALL TAGS WITH THE GIVEN NAME
            try:
                element_list.append(element.text)                                   #ADDS THEIR TEXT ATTRIBUTE TO A LIST
            except:
                print()                                                             #IF THERE IS NO TEXT, PRINT AN ERROR
                print("CANNOT FINDING CONTENT OF " + list_text + " ITERATION " + str(len(element_list - 1)) + " ON PAGE: " + browserChrome.current_url)
                print()                                                             #NOT IMPORTANT ENOUGH TO ADD TO LOG
    
    elif(list_text[:5] == "Class"):
        for element in browserChrome.find_elements(By.CLASS_NAME, list_text[6:]):   #FINDS ALL CLASSES WITH THE GIVEN NAME
            try:
                element_list.append(element.text)                                   #ADDS THEIR TEXT ATTRIBUTE TO A LIST
            except:
                print()                                                             #IF THERE IS NO TEXT, PRINT AN ERROR
                print("CANNOT FINDING CONTENT OF " + list_text + " ITERATION " + str(len(element_list - 1)) + " ON PAGE: " + browserChrome.current_url)
                print()                                                             #NOT IMPORTANT ENOUGH TO ADD TO LOG
    
    element_list.append(False)
    return element_list

def search_block(text_block_list):
    '''This function will search copy the location identifier (text_block_list[0]) to the return_list,
    then search the text_block_list contents after the location identifier for the TO_FIND word.
    If a match is found the word, and it's tag/class iteration, and word iteration
    will be saved to an output file.'''
    count = [0,1]
    word_list = []
    return_list = [text_block_list[0]]                          #ADDS DESCRIPTION TO return_list FROM THE DESCRIPTION EACH text_block IN text_block_list

    for text_block in text_block_list[1:]:
        count[1] = 1                                            #COUNTS TEXT BLOCK ITERATION, THEN WORD ITERATION PER TEXT BLOCK
        if(text_block is not False):                            #IF THE TEXT BLOCK IS NOT THE LAST ONE (INDICATED BY FALSE)
            word_list = text_block.split()
            count[0] += 1
            for each_word in word_list:                                             #WORD COUNTER
                if(each_word.lower() == TO_FIND.lower()):                           #IF THE WORD IS FOUND, ADD IT TO A LIST  
                    return_list.append("Found " + each_word + " at iteration : " + str(count[0])     #MULTI-LINE
                    + " of " + text_block_list[0] + ". Word number " + str(count[1]))                #MULTI-LINE
                count[1] += 1
        else:
            return_list.append("Finished searching " + text_block_list[0] + "\n")   #INDICATES THE TEXT BLOCK IS DONE BEING SEARCHED
    return return_list

def search_page(is_print=True):                                 #is_print DEFAULTS TO True, False IS USED TO INSTANTIATE THE url_list
    '''This function is intended to run all the find all text elements on a specific page.
    It is also used to call the find_hyperlinks function which builds and sorts a list of hyperlinks.
    Thirdly, this function writes content to the file.'''
    search_page_list = []
    output_file = open("log.txt", "a", encoding="UTF-8")                            #OPENS THE LOG FILE FOR USE IN APPEND MODE
    global http_list
    global tel_list
    global email_list
    
    temp_url_list = find_hyperlinks()                                               #FINDS ALL HYPERLINKS ON A PAGE
    temp_url_list = list(dict.fromkeys(temp_url_list))                              #REMOVE DUPLICATES FROM LIST
    
    if is_print:
        output_file.write("Starting Page: " + browserChrome.current_url + "\n")     #WRITES PAGE URL IN THE FILE FOR EASE

        search_page_list.append(search_block(find_elements("Tag body")))
        search_page_list.append(search_block(find_elements("Tag p")))
        search_page_list.append(search_block(find_elements("Tag h1")))
        search_page_list.append(search_block(find_elements("Tag h2")))
        search_page_list.append(search_block(find_elements("Tag h3")))
        search_page_list.append(search_block(find_elements("Tag h4")))
        search_page_list.append(search_block(find_elements("Tag h5")))
        search_page_list.append(search_block(find_elements("Tag h6")))

        search_page_list.append(search_block(find_elements("Class text-size-tiny")))
        search_page_list.append(search_block(find_elements("Class text-size-small")))
        search_page_list.append(search_block(find_elements("Class text-size-regular")))
        search_page_list.append(search_block(find_elements("Class text-size-medium")))
        search_page_list.append(search_block(find_elements("Class text-size-large")))
        search_page_list.append(search_block(find_elements("Class nav-link-text")))

        search_page_list.append(search_block(find_elements("Class heading-style-h1")))
        search_page_list.append(search_block(find_elements("Class heading-style-h2")))
        search_page_list.append(search_block(find_elements("Class heading-style-h3")))
        search_page_list.append(search_block(find_elements("Class heading-style-h4")))
        search_page_list.append(search_block(find_elements("Class heading-style-h5")))
        search_page_list.append(search_block(find_elements("Class heading-style-h6")))

        for each_search in search_page_list:
            if(each_search[1][:8] != "Finished"):           #IF THE 2ND ITEM IN each_list IS "Finished" DO NOT WRITE THE LOCATION, THIS MEANS THE LIST IS EMPTY
                output_file.write(str(each_search) + "\n")                          #WRITES THE LOCATION THE WORD WAS FOUND TO A FILE
        
        try:
            print(http_list[0])
        except:
            print("Nothing in http List.")                                          #IF http_list IS EMPTY DO NOT WRITE
        else:
            http_list = list(dict.fromkeys(http_list))                              #REMOVE DUPLICATES
            output_file.write("Http Links: " + str(http_list) + "\n")               #WRITES HTTP LINKS
        
        try:
            print(tel_list[0]) 
        except:
            print("Nothing in Telephone List.")                                     #IF tel_list IS EMPTY DO NOT WRITE
        else:
            tel_list = list(dict.fromkeys(tel_list))                                #REMOVE DUPLICATES
            output_file.write("Telephone numbers: " + str(tel_list) + "\n")         #WRITES TELEPHONE NUMBERS
        
        try:
            print(email_list[0]) 
        except:
            print("Nothing in Email List.")                                         #IF email_list IS EMPTY DO NOT WRITE
        else:
            email_list = list(dict.fromkeys(email_list))                            #REMOVE DUPLICATES
            output_file.write("Emails: " + str(email_list) + "\n")                  #WRITES TELEPHONE NUMBERS

        output_file.write("Finished Page: " + browserChrome.current_url + "\n\n")   #INDICATES END OF PAGE
    #END OF is_print
    
    http_list.clear()     #CLEARS LISTS OF DATA FROM CURRENT PAGE BEFORE MOVING TO NEXT PAGE
    tel_list.clear()
    email_list.clear()

    return temp_url_list

def navigate():
    '''This function is intended to search through the list of hyperlinks,
    find a link that has not been completed, verify that link is on the correct domain,
    add that link to the list of completed links, navigate to the bew page,
    then return the list of completed sites.'''
    global url_list
    global url_list_completed
    global url_issue_list

    for each_url in url_list[1:]:
        url_list_completed.append(browserChrome.current_url)                        #ADDS THIS PAGE TO THE url_list_completed
        url_list_completed = list(dict.fromkeys(url_list_completed))                #REMOVE DUPLICATES
        if each_url in url_list_completed:              #SEARCHES THE url_list FOR A URL THAT IS NOT ANYWHERE IN url_list_completed
            try:
                url_list.remove(each_url)                                           #REMOVES A FOUND LINK FROM url_list
            except:
                None
        else:
            url_list = update_url_list(search_page())                               #UPDATE THE url_list BEFORE GOING TO A NEW PAGE
            browserChrome.get(each_url)                                             #WHEN FOUND GO TO THAT PAGE
            if(browserChrome.current_url != each_url):                              #IF THE PAGE THAT WAS NAVIGATED TO IS NOT THE CORRECT PAGE, ADD IT TO THE ISSUE LIST AND COMPLETED LIST
                url_issue_list.append("Redirected to " + browserChrome.current_url + " instead of " + each_url)
                url_list_completed.append(each_url)

    url_list = update_url_list(url_list)

    if(len(url_list) != 1):                                                         #IF THE LIST HAS MORE THAN THE HOME PAGE
        url_list = update_url_list(navigate())                                      #RESTARTS WITH THE UPDATED url_list
    
    return update_url_list(url_list)                                                #LEAVES WITH THE UPDATED url_list 


#MAIN
browserChrome = webdriver.Chrome()                                                  #OPENS CHROME
browserChrome.get(SITE_LINK)                                                        #NAVIGATE TO SITE_LINK

url_list = update_url_list(search_page(is_print=False))                             #INSTANTIATE url_list WITH is_print=FALSE
url_list = navigate()     #ADDS THIS PAGE TO THE url_list_completed, SEARCHES THE PAGE, UPDATES url_list, THEN INTERNALLY NAVIGATES TO NEW PAGE


output_file = open("log.txt", "a", encoding="UTF-8")

output_file.write("\nISSUE LINKS:\n")
for url in url_list[1:]:
    output_file.write(url + "\n")                                                   #WRITES UNCLEARED url_list ITEMS
try:
    issue_url = url_issue_list[0]
    for issue_url in url_issue_list:
        output_file.write(issue_url + "\n")                                         #WRITES ISSUE URLS TO LOG
except:
    None

output_file.write("\nFOUND " + str(len(url_list_completed)) + " PAGES:\n")
for each_url_completed in url_list_completed:
    if(each_url_completed not in url_issue_list):
        output_file.write(each_url_completed + "\n")                                #WRITES ALL PAGES SEARCHED

output_file.write("END OF LOG")
output_file.close()
browserChrome.close()