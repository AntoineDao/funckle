import React from 'react'

import { Card, Col, Row } from 'antd'
import { ReactMarkdown } from 'react-markdown/lib/react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { dracula } from 'react-syntax-highlighter/dist/esm/styles/prism'

const Index = () => {

    const introText = `
# Welcome to Funckle: Your Automation Bot Repository for Speckle Streams

# ✨ ❤️ 🤖

Welcome to Funckle, your go-to platform for creating, sharing, and deploying automation bots that interact with Speckle Streams. Funckle empowers you to automate tasks and processes by utilizing a wide range of reusable functions. This guide will help you get started with Funckle, from signing up to deploying your first bot.

## Table of Contents
* What is Funckle?
* Getting Started
  * Signing Up
  * Exploring the Dashboard
* Creating Your First Bot
  * Choosing a Function
  * Deploying Your First Bot 🤖
* Managing Your Bots
  * Debugging Bots
  * Updating and Deleting Bots
* Creating Your Own Functions
* Collaboration and Sharing

## What is Funckle?
Funckle is a SaaS platform designed to simplify and streamline Speckle automation using reusable functions called deployed as bots . These bots are configured to listen to Speckle Streams, which are real-time data feeds, and perform specific actions based on the data they receive. Whether you're automating repetitive tasks, data processing, or notifications, Funckle makes it easy to harness the capabilities of automation.

## Getting Started
### Signing Up
1. If you don't already have a Speckle account, sign up at https://speckle.xyz/.
2. Click on the "Log In" button in the top right corner of the page.

### Exploring the App
After logging in you will have access to the following resources:

* **Functions**: A library of reusable functions that can be deployed as bots. You can also create your own functions!
* **Streams**: A list of Speckle Streams that you have access to.
* **Bots**: A list of bots that you have deployed. (You will have to access them through the "Streams" page.)

## Creating Your First Bot

### Choosing a Function
From the dashboard, navigate to the [Function Library](/functions).
Browse or search for a function that suits your automation needs.
Click on a function to view details, including its description and usage examples.

### Deploying Your First Bot 🤖
From the dashboard, navigate to the [Streams Page](/streams).
Browse or search for a Stream that suits your automation needs and click on it.
Click on the "New Bot" button in the top right corner of the page.
Fill in the form with the following information:
* **Bot Name**: Provide a name for your bot to distinguish it from others. (eg: "hello-world-bot")
* **Function**: Select the function you want to deploy as a bot. (eg: Antoine's "hello" function)
* **Trigger**: Select the event that will trigger your bot. (eg: "Branch Create" and "Branch Update")
Click "Create Bot" to deploy your bot.
Your bot is now live and actively listening to the stream for trigger events. 🎉🤖🎉

## Managing Your Bots

### Debugging Bots
You can view live logs for the bot from the last hour on the page where your bot is configured.

### Updating and Deleting Bots
Find the Stream that your bot is deployed on in the [Streams Page](/streams).
Click on the Stream to view the list of Bots deployed on it.
Click on the bot you want to manage.
You can update triggers and environment variables/secrets, as well as delete bots, from this page.

## Creating Your Own Functions

Create a new function by downloading the funckle CLI and following the steps below:
1. Install the Funckle CLI 
    \`\`\`console
    pip install funckle
    \`\`\`
2. Create a new function directory
    \`\`\`console
    funckle new <your-function-name>
    \`\`\`
3. Follow the instructions in the new folder (make changes to the function template)
4. Login to Funckle so you can deploy your function. This open a new browser window and after logging in will create a \`.funckle\` file in your home directory to store your credentials
    \`\`\`console
    funckle login
    \`\`\`
5. Deploy your function (run this command from inside the function directory)
    \`\`\`console
    funckle deploy --version <your-function-version>
    \`\`\`
6. Go to the Function page to view you function, check its build status and debug any build logs if necessary.


## Collaboration and Sharing
Funckle encourages collaboration among users:

* **Sharing Functions**: Share your functions with others! All functions are public by default. We might eventually provide capability to make them private if you want to keep them to yourself.

Start automating with Funckle and make your interactions with Speckle Streams more efficient and productive! 🚀
    `


    return (
        <Row>
            <Col span={24}>
                <Card>
                    <ReactMarkdown
                        children={introText}
                        components={{
                            code({ node, inline, className, children, ...props }) {
                                const match = /language-(\w+)/.exec(className || '')
                                return !inline && match ? (
                                    <SyntaxHighlighter
                                        {...props}
                                        children={String(children).replace(/\n$/, '')}
                                        style={dracula}
                                        language={match[1]}
                                        PreTag="div"
                                    />
                                ) : (
                                    <code {...props} className={className}>
                                        {children}
                                    </code>
                                )
                            }
                        }}
                    />
                </Card>
            </Col>
        </Row>

    )
}

export default Index