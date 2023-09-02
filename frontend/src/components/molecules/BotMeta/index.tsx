import React from 'react'
import { Avatar, Card, Space, Typography, Row, Col } from 'antd';
import { ShareAltOutlined } from '@ant-design/icons'

type Props = {
    slug: string,
    imageUrl: string,
    triggers: string[],
    description?: string
}

const BotMeta = (props: Props) => {
    return (
        <Card.Meta
            title={props.slug}
            avatar={<Avatar src={props.imageUrl} />}
            description={
                <Row gutter={16}>
                    <Col>
                        <Space>
                            <Typography.Text>{props.triggers?.length} x</Typography.Text>
                            <ShareAltOutlined />
                        </Space>
                    </Col>
                    <Col>|</Col>
                    <Col>{props.description !== "" ? props.description : "No description :("}</Col>
                </Row>

            }
        />

    )
}

export default BotMeta