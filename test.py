""" test python script for git module """

import controllers.controller_openai
import tools.git as git
from controllers.controller_openai import CodeReview


file_feedback = {}
i = 0
for file in git.iterate_files("."):
    print(file)
    if file.endswith(".py"):
        with open(file) as f:
            text = f.read()
            file_feedback[file] = controllers.controller_openai.code_review_chat(text)["choices"][0]["message"]["content"]  # type: ignore
            #file_summaries[file] = controllers.controller_openai.code_review_file_summary(text)["choices"][0]["message"]["content"]  # type: ignore
            i += 1
            if i == 3:
                break

all_summaries = ""
for file in file_feedback:
    all_summaries += file_feedback[file]

print("-----------------")
print("below is an overall summary of all files")
print("-----------------")
print(controllers.controller_openai.code_review_summary(text)["choices"][0]["message"]["content"])  # type: ignore

print("-----------------")
print("-----------------")

for file in file_feedback:
    print(file)
    print("-----------------")
    print(file_feedback[file])
    print("-----------------")


# code_review_chat = CodeReview()
# for file in git.iterate_files("."):
#    print(file)
#    if file.endswith(".py"):
#        with open(file) as f:
#            text = f.read()
#            code_review_chat.code_review_completion(text)
