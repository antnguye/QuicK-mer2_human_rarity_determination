# QuicK-mer2
k-mer based analysis for paralog specific copy number estimation

To compile the software, clone the repository, move the QuicK-mer2 directory and type make.

You may receive some warnings. This will create an executable named quicKmer2.  

If you are interested in generating copy-number estimates based on multi-mapping reads, consider fastCN, accessible at: https://github.com/KiddLab/fastCN


## Usage
The basic functionality of quickMer2 is described by executing the program with no options.

```
./quicKmer2 
QuicK-mer2
Operation modes: 
	index	Index a bed format kmer list
	count	CNV estimate from library
	search	Search K-kmer in genome
	est	GC normalization into copy number
	sparse	Fractionate indexed kmer for memory reduction or regenerate GC control/Window

Simple operation:
1. Construct a dictionary from fasta using "search"
2. Count depth from sample fasta/fastq "count"
3. Estimate copy number with "est"
```

The typical flow is to first create a set of unique k-mers from a genome reference fasta sequence using
the search command. The search command has several options.

```
./quicKmer2 search

quicKmer2 search [Options] ref.fa

Options:
-h		Show this help information
-k [num]	Size of K-mer. Must be between 3-32. Default 30
-t [num]	Number of threads for edit distance search
-s [num]	Size of hash dictionary. Can use suffix G,M,K
-e [num]	Edit distance search. 0, 1 or 2
-d [num]	Edit distance depth threshold to keep. 1..255, Default 100
-w [num]	Output window definition size. Default 1000
-c [filename]	Input bedfile for GC control regions
```

The -c option specifies a bedfile of regions that are not expected to be copy-number variable
across the analyzed samples. Sex chromosomes, unplaced chromosome sequences, known segmental duplications
and known copy-number variants should be excluded.  Exclusion files and be converted to inclusion files
using appropriate `bedtools` commands.  Note that sufficient memory for tabulating kmers must be available.  Threads
are used for searching for additional hits within an edit distance of 1 or 2 substituions.  Multiple threads greatly 
speedup this process. 

Next, the occurrences of each k-mer are tabulated in a set of sequence reads using the `count` command.

```
./quicKmer2 count -h

quicKmer2 count [Options] ref.fa sample.fast[a/q] Out_prefix

Options:
-h		Show this help information
-t [num]	Number of threads
```

To process from an aligned BAM file, a typical command would be:

```
samtools view -F 3840 PATH/TO/BAM/FILE | awk '{print ">\n"$10}' | 
QuicK-mer2/quicKmer2 count -t NUMTHREADS /dev/fd/0 GENOME/REF/FASTA.fa  OUTPUT/DIR/SAMPLE_NAME
```

For CRAM files, you made need to include the genome reference file (using `samtools -T`).  CRAM 
processing speed can be increased using the  `--input-fmt-option required_fields=0x202` option. 
Good performance gains are typically found with use of up 6 threads.  Sufficient memory to
load the k-mer database is required.  Input read sequences are processed as a stream. 


Finally, the count values are corrected for local GC content, converted to copy-number estimates,
and output in windows along the genome.  

```
./quicKmer2 est -h
GC control file missing.
quicKmer2 est ref.fa sample_prefix output.bed
	ref.fa		Prefix to genome reference. Program requires .qgc and .bed definition
	sample_prefix	Prefix to sample.bin
	output.bed	Output bedfile for copy number

No options available
```


An example command is:
```
QuicK-mer2/quicKmer2 est  GENOME/REF/FASTA.fa OUTPUT/DIR/SAMPLE_NAME  OUTPUT/DIR/SAMPLE_NAME.CN.1k.bed
```



