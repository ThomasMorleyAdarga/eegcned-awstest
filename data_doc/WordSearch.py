
import argparse



def main(input):



    dep_dict = {'O': 0, 'punct': 1, 'iobj': 2, 'parataxis': 3, 'auxpass': 4, 'aux': 5, 'conj': 6,
                'advcl': 7, 'acl:relcl': 8, 'nsubjpass': 9, 'csubj': 10, 'compound': 11, 'compound:prt': 12,
                'mwe': 13, 'cop': 14, 'neg': 15, 'nmod:poss': 16, 'appos': 17, 'cc:preconj': 18, 'nmod': 19,
                'nsubj': 20, 'xcomp': 21, 'det:predet': 22, 'nmod:npmod': 23, 'acl': 24, 'amod': 25,
                'expl': 26, 'csubjpass': 27, 'case': 28, 'ccomp': 29, 'dobj': 30, 'ROOT': 31,
                'discourse': 32, 'nmod:tmod': 33, 'dep': 34, 'nummod': 35, 'mark': 36, 'advmod': 37,
                'cc': 38, 'det': 39, 'nmod:in': 40, 'det:qmod': 41, 'nmod:until': 41, 'nmod:of': 43, 'nmod:on': 44,
                'advcl:as': 45, 'nmod:with': 46, 'nmod:by': 47,
                'nmod:instead_of': 48, 'nmod:for': 49, 'nmod:to': 50, 'ref': 52, 'nmod:agent': 53, 'conj:and': 54,
                'nmod:like': 55, 'nsubj:xsubj': 56,
                'nmod:at': 57, 'advcl:if': 58, 'nmod:than': 59, 'conj:or': 60, 'acl:to': 61, 'nmod:under': 62,
                'advcl:to': 63, 'acl:of': 64, 'nmod:from': 65,
                'nmod:between': 66, 'advcl:for': 67, 'conj:but': 68, 'advcl:in': 69, 'nmod:as': 70, 'advcl:because': 71,
                'advcl:than': 72, 'nmod:after': 73,
                'nmod:about': 74, 'nmod:over': 75, 'nmod:within': 76, 'advcl:about': 77, 'nsubjpass:xsubj': 78,
                'advcl:while': 79, 'nmod:through': 80,
                'advcl:into': 81, 'advcl:like': 82, 'nmod:against': 83, 'nmod:out_of': 84, 'nmod:across': 85,
                'acl:for': 86, 'nmod:because_of': 87,
                'conj:instead': 88, 'acl:in': 89, 'advcl:without': 90, 'nmod:because': 91, 'advcl:before': 92,
                'nmod:except_for': 93, 'nmod:around': 94,
                'advcl:at': 95, 'nmod:during': 96, 'nmod:according_to': 97, 'advcl:since': 98, 'conj:&': 99,
                'acl:whether': 100, 'advcl:so': 101,
                'advcl:unless': 102, 'nmod:toward': 103, 'advcl:until': 104, 'advcl:in_order': 105, 'acl:on': 106,
                'nmod:behind': 107, 'advcl:by': 108,
                'nmod:among': 109, "nmod:'s": 110, 'advcl:on': 111, 'nmod:without': 112, 'advcl:of': 113,
                'nmod:into': 114, 'nmod:such_as': 115,
                'nmod:except': 116, 'nmod:but': 117, 'nmod:far_from': 118, 'nmod:that': 119, 'nmod:near': 120,
                'nmod:out': 121, 'advcl:whether': 122,
                'advcl:with': 123, 'nmod:down': 124, 'advcl:so_that': 125, 'advcl:that': 126, 'acl:as': 127,
                'nmod:including': 128, 'nmod:before': 129,
                'nmod:beyond': 130, 'conj:in': 131, 'nmod:up': 132}


    with open(input, 'r') as file:
        for line in file:
            if len(line.split(' ')) > 1:
                if line.split(" ")[5] not in dep_dict:
                    print(f"elif syntactic_label_data[0].split(':')[1].startswith(\"{line.split(' ')[5].split(':')[1]}\") and syntactic_label_data[0].split(':')[0].startswith('{line.split(' ')[5].split(':')[0]}'):")
                    print("\tsyntactic_label_data[0] = syntactic_label_data[0].split(':')[0]")



















if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='egnn for ed')

    parser.add_argument('inp', default="", type=str)

    args = parser.parse_args()

    in_file = args.inp

    main(in_file)