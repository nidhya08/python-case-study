table = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
    'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
}
def open_file(inputfile):
"""Doc String: This method gets a input file and creates a sequence from it and also replaces escape sequences"""
	with open(inputfile,"r") as f:
		seq = f.read()
	seq = seq.replace("\n","")
	seq = seq.replace("\r","")
	return(seq)
"""Doc String: This method gets the DNA sequence and returns the computed amino acid sequence"""
def translate(seq):
	protein = ""
	if len(seq) % 3 ==0:
		for i in range(0,len(seq),3):
			codon = seq[i : i+3]
			protein += table[codon]
	return(protein)
	
protein_file = "protein.txt"
dna_file = "dna.txt"
protein_seq = open_file(protein_file)
dna_seq = open_file(dna_file)

retrieved_protein = translate(dna_seq[20:938])[:-1]
print(retrieved_protein)