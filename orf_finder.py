import os
import sys
import re

class ORFFinder:
    def _init_(self):
        pass

    def read_fasta_file(self, file_path):
        sequences = {}
        with open(file_path, 'r') as file:
            sequence_id = ''
            sequence = ''
            for line in file:
                line = line.strip()
                if line.startswith('>'):
                    if sequence_id:
                        sequences[sequence_id] = sequence
                        sequence = ''
                    sequence_id = line[1:]
                else:
                    sequence += line
            if sequence_id and sequence:
                sequences[sequence_id] = sequence
        return sequences

    def find_longest_orf(self, sequence):
        start_codon = 'ATG'
        stop_codons = ['TAG', 'TGA', 'TAA']
        longest_orf = ''

        for i in range(len(sequence)):
            if sequence[i:i + 3] == start_codon:
                for j in range(i + 3, len(sequence), 3):
                    codon = sequence[j:j + 3]
                    if codon in stop_codons:
                        current_orf = sequence[i:j + 3]
                        if len(current_orf) > len(longest_orf):
                            longest_orf = current_orf
                        break

        return longest_orf

    def process_sequences(self, sequences):
        longest_orfs = {}
        for seq_id, sequence in sequences.items():
            longest_orf = self.find_longest_orf(sequence)
            longest_orfs[seq_id] = longest_orf
        return longest_orfs

    def find_overall_longest_orf(self, file_path):
        sequences = self.read_fasta_file(file_path)
        longest_orfs = self.process_sequences(sequences)
        overall_longest_orf = ''
        for seq_id, longest_orf in longest_orfs.items():
            if len(longest_orf) > len(overall_longest_orf):
                overall_longest_orf = longest_orf
        return overall_longest_orf

def main():
    fasta_file_path = '/content/SeqRandom.txt'
    orf_finder = ORFFinder()
    result = orf_finder.process_sequences(orf_finder.read_fasta_file(fasta_file_path))
    for seq_id, longest_orf in result.items():
        print(f"Sequence ID: {seq_id}, Longest ORF: {longest_orf}, length: {len(longest_orf)}")
    # Overall longest ORF
    result = orf_finder.find_overall_longest_orf(fasta_file_path)
    print(f"Overall longest ORF: {result}, length: {len(result)}")

if __name__ == "__main__":
    main()
