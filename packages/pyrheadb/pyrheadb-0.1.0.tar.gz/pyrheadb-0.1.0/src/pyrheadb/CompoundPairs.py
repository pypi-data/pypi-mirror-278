#######################3
# find_closest_compounds_for_each_disconnected_cluster.py
#######################

import pandas as pd
from rdkit import Chem
from rdkit.Chem import rdFMCS
import numpy as np

import sys

# tell interpreter where to look
sys.path.insert(0, "..")
from map4.map4 import MAP4Calculator

checktype = 'MCS'
checktype = 'MAP4'

class CompoundPairs():
	def __init__(self):
		pass
	def lookup_pair(self, inchi1, inchi2):
		"""
		Function to lookup if pair exists in the Rhea graph
		:param inchi1:
		:param inchi2:
		:return:
		"""
		return
class MAP4FPEncoder():
	def __init__(self):
		self.dimensions = 2048
		self.radius = 2
		self.is_counted = False
		self.is_folded = False
	
	def get_minhash_distance(self, vec_a, vec_b):
		"""
		Copied from the function for distance calculation used in MAP4
		:param vec_b:
		:return:
		"""
		intersect = 0;
		length = len(vec_a)
		for i in range(len(vec_a)):
			if (vec_a[i] == vec_b[i]):
				intersect += 1
		return 1.0 - intersect / length
	
	def encode_list(self, smiles_list):
		calculator = MAP4Calculator(self.dimensions, self.radius, self.is_counted, self.is_folded)
		batch = [Chem.MolFromSmiles(i, sanitize=False) for i in smiles_list]
		return [np.array(list(i)) for i in calculator.calculate_many(batch)]
	
	def encode(self, smiles):
		mol = Chem.MolFromSmiles(smiles, sanitize=False)
		calculator = MAP4Calculator(self.dimensions, self.radius, self.is_counted, self.is_folded)
		return calculator.calculate(mol)

def compare_cluster_id(cluster_id, output_file):
	# cluster_id = 6
	
	compounds_disconnected = df_clusters[df_clusters['cluster_id'] == cluster_id]['chebi_id'].to_list()
	smiles = df_smiles[df_smiles['chebi_id'].isin(compounds_disconnected)]['smiles'].to_list()
	
	if checktype == 'MCS':
		mols = [Chem.MolFromSmiles(i) for i in smiles]
		for m in mols:
			Chem.RemoveStereochemistry(m)
	
	map4fps = mp4.encode_list(smiles)
	
	for sm in smiles_connected:
		if checktype == 'MCS':
			molcheck = Chem.MolFromSmiles(sm)
			Chem.RemoveStereochemistry(molcheck)
			mols_check = mols
			mols_check.append(molcheck)
			res = rdFMCS.FindMCS(mols_check)
			na = res.numAtoms
			nb = res.numBonds
			if na > 1:
				chebi_id = df_smiles[df_smiles['smiles'] == sm]['chebi_id'].iloc[0]
				print(res.numAtoms, res.numBonds, chebi_id)
			# print(res.smartsString)
		elif checktype == 'MAP4':
			fp_test = mp4.encode(sm)
			distances = [mp4.get_minhash_distance(fp_test, cluster_molecule_fp) for cluster_molecule_fp in map4fps]
			if any([i < 0.2 for i in distances]):
				chebi_id = df_smiles[df_smiles['smiles'] == sm]['chebi_id'].iloc[0]
				output_file.write(f"{cluster_id}\t{chebi_id}\t{';'.join(['%.2f' % i for i in distances])}\n")

mp4 = MAP4FPEncoder()

df_clusters = pd.read_csv('results/components_chebi_id_with_hub_human.csv')
print(df_clusters.head())
print(df_clusters.columns)

df_smiles = pd.read_csv('rhea-chebi-smiles.tsv', sep='\t', names=['chebi_id', 'smiles'])
print(df_smiles.head())

compounds_connected = df_clusters[df_clusters['cluster_id'] == 1]['chebi_id'].to_list()
smiles_connected = df_smiles[df_smiles['chebi_id'].isin(compounds_connected)]['smiles'].to_list()

clusters_ids = list(df_clusters['cluster_id'].unique())
cluster_ids_not_1 = list(set(clusters_ids) - {1})

output_file = open('results/cluter_ids_similarity.tsv', 'w')
output_file.write('cluster_id	compound	sim_scores\n')
for cluster_id in cluster_ids_not_1:
	print(cluster_id, type(cluster_id))
	compare_cluster_id(cluster_id, output_file)
output_file.close()
