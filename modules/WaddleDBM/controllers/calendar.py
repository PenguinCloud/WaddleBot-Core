# -*- coding: utf-8 -*-
import json
import datetime
import threading
import requests
import time
import logging

# TODO: Get the below variables from a config file
matterbridgePostURL = 'http://localhost:4200/api/message'

stop_threads = False

# try something like
def index(): return dict(message="hello from calendar.py")

# Function to decode names with space in
def decode_name(name):
    if not name:
        return None
    name = name.replace("%20", " ")
    name = name.replace("_", " ")

    return name

# Function to get a routing_gateway channel_id from a given routing_gateway_id. If it doesnt exist, return null.
def get_channel_id(routing_gateway_id):
    routing_gateway = db(db.routing_gateways.id == routing_gateway_id).select().first()
    if not routing_gateway:
        return None
    return routing_gateway.channel_id

# Function to get the account as a combination of the protocol and the server name from a given routing_gateway_id. If it doesnt exist, return null.
def get_account(routing_gateway_id):
    routing_gateway = db(db.routing_gateways.id == routing_gateway_id).select().first()
    if not routing_gateway:
        return None
    gateway_server = db(db.gateway_servers.id == routing_gateway.gateway_server).select().first()
    if not gateway_server:
        return None
    return f"{gateway_server.protocol}.{gateway_server.name}"

# Create a new calender event from a given payload. Throws an error if no payload is given.
def create():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'community_name' not in payload or 'event_name' not in payload or 'event_description' not in payload or 'event_start' not in payload or 'event_end' not in payload:
        return dict(msg="Payload missing required fields.")
    # Get the community id from the community name
    community = db(db.communities.community_name == payload['community_name']).select().first()
    if not community:
        return dict(msg="Community not found. Please try again.")
    
    # Create the event
    db.calendar.insert(community_id=community.id, event_name=payload['event_name'], event_description=payload['event_description'], event_start=payload['event_start'], event_end=payload['event_end'], notification_sent=False)
    return dict(msg="Event created.")

# Get all calender events.
def get_all():
    events = db(db.calendar).select()
    return dict(data=events)

# Get a calender event by its name. If the event does not exist, return an error.
def get_by_name():
    event_name = request.args(0)
    event_name = decode_name(event_name)
    event = db(db.calendar.event_name == event_name).select().first()
    if not event:
        return dict(msg="Event not found.")
    return dict(data=event)

# Get calendar events by a community name and between a start and end date from a payload. Return an error if the community does not exist.
def get_by_community():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'community_name' not in payload:
        return dict(msg="The community_name value is missing.")
    community = db(db.communities.community_name == payload['community_name']).select().first()
    if not community:
        return dict(msg="Community not found.")
    
    # The start and end date are optional. The start date is the current date and the end date is the current date plus 30 days.
    start_date = datetime.datetime.now()
    end_date = start_date + datetime.timedelta(days=30)

    if 'start_date' in payload:
        start_date = payload['start_date']
    if 'end_date' in payload:
        end_date = payload['end_date']

    events = db((db.calendar.community_id == community.id) & (db.calendar.event_start >= start_date) & (db.calendar.event_start <= end_date)).select()
    return dict(data=events)

# Update a calendar event by its event name and community name. If the event does not exist, return an error.
def update_by_name():
    event_name = request.args(0)
    event_name = decode_name(event_name)
    event = db(db.calendar.event_name == event_name).select().first()
    if not event:
        return dict(msg="Event not found.")
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    
    if 'community_name' not in payload:
        return dict(msg="The community name has not been provided.")
    # Get the community id from the community name
    community = db(db.communities.community_name == payload['community_name']).select().first()

    if community:
        event.community_id = community.id
    else:
        return dict(msg="Community not found.")
    if 'event_name' in payload:
        event.event_name = payload['event_name']
    if 'event_description' in payload:
        event.event_description = payload['event_description']
    if 'event_start' in payload:
        event.event_start = payload['event_start']
    if 'event_end' in payload:
        event.event_end = payload['event_end']
    event.update_record()
    return dict(msg="Event updated.")

# Delete a calendar event by its name and community name in a payload. If the event does not exist, return an error.
def delete_by_name():
    payload = request.body.read()
    if not payload:
        return dict(msg="No payload given.")
    payload = json.loads(payload)
    if 'community_name' not in payload or 'event_name' not in payload:
        return dict(msg="The community name or event_name has not been provided.")
    
    event_name = payload['event_name']
    event = db(db.calendar.event_name == event_name).select().first()
    if not event:
        return dict(msg="Event not found.")
    # Get the community id from the community name
    community = db(db.communities.community_name == payload['community_name']).select().first()
    if not community:
        return dict(msg="Community not found.")
    if event.community_id == community.id:
        event.delete_record()
        return dict(msg="Event deleted.")
    else:
        return dict(msg="Event not found.")
    
# A loop function to check if an event is starting in 30 minutes. If it is, send a message to the Matterbridge.
def check_events_start():
    print("Starting calendar event check loop.")
    while True:
        print("Checking for events.")
        events = db(db.calendar).select()
        if events:
            print("Events found. Checking if any events are starting in 30 minutes.")
            for event in events:
                if (event.event_start - datetime.timedelta(minutes=30) <= datetime.datetime.now() <= event.event_start) and event.not_start_sent == False:
                    event_name = event.event_name

                    # Using the event's community id, get the community name
                    community = db(db.communities.id == event.community_id).select().first()
                    if not community:
                        logging.error("Community not found. The given community must have been deleted.")
                        continue
                    
                    # In the routing table, get the routing_gateway_ids for the given community id. If the routing_gateway_ids list is empty, return an error.
                    routings = db(db.routing.community_id == community.id).select().first()

                    if not routings:
                        logging.error("No routings found for the current community.")
                        continue
                    
                    # Get the channel_id and account from the routing_gateway_ids
                    channel_ids = []
                    accounts = []
                    if len(routings.routing_gateway_ids) == 0:
                        logging.error("No routing gateways found for the current community. Unable to send a message.")
                        continue
                    
                    for routing_gateway_id in routings.routing_gateway_ids:
                        channel_id = get_channel_id(routing_gateway_id)
                        account = get_account(routing_gateway_id)
                        if channel_id and account:
                            channel_ids.append(channel_id)
                            accounts.append(account)

                    # Send a message to the Matterbridge for each channel_id and account
                    for channel_id, account in zip(channel_ids, accounts):
                        try:
                            message = f"Event {event_name} is starting in 30 minutes."
                            payload = {
                                "username": "Waddle Bot",
                                "gateway": channel_id,
                                "account": account,
                                "text": message
                            }
                            requests.post(matterbridgePostURL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
                        except Exception as e:
                            logging.error(f"Error sending message to Matterbridge: {e}")
                    
                    print(f"Event {event_name} is starting in 30 minutes. Messages sent to the Matterbridge.")

                    # Update the notification sent field in the event record
                    event.update_record(not_start_sent=True)

                    db.commit()

            if stop_threads:
                break
        # Sleep for 1 minute
        time.sleep(60)

# A loop function to check if an event has ended. If it has, send a message to the Matterbridge.
def check_events_end():
    print("Starting calendar event check loop.")
    while True:
        print("Checking for events.")
        events = db(db.calendar).select()
        if events:
            print("Events found. Checking if any events are ending.")
            for event in events:
                if event.event_end >= datetime.datetime.now() and event.not_end_sent == False:
                    event_name = event.event_name

                    # Using the event's community id, get the community name
                    community = db(db.communities.id == event.community_id).select().first()
                    if not community:
                        logging.error("Community not found. The given community must have been deleted.")
                        continue
                    
                    # In the routing table, get the routing_gateway_ids for the given community id. If the routing_gateway_ids list is empty, return an error.
                    routings = db(db.routing.community_id == community.id).select().first()

                    if not routings:
                        logging.error("No routings found for the current community.")
                        continue
                    
                    # Get the channel_id and account from the routing_gateway_ids
                    channel_ids = []
                    accounts = []
                    if len(routings.routing_gateway_ids) == 0:
                        logging.error("No routing gateways found for the current community. Unable to send a message.")
                        continue
                    
                    for routing_gateway_id in routings.routing_gateway_ids:
                        channel_id = get_channel_id(routing_gateway_id)
                        account = get_account(routing_gateway_id)
                        if channel_id and account:
                            channel_ids.append(channel_id)
                            accounts.append(account)

                    # Send a message to the Matterbridge for each channel_id and account
                    for channel_id, account in zip(channel_ids, accounts):
                        try:
                            message = f"Event {event_name} is ending."
                            payload = {
                                "username": "Waddle Bot",
                                "gateway": channel_id,
                                "account": account,
                                "text": message
                            }
                            requests.post(matterbridgePostURL, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
                        except Exception as e:
                            logging.error(f"Error sending message to Matterbridge: {e}")
                    
                    print(f"Event {event_name} is ending. Messages sent to the Matterbridge.")

                    # Update the notification sent field in the event record
                    event.update_record(not_end_sent=True)

                    db.commit()

            if stop_threads:
                break

        # Sleep for 1 minute
        time.sleep(60)

# Function to start the check_events loop in a new thread.
def start_event_check():
    event_start_check_thread = threading.Thread(target=check_events_start)
    event_start_check_thread.start()

    event_end_check_thread = threading.Thread(target=check_events_end)
    event_end_check_thread.start()

    return dict(msg="Event check loop started.")


# # Function to stop the check_events loop.
# def stop_event_check():
#     stop_threads = True
#     event_check_thread.join()
    
#     print('thread killed')

#     return dict(msg="Event check loop stopped.")
