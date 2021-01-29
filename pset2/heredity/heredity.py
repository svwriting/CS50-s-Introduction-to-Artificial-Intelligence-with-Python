import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    set_people=set(people)
    gngptpDic={} # gn,gp,tp=gene_num , gene_probability , trait_probability
    for person in people:
        if person in two_genes:
            gn=2
        elif person in one_gene:
            gn=1
        else:
            gn=0
        tp=PROBS["trait"][gn][person in have_trait]
        gp=None
        if people[person]['mother']==None and people[person]['father']==None:
            gp=PROBS["gene"][gn]
            set_people.remove(person)
        gngptpDic[person]={'gn':gn,'gp':gp,'tp':tp}
    # print(gngptpDic)
    while len(set_people)>0:
        set_=set_people.copy()
        for person in set_:
            if (gngptpDic[people[person]['mother']]!=None \
                    and gngptpDic[people[person]['mother']]['gp']==None) \
                or (gngptpDic[people[person]['father']]!=None \
                    and gngptpDic[people[person]['father']]['gp']==None):
                continue
            else:
                set_people.remove(person)
            momdad=(people[person]['mother'],people[person]['father'])
            if gngptpDic[person]['gn']==0:
                gp=1
                for parent in momdad:
                    if parent==None:
                        gp*=PROBS["gene"]['gn']
                    elif gngptpDic[parent]['gn']==0:
                        gp*=1-PROBS["mutation"]
                    elif gngptpDic[parent]['gn']==1:
                        gp*=0.5
                    else: # gngptpDic[parent['name']]['gn']==2
                        gp*=PROBS["mutation"]
            elif gngptpDic[person]['gn']==2:
                gp=1
                for parent in momdad:
                    if parent==None:
                        gp*=PROBS["gene"]['gn']
                    elif gngptpDic[parent]['gn']==0:
                        gp*=PROBS["mutation"]
                    elif gngptpDic[parent]['gn']==1:
                        gp*=0.5
                    else: # gngptpDic[parent['name']]['gn']==2
                        gp*=1-PROBS["mutation"]
            else: # gngptpDic[person]['gn']==1
                gp0,gp1=1,1
                for parent in momdad:
                    if parent==None:
                        gp0*=PROBS["gene"]['gn']
                        gp1*=PROBS["gene"]['gn']
                    elif gngptpDic[parent]['gn']==0:
                        gp0*=1-PROBS["mutation"]
                        gp1*=PROBS["mutation"]
                    elif gngptpDic[parent]['gn']==1:
                        gp0*=0.5
                        gp1*=0.5
                    else: # gngptpDic[parent['name']]['gn']==2
                        gp0*=PROBS["mutation"]
                        gp1*=1-PROBS["mutation"]
                    gp0,gp1=gp1,gp0
                gp=gp0+gp1
            gngptpDic[person]['gp']=gp
        # print(gngptpDic)
    EntireJointProbability=1
    for person in gngptpDic:
        EntireJointProbability*=gngptpDic[person]['gp']*gngptpDic[person]['tp']
    # print(" EP:",EntireJointProbability)
    # print(gngptpDic)
    """
    if(one_gene=={"Harry"} and two_genes=={"James"} and have_trait=={"James"}):
        person_s=("Lily","James","Harry")
        for person in person_s:
            print(person,gngptpDic[person]['gn'],gngptpDic[person]['gp'],gngptpDic[person]['tp'],gngptpDic[person]['gp']*gngptpDic[person]['tp'])
    """
    return EntireJointProbability
    raise NotImplementedError


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in two_genes:
            probabilities[person]['gene'][2]+=p
        elif person in one_gene:
            probabilities[person]['gene'][1]+=p
        else:
            probabilities[person]['gene'][0]+=p
        if person in have_trait:
            probabilities[person]['trait'][True]+=p
        else:
            probabilities[person]['trait'][False]+=p
    #print(probabilities)
    #raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        for gt in probabilities[person]:
            P_=0
            for i in probabilities[person][gt]:
                P_+=probabilities[person][gt][i]
            Z_=1/P_
            for i in probabilities[person][gt]:
                probabilities[person][gt][i]*=Z_
    #raise NotImplementedError


if __name__ == "__main__":
    main()
