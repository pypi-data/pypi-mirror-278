"""
This is a module designed to shred a genome into 'reads' of consistent length
along the entirety of the genome in a sliding window fashion.
Takes three arguments:
path is required. This refers to the directory of fastas
window_size defaults to 150. This refers to the length of the "read"
extension defaults to .fna. This refers to the input fasta file extension
"""

from Bio import SeqIO
import os

def window(fseq, window_size):
    for i in range(len(fseq) - window_size + 1):
        yield fseq[i:i+window_size]


def reads_generation(path,window_size=150,extension='.fna'):
#Identify the sequences from SequencePath argument or NN argument and generate in reads for each one at 100x coverage. Output to location.
#Note, NNs are not yet part of this script.
#Loop through sequences in directory, run dwgsim


    print("Generating reads by sliding window across genome")
    odirectory = (path + '/reads')
    if not os.path.exists(odirectory):
        os.makedirs(odirectory)

    print(odirectory)

    for file in os.listdir(path):
        if file.endswith(extension):
            print(file)
            input_file = (path + '/' + file)
            output_prefix = (os.path.basename(file).split(extension)[0])
            print(output_prefix)
            outputfile = ('{0}/{1}.sliding.fasta'.format(odirectory,output_prefix))

            with open(input_file,'r') as f:
                with open(outputfile,'w') as o:
                    for record in SeqIO.parse(f,'fasta'):
                        counter=0
                        for item in window(record.seq,window_size):
                            counter+=1
                            item=str(item)
                            id='{0}.{1}'.format(record.id,counter)
                            o.write(">{0}\n{1}\n".format(id,item))


