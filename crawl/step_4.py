import os
import json

MIN_DUPLICATE_PERCENT = 0.3


def clean_duplicate_data(path_file):
    f = open(path_file)
    data = json.load(f)
    list_prompt = data['prompt']
    list_image_src = data['image_src']

    list_clean_prompt = [list_prompt[0]]
    list_clean_image_src = [list_image_src[0]]

    for index, prompt in enumerate(list_prompt):
        if index == 0:
            continue

        flag = False
        for clean_prompt in list_clean_prompt:
            if calculate_duplicate(prompt, clean_prompt) >= MIN_DUPLICATE_PERCENT:
                flag = True
                break

        if flag:
            continue
        else:
            list_clean_prompt.append(list_prompt[index])
            list_clean_image_src.append(list_image_src[index])

        if index % 1000 == 0:
            print(index, len(list_clean_prompt))

    result = {'prompt': list_clean_prompt, 'image_src': list_clean_image_src}
    return result


def calculate_duplicate(sen1, sen2):
    list1 = sen1.split()
    list2 = sen2.split()

    count = 0
    for (word1, word2) in zip(list1, list2):
        if word1 == word2:
            count += 1

    duplicate_percent = count / (len(list2) + 1)
    return round(duplicate_percent, 3)


if __name__ == '__main__':
    for _file in os.listdir('crawl/parse_data'):
        clean_result = clean_duplicate_data(f"crawl/parse_data/{_file}")

        if not os.path.exists('crawl/clean_data'):
            os.mkdir('crawl/clean_data')

        with open(f"crawl/clean_data/{_file}", "w") as outfile:
            outfile.write(json.dumps(clean_result))
