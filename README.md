# Paper Notification Tool working on AWS Lambda

This is a function for AWS lambda to search new papers everyday on Microsoft Academic, fetch them to AWS SQS and send notifications to Slack.

For detail, please refer to this page https://qiita.com/snowyuki31/items/5c46b7870f2ae6958973 (Japanese)

# What you must add to the code (##### FILL HERE! )

1. FIFO queue name on AWS SQS

2. WebHook URL on your Slack

3. API KEY for Academic Knowledge API / Academic Search API

# What you might want to change in the code (## ~~~~ )

1. Messaging style

2. Frequency of notifications

3. Setting for the Slack notifier

4. Query for searching paper
