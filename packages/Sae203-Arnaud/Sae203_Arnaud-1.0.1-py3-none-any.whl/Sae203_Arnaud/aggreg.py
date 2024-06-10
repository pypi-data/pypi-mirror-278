#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 10:31:54 2024

@author: g23015097
"""

# --importation des motules--
# import json
import requests
import feedparser
from bs4 import BeautifulSoup as BS
import yaml

import os
import shutil
import pytz
from datetime import datetime

# Récupération du dossier du chemin du programme
global chemin_general
chemin_general = os.path.dirname(os.path.realpath(__file__))


def charge_urls(liste_url:list[str])-> list[str]:
    """Cette fonction permet de charger des flux rss avec des liens http

    Args:
        liste_url (list): liste d'url vers le fichier 
        
    Warnings:
        La fonction ne prend pas en compte si le fichier rss n'est pas bien formaté

    Returns:
        list[str]: La liste des fichiers rss récupérés
    """
    docs_rss = []
    for url in liste_url:
        # Pour chaque url on ajoute le document dans la liste
        try :
            requests.get(url)
            mon_feed = feedparser.parse(url)
            docs_rss.append(mon_feed)
        except:
            # Sauf si l'url n'est pas valide donc on ajoute None
            docs_rss.append(None)
        
    return docs_rss

def fusion_flux(liste_url:list[str], liste_flux:list[str], tri_chrono : bool) -> list[dict]:
    """Récupération des informations nécéssaires du flux, et organisation des information.
    On trie aussi en fonction
    - soit du temps
    - soit de la gravité de l'erreur

    Args:
        liste_url (list[str]): La liste des url de bases
        liste_flux (list[str]): Les fichiers rss chargés à partir de ces urls
        tri_chrono (bool): tri en fonction du temps si vrai. Sinon de la gravité

    Returns:
        list[dict]: Chaque élément est événement.
    """
    liste_finale=[]
    erreurs=[]
    for ind,flux in enumerate(liste_flux):
        if flux != None :
            # Si le flux a pu être récupéré :
            feed = flux
            # print(json.dumps(feed_dico,indent=3))
            # On ajoute les bons éléments dans le dictionnaire
            for entry in feed.entries:
                dico={}
                dico["titre"]=entry.title
                dico["categorie"] = entry.tags[0].term
                dico["serveur"] = feed.feed.links[0].href.split("/")[2]
                dico["date_publi"] = entry.published
                dico["lien"] = entry.links[0].href
                dico["description"] = entry.summary
                dico["guid"] = entry.links[0].href.split("/")[3].rstrip(".html")
                liste_finale.append(dico)
        else:
            # Sinon on considère que c'est une erreur et on précisé quel lien à donné l'erreur
            erreurs.append(liste_url[ind])
        # print(json.dumps(feed,indent=2))

    if not tri_chrono:
        # Triage en fonction de la gravité
        liste_finale.sort(key=lambda e : ["CRITICAL","MAJOR","MINOR",None].index(e["categorie"]))
    else :
        # Triage en fonction de la date au format RFC 822
        liste_finale.sort(key=lambda e: datetime.strptime(e["date_publi"], '%a, %d %b %Y %H:%M'),reverse=True)

    # On ajoute toutes les erreurs à la fin du dossiers
    liste_finale.append(erreurs)
    return liste_finale

def genere_html(liste_evenements:list[str],chemin_html:str):
    """Cette fonction génère une page html en fonction d'une liste d'événement.
    La liste d'événement doit être ce que a produit la fonction fusion_flux 
    
    Warnings :
        Pour que le fichier d'enregistre bien, l'utilisateur qui lance le programme python
        ait les droits d'écriture et d'éxécution sur le dossier

    Args:
        liste_evenements (list[str]): Ce que fusion_flux a produit
        chemin_html (str): chemin de l'endroit où le fichier

    Returns:
        format de beautifulsoup: le fichier html final sous format de beautifulsoup
    """
    
    # Ouverture du fichier de base et récupération
    with open(chemin_general + "/data/base.html","r",encoding="utf-8") as df:
        soup = BS(df,"html.parser")
    
    # On trouve le parent où on va mettre tous les articles
    art_principale = soup.find("article")
    
    # On inscrit la date actuelle
    date_actu = datetime.now(pytz.timezone('Europe/Paris')).strftime('%a, %d %b %Y %H:%M')
    date_actu_balise = art_principale.find("p")
    date_actu_balise.string = date_actu
    
    
    
    for evenement in liste_evenements:
        if type(evenement) is dict:
            # Si l'événement est un événement
            
            # On récupère son type et on lui ajoute une classe css
            cat_event = evenement["categorie"]
            if cat_event == "CRITICAL":
                css_class = "events_criticals_rod"
            elif cat_event == "MAJOR":
                css_class = "events_majors_rod"
            elif cat_event == "MINOR":
                css_class = "events_minors_rod"
            clss_class2 = css_class.rstrip("rod") + "category"
            barre = soup.new_tag("hr",attrs={"class":css_class})
            
            
            
            # On ajoute chaque élément dont on a besoin
            nouv_art = soup.new_tag("article",attrs={"class":"items"})
            art_principale.append(nouv_art)
            
            nouv_art.append(barre)
            
            
            header = soup.new_tag("header",attrs={"class":"events_headers"})
            nouv_art.append(header)
            
            titre = soup.new_tag("h1",attrs={"class":"events_title"})
            titre.string=evenement["titre"]
            header.append(titre)
            
            provenance = soup.new_tag("p",attrs={"class":"events_from"})
            provenance.string="from : " + evenement["serveur"]
            nouv_art.append(provenance)
            
            date = soup.new_tag("p",attrs={"class":"events_date"})
            date.string=evenement["date_publi"]
            nouv_art.append(date)
            
            
            category = soup.new_tag("p",attrs={"class":f"events_category {clss_class2}"})
            category.string=cat_event
            nouv_art.append(category)
            
            
            guid = soup.new_tag("p",attrs={"class":"events_guid"})
            guid.string=evenement["guid"]
            nouv_art.append(guid)
            
            papa_du_lien = soup.new_tag("p",attrs={"class":"events_p_link"})
            content = evenement["lien"]
            nouv_art.append(papa_du_lien)
            lien = soup.new_tag("a",attrs={"href":content,"class":"events_link"})
            lien.string = content
            papa_du_lien.append(lien)
            
            
            
            description = soup.new_tag("p",attrs={"class":"events_summary"})
            description.string=evenement["description"]
            nouv_art.append(description)
            
            barre = soup.new_tag("hr",attrs={"class":css_class})
            nouv_art.append(barre)
        else:
            # Si ce n'est pas un dictionnaire, c'est alors une erreur
            # On se retrouve dans ce cas si le lien n'a pas pu être chargé
            liens_srv_erreur=evenement
            for lien_srv_erreur in liens_srv_erreur:
                # Pour chaque erreur on affiche le lien qui a causé problème
                nouv_art = soup.new_tag("article",attrs={"class":"items"})
                art_principale.append(nouv_art)
                        
                header = soup.new_tag("header",attrs={"class":"events_headers"})
                nouv_art.append(header)
                
                            
                titre = soup.new_tag("h1",attrs={"class":"events_title"})
                titre.string="Erreur lors du chargement du serveur avec le lien suivant"
                header.append(titre)
                
                papa_du_lien = soup.new_tag("p",attrs={"class":"events_p_link"})
                
                nouv_art.append(papa_du_lien)
                lien = soup.new_tag("a",attrs={"href":lien_srv_erreur,"class":"events_link"})
                lien.string = lien_srv_erreur
                # print(lien_srv_erreur)
                papa_du_lien.append(lien)
            
    # On écrit le fichier à l'endroit de destination
    with open(chemin_html,"w",encoding="utf-8") as df:
        df.write(soup.prettify())
    return soup.prettify()
 
def main_test():
    """Fonction de test"""
    a = fusion_flux("http://none.url",feedparser.parse("rss30.xml"),True)
    genere_html(a,"sortie.html")

    

    """ res = charge_urls([
        "https://radiofrance.fr/franceinter/rss",
        "https://www.01net.com/info/flux-rss/actualites/feed/",
        "fake.url"])
    print(res[1])"""
   

def main_base():
    """Programme principale.
    Ce programme va faire plusieurs chose:
    - Récupérer les flux rss définis dans le fichier config
    - Récupérer les autres informations dans le fichier config
    - Crée un fichier html à la destination du fichier 
    """
    with open (chemin_general + "/data/config.yml","r",encoding="utf-8") as df :
        # Récupération des information du fichier yaml
        doc = yaml.safe_load(df)
    sources = doc["sources"]
    rss_name= doc["rss-name"]
    destination = doc["destination"]
    tri_chrono = doc["tri-chrono"]
    
    
    # On construit les lienx finaux
    urls = [element + "/" + rss_name for element in sources]
    # Chargement des fichiers rss
    fichiers_rss = charge_urls(urls)
    # Mise en forme des fichiers rss
    infos_flux = fusion_flux(urls,fichiers_rss,tri_chrono)
    # supression de l'ancien fichier html (pour être sur)
    try :os.remove(destination)
    except : pass
    # Génération de la page finale
    genere_html(infos_flux,destination)
    # Trouver le chemin pour mettre le fichiers css dans le même répertoire
    destination_css ="/".join(destination.split("/")[:-1])+"/feed.css"
    # Remplacement du fichier css avec celui actuel
    shutil.copyfile(chemin_general + "/data/feed.css",destination_css)



def main():
    main_base()
    
if __name__=="__main__":
    main()