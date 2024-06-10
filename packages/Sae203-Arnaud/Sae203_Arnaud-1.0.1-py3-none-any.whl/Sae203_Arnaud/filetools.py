import os
import subprocess
from pathlib import Path,PosixPath

# Récupération du dossier du chemin du programme
global chemin_general
chemin_general = os.path.dirname(os.path.realpath(__file__))


def default_editor() -> str :
    """
    Cette fonction trouve ou initialise l'éditeur par défaut de l'utilisateur

    Returns:
        str: le chemin d'accès vers l'editeur
    """
    chem=PosixPath(Path.home(),".selected_editor")
    if not os.path.exists(chem):
        subprocess.run("select-editor")
    with open(chem,"r",encoding="utf-8") as fd:
        line = fd.readlines()[1].rstrip("\n")
    editor = line.split("=")[1][1:-1]
    return editor

def pos_curseur_in_liste(liste:list,mot:str) -> int:
    """Trouve la position du curseur après un certain mot dans une liste
    après un readlines( sans retour à la ligne)

    Args:
        liste (list): f.open().readlines() sans le retour à la ligne pour chaque élémént
        mot (str): le mot où on veux placer le curseur juste après

    Returns:
        int: la position où devrait être le curseur
        
    Warnings:
        la fonction s'arrête à la première occurence du mot (mot)
    """
    indice = liste.index(mot)+1
    pos_curseur = 0
    for ligne in liste[:indice]:
        pos_curseur = pos_curseur+len(ligne)+1
    return pos_curseur

def ecrire_entre_bornes(file_path:str,borne1:str,contenu:str,borne2:str,default_decorations:bool=True) -> str:
    """Cette fonction permet d'écrire un texte dans un fichier, qui ne sera pas répété si la fonction est appelé plusieurs fois,
    qui est propre et délimité par des bornes pour que l'on sache ce que c'est.
    
    Si il n'y a pas de bornes ça écrit le bornes et le contenu à la fin du fichier.
    Sinon ça met à jour le contenu qu'il y a entre les deux bornes

    Args:
        file_path (str): Chemin d'accès vers le fichier d'origine
        borne1 (str): La borne qui va être placée avant le contenu
        contenu (str): Le contenu qui va être entre les deux bornes
        borne2 (str): La borne qui va être placée après le contenu
        default_decorations (bool, optional): Ajoute des décoration par défaux aux bornes. Defaults to True.

    Returns:
        str: Le fichier de sortie
    """
    # Ajout des décoration si nécéssaires
    if default_decorations:
        borne1 = f"# >>> {borne1} >>>"
        borne2 = f"# <<< {borne2} <<<"
    with open(file_path,"r+",encoding="utf-8") as f:
        # On ouvre le fichier en lecture-écriture
        
        # Récupération des lignes du fichier original
        original = f.readlines()
        original = [ ele[:-1] for ele in original ]
        
        if borne1 in original and borne2 in original:
            # Si il ya les deux bornes dans le fichier
            
            # On récupère la suite du fichier pour le mettre à la suite de la modification
            pos_curseur = pos_curseur_in_liste(original,borne2)
            f.seek(pos_curseur)
            suite_fichier = f.read()
            f.truncate()
            
            # Pour mettre à jour le contenu, on se place ça la borne un, on supprime tout
            # Puis on écrit le contenu, la borne 2 et la suite du fichier
            pos_curseur = pos_curseur_in_liste(original,borne1)
            f.truncate(pos_curseur)
            f.seek(pos_curseur)
            f.write(contenu)
            f.write(f"\n{borne2}")
            f.write("\n")
            f.write(suite_fichier)
        else:
            # Si il n'y a pas les deux bornes dans le fichier
            
            # On lit le fichier
            f.seek(0)
            pos_fin = len(f.read())
            if pos_fin:
                # Si le fichier n'est pas vide
                # On écrit un retour à la ligne si il n'y en a pas déjà un
                f.seek(pos_fin-1)
                if not f.read(1) == "\n":
                    f.write("\n")
            # On écrit les 2 bornes et le contenu en fin du fichier
            f.write(f"{borne1}\n")
            f.write(contenu)
            f.write(f"\n{borne2}")
            f.write("\n")
        
        # On renvoie le fichier finale (même si on a déjà appliqué les modifications.)
        f.seek(0)
        fich_finale = f.read()
    return fich_finale
            

def ecrire_entre_bornes_revert(file_path:str,borne1:str,borne2:str,default_decorations:bool=True) -> str:
    """Cette fonction annule ce que à produit ecrire_entre_bornes.
    Elle a juste besoin des deux bornes pour les supprimer et supprimer ce qu'il y a entre.

    Args:
        file_path (str): Le chemin d'accès
        borne1 (str): La borne qui va être placée avant le contenu
        borne2 (str): La borne qui va être placée après le contenu
        default_decorations (bool, optional): Ajoute des décoration par défaux aux bornes.Defaults to True.

    Returns:
        str: Le fichier de sortie
    """
    if default_decorations:
        borne1 = f"# >>> {borne1} >>>"
        borne2 = f"# <<< {borne2} <<<"
    with open(file_path,"r+",encoding="utf-8") as f:
        original = f.readlines()
        original = [ ele[:-1] for ele in original ]
        if borne1 in original and borne2 in original:
            # On supprime si une modification a été faite par la fonction primaire
            # On garde la suite du fichier
            pos_curseur = pos_curseur_in_liste(original,borne2)
            f.seek(pos_curseur)
            suite_fichier = f.read()
            if suite_fichier and suite_fichier[0] == "\n":
                suite_fichier = suite_fichier[1:]
                
            # print("Je dois supprimern et remettre\n"+suite_fichier+"\n"*3)
            f.truncate()
            # print("Liste originale : ",original)
            # print("indexe =",original.index(borne1))
            # Puis on coupe avant la première bornet et on ajoute la suite du fichier 
            pos_curseur = pos_curseur_in_liste(original,original[original.index(borne1)])-len(borne1)-1
            # print("position du dernier élément",pos_curseur)
            f.seek(pos_curseur)
            f.truncate()
            # print("Je supprime définitivement\n",f.read()+"\n"*3)
            # print("je me situe à ",f.tell())
            f.write(suite_fichier)



def add_path():
    """La fonction ajoute le répertoire par défaut des scripts console dans le bashrc
    Comme ça l'utilisateur pour éxécuter directement le programme peu imoprt où il se trouve.
    """
    emp_bashrc = PosixPath(Path.home(),".bashrc")
    emp_localbin = PosixPath(Path.home(),".local","bin")
    depart = "Set Path for Local Bin"
    commande = f"export PATH=$PATH:{emp_localbin}"
    fin = "Set Path for Local Bin"
    ecrire_entre_bornes(emp_bashrc,depart,commande,fin)

def remove_path():
    """Cette fonction est la fonction inverser de add_path
    """
    emp_bashrc = PosixPath( Path.home(),".bashrc")
    depart = "Set Path for Local Bin"
    fin = "Set Path for Local Bin"
    ecrire_entre_bornes_revert(emp_bashrc,depart,fin)

def create_crontab(schedule:str, command:str) -> str:
    """Cette fonction permet d'ajouter une exécution préiodique d'une commande.

    Args:
        schedule (str): la période de déclenchement au format de crontab
        command (str): La commande qui est éxécutée périodiquement

    Returns:
        str: Renoive la nouvelle crontab
    """
    tmp_file="/tmp/1v4x4ad4g4qx.txt"
    
    # Récupérer le crontab actuel
    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    current_crontab = result.stdout
    with open(tmp_file,"w",encoding="utf-8") as fd:
        fd.write(current_crontab)


    # Définition de la ligne qui va être dans la crontab
    new_line = f"\n{schedule} {command}\n"


    # Préparation du fichier de crontab
    debut = "Set a crontab for refreshing rss scraping"
    fin = "Set a crontab for refreshing rss scraping"
    result = ecrire_entre_bornes(tmp_file,debut,new_line,fin)
    
    # Appliquer ce changement
    with open(tmp_file,"r",encoding = "utf-8") as fd:
        new_crontab=fd.read()
        # print(new_crontab)
        
    process = subprocess.run(['crontab', '-'], input=new_crontab, text=True)
    if process.returncode == 0:
        pass
    else:
        print("Erreur lors de la mise à jour du crontab.")
    os.remove(tmp_file)
    return result



def delete_crontab() -> bool:
    """Fonction inverse, permet de supprimer les bornes et le contenu juste de la crontab, 
    initialisée par la fonction au dessus."""
    tmp_file="/tmp/1v4x4ad4g4qx.txt"
    
    # Récupérer le crontab actuel
    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    current_crontab = result.stdout
    with open(tmp_file,"w",encoding="utf-8") as fd:
        fd.write(current_crontab)
    # Préparation de la crontab
    debut = "Set a crontab for refreshing rss scraping"
    fin = "Set a crontab for refreshing rss scraping"
    ecrire_entre_bornes_revert(tmp_file,debut,fin)
    
    # Appliquer ce changement
    with open(tmp_file,"r",encoding="utf-8") as fd:
        new_crontab=fd.read()
        
    os.remove(tmp_file)
    process = subprocess.run(['crontab', '-'], input=new_crontab, text=True)
    if process.returncode == 0:
        # "Crontab mis à jour avec succès."
        return True
    else:
        # Erreur lors de la supression de la crontab
        return False


def _test_func():
    """Fonction de test
    """
    import sys
    if eval(sys.argv[1]):
        ecrire_entre_bornes(
            "test.txt",
            "Set a crontab for refreshing rss scraping",
            "* * * * * aggreg run",
            "Set a crontab for refreshing rss scraping")
    else:
        ecrire_entre_bornes_revert("test.txt",
            "Set a crontab for refreshing rss scraping",
            "Set a crontab for refreshing rss scraping")
    pass
    
    

if __name__ == "__main__":
    _test_func()