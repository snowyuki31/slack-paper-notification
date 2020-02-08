import json
import urllib.request
import datetime
import boto3

def lambda_handler(event, context):
    # TODO implement
    # Access to AWS SQS
    name = '**Your SQS name.fifo**' ##### FILL HERE!
    sqs = boto3.resource('sqs')
    try:
        queue = sqs.get_queue_by_name(QueueName=name)
    except:
        return {
            'statusCode': 500,
            'body': json.dumps('SQS_No_Exist')
        }

    # Fetch academic entities from Microsoft Academic   
    response_body = search_paper()

    # Form all entities into string messages and push them to SQS
    for e in response_body['entities']:
        message = "*Title* : {}\n*Journal* : {}\n*URL* : {}".format(e['Ti'],e['VFN'],e['S'][0]['U']) ## message style
        queue.send_message(MessageBody = message, MessageGroupId = 'group')

    # Pop one message out from SQS and send it to Slack
    messages = queue.receive_messages()
    if  len(messages) != 0:
        message = messages[0] ## How many items a day you need to be notified
        post_slack(message.body)
        message.delete()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

# Send POST request to WebHook
def post_slack(message):
    send_data = {
        "text" : message, ## setting for the Slack notifier
    }
    send_text = "payload=" + json.dumps(send_data)

    request = urllib.request.Request(
        "**WebHook URL**", ##### FILL HERE!
        data=send_text.encode('utf-8'),
        method="POST"
    )

    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode('utf-8')

# Search papers on Microsoft Academic beased on the given query and return its result
def search_paper():
    api_key = "**API KEY**" ##### FILL HERE!
    dt_now = str(datetime.date.today())
    query = "And(W='deep',W='learning',D='{}')".format(dt_now) ## Query for paper searching
    url = "https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?"+"expr="+query+"&attributes=Ti,S,VFN&count=20"

    request = urllib.request.Request(
        url,
        method="GET",
        headers={"Ocp-Apim-Subscription-Key" : api_key},
    )

    with urllib.request.urlopen(request) as response:
        response_body = json.loads(response.read().decode('utf-8'))

    return response_body
