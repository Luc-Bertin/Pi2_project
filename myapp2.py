# coding: utf-8
""" copyright© 2019 — Luc Bertin - License MIT """

from tkinter import *
from tkinter.font import Font
from Twitter_Class_Analysis import Twitter_Analysis
from Linkedin_Companies_scrapping import LinkedIn_Analysis
from google_search import *
from Sentimental_Analysis import SentimentalAnalysis

ressources_folder = 'ressources/'
data_folder = 'data/'
analysisLkdIn = LinkedIn_Analysis()

# FRONT
def action_on_button1():
    value_returned, well_done = Twitter_Analysis.authentificator()
    display_message.config(text = str(value_returned))

def action_on_button2():
    global data_folder
    dico = data_folder+str(dico_entry.get())
    filename = data_folder+str(filename_entry.get())
    CSV_LinkedIn = data_folder+str(companiesLinkedInfile_entry.get())
    max_tweets = int(str(maxtweets_entry.get()))
    company_name = str(company_entry.get())
    
    print('Entreprise renseignee : ' + company_name)
    print('CSV renseigne : ' + CSV_LinkedIn )
    
    analysis = Twitter_Analysis(dico_file=dico,filename=filename,
                                maxTweets=max_tweets, company_name=company_name,
                                companies_CSV_file=CSV_LinkedIn)
    value_returned, well_done = analysis.search()
    display_message.config(fg="green") if well_done else display_message.config(fg="red")
    display_message.config(text = value_returned)

def action_on_button3():
    global data_folder
    dico = data_folder+str(dico_entry.get())
    filename = data_folder+str(filename_entry.get())
    CSV_LinkedIn = data_folder+str(companiesLinkedInfile_entry.get())

    max_tweets = int(str(maxtweets_entry.get()))
    analysis = Twitter_Analysis(dico_file=dico, filename=filename,
                                maxTweets=max_tweets, company_name=company_entry.get(),
                                companies_CSV_file=CSV_LinkedIn)
    value_returned, well_done = analysis.tweets_to_dataframe()
    display_message.config(fg="green") if well_done else display_message.config(fg="red")
    display_message.config(text = value_returned)

def action_on_button4():
    global analysisLkdIn
    global data_folder
    if analysisLkdIn.STOP_EXECUTION==0:
        keyword = str(LinkedInKeyword_entry.get())
        analysisLkdIn.output_filename = data_folder+"LinkedInCompanies"+str(filename_entry.get())
        analysisLkdIn.keyword = keyword
        analysisLkdIn.start()
        analysisLkdIn.STOP_EXECUTION=1
    elif analysisLkdIn.STOP_EXECUTION==1:
        analysisLkdIn.STOP_EXECUTION = 2
        print('finish1')
        analysisLkdIn.join()
        print('finish2')
        analysisLkdIn = LinkedIn_Analysis()
        display_message.config(text = "execution stopped !")

def action_on_button5():
    filename = data_folder + str(companiesLinkedInfile_entry.get())
    analysis = BigSearchGoogle(csv_file=filename)
    value_returned, well_done = analysis.run()
    display_message.config(fg="green") if well_done else display_message.config(fg="red")
    display_message.config(text = value_returned)

def action_on_button6():
    filename = data_folder+str(filename_entry.get())+'.csv'
    analysis=SentimentalAnalysis(csv_tweets=filename)
    value_returned, well_done = analysis.run()
    display_message.config(fg="green") if well_done else display_message.config(fg="red")
    display_message.config(text = value_returned)

###### DEFINITION OF GUI COMPONENTS ######
root = Tk()
root.title('PI2 Project — Twitter Analysis')
root.geometry('{}x{}'.format(350, 680))
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
root.resizable(False, False)
myFont = Font(family="Helvetica Neue", size=15)

## Font Image
imgTop = PhotoImage(file=ressources_folder+"imgtop.png")
image_top_label = Label(root, image=imgTop, borderwidth=0, highlightthickness=0)
blank_label = Label(root, height='1')
imgBottom = PhotoImage(file=ressources_folder+"imgbottom.png")
image_bottom_label = Label(root, image=imgBottom, borderwidth=0, highlightthickness=0)
space_label = Label(root, height='1')


dico_label = Label(root, text='Nom du fichier dico de valeurs :', font=myFont)
dico_entry = Entry(root, background="lavender")
companiesLinkedInfile_label = Label(root, text='Nom du CSV LinkedIn :', font=myFont)
companiesLinkedInfile_entry = Entry(root, background="lavender")
filename_label = Label(root, text='Nom du fichier de sortie :', font=myFont)
filename_entry = Entry(root, background="lavender")
maxtweets_label = Label(root, text='Nb Maximum de tweets :', font=myFont)
maxtweets_entry = Entry(root, background="lavender")
company_filter = Label(root, text='Une entreprise en particulier ?', font=myFont)
company_entry = Entry(root, background="lavender")
display_message = Label(root, text='', fg='red', font=("Helvetica Neue", 15))


authentification_button = Button(root, text='Authentifiate!', width=25, command=action_on_button1)
tweeterJson_button = Button(root, text='JSON', width=25, command=action_on_button2)
tweeterCSV_button = Button(root, text='CSV', width=25, command=action_on_button3)
sentimentalAnalysis_button = Button(root, text='Analyse Sentimentale', width=25, command=action_on_button6)

## LinkedIn and Google Button
LinkedInKeyword_label = Label(root, text='Pas de CSV d\'entreprise?\n Quel Keyword d\'entreprise :', font=myFont)
LinkedInKeyword_entry = Entry(root, background="bisque")
LindedIn_ico = PhotoImage(file=ressources_folder+"linkedin-3-32.gif")
LinkedIn_button = Button(root, image=LindedIn_ico, command=action_on_button4)

Google_ico = PhotoImage(file=ressources_folder+"google-plus-3-32.gif")
Google_button = Button(root, image=Google_ico, command=action_on_button5)


## Default values
dico_entry.insert(END, 'dico_file.txt')
companiesLinkedInfile_entry.insert(END, 'LinkedInCompanies.csv')
filename_entry.insert(END, 'tweets')
maxtweets_entry.insert(END, '200')
company_entry.insert(END, 'Nike')
LinkedInKeyword_entry.insert(END, 'environnement')


image_top_label.pack()
blank_label.pack()
dico_label.pack()
dico_entry.pack()
companiesLinkedInfile_label.pack()
companiesLinkedInfile_entry.pack()
filename_label.pack()
filename_entry.pack()
maxtweets_label.pack()
maxtweets_entry.pack()
company_filter.pack()
company_entry.pack()
authentification_button.pack()
tweeterJson_button.pack()
tweeterCSV_button.pack()

display_message.pack()
space_label.pack()
sentimentalAnalysis_button.pack()

LinkedInKeyword_label.pack()
LinkedInKeyword_entry.pack()
LinkedIn_button.pack()
Google_button.pack()
image_bottom_label.pack(side=BOTTOM)


root.mainloop()
