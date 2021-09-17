from enum import IntEnum

Nucleotide: IntEnum = IntEnum("Nucleotide", ("A", "C", "G", "T"))

Codon = tuple[Nucleotide, Nucleotide, Nucleotide]
Gene = list[Codon]


def string_to_gene(s: str) -> Gene:
    gene: Gene = []
    for i in range(0, len(s), 3):
        if i + 2 >= len(s):
            break
        codon = (Nucleotide[s[i]], Nucleotide[s[i + 1]], Nucleotide[s[i + 2]])
        gene.append(codon)
    return gene


def linear_contains(gene: Gene, key: Codon) -> bool:
    return key in gene


def binary_contains(gene: Gene, key: Codon) -> bool:
    low: int = 0
    high = len(gene) - 1
    while low <= high:  # as long as there is search space
        mid: int = (low + high) // 2
        if gene[mid] > key:
            high = mid - 1
        elif gene[mid] < key:
            low = mid + 1
        else:
            return True
    return False


if __name__ == "__main__":
    gene_str = "AGTC" * 30
    gene = string_to_gene(gene_str)
    # print(gene)
    gtc = (Nucleotide.G, Nucleotide.T, Nucleotide.C)
    print(linear_contains(gene, gtc))
    print(binary_contains(sorted(gene), gtc))
