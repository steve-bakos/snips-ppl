#!/usr/bin/env python2
# -*-: coding utf-8 -*-

from hermes_python.hermes import Hermes
import json

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


INTENT_ENTRY_CREDIT_CARD_PROBLEM = "AIHub:entry_credit_card_problem"
INTENT_CREDIT_CARD_PROBLEM_STAGE_2_FAILED = "AIHub:credit_card_problem_lvl2_failed"
INTENT_CREDIT_CARD_PROBLEM_STAGE_2_WORKED = "AIHub:credit_card_problem_lvl2_worked"
INTENT_QUIT = "AIHub:Quit"
# INTENT_INTERRUPT = "interrupt"
# INTENT_DOES_NOT_KNOW = "does_not_know"

INTENT_FILTER_GET_RESPONSE = [
    INTENT_CREDIT_CARD_PROBLEM_STAGE_2_FAILED,
    INTENT_CREDIT_CARD_PROBLEM_STAGE_2_WORKED,
    INTENT_QUIT
]

SessionsStates = {}

CURRENT_LEVEL = 0

def write_to_file(sentence):
    with open('/var/lib/snips/skills/snips-ppl/voice_message.txt', 'w') as f:
        f.write(sentence) 

def user_starts_entry_card_problem(hermes, intent_message):
    global CURRENT_LEVEL

    CURRENT_LEVEL = 1
    sentence = "Try again with the black stripe facing the ground on the right."
    write_to_file(sentence)
    hermes.publish_continue_session(intent_message.session_id, sentence, INTENT_FILTER_GET_RESPONSE)

def user_starts_entry_card_problem_stage_2_failed(hermes, intent_message):
    global CURRENT_LEVEL

    if CURRENT_LEVEL == 1:
        sentence = "Check that the back of your card is clean."
        write_to_file(sentence)
        hermes.publish_continue_session(intent_message.session_id, sentence, INTENT_FILTER_GET_RESPONSE)
    else:
    	sentence = "You must access stage one first."
    	write_to_file(sentence)
    	hermes.publish_end_session(intent_message.session_id, sentence)

def user_starts_entry_card_problem_stage_2_worked(hermes, intent_message):
    global CURRENT_LEVEL

    if CURRENT_LEVEL == 1:
        sentence = "Press the green button and the gate will open."
        write_to_file(sentence)
        hermes.publish_end_session(intent_message.session_id, sentence)
        CURRENT_LEVEL = 0
    else:
        sentence = "You must access stage one first."
        write_to_file(sentence)
        hermes.publish_end_session(intent_message.session_id, sentence)

def quit(hermes, intent_message):
    sentence = "Shutting down."
    hermes.publish_end_session(intent_message.session_id, sentence)

def session_started(hermes, session_started_message):
    print("Session Started")

    print("sessionID: {}".format(session_started_message.session_id))
    print("session site ID: {}".format(session_started_message.site_id))
    print("sessionID: {}".format(session_started_message.custom_data))

    session_id = session_started_message.session_id

def session_ended(hermes, session_ended_message):
    print("Session Ended")
    session_id = session_ended_message.session_id
    session_site_id = session_ended_message.site_id

    if SessionsStates.get(session_id) is not None:
        hermes.publish_start_session_action(site_id=session_site_id,
                                            session_init_text="",
                                            session_init_intent_filter=INTENT_FILTER_GET_RESPONSE,
                                            session_init_can_be_enqueued=False,
                                            custom_data=session_id)

with Hermes(MQTT_ADDR) as h:

    h.subscribe_intent(INTENT_ENTRY_CREDIT_CARD_PROBLEM, user_starts_entry_card_problem) \
        .subscribe_intent(INTENT_QUIT, quit) \
        .subscribe_intent(INTENT_CREDIT_CARD_PROBLEM_STAGE_2_FAILED, user_starts_entry_card_problem_stage_2_failed) \
        .subscribe_intent(INTENT_CREDIT_CARD_PROBLEM_STAGE_2_WORKED, user_starts_entry_card_problem_stage_2_worked) \
        .subscribe_session_ended(session_ended) \
        .subscribe_session_started(session_started) \
        .start()
