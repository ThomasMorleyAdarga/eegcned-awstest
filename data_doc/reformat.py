import argparse
import json

def main(input, output):


    stringset = set()

    #First open Json file
    with open(input, 'r') as f:
        ace_original = json.load(f)

    with open(output, "w") as g:

        #Iterate data points
        for sample in ace_original:

            #Create array matrix for current sentence
            entire_block = [[None]*7 for i in range(len(sample['words']))]

            #Iterate words in this current sample
            for i, word in enumerate(entire_block):

                #Add token to the output matrix
                if sample['words'][i] == ' ' or sample['words'][i].startswith("\\"):
                    word[0] = 'q'
                else:
                    word[0] = sample['words'][i]

                #Add 'ace' for doc_id
                word[1] = 'ace'

                #Set default values for entity and event types
                word[2] = "O"
                word[3] = "O"
                word[4] = "O"

                #Set default syntactic labels because some data is a bit skew whiff
                word[5] = "O"
                word[6] = "O"

            # Set syntactic label
            for syntactic_label in sample['stanford-colcc']:

                syntactic_label_data = []

                if syntactic_label.split("/")[1].startswith("dep"):
                    syntactic_label_data.append(syntactic_label.split("/")[0])
                    syntactic_label_data.append(int(syntactic_label.split("/")[1][4:]))
                    syntactic_label_data.append(int(syntactic_label.split("/")[2][4:]))

                else:
                    syntactic_label_data.append(syntactic_label.split("/")[0] + syntactic_label.split("/")[1])
                    syntactic_label_data.append(int(syntactic_label.split("/")[2][4:]))
                    syntactic_label_data.append(int(syntactic_label.split("/")[3][4:]))

                dep_dict = {'O': 0, 'punct': 1, 'iobj': 2, 'parataxis': 3, 'auxpass': 4, 'aux': 5, 'conj': 6,
                            'advcl': 7, 'acl:relcl': 8, 'nsubjpass': 9, 'csubj': 10, 'compound': 11, 'compound:prt': 12,
                            'mwe': 13, 'cop': 14, 'neg': 15, 'nmod:poss': 16, 'appos': 17, 'cc:preconj': 18, 'nmod': 19,
                            'nsubj': 20, 'xcomp': 21, 'det:predet': 22, 'nmod:npmod': 23, 'acl': 24, 'amod': 25,
                            'expl': 26, 'csubjpass': 27, 'case': 28, 'ccomp': 29, 'dobj': 30, 'ROOT': 31,
                            'discourse': 32, 'nmod:tmod': 33, 'dep': 34, 'nummod': 35, 'mark': 36, 'advmod': 37,
                            'cc': 38, 'det': 39, 'nmod:in':40, 'det:qmod':41, 'nmod:until':41, 'nmod:of':43, 'nmod:on':44, 'advcl:as':45, 'nmod:with':46, 'nmod:by':47,
                            'nmod:instead_of':48, 'nmod:for':49, 'nmod:to':50, 'ref':52, 'nmod:agent':53, 'conj:and':54, 'nmod:like':55, 'nsubj:xsubj':56,
                            'nmod:at':57, 'advcl:if':58, 'nmod:than':59, 'conj:or':60, 'acl:to':61, 'nmod:under':62, 'advcl:to':63, 'acl:of':64, 'nmod:from':65,
                            'nmod:between':66, 'advcl:for':67, 'conj:but':68, 'advcl:in':69, 'nmod:as':70, 'advcl:because':71, 'advcl:than':72, 'nmod:after':73,
                            'nmod:about':74, 'nmod:over':75, 'nmod:within':76, 'advcl:about':77, 'nsubjpass:xsubj':78, 'advcl:while':79, 'nmod:through':80,
                            'advcl:into':81, 'advcl:like':82, 'nmod:against':83, 'nmod:out_of':84, 'nmod:across':85, 'acl:for':86, 'nmod:because_of':87,
                            'conj:instead':88, 'acl:in':89, 'advcl:without':90, 'nmod:because':91, 'advcl:before':92, 'nmod:except_for':93, 'nmod:around':94,
                            'advcl:at':95, 'nmod:during':96, 'nmod:according_to':97, 'advcl:since':98, 'conj:&':99, 'acl:whether':100, 'advcl:so':101,
                            'advcl:unless':102, 'nmod:toward':103, 'advcl:until':104, 'advcl:in_order':105, 'acl:on':106, 'nmod:behind':107, 'advcl:by':108,
                            'nmod:among':109, "nmod:'s":110, 'advcl:on':111, 'nmod:without':112, 'advcl:of':113, 'nmod:into':114, 'nmod:such_as':115,
                            'nmod:except':116, 'nmod:but':117, 'nmod:far_from':118, 'nmod:that':119, 'nmod:near':120, 'nmod:out':121, 'advcl:whether':122,
                            'advcl:with':123, 'nmod:down':124, 'advcl:so_that':125, 'advcl:that':126, 'acl:as':127, 'nmod:including':128, 'nmod:before':129,
                            'nmod:beyond':130, 'conj:in':131, 'nmod:up':132, 'nmod:atop':133, 'advcl:once':134, 'nmod:beginning':135, 'advcl:after':136, 'nmod:past':137, 'advcl:such':138, 'nmod:vs.':139, 'advcl:behind':140, 'nmod:inside_of':141,
                            'nmod:given':142, 'acl:based_on':143, 'nmod:plus':144, 'nmod:onto':145, 'nmod:\'':146, 'acl:before':147, 'conj:just':148, 'advcl:till':149,
                            'advcl:whilst':150, 'nmod:in_front_of':151, 'advcl:below':152, 'nmod:oconer':153, 'nmod:away_from':154, 'nmod:pending':155, 'acl:compared_to':156,
                            'acl:until':157, 'advcl:f.':158, 'conj:+':159, 'advcl:among':160, 'advcl:through':161, 'acl:including':162, 'nmod:together_with':163, 'acl:because':164,
                            'conj:plus':165, 'nmod:versus':166, 'acl:next_to':167, 'nmod:contrary_to':168, 'advcl:close_to':169, 'advcl:around':170, 'conj:andor':171, 'conj:as':172,
                            'nmod:above':173, 'nmod:while':174, 'acl:between':175, 'nmod:involving':176, 'nmod:towards':177, 'acl:instead_of':178, 'advcl:over':179, 'nmod:regarding':180,
                            'nmod:despite':181, 'nmod:next_to':182, 'nmod:as_for':183, 'nmod:besides':184, 'advcl:toward':185, 'acl:about':186, 'nmod:concerning':187, 'advcl:instead_of':188,
                            'advcl:not':189, 'conj:x':190, 'conj:v.':191, 'nmod:compared_with':192, 'nmod:both':193, 'conj:even':194, 'nmod:alongside':195, 'nmod:beside':196,
                            'nmod:along':197, 'advcl:though':198, 'nmod:across_from':199, 'nmod:aboard':200, 'nmod:on_behalf_of':201, 'nmod:upon':202, 'nmod:worth':203, 'advcl:either':204,
                            'nmod:with_regard_to':205, 'advcl:inside':206, 'acl:besides':207, 'nmod:throughout':208, 'nmod:as_of':209, 'conj:vs':210, 'nmod:amongst':211,
                            'nmod:considering':212, 'nmod:next':213, 'acl:at':214, 'conj:only':215, 'acl:from':216, 'nmod:regardless_of':217, 'nmod:and':218, 'nmod:excluding':219,
                            'advcl:compared_to':220, 'acl:over':221, 'advcl:_':222, 'acl:after':223, 'nmod:_':224, 'advcl:as_if':225, 'conj:so':226, 'advcl:ago':227, 'advcl:depending':228,
                            'nmod:inside':229, 'nmod:underneath':230, 'nmod:via':231, 'nmod:other':232, 'advcl:although':233, 'nmod:off':234, 'nmod:since':235, 'advcl:abc':236, 'nmod:beneath':237,
                            'advcl:rather_than':238, 'nmod:outside':239, 'nmod:either':240, 'nmod:close_to':241, 'nmod:in_spite_of':242, 'advcl:along':243, 'acl:against':244, 'nmod:along_with':245,
                            'advcl:under':246, 'nmod:once':247, 'nmod:per':248, 'nmod:on_top_of':249, 'nmod:amid':250, 'acl:without':251, 'advcl:in_case':252, 'acl:that':253, 'nmod:as_to':254, 'advcl:including':255,
                            'nmod:till':256, 'acl:as_to':257, 'advcl:\'s':258, 'nmod:apart_from':259, 'advcl:near':260, 'nmod:whether':261, 'conj:not':262, 'nmod:following':263, 'acl:except':264,
                            'nmod:based_on':265, 'nmod:in_addition_to':266, 'acl:since':267, 'advcl:ta':268, 'acl:like':269, 'nmod:de':270, 'nmod:outside_of':271, 'advcl:based_on':272, 'advcl:a.':273,
                            'nmod:or':274, 'conj:negcc':275, 'nmod:due_to':276, 'advcl:except':277, 'nmod:unlike':278, 'nmod:if':279, 'acl:with':280, 'nmod:below':281, 'advcl:within':282, 'advcl:outside':283, 'advcl:despite':284,
                            'conj:nor':285, 'nmod:thru':286, 'acl:by':287, 'advcl:out_of':288, 'advcl:out':289, 'nmod:in_case_of':290, 'advcl:during':291, 'advcl:from':292, 'advcl:between':293, 'conj:versus':294}



                if syntactic_label_data[0] not in dep_dict:
                    stringset.add(syntactic_label_data[0])

                """


                #contingenecies for unrecognised dependencies
                if len(syntactic_label_data[0].split(':')) > 1:
                    if syntactic_label_data[0].split(':')[1].startswith('in') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('up') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('in') and syntactic_label_data[0].split(":")[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('beyond') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('before') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('including') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('as') and syntactic_label_data[0].split(":")[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('that') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('so_that') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('down') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('with') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('whether') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('out') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('near') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('that') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('far_from') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('but') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('except') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('such_as') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('into') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('of') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('without') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('on') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("'s") and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('among') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('by') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('behind') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('on') and syntactic_label_data[0].split(":")[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('in_order') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('until') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('toward') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('unless') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('so') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('whether') and syntactic_label_data[0].split(":")[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('&') and syntactic_label_data[0].split(":")[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('since') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('according_to') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('during') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('at') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('around') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('except_for') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('before') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('because') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('instead') and syntactic_label_data[0].split(":")[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('in') and syntactic_label_data[0].split(":")[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('without') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('across') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('because_of') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('for') and syntactic_label_data[0].split(":")[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(":")[1].startswith('qmod') and syntactic_label_data[0].split(":")[0].startswith('det'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('until') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('of') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('as') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('on') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('with') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('by') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('instead_of') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('for') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('to') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('agent') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('and') and syntactic_label_data[0].split(":")[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('like') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('xsubj') and syntactic_label_data[0].split(":")[0].startswith('nsubj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('at') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('if') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('than') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('or') and syntactic_label_data[0].split(":")[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('to') and syntactic_label_data[0].split(":")[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('under') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('to') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('of') and syntactic_label_data[0].split(":")[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('from') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('between') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('for') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('but') and syntactic_label_data[0].split(":")[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('in') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('as') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('because') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('than') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('after') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('about') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('over') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('within') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('about') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('xsubj') and syntactic_label_data[0].split(":")[0].startswith('nsubjpass'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('while') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('through') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('into') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('like') and syntactic_label_data[0].split(":")[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('against') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith('out_of') and syntactic_label_data[0].split(":")[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]




                    elif syntactic_label_data[0].split(':')[1].startswith("amid") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("making") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("close_by") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]






                    elif syntactic_label_data[0].split(':')[1].startswith("out_of") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("in_case_of") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("alongside") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("with") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("besides") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("during") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("versus") and syntactic_label_data[0].split(':')[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("in_front_of") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("abc") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("from") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("concerning") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("as_of") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("beneath") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("instead_of") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("amongst") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("including") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("close_to") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("with_regard_to") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("off") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("x") and syntactic_label_data[0].split(':')[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("over") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("considering") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("either") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("away_from") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("on_top_of") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("after") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("f.") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("between") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("as_to") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("throughout") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("plus") and syntactic_label_data[0].split(':')[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("both") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("under") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("till") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("via") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("out") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("whilst") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("so") and syntactic_label_data[0].split(':')[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("behind") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("thru") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("andor") and syntactic_label_data[0].split(':')[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("compared_to") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("as_for") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("underneath") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("over") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("vs") and syntactic_label_data[0].split(':')[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("only") and syntactic_label_data[0].split(':')[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("instead_of") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("as_to") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("along") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("outside_of") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("next_to") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("besides") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("though") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("involving") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("negcc") and syntactic_label_data[0].split(':')[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("per") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("until") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("against") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("outside") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("as_if") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("against") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("versus") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("regardless_of") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("regarding") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("once") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("amid") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("outside") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("except") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("till") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("onto") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("around") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("except") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("a.") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("near") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("before") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("even") and syntactic_label_data[0].split(':')[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("that") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("from") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("below") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("other") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("given") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("inside_of") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("above") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("along") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("'") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("between") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("next_to") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("close_to") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("below") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("inside") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("either") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("aboard") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("such") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("in_case") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("across_from") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("pending") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("depending") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("if") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("next") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("within") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("rather_than") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("+") and syntactic_label_data[0].split(':')[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("apart_from") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("plus") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("de") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("or") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("worth") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("about") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("despite") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("based_on") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("vs.") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("by") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("not") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("since") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("not") and syntactic_label_data[0].split(':')[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("following") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("toward") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("despite") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("'s") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("through") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("ago") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("compared_with") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("inside") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("although") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("once") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("like") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("excluding") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("while") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("compared_to") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("towards") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("beginning") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("nor") and syntactic_label_data[0].split(':')[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("without") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("atop") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("after") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("whether") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("because") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("contrary_to") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("ta") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("beside") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("on_behalf_of") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("in_spite_of") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("due_to") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("_") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("since") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("including") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("based_on") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("in_addition_to") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("together_with") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("as") and syntactic_label_data[0].split(':')[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("_") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("based_on") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("along_with") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("past") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("just") and syntactic_label_data[0].split(':')[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("upon") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("oconer") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("and") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("at") and syntactic_label_data[0].split(':')[0].startswith('acl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("v.") and syntactic_label_data[0].split(':')[0].startswith('conj'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("among") and syntactic_label_data[0].split(':')[0].startswith('advcl'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]
                    elif syntactic_label_data[0].split(':')[1].startswith("unlike") and syntactic_label_data[0].split(':')[0].startswith('nmod'):
                        syntactic_label_data[0] = syntactic_label_data[0].split(':')[0]

                






                        
                        
                        
                        
                        
                        
                        
                        

                if syntactic_label_data[0].startswith('ref'):
                    syntactic_label_data[0] = 'nmod'
            """


                if syntactic_label_data[1] < len(entire_block):
                    entire_block[syntactic_label_data[1]][5] = str(syntactic_label_data[0])
                    entire_block[syntactic_label_data[1]][6] = str(syntactic_label_data[2])


            #Add entity types for all words

            for entity in sample['golden-entity-mentions']:

                wordIndex = entity['start']

                entity_type = ''
                entity_sub_type = ''
                sub = False

                for i, char in enumerate(entity['entity-type']):
                    if char == ':':
                        sub = True
                    else:
                        if sub == False:
                            entity_type = ((entity_type + '_') if char == '-' else (entity_type + str(char)))
                        if sub == True:
                            entity_sub_type = ((entity_sub_type + '_') if char == '-' else (entity_sub_type + str(char)))
                            if entity_sub_type.startswith("time"):
                                entity_sub_type = "Time"

                for i, B_I_O in enumerate(entity['text'].split()):
                    if i == 0:
                        entire_block[wordIndex][2] = "B-1_" + entity_type
                        entire_block[wordIndex][3] = "B-2_" + entity_sub_type
                    else:
                        entire_block[wordIndex + i][2] = "I-1_" + entity_type
                        entire_block[wordIndex + i][3] = "I-2_" + entity_sub_type


            #Add event type for all words

            for event in sample['golden-event-mentions']:

                wordIndex = event['trigger']['start']
                event_type = ''

                for i, char in enumerate(event['event_type']):
                    event_type = ((event_type + "_") if char == ':' or char == '-' else (event_type + str(char)))

                for i, B_I_O in enumerate(event['trigger']['text'].split()):
                    if i == 0:
                        entire_block[wordIndex][4] = "B-" + event_type
                    else:
                        entire_block[wordIndex + i][4] = "I-" + event_type


            #write data to output file

            for current_word in entire_block:
                for i, string_attribute in enumerate(current_word):
                    if i == 6:
                        if string_attribute == 'O':
                            g.write('-1')
                        else:
                            g.write(string_attribute)

                    else:
                        if string_attribute == 'O' and i == 5:
                            g.write('cc' + " ")
                        else:
                            g.write(string_attribute+" ")
                g.write("\n")
            g.write("\n")

    f.close()
    g.close()
    val = 133
    theNewLabels = ""
    for i in stringset:
        theNewLabels += ", '" + str(i) + "':" + str(val)
        val += 1
    print(theNewLabels)
        #print(f"elif syntactic_label_data[0].split(':')[1].startswith(\"{i.split(':')[1]}\") and syntactic_label_data[0].split(':')[0].startswith('{i.split(':')[0]}'):")
        #print("\tsyntactic_label_data[0] = syntactic_label_data[0].split(':')[0]")









if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='egnn for ed')

    parser.add_argument('inp', default="", type=str)
    parser.add_argument('out', default="", type=str)

    args = parser.parse_args()

    in_file = args.inp
    out_file = args.out

    main(in_file, out_file)