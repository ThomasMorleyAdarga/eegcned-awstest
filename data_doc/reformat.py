import argparse
import json

def main(input, output):

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
                if sample['words'][i] == ' ':
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

                    if entire_block[wordIndex][2] == 'O' and entire_block[wordIndex] == '0':

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









if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='egnn for ed')

    parser.add_argument('inp', default="", type=str)
    parser.add_argument('out', default="", type=str)

    args = parser.parse_args()

    in_file = args.inp
    out_file = args.out

    main(in_file, out_file)