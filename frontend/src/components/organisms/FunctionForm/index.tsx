import React from 'react'
import { Typography } from 'antd';

type Props = {}

const FunctionForm = (props: Props) => {

    return (
        <>
            <Typography.Paragraph>Create a new function by downloading the funckle CLI and following the steps below:</Typography.Paragraph>
            <Typography.Paragraph>
                <Typography.Text strong>1. </Typography.Text> Install the Funckle CLI
                <Typography.Text code copyable>pip install funckle</Typography.Text>
            </Typography.Paragraph>
            <Typography.Paragraph>
                <Typography.Text strong>2. </Typography.Text> Create a new function directory
                <Typography.Text code copyable>funckle new FUNCTION_NAME</Typography.Text>
            </Typography.Paragraph>
            <Typography.Paragraph>
                <Typography.Text strong>3. </Typography.Text> Follow the instructions in the new folder (make changes to the function template)
                <Typography.Text code copyable>funckle deploy</Typography.Text>
            </Typography.Paragraph>
            <Typography.Paragraph>
                <Typography.Text strong>4. </Typography.Text> Deploy your function
                <Typography.Text code copyable>funckle deploy</Typography.Text>
                <Typography.Text>(run this command from inside the function directory)</Typography.Text>
            </Typography.Paragraph>
        </>
    )
}

export default FunctionForm