#!/bin/python3
#-*- coding:utf-8 -*-

# Auteur : RAVAOZAFINDRASOA Ravo
# Version : 1.0

# Importations
import random as rd
import numpy as np
import argparse
from typing import List, Union, Tuple


# Variable globale
ALPHABET: List[str] = ['a', 't', 'c', 'g']


def generate_RdmSeq(sequence_length: int, random_state: int = None) -> str:
	"""
	Génère une séquence aléatoire en choisissant des nucléotides.

	Args:
		sequence_length (int): La longueur de la séquence à générer.
		random_state (int, optional): La graine (seed) pour la génération aléatoire. Si elle n'est pas spécifiée, la génération sera non déterministe.

	Returns:
		str: La séquence aléatoire générée.
	"""
	# Liste des nucléotides à choisir
	global ALPHABET

	# Si une graine aléatoire est spécifiée, utilisez-la pour la reproductibilité
	if random_state is not None:
		rd.seed(random_state)

	# Générez la séquence en choisissant des nucléotides
	return ''.join(rd.choice(ALPHABET) for _ in range(sequence_length))


def random_Q(mean: float, std_dev: float) -> int:
	"""
	Génère un score de qualité (Q-score) en fonction de la moyenne et de l'écart-type.

	Args:
		mean (float): La moyenne de la distribution.
		std_dev (float): L'écart-type de la distribution.

	Returns:
		int: Le score de qualité généré.
	"""
	# Génération d'un nombre aléatoire à partir d'une distribution normale
	q_score = int(np.random.normal(mean, std_dev))

	# S'assurer que le score de qualité est dans la plage acceptable (entre 0 et 40)
	return max(0, min(q_score, 40))


def Q_to_proba(Q: int) -> float:
	"""
	Convertit un score de qualité (Q) en probabilité d'erreur (P).

	Args:
		Q (int): Le score de qualité.

	Returns:
		float: La probabilité d'erreur correspondante.
	"""
	# Utilisation de la formule de conversion Q en P
	return 10 ** (-Q / 10)


def mutate_base(base: str, error_probability: float) -> str:
	"""
	Transforme une base en l'une des trois autres bases avec une probabilité d'erreur donnée.

	Args:
		base (str): La base nucléotidique d'origine (a, t, c ou g).
		error_probability (float): La probabilité d'erreur, par exemple 0.01 pour 1% d'erreur.

	Returns:
		str: La base transformée.
	"""
	# Choix d'une nouvelle base avec une probabilité d'erreur
	if rd.random() < error_probability:
		# Remplace la base d'origine par l'une des trois autres bases
		mutated_base = rd.choice("atcg".replace(base, ""))
	else:
		# Si aucune mutation, la base reste la même
		mutated_base = base

	return mutated_base


def Q_to_ascii(Q: int) -> str:
	"""
	Convertit un score de qualité en caractère ASCII.

	Args:
		Q (int): Le score de qualité en tant qu'entier.

	Returns:
		str: Le caractère ASCII correspondant.
	"""
	# Utilisation de la fonction chr() pour obtenir le caractère ASCII correspondant
	return chr(Q + 33)


def generate_read(sequence: str, mean: float, std_dev: float) -> Tuple[str, str]:
	"""
	Génère un read (read) à partir d'une séquence d'ADN avec des scores de qualité simulés.

	Args:
		sequence (str): La séquence d'ADN d'origine à partir de laquelle le read est générée.
		mean (float): La moyenne des scores de qualité.
		std_dev (float): L'écart-type des scores de qualité.

	Returns:
		Tuple[str, str]: Un tuple contenant la séquence de le read générée et sa qualité.

	Note:
		Cette fonction génère une read en itérant à travers chaque base de la séquence d'ADN
		d'origine. Pour chaque base, elle simule un score de qualité (Q-score) en utilisant la fonction
		`random_Q`, puis calcule la probabilité d'erreur associée à ce score à l'aide de la fonction
		`Q_to_proba`. Ensuite, la base est potentiellement mutée en une autre base en fonction de la
		probabilité d'erreur. Enfin, le caractère ASCII correspondant au score de qualité est obtenu avec
		la fonction `Q_to_ascii`. Le read générée est renvoyée sous forme d'un tuple contenant la
		séquence et la qualité.
	"""
	# Initialisation des variables pour la séquence finale et la qualité
	final_sequence = ''
	quality = ''

	# Itération à travers chaque base de la séquence d'ADN d'origine
	for base in sequence:
		# Simulation d'un score de qualité (Q-score) avec random_Q
		Q = random_Q(mean=mean, std_dev=std_dev)

		# Calcul de la probabilité d'erreur associée au score de qualité
		error_probability = Q_to_proba(Q=Q)

		# Potentielle mutation de la base en une autre base en fonction de la probabilité d'erreur
		final_sequence += mutate_base(base=base, error_probability=error_probability)

		# Obtention du caractère ASCII correspondant au score de qualité
		quality += Q_to_ascii(Q=Q)

	# Renvoi de la séquence générée et de sa qualité sous forme d'un tuple
	return final_sequence, quality


def choose_random_position(seq_length: int, min_length: int, max_length: int) -> Tuple[int, int]:
	"""
	Choisissez aléatoirement une position de début et de fin pour une sous-séquence.

	Args:
		seq_length (int): La longueur totale de la séquence d'origine.
		min_length (int): La longueur minimale de la sous-séquence.
		max_length (int): La longueur maximale de la sous-séquence.

	Returns:
		Tuple[int, int]: Un tuple contenant la position de début et de fin de la sous-séquence.
	"""

	# Choix aléatoire de la position de début et de fin
	min_position = rd.randint(0, seq_length)
	max_position = rd.randint(min_position, seq_length)

	# Vérification de la longueur de la sous-séquence
	while (max_position - min_position) < min_length or max_length < (max_position - min_position):
		min_position = rd.randint(0, seq_length)
		max_position = rd.randint(min_position, seq_length)

	# Renvoie un tuple contenant la position de début et de fin de la sous-séquence
	return min_position, max_position


def make_reads(dna_sequence: str,
			   n_reads: int,
			   min_length: int,
			   max_length: int,
			   mean: float,
			   std_dev: float) -> List[Tuple[str, str]]:
	"""
	Génère des reads à partir d'une séquence d'ADN.

	Args:
		dna_sequence (str): La séquence d'ADN d'origine.
		n_reads (int): Le nombre de reads à générer.
		min_length (int): La longueur minimale d'un read.
		max_length (int): La longueur maximale d'un read.
		mean (float): La moyenne des scores de qualité.
		std_dev (float): L'écart-type des scores de qualité.

	Returns:
		List[Tuple[str, str]]: Une liste de reads générés, chaque read étant un tuple (séquence, qualité).
	"""
	# Initialisation de la liste pour stocker les reads générés
	reads = []

	# Calcul de la longueur de la séquence d'ADN
	seq_length = len(dna_sequence)

	# Boucle pour générer le nombre spécifié de reads
	for i in range(n_reads):
		# Choix aléatoire de la position de début et de fin pour la sous-séquence
		min_pos, max_pos = choose_random_position(seq_length=seq_length, min_length=min_length, max_length=max_length)
		
		# Extraction de la sous-séquence
		sequence = dna_sequence[min_pos:max_pos]
		
		# Génération d'un read
		read = generate_read(sequence=sequence, mean=mean, std_dev=std_dev)
		
		# Ajout de le read à la liste des reads générés
		reads.append(read)

	# Renvoie la liste des reads générés
	return reads


def save_fasta(sequence: str, header: str, filename: str) -> None:
	"""
	Enregistre une séquence dans un fichier au format FASTA.

	Args:
		sequence (str): La séquence à enregistrer.
		header (str): L'en-tête de la séquence (nom).
		filename (str): Le nom du fichier de sortie.

	Returns:
		None
	"""
	# Ouvre le fichier en mode écriture
	with open(filename, 'w') as file:
		# Écrit l'en-tête de la séquence précédé d'un '>'
		file.write(f">{header}\n")
		# Écrit la séquence en morceaux de 60 caractères par ligne
		for i in range(0, len(sequence), 60):
			file.write(sequence[i:i + 60] + "\n")


def save_reads(reads: List[Tuple[str, str]], filename: str, output_format: str = "fastq") -> None:
	"""
	Enregistre une liste de reads au format FASTA ou FASTQ dans un fichier.

	Args:
		reads (List[Tuple[str, str]]): Liste de reads sous forme de tuples (séquence, qualité).
		filename (str): Le nom du fichier de sortie.
		output_format (str): Le format de sortie, "fasta" ou "fastq" (par défaut "fastq").

	Returns:
		None
	"""
	# Ouvre le fichier en mode écriture
	with open(filename, 'w') as file:
		# Parcourt la liste de reads en numérotant les reads à partir de 1
		for i, read in enumerate(reads, start=1):
			sequence, quality = read
			# Écrit les données du read dans le fichier au format FASTQ ou FASTA
			if output_format.lower() == "fastq":
				file.write(f"@read_{i}\n{sequence}\n+\n{quality}\n")
			elif output_format.lower() == "fasta":
				file.write(f">{sequence}_{i}\n{sequence}\n")
			else:
				# Si le format de sortie n'est ni "fasta" ni "fastq, lève une exception ValueError
				raise ValueError("Le format de sortie doit être 'fasta' ou 'fastq'.")


if __name__ == "__main__":

	# Crée un objet parser pour gérer les options de ligne de commande
	parser = argparse.ArgumentParser(description="Génère une séquence ADN aléatoire et des reads.")

	# Définit les options de ligne de commande avec des descriptions en français
	parser.add_argument("-r", "--random_state", type=int, default=42, help="Graine aléatoire pour la reproductibilité. (Défaut:42)")
	parser.add_argument("-s", "--sequence_length", type=int, default=10000, help="Longueur de la séquence ADN, . (Défaut:10000)")
	parser.add_argument("-n", "--n_reads", type=int, default=1000, help="Nombre de reads à générer, . (Défaut:1000)")
	parser.add_argument("-L", "--min_length", type=int, default=50, help="Longueur minimale des reads, . (Défaut:50)")
	parser.add_argument("-M", "--max_length", type=int, default=150, help="Longueur maximale des reads, . (Défaut:150)")
	parser.add_argument("-q", "--mean", type=float, default=18, help="Score de qualité moyen, . (Défaut:18)")
	parser.add_argument("-d", "--std_dev", type=float, default=3, help="Écart-type des scores de qualité, . (Défaut:3)")
	parser.add_argument("-H", "--header", type=str, default="sequence", help="En-tête pour le génome de référence. (Défaut:sequence)")
	parser.add_argument("-G", "--save_refGenome", action="store_true", help="Enregistrer le génome de référence")
	parser.add_argument("-N", "--no_save_refGenome", dest="save_refGenome", action="store_false", help="Ne pas enregistrer le génome de référence")
	parser.add_argument("-R", "--save_readsGenerated", action="store_true", help="Enregistrer les reads générés")
	parser.add_argument("-P", "--no_save_readsGenerated", dest="save_readsGenerated", action="store_false", help="Ne pas enregistrer les reads générés")
	parser.add_argument("-f", "--file_refGenome", type=str, default="sequenceRefGenomeGenerated.fasta", help="Nom de fichier pour le génome de référence, . (Défaut:'sequenceRefGenomeGenerated.fasta')")
	parser.add_argument("-F", "--file_reads", type=str, default="readsGenerated.fastq", help="Nom de fichier pour les reads générés, . (Défaut:'readsGenerated.fastq')")
	parser.add_argument("-o", "--output_format", type=str, default="fastq", help="Format de sortie pour les reads générés (fastq ou fasta). (Défaut:fastq)")

	# Analyse les options de ligne de commande
	args = parser.parse_args()

	# Génère une séquence ADN aléatoire
	dna_sequence = generate_RdmSeq(sequence_length=args.sequence_length, random_state=args.random_state)

	# Enregistre le génome de référence si l'option est activée
	if args.save_refGenome:
		save_fasta(sequence=dna_sequence, header=args.header, filename=args.file_refGenome)

	# Génère des reads à partir de la séquence ADN
	reads = make_reads(
		dna_sequence=dna_sequence,
		n_reads=args.n_reads,
		min_length=args.min_length,
		max_length=args.max_length,
		mean=args.mean,
		std_dev=args.std_dev
	)

	# Enregistre les reads générés si l'option est activée
	if args.save_readsGenerated:
		save_reads(reads=reads, filename=args.file_reads, output_format=args.output_format)