import click
import inquirer
import os
import subprocess
import yaml
from Sae203_Arnaud import aggreg
from Sae203_Arnaud import filetools
from pathlib import Path, PosixPath
import sys
from datetime import datetime
import pytz
# Récupération des variables globales
global chemin_general
chemin_general = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0,chemin_general)
global chemin_config
chemin_config = f"{chemin_general}/data/config.yml"


# Fonction qui permet de lire un fichier yaml rapidement
def yamlfiler(chem):
    with open(chem,"r",encoding="utf-8") as fd:
        return yaml.safe_load(fd)

# Fonction qui permet d'écrire rapidement un fichier yaml
def yamlfilew(data,chem):
    with open(chem,"w",encoding="utf-8") as fd:
        yaml.safe_dump(data,fd,allow_unicode=True)

# Les commandes principales
@click.group
def app():
    pass

# Les sous commandes de configuration
@app.group()
def config():
    """Permet de configurer les paramètres de l'agrégateur"""
    pass



@app.command()
def run():
    """Permet lancer le programme principal"""
    """La fonction lance le programme principale et affiche le chemin d'accès et la date
    """
    aggreg.main()
    click.echo(f"J'ai lancé le programme principale de {click.style('aggreg.py',fg='green')}")
    data = yamlfiler(chemin_config)
    destination = data["destination"]
    click.echo("Une nouvelle version du fichier html est disponible à "+click.style(destination,fg="magenta"))
    click.secho(datetime.now(pytz.timezone('Europe/Paris')).strftime('%a, %d %b %Y %H:%M'),fg="cyan")


    
@app.command()
@click.option("-e","--editor",default="",type=str)
def edit(editor):
    """Permet de modifier les fichiers du programme"""
    """Cette fonction propose à l'utilisateur de choisir un des 3 fichiers à modifier
    """
    # Si il n'y a pas d'éditeur on prend celui par céraut
    if not editor: 
        editor = filetools.default_editor()
    # On initialise les noms et correspondance des fichiers
    fich_nom={
        "Configuration":"config.yml",
        "Base HTML":"base.html",
        "Fichier CSS":"feed.css"
    }
    
    # Demande à l'utilisateur de choisir parmis la liste
    choix = inquirer.list_input("Quel fichier vous voulez modifier ?",choices=list(fich_nom.keys()))
    fichier = fich_nom[choix]
    
    chemin_fichier = f"{chemin_general}/data/{fichier}"    

    # Lance l'édition avec le programme choisi
    subprocess.run([editor, chemin_fichier])

# --------------- Les commandes de configuration -------------------
@config.command()
@click.argument("sources",type=str,nargs=-1)
def add_source(sources):
    """Permet d'ajouter une source ou des sources"""
    # Ouverture du fichier
    data = yamlfiler(chemin_config)
    # Pour chaque source que l'on veut ajouter on ajoute
    for source in sources:
        data["sources"].append(source)
    yamlfilew(data,chemin_config)
    click.secho("J'ai bien ajouté la ou les source(s) ! ",fg="green")

@config.command()
@click.option("-a","--all",is_flag=True,help="Supprimer tous les liens sources")
@click.argument("source",required=False)
def remove_source(source,all):
    """Permet de supprimer une ou toutes les sources"""
    
    # On crée une erreur si les entrées ne sont pas bones
    if not source and not all:
        raise click.UsageError("On ne peut pas rien enlever")
    data = yamlfiler(chemin_config)
    if all:
        # Si on veut supprimer toutes les sources
        data["sources"]=[]
        yamlfilew(data,chemin_config)
        click.secho("Toutes les sources ont été enlevées",fg="green")
    else:
        # On supprime qu'une seule source
        click.echo(f"J'enlève une source : {source}")
        if source in data["sources"]:
            # Si elle existe
            data["sources"].remove(source)
            click.secho("J'ai bien supprimé la source",fg="green")
            yamlfilew(data,chemin_config)
        else:
            # Si elle n'existe pas
            click.secho("La souce n'existe pas",fg="red")
            click.secho("Vous pouvez vérifier sa présence en faisant : config liste-sources")
            
@config.command()
def liste_sources():
    """Permet de lister les sources""" 
    data = yamlfiler(chemin_config)
    click.echo("\nVoici la liste des sources :\n")
    for lien in data["sources"]:
        click.echo("- ",nl=False)
        click.secho(lien,fg="blue")

@config.command()
@click.argument("destination")
def destination(destination):
    """Chemin du fichier html que va produire la commande run"""
    data = yamlfiler(chemin_config)
    data["destination"] = destination
    yamlfilew(data,chemin_config)
    click.secho(f"J'ai bien changé le fichier de destination en {destination}",fg="green")
    
    
@config.command()
@click.argument("rss_name")
def rss_name(rss_name,type=str):
    """Chemin du fichier html que va produire la commande run"""
    data = yamlfiler(chemin_config)
    data["rss-name"] = rss_name
    yamlfilew(data,chemin_config)
    click.secho(f"J'ai bien changé le fichier de nom du fichier rss en {rss_name}",fg="green")

    
@config.command()
@click.argument("boolean",type=bool)
def tri_chrono(boolean):
    """Trie-t-on en fonction du temps ?"""
    
    data=yamlfiler(chemin_config)
    data["tri-chrono"] = boolean
    yamlfilew(data,chemin_config)
    click.secho(f"Changement de tri-chrono en {boolean} réussi ! ",fg="green")


@app.command()
@click.option("-s","--schedule",required=False,type=str,help="""Insérer une planification,format de temps de crontab, \n vous pouvez vous référer au site : https://https://crontab.guru/
              \n\nExemple : -s "0 1 * * 1"
              \n\nPour relancer le programme principale tous les lundi à 1 h du matin
              """)
@click.option("-r","--remove",is_flag=True,required=False,help="Supprimer la planification")
def crontab(schedule,remove):
    """Permet de planifier le lancement du programme principal"""
    if not (schedule or remove ):
        raise click.exceptions.UsageError("Il faut préciser au moins un élément")

    if remove:
        # Si on veut enlever la crontab
        filetools.delete_crontab()
        click.secho("Crontab parfaitement supprimée !",fg="green")
    else:
        # Si on veut ajouter la crontab
        command = str(PosixPath(Path.home(),".local","bin"))+"/aggreg run"
        result =filetools.create_crontab(schedule,command)
        click.secho("Voici la nouvelle crontab\n",fg="green")
        click.secho(result,fg="magenta")




if __name__=="__main__":
    app()
    