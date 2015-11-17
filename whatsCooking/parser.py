
import json
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


def stem_tokens(tokens):
    stemmed = []
    for item in tokens:
        # stemmed.append(stemmer.stem(item))
        stemmed.append(lemmatizer.lemmatize(item))
    return stemmed


def tokenize_and_stem(text):
    tokens = word_tokenize(text)
    return stem_tokens(tokens)


def convert_entry_to_csv(json_entry, training_data=True):
    res = ""
    if training_data:
        res = json_entry["cuisine"] + ","

    # Default text as features
    # ingredients = [x.encode('ascii', 'ignore').lower().replace(" ", "_") for x in json_entry["ingredients"]]

    # Tokenizing and Stemming
    ingredients = ["_".join(tokenize_and_stem(x.encode('ascii', 'ignore').lower())) for x in json_entry["ingredients"]]

    # ADDED FEATURES
    # res += "," + str(len(ingredients))
    # if "onion" in res:
    #     res += "," + "has_onion"
    # if "salt" in res:
    #     res += "," + "has_salt"
    # if len(ingredients) > 6:
    #     res += "," + "more_than_6_ingredients"
    # if "tomatoes" in res:
    #     res += "," + "has_tomatoes"

    res += ",".join(ingredients)

    return res


def create_csv_and_vw_from_json_file(file_path, ret_csv_data, ret_vw_data, mapping, training_data=True):
    with open(file_path, 'r') as inp:
        data = json.load(inp)

    classes = 1
    for entry in data:
        if training_data:
            if entry["cuisine"] not in mapping:
                mapping[entry["cuisine"]] = classes
                classes += 1

        entry_csv = convert_entry_to_csv(entry, training_data)
        ret_csv_data.append(entry_csv)
        entry_vw = ""
        if training_data:
            entry_vw = str(mapping[entry["cuisine"]]) + " 1 " + entry["cuisine"] + "|f "
        else:
            entry_vw = "1 1|f "
        features = entry_csv.split(",")
        if training_data:
            features.pop(0)
        entry_vw += " ".join(features)
        ret_vw_data.append(entry_vw)


def write_list_to_file(file_path, _list):
    with open(file_path, 'w') as out:
        for entry in _list:
            out.write(entry)
            out.write("\n")


def redefine_data_using_mapping(out_file, in_csv_data, mapping):
    with open(out_file, 'w') as out:
        for entry in in_csv_data:
            out.write(str(mapping[entry.split(",")[0]]) + " " + entry.split(",")[0])
            out.write("\n")


def generate_training_data():
    write_list_to_file(out_train_vw_file_path, vw_data)
    write_list_to_file(out_train_csv_file_path, csv_data)
    redefine_data_using_mapping(out_train_truth_file_path, csv_data, classes_mapping)


def generate_testing_data():
    write_list_to_file(out_test_vw_file_path, vw_data)
    write_list_to_file(out_test_csv_file_path, csv_data)
    write_list_to_file(out_test_classes_mapping_file_path, classes_mapping)


def generate_submission_data(mapping):
    inv_map = {v: k for k, v in mapping.items()}
    with open(in_test_json_file_path, 'r') as inp:
        data = json.load(inp)
    i = 0
    with open(in_predictions_file_path, 'r') as inp:
        with open(out_submission_data_file_path, 'w') as out:
            out.write("id,cuisine\n")
            for line in inp:
                out.write(str(data[i]["id"]) + "," + inv_map[int(line.split(" ")[0])] + "\n")
                i += 1

in_train_json_file_path = "D:\\vm\\shared\\kaggle\\whatsCooking\\train.json"
out_train_csv_file_path = "D:\\vm\\shared\\kaggle\\whatsCooking\\train.csv"
out_train_vw_file_path = "D:\\vm\\shared\\kaggle\\whatsCooking\\train.vw"
out_train_truth_file_path = "D:\\vm\\shared\\kaggle\\whatsCooking\\train.truth"

in_test_json_file_path = "D:\\vm\\shared\\kaggle\\whatsCooking\\test.json"
out_test_csv_file_path = "D:\\vm\\shared\\kaggle\\whatsCooking\\test.csv"
out_test_vw_file_path = "D:\\vm\\shared\\kaggle\\whatsCooking\\test.vw"
out_test_classes_mapping_file_path = "D:\\vm\\shared\\kaggle\\whatsCooking\\test.mapping"

in_predictions_file_path = "D:\\vm\\shared\\kaggle\\whatsCooking\\test"
out_submission_data_file_path = "D:\\vm\\shared\\kaggle\\whatsCooking\\submission.csv"

generateTrainingAndTestingData = False
generateSubmissionData = True

classes_mapping = {}

csv_data = []
vw_data = []
create_csv_and_vw_from_json_file(in_train_json_file_path, csv_data, vw_data, classes_mapping)
if generateTrainingAndTestingData:
    print "Generating training data"
    generate_training_data()

csv_data = []
vw_data = []
create_csv_and_vw_from_json_file(in_test_json_file_path, csv_data, vw_data, classes_mapping, False)
if generateTrainingAndTestingData:
    print "Generating testing data"
    generate_testing_data()

if generateSubmissionData:
    print "Generating submission data"
    generate_submission_data(classes_mapping)















