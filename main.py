from bs4 import BeautifulSoup
import wget
import os

def dlloop (filename, filepath):
    with open(f'subscriptions/{filename}', 'rb') as f:
        data = f.read()


    Bs_data = BeautifulSoup(data, "xml")
    

    emissions = Bs_data.find_all('item')
    titre = Bs_data.find('title')
    titre = str(titre)
    titre = titre.replace('<title>', '')
    titre = titre.replace('</title>', '')

    subscripition = []

    dlindex = 0
    for item in emissions:
        date = (item.find('pubDate'))
        date = str(date)
        date = date.replace('<pubDate>', '')
        date = date.replace('</pubDate>', '')

        description = (item.find('description'))
        description = str(description)
        description = description.replace('<description>', '')
        description = description.replace('</description>', '')

        lien = item.find('enclosure')
        lien = lien.get('url')
        lien = str(lien)
        lien = lien.replace('<enclosure>', '')
        lien = lien.replace('</enclosure>', '')

        emission = {'name':titre,
        'description':description,
        'date':date,
        'link':lien,
        'dlindex':dlindex}

        subscripition.append(emission)
        dlindex+=1

    for i in range(len(subscripition)):
        idx = (len(subscripition)-i)-1
        print('=============================================')
        print('Titre:', subscripition[idx]['name'])
        print('')
        print('Description:', subscripition[idx]['description'])
        print('')
        print('Date:', subscripition[idx]['date'])
        print('')
        print('Index de téléchargement:', subscripition[idx]['dlindex'])
        print('')
        print('')

    userdl = None

    while userdl != 'exit':
        print('---------------------------------------------')
        userdl = input('Entrez l\'index de téléchargement de l\'émission que vous voulez télécharger (entrez "exit" pour quitter) : ')
        try:
            userdl=int(userdl)
            if userdl > len(subscripition):
                print('Veuillez entrer une valeur comprise dans le nombre total d\'émissions, c\'est à dire', len(subscripition)-1)
        
            else:
                fname = f'{subscripition[userdl]["name"]}{subscripition[userdl]["date"].replace(",", "").replace(":", "h")}.mp3'
                print(fname)
                wget.download(subscripition[userdl]['link'], f'{filepath}/{fname}')
        except ValueError:
            print('Veuillez entrer un nombre comme indice de téléchargement')
        
        print('')
        print('')

def get_sub(filename):
    wget.download(filename, f'subscriptions/temp.xml')
    with open('subscriptions/temp.xml', 'rb') as f:
        data = f.read()
    
    Bs_data = BeautifulSoup(data, "xml")

    titre = Bs_data.find('title')
    titre = str(titre)
    titre = titre.replace('<title>', '')
    titre = titre.replace('</title>', '')

    os.rename('subscriptions/temp.xml', f'subscriptions/{titre}.xml')

    return titre

def del_sub(filename):
    filename = filename+'.xml'
    if filename not in os.listdir('subscriptions'):
        print('L\'abonnement', filename.replace('.xml', ''), 'n\'existe pas !')
    else:
        os.remove(f'subscriptions/{filename}')
        print('')
        print('L\'abonnement', filename.replace('.xml', ''), 'à bien été supprimé')

def add_path(filepath):
    with open('dl_path.txt', 'w') as pf:
        pf.write(filepath)


action = None
while action!='exit':
    with open('dl_path.txt', 'r') as pf:
        path = pf.read()
    print("Liste des commandes disponibles : ")
    print('\t- "+abo" pour ajouter un abonnement')
    print('\t- "-abo" pour supprimer un abonnement')
    print('\t- "down" pour télécharger un épisode d\'un abonnement')
    print('\t- "=path" pour changer le chemin dans lequel seront téléchargés les podcasts')
    action = input('Que voulez-vous faire ? (entrez "exit" pour quitter) ')

    if action == '=path':
        user_path = input('Entrez le nouveau chemin d\'accès : (entrez "cancel" pour annuler et "downloads" pour retrouver le chemin d\'origine) ')
        if user_path != 'cancel':
            add_path(user_path)
            print('La demande à bien été annulée')
        print(f'Le chemin d\'accès à bien été changé pour {user_path}')

    if action == '+abo':
        rss_feed = input('Entrez le lien du flux RSS à ajouter : ')
        sub_t = get_sub(rss_feed)
        print('')
        print('Abonnement', sub_t, 'à bien été ajouté, il y a maintenant un total de', len(os.listdir('subscriptions')), 'abonnements.')

    elif action == '-abo':
        print('Abonnements actuels :')
        [print(f'\t- {i.replace(".xml", "")}') for i in os.listdir('subscriptions')]
        rss_del = input('Entrez le nom de l\'abonnement à supprimer : ')
        del_sub(rss_del)

    elif action == 'down':
        print('Abonnements actuels :')
        [print(f'\t- {i.replace(".xml", "")}') for i in os.listdir('subscriptions')]
        dl_abo = input('Entrez le nom de l\'abonnement dans lequel vous voulez télécharger un podcast : ')
        dlloop(dl_abo+'.xml', path)

    else:
        print('Cette demande n\'existe pas')