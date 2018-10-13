#!/usr/bin/env python2
# -*-: coding utf-8 -*-

from hermes_python.hermes import Hermes
import json

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))


INTENT_ENTRY_CREDIT_CARD_PROBLEM = "AIHub:EntryCreditCardProblem"
INTENT_CREDIT_CARD_PROBLEM_STAGE_2 = "AIHub:CreditCardProblemStage2"
# INTENT_INTERRUPT = "interrupt"
# INTENT_DOES_NOT_KNOW = "does_not_know"

INTENT_FILTER_GET_RESPONSE = [
    INTENT_CREDIT_CARD_PROBLEM_STAGE_2
]

SessionsStates = {}

def user_starts_entry_card_problem(hermes, intent_message):
    print("User has a card problem.")

    sentence = "Try again with the black stripe facing the ground on the right."

    hermes.publish_continue_session(intent_message.session_id, sentence, INTENT_FILTER_GET_RESPONSE)

def user_starts_entry_card_problem_stage_2(hermes, intent_message):
    print("User has a card problem stage 2.")

    sentence = "Check that the back of your card is clean."
    hermes.publish_end_session(intent_message.session_id, sentence)

def session_started(hermes, session_started_message):
    print("Session Started")

    print("sessionID: {}".format(session_started_message.session_id))
    print("session site ID: {}".format(session_started_message.site_id))
    print("sessionID: {}".format(session_started_message.custom_data))

    session_id = session_started_message.session_id
    custom_data = session_started_message.custom_data

    if custom_data:
        if SessionsStates.get(custom_data):
            SessionsStates[session_id] = SessionsStates[custom_data]
            SessionsStates.pop(custom_data)

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
        .subscribe_intent(INTENT_CREDIT_CARD_PROBLEM_STAGE_2, user_starts_entry_card_problem_stage_2) \
        .subscribe_session_ended(session_ended) \
        .subscribe_session_started(session_started) \
        .start()