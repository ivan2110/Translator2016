import re
import xml.etree.ElementTree as ET
import sys
import os

src_lang_prefix = sys.argv[1]
dst_lang_prefix = sys.argv[2]

def process_word(word):
    #regular expression: 3 variants
    #1 (letters or digits more then 1)
    #2 (one letter/digit)
    #3 (no letters/digits)
    pattern = r'^\W*(\w[\w\W]*\w)\W*$|^\W*(\w)\W*$|^(\W*)$'
    pair_words = re.findall(pattern, word.decode('utf-8'), re.U)[0]
    word_without_extra_symbols = pair_words[0] if pair_words[0] != "" \
        else pair_words[1] if pair_words[1] != "" else pair_words[2]
    return word_without_extra_symbols.lower()


def process_sentence(sentence, natural_sentences_file, indexes_sentences_file, mapping_file, mapping, last_index):
    formattedSentence = sentence.replace("\n", " ")
    natural_sentences_file.write(formattedSentence + "\n")
    words = map(process_word, formattedSentence.split())
    for word in words:
        if mapping.has_key(word) == False:
            last_index += 1
            mapping[word] =last_index
            mapping_file.write(word.encode('utf-8') + '\n')
    indexes = map(lambda word: mapping[word], words)
    map(lambda index: indexes_sentences_file.write(str(index) + " "), indexes)
    indexes_sentences_file.write("\n")
    return last_index


def process_corpus(corpus_file_name, threshold_alignment_values,
                   src_language_natural_sentences_file, dst_language_natural_sentences_file,
                   src_language_indexes_sentences_file, dst_language_indexes_sentences_file,
                   src_language_mapping_file, dst_language_mapping_file,
                   src_language_mapping, dst_language_mapping,
                   src_language_last_index, dst_language_last_index):

    tree = ET.parse(corpus_file_name)
    corpus = tree.getroot()

    current_quality = 1.0
    for aligned_sentence in corpus:
        if current_quality < threshold_alignment_values:
            break
        for attribute in aligned_sentence:
            if attribute.tag == "first_lang_sentence":
                src_language_last_index = process_sentence(attribute.text.encode("utf-8"),
                                 src_language_natural_sentences_file, src_language_indexes_sentences_file,
                                 src_language_mapping_file, src_language_mapping, src_language_last_index)
            elif attribute.tag == "second_lang_sentence":
                dst_language_last_index = process_sentence(attribute.text.encode("utf-8"),
                                 dst_language_natural_sentences_file, dst_language_indexes_sentences_file,
                                 dst_language_mapping_file, dst_language_mapping, dst_language_last_index)
            elif attribute.tag == "alignment_values":
                current_quality = attribute.text.encode("utf-8")
            else:
                print "Warning!"
    return (src_language_last_index, dst_language_last_index)


forward_corpus_file_name = src_lang_prefix + "_" + dst_lang_prefix + ".xml"
backward_corpus_file_name= dst_lang_prefix + "_" + src_lang_prefix + ".xml"

thr_alignment_value = 0.1

src_lang_natural_sentences_file_name = src_lang_prefix + "_natural_sentences.txt"
dst_lang_natural_sentences_file_name = dst_lang_prefix + "_natural_sentences.txt"
src_lang_natural_sentences_file = open(src_lang_natural_sentences_file_name, "w")
dst_lang_natural_sentences_file = open(dst_lang_natural_sentences_file_name, "w")

src_lang_indexes_sentences_file_name = src_lang_prefix + "_indexes_sentences.txt"
dst_lang_indexes_sentences_file_name = dst_lang_prefix + "_indexes_sentences.txt"
src_lang_indexes_sentences_file = open(src_lang_indexes_sentences_file_name, "w")
dst_lang_indexes_sentences_file = open(dst_lang_indexes_sentences_file_name, "w")

src_lang_mapping_file_name = src_lang_prefix + "_mapping.txt"
dst_lang_mapping_file_name = dst_lang_prefix + "_mapping.txt"
src_lang_mapping_file = open(src_lang_mapping_file_name, "w")
dst_lang_mapping_file = open(dst_lang_mapping_file_name, "w")

#Map((word, index))
src_lang_mapping = {}
dst_lang_mapping = {}
src_lang_last_index = -1
dst_lang_last_index = -1

(src_lang_last_index, dst_lang_last_index) = process_corpus(forward_corpus_file_name, thr_alignment_value,
                   src_lang_natural_sentences_file, dst_lang_natural_sentences_file,
                   src_lang_indexes_sentences_file, dst_lang_indexes_sentences_file,
                   src_lang_mapping_file, dst_lang_mapping_file,
                   src_lang_mapping, dst_lang_mapping,
                   src_lang_last_index, dst_lang_last_index)

(dst_lang_last_index, src_lang_last_index) = process_corpus(backward_corpus_file_name, thr_alignment_value,
                   dst_lang_natural_sentences_file, src_lang_natural_sentences_file,
                   dst_lang_indexes_sentences_file, src_lang_indexes_sentences_file,
                   dst_lang_mapping_file, src_lang_mapping_file,
                   dst_lang_mapping, src_lang_mapping,
                   dst_lang_last_index, src_lang_last_index)



src_lang_natural_sentences_file.close()
dst_lang_natural_sentences_file.close()

src_lang_indexes_sentences_file.close()
dst_lang_indexes_sentences_file.close()

src_lang_mapping_file.close()
dst_lang_mapping_file.close()

os.rename(src_lang_prefix + "_mapping.txt", src_lang_prefix + "_mapping" + str(src_lang_last_index + 1) + ".txt")
os.rename(dst_lang_prefix + "_mapping.txt", dst_lang_prefix + "_mapping" + str(dst_lang_last_index + 1) + ".txt")