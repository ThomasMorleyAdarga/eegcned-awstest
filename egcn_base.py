import copy
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import pdb

entity_subtype_dict = {'O': 0, '2_Individual': 1, '2_Time': 2, '2_Group': 3, '2_Nation': 4,
                       '2_Indeterminate': 5, '2_Population_Center': 6, '2_Government': 7,
                       '2_Commercial': 8, '2_Non_Governmental': 9, '2_Media': 10, '2_Building_Grounds': 11,
                       '2_Numeric': 12, '2_State_or_Province': 13, '2_Region_General': 14, '2_Sports': 15,
                       '2_Crime': 16, '2_Land': 17, '2_Air': 18, '2_Water': 19, '2_Airport': 20,
                       '2_Sentence': 21, '2_Educational': 22, '2_Celestial': 23, '2_Underspecified': 24,
                       '2_Shooting': 25, '2_Special': 26, '2_Subarea_Facility': 27, '2_Path': 28,
                       '2_GPE_Cluster': 29, '2_Exploding': 30, '2_Water_Body': 31, '2_Land_Region_Natural': 32,
                       '2_Nuclear': 33, '2_Projectile': 34, '2_Region_International': 35, '2_Medical_Science': 36,
                       '2_Continent': 37, '2_Job_Title': 38, '2_County_or_District': 39, '2_Religious': 40,
                       '2_Contact_Info': 41, '2_Chemical': 42, '2_Subarea_Vehicle': 43, '2_Entertainment': 44,
                       '2_Biological': 45, '2_Boundary': 46, '2_Plant': 47, '2_Address': 48, '2_Sharp': 49,
                       '2_Blunt': 50
                       }
'''
dep_dict = {'O': 0, 'punct': 1, 'iobj': 2, 'parataxis': 3, 'auxpass': 4, 'aux': 5,
            'conj': 6, 'advcl': 7, 'acl:relcl': 8, 'nsubjpass': 9, 'csubj': 10, 'compound': 11,
            'compound:prt': 12, 'mwe': 13, 'cop': 14, 'neg': 15, 'nmod:poss': 16, 'appos': 17,
            'cc:preconj': 18, 'nmod': 19, 'nsubj': 20, 'xcomp': 21, 'det:predet': 22,
            'nmod:npmod': 23, 'acl': 24, 'amod': 25, 'expl': 26, 'csubjpass': 27, 'case': 28,
            'ccomp': 29, 'dobj': 30, 'ROOT': 31, 'discourse': 32, 'nmod:tmod': 33, 'dep': 34,
            'nummod': 35, 'mark': 36, 'advmod': 37, 'cc': 38, 'det': 39
            }
'''


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
            'nmod:beyond': 130, 'conj:in': 131, 'nmod:up': 132, 'nmod:atop': 133, 'advcl:once': 134,
            'nmod:beginning': 135, 'advcl:after': 136, 'nmod:past': 137, 'advcl:such': 138, 'nmod:vs.': 139,
            'advcl:behind': 140, 'nmod:inside_of': 141,
            'nmod:given': 142, 'acl:based_on': 143, 'nmod:plus': 144, 'nmod:onto': 145, 'nmod:\'': 146,
            'acl:before': 147, 'conj:just': 148, 'advcl:till': 149,
            'advcl:whilst': 150, 'nmod:in_front_of': 151, 'advcl:below': 152, 'nmod:oconer': 153,
            'nmod:away_from': 154, 'nmod:pending': 155, 'acl:compared_to': 156,
            'acl:until': 157, 'advcl:f.': 158, 'conj:+': 159, 'advcl:among': 160, 'advcl:through': 161,
            'acl:including': 162, 'nmod:together_with': 163, 'acl:because': 164,
            'conj:plus': 165, 'nmod:versus': 166, 'acl:next_to': 167, 'nmod:contrary_to': 168,
            'advcl:close_to': 169, 'advcl:around': 170, 'conj:andor': 171, 'conj:as': 172,
            'nmod:above': 173, 'nmod:while': 174, 'acl:between': 175, 'nmod:involving': 176, 'nmod:towards': 177,
            'acl:instead_of': 178, 'advcl:over': 179, 'nmod:regarding': 180,
            'nmod:despite': 181, 'nmod:next_to': 182, 'nmod:as_for': 183, 'nmod:besides': 184, 'advcl:toward': 185,
            'acl:about': 186, 'nmod:concerning': 187, 'advcl:instead_of': 188,
            'advcl:not': 189, 'conj:x': 190, 'conj:v.': 191, 'nmod:compared_with': 192, 'nmod:both': 193,
            'conj:even': 194, 'nmod:alongside': 195, 'nmod:beside': 196,
            'nmod:along': 197, 'advcl:though': 198, 'nmod:across_from': 199, 'nmod:aboard': 200,
            'nmod:on_behalf_of': 201, 'nmod:upon': 202, 'nmod:worth': 203, 'advcl:either': 204,
            'nmod:with_regard_to': 205, 'advcl:inside': 206, 'acl:besides': 207, 'nmod:throughout': 208,
            'nmod:as_of': 209, 'conj:vs': 210, 'nmod:amongst': 211,
            'nmod:considering': 212, 'nmod:next': 213, 'acl:at': 214, 'conj:only': 215, 'acl:from': 216,
            'nmod:regardless_of': 217, 'nmod:and': 218, 'nmod:excluding': 219,
            'advcl:compared_to': 220, 'acl:over': 221, 'advcl:_': 222, 'acl:after': 223, 'nmod:_': 224,
            'advcl:as_if': 225, 'conj:so': 226, 'advcl:ago': 227, 'advcl:depending': 228,
            'nmod:inside': 229, 'nmod:underneath': 230, 'nmod:via': 231, 'nmod:other': 232, 'advcl:although': 233,
            'nmod:off': 234, 'nmod:since': 235, 'advcl:abc': 236, 'nmod:beneath': 237,
            'advcl:rather_than': 238, 'nmod:outside': 239, 'nmod:either': 240, 'nmod:close_to': 241,
            'nmod:in_spite_of': 242, 'advcl:along': 243, 'acl:against': 244, 'nmod:along_with': 245,
            'advcl:under': 246, 'nmod:once': 247, 'nmod:per': 248, 'nmod:on_top_of': 249, 'nmod:amid': 250,
            'acl:without': 251, 'advcl:in_case': 252, 'acl:that': 253, 'nmod:as_to': 254, 'advcl:including': 255,
            'nmod:till': 256, 'acl:as_to': 257, 'advcl:\'s': 258, 'nmod:apart_from': 259, 'advcl:near': 260,
            'nmod:whether': 261, 'conj:not': 262, 'nmod:following': 263, 'acl:except': 264,
            'nmod:based_on': 265, 'nmod:in_addition_to': 266, 'acl:since': 267, 'advcl:ta': 268, 'acl:like': 269,
            'nmod:de': 270, 'nmod:outside_of': 271, 'advcl:based_on': 272, 'advcl:a.': 273,
            'nmod:or': 274, 'conj:negcc': 275, 'nmod:due_to': 276, 'advcl:except': 277, 'nmod:unlike': 278,
            'nmod:if': 279, 'acl:with': 280, 'nmod:below': 281, 'advcl:within': 282, 'advcl:outside': 283,
            'advcl:despite': 284,
            'conj:nor': 285, 'nmod:thru': 286, 'acl:by': 287, 'advcl:out_of': 288, 'advcl:out': 289,
            'nmod:in_case_of': 290, 'advcl:during': 291, 'advcl:from': 292, 'advcl:between': 293,
            'conj:versus': 294}



class EDModel(nn.Module):

    print(len(dep_dict))

    def __init__(self, args, id_to_tag, device, pre_word_embed):
        super(EDModel, self).__init__()

        self.device = device
        self.gcn_model = EEGCN(device, pre_word_embed, args)
        self.gcn_dim = args.gcn_dim
        self.classifier = nn.Linear(self.gcn_dim, len(id_to_tag))

    def forward(self, word_sequence, x_len, entity_type_sequence, adj, dep):
        outputs, weight_adj = self.gcn_model(word_sequence, x_len, entity_type_sequence, adj, dep)
        logits = self.classifier(outputs)
        return logits, weight_adj


class EEGCN(nn.Module):
    def __init__(self, device, pre_word_embeds, args):
        super().__init__()

        self.device = device
        self.in_dim = args.word_embed_dim + args.bio_embed_dim
        self.maxLen = args.num_steps

        self.rnn_hidden = args.rnn_hidden
        self.rnn_dropout = args.rnn_dropout
        self.rnn_layers = args.rnn_layers

        self.gcn_dropout = args.gcn_dropout
        self.num_layers = args.num_layers
        self.gcn_dim = args.gcn_dim

        # Word Embedding Layer
        self.word_embed_dim = args.word_embed_dim
        self.wembeddings = nn.Embedding.from_pretrained(torch.FloatTensor(pre_word_embeds), freeze=False)

        # Entity Label Embedding Layer
        self.bio_size = len(entity_subtype_dict)
        self.bio_embed_dim = args.bio_embed_dim
        if self.bio_embed_dim:
            self.bio_embeddings = nn.Embedding(num_embeddings=self.bio_size, embedding_dim=self.bio_embed_dim)


        self.dep_size = len(dep_dict)
        self.dep_embed_dim = args.dep_embed_dim
        self.edge_embeddings = nn.Embedding(num_embeddings=self.dep_size,
                                            embedding_dim=self.dep_embed_dim,
                                            padding_idx=0)

        self.rnn = nn.LSTM(self.in_dim, self.rnn_hidden, self.rnn_layers, batch_first=True, \
                           dropout=self.rnn_dropout, bidirectional=True)
        self.rnn_drop = nn.Dropout(self.rnn_dropout)  # use on last layer output

        self.input_W_G = nn.Linear(self.rnn_hidden * 2, self.gcn_dim)
        self.pooling = args.pooling
        self.gcn_layers = nn.ModuleList()
        self.gcn_drop = nn.Dropout(self.gcn_dropout)
        for i in range(self.num_layers):
            self.gcn_layers.append(
                GraphConvLayer(self.device, self.gcn_dim, self.dep_embed_dim, args.pooling))
        self.aggregate_W = nn.Linear(self.gcn_dim + self.num_layers * self.gcn_dim, self.gcn_dim)

    def encode_with_rnn(self, rnn_inputs, seq_lens, batch_size):
        # seq_lens = list(masks.data.eq(constant.PAD_ID).long().sum(1).squeeze())
        h0, c0 = rnn_zero_state(batch_size, self.rnn_hidden, self.rnn_layers)
        h0, c0 = h0.to(self.device), c0.to(self.device)
        rnn_inputs = nn.utils.rnn.pack_padded_sequence(rnn_inputs, seq_lens.to('cpu'), batch_first=True)
        rnn_outputs, (ht, ct) = self.rnn(rnn_inputs, (h0, c0))
        rnn_outputs, _ = nn.utils.rnn.pad_packed_sequence(rnn_outputs, batch_first=True)
        return rnn_outputs

    def forward(self, word_sequence, x_len, entity_type_sequence, adj, edge):

        BATCH_SIZE = word_sequence.shape[0]
        BATCH_MAX_LEN = x_len[0]  

        word_sequence = word_sequence[:, :BATCH_MAX_LEN].contiguous()
        adj = adj[:, :BATCH_MAX_LEN, :BATCH_MAX_LEN].contiguous()
        edge = edge[:, :BATCH_MAX_LEN, :BATCH_MAX_LEN].contiguous()
        weight_adj = self.edge_embeddings(edge)  # [batch, seq, seq, dim_e]

        word_emb = self.wembeddings(word_sequence)
        x_emb = word_emb
        if self.bio_embed_dim:
            entity_type_sequence = entity_type_sequence[:, :BATCH_MAX_LEN].contiguous()
            entity_label_emb = self.bio_embeddings(entity_type_sequence)
            x_emb = torch.cat([x_emb, entity_label_emb], dim=2)

        rnn_outputs = self.rnn_drop(self.encode_with_rnn(x_emb, x_len, BATCH_SIZE))
        gcn_inputs = self.input_W_G(rnn_outputs)
        gcn_outputs = gcn_inputs
        layer_list = [gcn_inputs]

        src_mask = (word_sequence != 0)
        src_mask = src_mask[:, :BATCH_MAX_LEN].unsqueeze(-2).contiguous()

        for _layer in range(self.num_layers):
            gcn_outputs, weight_adj = self.gcn_layers[_layer](weight_adj,gcn_outputs)  # [batch, seq, dim]
            gcn_outputs = self.gcn_drop(gcn_outputs)
            weight_adj = self.gcn_drop(weight_adj)
            layer_list.append(gcn_outputs)
        
        outputs = torch.cat(layer_list, dim=-1)
        aggregate_out = self.aggregate_W(outputs)
        return aggregate_out, weight_adj


class GraphConvLayer(nn.Module):
    """ A GCN module operated on dependency graphs. """

    def __init__(self, device, gcn_dim, dep_embed_dim, pooling='avg'):
        super(GraphConvLayer, self).__init__()

        self.gcn_dim = gcn_dim
        self.dep_embed_dim = dep_embed_dim
        self.device = device
        self.pooling = pooling

        self.W = nn.Linear(self.gcn_dim, self.gcn_dim)
        self.highway = Edgeupdate(gcn_dim, self.dep_embed_dim, dropout_ratio=0.5)

    def forward(self, weight_adj, gcn_inputs):
        """
        :param weight_adj: [batch, seq, seq, dim_e]
        :param gcn_inputs: [batch, seq, dim]
        :return:
        """
        batch, seq, dim = gcn_inputs.shape
        weight_adj = weight_adj.permute(0, 3, 1, 2)  # [batch, dim_e, seq, seq]

        gcn_inputs = gcn_inputs.unsqueeze(1).expand(batch, self.dep_embed_dim, seq, dim)
        Ax = torch.matmul(weight_adj, gcn_inputs)  # [batch, dim_e, seq, dim]
        if self.pooling == 'avg':
            Ax = Ax.mean(dim=1)
        elif self.pooling == 'max':
            Ax, _ = Ax.max(dim=1)
        elif self.pooling == 'sum':
            Ax = Ax.sum(dim=1)
        # Ax: [batch, seq, dim]
        gcn_outputs = self.W(Ax)
        weights_gcn_outputs = F.relu(gcn_outputs)

        node_outputs = weights_gcn_outputs
        # Edge update weight_adj[batch, dim_e, seq, seq]
        weight_adj = weight_adj.permute(0, 2, 3, 1).contiguous()  # [batch, seq, seq, dim_e]
        node_outputs1 = node_outputs.unsqueeze(1).expand(batch, seq, seq, dim)
        node_outputs2 = node_outputs1.permute(0, 2, 1, 3).contiguous()
        edge_outputs = self.highway(weight_adj, node_outputs1, node_outputs2)
        return node_outputs, edge_outputs


class Edgeupdate(nn.Module):
    def __init__(self, hidden_dim, dim_e, dropout_ratio=0.5):
        super(Edgeupdate, self).__init__()
        self.hidden_dim = hidden_dim
        self.dim_e = dim_e
        self.dropout = dropout_ratio
        self.W = nn.Linear(self.hidden_dim * 2 + self.dim_e, self.dim_e)

    def forward(self, edge, node1, node2):
        """
        :param edge: [batch, seq, seq, dim_e]
        :param node: [batch, seq, seq, dim]
        :return:
        """

        node = torch.cat([node1, node2], dim=-1) # [batch, seq, seq, dim * 2]
        edge = self.W(torch.cat([edge, node], dim=-1))
        return edge  # [batch, seq, seq, dim_e]


def rnn_zero_state(batch_size, hidden_dim, num_layers, bidirectional=True):
    total_layers = num_layers * 2 if bidirectional else num_layers
    state_shape = (total_layers, batch_size, hidden_dim)
    h0 = c0 = Variable(torch.zeros(*state_shape), requires_grad=False)
    return h0, c0


def clones(module, N):
    return nn.ModuleList([copy.deepcopy(module) for _ in range(N)])


