#!/usr/bin/env python3
from bs4 import BeautifulSoup
from typing import Dict, List
import subprocess
import requests
import sys
import os


URL = "https://stackoverflow.com"


# Disclaimer: ColorPrint copied directly from Stackoverflow. ¯\_(ツ)_/¯
class ColorPrint:

    @staticmethod
    def print_title(message, end = "\n"):
        sys.stdout.write('\x1b[1;34m' + message + '\x1b[0m' + end)
    
    @staticmethod
    def print_fail(message, end = '\n'):
        sys.stderr.write('\x1b[1;31m' + message + '\x1b[0m' + end)

    @staticmethod
    def print_pass(message, end = '\n'):
        sys.stdout.write('\x1b[1;32m' + message + '\x1b[0m' + end)

    @staticmethod
    def print_warn(message, end = '\n'):
        sys.stderr.write('\x1b[1;33m' + message + '\x1b[0m' + end)

    @staticmethod
    def print_info(message, end = '\n'):
        sys.stdout.write('\x1b[1;34m' + message + '\x1b[0m' + end)

    @staticmethod
    def print_bold(message, end = '\n'):
        sys.stdout.write('\x1b[1;37m' + message + '\x1b[0m' + end)


def print_header():
    # Just print the header and exit

    ColorPrint.print_title("""
    ________    _____             ______      ________                _____ 
    __  ___/    __  /______ _________  /__    ___  __/  ______ _________  /_
    _____ \     _  __/  __ `/  ___/_  //_/    __  /_    _  __ `/_  ___/  __/
    ____/ /     / /_ / /_/ // /__ _  ,<       _  __/    / /_/ /_(__  )/ /_  
    /____/      \__/ \__,_/ \___/ /_/|_|      /_/       \__,_/ /____/ \__/  
   // Ask stackoverflow fast.. ♫                                        v0.1  ( We need some kind of version ¯\_(ツ)_/¯ )
    """)



def display_post_discussion(question_data: Dict[str, str]) -> None:
    # get's the question_data dict parse and display the post discussion.

    print()
    ColorPrint.print_fail("QUESTION: [" + question_data["question"] + "]")
    question_full_input = requests.get(URL + question_data["url"])
    data = BeautifulSoup(question_full_input.text, "html.parser")
    print(data.find(name="div", attrs={"class": "post-text"}).text)
    ColorPrint.print_pass("ANSWERS: ")
    ColorPrint.print_warn("=======================================")
    for idx, answer in enumerate(data.find_all(name="div", attrs={"class": "post-text"})[1:]):
        print(f"Answer #{idx + 1}\n{answer.text.strip()}")
        ColorPrint.print_warn("=======================================")


def dig_top_matched_simillar_questions(question: str) -> List[Dict[str, str]]:
    # dig stackoverflow page by the user input question and find the most relevant 
    # questions.
    # // input: question.
    # // return: list of dicts e.g [{url: "xxx", question: "zzz"}]

    data = requests.get(URL + "/search?tab=relevance&q=" + question)
    soup = BeautifulSoup(data.text, 'html.parser')
    questions = []
    for item in soup.find_all(name="div", class_="result-link"):
        try:
            url = (
                str(item).split("href=")[1]
                         .split(" title")[0]
                         .strip()
                         .replace('"', "")
                         .replace("?r=SearchResults", "")
            )
            question = item.text.strip().replace("Q: ", "").replace("A:", "").strip()
            questions.append(
                {"url": url, "question": question}
            )
        except:
            pass
    return questions


def display_questions(questions: List[Dict[str, str]]) -> None:
    # display the questions found in a menu like format.

    print()
    ColorPrint.print_bold("[ / PICK CLOSEST MATCH / ]")
    ColorPrint.print_bold("------------------------------------------")
    for idx, question in enumerate(questions):
        if idx % 2 == 0:
            ColorPrint.print_info(f"{idx + 1}) {question['question']}")
        else:
            ColorPrint.print_warn(f"{idx + 1}) {question['question']}")
        ColorPrint.print_bold("------------------------------------------")
    ColorPrint.print_fail("`gbmm`") 
    ColorPrint.print_pass("   to go back to main menu and change your question..")


def input_parser() -> str:
    # dummy parser to be catch the user question.
    # // return: str

    try:
        question = input('\x1b[0;32m' + "Q: >> " + '\x1b[0m')
        if not question:
            return ""
        if "exit" == question.lower():
            sys.exit(1)
        return question
    except:
        return ""


def clean_screen():
    # clean screen for better look at the terminal.

    subprocess.call('clear', shell=True)


def display_questions_pickup_menu_screen(questions: List[Dict[str, str]]) -> None:
    # menu screen to handle selected questions from inside the menu, till the user exit.
    # // input: questions e.g [{"url": "", "question": ""}]

    while True:
        clean_screen()
        display_questions(questions)
        answer = input('\x1b[0;32m' + "#No : >> " + '\x1b[0m')
        clean_screen()
        if "gbmm" in answer.lower():
            print_header()
            break

        try:
            ans = int(answer)
            if ans > len(questions):
                clean_screen()
                ColorPrint.print_fail("Unknown Question #NO")
            else:
                display_post_discussion(questions[ans - 1])
                input('\x1b[0;32m' + "Go back (Enter)" + '\x1b[0m')
        except:
            pass


if __name__ == '__main__':

    print_header()
    while True:
        question = input_parser()
        if not question: continue
        try:
            questions = dig_top_matched_simillar_questions(question)
            if questions:
                display_questions_pickup_menu_screen(questions)
                clean_screen()
                print_header()
            else:
                ColorPrint.print_warn("  No results found, try to rewrite your question.")
        except Exception as e:
            raise e
