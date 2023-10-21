# generator_SeqReads - Version 1.0

Ce script Python génère une séquence ADN aléatoire et des reads à partir de cette séquence. Il est utile pour la génération de données de test ou d'exemple.

## Installation

Avant d'exécuter le script, assurez-vous que Python est installé sur votre système.

   ```shell
   git clone https://github.com/RAVAO-Ravo/generator_SeqReads_fun.git
   ```
Accédez au répertoire du projet :
   ```shell
   cd generator_SeqReads_fun
   ```

Installez les dépendances à partir du fichier `requirements.txt` :
   ```shell
   pip3 install -r requirements.txt
   ```

## Utilisation

Exécutez le script avec les options de ligne de commande pour personnaliser la génération. Voici un exemple d'utilisation :

   ```shell
   python3 generator_SeqReads.py -s 10000 -n 1000 -q 20 -G -R
   ```

   Options disponibles :
   - `-r`, `--random_state` : Graine aléatoire pour la reproductibilité.
   - `-s`, `--sequence_length` : Longueur de la séquence ADN.
   - `-n`, `--n_reads` : Nombre de reads à générer.
   - `-L`, `--min_length` : Longueur minimale des reads.
   - `-M`, `--max_length` : Longueur maximale des reads.
   - `-q`, `--mean` : Score de qualité moyen.
   - `-d`, `--std_dev` : Écart-type des scores de qualité.
   - `-H`, `--header` : En-tête pour le génome de référence.
   - `-G`, `--save_refGenome` : Enregistrer le génome de référence.
   - `-N`, `--no_save_refGenome` : Ne pas enregistrer le génome de référence.
   - `-R`, `--save_readsGenerated` : Enregistrer les reads générés.
   - `-P`, `--no_save_readsGenerated` : Ne pas enregistrer les reads générés.
   - `-f`, `--file_refGenome` : Nom de fichier pour le génome de référence.
   - `-F`, `--file_reads` : Nom de fichier pour les reads générés.
   - `-o`, `--output_format` : Format de sortie pour les reads générés (fastq ou fasta).

1. Le script générera une séquence ADN et des reads en fonction des options fournies.

2. Les fichiers générés seront enregistrés dans le répertoire de travail.

3. Vous pouvez examiner les fichiers générés ou les utiliser pour vos besoins.

## Licence

Ce projet est sous licence Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0). Vous êtes libre de :

- Partager : copier et redistribuer le matériel sous quelque support que ce soit ou sous n'importe quel format.
- Adapter : remixer, transformer et créer à partir du matériel.

Selon les conditions suivantes :

- Attribution : Vous devez donner le crédit approprié, fournir un lien vers la licence et indiquer si des modifications ont été apportées. Vous devez le faire de la manière suggérée par l'auteur, mais pas d'une manière qui suggère qu'il vous soutient ou soutient votre utilisation du matériel.

- Utilisation non commerciale : Vous ne pouvez pas utiliser le matériel à des fins commerciales.

[![Logo CC BY-NC 4.0](https://licensebuttons.net/l/by-nc/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc/4.0/)

[En savoir plus sur la licence CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)
